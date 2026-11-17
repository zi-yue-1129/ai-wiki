---
status: draft
tags:
  - sentence embeddings
  - siamese networks
  - embeddings
aliases:
  - Sentence-BERT
  - SBERT
  - 句子嵌入
  - 孿生 BERT
---

# Sentence-BERT

Sentence-BERT (SBERT) turns a pre-trained BERT or RoBERTa into a siamese network that produces one fixed-size vector per sentence. Two sentences can then be compared with cosine similarity, without passing every pair through the model. The approach is the sentence-level member of the embedding family on the parent page, [Embeddings and Representation Learning](index.md), and it addresses a cost problem that the plain BERT cross-encoder cannot avoid.

## Problem

BERT takes a pair of sentences as one input and outputs a similarity score. This cross-encoder is accurate, but it must run once for every pair. Reimers and Gurevych (2019) give the cost for finding the most similar pair among 10,000 sentences: about 50 million pairwise inferences, roughly 65 hours on a V100 GPU. Simply averaging BERT's token outputs, or using the `[CLS]` vector, gave weak sentence embeddings. The paper reports Spearman correlations of 46.35 for the average and 16.50 for the `[CLS]` vector on the STS benchmark. The question was how to obtain embeddings that compare well and can be computed once per sentence.

## Core idea

SBERT runs two copies of the same BERT encoder with shared weights on the two sentences. A pooling layer turns the token outputs into one vector. The paper tests three pooling strategies: the `[CLS]` output, the mean of all token outputs (MEAN, the default), and the maximum over tokens (MAX). The weights are then fine-tuned on sentence-pair data so that cosine similarity between the two pooled vectors reflects the target label.

Because each sentence is encoded independently, the embeddings of a whole collection can be computed once and stored. Comparison then costs only the arithmetic of a dot product.

## Equation and algorithm

The paper uses three training objectives, depending on the labelled data:

- **Classification.** For sentence embeddings `u` and `v` of dimension `n` and `k` labels, the model forms `(u, v, |u − v|)`, applies a trainable matrix `W_t ∈ ℝ^{3n×k}`, and takes a softmax, `o = softmax(W_t(u, v, |u − v|))`. The loss is cross-entropy. The element-wise difference term lets the classifier respond to how far the two vectors differ.
- **Regression.** The cosine similarity between `u` and `v` is trained against a gold similarity score with mean-squared error.
- **Triplet.** For an anchor `s_a`, a positive `s_p` and a negative `s_n`, the loss is `max(‖s_a − s_p‖ − ‖s_a − s_n‖ + ε, 0)`, with Euclidean distance and margin `ε = 1` in the paper's experiments.

Training starts from natural language inference data, with the classification objective, and can be followed by fine-tuning on the STS benchmark with the regression objective.

## Results

The paper reports Spearman correlation (× 100) on the STS benchmark (STSb). The rows that are not trained on STSb show the transfer from natural language inference data alone:

| Model | Spearman |
|---|---|
| BERT average embeddings | 46.35 |
| SBERT-NLI-base (not trained on STSb) | 77.03 |
| SBERT-NLI-large (not trained on STSb) | 79.23 |
| SBERT-NLI-STSb-base | 85.35 ± 0.17 |
| SBERT-NLI-STSb-large | 86.10 ± 0.13 |
| BERT cross-encoder, NLI and STSb, base (reference) | 88.33 ± 0.19 |

The cross-encoder remains more accurate, which is the trade-off the method accepts. For the 10,000-sentence search, the paper reports about 5 seconds to compute the embeddings and about 0.01 seconds for the cosine comparisons.

## Limitations

- **Cross-topic transfer.** On the Argument Facet Similarity corpus, SBERT's cross-topic performance dropped by about seven points of Spearman correlation relative to BERT. The authors say that training needs more than two topics to work.
- **Independent encoding.** Each sentence is mapped without seeing the other, so SBERT cannot use the word-level attention between the two sentences that the cross-encoder uses.
- **Not a general transfer model.** The authors say SBERT embeddings are not meant for transfer learning, and they suggest fine-tuning BERT for a new task instead.
- **Mixed comparisons.** SBERT trails the Universal Sentence Encoder on some tasks, such as SICK-R and TREC, and the paper reports no significant gain from RoBERTa in its experiments.

## References

### Seminal papers

- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. arXiv. https://arxiv.org/abs/1908.10084 — Defines the siamese architecture, the three pooling strategies, the training objectives and the STSb and timing results on this page.
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv. https://arxiv.org/abs/1810.04805 — The encoder that SBERT adapts, and the cross-encoder baseline it is compared with.

### Surveys and textbooks

- Cer, D., Diab, M., Agirre, E., Lopez-Gazpio, I. & Specia, L. (2017). *SemEval-2017 Task 1: Semantic Textual Similarity – Multilingual and Cross-lingual Focused Evaluation*. arXiv. https://arxiv.org/abs/1708.00055 — Introduces the STS Benchmark used for the evaluation on this page.
- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — Background on learned representations and why they transfer.

### Articles and documentation

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — The word-level embeddings that averaging BERT tokens was meant to compete with, and the origin of the vector-comparison idea.
