---
related:
- theory/paradigms/reinforcement-learning/index.md
- theory/paradigms/imitation/adversarial-imitation/index.md
tags:
  - imitation learning
  - inverse reinforcement learning
  - reward learning
---

# Inverse Reinforcement Learning

Inverse reinforcement learning (IRL) infers the reward function that an expert appears to be optimising, given observations of the expert's behaviour. Once a reward is recovered, a policy can be trained with ordinary [reinforcement learning](../../reinforcement-learning/index.md). Because the reward is a compact description of intent, the learned policy can generalise to states the expert never visited, which [behavioural cloning](../behavioural-cloning/index.md) cannot do reliably.

## Overview

IRL is ill-posed. Many reward functions, including the trivial zero reward, make the same expert behaviour optimal, so practical methods need a rule for choosing among them. The main approaches differ in how they resolve this ambiguity and how they match the expert's feature expectations.

## Key approaches

- **Feature matching** (Abbeel & Ng, 2004): assume the reward is a linear combination of known features and search for a policy whose feature expectations match the expert's. The learned policy is then a mixture that is close to the expert in feature space.
- **Maximum-entropy IRL** (Ziebart et al., 2008): among all reward-consistent distributions over trajectories, choose the one with the highest entropy. This gives a probabilistic model of demonstrations that is robust to sub-optimal experts.
- **Guided cost learning** (Finn, Levine & Abbeel, 2016): scales maximum-entropy IRL to high-dimensional inputs such as images by estimating the partition function with samples from a learned policy, and by alternating reward and policy updates.
- **Early reward-recovery methods** (Ng & Russell, 2000): give the first formal treatment of recovering rewards from optimal policies, including the ambiguity problem.

## Ambiguity and identifiability

Because of the ambiguity noted above, recovered rewards may not transfer to new environments or to different dynamics. Regularisation, entropy objectives and assumptions about the expert's rationality are the usual ways to make the problem well-defined, but each adds modelling choices that can be wrong.

## Connections

IRL is the inverse of [reinforcement learning](../../reinforcement-learning/index.md): RL maps rewards to policies, IRL maps policies to rewards. The probabilistic view links it to Bayesian models of how people infer others' goals, a topic also touched on in [psychology and AI](../../../../brain-mind/psychology/index.md). Adversarial methods such as [adversarial imitation](../adversarial-imitation/index.md) can be seen as a practical route to IRL without an explicit inner RL loop.

## Applications

Modelling driver preferences for autonomous driving, learning cost functions for robot motion planning, inferring reward models for human-aware navigation, and explaining the goals behind observed human decisions.

## Open questions

Reward ambiguity remains the central difficulty, and recovered rewards are often sensitive to features and regularisation. Inner-loop RL is expensive, and it is unclear how to recover rewards from experts with limited or inconsistent rationality.

## References

### Seminal papers

- Ng & Russell (2000), "Algorithms for inverse reinforcement learning", ICML. https://aima.eecs.berkeley.edu/~russell/papers/ml00-irl.pdf — Early formal treatment of recovering rewards from optimal behaviour, including the ambiguity problem.
- Abbeel & Ng (2004), "Apprenticeship learning via inverse reinforcement learning", ICML. https://icml.cc/Conferences/2004/proceedings/abstracts/335.htm — Feature-matching apprenticeship learning with guarantees on performance relative to the expert.
- Ziebart, Maas, Bagnell & Dey (2008), "Maximum entropy inverse reinforcement learning", AAAI. https://www.cs.cmu.edu/~bziebart/publications/maximum-entropy-inverse-reinforcement-learning.html — Probabilistic IRL that picks the highest-entropy distribution consistent with demonstrations.
- Finn, Levine & Abbeel (2016), "Guided cost learning: deep inverse optimal control via policy optimization", ICML, [arXiv:1603.00448](https://arxiv.org/abs/1603.00448) — Scales maximum-entropy IRL to high-dimensional inputs with learned costs and a sampling-based partition function.

### Surveys and textbooks

- Osa et al. (2018), "An algorithmic perspective on imitation learning", [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — Survey covering reward-recovery methods alongside behavioural cloning.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Fu, Luo & Levine (2018), "Learning robust rewards with adversarial inverse reinforcement learning", ICLR, [arXiv:1710.11248](https://arxiv.org/abs/1710.11248) — Adversarial IRL that yields rewards which transfer across dynamics.
