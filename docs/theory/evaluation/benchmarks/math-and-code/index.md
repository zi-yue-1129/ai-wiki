---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
aliases:
  - Math and code benchmarks
  - 數學與程式基準
---

# Math and Code Benchmarks

These benchmarks test whether a model can reason through a problem with a checkable result: a number at the end of a word problem, a formal answer in competition mathematics, a function that passes unit tests, or a patch that makes a repository's tests pass. Because the result can be checked automatically, these tasks became a standard way to measure reasoning in language models.

## Overview

The first benchmark in the family, GSM8K, contains 8.5K grade-school word problems. Its authors found that even the largest transformer models of the time failed to reach high test accuracy, and they proposed training verifiers that rank many candidate solutions and select the best one. They reported that verification improved performance and scaled better with data than a fine-tuning baseline (Cobbe et al., 2021).

Competition mathematics is harder. The MATH dataset has 12,500 problems, each with a step-by-step solution. The authors report that accuracy stayed relatively low even with very large Transformer models, and that scaling alone was not solving the benchmark (Hendrycks et al., 2021).

Code benchmarks moved from single functions to whole repositories. HumanEval measures whether a generated Python function passes unit tests written for a docstring. The Codex paper reports that its model solved 28.8% of the problems, against 0% for GPT-3 and 11.4% for GPT-J, and that repeated sampling raised the solved share to 70.2% with 100 samples per problem (Chen et al., 2021). SWE-bench takes the task further: it uses 2,294 real GitHub issues from 12 Python repositories, and a model must edit the codebase so that the repository's tests pass (Jimenez et al., 2024).

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [GSM8K](gsm8k.md) | Grade-school word problems | Accuracy on the final number |
| [MATH](math.md) | Competition mathematics | Accuracy on the final answer |
| [HumanEval](humaneval.md) | Writing Python functions from docstrings | Fraction of problems passed, with repeated sampling reported as pass@k |
| [SWE-bench](swe-bench.md) | Resolving GitHub issues in Python repositories | Fraction of issues resolved by the repository's tests |

The first two check a final answer, so answer normalisation decides the score. The last two check behaviour: a program is judged by running it against tests, and an issue is judged by whether the patched repository passes them.

## Key concepts

- **Verifier**: a model or procedure that scores a candidate solution, used to choose among samples.
- **Repeated sampling**: drawing many solutions for one problem and counting a problem as solved if any sample passes. The number of samples must be reported with the score.
- **Scaffold**: the tools, prompts and loop around a model. For code agents, the scaffold is part of the result.

## How it works

For a math benchmark, the model writes a solution, the answer is extracted, and it is compared with the key after normalisation. For a code benchmark, the generated program or patch is run in a sandbox against held-out tests. Chain-of-thought prompting, which asks the model to write intermediate steps, improved results on GSM8K; the paper reports that a 540B-parameter model with eight examples exceeded a fine-tuned GPT-3 with a verifier (Wei et al., 2022).

## Common issues

- **Answer checking.** Equivalent answers written in different forms can be marked wrong, so the normaliser matters as much as the model.
- **Scaffold dependence.** Prompting, tool access and search change results, so two systems can differ mainly in their scaffolds.
- **Contamination.** Public problems, solutions and repositories may appear in training data.

## Connections

- [Chain-of-thought](../../../models/reasoning/chain-of-thought.md) is the prompting method most often used on these tasks, and [reasoning models](../../../models/reasoning/index.md) covers the wider family.
- [Reasoning and agent benchmarks](../reasoning-agents/index.md) extend the same question to multi-step tasks that need tools.
- [Accuracy](../../metrics/classification/accuracy.md) is the metric behind the first two benchmarks.

## Open questions

- Whether high scores on competition mathematics reflect general mathematical reasoning or retrieval of familiar techniques.
- How to compare code agents fairly when each system brings its own scaffold, search budget and test harness.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Language](../language/index.md) covers the understanding and knowledge benchmarks.

## References

### Seminal papers

- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv. https://arxiv.org/abs/2110.14168 — Introduces the 8.5K GSM8K problems and the verifier that ranks sampled solutions.
- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — Introduces 12,500 competition problems with step-by-step solutions and reports low accuracy at scale.
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces HumanEval, function-level tests, and the effect of repeated sampling.
- Jimenez, C. E. et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv (2023). https://arxiv.org/abs/2310.06770 — Introduces 2,294 repository-level issues judged by tests across 12 Python repositories.

### Articles and documentation

- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that writing intermediate reasoning steps improves results on GSM8K and other reasoning tasks.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Describes the prompting setup under which many of these benchmarks are run on large models.
