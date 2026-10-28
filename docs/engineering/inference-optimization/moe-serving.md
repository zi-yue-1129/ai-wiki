---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/mixture-of-experts
  - engineering/inference-optimization
  - engineering/hardware
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - MoE serving
  - Mixture-of-experts inference
  - 混合專家模型服務
---

# Serving Mixture-of-Experts Models

!!! info "Part of Inference Optimization"
    This page sits under [Inference Optimization](index.md). It compares the serving problems that mixture-of-experts models create; the architecture itself is covered in the [mixture-of-experts theory pages](../../theory/models/mixture-of-experts/index.md), and each named method has its own page.

A mixture-of-experts (MoE) model routes each token to a small number of expert sub-networks, so only a fraction of its parameters is active for any token. This makes computation cheaper per token than in a dense model of the same total size. The serving problem changes, though, because all the experts must still be stored, and the tokens in a batch are spread across experts that may live on different devices.

## Overview

An MoE model separates two numbers. The total parameter count sets the memory needed to hold the model. The active parameter count sets the computation per token. Serving is limited by memory when the model is large, and by communication when the experts are spread over many devices. A design that puts all experts on one GPU is simple but limits the model size. Spreading them across GPUs requires moving tokens to the experts and back, which adds communication to every layer.

## Key concepts

- **Expert parallelism.** Placing different experts on different devices, so that each device holds a subset of the experts and tokens are sent to the device that holds their expert.
- **Load balance.** The routing may send most tokens to a few experts. Overloaded experts slow the whole layer, because the layer waits for the slowest device.
- **Memory footprint versus active parameters.** The model must fit in memory by its total size, while its speed follows its active size.
- **Expert offloading.** Keeping inactive experts in host memory or on disk and loading them when they are needed.

## How it works

For each MoE layer, a router chooses the experts for each token. The tokens are grouped by expert and sent to the devices that hold those experts. Each expert processes its tokens, and the outputs are returned and combined.

```mermaid
flowchart LR
  T[Tokens in a batch] --> R[Router chooses experts]
  R --> A[All-to-all: send tokens to expert devices]
  A --> E[Experts compute on their devices]
  E --> B[All-to-all: return outputs]
  B --> C[Combine outputs for each token]
```

The two all-to-all communication steps are the cost that expert parallelism adds. Their size depends on the batch and on how evenly the router spreads tokens.

## Key methods

Each named method has its own page. The table compares them.

| Method | Problem it addresses | Core idea | Main trade-off | Page |
|---|---|---|---|---|
| GShard | A model with many experts must be sharded across devices by hand | Annotate the model and let the compiler shard the experts across devices | Needs the sharding annotations and a capable compiler | [GShard](gshard.md) |
| DeepSpeed-MoE | MoE models are costly to serve, both in memory and in latency | Compress the model and use an inference system built for MoE layers | Gains depend on the compression and the system being used | [DeepSpeed-MoE](deepspeed-moe.md) |
| Expert offloading | A large MoE model does not fit in the memory of a single device | Keep inactive experts off the device and load them on demand | Loading adds latency when the router needs an expert that is not resident | [Expert offloading](expert-offloading.md) |

## Results

The three methods are reported on different hardware and models, so their results are not comparable. GShard reports training a sparsely gated MoE model beyond 600 billion parameters with automatic sharding. DeepSpeed-MoE reports model compression that reduces MoE size by up to 3.7 times, and an inference system with 7.3 times better latency and cost than existing MoE inference solutions. Expert offloading reports running Mixtral-8x7B with mixed quantisation on desktop hardware, without giving speed figures in its abstract.

## Trade-offs

- **Locality versus memory.** Keeping all experts on the device is fast but limits the model size. Offloading fits a larger model but adds loading latency.
- **Balance versus accuracy.** Forcing an even spread of tokens across experts can change the model's outputs, so balancing is a trade-off with the routing.
- **Communication versus compute.** Expert parallelism adds all-to-all traffic to every layer. With small batches the traffic can cost more than the compute it saves.
- **Quantisation.** Quantising expert weights reduces memory, but the effect on quality varies with the router and the experts.

## Connections

- The architecture and routing are covered in the [mixture-of-experts theory pages](../../theory/models/mixture-of-experts/index.md), including [Mixtral](../../theory/models/mixture-of-experts/mixtral.md) and [Switch Transformer](../../theory/models/mixture-of-experts/switch-transformer.md).
- Serving the attention part of the same model follows the cache methods in [KV cache compression and eviction](kv-cache-compression.md).
- Splitting the prefill and decoding phases across machines is discussed in [Disaggregated prefill and decode](disaggregated-serving.md), which can also apply to MoE models.
- The hardware that carries the all-to-all traffic is covered in [AI Hardware](../hardware/index.md).

## Open questions

- How can the router be trained or constrained so that expert load stays balanced during serving, without changing the model's outputs?
- When an expert is offloaded, which experts should be kept resident, given that the routing changes with each prompt?

## References

### Seminal papers

- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv:2006.16668. https://arxiv.org/abs/2006.16668 — Annotation APIs and a compiler extension that shard a sparsely gated MoE model across devices, trained at over 600 billion parameters.
- Rajbhandari, S. et al. (2022). *DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale*. arXiv:2201.05596. https://arxiv.org/abs/2201.05596 — Model compression and an MoE inference system, with latency and cost results against dense and MoE baselines.
- Eliseev, A. & Mazur, D. (2023). *Fast Inference of Mixture-of-Experts Language Models with Offloading*. arXiv:2312.17238. https://arxiv.org/abs/2312.17238 — Parameter offloading for MoE inference, which runs Mixtral-8x7B on desktop hardware.
- Fedus, W., Zoph, B. & Shazeer, N. (2022). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. Journal of Machine Learning Research. arXiv:2101.03961. https://arxiv.org/abs/2101.03961 — Top-1 expert routing, which reduces the communication that routing adds per token.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — The serving memory layout that MoE serving systems build on for the attention part of the model.
