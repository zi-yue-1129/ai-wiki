---
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - contamination
---

# Contamination Detection

Contamination detection checks whether a benchmark's test items, or their answers, were present in a model's training data. If they were, the score measures memory rather than ability. Methods range from searching for overlapping text to statistical tests that use only the model's outputs (Oren et al., 2023).

## Procedure

Overlap methods compare the test items with the training corpus, usually with n-gram matching, and flag items that appear in it. Membership-inference methods ask whether the model finds the test text more likely than comparable new text, because memorised text tends to receive higher likelihood (Carlini et al., 2021). Oren et al. (2023) propose a statistical test that uses the ordering of the benchmark's examples to show that a model has seen the benchmark, using only black-box access.

## Key methods

Three methods have their own pages. They differ in what they need: the training corpus, the model's token probabilities, or a benchmark that never reaches the training data.

- [N-gram overlap decontamination](ngram-overlap-decontamination.md): searches the corpus for long shared word sequences. It is exact, but it needs the corpus.
- [Min-K% Prob](min-k-percent-prob.md): uses only the model's token probabilities. Shi et al. (2024) report a 7.4% improvement on WikiMIA over earlier likelihood methods.
- [LiveBench and refreshed benchmarks](livebench.md): avoids contamination by replacing questions monthly, so that test items postdate the training data.

## Reporting

State which method was used, the corpus or the model it was run on, the threshold for flagging an item, and what fraction of items was flagged. A method that finds no overlap does not prove the model has never seen the benchmark, because the training data may be closed or may have been filtered.

## Limitations

- **Closed training data.** Overlap checks need the corpus, which many providers do not release.
- **Paraphrase.** Rewritten items escape n-gram matching while keeping the same answers.
- **False signals.** Likelihood-based methods can flag text that is merely common or simple.

## Related

- [Protocols overview](../index.md) lists the leakage risks for splits.
- [Paired bootstrap](paired-bootstrap.md) gives the uncertainty of a score after contaminated items are removed.

## References

### Seminal papers

- Carlini, N. et al. (2021). *Extracting Training Data from Large Language Models*. arXiv. https://arxiv.org/abs/2012.07805 — Shows that language models memorise and reproduce training text, which underlies likelihood-based checks.
- Oren, Y. et al. (2023). *Proving Test Set Contamination in Black Box Language Models*. arXiv. https://arxiv.org/abs/2310.17623 — Gives a statistical test for whether a benchmark appeared in training, using only model outputs.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Describes 13-gram overlap filtering against benchmark test sets for GPT-3, and its small measured effects on most datasets.
- Shi, W. et al. (2024). *Detecting Pretraining Data from Large Language Models*. arXiv. https://arxiv.org/abs/2310.16789 — Proposes Min-K% Prob, a detector that needs no corpus or reference model.
- White, C. et al. (2024). *LiveBench: A Challenging, Contamination-Limited LLM Benchmark*. arXiv. https://arxiv.org/abs/2406.19314 — Describes a benchmark refreshed monthly so that its questions postdate training cutoffs.

### Articles and documentation

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics, with attention to how test data is reported.

### Additional sources

- Dodge, J. et al. (2021). *Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus*. arXiv. https://arxiv.org/abs/2104.08758 — Finds evaluation examples from other benchmark datasets inside the C4 web corpus.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
