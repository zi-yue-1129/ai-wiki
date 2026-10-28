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

DoRA, short for Weight-Decomposed Low-Rank Adaptation, is a variant of [LoRA](index.md) that splits each pre-trained weight matrix into a magnitude and a direction. The low-rank update is applied only to the direction, and the magnitude is trained directly. Liu et al. (2024) report that DoRA beats LoRA on commonsense reasoning, with no added inference latency once the update is merged into the original weight. It belongs to the LoRA family because it keeps the same low-rank update, and it changes how that update is applied.

## Problem

LoRA adds a low-rank update \(BA\) to a frozen weight \(W_0\), which is cheap to train and store. The paper compares how full fine-tuning and LoRA change the weights, and finds a difference in their behaviour. For the query and value matrices of VL-BART, LoRA's changes to magnitude and direction move together, while full fine-tuning's do not. The authors suspect that LoRA cannot make small directional changes alongside large magnitude changes, or the reverse, and that this limits its accuracy.

## Key concepts

- **Magnitude:** the norm of each column of the weight matrix. In DoRA it is a separate trainable vector \(m\).
- **Direction:** each column divided by its norm. The low-rank update is applied to this part.
- **Weight decomposition:** the paper writes the weight as \(W = m \cdot V / \lVert V \rVert_c\), where \(V\) is the directional matrix and \(\lVert \cdot \rVert_c\) is the column-wise norm.

## How it works

DoRA initialises \(V\) to \(W_0\) and keeps the magnitude vector \(m\) as a trainable parameter. The LoRA product \(BA\) updates the direction, so the adapted weight is

\[
W' = m \cdot \frac{W_0 + BA}{\lVert W_0 + BA \rVert_c}
\]

After training, the result can be merged into a single weight matrix, so inference costs the same as the original model.

## Results

On commonsense reasoning with LLaMA-7B, the paper's table reports an average of 74.7 for LoRA and 78.4 for DoRA, a gain of 3.7 points. A variant at half the rank reaches 77.5. The version used for these figures is the ICML 2024 proceedings version, and the numbers may differ in other versions of the preprint.

## Limitations

- **Narrow evidence.** The authors plan to test DoRA beyond language and vision, particularly audio, so its behaviour in other domains is not yet shown.
- **Smaller gains when full fine-tuning is worse.** On LLaVA-1.5-7B, where full fine-tuning underperforms LoRA, DoRA's advantage over LoRA is smaller.
- **Memory-saving variant.** The gradient modification that saves memory costs a small accuracy difference, about 0.2 on LLaMA.
- **Inherits LoRA's choices.** The rank and the matrices to adapt still need tuning, as in LoRA.

## Open questions

- **Why the decomposition helps.** The paper's analysis motivates the decomposition with observed differences in weight changes, but a full account of why separating magnitude and direction helps is open.
- **Interaction with quantisation.** How DoRA combines with a quantised base, as in [QLoRA](qlora.md), is a practical question that the paper does not settle.

## Connections

DoRA sits in the LoRA family alongside [QLoRA](qlora.md), which quantises the frozen base. Both are parameter-efficient fine-tuning methods described under [fine-tuning and adaptation](../../../paradigms/transfer/fine-tuning-and-adaptation/index.md). The practice of fine-tuning large models with these methods is covered under [training](../../../../engineering/training/index.md).

## References

### Seminal papers

- Liu, S.-Y., et al. (2024). *DoRA: Weight-Decomposed Low-Rank Adaptation*. ICML 2024, arXiv:2402.09353. https://arxiv.org/abs/2402.09353 — Decomposes each pre-trained weight into magnitude and direction, applies LoRA only to the direction, and reports gains over LoRA with no added inference latency.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — The low-rank update that DoRA modifies, with the frozen base and the merge at inference.
- Dettmers, T., Pagnoni, A., Holtzman, A., Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — Applies LoRA adapters to a 4-bit frozen base, the quantised counterpart in the same family.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters, the layer-adding alternative to low-rank updates.
- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Shows that parameter-efficient fine-tuning gives better accuracy and much lower compute than few-shot in-context learning.
