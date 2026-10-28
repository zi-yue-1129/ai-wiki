---
related:
- theory/paradigms/online/online-convex-optimisation/index.md
- theory/paradigms/online/stochastic-bandits/index.md
tags:
  - online learning
  - prediction with expert advice
  - adversarial bandits
---

# Adversarial and Expert Advice

Adversarial online learning makes no statistical assumptions about the data. An adversary chooses each outcome, possibly knowing the learner's algorithm, and the learner must still perform well relative to the best expert or action in hindsight. Multiplicative-weights methods and their bandit versions are the standard tools.

## Overview

In prediction with expert advice, the learner combines the predictions of several experts. Weighted-majority and Hedge keep a weight for each expert, shrink the weights of experts that err, and achieve regret of order the square root of the number of rounds times the log of the number of experts. When only the chosen action's reward is seen, the EXP3 algorithm achieves a similar bound by using importance-weighted estimates.

## Key algorithms

- **Weighted majority**: combine expert predictions with weights that shrink multiplicatively after mistakes.
- **Hedge (multiplicative weights)**: the same idea for losses in a continuous range, and the basis of many game-theoretic and boosting results.
- **EXP3**: an adversarial bandit algorithm that uses importance-weighted loss estimates to explore.

## Connections

Hedge is the source of the boosting algorithm AdaBoost, which is covered in [trees and ensembles](../../supervised/trees-and-ensembles/index.md). EXP3 is the adversarial counterpart of the methods in [stochastic bandits](../stochastic-bandits/index.md). Multiplicative weights also appear in the game-theoretic view of [reinforcement learning](../../reinforcement-learning/index.md), where two players learn against each other.

## Applications

Combining forecasts from many models, spam filtering with adaptive expert weights, and online portfolio and trading strategies that must hold up under adversarial markets.

## Open questions

Adversarial guarantees can be pessimistic for real data, and adaptive algorithms that do well both when data is adversarial and when it is benign are still being developed. Bandit feedback makes the adversarial setting much harder.

## References

### Seminal papers

- Littlestone & Warmuth (1994), "The weighted majority algorithm", Information and Computation. https://dx.doi.org/10.1006/inco.1994.1009 — Introduces weighted majority, with regret bounds for combining expert predictions.
- Freund & Schapire (1997), "A decision-theoretic generalization of on-line learning and an application to boosting", Journal of Computer and System Sciences. https://www.schapire.net/papers/FreundSc95.pdf — Hedge, a multiplicative-weights algorithm that also underlies AdaBoost.
- Auer, Cesa-Bianchi, Freund & Schapire (2002), "The nonstochastic multiarmed bandit problem", SIAM Journal on Computing. https://homepages.math.uic.edu/~lreyzin/papers/auer02.pdf — EXP3, an adversarial bandit algorithm with importance-weighted estimates.

### Surveys and textbooks

- Bubeck & Cesa-Bianchi (2012), "Regret analysis of stochastic and nonstochastic multi-armed bandit problems", Foundations and Trends in Machine Learning, arXiv:1204.5721 — Survey that covers the adversarial bandit results alongside the stochastic ones.
- Shalev-Shwartz (2012), "Online learning and online convex optimization", Foundations and Trends in Machine Learning. https://www.cs.huji.ac.il/~shais/papers/OLsurvey.pdf — Survey that places expert advice within the wider online learning framework.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Cesa-Bianchi & Lugosi (2006), *Prediction, Learning, and Games*, Cambridge University Press. No link checked.
