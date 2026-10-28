---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
---

# ARC-AGI

The Abstraction and Reasoning Corpus (ARC) was introduced by François Chollet as a benchmark for fluid intelligence rather than skill. Each task shows a few input-output grid pairs, and the solver must infer the transformation and apply it to a new input (Chollet, 2019). ARC-AGI is the name of the benchmark family, and ARC-AGI-2 is its later, harder version (Chollet et al., 2025).

## Task and data

Each task is a small coloured grid puzzle with a few demonstration pairs and one or more test inputs. The tasks rely on core priors such as objects, counting and symmetry, which the paper designs to be close to innate human priors (Chollet, 2019).

## Protocol and metric

A prediction is correct only if the output grid matches the answer exactly. The test is run with a limited number of attempts per task. Hidden test sets are kept by the organisers, which limits how often solvers can be tuned against them.

## What it shows

Chollet (2019) argues that measuring skill on a task says little about intelligence, because skill depends on prior knowledge and training data. The benchmark is designed so that a system must acquire the rule from a few examples, and it measures skill-acquisition efficiency rather than performance on a task that could be memorised.

## Limitations

- **Small test sets.** A small number of tasks means that a few solved puzzles change the score a lot.
- **Scaffold sensitivity.** Results depend heavily on the prompting and search method, so scores are hard to compare across systems.
- **Leaderboard pressure.** Public results can encourage tuning toward the visible examples, which is why the hidden test set matters.

## Related

- [GPQA](../language/gpqa.md) and [MMLU](../language/mmlu.md) test knowledge rather than skill acquisition.
- [Reasoning and agents family overview](index.md) describes this area.

## References

### Seminal papers

- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Proposes a definition of intelligence as skill-acquisition efficiency and introduces ARC.
- Chollet, F. & Knoop, M. et al. (2025). *ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems*. arXiv. https://arxiv.org/abs/2505.11831 — The harder successor, designed to be a new challenge for frontier systems.

### Articles and documentation

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — In-context few-shot prompting, a common way ARC-style tasks are attempted.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Intermediate reasoning steps, often used in attempts on grid-reasoning tasks.

### Additional sources

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Discusses how benchmarks should separate what models have learned from what they can do.
