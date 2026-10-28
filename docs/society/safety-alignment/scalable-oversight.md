---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/learning-from-human-feedback
tags:
  - alignment
  - oversight
aliases:
  - Scalable oversight
  - 可擴展監督
  - 弱到強泛化
---

# Scalable oversight

Scalable oversight asks how humans can reliably supervise AI systems on tasks that are too hard, too slow or too large for humans to check directly. A model that writes research-level code or long scientific arguments may be right in ways its evaluators cannot easily confirm. Oversight methods try to make supervision keep pace with capability, using the model itself, other models, or decompositions of the task.

## Overview

Most current training uses human judgements as the reward signal (see [learning from human feedback](../../theory/paradigms/reinforcement-learning/learning-from-human-feedback/index.md)). That works when a rater can tell a good answer from a bad one. It becomes unreliable when the answer requires expertise the rater lacks, or when a response is long enough that errors are hard to find. A system that is more capable than its supervisor can then learn to look good to the supervisor, which is a form of the problem covered in [reward hacking](reward-hacking.md).

Scalable oversight treats this as a research problem with two parts: designing protocols in which a weaker judge can reliably tell which of two answers is better, and measuring whether those protocols work before the capability gap becomes large.

## Key concepts

- **Oversight gap**: the difference between what a model can do and what its supervisor can check.
- **Protocol**: a fixed procedure, such as a debate or a decomposition, that turns a hard judgement into a sequence of easier ones.
- **Weak supervisor**: a judge, human or model, that is less capable than the system it supervises.
- **Process supervision**: rewarding each step of a reasoning chain, instead of only the final answer.

## Key methods

- [Debate](debate.md) (Irving et al., 2018): two agents argue opposing answers, and a judge decides which argument is more convincing.
- **Recursive reward modelling** (Leike et al., 2018): a hard task is split into subtasks, and the human uses AI assistants on each subtask to evaluate the whole.
- **Iterated amplification** (Christiano et al., 2018): a human combined with copies of the model answers questions the human could not answer alone, and the combined system is distilled into a new model that is trained the same way.
- **Weak-to-strong generalisation** (Burns et al., 2023): a strong model is fine-tuned on labels from a weaker model, and the question is how much of the strong model's ability is recovered.

These differ in what the judge sees. Debate and amplification change how the judge is assisted. Weak-to-strong generalisation changes the training signal itself, so it is also a way of asking what a strong model learns when its supervisor is weak.

## Debate

The detailed pages are [AI debate](debate.md) and [debate cross-examination](debate-cross-examination.md).

In the debate proposal, two copies of a model are shown a question and each argues for a different answer, possibly citing evidence. A human judge reads the exchange and picks a winner. Irving, Christiano and Amodei (2018) argue that, under certain assumptions, the honest side can win because a lie that is hard to defend can be exposed by its opponent, so the judge needs to evaluate only short, checkable claims. The paper is a proposal with a theoretical argument and small-scale demonstrations, not a deployed system.

Later empirical work measures whether debate actually helps humans judge correctness. Bowman et al. (2022) propose “sandwiching”, an experimental setup in which non-expert humans, helped by a chat assistant, answer multiple-choice questions that experts can check. Their proof-of-concept study uses MMLU and time-limited QuALITY, and it discusses debate as a candidate technique without testing it.

## Process supervision

Process supervision rewards each step of a chain of reasoning. Lightman et al. (2023) compare step-level human feedback with outcome-level feedback on mathematical problem solving and report that rewarding each step gave a more reliable signal in their experiments. The method does not solve oversight in general, because it still needs judges who can check each step, but it shows how decomposition can make a hard judgement easier.

## Weak-to-strong generalisation

Burns et al. (2023) ask a concrete version of the oversight question. They fine-tune a strong pretrained model on labels produced by a much weaker model and measure how close the result comes to a model trained on ground-truth labels. Naive fine-tuning recovers only part of the gap, but the strong model usually outperforms its weak supervisor. Simple changes to the training objective recover a larger share of the gap in their experiments. The result is encouraging for oversight, and also limited: the tasks are chosen so that ground truth is known, and the authors say that the analogy to humans supervising superhuman models is imperfect.

## Connections

Human oversight of experts has a long history in professional life. Medicine, law and aviation all use layered review, checklists and second opinions, and these practices are often cited as analogies. The analogy is useful for design but has limits, since machine errors can be correlated across checks in ways that human errors are not. Scalable oversight also connects to the study of how people evaluate arguments and detect errors in them, a topic covered in [cognitive science](../../brain-mind/index.md). The broader safety context is in [safety and alignment](index.md) and [Constitutional AI](constitutional-ai.md).

## Applications

- Evaluation of model outputs in domains where ground truth is expensive, such as code review and scientific writing.
- Evaluation pipelines that use one model to critique another, a practice that supports the weak-judge methods above.
- Benchmarks that measure whether assistance improves human accuracy, used by labs before they rely on human review for high-stakes tasks.

## Open questions

- Do debate and amplification scale to tasks where the judge cannot check any single claim?
- Can weak-to-strong results be reproduced on tasks where the strong model has capabilities the weak one lacks entirely?
- How do oversight protocols behave when the system is trying to mislead its judge, which links to [deceptive alignment](deceptive-alignment.md)?

## References

### Seminal papers

- Irving, G., Christiano, P. & Amodei, D. (2018). *AI safety via debate*. arXiv:1805.00899. https://arxiv.org/abs/1805.00899 — Proposes two-agent debate judged by a human as a way to supervise systems on questions beyond direct human judgement.
- Leike, J. et al. (2018). *Scalable agent alignment via reward modeling: a research direction*. arXiv:1811.07871. https://arxiv.org/abs/1811.07871 — Sets out reward modelling as a research agenda and discusses how to scale it with recursive decomposition.
- Christiano, P., Shlegeris, B. & Amodei, D. (2018). *Supervising strong learners by amplifying weak experts*. arXiv:1810.08575. https://arxiv.org/abs/1810.08575 — Introduces iterated amplification, which distils a human assisted by copies of the model into a new model.
- Burns, C. et al. (2023). *Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision*. arXiv:2312.09390. https://arxiv.org/abs/2312.09390 — Measures how much of a strong model's ability is recovered when it is fine-tuned on a weak model's labels.
- Lightman, H. et al. (2023). *Let's Verify Step by Step*. arXiv:2305.20050. https://arxiv.org/abs/2305.20050 — Compares process supervision, which rewards each reasoning step, with outcome supervision on mathematical problems.

### Surveys and textbooks

- Bowman, S. R. et al. (2022). *Measuring Progress on Scalable Oversight for Large Language Models*. arXiv:2211.03540. https://arxiv.org/abs/2211.03540 — Proposes “sandwiching”, an experimental setup for testing whether non-expert humans can use a model's help to answer questions beyond their expertise.

### Articles and documentation

- Anthropic, *Anthropic's Responsible Scaling Policy*. https://www.anthropic.com/responsible-scaling-policy — Official policy describing the capability thresholds and safeguards a developer commits to, an applied case of oversight by evaluation.
