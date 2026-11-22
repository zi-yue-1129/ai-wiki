---
status: complete
last_reviewed: 2026-10-28
related:
- engineering/hardware
- engineering/hardware/memory-hierarchy
tags:
- AI hardware
- training
- memory
- activation recomputation
aliases:
  - Gradient checkpointing
  - Activation checkpointing
  - Activation recomputation
  - 梯度檢查點
---

# Gradient Checkpointing

Gradient checkpointing trades computation for memory during training. The forward pass keeps only some intermediate activations, and the backward pass recomputes the rest when they are needed. Chen et al. (2016) show that for a chain of n layers, the memory for stored feature maps can fall to about O(√n), at the cost of roughly one extra forward pass per mini-batch. It sits in the [co-design overview](index.md) next to [mixed-precision training](mixed-precision.md), as a lever that trades one resource for another.

## Problem

Backpropagation needs the activations from the forward pass, so training stores them until the backward pass uses them. For deep networks this storage grows with depth, and it often limits the batch size or model that fits on a device well before compute runs out. Chen et al. report that, before their change, a 1,000-layer residual network trained on ImageNet needed about 48 GB.

## Key concepts

- **Checkpoint:** an activation kept in memory after the forward pass.
- **Segment:** the layers between two checkpoints. Their internal activations are discarded.
- **Recomputation:** rerunning a segment's forward pass during the backward pass, starting from its stored checkpoint, to rebuild the activations needed for that segment's gradients.

## Key methods

### Sublinear-memory checkpointing (Chen et al., 2016)

- **Problem:** backpropagation stores the activations of every layer, so memory grows with depth.
- **Core idea:** store activations only at about √n segment boundaries, and recompute each segment's forward pass during the backward pass.
- **Equations:** for n layers, the stored activations need O(√n) memory, at about one extra forward pass per mini-batch. A recursive variant reaches O(log n) memory at an extra O(n log n) forward computation.
- **Results:** for a 1,000-layer residual network on ImageNet, memory falls from 48 GB to 7 GB at about 30% extra running time.
- **Limitations:** the bound counts stored feature maps, so parameters and optimiser state lie outside it. The extra forward pass slows training, and the computation graph must be split into segments.

## How it works

The paper's √n scheme works as follows:

1. Split the n layers into about √n segments.
2. In the forward pass, store only the outputs at the segment boundaries, and discard every other activation.
3. In the backward pass, go from the last segment to the first. For each segment, rerun its forward pass from the stored boundary, compute its gradients, and then free its activations.

The stored feature maps then take about √n boundary tensors, plus the activations of the largest segment while it is being recomputed. That gives O(√n) memory, at the cost of about one extra forward pass per mini-batch.
The paper also describes a recursive version, in which each segment is handled by the same strategy. Memory then grows as O(log n), but the extra forward computation rises to O(n log n), which is far more expensive than the √n scheme.

### Activation storage and recomputation: animated walkthrough

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="Scrollable activation-checkpointing figure">
<img data-source-asset-urls src="../../../assets/concept-animations/checkpoint-recompute-still.svg" data-motion-src="../../../assets/concept-animations/checkpoint-recompute-motion.svg" data-still-src="../../../assets/concept-animations/checkpoint-recompute-still.svg" width="640" height="360" style="display:block;width:640px;min-width:640px;max-width:none;height:auto" alt="Eight layers yield activations A0 to A8. A0, A4, and A8 remain as checkpoints, while the internal activations of each segment are reconstructed just before its backward pass." />
</div>

*Original continuous teaching animation, CC BY-SA 4.0.* The illustrative eight-layer chain keeps boundary tensors **A0, A4 and A8** (cyan). After the forward sweep, each segment's discarded internal activations (amber) are reconstructed from its preceding checkpoint, starting with **A5–A7** and then **A1–A3** during the reverse traversal. The amber cursor recomputes each segment forward before the violet cursor performs its backward traversal; temporary internal activations are released after that segment finishes. The violet cursor represents **backward processing**, not an optimisation step. Three persistent boundary tensors out of nine are shown **only as a schematic storage example**, not as peak device memory: temporary recomputation buffers, gradients, parameters and optimiser states also occupy memory. On MkDocs, the existing Play/Pause button supports keyboard operation and reduced-motion preferences; the image can scroll horizontally on narrow displays. [View the complete SVG animation](../../../assets/concept-animations/checkpoint-recompute-motion.svg) · [GitHub-readable still](../../../assets/concept-animations/checkpoint-recompute-still.svg).

