---
status: complete
last_reviewed: 2026-10-28
related:
- engineering/hardware
- theory/model-compression
tags:
- AI hardware
- number formats
- mixed precision
- training
aliases:
  - Mixed-precision training
  - Mixed precision
  - 混合精度訓練
---

# Mixed-Precision Training

Mixed-precision training stores most values and runs most arithmetic in 16-bit floating point, while keeping a single-precision copy of the weights and scaling the loss so that small gradients survive. Micikevicius et al. (2017) report that this reduces the memory used by deep learning models by nearly two times, across several architectures. It is a training technique, and it sits in the [co-design overview](index.md) as the number-format lever for training.

## Problem

Training a network keeps the weights, the activations and the gradients in memory, and each of them is usually stored as a 32-bit float. Memory limits the size of model and batch that fits on a chip, and the bandwidth needed to move 32-bit values limits speed. Storing values in 16 bits halves the bytes moved for each one, but 16-bit values have a smaller range and precision, and training can lose accuracy or become unstable with them.

## Key concepts

- **Half precision:** a 16-bit floating-point format for activations and gradients, with less range and precision than 32-bit.
- **Master weights:** a single-precision copy of the weights, which accumulates the gradient updates after each optimiser step, so small updates are not lost to rounding.
- **Loss scaling:** multiplying the loss by a constant before the backward pass, so that small gradients do not underflow in half precision, and dividing the gradients by the same constant before the weight update.

## Key methods

### Mixed-precision training (Micikevicius et al., 2017)

- **Problem:** 32-bit storage doubles the memory and bandwidth a training step needs, but 16-bit values lose the range and precision that small gradients rely on.
- **Core idea:** keep an FP32 master copy of the weights, run the forward and backward passes in FP16, and scale the loss by a constant before the backward pass.
- **Equations:** the optimiser receives \(g = \tfrac{1}{S}\nabla_\theta(S \cdot L)\) and updates the FP32 master weights, \(\theta \leftarrow \theta - \eta\, g\). The scale \(S\) cancels, so the update matches full-precision training when no value overflows or underflows.
- **Results:** the paper reports nearly a 2× reduction in memory across convolutional, recurrent and generative adversarial networks.
- **Limitations:** the master weights and the optimiser state stay at full precision, so the saving is less than half. The scale must be tuned to avoid overflow.

The 8-bit extension is [FP8](fp8.md). The results and limits are discussed below.

## How it works

Each training step follows these stages:

1. Copy the single-precision master weights into a half-precision copy.
2. Run the forward pass and the backward pass in half precision, with the loss scaled.
3. Undo the loss scaling on the gradients.
4. Apply the update to the single-precision master weights.

The arithmetic and the stored activations run at the lower width, which is where the memory and bandwidth saving comes from. The master weights and the update remain at full width, which keeps small changes from being rounded away.

### Why loss scaling matters: continuous FP16 example

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" tabindex="0" role="region" aria-label="Scrollable FP16 loss-scaling figure">
<img data-source-asset-urls src="../../../assets/concept-animations/fp16-loss-scaling-still.svg" data-motion-src="../../../assets/concept-animations/fp16-loss-scaling-motion.svg" data-still-src="../../../assets/concept-animations/fp16-loss-scaling-still.svg" width="640" height="360" style="display:block;width:640px;min-width:640px;max-width:none;height:auto" alt="A schematic gradient of 2 to the minus 27 rounds to zero on direct IEEE FP16 casting. Multiplying by 1024 produces 2 to the minus 17 in FP16, and unscaling in FP32 restores the gradient." />
</div>

*Original continuous teaching animation, CC BY-SA 4.0.* This **analytical** example uses a gradient $g=2^{-27}\approx7.45\times10^{-9}$, below IEEE binary16's smallest positive subnormal value $2^{-24}$. With round-to-nearest-even, a direct FP16 cast rounds it to **zero** (it is below half the smallest positive subnormal); applying loss scale $S=2^{10}=1024$ **before backpropagation** yields the representable scaled gradient $Sg=2^{-17}$. Converting to FP32 and unscaling gives $g=(Sg)/S=2^{-27}$ for the FP32 optimiser/master-weight update. These values are **not model measurements**. In a real system the scale must also avoid **overflow**, and exact recovery is not guaranteed for arbitrary gradients because of rounding and possible subnormal flushing. The figure isolates a single gradient; it does not imply that all operations in mixed-precision training are FP16. MkDocs provides the existing keyboard-accessible Play/Pause and reduced-motion fallback; on narrow screens, scroll horizontally. [View the SVG animation](../../../assets/concept-animations/fp16-loss-scaling-motion.svg) · [GitHub-readable still](../../../assets/concept-animations/fp16-loss-scaling-still.svg).

