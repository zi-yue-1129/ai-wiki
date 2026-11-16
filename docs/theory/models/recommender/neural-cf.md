---
status: draft
last_reviewed: 2026-11-14
related:
  - theory/models/recommender
tags:
  - recommender systems
  - collaborative filtering
  - deep learning
aliases:
  - Neural Collaborative Filtering
  - NCF
  - NeuMF
  - 神經協同過濾
---

# Neural Collaborative Filtering (He et al., 2017)

Neural collaborative filtering (NCF) replaces the fixed inner product of [matrix factorisation](matrix-factorization.md) with a neural network that learns how a user and an item interact. The paper's main model, NeuMF, combines a matrix-factorisation path with a multi-layer perceptron (MLP) path.

This page is part of [Recommender Systems](index.md).

## Problem

Deep learning had succeeded in speech, vision and language, but in recommendation it was mostly used for side information, such as item text or audio. The user–item interaction itself was still scored by a matrix-factorisation inner product. He et al. (2017) ask whether a learned interaction function can improve pure collaborative filtering, which uses only the interaction data.

## Core idea

Each user and item is represented by an embedding. Instead of taking the inner product of the two vectors, the model passes them through layers that can learn a non-linear interaction. The paper states that NCF is generic and can express and generalise matrix factorisation within its framework. The output is a score that the user will interact with the item.

## Equation and training

The prediction has the form $\hat{y}_{ui} = f(P^{\top} v_u^{U}, Q^{\top} v_i^{I} \mid P, Q, \Theta_f)$, where $v_u^{U}$ and $v_i^{I}$ are one-hot encodings of the user and item, $P$ and $Q$ are the embedding matrices, and $f$ is the network. The network is trained on observed interactions as positives and sampled unobserved items as negatives, with four negatives per positive in the main setup. The loss is log loss, which the paper identifies with binary cross-entropy. The objective is non-convex, so gradient methods are not guaranteed to find a global optimum.

## Architecture

NeuMF combines two paths, and the paper lets each path learn its own embeddings.

- **GMF path.** The element-wise product of the user and item embeddings is kept as a vector, which generalises the matrix-factorisation inner product.
- **MLP path.** The user and item embeddings are concatenated and passed through hidden layers with ReLU activations.

The two paths are fused by concatenating the GMF product vector with the last MLP hidden layer. A final output layer with a sigmoid activation gives the predicted score. The paper also studies pre-training each path before the joint training.

## Results

The paper evaluates on two datasets. MovieLens has 1,000,209 interactions, 6,040 users and 3,706 items, with the explicit ratings converted to implicit feedback. The Pinterest subset has 1,500,809 interactions, 55,187 users and 9,916 items. The protocol is leave-one-out: one interaction of each user is held out as the test item, and it is ranked against 100 sampled items the user has not interacted with. Hit ratio (HR@10) and NDCG@10 measure the result. The baselines include ItemPop, item-based nearest neighbours (ItemKNN), BPR and eALS.

- With pre-training, NeuMF on MovieLens with 64 factors reaches HR@10 of 0.730 and NDCG@10 of 0.447.
- On Pinterest with 8 factors, NeuMF with pre-training reaches HR@10 of 0.878 and NDCG@10 of 0.555.
- The average relative improvement over the eALS and BPR baselines is 4.5% and 4.9%.
- Stacking MLP layers also helps. On MovieLens with 8 factors, HR@10 rises from 0.452 with no hidden layers to 0.678 with four layers. The authors also note that a model with no hidden layers is not better than the non-personalised ItemPop baseline.

## Limitations

- The paper's experiments focus on the pure collaborative-filtering setting. Side information is not used.
- Pairwise learning for NCF, such as the [BPR](bpr.md) objective, is left as future work, and so is non-uniform negative sampling.
- Large embedding sizes may overfit and reduce performance.
- Because the NeuMF objective is non-convex, gradient-based training is not guaranteed to find a global optimum.
- The evaluation uses sampled negatives. Scores on 100 sampled items are not the same as ranking the full catalogue.

## Connections

NCF keeps the embedding view of recommendation from the [Recommender Systems](index.md) overview and the [embedding](../embeddings/index.md) page. The MLP path is a standard [feed-forward network](../mlp/index.md).

## Applications

- **Personalised ranking** of items from logged clicks or purchases, where the learned interaction function replaces a fixed inner product.
- **Benchmarking** on public datasets with sampled-negative top-N metrics, a protocol the paper uses.

## Open questions

- How much a learned interaction function adds over a well-tuned inner product, on data other than these two, is not settled by the paper's experiments.
- The paper ranks each held-out item against 100 sampled negatives. Its numbers therefore do not directly show performance when ranking the full catalogue.

## References

### Seminal papers

- He, X., Liao, L., Zhang, H., Nie, L., Hu, X. & Chua, T.-S. (2017). Neural collaborative filtering. In *Proceedings of the 26th International Conference on World Wide Web (WWW 2017)*, pp. 173–182. https://doi.org/10.1145/3038912.3052569 — The source of this page: NeuMF, its datasets, leave-one-out protocol and HR@10 and NDCG@10 results.
- Koren, Y., Bell, R. & Volinsky, C. (2009). Matrix factorization techniques for recommender systems. *Computer*, 42, pp. 30–37. https://doi.org/10.1109/MC.2009.263 — The inner-product model that NCF generalises.
- Rendle, S., Freudenthaler, C., Gantner, Z. & Schmidt-Thieme, L. (2012). *BPR: Bayesian Personalized Ranking from Implicit Feedback*. arXiv:1205.2618, first published at UAI 2009. https://arxiv.org/abs/1205.2618 — The pairwise BPR baseline that NCF is compared against, and the pairwise objective it leaves to future work.
- Sarwar, B., Karypis, G., Konstan, J. & Riedl, J. (2001). Item-based collaborative filtering recommendation algorithms. In *Proceedings of the 10th International World Wide Web Conference (WWW10)*, pp. 285–295. https://doi.org/10.1145/371920.372071 — A neighbourhood baseline for item-based collaborative filtering, cited for context.

### Surveys and textbooks

- Ricci, F., Rokach, L. & Shapira, B. (eds.) (2015). *Recommender Systems Handbook*, 2nd ed. Springer. https://doi.org/10.1007/978-1-4899-7637-6 — Reference handbook covering collaborative, content-based and hybrid methods, and evaluation.
