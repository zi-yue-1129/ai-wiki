---
status: complete
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

Prefix tuning adapts a frozen language model by learning a short sequence of continuous vectors, the prefix, that every Transformer layer attends to as if it were extra context. The model's own weights are never changed. Li and Liang (2021) report that the method trains about 0.1% of the parameters, that on table-to-text it is roughly on par with full fine-tuning, that it is slightly behind on summarisation, and that it beats fine-tuning when data is scarce. It sits within [fine-tuning and adaptation](index.md) as a prompt-based method, and [prompt tuning](prompt-tuning.md) later simplified it.

## Problem

Full fine-tuning updates every parameter of a generation model, and it stores a full copy of the model for each task. Discrete text prompts avoid this cost, but they are hand-written, and their effect is limited by the words that can be chosen. The goal is to learn the conditioning as continuous vectors, with a small trainable part and a frozen model.

## Key concepts

- **Prefix:** a sequence of learned continuous vectors placed before the input. At every layer, the prefix positions supply key and value activations that the input tokens attend to, so the prefix acts as virtual tokens.
- **Reparameterisation:** the paper found that optimising the prefix directly was unstable and sensitive to the learning rate and initialisation. Training instead uses a smaller matrix passed through a feed-forward network to produce the prefix. Only the resulting prefix is kept after training.
- **Frozen model:** the pre-trained language model whose weights are not changed during adaptation.

## How it works

For each task, a prefix is trained by gradient descent on the task's objective while the language model's parameters stay fixed. The paper's main table-to-text setup uses a prefix length of 10. After training, the prefix is stored for the task, and one frozen model serves all tasks by swapping in the matching prefix. Tuning only the input embedding layer performs notably worse than tuning the prefix at every layer.

## Results

On table-to-text with GPT-2, prefix tuning trains about 0.1% of the parameters and is roughly on par with full fine-tuning across E2E, WebNLG and DART; on E2E with GPT-2 Medium it scores slightly higher on BLEU (69.7 against 68.2). On summarisation with BART-Large, full fine-tuning reaches ROUGE-L 37.25, while prefix tuning reaches 36.05 with 2% of the parameters and 35.05 with 0.1%, so it is slightly worse there.

With 50 to 500 training examples, prefix tuning outperforms fine-tuning on average, by about 2.9 BLEU on table-to-text, and the gap shrinks as data grows.
## Limitations

- **Narrow task set.** The main tasks are table-to-text and summarisation, so the paper does not show the method's behaviour on other tasks.
- **Sensitivity to design choices.** The prefix length and the reparameterisation matter, and the paper's own summarisation results depend on the prefix length.
- **Context budget.** The prefix occupies positions in the model's attention context, which reduces the room left for the actual input.

## Open questions

- **Why the prefix generalises.** The paper reports a gain over fine-tuning with few examples. What causes it is an open question for further study.
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
