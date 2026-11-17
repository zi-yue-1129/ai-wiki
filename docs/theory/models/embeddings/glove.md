---
status: draft
tags:
  - word vectors
  - embeddings
  - representation learning
aliases:
  - GloVe
  - Global Vectors for Word Representation
  - 全域詞向量
  - 共現矩陣分解
---

# GloVe

GloVe (Global Vectors for Word Representation) learns one vector per word by fitting the logarithm of word–word co-occurrence counts over the whole corpus. It was designed to combine two families of methods: count-based methods, which use global statistics, and prediction-based methods such as [word2vec](word2vec.md), which capture linear structure in the vectors. The parent page, [Embeddings and Representation Learning](index.md), places it among the other training signals.

## Problem

Pennington, Socher and Manning (2014) observed that the two families had complementary strengths. Count-based methods such as latent semantic analysis use global co-occurrence statistics efficiently, but they performed poorly on word analogies. Window-based prediction methods captured the linear structure that the analogies test, but they learned from local windows and did not use the global counts directly. The question was whether one model could use both.

## Core idea

Let `X_ij` be the number of times word `j` appears in the context of word `i`. GloVe learns a vector `w_i` for each word, a separate context vector `w̃_j`, and a bias for each, so that the dot product of the two vectors, plus the biases, approximates the logarithm of the count. Frequent pairs must fit well, and rare pairs should not dominate the fit, so each term is weighted.

The result is a model that starts from the full co-occurrence matrix, as count-based methods do, but optimises a regression target in the style of prediction-based methods. The authors argue that the two families are not fundamentally different, because both draw on the same co-occurrence statistics.

## Equation and algorithm

The model minimises a weighted least-squares objective over all pairs in a vocabulary of size `V`:

`J = Σ_{i,j=1}^{V} f(X_ij) (w_iᵀ w̃_j + b_i + b̃_j − log X_ij)²`

The weighting function is

`f(x) = (x / x_max)^α` if `x < x_max`, and `f(x) = 1` otherwise,

with `x_max = 100` and `α = 3/4`. The weight gives less influence to very frequent pairs, and the authors report that the choice of cutoff matters only weakly. They also report that `α = 3/4` gave a modest improvement over a linear weighting with `α = 1`.

Training is a single pass to build the co-occurrence matrix, followed by an iterative optimisation of `J` over the non-zero entries. Because only pairs with `X_ij > 0` contribute, the optimisation cost depends on the number of observed pairs rather than on the full vocabulary.

## Results

The paper evaluates on word analogies, using the same semantic and syntactic question sets as [word2vec](word2vec.md). The accuracies in the paper's Table 2 include:

| Model | Vector size | Corpus | Semantic | Syntactic | Overall |
|---|---|---|---|---|---|
| GloVe | 300 | 42B tokens | 81.9% | 69.3% | 75.0% |
| GloVe | 300 | 6B tokens | 77.4% | 67.0% | 71.7% |
| Skip-gram (authors' run) | 300 | 6B tokens | 73.0% | 66.0% | 69.1% |
| CBOW (authors' run) | 300 | 6B tokens | 63.6% | 67.4% | 65.7% |

The 75% headline figure comes from the 42-billion-token model. The authors also report that, when corpus, vocabulary, window size and training time are matched, GloVe outperforms word2vec. The corpora were Wikipedia dumps, Gigaword 5 and Common Crawl, and the vocabularies were the most frequent 400,000 words, apart from the Common Crawl model.

## Limitations

- **Empirical weighting.** The authors justify `α = 3/4` only empirically.
- **Hard comparison.** Many parameters affect word2vec and GloVe, so the comparison depends on defaults. The authors acknowledge that a more thorough analysis would relax this simplification.
- **Corpus effects.** Semantic accuracy did not increase monotonically with corpus size. The authors attribute part of this to Gigaword being a fixed news source that may contain outdated facts.
- **Cost bound.** The worst-case complexity is quadratic in the vocabulary size. A tighter estimate relies on an assumed power-law distribution of co-occurrences.
- **Static vectors.** As with word2vec, each word has one vector whatever its sense.

## References

### Seminal papers

- Pennington, J., Socher, R. & Manning, C. (2014). GloVe: Global Vectors for Word Representation. In *Proceedings of EMNLP 2014*, pp. 1532–1543. https://aclanthology.org/D14-1162/ — Defines the weighted least-squares objective, the weighting function and the analogy results reported on this page.
- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — The prediction-based word2vec models that GloVe is compared against.

### Surveys and textbooks

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — Background on distributed representations and why they generalise.

### Articles and documentation

- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). *Distributed Representations of Words and Phrases and their Compositionality*. arXiv. https://arxiv.org/abs/1310.4546 — The negative-sampling variant of word2vec, used in most comparisons with GloVe.
- Goldberg, Y. & Levy, O. (2014). *word2vec Explained: deriving Mikolov et al.'s negative-sampling word-embedding method*. arXiv. https://arxiv.org/abs/1402.3722 — Explains the word2vec objective that GloVe's results are compared with.
