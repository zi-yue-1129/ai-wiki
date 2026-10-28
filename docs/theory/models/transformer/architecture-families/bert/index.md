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
  - pre-training
  - natural language processing
aliases:
  - BERT
  - Bidirectional Encoder Representations from Transformers
  - 雙向編碼器表示
---

# BERT

BERT, or Bidirectional Encoder Representations from Transformers, is an encoder-only [Transformer](../../index.md) pre-trained to predict masked tokens from both left and right context. Devlin et al. (2019) showed that one pre-trained model can be fine-tuned with a single added output layer to reach state-of-the-art results on a wide range of language tasks. It is the landmark of the encoder-only family in the [architecture families](../index.md) overview.

## Overview

Before BERT, most pre-trained language models read text left to right. A left-to-right model can use only the words before a position, which limits what it learns about a word from its context. BERT reads the whole sequence at once, so every position attends to every other position in every layer. Its pre-training task hides some tokens and asks the model to recover them, which lets the bidirectional context be used without leaking the answer.

The paper argues that this design makes the pre-trained representation useful for many tasks with little task-specific architecture. The same network is used for pre-training and for fine-tuning, and only the output layer changes.

## Key concepts

- **WordPiece tokens**: subword units that the input is split into. The masking in pre-training is applied to these tokens.
- **Masked language model (MLM)**: the pre-training task that predicts hidden tokens from their context.
- **Special tokens**: \[CLS\] is placed at the start of every sequence and its final state is used for sentence-level predictions. \[SEP\] separates two sentences.
- **Segment embeddings**: a learned embedding added to each token to say whether it belongs to sentence A or sentence B.
- **Model sizes**: BERT-Base has 12 layers, hidden size 768, 12 heads and about 110M parameters. BERT-Large has 24 layers, hidden size 1024, 16 heads and about 340M parameters.

## How it works

The input is the sum of three embeddings for each token: the WordPiece embedding, a position embedding and a segment embedding. The sequence then passes through a stack of Transformer encoder blocks with bidirectional self-attention.

For pre-training, 15% of the WordPiece tokens in each sequence are selected at random. Of those, 80% are replaced by \[MASK\], 10% by a random token, and 10% are left unchanged. The model predicts the original token at each selected position, so the loss is the cross-entropy over those positions only:

\[
\mathcal{L}_{\text{MLM}} = -\sum_{i \in M} \log p_\theta\big(x_i \mid \tilde{x}\big)
\]

Here \(M\) is the set of selected positions and \(\tilde{x}\) is the corrupted input. The 80/10/10 rule keeps the model from relying on the \[MASK\] token alone, since that token never appears during fine-tuning.

The paper also pre-trains a second task, next sentence prediction. Half the time the second sentence really follows the first, and half the time it is a random sentence from the corpus. The model predicts which case holds from the \[CLS\] state.

The pre-training data is the BooksCorpus (800M words) and English Wikipedia (2,500M words).

## Key methods

### BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (Devlin et al., 2019)

- **Problem:** Language representations from left-to-right models cannot use the right context of a word, and task-specific architectures are needed for each task.
- **Core idea:** Pre-train a bidirectional Transformer encoder with masked-token prediction and sentence-pair prediction, then fine-tune all its weights with one output layer per task.
- **Equation or algorithm:** The masked-language-model loss above, with 15% of tokens selected and the 80/10/10 replacement rule. The next-sentence-prediction loss is a binary cross-entropy on the \[CLS\] state.
- **Results:** The abstract reports a GLUE score of 80.5% (a 7.7-point absolute improvement), MultiNLI accuracy of 86.7% (4.6 points), SQuAD v1.1 test F1 of 93.2 (1.5 points) and SQuAD v2.0 test F1 of 83.1 (5.1 points). It reports new state-of-the-art results on eleven natural language processing tasks.
- **Limitations:** Only 15% of tokens give a training signal in each sequence, so pre-training is expensive. The [MASK] token is absent at fine-tuning time, which the 80/10/10 rule only partly addresses. The model is an encoder, so it does not generate text in the way a decoder does.

## Components and variants

- **Model size.** BERT-Base and BERT-Large differ in depth, width and head count. Larger models gave better results in the paper.
- **Sentence pairs.** The segment embeddings and \[SEP\] token let one model take a pair of sentences for tasks such as question answering and entailment.
- **Objectives.** Next-sentence prediction is one of the two pre-training tasks in the paper. Later variants change the objective, and [T5](../t5/index.md) uses a different corruption objective.

## Connections

- BERT is the encoder-only member of the [architecture families](../index.md). Its encoder block is the one described in [Transformers & Attention](../../index.md).
- The encoder-decoder alternative is [T5](../t5/index.md), which uses the same kind of corruption idea over spans of text.
- The decoder-only alternative is covered by the [GPT-3](../../../llm/gpt-3-few-shot/index.md) page.
- The natural-language-processing applications are on the [NLP](../../../nlp/index.md) page.

## Applications

- Text classification, such as sentiment and topic labels, with a single output layer on top of the pre-trained encoder.
- Question answering on SQuAD-style benchmarks, where the model predicts the answer span from the passage and the question.
- Sentence-pair tasks such as natural language inference and paraphrase detection, as in the GLUE benchmark results.

## Open questions

- Whether next-sentence prediction helps, or whether it is a weak signal that other objectives replace.
- How much of the masked-token approach carries over to very large models, where decoder-only pre-training has become the default.
- How to reduce the cost of pre-training, since most tokens are not used as targets.

## References

### Seminal papers

- Devlin, J., et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL 2019. [DOI 10.18653/v1/N19-1423](https://doi.org/10.18653/v1/N19-1423) — Introduces BERT, pre-trained with masked-token and next-sentence prediction and fine-tuned with one output layer.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) — The Transformer block that BERT's encoder is built from.
- Raffel, C., et al. (2020). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. Journal of Machine Learning Research 21(140), 1–67. [arXiv:1910.10683](https://arxiv.org/abs/1910.10683) — The encoder-decoder comparison point, with a different corruption objective.

### Surveys and textbooks

(none checked for this page)

### Lectures

(none checked for this page)

### Articles and documentation

(none checked for this page)

## Further learning

(none added yet)
