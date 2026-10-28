---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
tags:
  - robotics
  - navigation
  - temporal distance
aliases:
  - ViNG
  - Visual navigation with visual goals
  - 以視覺目標導航
---

# ViNG

ViNG, introduced by Shah, Eysenbach, Kahn, Rhinehart and Levine (2021), learns to navigate toward goal images using a graph of images collected offline. Two learned heads do the work: one predicts the temporal distance between two images, which is used to plan through the graph, and the other predicts the relative pose to a nearby waypoint, which a controller follows. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

ViNG builds a topological graph from offline driving data, with nodes as images and edges where the temporal distance is short. The temporal distance head estimates how many steps separate two images, and it decides which edges are plausible. Once a path is planned, the pose head predicts the relative displacement to the next waypoint, and a proportional-derivative controller drives the robot toward it.

## Problem

Earlier topological systems had to decide the next move from discrete directions, and they struggled when the goal was far away or the graph was sparse. The paper asks whether a learned temporal distance can plan through the graph, and whether regressing a continuous waypoint works better than selecting a discrete command for control.

## Core idea

Separate planning from control. Planning uses a learned temporal distance over the graph to pick a path. Control uses a regression head that outputs the relative pose to the next waypoint. Graph pruning removes edges that the temporal distance model judges too long, which keeps planning reliable.

## How it works

1. Collect offline driving data and build a graph whose nodes are images and whose edges connect nearby frames.
2. Train the temporal distance head on image pairs, classifying how many steps apart they are, with negatives drawn from distant frames.
3. Train the pose head to predict the relative position of the waypoint from the current image and the waypoint image.
4. At run time, plan a shortest path through the pruned graph to the goal image, and follow it with the pose head and a PD controller.

## Results

The paper reports real-robot experiments on a small wheeled robot outdoors, with a graph built from about forty hours of offline data. The authors report that regressing the relative pose to a waypoint outperforms choosing among discrete directions, and that graph pruning matters for success. The exact success rates depend on goal distance and should be checked in the paper's tables.

## Limitations

- Building the graph needs a large offline dataset that covers the environment, and the graph does not adapt on its own to new areas.
- The temporal distance is learned on the training distribution. Large changes in appearance can make it inaccurate.
- The controller is a simple PD tracker, so the method's results depend on the robot's dynamics being similar to those in the data.

## Connections

- [SPTM](sptm.md) introduced the topological memory that ViNG builds on, with a discrete action output.
- [GNM](gnm.md) and [ViNT](vint.md) extend the same idea to many robots and to larger training sets.
- [Navigation with Visual Goals](index.md) compares the output spaces of these methods.

## Open questions

- How to add new environments to the graph without retraining the temporal distance model from scratch.
- Whether the temporal distance generalises across buildings, weather and seasons.

## References

- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — the source of the temporal distance and relative pose heads.
- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric topological memory for navigation*. ICLR 2018. arXiv:1803.00653. https://arxiv.org/abs/1803.00653 — the topological memory that ViNG extends.
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — a shared model trained on several robots, with output spaces compared.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — a larger successor that predicts temporal distance and waypoints.
- Codevilla, F., Santana, E., López, A. M., & Gaidon, A. (2019). *Exploring the limitations of behavior cloning for autonomous driving*. ICCV 2019. arXiv:1904.08980. https://arxiv.org/abs/1904.08980 — documents failure modes of behaviour cloning that bear on learned navigation.
