---
related:
- applications/finance
---

# Online Learning & Bandits

## Online learning

Data arrive **one example at a time**; the learner predicts, sees the outcome, and updates immediately. No assumption that data are i.i.d. — in the adversarial setting the sequence can even be chosen by an opponent.

**Performance measure — regret**: how much worse you did than the best fixed decision in hindsight.

\[
\text{Regret}_T = \sum_{t=1}^T \ell_t(w_t) - \min_w \sum_{t=1}^T \ell_t(w)
\]

Good algorithms achieve sublinear regret (e.g. \(O(\sqrt{T})\)), meaning average regret goes to zero.

| Algorithm | Notes |
|---|---|
| Online gradient descent | SGD viewed as an online algorithm |
| Perceptron | Classic online classifier |
| Hedge / multiplicative weights | Combine expert advice; foundational in learning theory and game theory |
| Follow-the-regularised-leader | Unifies many online methods |
| Online Newton step, AdaGrad | Adaptive step sizes (AdaGrad came from online learning) |

## Multi-armed bandits

A gambler faces K slot machines with unknown payout rates. Each pull reveals the reward **only of the arm pulled**. This is the purest form of the **exploration–exploitation trade-off**.

| Algorithm | Idea |
|---|---|
| ε-greedy | Usually exploit, explore with probability ε |
| Upper Confidence Bound (UCB) | "Optimism in the face of uncertainty": pick the arm with the highest plausible mean |
| Thompson sampling | Sample a belief from the posterior, act greedily on it |
| EXP3 | Adversarial bandits |
| Contextual bandits (LinUCB, neural bandits) | Choose an action given features of the situation |

Applications: news and product recommendation, ad placement, A/B testing that adapts traffic, adaptive clinical trials, dynamic pricing, choosing which LLM or prompt to route a query to.

Bandits are the one-step special case of [reinforcement learning](../reinforcement-learning/index.md) — no state transitions.

## Streaming and concept drift

Real streams drift. Tools: drift detectors (ADWIN, DDM, Page–Hinkley), sliding windows, incremental trees (Hoeffding trees), and libraries such as [River](https://riverml.xyz/). See also [Continual Learning](../continual/index.md) and [MLOps](../../../engineering/mlops/index.md).

## Exploration in brains and minds

- Humans use a **mix of directed exploration** (information-seeking, like UCB) and **random exploration** (decision noise, like Thompson/softmax) (Wilson et al., 2014; Gershman, 2018).
- **Locus coeruleus–norepinephrine** system is proposed to switch between exploitation and exploration (Aston-Jones & Cohen, 2005).
- **Frontopolar cortex** activity tracks exploratory choices in bandit tasks (Daw et al., 2006).
- Exploration declines with age, and children explore more than adults — a "high temperature" early-life search (Gopnik, 2020).
- Bandit tasks are standard tools in **computational psychiatry** to measure altered exploration in anxiety, depression and ADHD.

## Subtopics

- [Online convex optimisation](online-convex-optimisation/index.md): online gradient descent, follow-the-regularised-leader and regret bounds.
- [Stochastic bandits](stochastic-bandits/index.md): UCB, Thompson sampling and the logarithmic regret lower bound.
- [Contextual bandits](contextual-bandits/index.md): LinUCB and posterior sampling with features.
- [Adversarial and expert advice](adversarial-and-experts/index.md): weighted majority, Hedge and EXP3.
- [Streaming and concept drift](streaming-and-concept-drift/index.md): Hoeffding trees, drift detection and adaptive windows.

## Further reading

- Lattimore & Szepesvári, *Bandit Algorithms* (free PDF)
- Shalev-Shwartz (2012), "Online Learning and Online Convex Optimization"
- Hazan, *Introduction to Online Convex Optimization* (free)
- Russo et al., "A Tutorial on Thompson Sampling"

## References

### Seminal papers

- Zinkevich (2003), "Online convex programming and generalized infinitesimal gradient ascent", ICML. https://mlanthology.org/icml/2003/zinkevich2003icml-online — Introduces online gradient descent with a regret bound.
- Lai & Robbins (1985), "Asymptotically efficient adaptive allocation rules", Advances in Applied Mathematics. https://doi.org/10.1016/0196-8858(85)90002-8 — Logarithmic lower bound on regret for bandit problems.
- Auer, Cesa-Bianchi & Fischer (2002), "Finite-time analysis of the multiarmed bandit problem", Machine Learning. https://homes.di.unimi.it/~cesabian/Pubblicazioni/ml-02.pdf — UCB1, a simple algorithm with finite-time regret bounds.
- Littlestone & Warmuth (1994), "The weighted majority algorithm", Information and Computation. https://dx.doi.org/10.1006/inco.1994.1009 — Combines expert predictions with multiplicatively updated weights.

### Surveys and textbooks

- Gama et al. (2014), "A survey on concept drift adaptation", ACM Computing Surveys. https://doi.org/10.1145/2523813 — Survey of concept drift detection and adaptation in data streams.
- Hoi, Sahoo, Lu & Zhao (2018), "Online learning: a comprehensive survey", arXiv:1802.02871 — Broad survey of online learning settings and algorithms.
- Lattimore & Szepesvári (2020), *Bandit Algorithms*, Cambridge University Press. https://cambridge.org/core/books/bandit-algorithms/introduction/022B0BDCFDC5B66E5EF2C2690467D928 — Textbook covering the bandit algorithms on this page.
