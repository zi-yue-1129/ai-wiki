---
related:
- theory/model-compression/knowledge-distillation
- engineering/on-device-edge
tags:
- engineering
- systems
aliases:
- 知識蒸餾
---

# Knowledge Distillation

This page covers how distillation is used to produce models for devices and services with tight budgets. The method itself, including the temperature-softened loss and its variants, is covered in the theory chapter: [Knowledge Distillation](../../theory/model-compression/knowledge-distillation/index.md). The original procedure is in [Hinton Distillation](../../theory/model-compression/knowledge-distillation/response-based/hinton-distillation/index.md), and distillation for language models is in [Sequence-Level KD](../../theory/model-compression/knowledge-distillation/llm-distillation/sequence-level/index.md).

## Overview

A large model is accurate but too expensive to run on a phone or in a low-latency service. Distillation produces a smaller student that keeps much of the teacher's behaviour. For deployment the questions are different from those in the theory chapter: what the teacher costs, which inputs the student must handle, and how the student is compressed further.

## Engineering notes

- **Teacher cost**: the teacher must be run over the distillation data, which can dominate the total compute. Caching its outputs once and reusing them across student experiments saves time.
- **Student architecture**: choose a student that the target runtime supports well. A smaller network that uses operators the device accelerates is often faster than a smaller one that does not.
- **Data coverage**: the student only learns the behaviour that the distillation data shows. Use inputs drawn from the device's real traffic, because this is often the largest lever on quality.
- **Quantisation after distillation**: distil first, then quantise. Errors from the two steps can add up, so measure the final quantised model on the device's own test set. Post-training quantisation such as [GPTQ](../../theory/model-compression/quantisation/post-training/gptq/index.md) is covered in the theory chapter.
- **Tuning**: the temperature and the loss weighting need tuning for each task, and the best values can change when the student size changes.

## How it fits the device pipeline

```mermaid
flowchart LR
  T[Large teacher] --> D[Distillation on device-like data]
  D --> S[Student model]
  S --> Q[Quantisation]
  Q --> E[Evaluation on device test set]
  E -->|Quality gap| D
  E -->|Meets budget| R[Deploy to runtime]
```

## Open questions

- How should the distillation data be chosen when the teacher's behaviour on rare inputs is unknown?
- How does distillation combine with quantisation, so that the final device model is both small and accurate?

## References

### Seminal papers

- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — Introduces training a small student on the softened outputs of a large teacher, with the temperature as a control.

### Related work

- Han, S., Mao, H. & Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR 2016. arXiv:1510.00149. https://arxiv.org/abs/1510.00149 — A different route to smaller networks, combining pruning and quantisation, that distillation is often used alongside.
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Quantised inference for mobile hardware, which a distilled student is often deployed with.
- Frantar, E. et al. (2023). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. ICLR 2023. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — Post-training quantisation for large language models, which can be applied to a distilled model as well.
- Dettmers, T. et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS 2022. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 8-bit inference for large transformers that keeps the outlier features in higher precision.
