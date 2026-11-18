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

When fine-tuned as a sentence-pair cross-encoder, BERT takes both sentences as one input and outputs a similarity score. This cross-encoder is accurate, but it must run once for every pair. Reimers and Gurevych (2019) give the cost for finding the most similar pair among 10,000 sentences: about 50 million pairwise inferences, roughly 65 hours on a V100 GPU. Simply averaging BERT's token outputs, or using the `[CLS]` vector, gave weak sentence embeddings. The paper reports Spearman correlations of 46.35 for the average and 16.50 for the `[CLS]` vector on the STS benchmark. The question was how to obtain embeddings that compare well and can be computed once per sentence.

## Core idea

SBERT runs two copies of the same BERT encoder with shared weights on the two sentences. A pooling layer turns the token outputs into one vector. The paper tests three pooling strategies: the `[CLS]` output, the mean of all token outputs (MEAN, the default), and the maximum over tokens (MAX). The weights are then fine-tuned on sentence-pair data so that cosine similarity between the two pooled vectors reflects the target label.

Because each sentence is encoded independently, the embeddings of a whole collection can be computed once and stored. Comparison then costs only the arithmetic of a dot product.

## Equation and algorithm

The paper uses three training objectives, depending on the labelled data:

- **Classification.** For column embeddings \(u,v\in\mathbb R^n\), concatenate \(h=[u;v;|u-v|]\in\mathbb R^{3n}\). With \(k\) labels and \(W\in\mathbb R^{k\times3n}\), compute \(o=\operatorname{softmax}(Wh)\). This explicitly uses a column-vector convention; a row-vector convention transposes the weight matrix. The loss is cross-entropy. The element-wise difference term lets the classifier respond to how far the two vectors differ.
- **Regression.** The cosine similarity between `u` and `v` is trained against a gold similarity score with mean-squared error.
- **Triplet.** For an anchor `s_a`, a positive `s_p` and a negative `s_n`, the loss is \(\max(\lVert s_a-s_p\rVert_2-\lVert s_a-s_n\rVert_2+\varepsilon,0)\), with Euclidean distance and margin `ε = 1` in the paper's experiments.

Training starts from natural language inference data, with the classification objective, and can be followed by fine-tuning on the STS benchmark with the regression objective.

## Results

[Reimers and Gurevych (2019), Tables 1–2](https://aclanthology.org/D19-1410/), report Spearman correlation (× 100) on the STS benchmark (STSb). The rows that are not trained on STSb show the transfer from natural language inference data alone:

| Model | Spearman |
|---|---|
| BERT average embeddings | 46.35 |
| SBERT-NLI-base (not trained on STSb) | 77.03 |
| SBERT-NLI-large (not trained on STSb) | 79.23 |
| SBERT-NLI-STSb-base | 85.35 ± 0.17 |
| SBERT-NLI-STSb-large | 86.10 ± 0.13 |
| BERT cross-encoder, NLI and STSb, base (reference) | 88.33 ± 0.19 |

In these NLI-plus-STSb comparisons, the cross-encoder scores higher; this is not a universal accuracy ordering across models or tasks. For the 10,000-sentence search, the paper reports about 5 seconds to compute the embeddings and about 0.01 seconds for the cosine comparisons.

## Limitations

- **Cross-topic transfer.** In the paper's Argument Facet Similarity experiment, training on two topics and evaluating on a third leaves SBERT about seven Spearman points behind BERT. This illustrates a limitation of that data/setup, not a universal minimum number of training topics.
- **Independent encoding.** Each sentence is mapped without seeing the other, so SBERT cannot use the word-level attention between the two sentences that the cross-encoder uses.
- **Scope of the original transfer tests.** Section 5 evaluates frozen embeddings with SentEval classifiers. The authors emphasise similarity search rather than treating those embeddings as a substitute for task-specific BERT fine-tuning. This does not rule out transfer learning with later sentence-embedding models.
- **Mixed comparisons.** SBERT trails the Universal Sentence Encoder on some tasks, such as SICK-R and TREC, and the paper reports no significant gain from RoBERTa in its experiments.

## References

### Seminal papers

- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. arXiv. https://arxiv.org/abs/1908.10084 — Defines the siamese architecture, the three pooling strategies, the training objectives and the STSb and timing results on this page.
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv. https://arxiv.org/abs/1810.04805 — The encoder that SBERT adapts, and the cross-encoder baseline it is compared with.

### Surveys and textbooks

- Cer, D., Diab, M., Agirre, E., Lopez-Gazpio, I. & Specia, L. (2017). *SemEval-2017 Task 1: Semantic Textual Similarity – Multilingual and Cross-lingual Focused Evaluation*. arXiv. https://arxiv.org/abs/1708.00055 — Introduces the STS Benchmark used for the evaluation on this page.
- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — Background on learned representations and why they transfer.

### Articles and documentation

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — An efficient word-level embedding method, providing background for distributional vectors and sentence averaging.
