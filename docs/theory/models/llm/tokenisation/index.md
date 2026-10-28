---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/llm
  - theory/models/nlp
tags:
  - tokenisation
  - subword units
  - byte-pair encoding
  - SentencePiece
aliases:
  - Tokenisation
  - Tokenization
  - 分詞
  - Subword tokenisation
---

# Tokenisation

Language models read sequences of discrete units called tokens. A tokeniser maps raw text to a sequence of tokens and back again. The choice of tokens decides the vocabulary size, how long a text becomes, and which strings the model can represent at all. Part of [Large Language Models](../index.md).

## Overview

A neural model needs a fixed vocabulary. Whole words make the vocabulary too large and leave rare or unseen words with no entry. Single characters avoid that problem but make sequences long and expensive. Sennrich, Haddow and Birch (2016) brought subword units into neural machine translation, so that common words stay whole while rare words split into known pieces. Most modern language models use a learned subword tokeniser of this kind.

## Key concepts

- **Vocabulary**: the fixed set of tokens the model can emit, typically tens of thousands to a few hundred thousand entries.
- **Subword unit**: a piece of a word, such as `token` and `isation`, that is shorter than a word and usually longer than a character.
- **Segmentation**: the rule that splits a string into tokens. A learned tokeniser also fixes the segmentation of unseen text.
- **Byte-level tokeniser**: a tokeniser whose base alphabet is the 256 byte values, so any string, in any script, can be encoded without unknown symbols.
- **Fertility**: the average number of tokens per word, a measure of how efficiently a tokeniser represents a language.

## Problem

How should text be split into units so that the vocabulary is of manageable size, rare words are still representable, and sequences are short enough for the model to process?

## How it works

Most tokenisers are trained once on a corpus and then frozen. Training chooses a vocabulary and the rules that map text to it. Encoding a new string applies those rules in a fixed order, and decoding joins the tokens back into text.

Three families of learned tokenisers are in common use:

- **Byte-pair encoding (BPE)** starts from characters and repeatedly merges the most frequent adjacent pair. See [Byte-pair encoding](byte-pair-encoding.md).
- **WordPiece** is close to BPE, but chooses each merge to maximise the likelihood of the training data rather than the raw pair count. Schuster and Nakajima (2012) introduced it for Japanese and Korean voice search, and BERT (Devlin et al., 2019) used it.
- **Unigram language model** starts from a large candidate vocabulary and removes pieces that contribute least to the likelihood of the corpus. SentencePiece implements this method, along with BPE, and works directly on raw text without pre-splitting into words. See [SentencePiece and the unigram model](sentencepiece.md).

## Key methods

- [Byte-pair encoding](byte-pair-encoding.md): repeated merges of the most frequent symbol pair, the basis of many GPT-style tokenisers.
- [SentencePiece and the unigram model](sentencepiece.md): language-independent training on raw text, with sampled segmentations for regularisation.

## Variants

- **Word-level**: one token per word. Simple, but the vocabulary cannot cover rare words.
- **Character-level**: one token per character. Covers every string, but makes sequences long.
- **Byte-level subwords**: BPE over bytes, as studied by Wang et al. (2019). A string in any script is always representable.
- **Token-free models**: models that read bytes or characters directly. ByT5 (Xue et al., 2022) uses bytes with a light encoder, and CANINE (Clark et al., 2022) works on characters with a downsampling step.

## Results and limits

- Subword units let neural translation models handle rare and unseen words without an unknown-word token (Sennrich et al., 2016).
- Byte-level models avoid unknown symbols and are more robust to spelling noise, but the authors of ByT5 report that longer byte sequences make training and inference more costly (Xue et al., 2022).
- Tokeniser choice changes how many tokens the same text needs in different languages. A language that a tokeniser was not trained on often needs several tokens per word, which raises the cost of using the model in that language.
- Tokenisation can make some tasks harder than they look. Counting letters or doing arithmetic on digit strings depends on how the text was split.

## Applications

- **Multilingual language models**: choosing a vocabulary that covers several scripts without wasting tokens on any one.
- **Cost estimation**: counting tokens to price an API request or to fit a model into a context window.
- **Code models**: tokenisers trained on source code that keep identifiers and indentation efficient.

## Open questions

- Can a model learn from bytes or characters at the cost of a tokeniser, without losing too much compute efficiency?
- Should a vocabulary be fixed before training, or can segmentation be learned jointly with the model?
- How should a tokeniser be designed for scripts that do not separate words with spaces?

## Connections

- Parent topic: [Large Language Models](../index.md)
- Related: [Natural language processing](../../nlp/index.md)
- Other method on this topic: [Compute-optimal training](../compute-optimal-training/index.md), which counts training tokens rather than model parameters.

## References

### Seminal papers

- Sennrich, R., Haddow, B. & Birch, A. (2016). Neural Machine Translation of Rare Words with Subword Units. In *Proceedings of the 54th Annual Meeting of the ACL (Volume 1: Long Papers)*, 1715–1725. https://doi.org/10.18653/v1/P16-1162 — Adapts byte-pair encoding to build a subword vocabulary for neural machine translation.
- Schuster, M. & Nakajima, K. (2012). Japanese and Korean voice search. In *ICASSP 2012*, 5149–5152. https://doi.org/10.1109/ICASSP.2012.6289079 — Introduces the WordPiece segmentation for speech-recognition vocabularies.
- Kudo, T. & Richardson, J. (2018). SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing. arXiv:1808.06226. https://arxiv.org/abs/1808.06226 — Trains subword models directly on raw text, without pre-tokenisation.
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In *NAACL-HLT 2019*. arXiv:1810.04805. https://arxiv.org/abs/1810.04805 — Uses the WordPiece tokeniser in a widely used pre-trained encoder.

### Surveys and textbooks

- Xue, L. et al. (2022). ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models. *Transactions of the ACL* 10, 291–306. https://doi.org/10.1162/tacl_a_00461 — Studies byte-level models as a tokeniser-free alternative, with a discussion of their cost.
- Clark, J. H. et al. (2022). CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation. *Transactions of the ACL* 10, 73–91. https://doi.org/10.1162/tacl_a_00448 — Encoder that reads characters directly and downsamples them before the Transformer layers.
- Wang, C., Cho, K. & Gu, J. (2020). Neural Machine Translation with Byte-Level Subwords. In *AAAI 2020*. arXiv:1909.03341. https://arxiv.org/abs/1909.03341 — Byte-level subword segmentation for translation, which removes unknown-symbol failures.

## Further learning

- Hugging Face, *Summary of the tokenizers*. https://huggingface.co/docs/transformers/tokenizer_summary — An overview of the main tokenisers with runnable examples.
