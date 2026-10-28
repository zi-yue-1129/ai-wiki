---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
---

# Reasoning and Agent Benchmarks

This family asks whether a system can acquire a new rule from a few examples and apply it, rather than recall a fact or follow a known procedure. The benchmarks are designed so that memorised knowledge does not solve them.

| Benchmark | Task | Main metric |
|---|---|---|
| [ARC-AGI](arc-agi.md) | Infer a grid transformation from examples | Exact match on the output grid |

## Common issues

- **Small test sets.** A few tasks can change the score a lot.
- **Scaffold and search.** Prompting and search methods change results, so systems are hard to compare.
- **Leaderboard pressure.** Hidden test sets matter when public examples can be tuned against.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Few-shot](../few-shot/index.md) tests learning from few examples in a classification setting.

## References

### Seminal papers

- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Proposes skill-acquisition efficiency as a definition of intelligence and introduces ARC.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Introduces in-context few-shot prompting, the usual way these tasks are attempted.

### Articles and documentation

- Chollet, F. & Knoop, M. et al. (2025). *ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems*. arXiv. https://arxiv.org/abs/2505.11831 — Introduces a harder version designed to challenge frontier systems.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that intermediate reasoning steps change results on reasoning tasks.
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Describes how benchmarks for reasoning should be designed and reported.