### Choosing checkpoint intervals: the memory trade-off

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" role="region" tabindex="0" aria-label="Scrollable checkpoint-spacing animation">
<img data-source-asset-urls src="../../../assets/concept-animations/checkpoint-spacing-still.svg" data-motion-src="../../../assets/concept-animations/checkpoint-spacing-motion.svg" data-still-src="../../../assets/concept-animations/checkpoint-spacing-still.svg" width="640" height="360" style="display:block;width:640px;min-width:640px;max-width:none;height:auto" alt="For sixteen equal-size layers, the live KEEP and REBUILD counters change as segment length steps from 1 to 16: five persisted boundaries plus three rebuilt internal activations give eight peak slots at s equals four; the TOTAL REBUILT readout shows twelve internal activations reconstructed across all four segments. An amber bracket, a growing replay trace, and orange activation dots appearing one by one behind the cursor show forward reconstruction in the final segment (none at s equals one), while a live equation adds KEEP and REBUILD to produce PEAK SLOTS. The five totals form a U-shaped schematic curve." />
</div>

*Original computational SVG animation and GitHub-safe comparison, CC BY-SA 4.0.* For a **constructed chain of 16 equal-size layers**, let the segment length $s$ divide 16. Keep boundary activations $A_0,A_s,\ldots,A_{16}$ until backward processing needs them, and rebuild at most $s-1$ discarded internal activations for one segment. In this deliberately simplified retention model, the maximum simultaneous *activation slots* is

$$
M(s)=\left(\frac{16}{s}+1\right)+(s-1)=\frac{16}{s}+s.
$$

At $s=1,2,4,8,16$, the persistent checkpoint counts are **17, 9, 5, 3, 2**, the temporary internal counts are **0, 1, 3, 7, 15**, and the peak totals are **17, 10, 8, 10, 17**. Thus $s=4$ minimizes this *five-choice example*, illustrating the square-root balance described by Chen et al. (2016), already listed in References. It is **not a GPU peak-memory measurement**: it excludes gradients, parameters, optimiser state, unequal activation sizes, allocator effects, and the compute-time cost of replaying segments. The optimum can change for a nonuniform graph.

The animated **TOTAL REBUILT** readout makes the separate recomputation cost visible. If each segment reconstructs its $s-1$ internal activations once during the backward sweep, the cumulative number of recreated internal activation tensors across the 16-layer chain is

$$
B(s)=\frac{16}{s}(s-1)=16-\frac{16}{s}.
$$

For $s=1,2,4,8,16$, this gives **0, 8, 12, 14, 15** rebuilt tensors in total. The **REBUILD** bar instead counts the *maximum simultaneously live temporary slots in one segment* (**0, 1, 3, 7, 15**). Neither number is a measured FLOP count or runtime: real recomputation can execute additional layer operations and incur framework-specific overhead. This is an illustrative storage-versus-recreation comparison, not a benchmark.

The animation changes the checkpoint boundaries, the stored/rebuilt slot counts, and the active point on the cost curve together. **An amber bracket highlights only the last segment currently being replayed**: at $s=4$, it spans four layers, while the REBUILD count of three refers to the internal activations temporarily needed for that one segment. At $s=1$ every layer boundary is retained, so the bracket disappears: no internal activations are replayed. An amber cursor now sweeps from left to right along the bracket during each nontrivial segment size, indicating forward recomputation **inside one segment**, not a simultaneous replay of all segments or a backward-gradient cursor. The bracket, growing trace and cursor are spatial/temporal explanations, not additional activation allocations. The orange trace fills only the active segment as the forward replay cursor advances, resetting for each segment-length choice; it does not represent the total number of tensors rebuilt across all segments. **Small amber dots now appear at internal boundaries only after the replay cursor passes them**: there are three temporary reconstructed boundaries at $s=4$, fifteen at $s=16$, and none at $s=1$. These are **recreated temporary activations**, not newly retained checkpoints; the teal dots remain the persistent boundaries. **The live KEEP and REBUILD counters, together with the new PEAK SLOTS addition equation, expose the decomposition at each step**: at $s=4$, five persistent boundaries plus three temporary internal activations yield eight peak slots. These counters refer to activation tensors, not bytes or measured GPU memory. On MkDocs, **Previous/Next Step** selects the five segment sizes, the seek slider reveals intermediate forward replay, and **Play/Pause**, **Restart** (return directly to the first spacing choice), and 0.5×/1×/2× speed control the sequence. Switching to another browser tab automatically pauses the animation so intermediate replay states are not silently skipped; returning does not resume it automatically. The controls stay outside the horizontally scrollable figure on narrow screens. A bilingual synchronized readout beneath the controls distinguishes the **peak temporary slots in one segment** from **TOTAL REBUILT across all segments** and tracks reconstructed activations within the highlighted final segment; these are **illustrative tensor counts, not measured GPU memory or FLOPs**. Seeking or using Previous/Next Step also announces the selected state to assistive technology. The timeline slider itself exposes the current illustrative spacing and peak/rebuild counts as its accessible value rather than an arbitrary 0–1000 position. Reduced-motion users see the $s=4$ state, while the GitHub fallback compares **all five** choices without JavaScript. Switching the system's reduced-motion preference while this page is open changes between the still fallback and interactive timeline without requiring a reload. Focus the figure region to scroll with the keyboard. [GitHub static comparison](../../../assets/concept-animations/checkpoint-spacing-still.svg) · [Animated SVG](../../../assets/concept-animations/checkpoint-spacing-motion.svg).

