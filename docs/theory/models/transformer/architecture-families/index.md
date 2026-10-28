---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
  - theory/models/llm
  - theory/models/nlp
tags:
  - transformers
  - language models
  - pre-training
aliases:
  - Encoder-only, decoder-only and encoder-decoder Transformers
  - Transformer architecture families
  - 編碼器、解碼器與編碼器–解碼器
---

# Encoder-only, decoder-only and encoder-decoder Transformers

The [Transformer](../index.md) can be used in three shapes. An encoder-only model reads its whole input at once, a decoder-only model predicts each token from the tokens before it, and an encoder-decoder model reads an input with one stack and writes an output with a second stack that attends to the first. The shape decides which pre-training objective fits, and which tasks the model is good at. BERT, GPT and T5 are the three landmark examples.

## Overview

The original Transformer of [Vaswani et al. (2017)](../attention-is-all-you-need/index.md) was an encoder-decoder for machine translation. Later work kept one of its halves. BERT kept the encoder and trained it to fill in masked words, which suits understanding tasks. The GPT line kept the decoder and trained it to predict the next token, which suits generation. T5 kept both halves and framed every task as text-to-text, which made one model usable for many tasks.

The three shapes differ in what each position may attend to. That choice is the main design decision, and it sets which pre-training objectives are natural.

## Key concepts

- **Bidirectional attention**: every position attends to every other position, in both directions. The encoder uses it.
- **Causal attention**: a position attends only to earlier positions. The decoder uses it, so that generation is consistent with training.
- **Cross-attention**: a decoder position attends to the encoder's output. Only encoder-decoder models have it.
- **Pre-training objective**: the task used to train on unlabelled text, such as masked-token prediction or next-token prediction.

## How it works

| Family | Attention | Pre-training objective | Typical uses | Landmark examples |
|---|---|---|---|---|
| Encoder-only | Bidirectional | Masked-token prediction | Classification, extraction, embeddings | [BERT](bert/index.md) |
| Decoder-only | Causal | Next-token prediction | Open-ended generation, chat, few-shot prompting | [GPT-3](../../llm/gpt-3-few-shot/index.md) |
| Encoder-decoder | Bidirectional encoder, causal decoder with cross-attention | Span corruption or other sequence-to-sequence objectives | Translation, summarisation, question answering | [T5](t5/index.md) |

The masks are the whole difference in code. An encoder lets every token attend to every other token. A decoder adds a causal mask, so that the logits at position \(t\) depend only on tokens \(1, \dots, t\). That lets a decoder be trained on every position in one forward pass, using the next token as the target.

## Key methods

Each method below has its own page. The overview here is brief.

### BERT (Devlin et al., 2019)

- **Overview:** An encoder pre-trained to predict masked tokens from both left and right context, then fine-tuned with one output layer per task.
- **Comparison:** The encoder-only family. Its bidirectional context suits tasks that read the whole input, and it cannot generate text left to right in the way a decoder does.
- **Full write-up:** [BERT](bert/index.md)

### T5 (Raffel et al., 2020)

- **Overview:** An encoder-decoder trained with a span-corruption objective, and fine-tuned on every task in one text-to-text format.
- **Comparison:** Keeps both halves of the Transformer. It gives a single interface for many tasks, at the cost of running two stacks.
- **Full write-up:** [T5](t5/index.md)

### GPT (decoder-only)

- **Overview:** A decoder trained to predict the next token on large text corpora. Scaling it up gives few-shot performance from prompts alone.
- **Comparison:** The decoder-only family. Its causal objective matches generation directly. The GPT-3 page covers the scaling evidence and the few-shot results.
- **Full write-up:** [GPT-3: Language Models are Few-Shot Learners](../../llm/gpt-3-few-shot/index.md)

## Why decoder-only models dominate LLMs

Most large language models in use today are decoder-only. The reasons below are the common explanation, not settled results. The next-token objective is the same as generation, so the training signal and the use case match. A single decoder stack also handles any task as a continuation of a prompt, without a separate task-specific head. The [GPT-3 page](../../llm/gpt-3-few-shot/index.md) describes the evidence that few-shot performance grows with scale in this setting. Whether the advantage holds for every task is still discussed.

## Connections

- The attention block is described in [Transformers & Attention](../index.md), and the original encoder-decoder in [Attention Is All You Need](../attention-is-all-you-need/index.md).
- The language-model family, including instruction tuning and reasoning, is on the [LLM](../../llm/index.md) page.
- The natural-language-processing applications of each family are on the [NLP](../../nlp/index.md) page.

## Applications

- Encoder-only models for search ranking, text classification and named-entity recognition.
- Decoder-only models for chat assistants, code generation and open-ended writing.
- Encoder-decoder models for translation and summarisation.

## Open questions

- Whether a single decoder-only model can match a bidirectional encoder on tasks that need the whole input at once, such as classification with little data.
- Whether encoder-decoder models have a lasting advantage in tasks with a clear input and output split.
- How much of the decoder-only advantage comes from scale, and how much from the objective itself.

## References

### Seminal papers

- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) — The original encoder-decoder Transformer, which the three families descend from.
- Devlin, J., et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL 2019. [DOI 10.18653/v1/N19-1423](https://doi.org/10.18653/v1/N19-1423) — The encoder-only family, with masked-token pre-training.
- Raffel, C., et al. (2020). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. Journal of Machine Learning Research 21(140), 1–67. [arXiv:1910.10683](https://arxiv.org/abs/1910.10683) — The encoder-decoder family, with span corruption and a unified text-to-text format.
- Brown, T., et al. (2020). *Language Models are Few-Shot Learners*. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) — The decoder-only family at scale, with few-shot prompting.
- Lewis, M., et al. (2019). *BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension*. [arXiv:1910.13461](https://arxiv.org/abs/1910.13461) — A denoising encoder-decoder pre-trained by corrupting and reconstructing text, which the paper relates to BERT and GPT.

### Surveys and textbooks

(none checked for this page)

### Lectures

(none checked for this page)

### Articles and documentation

(none checked for this page)

## Further learning

(none added yet)
