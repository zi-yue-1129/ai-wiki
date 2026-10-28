---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Reward modelling
  - reward model
  - 獎勵建模
---

# Reward modelling from human comparisons (Christiano et al., 2017)

A reward function is learned from pairwise human comparisons, so that a reinforcement learning policy can be optimised against human preferences instead of a hand-written reward.

## Problem

For many tasks, a reward function is hard to write down. A backflip in a simulated robot is one example. People can judge which of two behaviours is better more easily than they can assign it a number. Christiano et al. ask whether a reward predictor fitted to such comparisons can drive reinforcement learning as well as the true reward.

## Core idea

A reward model \(r_\theta\) scores each observation and action. The probability that a person prefers one segment \(\sigma_1\) over another \(\sigma_2\) is modelled as a logistic function of the difference in their summed predicted rewards, which follows the Bradley–Terry model. The reward network is fitted by maximising the likelihood of the human labels, so it learns a score under which preferred segments rank higher. Stiennon et al. (2020) apply the same idea to text: a reward model scores summaries, and a policy is tuned with PPO against it, with a penalty for drifting from the supervised model.

## Equation or algorithm

For two segments, the preference probability is a softmax over their summed predicted rewards (Christiano et al., Equation 1). The reward model is trained with cross-entropy against the human labels. The procedure:

1. Sample pairs of behaviours from the current policy.
2. Ask a person which of each pair is better.
3. Fit the reward model by minimising the cross-entropy loss against those labels.
4. Optimise the policy with reinforcement learning against the learned reward.
5. Keep sampling new pairs from the improved policy and repeat, so that human labels cover the behaviours the policy now produces.

In the text setting, the policy is also penalised for a KL divergence from the supervised model, which keeps it near outputs the reward model has seen (Stiennon et al., 2020).

## Results

- **Atari.** Christiano et al. use 5,500 comparisons across seven games. They report that their method has more difficulty than reinforcement learning with the true reward in these environments, although it matches or exceeds it on some.
- **MuJoCo.** With 700 labels the method nearly matches reinforcement learning on all eight tasks. With 1,400 labels it performs slightly better than when given the true reward.
- **Novel behaviours.** A simulated Hopper learns to backflip from 900 queries, in under an hour.
- **Summarisation.** Stiennon et al. collect 64,832 summary comparisons on the TL;DR dataset. Their 1.3B human-feedback model reaches a raw preference of 61% against the reference summaries, against 43% for a supervised model ten times its size.

## Limitations

- **Over-optimisation.** As the policy is optimised further against the reward model, true human preferences fall relative to the prediction, and the paper reports that the reward model eventually becomes anti-correlated with human preferences.
- **Label cost.** Each comparison requires a person, so the number of labels limits what can be learned.
- **Coverage.** The reward model is only accurate on behaviours that were compared, which is why new comparisons are gathered from the improved policy.

## Connections

- Parent topic: [Learning from Human Feedback](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- The policy step usually uses [Proximal Policy Optimisation](../../proximal-policy-optimisation/index.md).
- The language-model version is the second step of [InstructGPT](../../../../models/llm/instructgpt-rlhf/index.md).
- [Direct preference optimisation](../dpo/index.md) skips the explicit reward model and fits the policy to the same comparisons.

## Applications

- **Robot and simulated control.** Learning behaviours such as backflips and locomotion from comparisons, as in the MuJoCo experiments.
- **Language model alignment.** Training summarisation and instruction-following models from human preference labels (Stiennon et al., 2020; Ouyang et al., 2022).

## Open questions

- How to detect and prevent over-optimisation of a learned reward.
- How to reduce the number of human comparisons needed.
- How well a reward model generalises beyond the behaviours it was trained on.

## References

### Seminal papers

- Christiano et al. (2017), "Deep reinforcement learning from human preferences", arXiv:1706.03741 — Learns a reward predictor from human comparisons and trains reinforcement learning on it, with the Atari and MuJoCo results above.
- Stiennon et al. (2020), "Learning to summarize from human feedback", NeurIPS 2020, arXiv:2009.01325 — Applies reward modelling and PPO to summarisation, and reports the over-optimisation result.
- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", arXiv:2203.02155 — InstructGPT, which uses a reward model trained on labeller rankings.
- Bradley & Terry (1952), "Rank analysis of incomplete block designs: I. The method of paired comparisons", *Biometrika* 39(3/4), 324. https://doi.org/10.2307/2334029 — The paired-comparison model behind the preference probability.
- Schulman et al. (2017), "Proximal policy optimization algorithms", arXiv:1707.06347 — The policy-optimisation step used against the learned reward.
