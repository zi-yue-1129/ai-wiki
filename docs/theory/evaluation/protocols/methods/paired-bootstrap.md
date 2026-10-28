---
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - statistics
---

# Paired Bootstrap

The paired bootstrap estimates how uncertain a difference between two methods is, by resampling the examples on which both methods were tested together. Because the two methods share each example, the resampling keeps that pairing and gives a tighter interval for the difference than comparing two independent averages (Efron, 1992).

## Procedure

For a test set of n examples, record the score of each method on every example. Draw n examples with replacement, compute the difference in the mean score on the resample, and repeat many times, commonly 1,000 or more. The middle 95 per cent of these differences gives an interval. If the interval excludes zero, the difference is unlikely to be explained by which examples happened to be in the test set.

## When it applies

The unit of resampling must match how the data depends on itself. Several turns in one conversation, or several questions about one document, are not independent, so they should be resampled together. SciPy's bootstrap implementation provides the general resampling machinery (SciPy contributors).

## Reporting

State the number of resamples, the resampling unit, the confidence level and the method for the interval, such as percentile or bias-corrected. Report the difference alongside the interval, not only the two scores.

## Limitations

- **Test-set variance only.** The bootstrap captures variation from which examples were tested, not from training runs. Repeat training with several seeds when the claim depends on it.
- **Small sets.** With very few examples, the interval is itself unreliable.
- **Dependence.** Ignoring a grouping in the data gives intervals that are too narrow.

## Related

- [Protocols overview](../index.md) explains why uncertainty must be reported.
- [Cross-validation](cross-validation.md) gives repeated estimates from different splits.

## References

### Seminal papers

- Efron, B. (1992). *Bootstrap Methods: Another Look at the Jackknife*. In *Breakthroughs in Statistics*, Vol. 1. Springer. https://doi.org/10.1007/978-1-4612-4380-9_41 — Introduces the bootstrap as a general method for estimating uncertainty, as a reprint of the 1979 paper.

### Articles and documentation

- SciPy contributors. *scipy.stats.bootstrap*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html — Describes bootstrap confidence intervals and the resampling options for matched observations.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.

### Additional sources

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics, so differences need intervals.
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
