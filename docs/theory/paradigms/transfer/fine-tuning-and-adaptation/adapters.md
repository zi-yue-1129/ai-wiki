---
status: draft
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

Adapter modules are small bottleneck layers inserted into a pre-trained network. Only the adapters are trained for each task, and the original weights stay frozen. Houlsby et al. (2019) report that on GLUE, adapters come within 0.4% of full fine-tuning while adding 3.6% parameters per task. They are one of the first parameter-efficient fine-tuning methods, and they set up the design that later methods such as [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md) changed.

## Problem

Full fine-tuning gives every task its own complete copy of the model. For a model with hundreds of millions of parameters, serving many tasks then means storing and loading many copies. The goal is a method that trains and stores only a small set of task-specific parameters, while the shared base model stays the same for all tasks.

## Key concepts

- **Bottleneck adapter:** a small module that projects the hidden activations down to a narrow width and back up, inserted into the layers of the pre-trained network.
- **Frozen base:** the pre-trained weights stay fixed. Only the adapter weights are trained per task.
- **Bottleneck width:** the size of the narrow layer. It sets how many parameters each task adds.

## How it works

For each task, new adapters are added to the network, and training updates only their parameters on the task data. At serving time, one frozen base model is loaded once, and the small adapter for each task is swapped in. Because each adapter is small, storing many tasks costs little more than storing one model.

## Results

The abstract reports that the authors transferred BERT to 26 text classification tasks, including GLUE. Adapters reach near state-of-the-art performance, within 0.4% of full fine-tuning on GLUE, while adding 3.6% parameters per task. Full fine-tuning trains 100% of the parameters for every task.

## Limitations

- **Added inference cost.** Adapters are extra layers, so they add computation and latency at inference unless they are fused into the base weights, which adapter designs do not always allow.
- **Architecture changes.** Adapters need modifications to the model's layers, unlike methods that only change the input.
- **Results beyond the tested setting.** The paper's experiments are on BERT and text classification, so results on other architectures and generation tasks need their own checks.

## Open questions

- **Placement and size.** Where adapters should go in the network, and how wide they should be for a given task, is usually chosen by search rather than by theory.
- **Comparison with low-rank updates.** Whether bottleneck adapters or low-rank updates such as LoRA give the better trade-off between parameters, latency and accuracy is still debated, and results depend on the task.

## Connections

Adapters are the first widely used member of the parameter-efficient family covered under [fine-tuning and adaptation](index.md). The low-rank alternative is [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md), and its quantised variant is [QLoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.md). Prompt-based alternatives that add no layers are [prefix tuning](prefix-tuning.md) and [prompt tuning](prompt-tuning.md). The training practice that uses these methods is described under [training and fine-tuning](../../../../engineering/training/index.md).

## References

### Seminal papers

- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces bottleneck adapters that come within 0.4% of full fine-tuning on GLUE while adding 3.6% parameters per task.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank updates on frozen weights as an alternative that adds no extra layers at inference.
- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — Trains a small continuous prefix with the language model frozen, as a prompt-based alternative to adapters.
- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — Learns soft prompts on a frozen model and shows the approach matches model tuning as models grow.
- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Shows that parameter-efficient fine-tuning gives better accuracy and much lower compute than few-shot in-context learning.