**Compare two checkpoint choices (MkDocs).** Use **Pin A** to freeze the current spacing as a baseline, then seek or step to another spacing, **B**. The A/B comparison reports both **PEAK** (simultaneous illustrative activation slots) and **TOTAL REBUILT** (all reconstructed internal boundaries), plus signed **B − A** differences. For example, from s=1 to s=4, peak slots decrease **17 → 8** while total reconstructed boundaries increase **0 → 12**; this is a *memory-versus-recomputation trade-off*, not measured GPU usage or wall-clock time. **Swap A/B** exchanges the pinned baseline and the current timeline state, so the signed **B − A** deltas reverse (s=4 versus s=1 changes ΔPEAK from −9 to +9 and ΔTOTAL REBUILT from +12 to −12). **Replace A** updates the baseline, and **Clear A** removes the comparison. Buttons work with keyboard focus and Enter; the comparison is hidden in reduced-motion mode, where the GitHub-readable still gives all five choices. The paired A/B bar gauges now animate the two trade-off quantities on **fixed, shared domains** (PEAK 0–17 illustrative slots, TOTAL REBUILT 0–15), so visual bar lengths remain comparable before and after swapping; the adjacent numbers are the exact values, not GPU measurements.

**Interpret the A/B verdict.** The synchronized comparison now distinguishes a memory–recomputation **trade-off** from **equal aggregate costs** and **dominance on both illustrated costs**. For example, `s=8` (PEAK 10, TOTAL REBUILT 14) is dominated by `s=4` (PEAK 8, TOTAL REBUILT 12) in this equal-activation, two-metric toy model. It does **not** establish an optimal real-world checkpoint schedule; tensor lifetimes, recomputation FLOPs and runtime overhead are excluded.

## Results

The abstract reports that, for a 1,000-layer residual network on ImageNet, memory falls from about 48 GB to 7 GB, with roughly 30% more running time. The body reports that its ResNet experiments used batch size 32, 224 × 224 inputs, MXNet on a single Titan X GPU, and counted each conv-bn-relu block as one layer. The abstract also reports a significant memory reduction when training complex recurrent networks.

## Limitations

- **Runtime cost.** The measured running time rose by about 30%. The backward pass costs about twice the forward pass, so recomputing the forward pass adds a large share of the work.
- **Framework support.** The computation graph must be split into segments, so frameworks without that support need custom training loops.
- **Scope of the saving.** The √n bound counts stored feature maps. Parameters and optimiser state lie outside it.

## Open questions

- **Choosing segments automatically.** Where the boundaries go depends on per-layer memory costs. How well a good choice holds for irregular graphs is not settled by this paper, whose abstract describes experiments on ImageNet residual networks and complex recurrent networks.
- **Combining with other memory savers.** How recomputation combines with lower-precision storage and with offloading to host memory is outside this paper, and it is where most practical training systems now operate.

## Connections

Checkpointing and [mixed-precision training](mixed-precision.md) are complementary. Mixed precision shrinks each stored value, while checkpointing stores fewer values and recomputes the rest. The trade is useful when memory capacity, not compute, limits training. Whether a given recomputation pays off depends on the balance described in [memory hierarchy and bandwidth](../memory-hierarchy/index.md) and [the roofline model](../memory-hierarchy/roofline.md).

## References

### Seminal papers

- Chen, T., Xu, B., Zhang, C. & Guestrin, C. (2016). *Training Deep Nets with Sublinear Memory Cost*. arXiv:1604.06174. https://arxiv.org/abs/1604.06174 — Stores only segment-boundary activations and recomputes the rest during the backward pass, reducing memory to O(√n) at about one extra forward pass.
- Micikevicius, P., et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Shrinks each stored value to 16 bits, a memory lever that complements storing fewer values.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys the energy and throughput of DNN hardware, the efficiency concerns behind the trade-off this page describes.

### Articles and documentation

- Ivanov, A., et al. (2020). *Data Movement Is All You Need: A Case Study on Optimizing Transformers*. arXiv:2007.00072. https://arxiv.org/abs/2007.00072 — Argues that data movement is the key bottleneck when training transformers, which is the cost checkpointing trades against.
- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory, rather than compute, has become the primary bottleneck for AI applications, particularly serving, the same pressure that makes recomputation attractive.
