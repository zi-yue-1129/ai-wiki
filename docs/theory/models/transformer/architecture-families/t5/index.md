---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/architecture-families
  - theory/models/transformer
  - theory/models/nlp
tags:
  - transformers
  - language models
  - transfer learning
  - pre-training
aliases:
  - T5
  - Text-to-Text Transfer Transformer
  - 文字到文字遷移 Transformer
---

# T5: Text-to-Text Transfer Transformer

T5, or the Text-to-Text Transfer Transformer, is an encoder-decoder [Transformer](../../index.md) that treats every language task as text in and text out. Raffel et al. (2020) pre-train it on a span-corruption objective, and fine-tune it on each task in the same text format. The paper also contributes the C4 corpus and a systematic comparison of the design choices behind transfer learning for language.

## Overview

BERT-style models need a task-specific output layer for each task, and that layer has a different shape for classification, span extraction and sequence labelling. T5 removes this difference: the input is a string that names the task, and the output is a string with the answer. Translation, summarisation, classification and question answering all use the same model and loss.

The paper is also a survey of choices. It compares pre-training objectives, architectures, unlabelled datasets and transfer approaches on many language understanding tasks, and reports how each choice affects the results.

## Key concepts

- **Text-to-text format**: every task is cast as mapping an input string to an output string. Classification outputs are the label words, not class indices.
- **Span corruption**: random spans of the input are replaced by sentinel tokens, and the target is the sequence of dropped spans, each introduced by its sentinel.
- **C4 (Colossal Clean Crawled Corpus)**: a cleaned web-text corpus of about 750 GB, built for pre-training.
- **Model sizes**: the paper trains models up to 11 billion parameters.

## How it works

The encoder reads the corrupted input with bidirectional self-attention. The decoder generates the target sequence token by token, with causal self-attention and cross-attention to the encoder output. The loss is the usual cross-entropy on the target tokens.

In span corruption, the paper drops 15% of input tokens and replaces each consecutive span of dropped tokens with one sentinel token. The target is the sequence of dropped spans, each preceded by its sentinel. This differs from the BERT-style masked language model. The target is the dropped spans rather than the masked tokens in place, and a decoder generates them.

\[
\mathcal{L} = -\sum_{t} \log p_\theta\big(y_t \mid y_{<t},\ \tilde{x}\big)
\]

where \(\tilde{x}\) is the corrupted input with sentinels and \(y\) is the target sequence of dropped spans.

## Key methods

### Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (Raffel et al., 2020)

- **Problem:** Transfer learning in language had many methods, each with its own task format and architecture, so it was hard to tell which design choices mattered.
- **Core idea:** Cast every task in one text-to-text format, pre-train an encoder-decoder with a denoising objective on a large clean corpus, and compare the design choices systematically under one framework.
- **Equation or algorithm:** The span-corruption cross-entropy above, with 15% of input tokens dropped and replaced by sentinel-marked spans.
- **Results:** The abstract reports that combining the exploration with scale and the C4 corpus gives state-of-the-art results on many benchmarks, covering summarisation, question answering and text classification. The paper releases the dataset, pre-trained models and code. The largest model has 11 billion parameters.
- **Limitations:** The 11-billion-parameter model is expensive to train and serve, and the paper's comparison is at a fixed compute budget. The text-to-text format also needs an output string for every task, which can make tasks with rich structured outputs awkward.

## Components and variants

- **Architecture.** The paper compares encoder-decoder and decoder-only variants under one framework, and reports how they differ on its task suite.
- **Objective.** Span corruption is compared with BERT-style masking and with prefix language modelling in the paper's comparison.
- **Scale.** The released models span several sizes, and the largest, at 11 billion parameters, is the one that reports the top results.

## Connections

- T5 is the encoder-decoder member of the [architecture families](../index.md). Its encoder and decoder blocks are described in [Transformers & Attention](../../index.md).
- [BERT](../bert/index.md) is the encoder-only alternative, with a masked-token objective that span corruption generalises.
- The decoder-only alternative is covered on the [GPT-3](../../../llm/gpt-3-few-shot/index.md) page.
- The language applications are on the [NLP](../../../nlp/index.md) page.

## Applications

- Summarisation and translation with one fine-tuned model per task.
- Question answering and text classification, cast as generating an answer string.
- Transfer to new language tasks by writing a task prefix and a target string, without a new output layer.

## Open questions

- Whether the text-to-text format still helps when a model is trained on instruction data at very large scale, where decoder-only models dominate.
- How much of the comparison's conclusions depend on the fixed compute budget used in the study.
- Whether span corruption is the best denoising objective, or whether other corruption patterns give better transfer.

## References

### Seminal papers

- Raffel, C., et al. (2020). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. Journal of Machine Learning Research 21(140), 1–67. [arXiv:1910.10683](https://arxiv.org/abs/1910.10683) — Introduces T5, the text-to-text framing, span corruption and the C4 corpus.
- Devlin, J., et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL 2019. [DOI 10.18653/v1/N19-1423](https://doi.org/10.18653/v1/N19-1423) — The masked-token objective that span corruption generalises.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) — The encoder-decoder Transformer that T5 uses.
- Lewis, M., et al. (2019). *BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension*. [arXiv:1910.13461](https://arxiv.org/abs/1910.13461) — A denoising encoder-decoder pre-trained by corrupting and reconstructing text, which the paper relates to BERT and GPT.
- Brown, T., et al. (2020). *Language Models are Few-Shot Learners*. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) — Scales the decoder-only model to 175 billion parameters and reports few-shot results from prompts alone.

### Surveys and textbooks

(none checked for this page)

### Lectures

(none checked for this page)

### Articles and documentation

(none checked for this page)

## Further learning

(none added yet)
