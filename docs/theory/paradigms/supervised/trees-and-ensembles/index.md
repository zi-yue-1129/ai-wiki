---
tags:
  - supervised learning
  - ensembles
  - tabular data
---

# Decision Trees and Ensembles

Tree-based methods split the input space into regions with simple rules, and ensembles combine many trees. On tabular data, gradient-boosted trees are still usually the strongest practical choice.

## Decision trees

A tree recursively picks the feature and threshold that best separates the labels, using an impurity measure: Gini impurity $1-\sum_k p_k^2$ or entropy $-\sum_k p_k\log p_k$ for classification, variance for regression (CART, Breiman et al. 1984; ID3/C4.5, Quinlan). A single deep tree has low bias and high variance; pruning or depth limits control it. Trees need no feature scaling, handle mixed data types and missing values, and give readable rules.

## Bagging and random forests

**Bagging** trains many trees on bootstrap resamples and averages them, which reduces variance. **Random forests** (Breiman, 2001) also pick a random subset of features at every split, which decorrelates the trees. Out-of-bag samples give a free validation estimate. Forests are robust, need little tuning and rarely overfit badly.

## Boosting

Boosting builds trees sequentially, each one correcting the errors of the ensemble so far.

- **AdaBoost** re-weights misclassified examples.
- **Gradient boosting** (Friedman, 2001) fits each new tree to the negative gradient of the loss, so $F_m = F_{m-1} + \eta\, h_m$.
- **XGBoost, LightGBM, CatBoost** add second-order information, regularisation, histogram-based splits and better handling of categorical features.

| Method | Reduces | Trees are | Tuning effort |
|---|---|---|---|
| Bagging / forest | Variance | Deep, independent | Low |
| Boosting | Bias (and some variance) | Shallow, sequential | Medium |

## Stacking and other ensembles

Stacking trains a meta-model on the predictions of diverse base models. Averaging several neural networks (deep ensembles) is also a strong baseline for uncertainty estimates.

## Key methods

Each named method has its own page with the problem, core idea, equations, results and limitations.

- [Random forests](random-forests.md) (Breiman, 2001): bagged trees with random feature selection at each split.
- [Gradient boosting](gradient-boosting.md) (Friedman, 2001): trees fitted in sequence to the negative gradient of the loss. The same page covers [XGBoost](gradient-boosting.md) (Chen & Guestrin, 2016), with brief notes on LightGBM and CatBoost.

## Connections

Why do trees beat deep networks on many tabular tasks? Grinsztajn et al. (2022) point to irregular target functions and uninformative features, where trees are more robust. Tree ensembles are widely used in finance, healthcare risk scoring and recommender ranking; see [Applications](../../../../applications/index.md).

## References

### Seminal papers

- Quinlan, J. R. (1986). Induction of decision trees. *Machine Learning*, 1(1), 81–106. https://doi.org/10.1007/BF00116251 — The ID3 algorithm for building decision trees by information gain.
- Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324 — Bagged trees with random feature selection, and out-of-bag error estimates.
- Friedman (2001), "Greedy function approximation: a gradient boosting machine", *Annals of Statistics* 29(5). https://doi.org/10.1214/AOS/1013203451 — Derives gradient boosting as gradient descent in function space.
- Ke et al. (2017), "LightGBM: a highly efficient gradient boosting decision tree", NeurIPS. https://neurips.cc/virtual/2017/poster/9099 — Histogram-based splits and leaf-wise tree growth for faster boosting on large data.
- Prokhorenkova et al. (2018), "CatBoost: unbiased boosting with categorical features", NeurIPS. https://proceedings.neurips.cc/paper/2018/hash/14491b756b3a51daac41c24863285549-Abstract.html — Ordered boosting and target statistics for categorical features without leakage.

### Surveys and textbooks

- Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning*, Springer (2009), chapters 9, 10 and 15. https://doi.org/10.1007/978-0-387-84858-7 — Covers trees, boosting and random forests in depth, with a free PDF from the authors.

### Lectures and videos

- Friedman, J. H. (2001). Greedy function approximation: a gradient boosting machine. *Annals of Statistics*, 29(5), 1189–1232. https://doi.org/10.1214/aos/1013203451 — Introduces gradient boosting, which adds weak learners by gradient descent in function space.

### Articles and documentation

- Grinsztajn, Oyallon & Varoquaux (2022), "Why do tree-based models still outperform deep learning on tabular data?", NeurIPS, [arXiv:2207.08815](https://arxiv.org/abs/2207.08815) — Benchmark and analysis explaining why tree ensembles often beat neural networks on tabular data.

## Further learning

- StatQuest with Josh Starmer, episodes on random forests and gradient boosting, YouTube. https://www.youtube.com/@statquest — Step-by-step animated walkthroughs of how trees are built and combined.

## Further reading

- Chen & Guestrin (2016), "XGBoost: a scalable tree boosting system", KDD. https://arxiv.org/abs/1603.02754 — The XGBoost system: regularised gradient-boosted trees built for speed and scale.
