---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - speech
---

# Speech Benchmarks

Speech benchmarks test automatic speech recognition, which turns audio into text. Scores are usually word error rate on a fixed test set, so results are comparable only when the split, the text normalisation and the decoding setup match.

| Benchmark | Task | Main metric |
|---|---|---|
| [LibriSpeech](librispeech.md) | Transcribing read English audiobook speech | Word error rate on clean and other test sets |

## Common issues

- **Normalisation.** Word error rate depends on how punctuation, casing and numbers are normalised before comparison, so the normalisation must be reported.
- **Domain shift.** Read audiobook speech differs from conversation, accents and noisy recordings, so a low error rate on one set does not carry over to others (Radford et al., 2022).
- **Training overlap.** Large web-scale training sets can contain recordings close to the test material, so the history of the test set matters.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Language](../language/index.md) covers the text-only counterparts.
- [Protocols](../../protocols/index.md) covers splits and reporting.

## References

### Seminal papers

- Graves, A. et al. (2006). *Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks*. ICML 2006. https://doi.org/10.1145/1143844.1143891 — Introduces the CTC loss, a training objective used by many speech recognisers.
- Hannun, A. et al. (2014). *Deep Speech: Scaling up end-to-end speech recognition*. arXiv. https://arxiv.org/abs/1412.5567 — Shows end-to-end recognition trained on large amounts of speech.

### Articles and documentation

- Radford, A. et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv. https://arxiv.org/abs/2212.04356 — Shows that large and varied training data improves robustness across test sets.

### Additional sources

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
