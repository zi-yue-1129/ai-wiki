---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/continual
tags:
  - agents
  - lifelong learning
  - embodied AI
aliases:
  - Voyager
  - Minecraft Agent
  - 終身學習代理
  - 技能庫
---

# Voyager (Wang et al., 2023)

Voyager is a language-model agent that plays Minecraft, explores the world on its own and keeps the skills it learns. It writes executable code for each skill, saves that code in a growing skill library, and retrieves it when a similar task comes up. Wang et al. (2023) introduced it with GPT-4 as the model, without fine-tuning.

This page is part of [Agent Engineering](index.md). It is one of the named methods in the section, and an example of how an agent can learn over time without changing its weights.

## Overview

A game such as Minecraft offers an open-ended world with many tasks, and an agent that keeps learning needs to build on what it has already done. Earlier agents in such settings either followed a fixed script or learned from scratch each time. Voyager combines three components so that it can keep discovering new things and remember what it has learned.

## Problem

Lifelong learning requires an agent to acquire new abilities without forgetting old ones and without a full retraining run for each new skill. The question Voyager addresses is how a language model agent can explore an open world, choose what to learn next, and reuse what it has learned, all through black-box queries to a model.

## Core idea

Voyager has three components. First, an automatic curriculum proposes the next task so as to maximise exploration. Second, a skill library stores executable code for skills that worked, and retrieves them later by embedding the task plan and environment feedback, so that complex behaviours are built from simpler ones. Third, an iterative prompting mechanism improves a program using environment feedback, execution errors and self-verification. The skills are temporally extended and compositional, which the authors argue allows abilities to compound and reduces catastrophic forgetting.

## Equation or algorithm

For each iteration:

1. The curriculum proposes a task based on what the agent has explored and what it can already do.
2. The model writes code for a skill, using relevant skills retrieved from the library.
3. The code runs in the environment. Errors, environment feedback and a self-verification by a separate GPT-4 critic are fed back, and the program is revised until the task succeeds or the attempt limit is reached.
4. A verified skill is added to the library, where later tasks can retrieve it.

## Results

The abstract reports that Voyager obtains 3.3 times more unique items, travels 2.3 times longer distances and unlocks key tech-tree milestones up to 15.3 times faster than prior state-of-the-art methods, in Minecraft. It also reports strong in-context lifelong learning.

## Limitations

- **Specific environment.** The results are in Minecraft, where actions and feedback are structured. Transfer to less structured environments is not established by the paper.
- **Dependence on a strong model.** The method uses GPT-4 through black-box queries, so its performance depends on that model.
- **Code as the skill format.** Skills expressed as code are inspectable and reusable, but they only cover what the environment's interface can express.
- **Retrieval errors.** A wrong skill retrieved from the library can be reused in the wrong situation.

## Connections

- The problem of learning without forgetting is the subject of [Continual Learning](../../theory/paradigms/continual/index.md).
- The reasoning-and-acting loop that Voyager builds on is [ReAct](react.md).
- Verbal feedback across attempts is compared with weight-based learning in [Reflexion](reflexion.md).
- Skill libraries resemble the way people store procedures; the memory literature is on [Memory & Learning in the Brain](../../brain-mind/memory-learning/index.md).

## Applications

- Game-playing agents that build up skills over long sessions.
- Simulation agents that reuse verified code for recurring subtasks.

## Open questions

- How can a skill library be kept free of skills that worked once by accident?
- Does the curriculum generalise beyond environments with clear progress measures?

## References

### Seminal papers

- Wang, G. et al. (2023). Voyager: An Open-Ended Embodied Agent with Large Language Models. arXiv. https://arxiv.org/abs/2305.16291 — Introduces Voyager, with an automatic curriculum, an executable skill library and iterative prompting in Minecraft.
- Yao, S. et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR. https://arxiv.org/abs/2210.03629 — The reasoning-and-acting approach on which the agent's action loop is built.
- Shinn, N. et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. arXiv. https://arxiv.org/abs/2303.11366 — Shows how language agents learn across attempts from verbal feedback, a contrast to skill libraries.
- Park, J. S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv. https://arxiv.org/abs/2304.03442 — Interactive agents with memory in a shared environment, a related use of stored experience.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering memory, planning and tool use.
