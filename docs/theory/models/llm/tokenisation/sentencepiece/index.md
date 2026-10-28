---
status: draft
last_reviewed: 2026-10-28
aliases:
  - SentencePiece
  - Unigram 語言模型
  - Unigram language model
---

# SentencePiece and the Unigram Model (Kudo and Richardson, 2018)

SentencePiece is a tokeniser library that learns subword pieces directly from raw text, treating spaces as ordinary symbols. Its unigram model chooses the vocabulary by asking which pieces the corpus can most afford to lose. The method is one of the three main approaches on the parent topic page, [Tokenisation](../index.md).

## Overview

Earlier pipelines split text into words on whitespace, applied language-specific rules, and then ran a subword method such as BPE on the result. That pipeline is awkward for languages written without spaces, such as Chinese and Japanese, and it makes detokenisation lossy, because the original spacing is lost. Kudo and Richardson (2018) built SentencePiece to avoid both problems. The input is a stream of Unicode characters with spaces replaced by a visible marker symbol. Training and encoding therefore need no language-specific preprocessing, and decoding restores the original text exactly.

This page concentrates on the unigram model.

## Key concepts

- **Unigram language model**: a model in which each piece has a probability and the probability of a segmentation is the product of its pieces' probabilities. Pieces are treated as independent.
- **Candidate vocabulary**: a large starting set of pieces, for example all frequent substrings of the corpus, from which the final vocabulary is pruned.
- **Viterbi segmentation**: the most probable segmentation of a string under the model, found by dynamic programming over all ways of cutting it.
- **Subword regularisation**: during training, sampling a segmentation from the model rather than always using the most probable one, so the network sees several splits of the same word (Kudo, 2018).

## How it works

For a string $x$, let $S(x)$ be the set of all ways to cut it into pieces from the vocabulary, and let a segmentation be $\mathbf{s} = (s_1, \dots, s_n)$. Under the unigram model, its probability is

$$P(\mathbf{s}) = \prod_{i=1}^{n} p(s_i), \qquad \sum_{v \in V} p(v) = 1,$$

and encoding picks the most probable segmentation, $\mathbf{s}^* = \arg\max_{\mathbf{s} \in S(x)} P(\mathbf{s})$.

Training fits the piece probabilities and then prunes the vocabulary:

1. Build a large candidate vocabulary of frequent substrings from the corpus.
2. Estimate the piece probabilities that maximise the corpus log-likelihood $\sum_{x \in D} \log \sum_{\mathbf{s} \in S(x)} P(\mathbf{s})$, using expectation-maximisation.
3. For each piece, estimate how much the corpus likelihood would fall if that piece were removed. Single-character pieces are kept so that every string stays encodable.
4. Remove a fixed fraction of the pieces with the smallest loss, and repeat steps 2 and 3 until the vocabulary reaches the target size.
5. Encode new text with Viterbi segmentation, or sample segmentations for regularisation.

Because the segmentation is defined on the raw character stream, decoding is simply concatenation followed by replacing the space marker with a space. This is the property that makes the method lossless.

## Results

The 2018 SentencePiece paper is mainly a system description of the released library, and its main contribution is the design and the tool. Evidence for the effect of the segmentation on translation quality comes mostly from Kudo (2018), which reports that sampling among segmentations improves neural machine translation in its experiments. The scores are in that paper and are not repeated here.

## Limitations

- **Independence assumption.** Pieces are scored independently, so the model does not capture which pieces tend to follow one another.
- **Morphology is not guaranteed.** Likelihood favours frequent pieces, which can cut across morphological boundaries.
- **Training cost.** Expectation-maximisation over a large candidate set takes more computation than a single pass of BPE merges.
- **Fixed vocabulary.** Like BPE, the method produces a fixed set of pieces, so text from a new script or domain can still be split into many small pieces.

## Open questions

- Does the unigram model give better downstream models than BPE when vocabulary size and data are matched exactly? Comparisons in the literature vary in setup.
- Do multilingual vocabularies built from raw text distribute tokens fairly across languages? Rust et al. (2021) show that tokeniser fit affects per-language performance.

## Connections

- Parent topic: [Tokenisation](../index.md).
- Sibling methods: [Byte-Pair Encoding](../bpe/index.md) and [ByT5](../byt5/index.md).

## References

### Seminal papers

- Kudo, T. & Richardson, J. (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing*. EMNLP (System Demonstrations). https://arxiv.org/abs/1808.06226 — Describes the SentencePiece library, which trains subword models directly on raw text without language-specific pre-tokenisation.
- Kudo, T. (2018). *Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates*. ACL. https://arxiv.org/abs/1804.10959 — Proposes sampling among several segmentations drawn from a unigram language model during training.
- Sennrich, R., Haddow, B. & Birch, A. (2016). *Neural Machine Translation of Rare Words with Subword Units*. ACL. https://arxiv.org/abs/1508.07909 — Introduces byte-pair encoding for neural machine translation, the main alternative to the unigram approach.

### Surveys and textbooks

- Mielke, S. J. et al. (2021). *Between words and characters: A Brief History of Open-Vocabulary Modeling and Tokenization in NLP*. arXiv. https://arxiv.org/abs/2112.10508 — A survey of how NLP moved from words to characters and subwords, with the trade-offs of each unit.

### Articles and documentation

- Rust, P. et al. (2021). *How Good is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models*. ACL. https://arxiv.org/abs/2012.15613 — Finds that a multilingual model's performance in a single language depends on how well the shared tokeniser fits that language.
- Petrov, A. et al. (2023). *Language Model Tokenizers Introduce Unfairness Between Languages*. arXiv. https://arxiv.org/abs/2305.15425 — Shows that tokenisers can make the same content cost many more tokens in some languages than in English.
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation*. arXiv. https://arxiv.org/abs/1609.08144 — Describes the GNMT system and the wordpiece segmentation it uses, for comparison with the unigram approach.
