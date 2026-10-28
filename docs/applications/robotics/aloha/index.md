---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation
  - theory/models/transformer
aliases:
  - ALOHA
  - Action Chunking with Transformers
  - ACT
  - 低成本雙臂操作
---

# ALOHA and ACT (Zhao et al. 2023)

Zhao and colleagues asked whether inexpensive, imprecise robot hardware can learn delicate two-handed tasks from a small number of real demonstrations. They built a low-cost bimanual system, called ALOHA, and a learning method, Action Chunking with Transformers (ACT). This page covers that paper; the parent topic is [Robotics](../index.md).

## Problem

Fine bimanual manipulation, such as opening a container or inserting a battery, is hard to learn by imitation. Errors compound over many steps, and human demonstrations are inconsistent. Precise robot hardware is expensive, which limits who can collect demonstrations.

## Core idea

ALOHA pairs low-cost arms with a remote-control setup, so a person can demonstrate a task directly. ACT predicts a chunk of future actions at once rather than one action per step, which reduces the effect of compounding errors. The policy models these action sequences with a transformer-based generative model.

## Procedure

1. Collect demonstrations with the teleoperation setup: 50 per task, and 100 for one task. The paper estimates about 10–20 minutes of data per task.
2. Train ACT to predict the chunk of actions that follows each observation.
3. At run time, execute the predicted chunk, then predict the next chunk from the latest observation.

## Results

The paper evaluates six real-world bimanual tasks, with one seed and 25 trials per task. ACT's final success rates range from 20% (threading Velcro) to 96% (inserting a battery), and the abstract highlights 80–90% on some tasks. The per-task figures are in the paper's Tables I and II.

## Limitations

- The results come from the authors' hardware and a small set of tasks.
- A chunk commits the robot to several steps at once, so a chunk planned from an outdated view can be wrong. How often this matters is a question for the full paper.
- Each new task still needs a person to demonstrate it.

## Connections

- The imitation-learning setting is covered in [Imitation Learning](../../../theory/paradigms/imitation/index.md).
- A diffusion-based policy for similar tasks is described in [Diffusion Policy](../diffusion-policy/index.md).
- The transformer architecture is covered in [Transformer](../../../theory/models/transformer/index.md).

## References

### Seminal papers

- Zhao, T. Z. et al. (2023). Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. arXiv. https://arxiv.org/abs/2304.13705 — Introduces the ALOHA hardware and the ACT policy, which predicts chunks of actions.
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — A transformer policy trained on large real-robot datasets, studying how generalisation changes with data and model size.
- Chi, C. et al. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. arXiv. https://arxiv.org/abs/2303.04137 — Generates robot actions with a conditional denoising diffusion model, an alternative to ACT for the same kind of task.

### Surveys and textbooks

- Hussein, A. et al. (2017). Imitation Learning: A Survey of Learning Methods. *ACM Computing Surveys* 50(2). https://doi.org/10.1145/3054912 — Survey of imitation learning methods, covering the setting that ACT uses.
- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — Survey of reinforcement learning for robots, the main alternative to demonstrations.
