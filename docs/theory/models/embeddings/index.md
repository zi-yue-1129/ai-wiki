---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised/index.md
  - brain-mind/neuroai
tags:
  - representation learning
  - embeddings
  - word vectors
aliases:
  - Embeddings
  - 嵌入表示
  - 嵌入向量
  - representation learning
  - 表徵學習
  - word2vec
---

# Embeddings and Representation Learning

An embedding maps an object, such as a word, sentence, image, user or graph node, to a vector, so that the geometry of the vector space reflects the similarity the task cares about. Once objects live in such a space, distance, angle and simple linear operations become useful tools for search, clustering, classification and recommendation. Learning the embedding, rather than designing it by hand, is what made embeddings central to modern AI.

## Overview

Bengio, Courville and Vincent (2012) frame the problem as *representation learning*: finding a transformation of the input that makes the features useful for many later tasks. Their review argues that good representations are often distributed, meaning each concept is spread over many units, and that they disentangle the factors that vary in the data. An embedding is the most common concrete form of such a representation: a fixed-length vector, stored and compared directly.

The same idea appears in every modality. A word embedding places words with related uses near each other. A sentence embedding places whole passages in one space so that they can be compared. An image–text embedding puts pictures and captions in one space. The training signal decides what the geometry means, and that choice is the main design decision.

## Key concepts

- **Embedding table**: a lookup from discrete items, such as word identifiers, to learned vectors.
- **Similarity**: usually cosine similarity or a dot product between two vectors, after normalisation.
- **Contrastive objective**: a loss that pulls matching pairs together and pushes non-matching pairs apart.
- **Triplet loss**: a loss over an anchor, a positive and a negative example, requiring the anchor to be closer to the positive by a margin.
- **Dimensionality**: the length of the vector. Higher dimensions hold more information, at a larger cost in storage and search.

## How it works

Four families of training signal cover most embeddings in use.

**Prediction from context.** word2vec (Mikolov et al., 2013) learns word vectors from large text corpora by predicting words from their neighbours. Words that occur in similar contexts end up with similar vectors. The paper's aim was to make such training efficient enough to run on very large corpora.

**Factorising co-occurrence counts.** GloVe (Pennington, Socher & Manning, 2014) starts from global word–word co-occurrence statistics and learns vectors whose inner products reflect them. It combines the global counts used by older count-based methods with the vector structure of prediction-based ones.

**Metric learning.** FaceNet (Schroff et al., 2015) trains a deep convolutional network to map face images into a space where distances reflect identity. The paper trains the embedding itself with a triplet-based objective, so that the same person is closer than a different person by a margin. The learned vectors are then used directly for recognition and clustering.

**Aligning modalities and sentences.** Sentence-BERT (Reimers & Gurevych, 2019) adapts a pre-trained transformer into a siamese network, so that sentences can be embedded once and compared with cosine similarity, rather than passed through the model in pairs. CLIP (Radford et al., 2021) learns image and text encoders from natural language supervision, so that matching images and captions have similar embeddings and can be used for zero-shot classification by comparing an image with text prompts.

## Key methods

Brief comparison. Each named method is a candidate for its own method page; those pages are not yet written, so the detail is given in this section for now.

- **word2vec (prediction from context)**: local context prediction, fast on large text. Produces static word vectors, one per word.
- **GloVe (co-occurrence factorisation)**: global counts, static word vectors. Similar role to word2vec, with a different route to the vectors.
- **FaceNet (metric learning)**: a learned embedding for identity, trained with a triplet-based objective. Specialised to comparisons between instances.
- **Sentence-BERT (siamese encoder)**: contextual sentence vectors that can be compared quickly. Trained for similarity rather than generation.
- **CLIP (modality alignment)**: a shared space for images and text, learned from paired data.

## Connections

Embeddings are the bridge between the [Transformer](../transformer/index.md) and [Large Language Models](../llm/index.md) on one side and retrieval, recommendation and multimodal systems on the other. Self-supervised pre-training is the usual source of the training signal, see [Self-Supervised Learning](../../paradigms/self-supervised/index.md). Image–text embeddings are central to [Multimodal Models](../multimodal/index.md).

Distributed representations have a long history in neuroscience. Population codes, in which a stimulus is represented by the joint activity of many neurons, are a natural counterpart to embedding vectors, and similarity structure in neural population activity is compared with model representations in [NeuroAI](../../../brain-mind/neuroai/index.md). The comparison is a hypothesis to be tested, not an established equivalence.

## Applications

- **Search and retrieval.** Nearest-neighbour search over embeddings finds documents, images or products similar to a query.
- **Recommendation.** Users and items are embedded so that the score is a similarity between them.
- **Face recognition and clustering.** FaceNet-style embeddings compare identities by distance.
- **Zero-shot classification.** Images are classified by comparing their embeddings with text descriptions of the classes.

## Open questions

- Static embeddings give a word one vector regardless of its sense. Contextual embeddings solve this, but at the cost of computing them per use.
- What the geometry of an embedding space means is hard to read, and similarity may encode biases from the training data.
- It is still unclear how much of an embedding's usefulness comes from scale of data rather than from the training objective.

## References

### Seminal papers

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — Introduces efficient word-vector training from large corpora, the basis of word2vec.
- Pennington, J., Socher, R. & Manning, C. (2014). GloVe: Global Vectors for Word Representation. In *Proceedings of EMNLP 2014*, pp. 1532–1543. https://aclanthology.org/D14-1162/ — Learns word vectors from global co-occurrence statistics.
- Schroff, F., Kalenichenko, D. & Philbin, J. (2015). *FaceNet: A Unified Embedding for Face Recognition and Clustering*. arXiv. https://arxiv.org/abs/1503.03832 — Trains a deep network to embed face images directly, with a triplet-based objective.
- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. arXiv. https://arxiv.org/abs/1908.10084 — Produces sentence embeddings that can be compared with cosine similarity, without pairwise passes through the model.
- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. & Sutskever, I. (2021). *Learning Transferable Visual Models From Natural Language Supervision*. arXiv. https://arxiv.org/abs/2103.00020 — CLIP: image and text embeddings learned from natural language supervision, with zero-shot transfer.

### Surveys and textbooks

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — A review of representation learning and the properties that make representations useful.
