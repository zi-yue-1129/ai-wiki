---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/evaluation/benchmarks/reasoning-agents
tags:
  - agents
  - evaluation
  - benchmarks
aliases:
  - Agent Evaluation
  - Agent Benchmarks
  - 代理評估
  - 代理基準測試
---

# Agent evaluation

Evaluating an agent means judging what it does over a sequence of steps in an environment, not only the final text. A correct answer can come from a poor process, and a sound process can fail on a small detail. Agent evaluation therefore checks trajectories and end states, and it counts cost and reliability along with success.

This page is part of [Agent Engineering](index.md).

## Overview

Question-answering benchmarks grade one response. Agents act across many turns, call tools and change state, so a benchmark needs an environment, a way to run the agent in it, and a check on the outcome. The check can be a program that inspects the final state, a grader model, or a human. Each choice trades cost against accuracy and against how easily the result can be reproduced.

## Key concepts

- **Task success rate:** the share of tasks whose end state meets the goal.
- **Trajectory:** the full sequence of observations, tool calls and outputs during a run.
- **Environment state:** the data that the task changes, such as a database or a web page, against which success is checked.
- **Simulated user:** a language model that plays the user in a dialogue, so that the agent can be tested in conversation.
- **pass^k:** the probability that an agent succeeds on all of k independent attempts at the same task. It measures reliability, which a single run cannot show.
- **Cost per task:** the model and tool cost needed to complete a task.

## How it works

A typical evaluation follows the same steps. The harness sets the task and initial state. The agent runs with a fixed set of tools. The run is logged as a trajectory. A checker compares the end state with the goal. The results are aggregated over tasks and over repeated runs, because a single run hides variance. The harness and tools must be the same across the systems being compared.

## Benchmarks

- **AgentBench** (Liu et al., 2023) evaluates language models as agents in eight distinct environments, and reports a large gap between commercial and open models.
- **WebArena** (Zhou et al., 2023) uses realistic, reproducible websites in four domains: e-commerce, social forums, collaborative software development and content management.
- **OSWorld** (Xie et al., 2024) uses a real computer environment, so that tasks are not confined to one application.
- **τ-bench** (Yao et al., 2024) emulates dialogues with a simulated user, in which the agent uses domain tools and follows policy guidelines. It compares the database state at the end of a conversation with an annotated goal state, and proposes pass^k as a reliability metric.
- **GAIA** (Mialon et al., 2023) tests general assistant tasks that need tools and multi-step reasoning. See [GAIA](../../theory/evaluation/benchmarks/reasoning-agents/gaia.md) for its own page.

## Critiques of current practice

Kapoor et al. (2024) argue that agent benchmarks focus narrowly on accuracy and so ignore cost. They show that some accuracy gains come from costly designs, and they propose reporting cost and accuracy together. Their analysis is a warning against comparing agents on success alone.

## Limitations

- **Grader errors.** A checker that is too strict or too loose changes the score.
- **Contamination.** Public tasks may appear in training data.
- **Variance.** A few tasks and a single run can give a misleading ranking.
- **Simplified environments.** A benchmark is a model of the real task, and gaps between the two affect the result.

## Connections

- Reasoning and agent benchmarks, including [ARC-AGI](../../theory/evaluation/benchmarks/reasoning-agents/arc-agi.md) and [WebArena](../../theory/evaluation/benchmarks/reasoning-agents/webarena.md), are on [Reasoning and Agent Benchmarks](../../theory/evaluation/benchmarks/reasoning-agents/index.md).
- General evaluation practice, including LLM-as-judge and contamination, is on [Evaluation & Benchmarks](../evaluation/index.md).
- Traces recorded in production can feed evaluation; see [Agent observability](agent-observability.md).

## Applications

- **Regression testing** of an agent before each release.
- **Comparing models or tools** for a fixed workflow, with cost reported next to success.
- **Safety testing**, where the environment includes tasks that should be refused.

## Open questions

- How can an evaluation be cheap enough to run often and still reflect real use?
- How should graders for open-ended outputs be validated?
- Which reliability measures matter for a deployed agent, beyond pass^k?

## References

### Seminal papers

- Liu, X. et al. (2023). AgentBench: Evaluating LLMs as Agents. arXiv. https://arxiv.org/abs/2308.03688 — A multi-dimensional benchmark of eight interactive environments for assessing LLM agents.
- Zhou, S. et al. (2023). WebArena: A Realistic Web Environment for Building Autonomous Agents. arXiv. https://arxiv.org/abs/2307.13854 — Reproducible websites in four domains for evaluating web agents.
- Xie, T. et al. (2024). OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments. arXiv. https://arxiv.org/abs/2404.07972 — A real computer environment for evaluating multimodal agents on open-ended tasks.
- Yao, S. et al. (2024). τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. arXiv. https://arxiv.org/abs/2406.12045 — Simulated-user dialogues with domain tools and policies, checked against database state, with the pass^k reliability metric.
- Mialon, G. et al. (2023). GAIA: a benchmark for General AI Assistants. arXiv. https://arxiv.org/abs/2311.12983 — Benchmark of general assistant tasks that need reasoning, tools and browsing.

### Surveys and textbooks

- Kapoor, S. et al. (2024). AI Agents That Matter. arXiv. https://arxiv.org/abs/2407.01502 — Critiques agent benchmarks for their narrow focus on accuracy and proposes evaluating cost alongside accuracy.
