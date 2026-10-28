---
status: complete
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

Prompt tuning adapts a frozen language model by learning soft prompts, which are trainable embedding vectors prepended to the input. Lester et al. (2021) show that these prompts can be trained on any number of labelled examples, unlike hand-written text prompts, and that as the frozen model grows, the method becomes competitive with full model tuning. It is a simplification of [prefix tuning](prefix-tuning.md), and it sits within [fine-tuning and adaptation](index.md).

## Problem

Text prompts are discrete words chosen by hand, so their effect is limited by what can be written down. Full model tuning gives the best accuracy but needs a full copy of the model per task. Prompt tuning seeks a middle path: learn the conditioning end to end, while sharing one frozen model across tasks.

## Key concepts

- **Soft prompt:** a block of \(p\) trainable vectors, each of the model's embedding width, placed in front of the embedded input. It is not made of real words, and it is trained by backpropagation.
- **Frozen model:** the pre-trained T5 model, whose parameters stay fixed while the prompt is learned.
- **Initialisation:** the paper compares random uniform values, embeddings of common vocabulary tokens, and embeddings of the output class labels. Initialising from the class labels is one of the options compared.

## How it works

The prompt vectors are placed in front of the input embeddings, and the frozen encoder-decoder processes the combined sequence. The loss on labelled task data is backpropagated to the prompt vectors alone. The default prompt length is 100 tokens, and the paper tests lengths of 1, 5, 20, 100 and 150. Each task therefore needs about \(E \times p\) new parameters, which for T5-XXL with a 100-token prompt is about 410K parameters, or 0.004% of the model. At serving time the model is shared, and each task brings its own prompt.

## Results

At T5-XXL (11B), prompt tuning matches a strong multi-task model-tuning baseline on SuperGLUE while using far fewer task-specific parameters. The method only becomes competitive at billions of parameters, and smaller models lag well behind. The paper also reports that prompt-tuned T5-Small matches GPT-3 XL, and prompt-tuned T5-Large beats GPT-3 175B on its evaluation.

On domain transfer, a prompt trained on SQuAD and tested on out-of-domain question answering datasets beats model tuning on most of them, with the largest gain about 12.5 F1 on TextbookQA. Model tuning is better on a few sets, notably DROP, which shares Wikipedia with SQuAD.

## Limitations

- **Small models.** Small models depend heavily on the prompt length and the initialisation, and the gap to model tuning is large until the model reaches XXL scale.
- **Unreliable frozen checkpoints.** Span-corruption T5 checkpoints worked well as frozen models at only 2 of 5 sizes. A language-model adaptation step fixes this, at roughly 10% of T5's original pre-training steps.
- **Long prompts.** Prompts longer than 100 tokens appear mildly detrimental for larger models, and long prompts make training slow.
- **Interpretability.** The learned prompts are hard to read, and the paper finds little structure in them beyond nearest-neighbour clusters.

## Open questions

- **Scale threshold.** The model size at which prompt tuning matches model tuning depends on the task and the model family, and the threshold is not known in general.
- **Convergence speed.** The paper does not compare convergence speed with model tuning across the full range of tasks.

## Connections

Prompt tuning is the simplest of the prompt-based methods. [Prefix tuning](prefix-tuning.md) learns conditioning at every layer, while prompt tuning learns it only at the input. [Adapters](adapters.md) instead add small layers, and [LoRA](../../../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md) adds low-rank updates. The large models that make prompt tuning competitive are the subject of [training and fine-tuning](../../../../engineering/training/index.md).

## References

### Seminal papers

- Lester, B., Al-Rfou, R., Constant, N. (2021). *The Power of Scale for Parameter-Efficient Prompt Tuning*. arXiv:2104.08691. https://arxiv.org/abs/2104.08691 — Learns soft prompts on a frozen T5 model, becoming competitive with model tuning as models grow.
- Li, X. L., Liang, P. (2021). *Prefix-Tuning: Optimizing Continuous Prompts for Generation*. arXiv:2101.00190. https://arxiv.org/abs/2101.00190 — The prompt-based method that prompt tuning simplifies, learning conditioning at every layer.
- Houlsby, N., et al. (2019). *Parameter-Efficient Transfer Learning for NLP*. arXiv:1902.00751. https://arxiv.org/abs/1902.00751 — Introduces adapters, the layer-adding alternative to prompt-based tuning.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank updates on frozen weights, a third route to parameter-efficient adaptation.
- Liu, H., et al. (2022). *Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than In-Context Learning*. arXiv:2205.05638. https://arxiv.org/abs/2205.05638 — Shows that parameter-efficient fine-tuning gives better accuracy and much lower compute than few-shot in-context learning.
