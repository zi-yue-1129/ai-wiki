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

SBERT applies the same BERT encoder, with shared weights, to each sentence separately. A pooling layer turns the token outputs into one vector. The paper tests three pooling strategies, using the `[CLS]` output, a mean of token outputs (MEAN, the default), or the maximum over tokens (MAX). Fine-tuning uses classification, regression or triplet objectives. The paper's similarity evaluation then compares the resulting embeddings with cosine similarity.[^objectives]

Because each sentence is encoded independently, the embeddings of a whole collection can be computed once and stored. Comparison then uses vector arithmetic, including length normalisation when computing cosine similarity.

## Equation and algorithm

### Pooling a padded batch

For a padded sequence of $T$ token states $h_i\in\mathbb R^n$, let $m_i\in\{0,1\}$ indicate which positions participate in pooling. With at least one included position, mean pooling is

$$
s=\frac{\sum_{i=1}^{T}m_i h_i}{\sum_{i=1}^{T}m_i}.
$$

Padding positions have mask zero. The cited Sentence Transformers implementation applies the attention mask to both the summed token states and the denominator in its ordinary mean-pooling path.[^pooling] As a constructed example, states $(2,0)$, $(0,2)$ and $(8,0)$ with mask $(1,1,0)$ pool to $(1,1)$. Averaging all three states instead gives $(10/3,2/3)$. This demonstrates why padded outputs must be excluded. Mean pooling alone does not make the resulting vector unit length.

### Training objectives

The paper uses three training objectives, depending on the labelled data:

- **Classification.** For column embeddings $u,v\in\mathbb R^n$, concatenate $h=[u;v;|u-v|]\in\mathbb R^{3n}$. With $k$ labels and $W\in\mathbb R^{k\times3n}$, compute $o=\operatorname{softmax}(Wh)$. This explicitly uses a column-vector convention; a row-vector convention transposes the weight matrix. The loss is cross-entropy. The element-wise difference term lets the classifier respond to how far the two vectors differ.
- **Regression.** The cosine similarity between `u` and `v` is trained against a gold similarity score with mean-squared error.
- **Triplet.** For an anchor `s_a`, a positive `s_p` and a negative `s_n`, the loss is $\max(\lVert s_a-s_p\rVert_2-\lVert s_a-s_n\rVert_2+\varepsilon,0)$, with Euclidean distance and margin `ε = 1` in the paper's experiments.

The paper evaluates both regression trained only on STSb and classification on natural language inference (NLI) data followed by regression on STSb.[^objectives]

The NLI classifier and the cosine score serve different roles. The classifier produces $k$ class probabilities from the ordered features $[u;v;|u-v|]$. Swapping the sentences gives $[v;u;|u-v|]$, so its output can change with sentence order. Cosine is symmetric and gives one similarity value. The paper uses the embeddings with cosine for STS inference, without the NLI classification head. A cosine score is therefore not an entailment probability.[^objectives]

## Comparing and searching embeddings

For nonzero embeddings $u$ and $v$, cosine similarity can be written as

$$
\operatorname{cos}(u,v)=\frac{u^\top v}{\lVert u\rVert_2\lVert v\rVert_2}
=\widehat u^\top\widehat v,\qquad
\widehat u=\frac{u}{\lVert u\rVert_2},\quad
\widehat v=\frac{v}{\lVert v\rVert_2}.
$$

To reproduce cosine scores with an inner-product search, use the unit vectors $\widehat u,\widehat v$. Raw dot products can give a different ranking. For example, take the constructed query vector $u=(1,0)$.

| Candidate vector | Raw dot product with $u$ | Cosine with $u$ |
|---|---|---|
| $(0.8,0.6)$ | 0.8 | 0.8 |
| $(0.7,0)$ | 0.7 | 1.0 |

Raw dot product ranks the first candidate higher, while cosine ranks the second higher. Normalising the vectors before taking the dot product reproduces the cosine column. These are vector calculations, not measurements of sentence meanings.

Precomputing a collection of $M$ embeddings removes repeated transformer passes over candidate pairs.[^cost] An exhaustive search still computes vector scores. One new query requires $M$ scores for a full scan, and comparing every unordered pair in the collection requires $M(M-1)/2$. At $M=10{,}000$, that is $49{,}995{,}000$ vector comparisons after encoding the sentences once. The model changes the cost of each comparison, while exhaustive comparison retains this pair count.

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

[^objectives]: Reimers and Gurevych (2019), Sections 3 and 4.2 and Figures 1–2, distinguish the training setups from cosine inference. Section 6 states that the concatenation is used for training the softmax classifier. The sentence-order observation follows from the ordered feature vector.
[^pooling]: Sentence Transformers, `pooling.py` at commit `cddcaee`, `_forward_padded`, the ordinary `mean` branch without token weighting, linked below. The masked-mean example assumes at least one included token.
[^cost]: Reimers and Gurevych (2019), Section 1, contrasts repeated cross-encoder computations with independently cached embeddings. The full-scan and pair counts above are direct counts of comparisons.

## References

### Seminal papers

- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. arXiv. https://arxiv.org/abs/1908.10084 — Defines the siamese architecture, the three pooling strategies, the training objectives and the STSb and timing results on this page.
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv. https://arxiv.org/abs/1810.04805 — The encoder that SBERT adapts, and the cross-encoder baseline it is compared with.

### Surveys and textbooks

- Cer, D., Diab, M., Agirre, E., Lopez-Gazpio, I. & Specia, L. (2017). *SemEval-2017 Task 1: Semantic Textual Similarity – Multilingual and Cross-lingual Focused Evaluation*. arXiv. https://arxiv.org/abs/1708.00055 — Introduces the STS Benchmark used for the evaluation on this page.
- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — Background on learned representations and why they transfer.

### Articles and documentation

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — An efficient word-level embedding method, providing background for distributional vectors and sentence averaging.
- Sentence Transformers contributors. *Pooling implementation*. https://github.com/huggingface/sentence-transformers/blob/cddcaee3405a5efde83c1d98f89c6ebd6733dab6/sentence_transformers/sentence_transformer/modules/pooling.py — Implements pooling over padded token states, including attention-mask handling for the mean and its denominator.
