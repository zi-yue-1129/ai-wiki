---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/model-based-rl
  - brain-mind/computational-neuroscience
tags:
  - world models
  - reinforcement learning
  - model-based
aliases:
  - Dreamer
  - 夢想家
  - 想像式強化學習
---

# Dreamer

Dreamer is a family of reinforcement-learning agents from Danijar Hafner and colleagues. Each agent learns a latent world model from its own experience, then learns its behaviour by imagining trajectories inside that model. One stretch of real experience can therefore support many learning updates. The family has three published versions, DreamerV1, V2 and V3. They keep the same core loop and change the form of the latent state and the training recipe.

## Overview

A Dreamer agent has three learned parts. A world model encodes observations into a compact latent state, predicts how that state changes given actions, and predicts rewards from it. An actor chooses actions, and a critic (value model) estimates the value of latent states. The actor and critic are trained on imagined latent trajectories produced by the world model. This is the latent-imagination form of [model-based reinforcement learning](../../paradigms/reinforcement-learning/model-based-rl/index.md).

## Key concepts

- **Latent state**: a compressed representation of the observation that the model predicts forward. In DreamerV1 it is a diagonal Gaussian; in DreamerV2 and V3 it is built from discrete variables.
- **Imagined rollout**: a sequence of latent states and predicted rewards produced by the model without touching the environment.
- **Actor-critic on imagination**: the policy is improved by gradients of predicted values, computed through the imagined sequence using a λ-weighted value target.

## How it works

1. Store real experience in a replay buffer.
2. Train the world model to reconstruct observations and predict rewards from latent states, so that the latent state keeps what matters for control. In DreamerV1 this is a variational objective (see below).
3. From sampled real states, roll the actor forward inside the latent model for a fixed horizon \(H\).
4. Train the critic on imagined λ-returns, and train the actor to maximise predicted values, backpropagating through the imagined sequence.

For DreamerV1, the λ-weighted value target over imagined states, with discount \(\gamma\) and mixing weight \(\lambda\), is

\[
V_\lambda(s_\tau) \doteq (1-\lambda)\sum_{n=1}^{H-1}\lambda^{n-1}V^{n}_{N}(s_\tau) + \lambda^{H-1}V^{H}_{N}(s_\tau)
\]

where \(V^{k}_{N}\) is the \(k\)-step estimate that sums imagined rewards and bootstraps from the learned value function. The actor maximises the sum of these values along the imagined trajectory,

\[
\max_{\phi}\ \mathbb{E}\Big[\sum_{\tau=t}^{t+H} V_\lambda(s_\tau)\Big]
\]

and the world model maximises a variational lower bound made of observation, reward and KL terms,

\[
J_{\text{REC}} = \mathbb{E}_p\Big[\sum_t \big(\ln q(o_t\mid s_t) + \ln q(r_t\mid s_t) - \beta\,\mathrm{KL}[\,p(s_t\mid s_{t-1},a_{t-1},o_t)\,\|\,q(s_t\mid s_{t-1},a_{t-1})\,]\big)\Big] + \text{const}
\]

## Key methods

### DreamerV1 (Hafner et al., 2020)

- **Problem:** PlaNet, the latent-dynamics agent it builds on, plans with its model at each decision. The paper asks whether a policy can instead be learned by gradients through imagined latent trajectories.
- **Core idea:** Learn an action model and a value model, and train the action model by backpropagating the predicted λ-values through imagined latent trajectories. The latent model uses Gaussian latent variables with a recurrent state-space structure.
- **Equation or algorithm:** the \(V_\lambda\) target, the actor objective and the world-model bound given in How it works. The main setting uses \(H = 15\), \(\gamma = 0.99\) and \(\lambda = 0.95\).
- **Results:** On 20 visual tasks of the DeepMind Control Suite, with 64×64×3 image observations, the paper reports an average score of 823 for Dreamer after 5 × 10⁶ environment steps. PlaNet reaches 332 at the same budget. The model-free D4PG reaches 786, but after 10⁸ steps (Appendix G table).
- **Limitations:** The main experiments cover one benchmark family and use action repeat 2. Discrete-action experiments (Atari and DeepMind Lab) are in an appendix. Imagined returns are only as good as the learned model over the horizon, and the paper sweeps the horizon (Figure 4) rather than deriving it.

### DreamerV2 (Hafner et al., 2021)

- **Problem:** Can an agent that learns its behaviour inside a world model match the best model-free agents on the Atari benchmark of 55 games?
- **Core idea:** Replace the Gaussian latent of V1 with discrete categorical latents. Use KL balancing, which weights the prior and posterior parts of the KL term differently. The actor-critic on imagined trajectories is kept.
- **Equation or algorithm:** the latent state is 32 categorical variables with 32 classes each, which gives 32 active bits in a binary vector of length 1024. The KL weight is \(\alpha = 0.8\) for the prior and \(1-\alpha\) for the posterior, and the overall KL scale is \(\beta = 0.1\) for Atari. Imagination uses \(H = 15\) and \(\lambda = 0.95\). Training runs for 200M environment steps with action repeat 4.
- **Results:** In Table 1 (Atari, 200M steps), DreamerV2 has a gamer-normalised median of 2.15 and a gamer-normalised mean of 11.33. The same table lists IQN with a median of 1.29, Rainbow with 1.47, C51 with 1.09 and DQN with 0.65. DreamerV2 is highest in each column of that table. The abstract claims that it is the first agent to reach human-level performance on the 55-task Atari benchmark. It also reports learning stand-up and walking for a humanoid from pixels.
- **Limitations:** The results use 200M steps, far beyond a data-efficient regime, and the paper reports no Atari 100k result. The headline claim depends on the choice of normalisation, and the paper's text gives different discount values in different sections (0.999 in the text and 0.995 in Table D.1). Check the appendix before reusing its settings.

