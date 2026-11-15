---
status: draft
last_reviewed: 2026-11-14
related:
  - theory/models/recommender
tags:
  - recommender systems
  - implicit feedback
  - ranking
aliases:
  - BPR
  - Bayesian Personalized Ranking
  - Bayesian Personalised Ranking
  - 貝氏個人化排序
---

# BPR: Bayesian Personalised Ranking (Rendle et al., 2012)

Bayesian Personalised Ranking (BPR) trains a recommender from implicit feedback by learning which items a user prefers over others, rather than by fitting a score to each interaction. The method is a standard starting point for top-N ranking.

This page is part of [Recommender Systems](index.md).

## Problem

Implicit feedback such as clicks, views and purchases records what a user did, not what the user disliked. A missing interaction may mean "not interested" or "never seen". Common models, such as matrix factorisation and nearest-neighbour methods, are usually trained to predict a value for each observed entry. Rendle et al. (2012) argue that none of these is trained directly on the ranking task, which is what the recommender is used for.

## Core idea

For a user $u$, an observed item $i$ should be ranked above an unobserved item $j$. BPR turns each user's history into such pairs and learns a model in which the pairwise order holds. The method is generic: the paper applies it to matrix factorisation and to adaptive nearest-neighbour models.

## Equation

Let $\hat{x}_{uij}$ be the model's score difference for user $u$ between items $i$ and $j$, written as $\hat{x}_{ui} - \hat{x}_{uj}$. The likelihood that the user prefers $i$ to $j$ is modelled with the logistic sigmoid:

$$p(i >_u j \mid \Theta) = \sigma\left(\hat{x}_{uij}(\Theta)\right), \qquad \sigma(x) = \frac{1}{1 + e^{-x}}$$

With a zero-mean normal prior on the parameters $\Theta$, the paper's maximum posterior estimate gives the criterion BPR-Opt:

$$\text{BPR-Opt} = \sum_{(u,i,j)\in D_S} \ln \sigma\left(\hat{x}_{uij}\right) - \lambda_\Theta \lVert \Theta \rVert^2$$

Here $D_S$ is the set of training triples and $\lambda_\Theta$ is a model-specific regularisation parameter.

## Algorithm

The criterion is optimised by stochastic gradient ascent over sampled triples. The paper chooses the triples uniformly at random and uses bootstrap sampling with replacement, which means training can be stopped at any step. For each step, one observed pair $(u, i)$ is drawn with a randomly chosen unobserved item $j$, and the parameters move in the direction that increases $\ln \sigma(\hat{x}_{uij})$.

## Results

The paper evaluates on two datasets converted to implicit feedback. The first is a Rossmann online-shop purchase history with 10,000 users, 4,000 items and 426,612 purchases. The second is a Netflix subsample of 10,000 users and 5,000 items with 565,738 rating actions, where the ratings are stripped to implicit feedback. The exact AUC values are shown in a figure in the paper. The text reports the following comparisons:

- On both datasets, BPR-MF "outperforms WR-MF clearly for the task of ranking".
- On Netflix, an 8-dimensional BPR-MF model achieves comparable quality to a 128-dimensional WR-MF model.
- The two BPR-optimised methods outperform the other methods in prediction quality.
- The quality of SVD-MF decreases as the number of dimensions increases.

## Limitations

- The paper focuses on offline learning of the model parameters. Online learning is mentioned as a possible extension, and the authors note that a fold-in strategy could be used, but they do not evaluate it.
- The authors compute an upper bound on the AUC that is "non-tight", so the bound does not show how close the methods come to the best achievable ranking.
- Hyperparameters were set by grid search in the first round and then kept constant in the remaining repetitions.
- The paper draws the unobserved item $j$ uniformly at random. It does not study other ways of choosing negatives. [Neural collaborative filtering](neural-cf.md) likewise leaves non-uniform negative sampling as future work.

## Connections

BPR is a pairwise ranking loss, a close relative of the ranking objectives used in learning to rank. Its user and item factors are the same kind of [embedding](../embeddings/index.md) that the [matrix factorisation](matrix-factorization.md) page describes, and it is the ranking baseline against which [neural collaborative filtering](neural-cf.md) is compared.

## Applications

- **Product and media ranking**, where logged purchases or views are the only signal available.
- **Top-N lists**, where the output is an ordered short list and the order matters more than the predicted value.

## Open questions

- Which negatives should be sampled for pairwise training, and how much does that choice change the final ranking?
- How should pairwise objectives be combined with the sequential and context information that now drives many recommenders?

## References

### Seminal papers

- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2012). *BPR: Bayesian Personalized Ranking from Implicit Feedback*. arXiv:1205.2618, first published at UAI 2009. https://arxiv.org/abs/1205.2618 — The source of this page: the BPR-Opt criterion, sampled training triples and AUC comparisons.
- Sarwar, B., Karypis, G., Konstan, J. & Riedl, J. (2001). Item-based collaborative filtering recommendation algorithms. In *Proceedings of the 10th International World Wide Web Conference (WWW10)*, pp. 285–295. https://doi.org/10.1145/371920.372071 — A neighbourhood baseline for item-based collaborative filtering, cited for context.
- Koren, Y., Bell, R. & Volinsky, C. (2009). Matrix factorization techniques for recommender systems. *Computer*, 42, pp. 30–37. https://doi.org/10.1109/MC.2009.263 — The rating-based matrix factorisation that BPR-MF retrains with a ranking objective.
- He, X., Liao, L., Zhang, H., Nie, L., Hu, X. & Chua, T.-S. (2017). Neural collaborative filtering. In *Proceedings of the 26th International Conference on World Wide Web (WWW 2017)*, pp. 173–182. https://doi.org/10.1145/3038912.3052569 — A later model evaluated with top-N metrics, which lists pairwise learning as future work.

### Surveys and textbooks

- Ricci, F., Rokach, L. & Shapira, B. (eds.) (2015). *Recommender Systems Handbook*, 2nd ed. Springer. https://doi.org/10.1007/978-1-4899-7637-6 — Reference handbook covering collaborative, content-based and hybrid methods, and evaluation.
