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

The Bayesian view links to [Probabilistic & Bayesian Methods](../../probabilistic/index.md). In psychology, exemplar theories of categorisation are kNN-like and prototype theories are centroid classifiers.

## References

### Seminal papers

- Cover, T. M. & Hart, P. E. (1967). Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, 13(1), 21–27. https://doi.org/10.1109/TIT.1967.1053964 — Proves the asymptotic error bound for the nearest-neighbour rule.
- Ng & Jordan (2001), "On discriminative vs. generative classifiers: a comparison of logistic regression and naive Bayes", NeurIPS. https://papers.nips.cc/paper/2001/hash/7b7a53e239400a13bd6be6c91c4f6c4e-Abstract.html — Compares how much data each classifier needs and when each wins.
- Bartlett, Jordan & McAuliffe (2006), "Convexity, classification, and risk bounds", *JASA* 101(473), 138–156. https://doi.org/10.1198/016214505000000907 — Shows which convex surrogate losses still yield good classifiers.
- Niculescu-Mizil & Caruana (2005), "Predicting good probabilities with supervised learning", ICML. https://doi.org/10.1145/1102351.1102430 — Empirical comparison of probability calibration across standard classifiers.
- Guo et al. (2017), "On calibration of modern neural networks", ICML, arXiv:1706.04599 — Shows that predicted probabilities can be miscalibrated and proposes temperature scaling as a fix.

### Surveys and textbooks

- Rasmussen & Williams, *Gaussian Processes for Machine Learning*, MIT Press (2006). Free online chapters: https://gaussianprocess.org/gpml/chapters — The standard reference for Gaussian process models and their inference.

### Lectures and videos

- Hand, D. J. & Yu, K. (2001). Idiot’s Bayes: not so stupid after all? *International Statistical Review*, 69(3), 385–398. https://doi.org/10.1111/j.1751-5823.2001.tb00465.x — Explains why naive Bayes classifiers perform well even when the independence assumption fails.

### Articles and documentation

(none beyond the entries above)

## Further learning

- StatQuest with Josh Starmer, episodes on Naive Bayes, YouTube. https://www.youtube.com/@statquest — Visual, step-by-step explanation of how Naive Bayes computes class probabilities.

## Further reading

- Murphy, *Probabilistic Machine Learning: An Introduction*, MIT Press (2022). https://probml.github.io/pml-book/ — Free online textbook; covers probabilistic classifiers such as naive Bayes.
