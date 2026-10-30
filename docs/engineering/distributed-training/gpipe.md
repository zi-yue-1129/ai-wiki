---
tags:
- engineering
- systems
aliases:
- GPipe 管線平行
---

# GPipe: Pipeline Parallelism with Micro-Batches

GPipe splits a network into sequential stages placed on different devices, then divides each mini-batch into micro-batches so that several stages can work at once. The gradients of all micro-batches are accumulated, and the optimizer takes one step per batch, so training keeps the semantics of synchronous SGD.

## Overview

A model too large for one device can be split by layers, with each device holding a contiguous group of layers. Done naively, only one device works at a time. GPipe fills the pipeline by sending micro-batches through the stages in sequence, so each stage processes a different micro-batch while its neighbours process others. The cost is the idle time at the start and end of each step, called the pipeline bubble.

## Key concepts

- **Stage**: a contiguous group of layers placed on one device.
- **Micro-batch**: a slice of the mini-batch that flows through the pipeline as a unit.
- **Bubble**: the fraction of time devices sit idle while the pipeline fills and drains.
- **Activation memory**: each in-flight micro-batch must keep its activations until its backward pass, which limits how many can be in flight.

## How it works

With $K$ stages and $M$ micro-batches, the forward passes are scheduled through the pipeline, then the backward passes run in reverse order. The idle fraction, or bubble, is approximately $\frac{K-1}{M+K-1}$, so more micro-batches make the pipeline more efficient. Gradients from all micro-batches are summed before a single optimizer step.


**Interactive timeline on MkDocs:** Play/Pause, step backward/forward, scrub the timeline, or choose 0.5×/1×/2× speed. Motion starts paused, controls are keyboard-accessible, and reduced-motion preferences retain the readable still image. All timings and values are schematic, not measured GPU results.

![Animated GPipe schedule: four micro-batches fill three stages in forward order, then backward work drains the pipeline in reverse micro-batch order. Grey cells are idle bubbles.](../../assets/concept-animations/gpipe-fill-drain-motion.svg)

*Original continuous teaching animation, CC BY-SA 4.0.* The moving orange playhead reveals completed work; teal F1–F4 cells are forward computations and violet B4–B1 cells are backward computations. The grey cells make fill/drain bubbles visible. This **illustrative, equal-duration** 3-stage/4-micro-batch schedule has 12 idle stage-slots out of 36 (one-third), consistent with the idealised bubble fraction above; it is **not measured GPU utilisation**. Gradients accumulate over all four backward micro-batches before **one** optimizer update. On MkDocs, use **Play/Pause** (keyboard accessible); reduced-motion settings show the static fallback. On narrow screens, scroll horizontally to inspect all time slots. [GitHub-readable static schedule](../../assets/concept-animations/gpipe-fill-drain-still.svg).

### Gradient accumulation before the optimizer step

![Animated GPipe gradient accumulation: each of three pipeline stages receives backward gradients B4 through B1 at staggered times, and the optimizer step occurs only after all twelve stage-local arrivals.](../../assets/concept-animations/gpipe-gradient-accumulation-motion.svg)

*Original teaching animation, CC BY-SA 4.0.* Each filled teal dot marks **one completed micro-batch gradient contribution** at that pipeline stage, not a gradient magnitude. GPU 3 starts accumulating B4 first, followed by GPU 2 and GPU 1; each stage receives B4–B1 in backward order. Only after **all four contributions at every stage** does one logical optimizer step update the stage-local parameter partitions. The 13-slot clock and gradient arrival times are **schematic, not measured latency**. The MkDocs player supports keyboard Play/Pause and a reduced-motion still; on mobile, scroll horizontally. [GitHub-readable final-state preview](../../assets/concept-animations/gpipe-gradient-accumulation-still.svg).

## Key methods

The method is the micro-batch pipeline with synchronous gradient accumulation. The paper's evidence is measured throughput as the number of accelerators grows, for very large image models.

## Results

The paper reports close to linear speedup as accelerators are added for the models it evaluates. The bubble formula predicts the overhead, and the paper uses micro-batch counts that keep it small.

## Limitations

- **Bubble overhead**: with few micro-batches, the bubble is large and devices sit idle.
- **Activation memory**: all in-flight micro-batches keep their activations, which later schedules reduce.
- **Stage balance**: uneven stage costs leave the slowest stage as the bottleneck.

## Open questions

- Which schedules, such as interleaved or one-forward-one-backward schedules, reduce the bubble and activation memory best for transformer language models?
- How should stages be balanced when layers have very different costs?

## References

### Seminal papers

- Huang, Y. et al. (2019). *GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism*. NeurIPS 2019. https://arxiv.org/abs/1811.06965 — Pipelines micro-batches across model partitions and analyses the resulting bubble overhead.

### Related work

- Narayanan, D. et al. (2021). *Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM*. SC 2021. https://arxiv.org/abs/2104.04473 — Combines pipeline parallelism with tensor and data parallelism for transformer models.
- Shoeybi, M. et al. (2019). *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*. https://arxiv.org/abs/1909.08053 — The layer-internal split that pipeline parallelism complements.
- Rajbhandari, S. et al. (2020). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. SC 2020. https://arxiv.org/abs/1910.02054 — Reduces model-state memory on each stage, a different route to fitting large models.
- Li, S. et al. (2020). *PyTorch Distributed: Experiences on Accelerating Data Parallel Training*. VLDB 2020. https://arxiv.org/abs/2006.15704 — Describes the data-parallel communication that pipelines are often combined with.
