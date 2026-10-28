---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/mixture-of-experts
  - engineering/inference-optimization
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - GShard
  - Automatic sharding
---

# GShard

!!! info "Part of Serving Mixture-of-Experts Models"
    This method page belongs to [Serving Mixture-of-Experts Models](moe-serving.md). It explains GShard in detail; the parent page compares it with the other methods.

GShard is a module of annotation APIs and an extension to the XLA compiler that shards a sparsely gated mixture-of-experts model across many devices. The authors use it to train a model with over 600 billion parameters, by annotating how the tensors should be split and letting the compiler generate the partitioned program. It is primarily a training system, but its sharding method is the basis of expert parallelism at serving time.

## Problem

A model with many experts is too large for one device, so its experts must be spread across devices. Writing the communication between devices by hand for each model and each layout is error-prone and does not scale to many layouts. The problem is to express the parallel layout with a small set of annotations, and to let the compiler produce the device program.

## Core idea

GShard asks the programmer to annotate which tensor dimensions are split across devices, such as the expert dimension, and where the model should be replicated. The compiler, which GShard extends, then partitions the computation and inserts the communication. For a sparsely gated mixture-of-experts layer, the expert dimension is split across devices, and the tokens are routed to the devices that hold their experts.

## Procedure

1. Write the model with annotations marking the tensor dimensions to split across devices.
2. Annotate the expert layers so that each expert, or group of experts, lives on a device.
3. Compile the annotated model with the extended XLA compiler, which partitions the program.
4. Run the partitioned program, with the compiler inserting the communication that routing requires.
5. Check the layout against the devices and adjust the annotations if the communication dominates.

## Results

The paper reports training a sparsely gated mixture-of-experts model with automatic sharding beyond 600 billion parameters. It reports training a translation model from 100 languages to English on 2048 TPU v3 accelerators in 4 days. These are training results, and the paper's focus is training, so the serving consequences must be drawn from the design rather than from a reported serving benchmark.

## Limitations

- **Training focus.** The paper is about training the model. Serving has different batch sizes and latency needs, so the layout chosen for training may not be the best one for inference.
- **Compiler dependence.** The method depends on the XLA extension, so its benefits follow the compiler's support for the target hardware.
- **Routing communication.** Routing requires all-to-all traffic for every layer, and the traffic depends on how evenly tokens spread across experts.

## Connections

- The compiler that GShard extends is the subject of [XLA](../frameworks/compilers-and-kernels/xla.md), which is covered in the frameworks section.
- The architecture and routing are in the [mixture-of-experts theory pages](../../theory/models/mixture-of-experts/index.md).
- The serving alternatives are [DeepSpeed-MoE](deepspeed-moe.md) and [expert offloading](expert-offloading.md).

## Open questions

- What is the best expert layout for inference, when batch sizes are small and latency matters more than throughput?
- Can the annotations be inferred automatically from the serving workload, rather than written by the programmer?

## References

### Seminal papers

- Lepikhin, D. et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv:2006.16668. https://arxiv.org/abs/2006.16668 — The primary paper: annotation APIs and an XLA extension for sharding a sparsely gated MoE model, with training results.
- Shazeer, N. et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538. https://arxiv.org/abs/1701.06538 — The sparsely gated mixture-of-experts layer that GShard shards.
- Fedus, W., Zoph, B. & Shazeer, N. (2022). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. Journal of Machine Learning Research. arXiv:2101.03961. https://arxiv.org/abs/2101.03961 — Top-1 routing, which simplifies the communication that GShard's layout must support.
- Rajbhandari, S. et al. (2022). *DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale*. arXiv:2201.05596. https://arxiv.org/abs/2201.05596 — An MoE system that focuses on inference, for comparison with a training-first design.
- Eliseev, A. & Mazur, D. (2023). *Fast Inference of Mixture-of-Experts Language Models with Offloading*. arXiv:2312.17238. https://arxiv.org/abs/2312.17238 — Offloading as a way to serve MoE models on hardware with less memory.
