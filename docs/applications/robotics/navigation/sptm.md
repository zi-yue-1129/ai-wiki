---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
tags:
  - robotics
  - navigation
  - topological memory
aliases:
  - SPTM
  - Semi-parametric topological memory
  - 半參數拓撲記憶
---

# Semi-Parametric Topological Memory (SPTM)

SPTM, introduced by Savinov, Dosovitskiy and Koltun (2018), navigates with a graph of stored images. A learned network chooses the next action from the current image and the next waypoint image in the graph. The method is trained on a short video of the environment, and it does not need a metric map. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

SPTM has three parts: a memory of images organised as a topological graph, a retrieval step that localises the current view in the graph, and a locomotion network that outputs a discrete action. The graph is built from a single traversal, and each node is a frame. The name reflects that the memory is stored non-parametrically as images, while the localisation and locomotion are learned.

## Problem

Goal-directed navigation from images needs to know where the robot is in a map, and it needs to choose actions that move it toward the goal. Earlier topological methods had to localise from scratch on each frame, which is unreliable in repetitive environments, and they relied on hand-designed action rules. The paper asks whether a learned locomotion model, trained with self-supervision on the stored video, can replace both.

## Core idea

Pick a waypoint from the graph that is ahead of the robot and reachable with high confidence. Then train a locomotion network to predict the action that moves the agent from its current view toward that waypoint view. The waypoint is chosen by a reachability estimate, so the lookahead adapts to how far the robot can go with confidence.

## How it works

1. Build the graph from a video of the environment by linking frames that are close in time.
2. Localise the current observation in the graph. Search near the previous location, and fall back to a global search only when that fails.
3. Pick the furthest waypoint whose predicted reachability exceeds a threshold, within a bounded window of graph steps.
4. Feed the current image and the waypoint image into the locomotion network, and execute the predicted discrete action.

## Results

The authors report that SPTM achieved about three times the success of the best baseline in their maze experiments with about five minutes of video. The ablations show that temporally consistent localisation beats localising each frame independently. The experiments are in simulation, in mazes built on the DOOM engine, so their transfer to real robots is not shown in the original paper.

## Limitations

- The action space is discrete, so the robot can only turn or move in fixed steps. Later methods show that continuous outputs handle sharp turns better.
- Localisation depends on the graph covering the environment well, and places that look similar can confuse the retrieval step.
- The original evaluation is in simulation, so the paper does not show behaviour on a real robot.

## Connections

- [Navigation with Visual Goals](index.md) puts SPTM in context with later learned methods.
- [ViNG](ving.md) keeps the topological graph but learns temporal distance and continuous relative pose.
- [Visual teach-and-repeat](visual-teach-and-repeat.md) is the classical approach to the same route-following problem.
- [Meng et al. (2020)](https://arxiv.org/abs/1909.12329) scale local control to large topological maps by regressing waypoints.

## Open questions

- How to choose the reachability threshold and the lookahead window for real environments with long corridors and open spaces.
- Whether discrete action policies can be made to cope with sharp turns without losing their simplicity.

## References

- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric topological memory for navigation*. ICLR 2018. arXiv:1803.00653. https://arxiv.org/abs/1803.00653 — the original method and its ablations.
- Meng, X., Ratliff, N., Xiang, Y., & Fox, D. (2020). *Scaling local control to large-scale topological navigation*. ICRA 2020. arXiv:1909.12329. https://arxiv.org/abs/1909.12329 — compares direct control regression with waypoint regression on topological maps.
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — the continuous successor that learns temporal distance and relative pose.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — a large-scale successor that keeps the topological graph.
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep visual MPC-policy learning for navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. arXiv:1903.02749. https://arxiv.org/abs/1903.02749 — image-subgoal navigation with a learned policy.
