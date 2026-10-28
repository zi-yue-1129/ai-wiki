---
status: draft
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

Two broad recipes are common. In **sequence-level** distillation, the teacher generates responses to a set of prompts, and the student is trained on them with ordinary supervised learning. In **on-policy** distillation, the student generates its own responses, and the teacher scores them, so that the student is trained on the distribution it actually produces. A third recipe distils reasoning traces, the step-by-step solutions that a strong model writes, into a smaller model, which then learns to reason in a similar way.

## Key concepts

- **Teacher-generated data.** Responses produced by the large model and used as training targets for the small one.
- **On-policy training.** Training on the student's own samples, scored by the teacher, which reduces the mismatch between training and generation.
- **Reasoning traces.** Intermediate steps that a model writes before its answer. Distilling them transfers how a problem is solved, not only the final answer.
- **Model families.** Students are often smaller models from the same family, which makes the tokenisers and output spaces match.

## Key methods

### MiniLLM: On-Policy Distillation of Large Language Models (Gu et al., 2023)

- **Problem:** Standard distillation of language models uses the teacher's distribution over sequences, which the student does not produce during generation, so errors compound at inference time.
- **Core idea:** Train the student on its own generated sequences, with a reverse-direction divergence that favours the modes of the teacher's distribution, so that the student concentrates on outputs the teacher finds likely.
- **Equation or algorithm:** The student's samples are scored by a divergence between the teacher and student distributions, and the student is updated with a policy-gradient style estimator, since the sampling is not differentiable.
- **Results:** The abstract states that the method is scalable for different model families with 120 million to 13 billion parameters. The comparisons with baselines are reported in the paper.
- **Limitations:** Policy-gradient style updates are more complex and costlier than supervised distillation, and the method needs a teacher that can be run during training.

### DeepSeek-R1 (DeepSeek-AI, 2025)

- **Problem:** Strong reasoning in language models was thought to need very large models, and smaller models could not learn it from data alone.
- **Core idea:** The paper shows that reasoning patterns found by reinforcement learning in large models can be used to guide and enhance the reasoning of smaller models. The distillation of these reasoning traces is one of its main results.
- **Equation or algorithm:** The large model is trained with reinforcement learning, and its reasoning outputs are then used as training data for smaller models in the same family.
- **Results:** The abstract states that reasoning patterns from large models can be systematically harnessed to guide and enhance the reasoning capabilities of smaller models. Benchmark numbers are in the paper.
- **Limitations:** The reasoning distilled into small models is bounded by the teacher's reasoning, and the training data are long reasoning traces, which are costly to produce.

## Trade-offs

- **Quality versus generation cost.** Teacher-generated data are cheap compared with human labels, but long reasoning traces are expensive to produce.
- **Teacher terms of use.** Training a student on a proprietary model's outputs may be restricted, depending on the provider.
- **Diversity.** A student trained only on teacher outputs can inherit the teacher's style and miss its failure modes.

## More variants and open issues

- **Variant:** [data-free distillation](../data-free/index.md), where the synthetic data come from the teacher without prompts.
- **Open issue:** what a student learns from reasoning traces, and whether it generalises beyond the tasks in the training data.
- **Open issue:** how to measure whether a distilled model is faithful to the teacher's reasoning rather than only its final answers.

## Connections

LLM distillation sits between the [training](../../../../engineering/training/index.md) pipeline and the [large language model](../../../models/llm/index.md) page, which lists distillation among the methods for reducing cost. The use of a large model to produce training data for a small one echoes how people learn from worked examples, discussed in [cognitive science](../../../../brain-mind/cognitive-science/index.md).

## References

### Seminal papers

- Gu, Y., Dong, L., Wei, F., Huang, M. (2023). *MiniLLM: On-Policy Distillation of Large Language Models*. arXiv:2306.08543. https://arxiv.org/abs/2306.08543 — On-policy distillation that trains the student on its own samples, scalable from 120 million to 13 billion parameters.
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948. https://arxiv.org/abs/2501.12948 — Shows that reasoning patterns from large models can be harnessed to enhance smaller models.
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — Trains on the teacher's own sequence outputs, the earlier form of LLM distillation.
- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Distils a language model that keeps 97% of BERT's language understanding at 40% smaller size.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation, the background for the language-model methods above.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The original distillation objective, which the language-model methods above build on.
