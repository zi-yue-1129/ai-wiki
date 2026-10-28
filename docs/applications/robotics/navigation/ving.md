---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/paradigms/imitation
tags:
  - robotics
  - navigation
  - topological graph
aliases:
  - ViNG
  - Visual Navigation Graph
  - 視覺目標導航圖
---

# ViNG: Learning Open-World Navigation with Visual Goals

ViNG, introduced by Shah, Eysenbach, Kahn, Rhinehart and Levine (ICRA 2021), is a learning-based system for reaching a goal image on a real mobile robot. It combines a learned distance estimate with a topological graph built from previously collected observations, so that the goal can be changed at deployment without retraining. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

Learned navigation policies are hard to redirect. A conventional planner can be given a new goal, but a policy trained for one destination must be retrained to go elsewhere. ViNG keeps the learned part small. It learns how far apart two observations are and how to move toward a nearby observation, and it uses a graph of past observations to decide the route to a goal image. The authors report that the system works in real outdoor environments and reaches goals more than 40 metres away, which no baseline in the paper does (Shah et al., 2021).

## Problem

A system that navigates to a visually indicated goal must answer two questions: which places in the environment are connected, and how to move from one to the next. Metric mapping answers both with geometry, and it is brittle when the environment is unstructured. Learning can capture navigational affordances, such as tall grass being passable and walls not being passable, but a single end-to-end policy is hard to redirect at test time.

## Core idea

Use a learned distance function to weight a graph of observations, and let graph search pick the route. A learned pose predictor and a conventional controller then drive the robot to the next waypoint on that route. Three insights make the approach work: proposing waypoints as the action space, pruning easily traversable edges from the graph, and mining negative pairs from different trajectories.

## Equation or algorithm

The system has three components:

1. **Temporal distance function.** It takes two observations, each 160 by 120 pixels, and estimates the number of time steps between them. A MobileNet encoder feeds three dense layers over 50 bins, trained with cross-entropy.
2. **Relative pose predictor.** It uses the same encoder design and regresses the relative waypoint offset, horizontal and vertical, from odometry-derived poses, trained with an L2 loss.
3. **Controller.** A proportional-derivative controller steers the robot toward the current waypoint, using the predicted offset. It outputs continuous linear and angular velocities, and it is not itself learned.

The graph is built from offline observations, with nodes as images and no geometric coordinates. Edges are weighted by the distance function. Edges whose estimated traversal is below a sparsity threshold are dropped. At test time the current and goal images are added to the graph and connected to their most traversable neighbours, and a weighted Dijkstra search gives the shortest path. The robot then moves toward the next node on that path.

## Results

In real-world trials, the authors report a success rate of 86% on the most challenging tasks. ViNG is the only method in the paper that reaches goals more than 40 metres away. The baselines are SPTM, an off-SoRB variant, a state estimator using GPS ground truth, and a random policy (Shah et al., 2021, Fig. 3).

Ablations are reported at a goal distance of 50 metres (Table II). The temporal-difference variant of the waypoint method scores 0.87, and the base waypoint method scores 0.81. Discrete actions score 0.70, and removing graph pruning drops the score to 0.52. Training on positive pairs only scores 0.43, and predicting actions directly scores 0.40.

On four new outdoor sites (barracks, industrial, park and tall grass), fine-tuned ViNG scores 0.96, 0.84, 0.82 and 0.79. Fine-tuned SPTM scores 0.74, 0.68, 0.71 and 0.56 on the same sites.

## Limitations

- The planner works over a static, offline dataset of observations, which the authors list as a limitation of the approach.
- It does not yet handle non-stationary changes such as lighting and dynamic objects. The authors identify robust representations as future work.
- The paper's controller is hand-designed. The learned parts do not cover control, so the controller's behaviour is not learned from the same data.

## Connections

- [SPTM](sptm.md) is the memory method ViNG builds on. ViNG replaces its retrieval network with a learned distance function.
- [GNM](gnm.md) and [ViNT](vint.md) are later learned policies that predict future motion from image inputs, with the goal given as an image.
- [Visual teach-and-repeat](visual-teach-and-repeat.md) is the classical route-following method, which needs no learned distance.

## Open questions

- Whether the graph can be extended online as the robot explores, rather than built from offline data alone.
- How to keep the distance estimate reliable when lighting and appearance change between collection and deployment.

## References

- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N. & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — The source of the distance function, the graph method, the ablations and the real-world results.
- Savinov, N., Dosovitskiy, A. & Koltun, V. (2018). *Semi-parametric Topological Memory for Navigation*. arXiv. https://arxiv.org/abs/1803.00653 — The topological memory that ViNG extends, and the baseline compared in the real-world trials.
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N. & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — A later model that trains one shared policy across robots, with waypoint outputs.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N. & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — A transformer successor that uses a graph for subgoal selection.
- Furgale, P. & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — The classical route-following method that graph-based learning generalises.
