---
status: draft
tags:
  - word vectors
  - embeddings
  - representation learning
aliases:
  - word2vec
  - Word2Vec
  - skip-gram
  - CBOW
  - 詞向量
  - 詞嵌入
---

# word2vec

word2vec is a family of efficient methods for learning one dense vector per word from a large text corpus. Its two architectures, CBOW and Skip-gram, learn the vectors as a by-product of predicting words from their neighbours. The method is the best-known example of prediction-based word embeddings, and it is the reference point for the [GloVe](glove.md) page, which takes the count-based route to similar vectors. The parent page, [Embeddings and Representation Learning](index.md), compares this with the other training signals.

## Problem

Earlier neural language models learned good word vectors, but they were costly to train. Their cost grew with the vocabulary and with the size of the hidden layer, making very large-corpus training expensive. Mikolov et al. (2013) asked how to learn word vectors of good quality from corpora with billions of words, and how to measure whether the vectors captured meaning.

## Core idea

Both architectures drop the hidden non-linear layer of the earlier models and keep only a projection of each word into a vector space.

- **CBOW (continuous bag of words)** predicts the middle word from the words around it. The paper's setup uses four history words and four future words as input, and its training criterion is to classify the current word correctly.
- **Skip-gram** does the reverse. It takes the current word as input and predicts the words within a window of size `C` before and after it.

Words that occur in similar contexts receive similar vectors, because the same prediction task encourages related distributional representations, without guaranteeing identical vectors. The vector space therefore records distributional similarity, and the paper reports that some relations such as capital cities and past tenses are approximately linear in it.

## Equation and algorithm

The paper gives a training cost for each model. For \(E\) epochs, \(T\) training words, vector size \(D\), vocabulary size \(V\) and the paper's context/window parameters \(N\) (CBOW) or \(C\) (Skip-gram), its approximate training-cost accounting is \(O=E\times T\times Q\), where

- CBOW: \(Q=ND+D\log_2V\),
- Skip-gram: \(Q=C(D+D\log_2V)\).

The \(\log_2V\) term comes from the output layer, which uses a hierarchical softmax over a tree of words. This is why the cost grows slowly with the vocabulary. The later paper by Mikolov et al. (2013b) introduces negative sampling as an alternative to hierarchical softmax, which the parent page mentions and [Goldberg and Levy (2014)](https://arxiv.org/abs/1402.3722) explain in detail.

The training loop is standard stochastic gradient descent over sliding windows of text. Each window gives one or several prediction targets, and the gradient updates the input and output vectors involved: CBOW uses context words as inputs, while Skip-gram uses the centre word as input.

## Results

The paper evaluates vectors on a semantic-syntactic word relationship test. Each question asks for a word that completes an analogy, such as one word being to another as a city is to its country. The accuracies below are from Tables 5 and 6 of [Mikolov et al. (2013)](https://arxiv.org/abs/1301.3781); the 6B-word rows use distributed DistBelief training, not the same setup as the 1.6B-word rows:

| Model | Vector size | Training words | Semantic | Syntactic | Total |
|---|---|---|---|---|---|
| CBOW | 300 | 1.6B (1 epoch) | 16.1% | 52.6% | 36.1% |
| Skip-gram | 300 | 1.6B (1 epoch) | 52.2% | 55.1% | 53.8% |
| CBOW | 1000 | 6B | 57.3% | 68.9% | 63.7% |
| Skip-gram | 1000 | 6B | 66.1% | 65.1% | 65.6% |

These paired rows give Skip-gram higher semantic accuracy than CBOW. The paper studies gains from corpus size and vector dimension; these selected results do not establish that either increase always improves every metric. The table is the paper's own; the figures were not recomputed for this page.

## Limitations

- **No morphology.** The models receive no information about the internal structure of words. The authors state that reaching 100% accuracy on the test is likely impossible for this reason, and they suggest adding word-structure information.
- **Exact-match scoring.** The test counts a synonym that differs from the expected word as an error.
- **One vector per word.** Each word has a single vector whatever its sense, a limitation that contextual models later addressed.
- **Training cost at scale.** The paper expects that larger corpora and larger vectors will do better, and the cost grows with both, which motivated distributed training.

## References

### Seminal papers

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — Defines the CBOW and Skip-gram architectures, the training cost of each, and the semantic-syntactic evaluation used on this page.
- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). *Distributed Representations of Words and Phrases and their Compositionality*. arXiv. https://arxiv.org/abs/1310.4546 — Introduces negative sampling as a substitute for the hierarchical softmax, together with subsampling of frequent words.

### Surveys and textbooks

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — A review of why learned, distributed representations help, the setting in which word vectors were developed.

### Articles and documentation

- Goldberg, Y. & Levy, O. (2014). *word2vec Explained: deriving Mikolov et al.'s negative-sampling word-embedding method*. arXiv. https://arxiv.org/abs/1402.3722 — Works through the negative-sampling objective step by step, for readers who find the original notation hard to follow.

### Comparison

- Pennington, J., Socher, R. & Manning, C. (2014). GloVe: Global Vectors for Word Representation. In *Proceedings of EMNLP 2014*, pp. 1532–1543. https://aclanthology.org/D14-1162/ — The count-based alternative that is compared with word2vec on the same analogy test.
