---
related:
- theory/models/transformer
tags:
- engineering
- systems
aliases:
- 分散式訓練
---

# Distributed Training

Distributed training spreads the work of training one model across many accelerators. It is needed when a model's weights, gradients and optimizer state do not fit on one device, or when training would take too long on one device. The engineering problem is to split computation and memory while keeping communication between devices from dominating run time.

## Overview

Training a large model needs three kinds of memory on every device: the weights, the gradients, and the optimizer state. With mixed-precision Adam, the state alone costs about 16 bytes per parameter, so a model with a few billion parameters can exceed the memory of one accelerator before any activations are stored. Distributed training answers this in two ways: replicate the model and split the data, or split the model itself.

## Key concepts

- **Data parallelism (DP)**: every device holds a full copy of the model and processes a different slice of each batch. Gradients are averaged with an all-reduce before each update.
- **Tensor parallelism (TP)**: individual matrix multiplications are split across devices, so each holds part of every layer. It needs fast links between devices, usually inside one node.
- **Pipeline parallelism (PP)**: consecutive groups of layers live on different devices, and micro-batches flow through them like an assembly line. The idle time at the start and end of each step is the *pipeline bubble*.
- **Sequence and context parallelism**: long sequences are split along the token dimension, so attention and activations fit in memory.
- **Expert parallelism**: in mixture-of-experts models, different experts live on different devices and tokens are routed to them, so the all-to-all exchange of tokens becomes the main communication cost.
- **Sharding (ZeRO, FSDP)**: data parallelism in which optimizer state, gradients or parameters are partitioned across the data-parallel group, and gathered only when needed.
- **Collective communication**: all-reduce, all-gather and reduce-scatter. For a ring all-reduce of $S$ bytes across $N$ devices, each device sends about $2\frac{N-1}{N}S$ bytes, so the cost is nearly independent of $N$ but depends strongly on bandwidth.

## How it works

Memory and communication decide the strategy. A common recipe in large runs is to combine them:

```mermaid
flowchart TD
  G[GPUs] --> T[Tensor parallel inside a node: fast NVLink]
  T --> P[Pipeline parallel across nodes]
  P --> D[Data parallel with sharded optimizer across replicas]
  D --> S[Sequence parallel for long contexts]
```

The inner dimensions need the most bandwidth, so they stay within a node. Outer dimensions, which exchange less data, can cross slower networks. The right mix depends on model size, sequence length and interconnect; the bandwidth limits behind this are covered in [AI Hardware](../hardware/index.md).

## Key methods

### Megatron-LM tensor parallelism (Shoeybi et al., 2019)

- **Problem:** a transformer layer's weight matrices could not fit on one GPU, and data parallelism alone did not reduce per-device memory.
- **Core idea:** split each MLP block's first weight matrix by columns and the second by rows, so the two halves combine with a single all-reduce per block. Attention is split by heads in the same way.
- **Equation or algorithm:** for $Y = \mathrm{GeLU}(XA)$ with $A = [A_1, A_2]$ split by columns, each device computes $\mathrm{GeLU}(XA_i)$ on its own, and the next matrix is split by rows so that the partial results sum in one reduction.
- **Results:** the paper reports training multi-billion-parameter language models on hundreds of GPUs, with scaling that stays close to linear for that size of model.
- **Limitations:** the communication pattern assumes fast intra-node links; tensor parallelism across slow networks is costly.

### ZeRO: partitioning optimizer state, gradients and parameters (Rajbhandari et al., 2020)

- **Problem:** data parallelism replicates all model state on every device, so the memory per device does not shrink as more devices are added.
- **Core idea:** partition the state across the data-parallel group in three stages. Stage 1 shards the optimizer state, stage 2 also shards gradients, and stage 3 also shards parameters, which are gathered layer by layer when needed.
- **Equation or algorithm:** with $\Psi$ parameters, $N_d$ data-parallel devices and Adam in mixed precision (about $K = 12$ bytes of optimizer state per parameter), the paper's per-device memory is $(4 + \tfrac{12}{N_d})\Psi$ bytes for stage 1, $(2 + \tfrac{14}{N_d})\Psi$ for stage 2, and $\tfrac{16}{N_d}\Psi$ for stage 3.
- **Results:** the paper reports training models of more than a hundred billion parameters on large clusters, with memory reduction that scales with the number of devices.
- **Limitations:** stage 3 adds all-gather traffic in both forward and backward passes, so communication cost rises as memory falls.

