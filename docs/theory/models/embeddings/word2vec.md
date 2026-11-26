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

CBOW and Skip-gram specify the direction of prediction. The output training objective is a separate choice, including hierarchical softmax or negative sampling.[^objectives]

### Cost with hierarchical softmax

The paper gives a training cost for each model. For $E$ epochs, $T$ training words, vector size $D$, vocabulary size $V$ and the paper's context/window parameters $N$ (CBOW) or $C$ (Skip-gram), its approximate training-cost accounting is $O=E\times T\times Q$, where

- CBOW: $Q=ND+D\log_2V$,
- Skip-gram: $Q=C(D+D\log_2V)$.

The $\log_2V$ term comes from the output layer, which uses a hierarchical softmax over a tree of words. This is why the cost grows slowly with the vocabulary. The later paper by Mikolov et al. (2013b) introduces negative sampling as an alternative to hierarchical softmax, which the parent page mentions and [Goldberg and Levy (2014)](https://arxiv.org/abs/1402.3722) explain in detail.

The training loop is standard stochastic gradient descent over sliding windows of text. Each window gives one or several prediction targets, and the gradient updates the input and output vectors involved: CBOW uses context words as inputs, while Skip-gram uses the centre word as input.

### Skip-gram with negative sampling

Let $v_w\in\mathbb R^D$ be the input vector for centre word $w$, and $u_c\in\mathbb R^D$ the output vector for context $c$. These are separate parameter tables, even when the word and context vocabularies contain the same tokens. Write $s_{wc}=u_c^\top v_w$. For a context vocabulary $\mathcal V$, a full softmax would define the normalised conditional distribution[^objectives]

$$
p_\theta(c\mid w)=\frac{\exp(s_{wc})}{\sum_{c'\in\mathcal V}\exp(s_{wc'})}.
$$

Skip-gram with negative sampling (SGNS) instead trains a binary classifier to distinguish observed word–context pairs from noise pairs. For one observed pair $(w,c)$ and $k\ge1$ context draws $n_r$ from a noise distribution $q$, minimise[^objectives]

$$
\begin{aligned}
\ell(w,c)&=-\log\sigma(s_{wc})-\sum_{r=1}^{k}\log\sigma(-s_{w n_r}),\\
\sigma(s)&=\frac{1}{1+\exp(-s)},\qquad n_r\sim q.
\end{aligned}
$$

This sampled loss evaluates one positive and $k$ negative dot products, costing $O((k+1)D)$ per observed pair for those scores and updates. The earlier hierarchical-softmax cost formula does not describe this output objective. SGNS optimises a different loss from the full-softmax log likelihood.[^objectives]

Mikolov et al. (2013b) use a noise distribution based on unigram frequencies $f(c)$ raised to the power $3/4$,[^noise]

$$
q(c)=\frac{f(c)^{3/4}}{\sum_{c'\in\mathcal V}f(c')^{3/4}}.
$$

This controls which contexts are sampled as negatives. Frequent-word subsampling discards some corpus tokens when forming training examples. A noise sample is a training label, so it does not certify that the sampled word is semantically incompatible with the centre word.[^noise]

## Interpreting the sigmoid

The SGNS sigmoid scores a pair's membership in the observed-versus-noise classification task. It is not normalised over the context vocabulary. To see the distinction, fix a centre word and a context with empirical conditional probability $p=p_{\mathrm{data}}(c\mid w)>0$ and $q(c)>0$. Grouping the expected positive and negative terms gives the pair-specific loss[^interpretation]

$$
j(s)=-p\log\sigma(s)-kq(c)\log\sigma(-s).
$$

If each pair score can be optimised independently, setting $j'(s)=(p+kq(c))\sigma(s)-p$ to zero yields

$$
s^*=\log\frac{p}{kq(c)},\qquad
\sigma(s^*)=\frac{p}{p+kq(c)}.
$$

This idealised optimum assumes independently adjustable pair scores. Finite-dimensional word and context vectors couple the pair scores, so a trained embedding need not attain every such optimum.[^interpretation]

For a constructed two-context example, let $k=5$ and $q(c)=0.5$ for both contexts. Natural logarithms give the following values, rounded to four decimals.

| Context | $p_{\mathrm{data}}(c\mid w)$ | Ideal score $s^*$ | Binary sigmoid $\sigma(s^*)$ |
|---|---|---|---|
| A | 0.8 | -1.1394 | 0.2424 |
| B | 0.2 | -2.5257 | 0.0741 |

The empirical conditional probabilities sum to one, while the ideal binary sigmoids sum to about $0.3165$. Changing $k$ or $q$ changes those sigmoids even when the empirical conditional distribution is fixed. The table illustrates the objective, not measured word2vec outputs.

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

[^objectives]: Mikolov et al. (2013b), Section 2.2, Equation (4), and Goldberg and Levy (2014), Sections 1–2, distinguish the softmax conditional distribution from the negative-sampling objective and its separate word/context vectors. The per-pair cost follows by counting the $k+1$ scored vector pairs.
[^noise]: Mikolov et al. (2013b), Sections 2.2–2.3, specify the $3/4$ noise distribution and the separate frequent-token subsampling procedure. Goldberg and Levy (2014), Section 2, explains the binary labels assigned to sampled pairs.
[^interpretation]: Levy and Goldberg (2014), Sections 3.1–3.2 and footnote 1, analyse independently optimised scores, unigram noise, its smoothed variant and dimensionality constraints. The general-$q$ formula and table here follow by differentiating the displayed expected loss.

## References

### Seminal papers

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — Defines the CBOW and Skip-gram architectures, the training cost of each, and the semantic-syntactic evaluation used on this page.
- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). *Distributed Representations of Words and Phrases and their Compositionality*. arXiv. https://arxiv.org/abs/1310.4546 — Introduces negative sampling as a substitute for the hierarchical softmax, together with subsampling of frequent words.
- Levy, O. & Goldberg, Y. (2014). *Neural Word Embedding as Implicit Matrix Factorization*. NIPS 27. https://proceedings.neurips.cc/paper/2014/hash/b78666971ceae55a8e87efb7cbfd9ad4-Abstract.html — Derives the shifted-PMI interpretation for unigram-noise SGNS and explains how finite embedding dimensions constrain the ideal pair scores.

### Surveys and textbooks

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — A review of why learned, distributed representations help, the setting in which word vectors were developed.

### Articles and documentation

- Goldberg, Y. & Levy, O. (2014). *word2vec Explained: deriving Mikolov et al.'s negative-sampling word-embedding method*. arXiv. https://arxiv.org/abs/1402.3722 — Works through the negative-sampling objective step by step, for readers who find the original notation hard to follow.

### Comparison

- Pennington, J., Socher, R. & Manning, C. (2014). GloVe: Global Vectors for Word Representation. In *Proceedings of EMNLP 2014*, pp. 1532–1543. https://aclanthology.org/D14-1162/ — The count-based alternative that is compared with word2vec on the same analogy test.