### Loss-scale range: rescuing a small gradient can overflow a large one

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" role="region" tabindex="0" aria-label="Scrollable FP16 loss-scale window animation">
<img data-source-asset-urls src="../../../assets/concept-animations/fp16-scaling-window-still.svg" data-motion-src="../../../assets/concept-animations/fp16-scaling-window-motion.svg" data-still-src="../../../assets/concept-animations/fp16-scaling-window-still.svg" width="640" height="360" style="display:block;width:640px;min-width:640px;max-width:none;height:auto" alt="Two synthetic gradients, two to minus twenty-seven and two to five, advance together through exact integer power-of-two loss scales from one to 4096 and back. The current-scale and outcome footer shows small-gradient zero through S equals four, both finite from eight through 1024, and large-gradient overflow from 2048 onward. A dashed purple connector and its moving Δ log₂ = 32 badge expose their invariant 32-exponent gap; separate LOW/HIGH row labels show each rounded FP16 outcome (0, OK or INF) without moving the pre-rounding dots, and a vertical boundary marks the 2^-25 tie-to-zero cutoff. A conditional finite-gradient gate shows STEP ELIGIBLE even when the tiny gradient rounded to zero, but SKIP (INF) when the large gradient overflows." />
</div>

*Original stepwise SVG teaching animation and three-case GitHub fallback, CC BY-SA 4.0.* Consider **two illustrative gradients**, $g_{\mathrm{low}}=2^{-27}$ and $g_{\mathrm{high}}=2^5$, scaled by the same power-of-two $S$ *before* their FP16 representation. Under IEEE binary16 with subnormals and round-to-nearest-even, the minimum positive subnormal is $2^{-24}$ and the largest finite value is **65504**. At $S=1$, the small value rounds to zero; at $S=2^{10}=1024$, the scaled pair is $2^{-17}$ and $2^{15}$, both representable; at $S=2^{12}=4096$, the large value becomes $2^{17}$ and overflows. For these **specific** powers-of-two inputs and scales, **$8\le S\le1024$** is the simultaneous nonzero-finite range, with $S$ restricted to powers of two.

At $S=4$, the tiny value is $2^{-25}$, exactly halfway to the smallest positive subnormal, so round-to-nearest-even still returns zero. At **$S=8$**, it becomes the representable $2^{-24}$; at **$S=2048$**, the large value becomes $2^{16}=65536>65504$ and overflows. The animation visits **integer powers of two only**, and the footer synchronises the exact current $S$ with LOW ZERO, BOTH FINITE or HIGH INF. The moving markers show the exponents of $|Sg|$ on one shared axis. **A purple dashed link and its moving “Δ log₂ = 32” badge translate with both pre-rounding values, explicitly preserving the 32-binary-exponent separation.** Multiplying both values by the same scale leaves their ratio unchanged:

$
\begin{aligned}
\frac{|Sg_{\mathrm{high}}|}{|Sg_{\mathrm{low}}|}
  &= \frac{|g_{\mathrm{high}}|}{|g_{\mathrm{low}}|},\\
\log_2\frac{|g_{\mathrm{high}}|}{|g_{\mathrm{low}}|}
  &= 32.
\end{aligned}
$

