---
status: complete
last_reviewed: 2026-10-28
related:
- theory/models/llm
- engineering/training
tags:
- model compression
- knowledge distillation
- large language models
aliases:
  - LLM distillation
  - On-policy distillation
  - Reasoning distillation
  - 大型語言模型蒸餾
---

# Distillation for Large Language Models

Distillation for language models transfers the behaviour of a large model into a smaller one by training on the model's generated text, often including its reasoning. It is the form of [knowledge distillation](../index.md) most used in practice today, because the teacher can produce large amounts of training data cheaply.

## Overview

Two broad recipes are common. In **sequence-level** distillation, the teacher generates responses to a set of prompts, and the student is trained on them with ordinary supervised learning. In **on-policy** distillation, the student generates its own responses and the teacher scores them, so that the student is trained on the distribution it actually produces. A third recipe distils reasoning traces, the step-by-step solutions a strong model writes, into a smaller model, which is then trained to produce similar traces.

## Key concepts

- **Teacher-generated data.** Responses produced by the large model and used as training targets for the small one.
- **On-policy training.** Training on the student's own samples, scored by the teacher, which reduces the mismatch between training and generation.
- **Reasoning traces.** Intermediate steps that a model writes before its answer. Distilling them transfers how a problem is approached, not only the final answer.
- **Model families.** Students are often smaller models from the same family, which makes the tokenisers and output spaces match.

## Key methods

The three landmark methods below all train a small model on a large model's output, but they differ in who generates the data and what the training objective is.

- [Sequence-level knowledge distillation (Kim & Rush, 2016)](sequence-level/index.md): the teacher produces sequences that the student learns by ordinary maximum likelihood. This is the simplest recipe and the earliest form of language-model distillation.
- [MiniLLM (Gu et al., 2023)](minillm/index.md): the student generates its own samples, and training uses a reverse KL objective with an on-policy optimisation method, which targets the mismatch between training and generation.
- [DeepSeek-R1 distillation (DeepSeek-AI, 2025)](deepseek-r1/index.md): smaller models are trained on reasoning patterns from a large reasoning model, which the paper reports can enhance the reasoning of smaller models.

Sequence-level distillation is the cheapest, because the teacher's outputs are generated once. MiniLLM is costlier, because the teacher scores samples from the student during training, but it addresses the mismatch between training and generation. Reasoning distillation applies the sequence-level recipe to long traces, where the quality of the traces matters most.

## Trade-offs

- **Quality versus generation cost.** Teacher-generated data are cheap compared with human labels, but long reasoning traces are expensive to produce.
- **Teacher terms of use.** Training a student on a proprietary model's outputs may be restricted, depending on the provider.
- **Diversity.** A student trained only on teacher outputs can inherit the teacher's style and miss its failure modes.

## More variants and open issues

- **Variant:** [data-free distillation](../data-free/index.md), where the synthetic data come from the teacher without prompts.
- **Open issue:** what a student learns from reasoning traces, and whether it generalises beyond the tasks in the training data.
- **Open issue:** how to measure whether a distilled model is faithful to the teacher's reasoning rather than only its final answers.

## Connections

LLM distillation sits between the [training](../../../../engineering/training/index.md) pipeline and the [large language model](../../../models/llm/index.md) page, which covers distillation among the methods for reducing cost. Using a large model to produce training data for a small one echoes how people learn from worked examples, discussed in [cognitive science](../../../../brain-mind/cognitive-science/index.md).

## References

### Seminal papers

- Kim, Y. & Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — Trains on the teacher's own sequence outputs; the abstract reports a student about 10 times faster than its teacher with little loss in quality.
- Gu, Y., Dong, L., Wei, F. & Huang, M. (2023). *MiniLLM: On-Policy Distillation of Large Language Models*. arXiv:2306.08543. https://arxiv.org/abs/2306.08543 — Replaces the forward KL of standard distillation with reverse KL and optimises it on-policy; the method scales from 120M to 13B parameters in the abstract's report.
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948. https://arxiv.org/abs/2501.12948 — Reports reasoning trained by reinforcement learning in large models, and states that the reasoning patterns of large models can be used to enhance smaller ones.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The original distillation objective, which the language-model methods above build on.

### Surveys and textbooks

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation, the background for the language-model methods above.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Distils BERT into a model about 40% smaller that keeps 97% of its language understanding, an early encoder-model precedent for distilling pretrained language models.
