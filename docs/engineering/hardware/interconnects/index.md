---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- engineering/distributed-training
- theory/models/transformer
tags:
- AI hardware
- interconnects
- collective communication
- scaling
- NVLink
- InfiniBand
aliases:
  - Interconnects
  - Interconnect and scaling
  - Collective communication
  - 互連與擴展
---

# Interconnects and Scaling

Once a model no longer fits on one accelerator, the speed of a single chip matters less than the links between chips. Training and serving then split weights, activations and gradients across many devices, and the bandwidth and latency of the links set how much of that work can run in parallel. Interconnects form a hierarchy much like memory: very fast links inside a package or server, and slower links across racks and clusters. This page is a subchapter of [AI Hardware](../index.md). It covers the link tiers, the collective operations that use them, and how the parallelism strategy decides what crosses each link.

## Problem

When a matrix multiplication is sharded across chips, some of the data it needs lives on other chips, whether partial sums, activations or gradients. Moving that data can take longer than computing with it. The parallel layout therefore has to keep the heavy traffic on the fastest links and overlap the rest with computation.

## Core idea

Links come in tiers, and each tier sets the scope of the parallelism that can run on it efficiently:

| Tier | Examples | Typical scope |
|---|---|---|
| Within a server or rack-scale domain | NVLink and NVSwitch in GPU systems | A group of GPUs with very high bandwidth between any pair |
| Within a pod or slice | Inter-chip interconnect (ICI) in TPU systems, arranged as a 3D torus | A TPU slice or pod |
| Between servers | InfiniBand, or Ethernet with RDMA (RoCE) | A cluster, at lower bandwidth per chip |

Parallel work is usually split so that the most frequent communication stays in the fastest tier. Tensor parallelism exchanges data inside every layer and so needs the fastest links, while data parallelism exchanges gradients once per step and tolerates slower ones.

Collective operations describe the common communication patterns. All-reduce sums values across chips and gives every chip the result. All-gather collects shards onto every chip, and reduce-scatter sums values and leaves each chip with one shard. All-to-all sends a different piece to every other chip, which is the pattern that routes tokens to experts in a mixture-of-experts model.

## Equation or algorithm

A ring all-reduce arranges the chips in a cycle. It runs as a reduce-scatter followed by an all-gather, and each chip sends and receives a fraction of the data in every step. Patarasuk and Yuan show that this is bandwidth-optimal, and the per-chip bandwidth cost is then

\[
T \approx \frac{2(N-1)}{N} \cdot \frac{S}{B}
\]

where \(N\) is the number of chips, \(S\) the size of the data on each chip and \(B\) the bandwidth of the link. The factor \(2(N-1)/N\) approaches two as \(N\) grows, so the per-chip traffic stays nearly constant as the cluster grows. Latency is ignored here, and it matters for small messages. If the communication is perfectly overlapped with computation, the step time is the larger of the two rather than their sum.

Parallelism strategies differ in what they send. Data parallelism all-reduces gradients once per step. Tensor parallelism all-reduces activations inside each layer, which is frequent and needs fast links. Pipeline parallelism sends activations only between neighbouring stages, which is much less data. Sharded data parallelism, as in ZeRO and FSDP, all-gathers parameters before use and reduce-scatters gradients after it.

## Results

Jouppi et al. (2023) describe the TPU v4 pod, which uses optical circuit switches to reconfigure its interconnect topology. They report that the switches and their optical components are under 5% of system cost and under 3% of system power. For similar-sized systems, TPU v4 is 1.2 to 1.7 times faster and uses 1.3 to 1.9 times less power than the Nvidia A100.

Shoeybi et al. (2019) train an 8.3 billion parameter transformer on 512 GPUs with 76% scaling efficiency, by splitting each layer across GPUs. Rajbhandari et al. (2019) show that ZeRO eliminates memory redundancy in data- and model-parallel training while keeping communication volume low. Narayanan et al. (2021) combine tensor, pipeline and data parallelism to train a model with one trillion parameters on 3072 GPUs. They note that naive use of these methods becomes costly because of expensive cross-node communication.

## Limitations

Bandwidth figures differ across generations and vendors, and they are often quoted per direction, per link or per chip, so they are not directly comparable. Topology matters as well: a torus, a switched fabric and a tree give different collective costs at the same nominal bandwidth. The bandwidth model above ignores latency and contention, and real scaling efficiency also depends on overlap, load balance and failures, which become more frequent at large scale.

## Open questions

- **How far a fast domain can grow.** The point at which a tightly coupled group should be split across slower links depends on the workload. Optical switching, as in TPU v4, is one answer to making larger domains cheap.
- **Expert routing.** The all-to-all traffic from [mixture-of-experts](../../../theory/models/mixture-of-experts/index.md) routing is a different pattern from all-reduce, and it can be harder to overlap with computation.
- **Smaller messages.** Lower-precision gradients and activations reduce traffic; see [quantisation](../../../theory/model-compression/quantisation/index.md).
- **Related:** the [memory hierarchy](../memory-hierarchy/index.md) follows the same logic inside a chip, where bandwidth between levels decides speed.

## Connections

The training side of this topic is covered in [distributed training](../../distributed-training/index.md), including [ZeRO](../../distributed-training/zero.md), [Megatron tensor parallelism](../../distributed-training/megatron-tensor-parallelism.md), [FSDP](../../distributed-training/fsdp.md) and [GPipe](../../distributed-training/gpipe.md). The pod design of the [TPU](../accelerators/tpu/index.md) is the hardware counterpart of the topologies discussed here.

## References

### Seminal papers

- Jouppi, N. P., et al. (2023). *TPU v4: An Optically Reconfigurable Supercomputer for Machine Learning with Hardware Support for Embeddings*. arXiv:2304.01433. https://arxiv.org/abs/2304.01433 — Describes optical circuit switching for reconfiguring the TPU v4 network and reports its speed and power against the A100.
- Shoeybi, M., et al. (2019). *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. arXiv:1909.08053. https://arxiv.org/abs/1909.08053 — Shows intra-layer model parallelism training an 8.3 billion parameter transformer on 512 GPUs at 76% scaling efficiency.
- Rajbhandari, S., et al. (2019). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. arXiv:1910.02054. https://arxiv.org/abs/1910.02054 — Eliminates memory redundancy in data- and model-parallel training while keeping communication volume low.
- Narayanan, D., et al. (2021). *Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM*. arXiv:2104.04473. https://arxiv.org/abs/2104.04473 — Combines tensor, pipeline and data parallelism for one-trillion-parameter training and discusses the cost of cross-node transfer.
- Sergeev, A. and Del Balso, M. (2018). *Horovod: fast and easy distributed deep learning in TensorFlow*. arXiv:1802.05799. https://arxiv.org/abs/1802.05799 — Uses ring reduction for efficient inter-GPU communication in data-parallel training.
- Patarasuk, P. and Yuan, X. (2009). *Bandwidth optimal all-reduce algorithms for clusters of workstations*. Journal of Parallel and Distributed Computing 69, 117–124. https://doi.org/10.1016/j.jpdc.2008.09.002 — Shows that the ring all-reduce is bandwidth-optimal, the basis of the cost formula above.
