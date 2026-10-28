---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/llm
- engineering/training
tags:
- model compression
- knowledge distillation
- on-policy distillation
- large language models
aliases:
  - MiniLLM
  - On-policy distillation
  - Reverse KL distillation
  - 同策略蒸餾
---

# MiniLLM

MiniLLM distils a large language model by training the student on its own generated text, scored by the teacher, rather than on the teacher's text alone. Gu et al. replace the usual forward KL divergence with a reverse KL, which stops the student from putting probability on regions the teacher finds unlikely. The paper reports that the method scales across model families from 120 million to 13 billion parameters. It is an [on-policy](../index.md) method within [language-model distillation](../index.md), and the closest relative of [sequence-level distillation](../sequence-level/index.md).

## Problem

Standard distillation of a language model trains the student on sequences that the teacher produces or the teacher's distribution over them. At generation time, however, the student produces its own sequences. Early errors then compound, because the student reaches states it never saw during training. The forward KL used in standard distillation also encourages the student to spread probability over every mode of the teacher, including those it cannot match well.

## Core idea

Sample responses from the student, and ask the teacher how likely it finds each one. Train the student on its own samples with a reverse KL, which is mode-seeking: the student concentrates on outputs the teacher finds likely, rather than covering all of the teacher's distribution.

## Equation or algorithm

Write \(p\) for the teacher's distribution and \(q_\theta\) for the student's. Standard distillation minimises the forward KL \(\mathrm{KL}(p \Vert q_\theta)\). MiniLLM instead minimises the reverse KL \(\mathrm{KL}(q_\theta \Vert p)\), which the paper optimises on the student's own samples. Since sampling is not differentiable, the gradient is estimated with a policy-gradient style method, and the paper adds techniques to reduce its variance and to stabilise training over long generations.

## Results

The abstract reports that the method is scalable for different model families with 120 million to 13 billion parameters. Comparisons with baselines on instruction-following and other tasks are reported in the paper.

## Limitations

The policy-gradient style update is more complex and costlier than supervised distillation, and it needs the teacher to score the student's samples during training. The stability of the optimisation over long generations is a practical concern.

## Open issues and related variants

- **Choice of divergence.** Reverse KL is mode-seeking, and forward KL is mode-covering. Which divergence suits a given task, and whether a mix of the two is better, is not settled.
- **Cost of on-policy sampling.** Generating samples from the student at every step is expensive, and cheaper schemes that reuse samples are an open area.
- **Related:** [sequence-level distillation](../sequence-level/index.md) trains on the teacher's outputs, which avoids the on-policy cost but suffers the mismatch that MiniLLM addresses.

## Connections

On-policy training is a reinforcement-learning idea, which links the method to the [training](../../../../../engineering/training/index.md) pipeline and to the [language model](../../../../../theory/models/llm/index.md) page, where post-training with feedback is discussed.

## References

### Seminal papers

- Gu, Y., Dong, L., Wei, F., Huang, M. (2023). *MiniLLM: On-Policy Distillation of Large Language Models*. arXiv:2306.08543. https://arxiv.org/abs/2306.08543 — Trains the student on its own samples with reverse KL, scalable from 120 million to 13 billion parameters.
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — The teacher-output method that MiniLLM improves on, with a 10 times faster student.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The forward-KL soft-target objective that the method replaces with reverse KL.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation and the divergences used to match the teacher.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948. https://arxiv.org/abs/2501.12948 — A later large-scale use of teacher-generated reasoning to train smaller models.
