---
status: draft
last_reviewed: 2026-10-28
tags:
- agents
- evaluation
- benchmarks
aliases:
- WebArena
- 可重現網路環境
- 網頁代理人基準
---

# WebArena: Reproducible Web Environments for Agents

WebArena (Zhou et al., 2023) provides self-hosted, fully functional websites from four common domains, together with benchmark tasks scored by checking the outcome. It is one of three landmark methods on the [Agent Evaluation](../index.md) page, and the web counterpart of the desktop environments described in [OSWorld](../../sandboxing-and-computer-use/osworld/index.md).

## Overview

Before WebArena, agents were tested either in simplified synthetic environments or on live websites. Synthetic environments lack realism. Live websites change without notice, and their state cannot be restored, so a result cannot be repeated. WebArena builds working copies of four kinds of site: e-commerce, social forum discussions, collaborative software development and content management. It adds tools, such as a map, and knowledge sources, such as user manuals, to encourage human-like problem solving (Zhou et al., 2023).

The benchmark tasks are long-horizon and resemble routine work on the internet. They are judged by their functional correctness, meaning whether the task was actually accomplished.

## Key concepts

- **Self-hosted environment**: the sites run locally in a fixed version, so the same action produces the same result.
- **Reset**: the site's data is restored before each run, so attempts do not affect one another.
- **Functional correctness**: success is judged by the outcome, such as the right order being placed or the right page being reached, not by matching a reference sequence of clicks.
- **Long-horizon task**: a task that takes many steps, each of which changes the page the agent sees next.

## How it works

1. Start the self-hosted sites from a known image and reset their data.
2. Give the agent a natural-language intent, such as a request about an order or a repository.
3. The agent reads the current page and issues a browser action, such as clicking, typing or navigating.
4. The environment returns the new page. Steps 3 and 4 repeat until the agent stops or reaches a step limit.
5. An evaluator checks the outcome. Depending on the task, it inspects the final state of the site, or compares the answer the agent returned with a reference.

Because each task has its own check, the quality of the benchmark depends on how carefully those checks were written.

## Results

The paper's abstract reports that the best GPT-4-based agent reaches an end-to-end task success rate of 14.41 percent, against 78.24 percent for humans on the same tasks (Zhou et al., 2023). The baseline agents included recent techniques such as reasoning before acting. The gap is the paper's main evidence that current models were far from reliable on realistic web tasks at the time.

The numbers describe agents from 2023. Later systems have improved considerably, so the gap should be read as a historical snapshot rather than a current measure.

## Limitations

- **Simplified copies.** Self-hosted sites are more stable and tidier than the live web, and they cover only four domains. Their reproducibility is bought at the price of realism.
- **Outcome checks.** A check written for one intended path can reject a correct result reached differently, and a narrow check can accept a wrong one.
- **Human baseline.** The human figure comes from the paper's own annotators under its own conditions, so it is a reference point rather than a population estimate.
- **Text-first observation.** The original tasks are built around text and page structure, which leaves out visual content until a later extension.

## Open questions

- **Visual grounding.** VisualWebArena extends the approach to tasks that need images and visually grounded reasoning (Koh et al., 2024). How much of the difficulty of web agents comes from vision rather than from navigation is not settled.
- **Keeping environments current.** Realistic sites age. How to update them without breaking comparisons across versions is an open maintenance problem.
- **Measuring usefulness.** A functional check confirms that a task was completed, not that the user found the result acceptable.

## References

### Seminal papers

- Zhou, S. et al. (2023). *WebArena: A Realistic Web Environment for Building Autonomous Agents*. arXiv. https://arxiv.org/abs/2307.13854 — Self-hosted, functional websites from four domains, with benchmark tasks scored by functional correctness.
- Koh, J. Y. et al. (2024). *VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks*. arXiv. https://arxiv.org/abs/2401.13649 — Extends the web-agent approach to visually grounded tasks that require image understanding.
- Xie, T. et al. (2024). *OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments*. arXiv. https://arxiv.org/abs/2404.07972 — Execution-based benchmark for agents on real operating systems, the desktop counterpart of WebArena.
- Liu, X. et al. (2023). *AgentBench: Evaluating LLMs as Agents*. arXiv. https://arxiv.org/abs/2308.03688 — Eight interactive environments for assessing LLMs as agents, with an analysis of why agents fail in them.

### Surveys and textbooks

- Yehudai, A. et al. (2025). *Survey on Evaluation of LLM-based Agents*. arXiv. https://arxiv.org/abs/2503.16416 — Survey of agent evaluation that treats web agents as an application benchmark category.

### Articles and documentation

- Kapoor, S. et al. (2024). *AI Agents That Matter*. arXiv. https://arxiv.org/abs/2407.01502 — Critique of agent benchmarking that argues for reporting cost with accuracy.
