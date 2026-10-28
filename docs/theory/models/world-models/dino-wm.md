---
status: draft
last_reviewed: 2026-10-28
tags:
  - world models
  - self-supervised
  - planning
aliases:
  - DINO-WM
  - DINO 世界模型
---

# DINO-WM

DINO-WM is a latent world model that predicts future visual features rather than pixels. The features come from a frozen, pre-trained DINOv2 encoder, and an action-conditioned transformer predicts how those features change. The authors use the predictor to plan with no task-specific training, which they describe as zero-shot planning.

## Problem

Pixel-level world models spend capacity on details that do not matter for control, such as textures and lighting. Learning a predictor from scratch on a robot's own data is also expensive. DINO-WM asks whether a general visual representation, trained without actions, can serve as the state space for a world model that plans.

## Core idea

The observation model stays fixed. The authors state that "the observation model remains frozen during training and testing". The predictor is a transformer based on the ViT design. Each action goes through a small MLP, and the resulting vector is concatenated to every patch vector of the frame. Training uses offline trajectories: given the patch features of past frames and the actions taken, the predictor forecasts the patch features of future frames. Planning then searches over action sequences whose predicted final features match a goal image.

## How it works

1. Encode each frame into DINOv2 patch features with the frozen encoder.
2. Embed each action with an MLP and concatenate the embedding to each patch token.
3. Train a causal transformer predictor on offline trajectories to forecast future patch features.
4. At test time, choose action sequences by optimisation in the predicted feature space, scoring them against a goal observation.

## Key methods

DINO-WM is one of several ways to make an action-conditioned predictor. Compared with the others:

- Versus [LAPO](lapo.md), which learns the action itself from video, DINO-WM assumes actions are known and focuses on the predictor's state space.
- Versus [V-JEPA 2](v-jepa-2.md), which is trained on large video and then post-trained on robot data, DINO-WM keeps the visual encoder frozen and trains only the predictor on the target environment's trajectories.

## Results

The abstract reports that the method plans on several environments with the predictor learned from offline data. The numbers are in the paper and should be copied from there, not from secondary summaries.

## Limitations

- The predictor can only forecast what the frozen encoder keeps. Details that DINOv2 features discard cannot be predicted.
- Concatenating the action to each token is a simple conditioning choice. Whether it keeps the predictor sensitive to the action is the controllability question covered in [Action controllability](action-controllability.md).

## Connections

DINO-WM sits between [self-supervised](../../paradigms/self-supervised/index.md) visual representation learning and model-based planning. Its use of a latent prediction target is related to the joint-embedding predictive family, which predicts representations rather than pixels. The same world-model family is described on the [parent overview](index.md).

## Applications

Robot planning from images, and goal-directed navigation or manipulation in simulated environments where a predictor can be trained from logged trajectories.

## Open questions

- Whether a frozen encoder trained for appearance is the right state space for contact-rich tasks.
- How planning cost scales with the horizon and with the size of the action space.

## References

### Seminal papers

- Zhou, G., Pan, H., LeCun, Y. & Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025. https://proceedings.mlr.press/v267/zhou25t.html — Introduces the method: an action-conditioned predictor on frozen DINOv2 patch features, used for zero-shot planning. The arXiv version is at https://arxiv.org/abs/2411.04983.

### Articles and preprints

- Oquab, M. et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv preprint. https://arxiv.org/abs/2304.07193 — Self-supervised visual features whose patch tokens DINO-WM uses as its frozen state space.
- Assran, M. et al. (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning*. arXiv preprint. https://arxiv.org/abs/2506.09985 — A video-trained alternative that adds action conditioning through robot-video post-training.
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv preprint. https://arxiv.org/abs/1803.10122 — Early latent world model in which a policy is trained inside the model's own simulated environment.
- Moerland, T. M. et al. (2020). *Model-based Reinforcement Learning: A Survey*. arXiv preprint. https://arxiv.org/abs/2006.16712 — Survey of learned dynamics models and their use in planning.
