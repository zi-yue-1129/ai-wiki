---
status: draft
last_reviewed: 2026-10-28
tags:
  - retrieval
  - large language models
aliases:
  - DSSM
  - 深層結構化語意模型
---

# DSSM (Huang et al. 2013)

The Deep Structured Semantic Model (DSSM) maps a query and a web document into the same low-dimensional vector space, so that relevance becomes a distance between two vectors. Huang and colleagues trained it on clickthrough data from a web search engine. It is one of the early neural methods for [retrieval in web search](../index.md), and the parent topic page is [Search Engines and Information Retrieval](../index.md).

## Overview

Keyword retrieval scores a document by the words it shares with the query. Two texts about the same subject can share few words, and a query such as a symptom description may match a document that uses different medical vocabulary. Latent semantic models, such as latent semantic analysis (LSA), tackled this by projecting text into a low-dimensional space, but they were trained without the clicks that tell a search engine what people actually wanted.

## Key concepts

- **Two towers**: one network for the query and one for the document. Each maps its text to a vector, and the two networks are not shared.
- **Cosine relevance**: the relevance of a document to a query is the cosine similarity of their two vectors.
- **Word hashing**: each word is split into letter trigrams with boundary markers, so "go" becomes "#go" and "go#". The vocabulary stays small, and misspellings and rare words share features with known ones.
- **Clickthrough training**: a document that a user clicked for a query is a positive example, and documents shown but not clicked, or sampled from the collection, serve as negatives.

## How it works

For a query $Q$ and a document $D$, let $y_Q$ and $y_D$ be the vectors produced by the two towers. The relevance and the probability of a document given the query are

$$
R(Q,D) = \cos(y_Q, y_D), \qquad P(D \mid Q) = \frac{\exp(\gamma R(Q,D))}{\sum_{D' \in \mathcal{D}} \exp(\gamma R(Q,D'))}
$$

where $\gamma$ is a smoothing factor and $\mathcal{D}$ is the set of candidates for the query, which includes the clicked document $D^{+}$. Training maximises the likelihood of the clicked documents, which is equivalent to minimising $-\sum \log P(D^{+} \mid Q)$ over the training pairs.

The procedure is:

1. Convert each query and document into a bag of letter trigrams (word hashing).
2. Pass each representation through several nonlinear layers in its own tower, producing a low-dimensional vector.
3. For a query with a clicked document and sampled negatives, compute the cosine similarity of each pair.
4. Apply the softmax above and update both towers by gradient descent on the negative log-likelihood of the clicked document.
5. At serving time, encode all documents once and store their vectors. For each query, encode the query and rank the stored documents by cosine similarity.

Step 5 is what makes the model practical. Document vectors are computed offline, so the online cost is one query encoding and a nearest-neighbour search.

## Results

The paper evaluates the models on a web document ranking task built from real search data. The authors report that their best model significantly outperforms the other latent semantic models, which were the state of the art before this work. The abstract gives no figures, so this page does not quote numbers.

## Limitations

- **No word-level interaction.** The query and document meet only through one cosine score, so the model cannot see which query word matches which passage word. Later models, such as the Duet model of Mitra et al. (2016), combine exact term matching with distributed representations for this reason.
- **Bag of trigrams.** Word hashing removes word order and makes the representation coarse, so phrases with different meanings but the same letters can collide.
- **Single vector per document.** One vector must summarise a whole document. Long documents with several topics lose detail, which motivates multi-vector methods such as [ColBERT](../../../engineering/vector-databases/colbert.md).

## Open questions

- Dual encoders are now common for first-stage retrieval, but the best way to train them, and whether they can match the accuracy of cross-encoders, remains debated.

## Connections

- The dual-encoder design is the same idea as [Dense passage retrieval](../../../engineering/vector-databases/dense-passage-retrieval.md), which was introduced for open-domain question answering.
- The training objective is a softmax over candidates of the kind used in [contrastive learning](../../../theory/paradigms/self-supervised/contrastive-learning/index.md).
- Candidates retrieved this way are then ordered by a ranker such as [RankNet](../ranknet/index.md) or by a model like [Wide & Deep](../wide-and-deep/index.md).

## Applications

DSSM-style two-tower models are used to retrieve candidate documents, ads and items in search and recommendation, where the item vectors can be indexed in advance.

## References

### Seminal papers

- Huang, P.-S. et al. (2013). Learning deep structured semantic models for web search using clickthrough data. CIKM. https://doi.org/10.1145/2505515.2505665 — Trains query and document networks on clickthrough data so that clicked documents score higher in a shared semantic space, with word hashing for scale.
- Mitra, B., Diaz, F. & Craswell, N. (2016). Learning to match using local and distributed representations of text for web search. https://arxiv.org/abs/1610.08136 — Combines exact term matching with learned distributed representations for web document ranking, addressing the lack of word-level interaction in dual encoders.
- Karpukhin, V. et al. (2020). Dense passage retrieval for open-domain question answering. https://arxiv.org/abs/2004.04906 — Shows that a trained dual encoder with a dot-product score can replace BM25 for passage retrieval, using a small set of question and passage pairs.
- Formal, T. et al. (2021). SPLADE: Sparse lexical and expansion model for first stage ranking. https://arxiv.org/abs/2107.05720 — Learns sparse query and document representations that keep the efficiency of inverted indexes, a competing answer to dense first-stage retrieval.

### Surveys and textbooks

- Lin, J., Nogueira, R. & Yates, A. (2020). Pretrained transformers for text ranking: BERT and beyond. https://arxiv.org/abs/2010.06467 — Survey of neural text ranking that places dual encoders and rerankers side by side and compares their trade-offs.
