---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/llm
- engineering/training
tags:
- model compression
- knowledge distillation
- reasoning distillation
- large language models
aliases:
  - DeepSeek-R1 distillation
  - Reasoning distillation
  - 推理蒸餾
---

# DeepSeek-R1 Distillation

DeepSeek-R1 distillation transfers the reasoning of a large model into smaller models by training them on the large model's reasoning traces. The DeepSeek-AI report shows that reasoning patterns found in large models can be used to strengthen smaller ones, and it reports that distilling those patterns works better than reinforcement learning applied to the small models directly. It is a [language-model](../index.md) distillation method, and a form of [sequence-level distillation](../sequence-level/index.md) for long reasoning outputs.

## Problem

Strong multi-step reasoning was thought to need very large models. A small model trained with reinforcement learning from scratch reasons less well than a large one, and it is unclear whether the small model can learn the same behaviour more cheaply.

## Core idea

Train a large model with reinforcement learning until it reasons well, then use its reasoning traces as supervised training data for smaller models. The small models learn to write the same kind of step-by-step solutions, without running reinforcement learning themselves.

## Equation or algorithm

The large model produces reasoning traces and answers for a set of prompts, which are filtered for quality. The small models, taken from open base families such as Qwen and Llama, are then fine-tuned on these traces with the ordinary next-token objective. The step is supervised learning, so it does not need a reward model at the small scale.

## Results

The abstract states that reasoning patterns discovered by a larger model can be systematically harnessed to guide and enhance the reasoning capabilities of smaller models. The paper reports that distilled models outperform reinforcement learning applied directly to small models. Benchmark numbers are in the paper.

## Limitations

The student's reasoning is bounded by the teacher's, and the training data are long traces, which are expensive to generate. The paper does not isolate every factor in the comparison, so the gap depends on the benchmarks chosen.

## Open issues and related variants

- **Faithfulness.** Whether a student's reasoning follows the teacher's steps, or only imitates their form, is open.
- **Generalisation.** Reasoning learned on mathematics and code may not transfer to other domains.
- **Related:** [MiniLLM](../minillm/index.md) trains the student on its own samples rather than on fixed traces, which reduces the mismatch between training and generation.

## Connections

The idea that reasoning can be taught by imitation connects to the [language model](../../../../../theory/models/llm/index.md) page, where chain-of-thought behaviour is discussed. The cost of producing traces is a [training](../../../../../engineering/training/index.md) concern.

## References

### Seminal papers

- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948. https://arxiv.org/abs/2501.12948 — Shows that reasoning patterns from a large model can be harnessed to enhance smaller models.
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — The earlier teacher-output method, which trains on the teacher's best sequences.
- Gu, Y., Dong, L., Wei, F., Huang, M. (2023). *MiniLLM: On-Policy Distillation of Large Language Models*. arXiv:2306.08543. https://arxiv.org/abs/2306.08543 — On-policy distillation, the alternative that trains on the student's own samples.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation, the background for training smaller models on a teacher's outputs.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The original distillation objective, which reasoning distillation extends to text.
