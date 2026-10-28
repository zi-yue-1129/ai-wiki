---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# SWE-bench

SWE-bench evaluates language models on software engineering. It contains 2,294 problems drawn from real GitHub issues and their pull requests, across 12 popular Python repositories. The model must edit the codebase so that the issue is resolved (Jimenez et al., 2024).

## Task and data

Each task gives the model a codebase and an issue description. Resolving the issue often requires changes across several functions, classes or files, and the model may need to run code and read the test output (Jimenez et al., 2024).

## Protocol and metric

A candidate patch is applied to the repository and judged by the repository's tests. The tests that fail before the fix and pass after it decide success. The score is the fraction of tasks resolved. Because the outcome depends on the agent scaffold, such as how the model can read files and run commands, the scaffold must be reported with the score. Yang et al. (2024) show that a purpose-built agent-computer interface changes the results considerably.

## What it shows

The benchmark moved the evaluation of code models from function-level generation with unit tests (Chen et al., 2021) toward whole-repository tasks. It measures whether a system can work in a realistic codebase rather than complete a single function.

## Limitations

- **Language coverage.** All tasks are in Python.
- **Contamination.** The repositories and issues are public, so they may appear in training data.
- **Test quality.** Tests can be incomplete or flawed, so a patch may pass tests and still be wrong, or fail tests and still be correct.
- **Scaffold dependence.** The score reflects the model and the tools together, which makes model-to-model comparisons unreliable unless the scaffold is the same.

## Related

- [GSM8K](gsm8k.md) and [MATH](math.md) cover reasoning in mathematics.
- [Math and code family overview](index.md) compares the benchmarks in this area.

## References

### Seminal papers

- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv. https://arxiv.org/abs/2310.06770 — Introduces the 2,294 issues, the repository tests and the resolved-rate metric.
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces function-level code evaluation with unit tests and the pass@k metric.

### Articles and documentation

- Yang, J. et al. (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. arXiv. https://arxiv.org/abs/2405.15793 — Shows that the interface an agent uses changes how many issues it resolves.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Reasoning prompts that are often used alongside code agents.

### Additional sources

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Describes why benchmark design must account for how models are prompted and scaffolded.