### GPipe: pipeline parallelism with micro-batches (Huang et al., 2019)

- **Problem:** a model too large for one device cannot be placed on one device, and a single batch leaves the other stages idle while one stage works.
- **Core idea:** split the network into $K$ sequential stages on $K$ devices, divide each mini-batch into $M$ micro-batches, and pipeline them so that several stages work at once. Gradients are accumulated and the optimizer step is taken once per batch, which keeps the training semantics of synchronous SGD.
- **Equation or algorithm:** the idle fraction, or bubble, is approximately $\frac{K-1}{M+K-1}$, so more micro-batches make the pipeline more efficient.
- **Results:** the paper reports near-linear speedup with more accelerators for very large image models, the setting in which it was evaluated.
- **Limitations:** the bubble grows when $M$ is small, and activations for every in-flight micro-batch must be kept, which motivated later schedules such as 1F1B.

### PyTorch FSDP (Zhao et al., 2023)

- **Problem:** data-parallel sharding, as in ZeRO, has to be practical inside a mainstream deep-learning framework, with minimal changes to user code.
- **Core idea:** wrap each module in a sharded unit, store its flattened parameters across devices, all-gather them just before use, and free them afterwards. Prefetching overlaps the all-gather with computation.
- **Equation or algorithm:** each sharded unit performs an all-gather of its parameters in the forward pass and again in the backward pass, followed by a reduce-scatter of gradients.
- **Results:** the paper reports memory and throughput results for large transformer models on many GPUs, and documents the design trade-offs that affect performance.
- **Limitations:** unit boundaries and prefetch settings strongly affect throughput, so tuning is needed for each model.

## Connections

- Optimizer and learning-rate choices in large batches are covered in [Training & Fine-tuning](../training/index.md).
- Interconnects and memory bandwidth set what communication pattern is affordable: see [AI Hardware](../hardware/index.md).
- Serving a sharded model follows different constraints, covered in [Inference optimization](../inference-optimization/index.md).
- Mixture-of-experts layers add expert parallelism to the mix, so they connect this page to the architecture material under [Transformer](../../theory/models/transformer/index.md).

## Applications

- **Pre-training frontier language models**: combinations of tensor, pipeline and data parallelism across thousands of accelerators.
- **Fine-tuning models that do not fit on one GPU**: sharded data parallelism with FSDP or DeepSpeed ZeRO is the usual route.
- **Vision and multimodal training**: data parallelism with gradient all-reduce is often enough when the model fits on one device.

## Open questions

- **Communication versus compute**: overlapping communication with computation works well on fast networks, but not always on slow ones.
- **Fault tolerance**: long runs across thousands of devices fail often, so checkpointing and restart strategy matter as much as speed.
- **Load balance**: pipeline stages and expert routing can be uneven, which wastes devices.
- **More variants**: sequence-parallel attention schemes, asynchronous updates and automatic parallelism planners each trade simplicity against efficiency.

## References

### Seminal papers

- Shoeybi, M. et al. (2019). *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. https://arxiv.org/abs/1909.08053 — Introduces intra-layer tensor parallelism for transformers that needs one all-reduce per block.
- Rajbhandari, S. et al. (2020). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. SC 2020. https://arxiv.org/abs/1910.02054 — Partitions optimizer state, gradients and parameters across data-parallel devices to cut per-device memory.
- Huang, Y. et al. (2019). *GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism*. NeurIPS 2019. https://arxiv.org/abs/1811.06965 — Pipelines micro-batches across model partitions and analyses the resulting bubble overhead.
- Li, S. et al. (2020). *PyTorch Distributed: Experiences on Accelerating Data Parallel Training*. VLDB 2020. https://arxiv.org/abs/2006.15704 — Describes the design of PyTorch's data-parallel training, including gradient bucketing that overlaps communication with computation.
- Zhao, Y. et al. (2023). *PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel*. VLDB 2023. https://arxiv.org/abs/2304.11277 — Documents the design of fully sharded data parallelism inside PyTorch and its performance trade-offs.

### Surveys and systems papers

- Narayanan, D. et al. (2021). *Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM*. SC 2021. https://arxiv.org/abs/2104.04473 — Combines tensor, pipeline and data parallelism and studies how to map them onto GPU clusters.
