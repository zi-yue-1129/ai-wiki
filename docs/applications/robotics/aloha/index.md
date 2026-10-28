---
status: complete
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

ALOHA pairs two low-cost follower arms with two leader arms that a person backdrives, so the person demonstrates a task directly through joint-space teleoperation (Sec. III). The whole system is built for under a 20k USD budget (Sec. III).

ACT predicts a chunk of future actions at once rather than one action per step, which reduces the effect of compounding errors. It is trained as a conditional variational autoencoder, and its transformer policy generates a chunk of 100 target joint positions per inference (Sec. IV).

## Procedure

1. **Demonstrations:** collect 50 demonstrations per real-world task, and 100 for Thread Velcro. Each simulated task has 50 scripted and 50 human demonstrations (Sec. V-B).
2. **Training:** train ACT from scratch for each task, with a CVAE objective weighted by β = 10. The CVAE encoder is used only in training, and the latent variable is set to zero at test time (Sec. IV-B, Table III).
3. **Inference with temporal ensembling:** query the policy at every timestep, then average the overlapping predictions for the current step with weights exp(−m·i), where i = 0 is the oldest prediction. A smaller m gives new observations more weight (Sec. IV-A, Alg. 2).

Each camera image passes through a ResNet-18 backbone, and the resulting features are flattened into tokens for a transformer. The model has about 80M parameters, trains in about 5 hours on one 11 GB GPU, and runs inference in about 0.01 s (Sec. IV-C).

## Results

The paper evaluates six real-world bimanual tasks, with one seed and 25 trials per task. Final-stage success rates for ACT are 88% on Slide Ziploc, 96% on Slot Battery, 84% on Open Cup, 20% on Thread Velcro, 64% on Prep Tape and 92% on Put On Shoe (Tables I–II). Every baseline reaches 0% at the final stage on Slide Ziploc and Slot Battery. On the other four tasks, the best baseline, BeT, also reaches 0%. Baselines do reach nonzero success on early subtasks, such as 28% grasp success for VINN on Slide Ziploc.

In simulation (Table I, 3 seeds and 50 trials), ACT reaches 86% on the scripted Cube Transfer and 50% on human demonstrations. On Bimanual Insertion it reaches 32% on scripted and 20% on human demonstrations. BeT, RT-1, VINN and BC-ConvMLP reach at most 27% on the scripted Cube Transfer, and 3% or less on the other human and insertion results.

The ablations (Fig. 8) show the following:

- **Chunk size:** success rises from 1% at k = 1 to 44% at k = 100, then tapers, with a small dip at k = 200 and k = 400. Adding chunking to BC-ConvMLP and VINN also improved them.
- **Temporal ensembling:** it adds 4% for BC-ConvMLP and 3.3% for ACT. VINN drops by 20%.
- **CVAE:** removing it makes almost no difference on scripted data. On human data, performance falls from 35.3% to 2%.
- **Control frequency:** in a six-person user study, lowering control from 50 Hz to 5 Hz increased teleoperation time by 62% (p < 0.001) (Sec. VI-C).

## Limitations

- **Hardware:** ALOHA struggles with tasks that need several fingers from both hands, and with high forces, because the low-cost motors lack torque. Tasks that depend on fingernails, such as lifting packing tape edges, are also difficult (App. F).
- **Policy:** ACT failed to learn unwrapping candies (0 of 10 unwraps in one protocol). Opening a flat ziploc bag was also difficult, because the policy picks it up but struggles with mid-air steps (App. F). Thread Velcro reaches only 20% (Sec. V-C).
- **Scope:** the conclusion notes that tasks such as buttoning a dress shirt are beyond the current system (Sec. VII). The authors suggest pretraining, more data and better perception as future directions (App. F).
- **Not called out by the authors:** the paper does not list force feedback, generalisation or single-task training as limitations. It does state that ACT is trained from scratch for each task and relies on 50 demonstrations per task (Sec. IV-C, Sec. V-B).

## Connections

- The imitation-learning setting is covered in [Imitation Learning](../../../theory/paradigms/imitation/index.md).
- A diffusion-based policy for similar tasks is described in [Diffusion Policy](../diffusion-policy/index.md).
- The transformer architecture is covered in [Transformer](../../../theory/models/transformer/index.md).

## References

### Seminal papers

- Zhao, T. Z. et al. (2023). Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. arXiv. https://arxiv.org/abs/2304.13705 — Introduces the ALOHA hardware and the ACT policy, which predicts chunks of actions.
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — A transformer policy trained on a large real-robot dataset for real-world control.
- Chi, C. et al. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. arXiv. https://arxiv.org/abs/2303.04137 — Generates robot actions with a conditional denoising diffusion model, an alternative to ACT for the same kind of task.

### Surveys and textbooks

- Hussein, A. et al. (2017). Imitation Learning: A Survey of Learning Methods. *ACM Computing Surveys* 50(2). https://doi.org/10.1145/3054912 — Survey of imitation learning methods, covering the setting that ACT uses.
- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — Survey of reinforcement learning applied to robots.
