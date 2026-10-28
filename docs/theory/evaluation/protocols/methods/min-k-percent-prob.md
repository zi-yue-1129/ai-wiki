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
  - Min-K% Prob
  - Min-K 概率
---

# Min-K% Prob

!!! info "Part of Contamination Detection"
    This method page belongs to [Contamination Detection](contamination-detection.md). It explains the likelihood-based method in detail; the parent page compares it with the other detection methods.

Min-K% Prob is a detection method that decides whether a text was in a model's pretraining data, using only the model's token probabilities. It is based on the observation that a text the model has seen rarely contains very unlikely words, whereas an unseen text usually does. Shi et al. (2024) propose it and report that it improves on earlier likelihood-based methods on the WikiMIA benchmark.

## Problem

Overlap checks need the training corpus, and many models do not publish theirs. Some earlier detection methods need a reference model trained on similar data. The problem is to detect pretraining data with access only to the model's outputs and no knowledge of the corpus.

## Core idea

An unseen example usually contains some words that the model considers very unlikely. A seen example rarely does, because training pushed up the probability of its words. So the score of a text should be driven by its least likely tokens, not by its average likelihood. Min-K% Prob averages the log-probabilities of the K% of tokens with the lowest probability, and a high score (a less surprising low tail) suggests the text was in the training data.

## Procedure

1. Compute the probability the model assigns to each token of the candidate text, given the preceding tokens.
2. Sort the tokens by probability and keep the lowest K% of them.
3. Average the log-probabilities of the kept tokens. This is the Min-K% score.
4. Compare the score with a threshold, or use it to rank candidates, and evaluate the ranking with an AUC.

The method needs no reference model and no training of an attack classifier.

## Results

The abstract of Shi et al. (2024) reports that Min-K% Prob achieves a 7.4% improvement on WikiMIA over previous methods. The paper reports its WikiMIA results as AUC, with an average of 0.72 for Min-K% Prob in Table 1.

## Limitations

- **Benchmark dependence.** The reported gain is on WikiMIA. The paper's evaluation does not show how the method behaves on code or other text types.
- **Choice of K.** The paper sets k = 20 after a sweep from 10 to 50 on a validation set. This page does not show that 20 is best for other corpora.
- **Decision direction.** Figure 1 says a high average log-likelihood indicates pretraining data, but Algorithm 1 is written the other way. Check the sign convention before reusing a threshold.
- **Ranking, not proof.** The score shows that a text is probably in the training data. It does not show exactly which documents were used, so it is a statistical signal, not a definitive check.
- **Model access.** The method needs token probabilities from the model, so it cannot be applied to models that do not expose them.

## Connections

- The exact-match alternative is [N-gram Overlap Decontamination](ngram-overlap-decontamination.md), which needs the corpus.
- The membership-inference attacks in privacy research use the same idea of comparing a model's behaviour on seen and unseen data. See [Membership Inference](../../../../society/privacy/membership-inference.md).

## Open questions

- Does the signal survive when the model is trained on deduplicated data, which lowers the probabilities of repeated text?
- How should a threshold be set when the proportion of contaminated items in a benchmark is unknown?

## References

### Seminal papers

- Shi, W. et al. (2024). *Detecting Pretraining Data from Large Language Models*. arXiv. https://arxiv.org/abs/2310.16789 — Proposes Min-K% Prob, a likelihood-based detector that needs no reference model, and reports a 7.4% improvement on WikiMIA.
- Carlini, N. et al. (2021). *Extracting Training Data from Large Language Models*. arXiv. https://arxiv.org/abs/2012.07805 — Shows that training examples can be extracted from a language model by querying it, which motivates detecting memorised text.
- Shokri, R., Stronati, M., Song, C. & Shmatikov, V. (2017). *Membership Inference Attacks Against Machine Learning Models*. IEEE Symposium on Security and Privacy. https://arxiv.org/abs/1610.05820 — Studies whether a model with black-box access reveals if a given record was in its training data, the attack family that likelihood-based detection resembles.
- Oren, Y. et al. (2023). *Proving Test Set Contamination in Black Box Language Models*. arXiv. https://arxiv.org/abs/2310.17623 — Gives a black-box statistical test for contamination that needs neither pretraining data nor model weights.
- Dodge, J. et al. (2021). *Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus*. arXiv. https://arxiv.org/abs/2104.08758 — Finds benchmark evaluation examples inside the C4 web corpus, showing that pretraining text can contain test data.
