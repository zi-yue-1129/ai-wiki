---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
aliases:
  - Reasoning and agent benchmarks
  - 推理與代理基準
---

# Reasoning and Agent Benchmarks

This family asks whether a system can acquire a new rule from a few examples and apply it, rather than recall a fact or follow a known procedure. Agent benchmarks add the question of whether it can carry out multi-step tasks with tools or inside a web environment. The benchmarks are designed so that memorised knowledge alone does not solve them.

## Overview

Chollet (2019) argues that skill on a fixed task is a weak measure of intelligence, because skill depends heavily on prior knowledge and experience. Using that view, he introduced the Abstraction and Reasoning Corpus (ARC), in which each task shows a few input-output grid pairs and asks the solver to infer the rule and apply it to a new input. ARC-AGI-2 (Chollet et al., 2025) keeps the same input-output format but adds a newly curated set of harder tasks and reports human testing to calibrate their difficulty.

Agent benchmarks ask a related question in a different setting. GAIA contains 466 real-world questions that need reasoning, browsing and tool use. The authors report that humans answered 92% of them correctly, while GPT-4 with plugins reached 15% (Mialon et al., 2023). WebArena places an agent in self-hosted copies of four websites, covering e-commerce, social forum discussion, collaborative software development and content management, and scores whether the task was completed correctly (Zhou et al., 2023).

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [ARC-AGI](arc-agi.md) | Infer a grid transformation from examples | Exact match on the output grid |
| [GAIA](gaia.md) | Real-world questions that need browsing and tools | Exact-match accuracy |
| [WebArena](webarena.md) | Tasks on self-hosted websites | Task success rate, judged by functional correctness |

ARC-style tasks are scored strictly: an output grid is either exactly right or wrong. Agent tasks are scored by the final state of the environment or the final answer, so a run can fail after many correct steps. The two scoring rules measure different things, and a single number does not compare them directly.

## Key concepts

- **Few-shot rule induction**: infer a rule from a small number of demonstrations and apply it to an unseen input.
- **Functional correctness**: judged by the outcome of an action, such as whether the order was placed, not by comparing the action sequence with a reference.
- **Scaffold**: the prompting, search and tool loop around a model. In agent benchmarks, the scaffold is part of the system being measured.

## How it works

A typical run gives the system a task description and, for agent benchmarks, access to tools or a browser. The score counts only the final outcome. Prompting methods change results substantially: chain-of-thought prompting, which asks a model to write intermediate reasoning, improved performance on reasoning tasks (Wei et al., 2022). Few-shot prompting, in which a language model is given demonstrations in its input without any gradient updates, is the usual way these tasks are attempted with large models (Brown et al., 2020).

## Common issues

- **Small test sets.** A few tasks can change the score a lot, so confidence intervals matter.
- **Scaffold and search.** Prompting and search methods change results, so systems are hard to compare unless the scaffold is reported.
- **Leaderboard pressure.** Public examples can be tuned against. Hidden test sets and held-out tasks reduce this risk.
- **Environment drift.** Live websites change over time. Self-hosted copies, as in WebArena, keep runs reproducible.

## Connections

- [Math and code](../math-and-code/index.md) covers the reasoning benchmarks with checkable answers.
- [Agents](../../../models/agents/index.md) describes the systems these benchmarks evaluate.
- [Few-shot](../few-shot/index.md) tests learning from few examples in a classification setting.

## Open questions

- Whether a fixed rule-induction benchmark can be designed that is hard for search-based systems but still easy for people.
- How to score long agent tasks when partial progress matters and a single failed step ends the run.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Multimodal](../multimodal/index.md) covers tasks that combine images with reasoning.

## References

### Seminal papers

- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Argues that skill on a task is a weak measure of intelligence and introduces the ARC task format.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Introduces in-context few-shot prompting with GPT-3, the usual way these tasks are attempted.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that intermediate reasoning steps improve results on arithmetic, commonsense and symbolic reasoning.

### Articles and documentation

- Chollet, F., Knoop, M., Kamradt, G., Landers, B. & Pinkard, H. (2025). *ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems*. arXiv. https://arxiv.org/abs/2505.11831 — Introduces the harder ARC-AGI-2 tasks, keeping the input-output format, with human testing results.
- Mialon, G. et al. (2023). *GAIA: a benchmark for General AI Assistants*. arXiv. https://arxiv.org/abs/2311.12983 — Introduces 466 real-world questions and reports human and GPT-4 results.
- Zhou, S. et al. (2023). *WebArena: A Realistic Web Environment for Building Autonomous Agents*. arXiv. https://arxiv.org/abs/2307.13854 — Introduces the self-hosted website environment and functional-correctness tasks.
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Introduces BIG-bench, 204 tasks contributed by 450 authors across 132 institutions, covering topics from linguistics to physics.
