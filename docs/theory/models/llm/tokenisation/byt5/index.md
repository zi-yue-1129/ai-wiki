---
status: draft
last_reviewed: 2026-10-28
aliases:
  - ByT5
  - 無分詞模型
  - Token-free models
---

# ByT5: Token-Free Byte-Level Modelling (Xue et al., 2022)

ByT5 is a pretrained Transformer that reads the UTF-8 bytes of text directly, so it needs no learned tokeniser at all. It removes the vocabulary question that the parent topic, [Tokenisation](../index.md), is built around, at the cost of much longer input sequences.

## Overview

Subword tokenisers compress text into pieces, and their vocabularies are fixed when the tokeniser is trained. Xue et al. (2022) asked whether a model could work on the lowest-level representation of text instead. Every string can be written as a sequence of bytes, and the byte values form a fixed alphabet of 256 symbols that covers all languages. A byte-level model therefore cannot meet an unknown symbol, and it sees spelling and character-level structure directly.

ByT5 is built as a byte-level version of mT5, a multilingual subword model with the same encoder-decoder design. The authors changed the balance between encoder and decoder size to take account of the longer sequences, and they pretrained on a span-corruption objective adapted to bytes.

## Key concepts

- **UTF-8 bytes**: the encoding that represents each Unicode character as one to four bytes. ASCII letters take one byte, most European accented letters take two, and most CJK characters take three.
- **Byte vocabulary**: the 256 byte values plus a small number of special ids, so the embedding table is tiny compared with a subword vocabulary.
- **Sequence inflation**: the same text becomes a longer sequence in bytes than in tokens, which raises the cost of attention and of generation.
- **Span corruption**: a pretraining task in which random spans of input are replaced by sentinel markers and the model predicts the missing spans.

## How it works

The model handles text in a small number of steps:

1. Encode the input string as UTF-8 bytes.
2. Map each byte value to an id, offset by the number of special tokens.
3. Pretrain an encoder-decoder Transformer with span corruption: mask random byte spans and train the decoder to reconstruct them.
4. Fine-tune on downstream tasks in the same byte format.
5. At generation time, decode the predicted bytes back to text. Outputs that split a multi-byte character across steps must be handled explicitly, because the bytes alone do not form valid characters until the whole sequence is complete.

The cost is easy to state. For a fixed passage, the number of positions is the total number of UTF-8 bytes. A Chinese sentence is therefore several times longer in ByT5 than in a model with a Chinese-aware subword vocabulary, and the computation grows with the square of length in full attention.

## Results

Xue et al. report that ByT5 is competitive with its subword counterpart, mT5, on standard multilingual benchmarks at comparable model size. They also report advantages on tasks that depend on spelling and pronunciation, and better robustness when input text contains noise such as misspellings. Generation is slower because the output sequences are longer. The exact scores are in the paper and are not repeated here.

## Limitations

- **Longer sequences.** Training and inference cost more for the same text, and long documents fit less content in a fixed context window.
- **Capacity allocation.** A byte-level model must spend capacity on learning how characters combine into words, a job that subword vocabularies do in advance.
- **Benefit depends on the task.** Gains on spelling and noise-sensitive tasks do not automatically carry over to knowledge-heavy or long-context tasks.
- **Ecosystem.** Most deployed models and their tooling assume subword tokenisers, which makes byte-level models harder to adopt.

## Open questions

- Can byte-level models keep their robustness while recovering the efficiency of subword models? The Byte Latent Transformer (Pagnoni et al., 2024) groups bytes into dynamically sized patches to do so, and its scaling behaviour is an active test case.
- How should byte-level models be compared fairly with subword models of the same training cost, rather than the same parameter count?
- Does removing the tokeniser change what a model can learn about morphology and spelling? The question connects to the human-comparison debate in the parent topic.

## Connections

- Parent topic: [Tokenisation](../index.md).
- Sibling methods: [Byte-Pair Encoding](../bpe/index.md), which the byte-level idea extends through byte-level BPE, and [SentencePiece](../sentencepiece/index.md).
- The model family: [Large Language Models](../../index.md).

## References

### Seminal papers

- Xue, L. et al. (2022). *ByT5: Towards a token-free future with pre-trained byte-to-byte models*. TACL. https://arxiv.org/abs/2105.13626 — A byte-level pretrained Transformer that removes the tokeniser entirely and compares it with subword models.
- Wang, C., Cho, K. & Gu, J. (2019). *Neural Machine Translation with Byte-Level Subwords*. arXiv. https://arxiv.org/abs/1909.03341 — Applies byte-level BPE to translation, so that any text can be encoded from a base vocabulary of 256 byte values.
- Pagnoni, A. et al. (2024). *Byte Latent Transformer: Patches Scale Better Than Tokens*. arXiv. https://arxiv.org/abs/2412.09871 — Proposes a byte-level model that groups bytes into dynamically sized patches and compares its scaling with tokeniser-based models.

### Surveys and textbooks

- Mielke, S. J. et al. (2021). *Between words and characters: A Brief History of Open-Vocabulary Modeling and Tokenization in NLP*. arXiv. https://arxiv.org/abs/2112.10508 — A survey of how NLP moved from words to characters and subwords, with the trade-offs of each unit.

### Articles and documentation

- Petrov, A. et al. (2023). *Language Model Tokenizers Introduce Unfairness Between Languages*. arXiv. https://arxiv.org/abs/2305.15425 — Shows that tokenisers can make the same content cost many more tokens in some languages than in English.
- Schmidt, C. W. et al. (2024). *Tokenization Is More Than Compression*. arXiv. https://arxiv.org/abs/2402.18376 — Argues that compression alone does not predict how well a tokeniser serves downstream language modelling, and compares tokenisers on other criteria.
