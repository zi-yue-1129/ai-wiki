---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
aliases:
  - Diffusion Policy
  - 擴散策略
---

# Diffusion Policy (Chi et al. 2023)

Chi and colleagues proposed generating robot behaviour with a denoising diffusion model. Instead of predicting one action from an observation, the policy turns noise into a sequence of actions, guided by what the robot sees. This page covers that paper; the parent topic is [Robotics](../index.md).

## Problem

Imitation policies often struggle when many different actions are correct in the same situation. A standard regression model averages those choices, and the average may be a poor action. Robot action spaces are also high-dimensional, which makes this worse.

## Core idea

The paper models the visuomotor policy as a conditional denoising diffusion process. Starting from random noise, the model repeatedly removes noise, and each step is conditioned on the current observations. The result is an action sequence that stays close to one of the demonstrated modes rather than their average. The authors argue that diffusion handles multimodal actions and high-dimensional spaces well, and that it trains stably.

## Procedure

1. Collect demonstrations of the task, pairing each observation with the actions taken.
2. Train a network to predict the noise added to demonstrated action sequences, conditioned on observations. The underlying method is the [denoising diffusion model](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/index.md).
3. At run time, sample an action sequence from noise by running the denoising steps, then execute part of it. The paper describes receding-horizon control: the policy executes part of each predicted sequence before it predicts again.

## Results

The paper reports an average improvement of 46.9% over prior state-of-the-art methods. The abstract describes 15 tasks from four manipulation benchmarks, and the main comparison table lists 12 of them (8 simulated and 4 real-world). Real-robot experiments are also reported. The per-task figures need the full paper.

## Limitations

- Generating an action sequence takes several denoising steps, which costs inference time compared with a single forward pass.
- The reported gains are measured on the authors' benchmarks and robot setups.
- The paper's comparisons are against the methods of its time, which have since changed.

## Connections

- The imitation-learning setting is covered in [Imitation Learning](../../../theory/paradigms/imitation/index.md).
- The method it builds on is [diffusion models](../../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/index.md).
- A transformer-based policy for similar tasks is [ALOHA and ACT](../aloha/index.md).

## References

### Seminal papers

- Chi, C. et al. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. arXiv. https://arxiv.org/abs/2303.04137 — Models a visuomotor policy as conditional denoising diffusion, with results across 15 manipulation tasks from four benchmarks.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — The diffusion model that the policy's training and sampling procedure builds on.
- Zhao, T. Z. et al. (2023). Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. arXiv. https://arxiv.org/abs/2304.13705 — The ACT policy, a competing approach for the same kind of task.

### Surveys and textbooks

- Hussein, A. et al. (2017). Imitation Learning: A Survey of Learning Methods. *ACM Computing Surveys* 50(2). https://doi.org/10.1145/3054912 — Survey of imitation learning methods.
- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — Survey of reinforcement learning for robots.
