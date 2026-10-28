---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
---

# WebArena

WebArena is a reproducible environment for language-guided agents that perform tasks on websites. It provides fully functional sites from four common domains: e-commerce, social forum discussion, collaborative software development and content management. The sites come with tools such as a map and external knowledge sources (Zhou et al., 2023).

## Task and data

An agent receives a natural-language instruction, such as a purchase, a post or a repository change, and must act through a browser on the sites. Because the environment is self-hosted, every run starts from the same state, which makes results comparable across systems (Zhou et al., 2023).

## Protocol and metric

Success is judged by whether the final state of the website meets the goal, rather than by the agent's text. The metric is **task success rate**. The result depends on the observation format, the action space and the step limit, so these must be reported with the score.

## What it shows

Realistic web tasks are hard for agents built on current models, and the gap between the best agent and a person is large. The benchmark was built because agents tested in simplified synthetic settings did not transfer to real websites (Zhou et al., 2023).

## Limitations

- **Simulated sites.** The sites are realistic copies, not the live web, so behaviour on the open internet can differ.
- **Four domains.** Coverage is limited to four types of site.
- **Observation design.** How the page is shown to the model, as text, screenshot or accessibility tree, changes results a great deal.
- **Step limits.** Long tasks are sensitive to the budget, so scores at different budgets are not comparable.

## Related

- [GAIA](gaia.md) tests assistants on open-web questions.
- [SWE-bench](../math-and-code/swe-bench.md) tests agents on software repositories with tests as the judge.
- [Reasoning and agents family overview](index.md) compares the benchmarks in this area.

## References

### Seminal papers

- Zhou, S. et al. (2023). *WebArena: A Realistic Web Environment for Building Autonomous Agents*. arXiv. https://arxiv.org/abs/2307.13854 — Introduces the self-hosted websites, the tasks and the success-based evaluation.
- Mialon, G. et al. (2023). *GAIA: a benchmark for General AI Assistants*. arXiv. https://arxiv.org/abs/2311.12983 — A benchmark for assistants that use web browsing among other tools.

### Articles and documentation

- Yang, J. et al. (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. arXiv. https://arxiv.org/abs/2405.15793 — Shows that the interface an agent is given changes how many tasks it completes.
- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv. https://arxiv.org/abs/2310.06770 — A parallel benchmark for agents that act in a software environment.

### Additional sources

- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Reasoning steps that agents often use between observations and actions.
