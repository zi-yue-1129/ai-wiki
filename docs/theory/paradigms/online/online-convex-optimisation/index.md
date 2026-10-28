---
related:
- theory/paradigms/supervised/loss-functions-and-optimization/index.md
tags:
  - online learning
  - regret
  - online convex optimisation
---

# Online Convex Optimisation

Online convex optimisation is the basic framework of online learning. In each round the learner picks a point in a convex set, then a convex loss is revealed, and the learner is judged by its regret against the best fixed point in hindsight. Most online algorithms are variants of online gradient descent analysed in this framework.

## Overview

Regret is the gap between the learner's total loss and the loss of the best fixed decision chosen after seeing all rounds. For convex losses on bounded sets, online gradient descent with a decreasing step size achieves regret of order the square root of the number of rounds, so average regret goes to zero. Stronger assumptions, such as strongly convex losses, give logarithmic regret.

## Key algorithms

- **Online gradient descent**: take a gradient step after each loss and project back to the feasible set. Simple and optimal for general convex losses.
- **Follow-the-regularised-leader**: play the minimiser of past losses plus a regulariser, which unifies many algorithms.
- **Adaptive methods**: scale each coordinate's step size by its past gradients, which is the origin of AdaGrad.

## Connections

The framework is a non-stochastic view of [supervised learning](../../supervised/loss-functions-and-optimization/index.md): stochastic gradient descent is the same algorithm with i.i.d. data, and the regret bounds become generalisation bounds through an online-to-batch conversion. The same algorithms train the large models described in [engineering: training](../../../../engineering/training/index.md).

## Applications

Online advertising and recommendation models that update as clicks arrive, portfolio selection that rebalances each day, and large-scale linear classifiers trained on streams of web data.

## Open questions

Regret bounds are worst case and can be pessimistic for benign data. Adapting step sizes to data without tuning, and extending the framework to non-convex losses used in deep learning, are still active areas.

## References

### Seminal papers

- Zinkevich (2003), "Online convex programming and generalized infinitesimal gradient ascent", ICML. https://www.cs.cmu.edu/~maz/publications/ICML03.pdf — Introduces online gradient descent and proves its regret bound for convex losses.
- Bottou (2010), "Large-scale machine learning with stochastic gradient descent", COMPSTAT. https://leon.bottou.org/papers/bottou-2010 — Shows how stochastic gradient descent, viewed as an online method, scales to very large datasets.

### Surveys and textbooks

- Shalev-Shwartz (2012), "Online learning and online convex optimization", Foundations and Trends in Machine Learning. https://www.cs.huji.ac.il/~shais/papers/OLsurvey.pdf — Survey that develops the regret framework and its main algorithms from first principles.
- Hazan (2019), "Introduction to online convex optimization", [arXiv:1909.05207](https://arxiv.org/abs/1909.05207) — Textbook introduction with proofs of the main regret bounds.
- Hoi, Sahoo, Lu & Zhao (2018), "Online learning: a comprehensive survey", [arXiv:1802.02871](https://arxiv.org/abs/1802.02871) — Survey covering online convex methods alongside other online learning settings.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Cesa-Bianchi & Lugosi (2006), *Prediction, Learning, and Games*, Cambridge University Press. https://www.cambridge.org/core/books/abs/prediction-learning-and-games/preface/57367F57F5C14A8E04EC732E20711EA1 — Covers online prediction with expert advice and games in depth.
