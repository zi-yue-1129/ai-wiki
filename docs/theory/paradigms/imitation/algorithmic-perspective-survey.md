---
related:
  - theory/paradigms/imitation
  - theory/paradigms/reinforcement-learning
  - applications/robotics
tags:
  - imitation learning
  - behavioural cloning
  - inverse reinforcement learning
  - survey
aliases:
  - An Algorithmic Perspective on Imitation Learning
  - Osa et al. survey
  - 模仿學習的演算法觀點
last_reviewed: 2026-11-01
---

# An Algorithmic Perspective on Imitation Learning

Osa et al. (2018) is a monograph that surveys imitation learning from an algorithmic point of view. It is written for machine learning researchers and roboticists alike, and it organises the field around two families: behavioural cloning, which learns a direct mapping from observations to actions, and inverse reinforcement learning, which recovers the reward the expert seems to be optimising. The survey is a useful map of the field, and the family-level comparison is on the [Imitation Learning](index.md) page.

## Overview

Imitation learning builds a policy from demonstrations rather than from a reward signal. The monograph treats the field as a set of design choices. These include what the demonstrations look like, whether the learner can observe what the expert observed, how the policy is represented, and how it is trained. Each choice changes which algorithm is appropriate, so the survey organises the methods around those choices.

## Scope and structure

The monograph has five chapters.

- **Chapter 2, design choices:** observability, policy abstraction, behaviour descriptors and an information-theoretic analysis.
- **Chapter 3, behavioural cloning:** supervised learning of actions or trajectories from demonstrations. It covers action-state models with neural networks, including recurrent networks, teacher-student interaction, trajectory learning with movement primitives, task-level planning and model-based approaches.
- **Chapter 4, inverse reinforcement learning:** model-based methods such as maximum-margin planning and maximum-entropy IRL, and model-free methods such as relative-entropy IRL and generative adversarial imitation learning (GAIL).
- **Chapter 5, challenges:** the relation between behavioural cloning and IRL, and open questions about data, design choices, algorithms and evaluation.

Interactive methods such as DAgger are placed in Chapter 3 under teacher-student interaction. GAIL is treated in Section 4.5.2 rather than in a separate adversarial chapter.

## Core problem

The monograph explains the central difficulty of behavioural cloning as distribution shift. The learner often reaches states that the expert never visited, so small early mistakes can lead to poor behaviour later. Interactive methods are presented as a response, because they let the learner's own states be labelled. The survey also notes that maximum-likelihood cloning may not work well in many applications, and it writes the matching of the learner's trajectory distribution to the expert's as a KL-divergence objective (Section 2.7.2).

## Open challenges

The monograph lists several difficulties that remain open.

- **Projection.** The authors state that no existing imitation method performs the I-projection exactly, and they call I-projection-based methods an interesting research direction.
- **Model learning.** Learning the dynamics is hard for some tasks, for example contact between deformable objects.
- **Mismatch between expert and learner.** Demonstrations can be suboptimal for a learner that observes different information or has a different body.
- **Hierarchy.** Learning high-level and low-level policies together is described as not trivial.
- **Cost of data.** Demonstrations and rollouts are expensive, and recent methods often need large datasets.

## Connections

- The interactive method is [DAgger](interactive-imitation/index.md), which addresses the distribution shift that the survey describes.
- The inverse reinforcement learning chapter is the family covered in [inverse reinforcement learning](inverse-reinforcement-learning/index.md).
- The reinforcement learning methods that imitation can replace or support are on the [Reinforcement Learning](../reinforcement-learning/index.md) page.

## Open issues

- How much of the distribution-shift problem can be solved without an interactive expert?
- Can the reward recovered by inverse reinforcement learning transfer to new embodiments?
- What evaluation protocol shows that an imitation policy generalises rather than reproduces the demonstrations?

## References

### Seminal papers

- Osa, T., Pajarinen, J., Neumann, G., Bagnell, J. A., Abbeel, P. & Peters, J. (2018). An Algorithmic Perspective on Imitation Learning. Foundations and Trends in Robotics, 7(1–2), 1–179. [DOI 10.1561/2300000053](https://doi.org/10.1561/2300000053) — The monograph this page summarises, covering behavioural cloning, inverse reinforcement learning and open challenges.
- Ross, S., Gordon, G. J. & Bagnell, J. A. (2010). A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — Introduces DAgger, the interactive method for the distribution-shift problem.
- Ho, J. & Ermon, S. (2016). Generative Adversarial Imitation Learning. [arXiv:1606.03476](https://arxiv.org/abs/1606.03476) — GAIL, the adversarial method treated in Section 4.5.2 of the survey.
- Argall, B. D. et al. (2009). A survey of robot learning from demonstration. Robotics and Autonomous Systems, 57, 469–483. [DOI 10.1016/j.robot.2008.10.024](https://doi.org/10.1016/j.robot.2008.10.024) — An earlier survey of learning from demonstration in robotics, covering the same problem from a robotics viewpoint.

### Surveys and textbooks

- Goodfellow, I. J. et al. (2014). Generative Adversarial Networks. [arXiv:1406.2661](https://arxiv.org/abs/1406.2661) — The adversarial training framework that GAIL adapts to imitation.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
