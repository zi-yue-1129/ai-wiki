---
tags:
  - imitation learning
  - behavioural cloning
---

# Behavioural Cloning

Behavioural cloning treats imitation as supervised learning: it fits a policy that maps observations to the actions an expert took in the same situations. It is the simplest and most widely used form of imitation learning, and it is the starting point for most robot and driving systems.

## Overview

Collect a dataset of expert state–action pairs $(s_i, a_i)$ and minimise a loss between the policy's prediction $\pi_\theta(s_i)$ and $a_i$. For continuous actions this is usually mean squared error, and for discrete actions it is cross-entropy. No reward or environment interaction is needed during training, which makes the method cheap and stable.

## Why it fails

Behavioural cloning suffers from **covariate shift**. The learner's own mistakes lead it to states the expert never visited, and in those states it has no training data. Small errors then compound over a long trajectory, so a policy with low training loss can still fail badly in practice (Ross & Bagnell, 2010). Multi-modal experts, where several actions are equally good, also cause averaging artefacts with simple regression losses.

## Remedies

- **More and better data**: diverse demonstrations and corrective examples that show recovery from errors.
- **Richer models**: mixture densities, diffusion policies and action chunking, which model several plausible actions and keep trajectories coherent.
- **Interactive collection**: asking the expert to correct the learner, see [interactive imitation](../interactive-imitation/index.md).
- **Combining with reinforcement learning**: fine-tuning a cloned policy with rewards, see [reinforcement learning](../../reinforcement-learning/index.md).

## Connections

Behavioural cloning is supervised learning on demonstrations, so the usual [supervised learning](../../supervised/index.md) tools and pitfalls apply, including overfitting and distribution shift. The same idea trains the supervised fine-tuning stage of language models, see [imitation in foundation models](../../../../models/llm/imitation-in-foundation-models/index.md). Learning by watching others has a parallel in human observational learning, see [psychology and AI](../../../../brain-mind/psychology/index.md).

## Applications

Autonomous driving from human drivers, industrial robot arms taught by teleoperation, household manipulation from demonstration, and game agents trained on human play.

## Open questions

Covariate shift is only partly solved by better data and models. Learning from demonstrations that are noisy, sub-optimal or from different embodiments remains difficult, and safety guarantees for cloned policies are limited.

## References

### Seminal papers

- Pomerleau (1989), "ALVINN: an autonomous land vehicle in a neural network", NeurIPS 1988 proceedings. https://papers.nips.cc/paper/1988/hash/812b4ba287f5ee0bc9d43bbf5bbe87fb-Abstract.html — One of the first systems to learn driving by copying a human driver's steering.
- Ross & Bagnell (2010), "Efficient reductions for imitation learning", AISTATS. https://proceedings.mlr.press/v9/ross10a.html — Analyses how the errors of a cloned policy compound over the horizon.
- Ross, Gordon & Bagnell (2011), "A reduction of imitation learning and structured prediction to no-regret online learning", AISTATS, arXiv:1011.0686 — Shows how covariate shift makes behavioural cloning fail and introduces DAgger.
- Zhao, Kumar, Levine & Finn (2023), "Learning fine-grained bimanual manipulation with low-cost hardware", RSS, arXiv:2304.13705 — ACT, a transformer policy that predicts action chunks to model coherent multi-step behaviour.

### Surveys and textbooks

- Osa et al. (2018), "An algorithmic perspective on imitation learning", arXiv:1811.06711 — Survey of imitation learning algorithms, from behavioural cloning to inverse reinforcement learning.

### Lectures and videos

- Levine, CS 285 "Deep Reinforcement Learning", UC Berkeley, https://rail.eecs.berkeley.edu/deeprlcourse — Course site with lecture material on imitation learning and its failure modes.

### Articles and documentation

No further entries; the articles above are covered in the seminal papers group.

## Further reading

- Argall, Chernova, Veloso & Browning (2009), "A survey of robot learning from demonstration", *Robotics and Autonomous Systems*. No link checked.
