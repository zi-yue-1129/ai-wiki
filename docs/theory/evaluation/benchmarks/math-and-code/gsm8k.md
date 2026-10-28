---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# GSM8K

GSM8K is a dataset of 8,500 grade-school math word problems that require several steps of arithmetic reasoning. The paper that introduced it also proposed training verifiers, which score candidate solutions, as a way to improve accuracy (Cobbe et al., 2021).

## Task and data

Each problem is written in natural language and has a single numerical answer. The problems are linguistically varied, and the reasoning is simple at each step, so the difficulty comes from combining steps correctly (Cobbe et al., 2021).

## Protocol and metric

The metric is **accuracy on the final numerical answer**. Intermediate steps are not scored directly. Chain-of-thought prompting (Wei et al., 2022) and self-consistency, which samples several reasoning paths and takes the majority answer (Wang et al., 2022), both raised scores on this benchmark. Results therefore depend strongly on the prompting and decoding setup, which must be reported.

## What it shows

The original paper found that even large transformers failed to reach high test accuracy, and that verification scaled better with more data than fine-tuning alone (Cobbe et al., 2021). It is useful as a diagnostic of multi-step reasoning in language models.

## Limitations

- **Saturation.** Recent models score very high, so differences between them are hard to read without an interval.
- **Contamination.** The problems are public, and similar problems may appear in training data.
- **Answer-only scoring.** A correct final answer reached by an invalid path is counted as correct.

## Related

- [MATH](math.md) is a harder benchmark of competition mathematics.
- [SWE-bench](swe-bench.md) covers software engineering, with tests as the judge.
- [Math and code family overview](index.md) compares the benchmarks in this area.

## References

### Seminal papers

- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv. https://arxiv.org/abs/2110.14168 — Introduces the 8.5K problems and the verifier approach.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that intermediate reasoning steps raise accuracy on arithmetic word problems.

### Articles and documentation

- Wang, X. et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv. https://arxiv.org/abs/2203.11171 — Samples several reasoning paths and takes the majority answer, with gains on GSM8K.
- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — A harder mathematics benchmark that follows GSM8K.

### Additional sources

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Introduces in-context prompting, which is how many GSM8K results are obtained.
