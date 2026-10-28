---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/agents
tags:
  - agents
  - reinforcement learning
  - memory
aliases:
  - Reflexion
  - Verbal Reinforcement Learning
  - 語言回饋強化
  - 反思式代理
---

# Reflexion (Shinn et al., 2023)

Reflexion is a framework that improves a language agent across repeated attempts without changing its weights. After each failed attempt, the agent writes a verbal reflection on the feedback it received and stores that reflection in a memory buffer, which conditions the next attempt. Shinn et al. (2023) introduced it and reported gains on decision-making, coding and reasoning tasks.

This page is part of [Agent Engineering](index.md). It is one of the named methods behind the agent engineering section.

## Overview

Traditional reinforcement learning improves an agent by many gradient updates over many episodes, which is costly for a large language model. Reflexion takes a different route. Instead of changing weights, it changes the context: the agent learns from the outcome of a trial in the form of text, and carries that text into the next trial.

## Problem

A language agent that interacts with an environment, such as a game, a compiler or an API, can fail the same way repeatedly. Fine-tuning after each failure is slow and expensive. The problem is how an agent can learn quickly from trial and error without a large training run.

## Core idea

Reflexion has three roles. An actor produces a trajectory of actions in the environment. An evaluator scores the trajectory, using a signal that can be a scalar value or free-form language, from an external source or from a simulated check. A self-reflection step then writes a short verbal analysis of what went wrong and what to try next. The reflection is kept in an episodic memory buffer, and the actor reads it at the start of the next trial. The paper states that the feedback can be scalar or language and can come from outside the agent or be simulated inside it.

## Equation or algorithm

For each task, repeat for a fixed number of trials:

1. The actor runs an attempt, guided by the current task and the stored reflections.
2. The evaluator scores the attempt.
3. If the attempt succeeds, stop. Otherwise, the self-reflection step writes a reflection from the trajectory and the feedback.
4. The reflection is appended to the memory buffer, and the next trial begins.

No weights change during this loop.

## Results

The abstract reports that Reflexion obtains significant improvements over a baseline agent across sequential decision-making, coding and language reasoning tasks. On the HumanEval coding benchmark it reaches 91% pass@1, above the 80% that the abstract gives for GPT-4 as the previous state of the art. The paper also reports ablations on feedback types, feedback incorporation methods and agent types. On AlfWorld, Reflexion improves on ReAct by an absolute 22% over 12 learning trials.

## Limitations

- **Depends on feedback quality.** A weak evaluator gives weak reflections, and the reflections can encode a wrong lesson.
- **Context grows with memory.** Stored reflections use the context window, so long memories need selection.
- **Repeated attempts cost more.** Gains come from extra trials, so the comparison with single-attempt systems depends on the budget used.
- **Benchmark scope.** The reported results cover the tasks in the paper; generalisation to open-ended settings is an open question.

## Connections

- Reflexion builds on the loop in [ReAct](react.md), adding feedback across trials.
- The reinforcement-learning framing, in which feedback signals drive improvement, is on [Reinforcement Learning](../../theory/paradigms/reinforcement-learning/index.md).
- Episodic memory and its role in learning are described on [Memory & Learning in the Brain](../../brain-mind/memory-learning/index.md).
- Coding benchmarks in which such agents are tested include [HumanEval](../../theory/evaluation/benchmarks/math-and-code/humaneval.md).

## Applications

- Coding agents that run tests, read failures and retry.
- Game or simulation agents that learn a strategy across episodes without retraining.

## Open questions

- How should a reflection be checked before it is stored?
- When does verbal memory stop helping and start to mislead?

## References

### Seminal papers

- Shinn, N. et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS. https://doi.org/10.52202/075280-0377 — Introduces Reflexion, which stores verbal reflections in an episodic memory to improve later trials without weight updates.
- Yao, S. et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR. https://arxiv.org/abs/2210.03629 — The reasoning-and-acting loop that Reflexion extends.
- Madaan, A. et al. (2023). Self-Refine: Iterative Refinement with Self-Feedback. NeurIPS. https://doi.org/10.52202/075280-2019 — Refines outputs through iterated self-feedback, a related idea without an episodic memory across tasks.
- Chen, M. et al. (2021). Evaluating Large Language Models Trained on Code. arXiv. https://arxiv.org/abs/2107.03374 — Introduces HumanEval and the pass@k measure used to score coding attempts.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering reflection and memory in agent design.
