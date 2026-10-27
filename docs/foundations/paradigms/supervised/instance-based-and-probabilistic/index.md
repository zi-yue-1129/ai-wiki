---
tags:
  - supervised learning
  - probabilistic models
  - bayesian
---

# Instance-Based and Probabilistic Classifiers

Two families that reason about new inputs by similarity to stored examples (k-nearest neighbours) or by explicit probability models (naive Bayes, discriminant analysis, Gaussian processes).

## k-nearest neighbours (kNN)

Store the training set; to classify $x$, find its $k$ closest examples under a distance (Euclidean, cosine, learned metric) and vote, or average for regression. There is no training phase. kNN suffers from the curse of dimensionality, since distances become uninformative in high dimensions, and from slow queries, which approximate nearest-neighbour indexes (HNSW, product quantisation) mitigate. Cover & Hart (1967) proved that the 1-NN error is at most twice the Bayes error as $n\to\infty$. Modern retrieval-augmented systems, such as kNN-LM and vector-database lookups, are kNN over learned embeddings.

## Generative classifiers

These model $p(x\mid y)$ and $p(y)$, then apply Bayes' rule: $p(y\mid x)\propto p(x\mid y)p(y)$.

- **Naive Bayes** assumes features are conditionally independent given the class. The assumption is wrong but the classifier works well for text and spam filtering with little data.
- **Linear / quadratic discriminant analysis** assume Gaussian class densities with shared (LDA) or per-class (QDA) covariance.
- **Hidden Markov models and CRFs** extend the idea to sequences; CRFs are the discriminative counterpart.

Ng & Jordan (2001) showed that generative classifiers reach their (higher) asymptotic error faster, while discriminative ones such as logistic regression win with more data.

## Gaussian processes (GPs)

A GP places a prior over functions, $f\sim\mathcal{GP}(m,k)$, and returns a full predictive distribution at each point:

$$
\mu_* = K_*^\top (K+\sigma^2 I)^{-1} y,\qquad \sigma_*^2 = k_{**} - K_*^\top (K+\sigma^2 I)^{-1}K_*.
$$

GPs give calibrated uncertainty with few data points and drive Bayesian optimisation and [active learning](../../active/index.md). Exact inference costs $O(n^3)$, so sparse and variational approximations are used for large sets.

## Connections

The Bayesian view links to [Probabilistic & Bayesian Methods](../../../probabilistic/index.md). In psychology, exemplar theories of categorisation (Nosofsky) are kNN-like and prototype theories are centroid classifiers.

## Further reading

- Cover & Hart (1967), "Nearest neighbor pattern classification", *IEEE Transactions on Information Theory* 13(1). The k-NN error bound.
- Ng & Jordan (2001), "On discriminative vs. generative classifiers: a comparison of logistic regression and naive Bayes", NeurIPS. The sample-complexity comparison discussed above.
- Rasmussen & Williams, *Gaussian Processes for Machine Learning* (2006). Free online; the standard GP reference.
- Murphy, *Probabilistic Machine Learning: An Introduction* (2022). Chapters on generative classifiers and GPs.
- Video: StatQuest with Josh Starmer (YouTube channel), episodes on Naive Bayes.
