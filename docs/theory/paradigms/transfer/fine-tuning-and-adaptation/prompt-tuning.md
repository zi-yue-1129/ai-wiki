---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/transfer/fine-tuning-and-adaptation/index.md
- theory/paradigms/transfer/fine-tuning-and-adaptation/prefix-tuning.md
- theory/paradigms/transfer/fine-tuning-and-adaptation/adapters.md
tags:
- transfer learning
- fine-tuning
- parameter-efficient fine-tuning
- prompt-based methods
- large language models
aliases:
  - Prompt tuning
  - Soft prompts
  - 提示調校
---

# Prompt Tuning

Prompt tuning adapts a frozen language model by learning soft prompts, which are sequences of trainable embedding vectors prepended to the input. Lester et al. (2021) show that these learned prompts, unlike hand-written text prompts, can use the signal from any number of labelled examples, and that as models grow the method becomes competitive with full model tuning. It is a simplification of [prefix tuning](prefix-tuning.md), and it sits within [fine-tuning and adaptation](index.md).

## Problem

Text prompts are discrete words chosen by hand, so their effect is limited by what can be written down. Full model tuning gives the best accuracy but needs a full copy of the model per task. Prompt tuning seeks a middle path: learn the conditioning end to end, while sharing one frozen model across tasks.

## Key concepts

- **Soft prompt:** a sequence of learned vectors in the model's embedding space. It is not made of real words, and it is trained by backpropagation.
- **Frozen model:** the pre-trained model, whose parameters stay fixed while the prompt is learned.
- **Model scale:** the paper's central variable. Its results depend on how large the frozen model is.

## How it works

A small set of prompt vectors is placed in front of the input embeddings. The loss on labelled task data is backpropagated to the prompt vectors alone, and the model's weights are not updated. At serving time, the model is shared, and each task brings its own prompt. Since a prompt is only a few small vectors, storing many tasks is cheap.

## Results

The abstract reports that the learned prompts outperform GPT-3's few-shot learning by a large margin. In ablations over T5 model sizes, prompt tuning becomes more competitive as models grow, and beyond billions of parameters it matches the performance of model tuning, where all weights are updated. The authors also report that conditioning a frozen model with soft prompts gives better robustness to domain transfer than model tuning does.

## Limitations

- **Small models.** The paper's own results show that prompt tuning is weaker than model tuning at smaller scales, so its benefit depends on the model being large.
- **Optimisation.** Soft prompts are continuous vectors that are not easy to read or edit, so debugging and manual control are harder than with text prompts.
- **Single-task framing.** The paper studies task-specific prompts. Combining prompts for many tasks at once is a separate question that the paper does not settle.

## Open questions

- **Scale threshold.** The model size at which prompt tuning matches model tuning depends on the task and the model family, and the threshold is not known in general.
- **Initialisation and length.** How the prompt is initialised and how long it should be affect results, and both are usually chosen by search.

## Connections

Prompt tuning is the simplest of the prompt-based methods. [Prefix tuning](prefix-tuning.md) learns conditioning at every layer, while prompt tuning learns it only at the input. [Adapters](adapters.md) instead add small layers, and [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md) adds low-rank updates. The large models that make prompt tuning competitive are the subject of [training and fine-tuning](../../../../engineering/training/index.md).

## References

### Seminal papers

- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — Learns soft prompts on a frozen model, becoming competitive with model tuning as models grow.
- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — The prompt-based method that prompt tuning simplifies, learning conditioning at every layer.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters, the layer-adding alternative to prompt-based tuning.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank updates on frozen weights, a third route to parameter-efficient adaptation.
- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Shows that parameter-efficient fine-tuning gives better accuracy and much lower compute than few-shot in-context learning.
