---
related:
- theory/paradigms/imitation/inverse-reinforcement-learning/index.md
- theory/paradigms/reinforcement-learning/index.md
tags:
  - imitation learning
  - generative adversarial imitation
  - GAIL
---

# Adversarial Imitation Learning

Adversarial imitation learning trains a policy so that its trajectories cannot be told apart from the expert's. A discriminator is trained to separate expert trajectories from the learner's, and the learner is rewarded for fooling it. The approach borrows the training scheme of [generative adversarial networks](https://arxiv.org/abs/1406.2661) and avoids hand-designing a reward, while still using the environment during training.

## Overview

The learner alternates two updates. The discriminator is updated to score expert state–action pairs high and learner pairs low. The policy is then updated with reinforcement learning, using the discriminator's output as a reward. Because the reward is learned from the discriminator, this is a form of implicit [inverse reinforcement learning](../inverse-reinforcement-learning/index.md) with no explicit inner IRL loop.

## Generative adversarial imitation learning

GAIL (Ho & Ermon, 2016) shows that matching the occupancy measure of the expert, which is the distribution of state–action pairs it visits, can be cast as a saddle-point problem. The learner is then trained with a policy-gradient method such as TRPO. GAIL is sample-efficient compared with explicit IRL and does not require a known reward or environment model.

## Adversarial inverse reinforcement learning

AIRL (Fu, Luo & Levine, 2018) structures the discriminator so that it recovers a reward that depends mainly on the state rather than on the environment's dynamics. The learned reward can then be reused when the dynamics change, which makes it more useful as a transferable reward than the discriminator used in GAIL.

## Practical issues

Adversarial training is unstable. The discriminator can become too strong, which removes useful learning signal, or too weak, which gives no signal at all. Regularisation, gradient penalties and careful choice of the policy optimiser are typical remedies. The method also needs online environment interaction, which is expensive on physical robots.

## Connections

Adversarial imitation combines ideas from [generative adversarial networks](https://arxiv.org/abs/1406.2661), [reinforcement learning](../../reinforcement-learning/index.md) and [inverse reinforcement learning](../inverse-reinforcement-learning/index.md). It differs from [behavioural cloning](../behavioural-cloning/index.md) in that it matches the distribution of whole trajectories rather than single actions, which removes the need for explicit correction of compounding errors.

## Applications

Locomotion and manipulation control in simulation, imitation of motion-capture data for animated characters, and learning control policies from a small number of demonstrations.

## Open questions

Training stability and sample efficiency on real hardware are still limiting. Discriminators can exploit superficial differences between expert and learner data, and it is not clear when the learned rewards generalise to new tasks.

## References

### Seminal papers

- Ho & Ermon (2016), "Generative adversarial imitation learning", NeurIPS, [arXiv:1606.03476](https://arxiv.org/abs/1606.03476) — Introduces GAIL, which matches the expert's state–action distribution with a discriminator and policy-gradient RL.
- Fu, Luo & Levine (2018), "Learning robust rewards with adversarial inverse reinforcement learning", ICLR, [arXiv:1710.11248](https://arxiv.org/abs/1710.11248) — AIRL, which recovers state-dependent rewards that transfer across changed dynamics.
- Finn, Levine & Abbeel (2016), "Guided cost learning: deep inverse optimal control via policy optimization", ICML, [arXiv:1603.00448](https://arxiv.org/abs/1603.00448) — Connects inverse optimal control with a generative-adversarial view of learning costs from samples.
- Goodfellow, Pouget-Abadie, Mirza, Xu, Warde-Farley, Ozair, Courville & Bengio (2014), "Generative adversarial networks", NeurIPS, [arXiv:1406.2661](https://arxiv.org/abs/1406.2661) — The adversarial training framework that these imitation methods build on.

### Surveys and textbooks

- Osa et al. (2018), "An algorithmic perspective on imitation learning", [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — Survey that places adversarial imitation among other learning-from-demonstration methods.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Kostrikov, Agrawal, Dwibedi, Levine & Tompson (2019), "Imitation learning via off-policy distribution matching", [arXiv:1912.05032](https://arxiv.org/abs/1912.05032) — Off-policy variant that avoids much of the online interaction needed by GAIL.