A common $S$ shifts both positions equally; it cannot compress the gradient dynamic range. This is why one safe scale must satisfy the lower and upper FP16 limits at once. The left orange band ends at the marked $2^{-25}$ **round-to-zero midpoint**, not at the smallest representable subnormal $2^{-24}$. At the midpoint ties-to-even still gives zero, but values just above it can round *up* to a nonzero subnormal. The plotted circles track **pre-rounding** $|Sg|$; the status footer reports **rounded binary16 outcomes**. New adjacent **LOW/HIGH** indicators reveal each rounded result independently: LOW reads `0` at $S=1$–$4$ and `OK` from $S=8$ onward, whereas HIGH reads `OK` through $S=1024$ and `INF` at $S=2048$–$4096$. `OK` means **nonzero and finite**, not a claim about training quality or numerical accuracy. Thus an invalid rounded value remains explicitly distinguished from its pre-rounding plotted location. The right orange band marks the first overflowing *sampled power of two*, $2^{16}$, rather than a general real-valued overflow threshold. This is **synthetic numerical arithmetic, not measured training performance** or a universal safe loss-scale interval. Actual training distributions vary, some devices flush subnormals to zero, and many operations accumulate in FP32. Loss scaling must be undone before the optimiser update, as explained above. The MkDocs player adds **Previous/Next Step** for the key underflow, finite and overflow boundaries in both directions, continuous seeking for intermediate power-of-two scales, **Play/Pause**, **Restart** (the first scale), and 0.5×/1×/2× speed. Switching tabs pauses playback automatically; it does not resume without another Play action. Controls remain outside the narrow-screen horizontal figure scroller. A synchronized text readout reports the current power-of-two scale, both rounded gradient states and whether the illustrative optimizer step is eligible or skipped. It explicitly identifies a rounded **zero as silent underflow, not an Inf/NaN skip**; stepping and seeking also announce the selection to assistive technology. The keyboard-operable timeline exposes its current schematic loss scale and rounded gradient outcomes as an accessible value instead of only a 0–1000 slider position; the GradScaler timeline similarly exposes its iteration and next scale. The GitHub [static comparison](../../../assets/concept-animations/fp16-scaling-window-still.svg) gives the three exact outcomes, and the [SVG motion](../../../assets/concept-animations/fp16-scaling-window-motion.svg) shows the boundary crossings. Reduced-motion mode displays the static comparison. Switching the system's reduced-motion preference while this page is open updates both teaching timelines without reloading; the static fallbacks remain available.

**Non-finite check versus lost information.** The animated **STEP ELIGIBLE** gate is deliberately different from the numerical-quality status. If these two synthetic gradients were the only inputs to a typical `GradScaler`-style step, $S=1,2,4$ would leave the low gradient silently rounded to zero **but would not trigger an Inf/NaN skip**; the step is eligible despite that lost information. At $S=8$–$1024$, both gradients are finite and the step is eligible. At $S=2048$–$4096$, the large gradient is Inf and the gate displays **SKIP (INF)**, illustrating a non-finite-aware scaler skipping the parameter update. The label **eligible** is a conditional result for these two numbers only, **not proof that an optimiser update actually ran or that training is accurate**; other gradients, accumulation and framework details matter.[^amp-step-gate]

