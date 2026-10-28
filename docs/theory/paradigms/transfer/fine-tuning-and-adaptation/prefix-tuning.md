---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/transfer/fine-tuning-and-adaptation/index.md
- theory/paradigms/transfer/fine-tuning-and-adaptation/adapters.md
- theory/paradigms/transfer/fine-tuning-and-adaptation/prompt-tuning.md
tags:
- transfer learning
- fine-tuning
- parameter-efficient fine-tuning
- prompt-based methods
aliases:
  - Prefix tuning
  - Prefix-Tuning
  - 前綴調校
---

# Prefix Tuning

Prefix tuning adapts a frozen language model by learning a short sequence of continuous vectors, called the prefix, that conditions the model on the task. The model's own weights are never changed. Li and Liang (2021) report that it trains about 0.1% of the parameters and reaches performance comparable to full fine-tuning on table-to-text and summarisation, with better results than fine-tuning in low-data settings. It is a parameter-efficient method within [fine-tuning and adaptation](index.md) that changes what the model attends to rather than adding layers, and it is the direct predecessor of [prompt tuning](prompt-tuning.md).

## Problem

Full fine-tuning updates every parameter of a generation model, and it stores a full copy of the model for each task. Discrete text prompts avoid this cost, but they are hand-written, and their effect is limited by the words that can be chosen. The goal is to learn the conditioning as continuous vectors, with a small trainable part and a frozen model.

## Key concepts

- **Prefix:** a sequence of continuous vectors, learned for one task, that the frozen model reads before or alongside its input.
- **Frozen model:** the pre-trained language model whose weights are not changed during adaptation.
- **Trained fraction:** the share of parameters that are trained, which the paper puts at about 0.1%.

## How it works

For a task, a set of prefix vectors is initialised and optimised by gradient descent on the task's objective, while the language model's parameters stay fixed. The prefix is then stored for that task, and one frozen model serves all tasks by swapping in the matching prefix. Because the model itself is not modified, many tasks can share one copy of it.

## Results

The abstract reports that, with GPT-2 on table-to-text and BART on summarisation, prefix tuning reaches performance comparable to fine-tuning when all the data is available. It outperforms fine-tuning in low-data settings, and it extrapolates better to examples whose topics were not seen in training. It trains about 0.1% of the parameters.

## Limitations

- **Narrow task set.** The paper's main tasks are table-to-text and summarisation, so the comparison on other tasks is not shown by it.
- **Sensitivity to design choices.** The prefix length and its initialisation affect results, and they are usually chosen by experiment.
- **Context budget.** The prefix takes positions in the model's input or attention context, which reduces the room left for the actual input.

## Open questions

- **Where the prefix helps most.** Why conditioning with a prefix generalises better in low-data settings is not explained in the abstract, and it is a question for further study.
- **Versus adapters.** How prefix tuning compares with adapters across model sizes and tasks depends on the setting, and the two are hard to compare on equal footing.

## Connections

Prefix tuning is one of the prompt-based parameter-efficient methods. [Prompt tuning](prompt-tuning.md) simplifies it by learning soft prompts only at the input, and [adapters](adapters.md) take the other route of adding small layers. The low-rank alternative is [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md).

## References

### Seminal papers

- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — Optimises a continuous prefix with the language model frozen, training about 0.1% of the parameters.
- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — Simplifies prefix tuning to soft prompts at the input and shows it matches model tuning as models grow.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters, the layer-adding alternative to prompt-based parameter-efficient tuning.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank updates on frozen weights, a third route to parameter-efficient adaptation.
- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Shows that parameter-efficient fine-tuning gives better accuracy and much lower compute than few-shot in-context learning.
