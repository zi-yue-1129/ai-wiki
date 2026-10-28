---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 位元組對編碼
  - BPE
  - Byte-Pair Encoding
---

# Byte-Pair Encoding (Sennrich et al., 2016)

Byte-pair encoding (BPE) builds a subword vocabulary by repeatedly merging the most frequent adjacent pair of symbols in a corpus. It is the most widely used family of tokenisers in language models. Its place among the other methods is described on the parent topic page, [Tokenisation](../index.md).

## Overview

BPE began as a lossless data-compression idea: replace the most common pair of bytes in a file with a new, unused byte and record the replacement. Sennrich, Haddow and Birch (2016) adapted it for neural machine translation. Translation systems of the time used a fixed word vocabulary, so rare words and names were mapped to one unknown symbol and could not be translated. Their proposal split such words into subword units learned from the training text, so a rare word could be assembled from pieces that were common in the corpus.

## Key concepts

- **Symbol**: the starting unit, a character or a byte. Merging turns symbols into longer units as training proceeds.
- **Merge rule**: an ordered pair of symbols that is joined into a new symbol. The learned list of merges is the tokeniser.
- **Greedy merging**: each step takes the currently most frequent pair. The result depends on the order of merges and is not guaranteed to be optimal under any global criterion.

## How it works

Training proceeds in numbered steps:

1. Count every distinct word in the corpus and split each word into characters, adding an end-of-word marker to its last symbol.
2. Count how often each adjacent pair of symbols occurs across all words, weighted by word frequency.
3. Choose the pair $(a, b)$ that maximises the weighted count $f(a,b)$, and create the new symbol $ab$.
4. Replace every occurrence of $a\ b$ in the word table with $ab$, and record the rule $a + b \rightarrow ab$.
5. Repeat steps 2 to 4 until the vocabulary reaches the target size or the merge budget is used up.

Encoding a new word starts from its characters and applies the recorded merges in the order they were learned, until none applies. A word that never appeared in training is still encodable, because every character in the base alphabet has an entry. Byte-level variants go further: they start from the 256 byte values, so no input can be unknown (Wang et al., 2019).

Two close relatives are worth knowing. WordPiece, described in the GNMT system (Wu et al., 2016), keeps the same merge loop but scores candidate merges by their effect on training likelihood rather than raw frequency.

## Results

Sennrich et al. evaluate BPE segmentation on machine translation benchmarks and compare it with word-level systems and with a back-off dictionary approach for rare words. They report measured translation quality in BLEU and conclude that subword segmentation improves the handling of rare words. The exact scores are in the paper and are not repeated here.

## Limitations

- **Greedy and order-dependent.** Each merge is chosen locally, so the final vocabulary is not the best possible for the corpus.
- **Corpus-dependent.** The merges reflect the training text. Text from another domain or script is cut into more and smaller pieces, and languages that are scarce in the merge data pay the most.
- **One split per word.** Deterministic segmentation gives the model a single view of each word. Subword regularisation (Kudo, 2018) was proposed partly to address this.
- **Pre-tokenisation interacts with merging.** Where whitespace and punctuation boundaries are drawn decides which merges can happen, so two systems that both say "BPE" can behave differently.
- **Fairness across languages.** As Petrov et al. (2023) show for several tokenisers, the same content can cost very different numbers of tokens in different languages.

## Open questions

- Do learned merges capture morphology, or mostly frequency? Whether the two can be separated cleanly is unclear.
- Do likelihood-based merges (WordPiece) or sampled segmentations (Kudo, 2018) produce better models at large scale, once data and compute are controlled?

## Connections

- Parent topic: [Tokenisation](../index.md).
- Sibling methods on the same page family: [SentencePiece](../sentencepiece/index.md), which uses a unigram model instead of merges, and [ByT5](../byt5/index.md), which removes the learned vocabulary.

## References

### Seminal papers

- Sennrich, R., Haddow, B. & Birch, A. (2016). *Neural Machine Translation of Rare Words with Subword Units*. ACL. https://arxiv.org/abs/1508.07909 — Introduces byte-pair encoding for neural machine translation, so that rare and unseen words can be built from known subword units.
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation*. arXiv. https://arxiv.org/abs/1609.08144 — Describes the GNMT system and its wordpiece segmentation, a BPE-like subword method used in production translation.
- Kudo, T. (2018). *Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates*. ACL. https://arxiv.org/abs/1804.10959 — Proposes sampling among several segmentations drawn from a unigram language model during training.

### Surveys and textbooks

- Mielke, S. J. et al. (2021). *Between words and characters: A Brief History of Open-Vocabulary Modeling and Tokenization in NLP*. arXiv. https://arxiv.org/abs/2112.10508 — A survey of how NLP moved from words to characters and subwords, with the trade-offs of each unit.

### Articles and documentation

- Wang, C., Cho, K. & Gu, J. (2019). *Neural Machine Translation with Byte-Level Subwords*. arXiv. https://arxiv.org/abs/1909.03341 — Applies byte-level BPE to translation, so that any text can be encoded from a base vocabulary of 256 byte values.
- Petrov, A. et al. (2023). *Language Model Tokenizers Introduce Unfairness Between Languages*. arXiv. https://arxiv.org/abs/2305.15425 — Shows that tokenisers can make the same content cost many more tokens in some languages than in English.
- Schmidt, C. W. et al. (2024). *Tokenization Is More Than Compression*. arXiv. https://arxiv.org/abs/2402.18376 — Argues that compression alone does not predict how well a tokeniser serves downstream language modelling, and compares tokenisers on other criteria.
