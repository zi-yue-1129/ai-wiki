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

## Further reading

- Lattimore & Szepesvári, *Bandit Algorithms* (free PDF)
- Shalev-Shwartz (2012), "Online Learning and Online Convex Optimization"
- Hazan, *Introduction to Online Convex Optimization* (free)
- Russo et al., "A Tutorial on Thompson Sampling"
