---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# HumanEval

HumanEval is a set of 164 hand-written Python programming problems, each with unit tests, used to measure whether a code model can write a correct function from a docstring (Chen et al., 2021). It introduced the pass@k metric, which is now the standard way to report code generation results.

## Task and data

Each problem gives a function signature and a docstring, and the model must complete the function body. The problems cover basic algorithms, string handling and simple mathematics. Each one comes with hidden unit tests, and the program passes only if all of them pass (Chen et al., 2021).

## Protocol and metric

The metric is pass@k: the probability that at least one of k sampled solutions passes all tests. Chen et al. (2021) give an unbiased estimator that draws n samples per problem, with n at least k, and counts the correct ones c. Scores depend on the sampling temperature, the number of samples and the execution sandbox, so all three must be reported.

## What it shows

It shows whether a model can turn a precise specification into a program that behaves correctly. Because the tests check behaviour rather than text, a solution is judged by what it does, not by how it looks.

## Limitations

- **Small set.** With 164 problems, a few solved items change the score noticeably, so intervals are needed.
- **Contamination.** Public problems can appear in training data, and the paper's problems are widely copied.
- **Easy problems.** Many items are short functions, so the benchmark says little about large codebases, which SWE-bench covers.

## Related

- [Math and code overview](index.md) compares the math and code benchmarks.
- [SWE-bench](swe-bench.md) tests repository-scale software engineering.

## References

### Seminal papers

- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces HumanEval and the pass@k metric with its unbiased estimator.

### Articles and documentation

- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics to expose trade-offs.
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.

### Additional sources

- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Argues that skill on a fixed task is a weak measure of intelligence.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
