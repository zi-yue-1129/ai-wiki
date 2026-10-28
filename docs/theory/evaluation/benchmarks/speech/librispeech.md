---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - speech
---

# LibriSpeech

LibriSpeech is a corpus of about 1,000 hours of read English speech, built from public-domain audiobooks, and a standard benchmark for automatic speech recognition (Panayotov et al., 2015). Many speech papers report it before turning to other data.

## Task and data

The input is a segment of recorded speech and the output is its transcript. The audio comes from LibriVox recordings aligned to the text of the books. The corpus is split into training data and development and test sets, and the development and test sets are each divided into clean and other subsets. The other subsets were chosen to be harder for a recogniser, so they contain more difficult recordings (Panayotov et al., 2015).

## Protocol and metric

The main metric is word error rate: the number of substitutions, deletions and insertions divided by the number of reference words. Scores depend on text normalisation and on whether a language model is used during decoding, so papers must state both. Connectionist temporal classification, a common training objective for systems evaluated here, is described in Graves et al. (2006).

## What it shows

It shows how a recogniser performs on read, fairly clean speech. The gap between the clean and other sets indicates how a system handles harder recordings.

## Limitations

- **Read speech.** Audiobook narration is more regular than conversation, so scores can overstate performance in practice.
- **Limited conditions.** The corpus covers a fixed range of speakers and recording conditions.
- **Small differences.** Strong systems reach low error on the clean set, so small gaps need confidence intervals.

## Related

- [Speech overview](index.md) compares the speech benchmarks.
- [Benchmarks overview](../index.md) lists all families.

## References

### Seminal papers

- Panayotov, V. et al. (2015). *Librispeech: An ASR corpus based on public domain audio books*. ICASSP 2015. https://doi.org/10.1109/ICASSP.2015.7178964 — Describes the corpus, its splits and the clean and other subsets.

### Articles and documentation

- Graves, A. et al. (2006). *Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks*. ICML 2006. https://doi.org/10.1145/1143844.1143891 — Introduces the CTC loss used by many recognisers on this corpus.
- Radford, A. et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv. https://arxiv.org/abs/2212.04356 — Evaluates a large recogniser on many speech test sets, not only one.

### Additional sources

- Hannun, A. et al. (2014). *Deep Speech: Scaling up end-to-end speech recognition*. arXiv. https://arxiv.org/abs/1412.5567 — Shows end-to-end recognition trained on large amounts of speech.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