[^amp-step-gate]: PyTorch, [*Automatic Mixed Precision examples*](https://docs.pytorch.org/docs/stable/notes/amp_examples.html), explains that `GradScaler.step` unscales, checks gradients for Inf/NaN and skips the optimizer step if any are detected.

### Dynamic loss scaling: feedback across training iterations

<div class="concept-motion-scroll" style="width:100%;overflow-x:auto" role="region" tabindex="0" aria-label="Scrollable dynamic GradScaler feedback animation">
<img data-source-asset-urls src="../../../assets/concept-animations/gradscaler-feedback-still.svg" data-motion-src="../../../assets/concept-animations/gradscaler-feedback-motion.svg" data-still-src="../../../assets/concept-animations/gradscaler-feedback-still.svg" width="640" height="360" style="display:block;width:640px;min-width:640px;max-width:none;height:auto" alt="A moving focus marker follows six synthetic training iterations. Scale 1024 passes the finite-gradient check on iterations one and two, so the next iteration uses 2048. At 2048 the high gradient overflows, the optimizer step is skipped, and the next scale halves to 1024. The finite-check growth and overflow-backoff cycle repeats for iterations four through six. The STREAK row fills one or two small dots after successful checks or shows a cross for overflow reset; NEXT S shows the next scale, while the animated footer tracks the finite-check count. The full six-step trace remains readable without animation." />
</div>

*Original SVG feedback animation with GitHub-readable non-animated fallback, CC BY-SA 4.0.* This extends the two fixed synthetic gradients above into a **six-iteration thought experiment** about feedback, rather than just a sweep of possible scales. The illustrative settings are `growth_interval=2`, `growth_factor=2`, `backoff_factor=0.5`, and initial scale 1024. The finite-gradient counter resets after overflow. The figure assumes the only gradients examined are the earlier $2^{-27}$ and $2^5$ examples: at 1024 both scaled gradients are finite, while at 2048 the large one overflows. Thus two successful finite checks allow the **next iteration** to use twice the scale, whereas a detected Inf both **skips the current optimizer update** and halves the scale for the **next iteration**.[^dynamic-gradscaler]

| Iteration | Scale used | Finite check | Optimizer step | Next scale |
| --- | ---: | --- | --- | ---: |
| 1 | 1024 | OK | Eligible | 1024 |
| 2 | 1024 | OK | Eligible | 2048 |
| 3 | 2048 | Inf | Skipped | 1024 |
| 4 | 1024 | OK | Eligible | 1024 |
| 5 | 1024 | OK | Eligible | 2048 |
| 6 | 2048 | Inf | Skipped | 1024 |

The chart separates three different states: the curve shows the **current scale**; the `NEXT S` row gives the scale **after** each finite-value check; and the moving footer exposes the **consecutive finite-check streak** that triggers growth or resets on overflow. At t2 the streak reaches 2/2 and grows the next scale to 2048, then t3 detects Inf, skips the update, resets the streak and backs off to 1024. The last `NEXT S=1024` is for the unplotted seventh iteration. The `2/2` label is the growth-triggering count, **before** the counter resets for the next iteration. The **STREAK** strip beneath the scale points gives a GitHub-readable visual trace: one filled dot at t1/t4, two at t2/t5 (growth threshold), and a crossed marker at t3/t6 (overflow/reset). These represent a simplified finite-check counter, **not optimizer progress or loss improvement**. All values are schematic, not measured model gradients.

The timeline plots the scale **used by each iteration**, not the newly computed scale after the check. The last backoff therefore takes effect in an unshown seventh iteration. For comparison, PyTorch's documented **default** growth interval is **2000**, not 2; the shortened interval and repeating Inf pattern exist solely to expose the control loop within six frames. The chart does **not** simulate an actual optimizer, guarantee that every eligible step improves the loss, or represent measured GPU gradients. On MkDocs, **Previous/Next Step** visits each of the six finite checks, the seek slider can select times between checks, and **Play/Pause**, **Restart** (return to t1), and 0.5×/1×/2× speed control the 12-second loop. Tab switching pauses the demonstration without silently advancing through finite checks. On small screens, the figure scrolls horizontally using the keyboard while the controls stay outside the scroller. The same synchronized readout identifies the selected iteration, its **current and next** loss scale, whether the step is **eligible or skipped** under the two-gradient finite check, and the growth or reset decision. These are derived from the fixed teaching example, not real training measurements. Reduced-motion mode and GitHub display the fully labelled static trajectory. [Full SVG animation](../../../assets/concept-animations/gradscaler-feedback-motion.svg) · [GitHub fallback preview](../../../assets/concept-animations/gradscaler-feedback-still.svg).

[^dynamic-gradscaler]: PyTorch, [*Automatic Mixed Precision package — torch.amp*](https://docs.pytorch.org/docs/stable/amp.html), documents the growth/backoff factors, default growth interval and GradScaler scaling policy; [*Automatic Mixed Precision examples*](https://docs.pytorch.org/docs/stable/notes/amp_examples.html) describes the Inf/NaN step-skipping rule.

**Compare two precision states (MkDocs).** Both animations have an independent **Pin A** baseline: select a loss scale or GradScaler iteration, pin it, then use the timeline to inspect **B**. The FP16 comparison reports **both rounded gradient outcomes** (including silent zero underflow), optimizer-step **eligibility**, and the **signed change in scale exponent**; for example, S=1 versus S=2048 switches from a lost finite tiny gradient to a non-finite large gradient, which changes **ELIGIBLE → SKIP**. The GradScaler comparison shows the current and following scale, the **decision-time finite-success count**, the **signed change in next scale**, and whether the synthetic non-finite check would make that iteration eligible or skipped. For example, t1 and t5 are both eligible, but their **NEXT S** differs (**1024** versus **2048**) because their accumulated finite-check streaks differ; this is an iteration-history comparison, not a treatment effect. **Swap A/B** exchanges the pinned and live states, seeks the SVG to the previous A state, and reverses the direction of the outcome/exponent comparison; it does not change the numerical experiment. **Replace A** re-pins the baseline and **Clear A** removes it. These are analytical comparisons of **synthetic examples**, not observed optimizer updates or training results. Controls support mouse and keyboard; reduced-motion and GitHub previews retain their standalone static explanations. The paired gauges visualize three FP16 conditions (scale exponent, whether LOW remains nonzero, whether HIGH remains finite) and two GradScaler state quantities (decision-time streak, next scale), all on **fixed domains shared by A and B**. They are illustrations of the same synthetic readout, not measured gradients or optimizer outcomes.

**Interpret the qualitative transitions.** FP16 A/B now identifies whether the selected synthetic gradients are in a **LOW ZERO**, **BOTH FINITE NONZERO**, or **HIGH INF** regime. These are rounded outcomes for exactly the two illustrated gradients, not a guarantee of safe scaling for a whole model. GradScaler A/B additionally names the next-scale action as **hold**, **grow**, or **backoff**, explicitly separating finite-check history from a single iteration's eligibility. Neither display is a measured optimizer result.

**Guided numerical-boundary cases (MkDocs).** Each diagram's keyboard-accessible **Try a worked comparison…** menu pauses and loads a pinned A and live B. In the FP16 window, **S=4 → 8** crosses the small-gradient zero-rounding boundary while **S=1024 → 2048** crosses the large-gradient overflow boundary; these are distinct failure modes. In the GradScaler controller, **t1 → t5** compares identical finite checks with different *history-dependent* next scales, while **t2 → t3** reveals overflow-triggered backoff after growth. **Swap A/B**, seek and manual pinning still work. All inputs and outputs are constructed examples, not observed training runs. **Sweep A→B** makes the intervening synthetic FP16 scales or GradScaler iterations visible instead of only jumping between endpoints; it takes approximately three seconds at 1×, stops exactly at B, and supports either comparison direction. Playback speed, Pause, seeking and reduced-motion changes still apply. This scan replays prescribed *display states*, **not** a new training run, a measured loss-scale trajectory, or evidence of a causal effect.

**Key-transition navigation (MkDocs):** The FP16 figure exposes four keyboard-focusable boundary buttons: LOW recovery on the rising scale, HIGH overflow, HIGH recovery on the falling scale, and LOW underflow on the falling scale. The GradScaler figure exposes all six `t1–t6` decisions (hold, grow, backoff). Buttons seek to exact prescribed synthetic states and pause playback; they are not new optimizer runs or evidence of a model-wide safe scale. The active FP16 boundary stays visibly selected throughout its complete discrete power-of-two state (on either directional sweep), rather than flashing only near the button's timestamp. **Previous/Next Step** also reaches the descending HIGH-finite (`S=1024`) and LOW-zero (`S=4`) boundaries; a state outside those four specific events leaves the transition strip unselected.

**Keyboard timeline navigation (MkDocs).** Focus either time slider: **Left/Right** moves between actual discrete teaching states—one sampled power-of-two frame on the ascending *or descending* FP16 path, or one `t1–t6` GradScaler check. **Shift+Left/Right** retains native fine-grained seeking, and **Home/End** seeks to the beginning/end. These keys pause playback or A→B Sweep without resetting the pinned baseline, and update the numerical readout and `aria-valuetext`; mouse/touch dragging remains continuous. During continuous scrubbing, the SVG, numerical interpretation and accessible slider state update immediately; the polite status region announces the chosen result only when the user finishes seeking, avoiding repetitive screen-reader announcements. The FP16 end sample repeats the initial power-of-two value and is not a separate nonzero-duration frame.

**Viewport-aware playback (MkDocs).** Each FP16 and GradScaler timeline automatically pauses only when **both** its scrollable figure and its separate controls are outside the visible viewport. Returning does not autoplay it; press **Play** to resume. The pinned A/B baseline is preserved. This avoids unseen animation work and is **not** a numerical or optimiser decision.

**SVG load-failure fallback (MkDocs).** If either animated figure fails to load or receives a non-SVG document, its unusable timeline is hidden and the reviewed still SVG remains visible, with localized alternative text. A page reload can retry a transient asset failure; neither fallback implies measured gradients or a training trace.

**Compare adjacent numerical states (MkDocs).** **Compare previous** pins the preceding sampled scale or iteration as **A**, while the selected state remains **B**; it is disabled at the start. In the FP16 window, use it at rising **S=8** to compare with **S=4** (LOW zero → nonzero), or at falling **S=1024** to compare with the preceding **S=2048** (HIGH Inf → finite). The comparison follows the **time direction**, so it does not conflate rising and falling threshold crossings. In the GradScaler example, using it at **t3** compares with **t2**, showing growth followed by overflow backoff. The pinned comparison, reversible signed differences and paired gauges are schematic rather than recorded training measurements.

## Results

Micikevicius et al. (2017) report that using this approach reduces the memory consumption of deep learning models by nearly two times. They recommend keeping a single-precision copy of the weights that accumulates the gradients after each optimiser step, and scaling the loss to handle the loss of information in half-precision gradients. They tested convolutional, recurrent and generative adversarial networks.

Micikevicius et al. (2022) extend the idea to [8-bit floating-point formats](fp8.md), E4M3 and E5M2. They report that on models up to 175 billion parameters, training with these formats effectively matches the result quality of 16-bit training, with the hyperparameters left unchanged. That result is for training; the lower-precision inference methods covered in [quantisation](../../../theory/model-compression/quantisation/index.md) are a separate line of work.

## Limitations

The saving is less than a full halving of all memory, because the master weights stay in single precision and the optimiser state is not reduced by this method. Half-precision gradients can lose information, which is why loss scaling is needed, and the scale must be chosen so that values neither underflow nor overflow. The paper's experiments cover the architectures listed above, so results on other models need their own checks.

## Open questions

- **How far below 16 bits training can go.** The FP8 results show that 8-bit formats can match 16-bit quality on large models, but which operations and which stages of training tolerate the lower precision is still being worked out.
- **Hardware support.** Whether a chip runs half-precision and 8-bit arithmetic at the speed its memory saving suggests depends on the hardware, which is why the [accelerators](../accelerators/index.md) comparison matters.

## Connections

Mixed precision is one of the three levers in the [co-design overview](index.md). The memory it saves is the cost that [memory hierarchy and bandwidth](../memory-hierarchy/index.md) describes, and the same idea of fewer bits per value appears in the inference side of [quantisation](../../../theory/model-compression/quantisation/index.md). [FlashAttention](../../../theory/models/transformer/attention-variants/flash-attention/index.md) is a kernel that works within the same memory constraints.

## References

### Seminal papers

- Micikevicius, P., et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Shows that 16-bit training reduces memory use by nearly two times across architectures, with master weights and loss scaling.
- Micikevicius, P., et al. (2022). *FP8 Formats for Deep Learning*. arXiv:2209.05433. https://arxiv.org/abs/2209.05433 — Proposes two 8-bit floating-point encodings that match 16-bit training quality on models up to 175 billion parameters.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys the energy and throughput trade-offs of DNN hardware, including hardware–algorithm co-design.

### Articles and documentation

- PyTorch. *Automatic Mixed Precision examples*. https://docs.pytorch.org/docs/stable/notes/amp_examples.html — Describes gradient unscaling and the Inf/NaN check that skips an optimizer step; basis for the illustrative step gate.

- Krishnamoorthi, R. (2018). *Quantizing deep convolutional networks for efficient inference: A whitepaper*. arXiv:1806.08342. https://arxiv.org/abs/1806.08342 — Shows the inference-side counterpart: per-channel 8-bit quantisation keeps many CNNs within 2% of floating-point accuracy.
- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory, rather than compute, has become the primary bottleneck for AI applications, particularly serving, which is the pressure this method relieves.
