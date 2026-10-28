---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# Math and Code Benchmarks

These benchmarks test whether a model can reason through a problem with a checkable answer: a number in a word problem, a formal answer in competition mathematics, or a passing test suite in a real repository.

| Benchmark | Task | Main metric |
|---|---|---|
| [GSM8K](gsm8k.md) | Grade-school word problems | Accuracy on the final number |
| [MATH](math.md) | Competition mathematics | Accuracy on the final answer |
| [SWE-bench](swe-bench.md) | Resolving GitHub issues in Python repositories | Fraction of issues resolved by tests |

## Common issues

- **Answer checking.** Equivalent answers in different forms can be marked wrong, so the normaliser matters.
- **Scaffold dependence.** For code agents, the tools and the prompt are part of the result.
- **Contamination.** Public problems and repositories may appear in training data.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Accuracy](../../metrics/classification/accuracy.md) is the metric behind the first two.

## References

### Seminal papers

- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv. https://arxiv.org/abs/2110.14168 — Introduces the GSM8K word problems and the verifier approach.
- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — Introduces the MATH competition problems and their solutions.
- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv. https://arxiv.org/abs/2310.06770 — Introduces repository-level software engineering tasks judged by tests.

### Articles and documentation

- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces function-level code evaluation with unit tests and pass@k.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that intermediate reasoning steps change scores on these benchmarks.
