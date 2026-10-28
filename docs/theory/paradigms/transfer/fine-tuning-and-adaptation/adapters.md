---
status: complete
last_reviewed: 2026-10-28
related:
- theory/paradigms/transfer/fine-tuning-and-adaptation/index.md
- theory/model-compression/low-rank-and-efficient-architectures/lora/index.md
tags:
- transfer learning
- fine-tuning
- parameter-efficient fine-tuning
- adapters
aliases:
  - Adapter modules
  - Adapters
  - 適配器模組
---

# Adapter Modules

Adapter modules are small bottleneck networks inserted into a pre-trained Transformer. For each task only the adapters, and the layer normalisation parameters, are trained, while the original weights stay frozen. Houlsby et al. (2019) report that on GLUE, adapters reach a mean score 0.4 points below full fine-tuning while adding 3.6% parameters per task. They are one of the first parameter-efficient fine-tuning methods, and the design that later methods such as [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md) changed.

## Problem

Full fine-tuning gives every task its own complete copy of the model. For a model with hundreds of millions of parameters, serving many tasks then means storing and loading many copies. The goal is a method that trains and stores only a small set of task-specific parameters, while the shared base model stays the same for all tasks.

## Key concepts

- **Bottleneck adapter:** a module that projects the hidden activations down to a narrow width \(m\), applies a non-linearity, and projects back up to the model width \(d\). It has an internal skip connection, so near initialisation it passes its input through.
- **Placement:** each Transformer layer gets two adapters, one after the attention sub-layer and one after the feed-forward sub-layer.
- **Trained parameters:** the adapter weights, plus the layer normalisation parameters, which are trained together with them.

## How it works

The adapter weights are initialised near zero, so each adapter starts close to the identity function, and the pre-trained network's behaviour is preserved at the start of training. For each task, training updates the adapters and layer norms on the task data while everything else stays fixed. At serving time, one frozen base model is loaded once, and the small set of parameters for each task is swapped in. Because each set is small, storing many tasks costs little more than storing one model.

## Results

The paper transfers BERT to 26 text classification tasks, including GLUE. With the bottleneck size chosen per task from {8, 64, 256}, adapters use about 3.6% of the parameters per task, and reach a mean GLUE score of 80.0 against 80.4 for full fine-tuning. With a fixed bottleneck of 64, they use about 2.1% per task and score 79.6. Solving all GLUE tasks takes about 1.3 times the parameters of BERT with adapters, against about 9 times with full fine-tuning.

## Limitations

- **Added computation.** Adapters are extra layers, so they add computation at inference, and the adapter design does not fold them into the base weights the way LoRA does.
- **Architecture changes.** Adapters require changes to the model's layers, unlike methods that only change the input.
- **Scope of the evidence.** The paper's experiments are on BERT and classification tasks, so results on other architectures and generation tasks need their own checks.

## Open questions

- **Placement and size.** How wide the bottleneck should be for a given task, and whether the two-per-layer placement is best, are chosen by experiment rather than by theory.
- **Comparison with low-rank updates.** Whether bottleneck adapters or low-rank updates such as LoRA give the better trade-off between parameters, latency and accuracy is still debated, and results depend on the task.

## Connections

Adapters are the first widely used member of the parameter-efficient family covered under [fine-tuning and adaptation](index.md). The low-rank alternative is [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md), and its quantised variant is [QLoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.md). Prompt-based alternatives that add no layers are [prefix tuning](prefix-tuning.md) and [prompt tuning](prompt-tuning.md). The training practice that uses these methods is described under [training and fine-tuning](../../../../engineering/training/index.md).

## References

### Seminal papers

- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces bottleneck adapters that reach a mean GLUE score 0.4 points below full fine-tuning while adding 3.6% parameters per task.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank updates on frozen weights as an alternative that adds no extra layers at inference.
- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — Trains a small continuous prefix with the language model frozen, as a prompt-based alternative to adapters.
- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — Learns soft prompts on a frozen model and shows the approach matches model tuning as models grow.
- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Shows that parameter-efficient fine-tuning gives better accuracy and much lower compute than few-shot in-context learning.
