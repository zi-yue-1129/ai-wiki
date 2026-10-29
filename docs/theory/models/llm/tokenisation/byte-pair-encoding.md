---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/llm/tokenisation
tags:
  - byte-pair encoding
  - subword tokenisation
  - merge rules
aliases:
  - Byte-pair encoding
  - BPE
  - 位元組對編碼
---

# Byte-pair encoding (Sennrich et al., 2016)

Byte-pair encoding (BPE) builds a subword vocabulary by repeatedly merging the most frequent adjacent pair of symbols in a corpus. The learned merges define how any new text is split. Part of [Tokenisation](index.md).

## Overview

BPE was adapted to neural machine translation by Sennrich, Haddow and Birch (2016). Starting from characters, each merge adds one new symbol to the vocabulary, so a fixed number of merges gives a fixed vocabulary size. Frequent words end up as single tokens, and rare words split into a few pieces that the model has seen before.

## Key concepts

- **Symbol**: a unit in the current vocabulary, starting as single characters plus an end-of-word marker.
- **Pair count**: the number of times two adjacent symbols appear next to each other across the corpus, weighted by word frequency.
- **Merge rule**: an ordered rule that joins two symbols into one. The order in which rules were learned decides how new text is segmented.
- **Vocabulary size**: the number of initial symbols plus the number of merges.

## Problem

Given a corpus and a target vocabulary size, which subword units should the vocabulary contain, so that frequent strings are cheap and rare strings can still be written?

## How it works

Let \(V\) be the current set of symbols, and let \(c(a,b)\) be the count of the adjacent pair \((a,b)\) in the training corpus. Each step chooses

\[
(a^\ast, b^\ast) = \arg\max_{(a,b)} c(a,b),
\]

replaces every occurrence of \(a^\ast b^\ast\) by the new symbol \(a^\ast b^\ast\), and adds it to \(V\). The procedure repeats until \(|V|\) reaches the target size.

To tokenise new text, the text is first split into characters. The learned merges are then applied in the order they were learned, so that the most common merges take effect first.

### Visual walkthrough: learning and applying merge rules

![Four-stage BPE animation: count adjacent symbol pairs, merge m and a, merge ma and ma, and apply the ordered rules to an input.](../../../../assets/concept-animations/bpe-ordered-merges-motion.svg)

*Original teaching animation, CC BY-SA 4.0.* In the toy word-frequency corpus **mama × 4** and **map × 1**, the pair `m + a` occurs **9** times (twice in each `mama`, once in `map`). After merging it throughout the corpus, `ma + ma` occurs **4** times. The two learned rules, applied in rank order, segment the input `mama` as one symbol. This is **character-level, word-internal BPE**; it does not illustrate byte-level tokenisation, end-of-word markers, or model benchmark results. Counts are calculated for the toy corpus, not measured on a trained tokeniser. On the MkDocs site, use Play/Pause (also accessible by keyboard); [view the four-stage static fallback](../../../../assets/concept-animations/bpe-ordered-merges-still.svg) in GitHub Markdown.

## Key methods

The method is one algorithm with several practical variants. The steps are:

1. Count the words in the corpus, and split each into characters with an end-of-word marker.
2. Count every adjacent symbol pair, weighted by word frequency.
3. Merge the most frequent pair, and update the word splits.
4. Repeat steps 2 and 3 until the vocabulary reaches its target size.
5. To encode text, apply the merges in learned order.

## Variants

- **Word-internal BPE** keeps merges within words, so tokens never cross a space. This is the version in Sennrich et al. (2016).
- **Byte-level BPE** starts from the 256 byte values instead of characters. Any string can be encoded, and no symbol is ever unknown. Wang, Cho and Gu (2020) study this variant for translation.
- **Probabilistic segmentation** replaces the greedy choice with sampling over possible segmentations, as in subword regularisation (see [SentencePiece and the unigram model](sentencepiece.md)).

## Results and limits

- In the experiments of Sennrich et al. (2016), subword units let a translation model handle rare and unseen words, and improved translation quality over word-level baselines.
- Each merge is chosen greedily by frequency. The method does not optimise a likelihood, so it can prefer a merge that is frequent but gives a poor segmentation for some words.
- A vocabulary learned on one corpus can split text in another language or domain into many more tokens, which raises cost.
- Byte-level variants avoid unknown symbols but produce longer sequences for scripts with large character sets.

## Applications

- **Machine translation**: a shared subword vocabulary across source and target languages.
- **Language models**: the tokeniser of many GPT-style models is a byte-level BPE, learned once and then frozen.
- **Data compression**: BPE started as a compression method, as Sennrich et al. (2016) note, and its merge rules are compact to store.

## Open questions

- Which corpus and vocabulary size give the best trade-off between sequence length and coverage for a given language?
- Can greedy merges be replaced by an objective that better matches downstream loss without making training much slower?

## Connections

- Parent topic: [Tokenisation](index.md)
- Other method on this topic: [SentencePiece and the unigram model](sentencepiece.md)
- Used in: [Large Language Models](../index.md)

## References

### Seminal papers

- Sennrich, R., Haddow, B. & Birch, A. (2016). Neural Machine Translation of Rare Words with Subword Units. In *Proceedings of the 54th Annual Meeting of the ACL (Volume 1: Long Papers)*, 1715–1725. https://doi.org/10.18653/v1/P16-1162 — Adapts BPE to build subword vocabularies for neural machine translation, and reports the gains over word-level models.
- Wang, C., Cho, K. & Gu, J. (2020). Neural Machine Translation with Byte-Level Subwords. In *AAAI 2020*. arXiv:1909.03341. https://arxiv.org/abs/1909.03341 — Byte-level BPE for translation, which has no unknown symbols.
- Kudo, T. & Richardson, J. (2018). SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing. arXiv:1808.06226. https://arxiv.org/abs/1808.06226 — Implements BPE and unigram segmentation in one framework that trains directly on raw text.

### Surveys and textbooks

- Xue, L. et al. (2022). ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models. *Transactions of the ACL* 10, 291–306. https://doi.org/10.1162/tacl_a_00461 — Discusses the trade-off between byte-level sequences and the cost of BPE-based subword models.
- Schuster, M. & Nakajima, K. (2012). Japanese and Korean voice search. In *ICASSP 2012*, 5149–5152. https://doi.org/10.1109/ICASSP.2012.6289079 — Introduces WordPiece, a data-driven subword segmentation that is often compared with BPE.
- Devlin, J. et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In *NAACL-HLT 2019*. arXiv:1810.04805. https://arxiv.org/abs/1810.04805 — Uses a close relative of BPE, WordPiece, in a widely used model.
