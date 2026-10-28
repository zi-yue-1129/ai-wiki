---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/llm/tokenisation
tags:
  - SentencePiece
  - unigram language model
  - subword regularisation
aliases:
  - SentencePiece
  - Unigram language model tokeniser
  - 句子片段
---

# SentencePiece and the unigram model (Kudo, 2018)

SentencePiece is a tokeniser that trains directly on raw text, without first splitting it into words, and can use either byte-pair encoding or a unigram language model to choose its pieces. The unigram variant scores a whole segmentation by its likelihood, and can sample segmentations during training. Part of [Tokenisation](index.md).

## Overview

Earlier subword tools assumed that the input had already been split into words, which is hard for languages such as Japanese and Chinese that do not separate words with spaces. Kudo and Richardson (2018) built SentencePiece to treat the input as a raw stream of characters, with spaces encoded as a visible symbol. This makes the segmentation reversible, so detokenisation recovers the original text exactly. Kudo (2018) added the unigram model and a method for sampling different segmentations of the same sentence.

## Key concepts

- **Piece**: a unit in the vocabulary, which may be a character, a subword or a whole word.
- **Unigram language model**: a model that gives each piece a probability and treats a segmentation as a product of piece probabilities.
- **Segmentation lattice**: the set of all ways to split a sentence into pieces from the vocabulary.
- **Subword regularisation**: training on sampled segmentations rather than the single most likely one, so the model sees several splits of the same word.
- **Whitespace marker**: a symbol that stands for a space before a piece, so that spaces are part of the token sequence and can be restored.

## Problem

How should a subword vocabulary be learned from raw text in any language, and how should a sentence be segmented, so that the result is reversible and the model can benefit from uncertainty about segmentation?

## How it works

The unigram method treats a sentence \(X\) as a sequence of pieces \(\mathbf{x}=(x_1,\dots,x_M)\) with probability

\[
p(\mathbf{x}) = \prod_{i=1}^{M} p(x_i), \qquad \sum_{x\in V} p(x) = 1.
\]

Given the vocabulary and piece probabilities, the segmentation is chosen by the Viterbi algorithm, which finds \(\mathbf{x}^\ast = \arg\max_{\mathbf{x}\in S(X)} p(\mathbf{x})\), where \(S(X)\) is the set of all segmentations of \(X\) from the vocabulary.

Training starts from a large candidate vocabulary. It fits the piece probabilities by expectation–maximisation over the corpus, then removes a fraction of the pieces whose removal reduces the corpus likelihood least. Repeating these steps shrinks the vocabulary to the target size.

For subword regularisation, a segmentation is sampled instead of taken as the maximum. Kudo (2018) samples from \(P(\mathbf{x}\mid X) \propto p(\mathbf{x})^{\alpha}\), where \(\alpha\) controls how much the sampling favours likely segmentations.

## Key methods

- **BPE mode**: SentencePiece also implements byte-pair encoding on raw text, so the same tool can produce either kind of vocabulary. See [Byte-pair encoding](byte-pair-encoding.md).
- **Unigram mode**: the likelihood-based method described above, with optional sampling.

## Variants

- **Deterministic unigram**: always uses the Viterbi segmentation, which is reproducible and simpler to serve.
- **Sampled unigram**: draws segmentations during training, as in subword regularisation. This acts as a data augmentation over the input text.
- **Byte fallback**: an option in later implementations that encodes characters outside the vocabulary as bytes, so no input is unknown.

## Results and limits

- Kudo and Richardson (2018) report a validation experiment on English–Japanese translation, which found that training subword models directly on raw sentences gave accuracy comparable to training on pre-tokenised input.
- Kudo (2018) reports that subword regularisation improves translation quality over a single fixed segmentation on several datasets.
- The unigram vocabulary depends on the corpus used to fit it, so a vocabulary learned on one domain may split text from another domain poorly.
- Training on sampled segmentations while testing on the most likely one creates a mismatch between training and inference, which the method accepts by design.

## Applications

- **Multilingual translation and speech models**: one vocabulary for many languages, including languages without spaces.
- **Pre-trained language models**: many multilingual models use a SentencePiece vocabulary, and the reversible whitespace marker lets them output exact text.
- **Data augmentation**: sampled segmentations expose a model to alternative splits of rare words.

## Open questions

- How should the sampling temperature \(\alpha\) be set when the training data is large and diverse?
- Does sampling help large pre-training runs, or is its benefit limited to small translation datasets?

## Connections

- Parent topic: [Tokenisation](index.md)
- Other method on this topic: [Byte-pair encoding](byte-pair-encoding.md)
- Used in: [Large Language Models](../index.md)

## References

### Seminal papers

- Kudo, T. & Richardson, J. (2018). SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing. arXiv:1808.06226. https://arxiv.org/abs/1808.06226 — Describes the SentencePiece library, which trains BPE or unigram vocabularies on raw text and detokenises reversibly.
- Kudo, T. (2018). Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates. In *Proceedings of the 56th Annual Meeting of the ACL (Volume 1: Long Papers)*, 66–75. https://doi.org/10.18653/v1/P18-1007 — Introduces the unigram segmentation model and sampling of subword candidates for regularisation.
- Sennrich, R., Haddow, B. & Birch, A. (2016). Neural Machine Translation of Rare Words with Subword Units. In *Proceedings of the 54th Annual Meeting of the ACL (Volume 1: Long Papers)*, 1715–1725. https://doi.org/10.18653/v1/P16-1162 — The byte-pair encoding baseline that SentencePiece implements alongside the unigram model.

### Surveys and textbooks

- Schuster, M. & Nakajima, K. (2012). Japanese and Korean voice search. In *ICASSP 2012*, 5149–5152. https://doi.org/10.1109/ICASSP.2012.6289079 — Data-driven subword segmentation for languages without word boundaries, a motivation for the raw-text design.
- Xue, L. et al. (2022). ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models. *Transactions of the ACL* 10, 291–306. https://doi.org/10.1162/tacl_a_00461 — Compares subword vocabularies with byte-level input, which removes the need for a learned vocabulary.
- Wang, C., Cho, K. & Gu, J. (2020). Neural Machine Translation with Byte-Level Subwords. In *AAAI 2020*. arXiv:1909.03341. https://arxiv.org/abs/1909.03341 — Byte-level segmentation as an alternative when the character set is large.
