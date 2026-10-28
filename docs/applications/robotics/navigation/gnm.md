---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
tags:
  - robotics
  - navigation
  - foundation model
aliases:
  - GNM
  - General Navigation Model
  - 通用導航模型
---

# GNM: General Navigation Model

GNM, introduced by Shah, Sridhar, Bhorkar, Hirose and Levine (2023), is a single navigation model trained on data from several different robots. It takes the current image and an image goal, and it outputs a short sequence of normalised waypoints. The paper's main comparison is about the output space: waypoints that are normalised to the robot's scale succeeded where velocity outputs and raw waypoints did not. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

GNM is trained by imitation on driving data gathered by several robots and then fine-tuned to a new robot with a small amount of its data. The network also predicts how many steps separate the current image from the goal, so the same model supports image-goal navigation and exploration. Its output is a short sequence of future positions, which a low-level controller follows.

## Problem

Navigation policies are usually trained for one robot, and they fail when the platform changes. The paper asks whether one model can work across robots with different cameras and dynamics, and which representation of the action is most useful for goal-directed driving.

## Core idea

Use a shared visual encoder with a head for each robot, and predict normalised waypoints rather than velocities. The normalisation makes the outputs comparable across robots of different sizes and speeds. Temporal context, meaning several past frames, helps the model handle manoeuvres that need more information than the current view.

## How it works

1. Gather driving data from several robots, each with its own camera and dynamics, and label it with the relative positions reached later.
2. Train one visual encoder on all of the data, together with a head for each robot embodiment.
3. Predict a sequence of normalised waypoints from the current image, a goal image and the past frames.
4. Fine-tune on a new robot with a small amount of its data, and follow the predicted waypoints with a controller.

## Results

The paper reports an ablation over the output space on ten environments, comparing velocities, raw waypoints and normalised waypoints. The authors report that normalised waypoints gave the highest success, and that velocity policies struggle in environments that need sharp turns. They also report that adding several past frames improves success in hard environments. The figures should be checked in the paper before reuse.

## Limitations

- Most of the data is from wheeled ground robots, so claims for aerial or legged robots are outside the evaluated range.
- The model is trained by imitation, and it inherits the limitations of behaviour cloning, including sensitivity to the distribution of the training data.
- The normalisation depends on a reference scale for each robot, which must be set for every new platform.

## Connections

- [ViNG](ving.md) is the earlier method, whose output head regresses relative pose on a single robot.
- [ViNT](vint.md) scales the same idea to a larger transformer and a larger dataset.
- [NoMaD](nomad.md) changes the output to a diffusion model over actions.

## Open questions

- Whether the normalised waypoint representation holds up for robots whose control interface is not a planar velocity.
- How much robot-specific data is needed to adapt the shared model to a new platform reliably.

## References

- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — the source of the shared model and the output-space comparison.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — a larger transformer successor.
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — the single-robot predecessor.
- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv:2310.07896. https://arxiv.org/abs/2310.07896 — a diffusion-based successor for goal-conditioned navigation and exploration.
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep visual MPC-policy learning for navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. arXiv:1903.02749. https://arxiv.org/abs/1903.02749 — an earlier learned navigation policy trained toward image subgoals.
