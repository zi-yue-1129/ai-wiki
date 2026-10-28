---
status: draft
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

## How it works

The paper's √n scheme works as follows:

1. Split the n layers into about √n segments.
2. In the forward pass, store only the outputs at the segment boundaries, and discard every other activation.
3. In the backward pass, go from the last segment to the first. For each segment, rerun its forward pass from the stored boundary, compute its gradients, and then free its activations.

The stored feature maps then take about √n boundary tensors, plus the activations of the largest segment while it is being recomputed. That gives O(√n) memory, at the cost of about one extra forward pass per mini-batch. When layers have very different memory costs, the paper uses a greedy planner under a memory budget, and it searches over the budget to choose the split.

The paper also describes a recursive version, in which each segment is handled by the same strategy. Memory then grows as O(log n), but the extra forward computation rises to O(n log n), which is far more expensive than the √n scheme.

## Results

The abstract reports that, for a 1,000-layer residual network on ImageNet, memory falls from about 48 GB to 7 GB, with roughly 30% more running time. The body gives the setting: batch size 32, 224 × 224 inputs, MXNet on a single Titan X GPU, and each conv-bn-relu block counted as one layer. The abstract also reports large memory savings when training recurrent networks on very long sequences.

## Limitations

- **Runtime cost.** The measured running time rose by about 30%. The backward pass costs about twice the forward pass, so recomputing the forward pass adds a large share of the work.
- **Framework support.** The computation graph must be split into segments. Users either set the recomputation count for each node or rely on the planner, and frameworks without this support need custom training loops.
- **Scope of the saving.** The reported memory covers feature maps and gradients only. It does not cover parameters, optimiser state or temporary buffers such as convolution workspace.
- **Constant-factor optimisations.** The in-place and memory-sharing optimisations in the paper reduce memory only by a constant factor, and they work only when the graph declares its dependencies minimally.
- **Failure cases.** The paper does not describe cases where the scheme fails to help.

## Open questions

- **Choosing segments automatically.** The planner depends on per-layer memory costs and a budget. How well its choices hold for irregular graphs is not settled by this paper, whose experiments the abstract describes as residual and recurrent networks.
- **Combining with other memory savers.** How recomputation combines with lower-precision storage and with offloading to host memory is outside this paper, and it is where most practical training systems now operate.

## Connections

Checkpointing and [mixed-precision training](mixed-precision.md) are complementary. Mixed precision shrinks each stored value, while checkpointing stores fewer values and recomputes the rest. The trade is useful when memory capacity, not compute, limits training. Whether a given recomputation pays off depends on the balance described in [memory hierarchy and bandwidth](../memory-hierarchy/index.md) and [the roofline model](../memory-hierarchy/roofline.md).

## References

### Seminal papers

- Chen, T., Xu, B., Zhang, C. & Guestrin, C. (2016). *Training Deep Nets with Sublinear Memory Cost*. arXiv:1604.06174. https://arxiv.org/abs/1604.06174 — Stores only segment-boundary activations and recomputes the rest during the backward pass, reducing memory to O(√n) at about one extra forward pass.
- Micikevicius, P., et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Shrinks each stored value to 16 bits, a memory lever that complements storing fewer values.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys how reusing data in local storage reduces the energy cost of moving it, the same trade-off this page describes.

### Articles and documentation

- Ivanov, A., et al. (2020). *Data Movement Is All You Need: A Case Study on Optimizing Transformers*. arXiv:2007.00072. https://arxiv.org/abs/2007.00072 — Argues that data movement is the key bottleneck when training transformers, which is the cost checkpointing trades against.
- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is the primary bottleneck for AI serving, the same pressure that makes recomputation attractive.
