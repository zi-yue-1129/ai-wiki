---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/training
- theory/paradigms/transfer/fine-tuning-and-adaptation/index.md
tags:
- model compression
- low-rank factorisation
- fine-tuning
- large language models
aliases:
  - DoRA
  - Weight-Decomposed Low-Rank Adaptation
  - 權重分解低秩適應
---

# DoRA

DoRA, short for Weight-Decomposed Low-Rank Adaptation, is a variant of [LoRA](index.md) that splits each pre-trained weight matrix into a magnitude and a direction, and applies the low-rank update only to the direction. Liu et al. (2024) report that this outperforms LoRA at the same parameter budget, with no added inference latency once the update is merged into the original weight. It belongs to the LoRA family because it keeps the same low-rank mechanism, and it changes only how the update is applied.

## Problem

LoRA adds a low-rank update \(BA\) to a frozen weight \(W_0\), which is cheap to train and store. Its accuracy can still fall short of full fine-tuning on some tasks. DoRA aims to close that gap by changing how the low-rank update is applied, rather than by adding layers.

## Key concepts

- **Magnitude:** the size of each column of the weight matrix. In DoRA it is a separate trainable vector.
- **Direction:** the unit vector of each column. The low-rank update is applied to this part.
- **Weight decomposition:** writing the pre-trained weight as the magnitude times the direction, so the two can be trained separately.

## How it works

The pre-trained weight is decomposed into a trainable magnitude vector and a directional component. The directional component is adapted with a LoRA update, and the magnitude is trained directly. After training, the result is merged back into a single weight matrix, so inference costs the same as the original model, which is the no-latency property the paper reports.

## Results

The paper reports that DoRA outperforms LoRA when both are applied to the same models and tasks, with no added inference latency once the update is merged into the original weight. The experiments cover commonsense reasoning, visual instruction tuning and image and video-text understanding, and the paper reports gains on several LLaMA models over LoRA. The exact gains differ between versions of the paper, so they should be taken from the version cited.

## Limitations

- **Training cost.** The decomposition adds a magnitude vector and the bookkeeping for the directional part, so training is somewhat more involved than plain LoRA.
- **Gains are task-dependent.** The reported improvements are modest on some tasks, and they vary with the model and the rank, so they should not be read as a general speed-up in accuracy.
- **Relies on the LoRA setting.** The method inherits LoRA's choices of rank and of which matrices to adapt, which still need tuning.

## Open questions

- **Why the decomposition helps.** The paper argues from how full fine-tuning changes weights, but a full account of why separating magnitude and direction helps is still open.
- **Interaction with quantisation.** How DoRA combines with a quantised base, as in [QLoRA](qlora.md), is a practical question that the paper does not settle.

## Connections

DoRA sits in the LoRA family alongside [QLoRA](qlora.md), which quantises the frozen base. Both are parameter-efficient fine-tuning methods described under [fine-tuning and adaptation](../../../paradigms/transfer/fine-tuning-and-adaptation/index.md). The practice of fine-tuning large models with these methods is covered under [training](../../../../engineering/training/index.md).

## References

### Seminal papers

- Liu, S.-Y., et al. (2024). *DoRA: Weight-Decomposed Low-Rank Adaptation*. arXiv:2402.09353. https://arxiv.org/abs/2402.09353 — Decomposes each pre-trained weight into magnitude and direction, applies LoRA only to the direction, and reports gains over LoRA with no added inference latency.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — The low-rank update that DoRA modifies, with the frozen base and the merge at inference.
- Dettmers, T., Pagnoni, A., Holtzman, A., Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — Applies LoRA adapters to a 4-bit frozen base, the quantised counterpart in the same family.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters, the layer-adding alternative to low-rank updates.
- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Shows that parameter-efficient fine-tuning gives better accuracy and much lower compute than few-shot in-context learning.
