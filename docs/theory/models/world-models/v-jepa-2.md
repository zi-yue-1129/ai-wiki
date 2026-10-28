---
status: draft
last_reviewed: 2026-10-28
tags:
  - world models
  - self-supervised
  - robotics
aliases:
  - V-JEPA 2
  - V-JEPA 2-AC
---

# V-JEPA 2

V-JEPA 2 is a self-supervised video model that predicts masked content in representation space, not in pixels. The paper extends it to a world model, V-JEPA 2-AC, by post-training an action-conditioned predictor on a small amount of unlabelled robot video. The authors then use this predictor to plan robot actions.

## Problem

Video models learn a lot about appearance and motion, but a model that only predicts video does not tell a robot what its actions will do. The paper asks whether a video representation learned without labels can be turned into an action-conditioned predictor, with little robot data, and used for planning on a real arm.

## Core idea

The encoder is trained on large amounts of video with a joint-embedding predictive objective, which predicts the representations of hidden parts of the input. For control, the authors post-train an action-conditioned predictor on robot trajectories, conditioning it on the executed actions. The predictor is then used in a planning loop that searches for actions reaching a goal image.

## How it works

1. Pre-train a video encoder by predicting representations of masked video regions, in the joint-embedding predictive style of [I-JEPA](../../paradigms/self-supervised/index.md).
2. Post-train an action-conditioned predictor on robot video, where the actions are the recorded robot motions.
3. At control time, sample candidate action sequences, predict their outcomes in representation space, and pick the one whose predicted state is closest to the goal image.

The exact training objectives and their weights are given in the paper's method section. Read it before reusing the recipe.

## Key methods

V-JEPA 2 is one of several ways to add actions to a pre-trained video predictor. Compared with the others:

- Versus [DINO-WM](dino-wm.md), which trains its predictor on the target environment's own trajectories with a frozen image encoder, V-JEPA 2 starts from a video encoder trained on large general video data and post-trains with robot video.
- Versus [Genie](genie.md), which generates interactive video, V-JEPA 2 predicts in representation space and is used for planning rather than for generating pixels.

## Results

According to the abstract, V-JEPA 2-AC was post-trained on under 62 hours of unlabelled robot video from the DROID dataset. It was then deployed zero-shot on Franka arms in two labs to pick and place objects by planning toward image goals. The abstract's headline numbers should be copied from the paper, not from secondary summaries.

## Limitations

- The reported robot evaluation uses a specific arm and a specific set of tasks. Generality to other embodiments is a question the paper does not settle.
- Planning in representation space depends on the encoder keeping the features needed to tell goals apart.

## Connections

V-JEPA 2 links the [self-supervised](../../paradigms/self-supervised/index.md) line of joint-embedding predictive work to model-based control. Its action conditioning raises the same question as [action controllability](action-controllability.md): whether the predictor really depends on the action it is given. For the wider family of world models, see the [parent overview](index.md).

## Applications

Zero-shot pick-and-place with a learned predictor, and planning from video goals in laboratories with different robots.

## Open questions

- How much robot data is needed for a new embodiment, and whether the 62-hour figure is a lower bound.
- Whether planning in representation space keeps the fine spatial detail that precise grasping needs.

## References

### Seminal papers

- Assran, M., Bardes, A., Fan, D. et al. (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning*. arXiv preprint. https://arxiv.org/abs/2506.09985 — Introduces V-JEPA 2 and its action-conditioned variant V-JEPA 2-AC, post-trained on robot video for zero-shot planning.

### Articles and preprints

- Zhou, G. et al. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025. https://proceedings.mlr.press/v267/zhou25t.html — A predictor on frozen image features, the comparison point for planning from video-pretrained features.
- Bruce, J. et al. (2024). *Genie: Generative Interactive Environments*. ICML 2024. https://proceedings.mlr.press/v235/bruce24a.html — The generative counterpart: a latent action model trained on unlabelled video.
- Assran, M. et al. (2023). *Self-Supervised Learning From Images With a Joint-Embedding Predictive Architecture*. CVPR 2023. https://openaccess.thecvf.com/content/CVPR2023/html/Assran_Self-Supervised_Learning_From_Images_With_a_Joint-Embedding_Predictive_Architecture_CVPR_2023_paper.html — The image version of the joint-embedding predictive approach that V-JEPA 2 extends to video.
