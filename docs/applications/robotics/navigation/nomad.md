---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
tags:
  - robotics
  - navigation
  - diffusion policy
  - exploration
aliases:
  - NoMaD
  - Goal masked diffusion policy
  - 目標遮罩擴散策略
---

# NoMaD: Goal-Masked Diffusion Policies

NoMaD, introduced by Sridhar, Shah, Glossop and Levine (2023), is a navigation policy that uses a diffusion model over action sequences instead of a single regressed output. Its goal masking lets one network both reach a goal image and explore without one. The paper's central argument is that a unimodal regression is poorly suited to junctions, where several actions are equally good, and that a sampled distribution keeps those options open. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

NoMaD is a diffusion policy: it generates a sequence of future actions by denoising a random sample, conditioned on the current observation. During training, the goal image is sometimes masked out, so the same network is trained for goal-conditioned navigation and for unconditioned exploration. The model is compact, and the paper reports that it runs on a small embedded computer.

## Problem

A regression policy that outputs one action per observation averages over modes. At a junction, where the robot could turn left or right, the average can be a straight path into a wall. The paper asks whether a generative policy avoids this, and whether one model can do both goal-directed navigation and exploration.

## Core idea

Model the distribution of action sequences with a diffusion process, and condition it on the observation and, when present, the goal. Masking the goal during training teaches the model to explore when no goal is given, which avoids training a second network.

## How it works

1. Encode the current observation and, when available, the goal image.
2. Start from a random sample of an action sequence and denoise it, conditioned on the encoded inputs.
3. Execute the first few actions of the sampled sequence, and then sample again.
4. During training, mask the goal in a fraction of the examples so that the model learns unconditioned behaviour.

## Results

The paper reports goal-conditioned success rates comparable to ViNT, and it reports that the model explores with few collisions while being much smaller than the subgoal-diffusion baseline it compares against. The authors also report that the model runs in real time on a small embedded computer. The figures should be checked in the paper before reuse, since they depend on the environments used.

## Limitations

- Diffusion sampling takes several denoising steps, so the policy needs more computation per action than a single forward pass.
- The benefit over regression is clearest in multimodal situations such as junctions. In open corridors the advantage is smaller.
- The evaluation is on the robot platforms and environments used by the authors, so generalisation to other platforms is not shown.

## Connections

- [ViNT](vint.md) is the transformer regression policy whose goal-conditioned performance NoMaD is compared with.
- [GNM](gnm.md) is the shared-model predecessor on which the same group built its navigation work.
- [Hirose et al. (2019)](https://arxiv.org/abs/1903.02749) showed earlier that distilling a scored objective into a policy can outperform scoring at run time.

## Open questions

- Whether the diffusion policy's advantage over regression holds when the number of denoising steps is reduced for faster control.
- How the goal masking interacts with environments where exploration and goal reaching need different behaviour over long horizons.

## References

- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv:2310.07896. https://arxiv.org/abs/2310.07896 — the source of the masked diffusion policy and its navigation results.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — the regression baseline for goal-conditioned navigation.
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — the shared model and output-space comparison.
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep visual MPC-policy learning for navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. arXiv:1903.02749. https://arxiv.org/abs/1903.02749 — the distillation of a scored objective into a policy.
- Meng, X., Ratliff, N., Xiang, Y., & Fox, D. (2020). *Scaling local control to large-scale topological navigation*. ICRA 2020. arXiv:1909.12329. https://arxiv.org/abs/1909.12329 — a comparison of control outputs on topological maps.
