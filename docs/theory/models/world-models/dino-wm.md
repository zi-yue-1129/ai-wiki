---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
tags:
  - world models
  - self-supervised
  - planning
aliases:
  - DINO-WM
  - DINO 世界模型
---

# DINO-WM

DINO-WM is a latent world model that predicts how the patch features of a scene change under actions. The features come from a frozen DINOv2 encoder, and an action-conditioned transformer is trained on offline trajectories. Planning then searches over action sequences in that feature space. The authors call this zero-shot planning because the planner needs no task-specific reward or expert demonstrations at test time.

## Overview

Zhou, Pan, LeCun and Pinto (2025) ask whether a general, pre-trained visual representation can serve as the state space of a planning world model. Their stated goals are a model that can be trained on offline data, can be optimised at test time, and does not depend on learned reward models or inverse models. The evaluation covers six simulated environments (PointMaze, Wall, Reach, Push-T, Rope and Granular) plus several generalisation variants. The natural use is planning from images, where logged trajectories are available and a goal image specifies the task.

## Key concepts

- **Latent world model**: a predictor that maps the current state and an action to the next state in an embedding space, not in pixel space.
- **Patch features**: DINOv2 produces one feature vector per image patch. The paper's observations are tokenised as a 14×14 grid of 196 patch tokens per frame, each with a 384-dimensional feature.
- **Frozen encoder**: the DINOv2 weights are not updated during training or testing, so only the predictor is learned.
- **Action conditioning**: each action is embedded by a small MLP and the embedding is concatenated to every patch token.
- **Goal-matching cost**: a candidate plan is scored by how close its predicted final feature is to the feature of the goal image.

## How it works

1. Encode each frame with the frozen DINOv2 encoder into patch tokens.
2. Embed each action with an MLP and concatenate the embedding to every patch token of the frame.
3. Run a causal transformer predictor over a short history of frames, with a frame-level causal mask, to forecast the patch tokens of the next frame. The history length is 3 in some environments and 1 in others.
4. Train on offline trajectories with teacher forcing. For each training segment, the squared latent distance between each predicted frame and the encoded true frame is minimised.
5. At test time, run model predictive control (MPC) with the cross-entropy method (CEM). Sample action sequences, roll them out in feature space, keep the best ones, refit a Gaussian over actions, and repeat. Execute the first actions, then replan.

## Key methods

### DINO-WM (Zhou, Pan, LeCun & Pinto, 2025)

- **Problem:** Pixel-level world models spend capacity on appearance details that matter little for control, and learning a predictor from scratch for each robot is costly. The question is whether frozen, general-purpose visual features can serve as the planning state space.
- **Core idea:** Keep a self-supervised visual encoder fixed and learn only an action-conditioned predictor over its patch tokens. Plan by optimising actions so that the predicted final features match the goal image's features. The paper also trains a pixel decoder, but that decoder is trained separately and is not used for planning.
- **Equation or algorithm:** The training loss is the squared L2 distance in latent space between the predicted frame and the encoded next observation. It is applied to each predicted frame in the segment. In schematic form:

\[
\mathcal{L}_{\text{pred}} = \sum_{k} \big\lVert \hat z_{k+1} - z_{k+1} \big\rVert_2^2
\]

  Planning minimises the squared distance between the predicted final latent and the goal latent:

\[
C(a_{1:T}) = \big\lVert \hat z_T - z_g \big\rVert_2^2
\]

  The paper compares CEM with gradient descent through the model and reports that CEM performed better in its experiments. The predictor is trained with AdamW at a learning rate of 5e-5 for 100 epochs with batch size 32, as listed in its hyperparameter table.

- **Results:** The paper's Table 1 reports success rate (SR, higher is better) on Maze, Wall, Reach and Push-T, and Chamfer distance (CD, lower is better) on Rope and Granular.

| Model | Maze SR | Wall SR | Reach SR | Push-T SR | Rope CD | Granular CD |
|---|---|---|---|---|---|---|
| IRIS | 0.74 | 0.04 | 0.18 | 0.32 | 1.11 | 0.37 |
| DreamerV3 | 1.00 | 1.00 | 0.64 | 0.30 | 2.49 | 1.05 |
| TD-MPC2 | 0.00 | 0.00 | 0.00 | 0.00 | 2.52 | 1.21 |
| DINO-WM | 0.98 | 0.96 | 0.92 | 0.90 | 0.41 | 0.26 |

  DINO-WM scores highest on Reach, Push-T, Rope and Granular in this table. DreamerV3 is higher on Maze (1.00 against 0.98) and Wall (1.00 against 0.96), so the claim of a clear advantage holds only for some tasks. The success rates use 50 random start and goal pairs for Maze, Wall, Reach and Push-T, and 10 for Rope and Granular. The paper does not report random seeds or error bars.

- **Limitations:** The method needs offline data with good state-action coverage, which the paper says may be hard to obtain in complex environments. It needs ground-truth action labels, which limits its use with unlabelled internet video. Planning works in action space, and the authors suggest a hierarchical extension for fine control. Gradient descent planning does worse than CEM. The PushObj generalisation task stays hard. The Push-T training data are replays of released expert trajectories with added noise, so the "without expert demonstrations" claim applies to test time, not to the whole pipeline. The paper gives the input size as both 196×196 and 224×224, and the text does not name the DINOv2 variant, so exact reproduction needs the released code.

## Connections

[LAPO](lapo.md) learns the actions from video, while DINO-WM assumes the actions are known and studies the predictor's state space. [V-JEPA 2](v-jepa-2.md) takes the opposite route, starting from a video encoder and post-training on robot video. Both raise the question studied in [action controllability](action-controllability.md): whether the predictor actually depends on the action it is given. The frozen visual features come from the [self-supervised](../../paradigms/self-supervised/index.md) line of work. The wider family is described on the [parent overview](index.md).

## Open questions

- Whether a frozen appearance encoder can support contact-rich tasks, where small visual details decide success.
- How planning cost grows with the horizon and the action dimension. The paper's timing table compares different batch sizes, so it does not give a clean cost curve.
- How stable the success rates are across runs. With no seeds or error bars reported, the spread is unknown.

## References

### Seminal papers

- Zhou, G., Pan, H., LeCun, Y. & Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025, PMLR 267, pp. 79115–79135. https://proceedings.mlr.press/v267/zhou25t.html — Introduces the frozen-feature predictor and CEM planning described on this page. The arXiv version is https://arxiv.org/abs/2411.04983.
- Oquab, M. et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — Self-supervised visual encoder whose frozen patch tokens form DINO-WM's state space.
- Assran, M. et al. (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning*. arXiv:2506.09985. https://arxiv.org/abs/2506.09985 — Video-pretrained alternative that adds action conditioning through robot-video post-training.
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv:1803.10122. https://arxiv.org/abs/1803.10122 — Early latent world model that learns a compact dynamics model and uses it for control.

### Surveys and textbooks

- Moerland, T. M. et al. (2020). *Model-based Reinforcement Learning: A Survey*. arXiv:2006.16712. https://arxiv.org/abs/2006.16712 — Survey of learned dynamics models and their use in planning and control.
