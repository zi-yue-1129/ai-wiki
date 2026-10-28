---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - theory/evaluation/protocols/methods/contamination-detection.md
tags:
  - evaluation
  - protocols
  - contamination
aliases:
  - N-gram overlap decontamination
  - 13-gram 去污染
  - n-gram 重疊去污染
---

# N-gram Overlap Decontamination

!!! info "Part of Contamination Detection"
    This method page belongs to [Contamination Detection](contamination-detection.md). It explains the overlap method in detail; the parent page compares it with the other detection methods.

N-gram overlap decontamination searches a training corpus for long word sequences that also appear in a benchmark's test items, and removes or flags the matching items. It is a direct check for contamination, and GPT-3 used a 13-gram version of it (Brown et al., 2020). Its weakness is that it only finds copies that match word for word.

## Problem

A benchmark score measures ability only if the model has not seen the test items. Web-scale training corpora are large, and benchmark questions are posted online, so copies can end up in training data without anyone choosing them. The problem is to find these copies and report a score on the remaining items.

## Core idea

Break each test item and each training document into word sequences of a fixed length, called n-grams, and flag an item when it shares a long enough n-gram with the training data. Items that are flagged are removed from the clean version of the benchmark, and the score is reported on that version.

## Procedure

1. Choose a window size n. Brown et al. (2020) use 13-grams: a test item is flagged if it has a 13-gram overlap with the pretraining set. Items shorter than 13 words are compared as a whole.
2. Index the training corpus, for example with a hash of every n-gram.
3. For each test item, check whether any of its n-grams occurs in the index.
4. Remove the flagged items, or report them separately, and recompute the score on the clean subset.

The window size is a trade-off. A short window flags common phrases that are not real copies, and a long one misses copies that have small edits.

## Results

Brown et al. (2020, Section 4) describe the procedure and its effect on GPT-3. They expect contamination to be frequent, but that its effects "may not be as large as feared", and the introduction states that contamination has a minimal effect on most datasets. For LAMBADA the paper reports a negligible effect, and for Winograd a small one. The paper also records a bug that removed only part of the detected overlaps, which is a reminder that the cleaning itself needs testing.

Dodge et al. (2021) show the same risk from the corpus side. Their documentation of the C4 corpus finds that it contains evaluation examples from other benchmark NLP datasets.

## Limitations

- **Exact match only.** A paraphrase, a translation or a reformatted item keeps the answer but escapes the n-gram check.
- **Closed corpora.** The check needs the training data. Many providers do not release it, so the check can only be run by the provider or not at all.
- **Window choice.** The result depends on n and on tokenisation. Two teams using different windows can report different clean subsets.
- **No proof of absence.** A pass shows that no long copy was found, not that the model has never seen the item.

## Connections

- The likelihood-based alternative, which needs no corpus, is [Min-K% Prob](min-k-percent-prob.md).
- A benchmark that avoids the problem by changing its questions is [LiveBench](livebench.md).
- The risks for data splits, and the leakage rules for preprocessing, are on the [Evaluation Protocols](../index.md) overview.

## Open questions

- How should decontamination handle paraphrased copies, which are common in web text and in test items written from textbooks?
- Can a provider report a clean score without publishing the corpus, for example through a third-party audit?

## References

### Seminal papers

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Introduces GPT-3 and describes 13-gram overlap filtering between the training data and benchmark test sets, with its effects.
- Dodge, J. et al. (2021). *Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus*. arXiv. https://arxiv.org/abs/2104.08758 — Documents C4 and finds evaluation examples from other benchmark datasets in the corpus.
- Carlini, N. et al. (2021). *Extracting Training Data from Large Language Models*. arXiv. https://arxiv.org/abs/2012.07805 — Shows that training examples can be extracted from a language model by querying it, which is why exact copies of test items matter.
- Oren, Y. et al. (2023). *Proving Test Set Contamination in Black Box Language Models*. arXiv. https://arxiv.org/abs/2310.17623 — Gives a black-box test for contamination, which is the alternative when the corpus cannot be searched.
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — The BIG-bench benchmark, whose task files carry canary strings against web scraping.
