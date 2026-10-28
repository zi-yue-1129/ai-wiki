---
status: complete
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/models/transformer
tags:
  - robotics
  - navigation
  - foundation model
aliases:
  - ViNT
  - Visual Navigation Transformer
  - 視覺導航 Transformer
---

# ViNT: A Foundation Model for Visual Navigation

ViNT, introduced by Shah, Sridhar, Dashora, Stachowicz, Black, Hirose and Levine (arXiv 2023), is a transformer-based foundation model for goal-image navigation. It is trained on many existing navigation datasets from different robots, it can be adapted to a new task with a small amount of data, and it can be paired with diffusion-based subgoal proposals for exploration over long distances. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

General-purpose pre-trained models have helped in many machine learning problems because a large, weakly labelled pre-training set makes small downstream datasets sufficient. ViNT asks whether the same holds for navigation. The authors train one transformer with a general goal-reaching objective on any navigation dataset, and they report that the resulting model shows positive transfer, outperforming specialist models trained on single datasets (Shah et al., 2023).

The model is not only a single policy. Combined with a diffusion model that proposes subgoal images, ViNT can explore novel environments, and the authors report kilometre-scale navigation runs, guided by GPS or by satellite imagery.

## Problem

Navigation datasets come from different robots, cameras and environments, and each is small. A policy trained on one dataset rarely works on another platform. Pooling the datasets requires a model that can absorb heterogeneous data, and an adaptation method that needs little data for each new task.

## Core idea

Use a transformer that reads a short history of observations, and a goal image, and predicts both how far the goal is and a sequence of future waypoints. Train it on everything, then fine-tune the whole model with a small learning rate for a new task. For long-range exploration, sample subgoal images from a diffusion model and select among them with a search that uses the goal as a heuristic.

## Equation or algorithm

The architecture has four main parts:

1. **Encoders.** Two EfficientNet-B0 encoders process the current observation with its past context, and the goal. The goal encoder is fused with the current observation by stacking them channel-wise.
2. **Transformer.** A decoder-only transformer with four layers, four heads and 512-dimensional tokens. The model has about 31 million parameters, and the paper uses five past frames as context.
3. **Outputs.** One head predicts the temporal distance to the subgoal. The second predicts five future relative waypoints.
4. **Subgoal search.** A diffusion model with about 318 million parameters, sampled with 200 DDIM steps, proposes candidate subgoal images. ViNT grounds each candidate by predicting how far it is, and an A*-like search with a goal-directed heuristic picks the next subgoal.

For adaptation, the whole model is fine-tuned end to end with a learning rate of 10⁻⁴ for five epochs. A learned goal token can replace the image goal encoder so that the model accepts other goal types, such as GPS waypoints or routing commands.

## Results

The main text describes the training data as eleven datasets from eight robotic platforms, with over 100 hours of trajectories. Other totals appear in the paper's tables and captions, so the exact amount should be taken from the paper's data table. For undirected goal reaching, ViNT scores 0.94 indoors and 1.00 outdoors, against 0.72 and 0.44 for end-to-end behaviour cloning and 0.19 and 0.23 for RECON on the same settings (Shah et al., 2023, Table 1).

With subgoal diffusion, the paper reports distances of 1,270 metres in a GPS-guided run and 1,040 metres in a satellite-guided run, with success rates of 0.95 and 1.00 (Table 2). In zero-shot runs on new robots, ViNT covers more distance than GNM on the LoCoBot (120 m against 60 m), the Go 1 (45 m against 8 m) and the Vizbot (110 m against 20 m). On the Clearpath Jackal the two are nearly equal, at 438 m and 427 m (Table 3). The paper reports that fine-tuning can master a new environment with about one hour of data, with about 80% success.

## Limitations

- The kilometre-scale results depend on the added subgoal diffusion and graph search. Success in those runs is judged informally, as reaching the goal without intervention, and the paper gives no formal definition beyond that.
- The paper's dataset totals differ between sections, so claims about data size should be checked against the paper.
- Goal images, though general, are not always the most natural way for a user to say where to go. The authors propose a learned goal token for other goal types, but the reported experiments are with images.
- The Jackal results show that, on some platforms, ViNT and GNM perform about the same, so the gain is not uniform across robots.

## Connections

- [GNM](gnm.md) is the shared-data navigation model that ViNT extends with a larger transformer and more data.
- [ViNG](ving.md) is the earlier graph-based method, whose graph search ViNT's subgoal selection resembles.
- [NoMaD](nomad.md) uses a related transformer encoder with a diffusion decoder, and adds goal masking for exploration.
- [Transformers](../../../theory/models/transformer/index.md) cover the architecture that ViNT uses.

## Open questions

- Whether a navigation foundation model can be adapted to very different tasks, such as manipulation near the robot, with a comparable amount of data.
- How much of the kilometre-scale performance comes from the learned model, and how much from the search and the diffusion proposals.

## References

- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N. & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — The source of the model, the training data, the adaptation method and the kilometre-scale results.
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N. & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — The shared navigation model from which ViNT's multi-dataset training follows.
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N. & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — The graph-based predecessor whose search ViNT's subgoal selection extends.
- Sridhar, A., Shah, D., Glossop, C. & Levine, S. (2023). *NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration*. arXiv. https://arxiv.org/abs/2310.07896 — A later diffusion-based model that uses a related transformer encoder.
- Savinov, N., Dosovitskiy, A. & Koltun, V. (2018). *Semi-parametric Topological Memory for Navigation*. arXiv. https://arxiv.org/abs/1803.00653 — The topological memory whose graph idea the subgoal search builds on.