### DreamerV3 (Hafner et al., 2023; Nature 2025)

- **Problem:** A single algorithm with one fixed hyperparameter configuration that works across many domains, without per-task tuning.
- **Core idea:** Use normalisation and robustness techniques so that the same settings work when signal scales differ. These include a symlog transform for values of very different size, KL balancing with free bits, and return normalisation based on a range of returns.
- **Equation or algorithm:** the symlog transform is \(\operatorname{symlog}(x) = \operatorname{sign}(x)\ln(|x|+1)\), with inverse \(\operatorname{symexp}(x) = \operatorname{sign}(x)(\exp(|x|)-1)\). The paper sets the world-model loss weights to \(\beta_{\text{pred}} = 1\), \(\beta_{\text{dyn}} = 1\) and \(\beta_{\text{rep}} = 0.1\), and clips the dynamics and representation losses below 1 nat (about 1.44 bits). The return range is computed from the 5th to the 95th percentile of the return batch. The paper defines six nominal model sizes, from 12M to 400M parameters.
- **Results:** The abstract reports that the algorithm outperforms specialised methods across more than 150 diverse tasks with a single configuration. The paper evaluates 8 domains under fixed hyperparameters. The abstract also states that Dreamer is the first algorithm to collect diamonds in Minecraft from scratch, without human data or curricula. The Minecraft runs use a budget of 100M environment steps.
- **Limitations:** The generality claim is measured on the suites the authors chose. A single configuration does not mean it is the best setting for each task. The Minecraft result is reported at one step budget, and the abstract does not name the benchmarks.

## Connections

Dreamer sits in the same family as the other [world models](index.md) on this site. Its latent prediction is a form of learned forward modelling. Its lineage runs from PlaNet (Hafner et al., 2019), whose recurrent latent model DreamerV1 builds on, and from the earlier idea of Ha and Schmidhuber (2018) of training a controller inside a learned model. Whether its imagination mechanism corresponds to processes in the brain is an open hypothesis, not something the Dreamer papers establish. The neuroscience-side discussion of planning and simulation is on the [computational neuroscience](../../../brain-mind/computational-neuroscience/index.md) page.

The video branch of world models, which generates pixels a user can play with, is covered by [Genie](genie.md). Dreamer's latent models instead predict compact states for control.

## Applications

Dreamer-style agents have been used for continuous control from pixels (DreamerV1 on the DeepMind Control Suite), for Atari and humanoid control (DreamerV2), and for a broad range of domains with one configuration, including Minecraft (DreamerV3). The DreamerV3 paper reports results across domains, which is the main evidence for its generality.

## Open questions

- How far the model's errors can grow across a long imagined horizon before the actor learns from misleading values.
- Whether one configuration works equally well for tasks that differ much from those in the benchmark suites.
- How the latent model should handle actions that do not change the observation, which is the controllability problem covered in [Action controllability](action-controllability.md).

## References

### Seminal papers

- Hafner, D., Lillicrap, T., Ba, J. & Norouzi, M. (2020). *Dream to Control: Learning Behaviors by Latent Imagination*. ICLR 2020. https://arxiv.org/abs/1912.01603 — Introduces Dreamer, which learns behaviour by backpropagating through imagined latent trajectories.
- Hafner, D., Lillicrap, T., Norouzi, M. & Ba, J. (2021). *Mastering Atari with Discrete World Models*. ICLR 2021. https://arxiv.org/abs/2010.02193 — DreamerV2, with discrete latent states and results on the 55-game Atari benchmark.
- Hafner, D., Pasukonis, J., Ba, J. & Lillicrap, T. (2025). *Mastering diverse control tasks through world models*. Nature 640. https://doi.org/10.1038/s41586-025-08744-2 — Journal version of DreamerV3, with one configuration for more than 150 tasks. The arXiv preprint, *Mastering Diverse Domains through World Models*, is at https://arxiv.org/abs/2301.04104.
- Hafner, D., Lillicrap, T., Fischer, I., Villegas, R., Ha, D., Lee, H. & Davidson, J. (2019). *Learning Latent Dynamics for Planning from Pixels*. ICML 2019. https://proceedings.mlr.press/v97/hafner19a.html — PlaNet, the latent-dynamics planning agent that DreamerV1 compares against and builds on.
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv preprint. https://arxiv.org/abs/1803.10122 — Early latent world model in which a controller is trained inside the model's own simulated rollouts, a precursor to Dreamer.

### Surveys and textbooks

- Moerland, T. M., Broekens, J., Plaat, A. & Jonker, C. M. (2020). *Model-based Reinforcement Learning: A Survey*. arXiv preprint. https://arxiv.org/abs/2006.16712 — Survey of model-based reinforcement learning, covering learned dynamics models and how they are used for planning and policy learning.

## Further learning

- Hafner, D., *Dreamer* project page. https://danijar.com/project/dreamer/ — The author's project page for the Dreamer line of work.
