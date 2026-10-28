---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/models/world-models
tags:
  - robotics
  - navigation
  - topological map
aliases:
  - SPTM
  - Semi-parametric Topological Memory
  - 半參數拓撲記憶
---

# SPTM: Semi-Parametric Topological Memory

SPTM, introduced by Savinov, Dosovitskiy and Koltun (arXiv 2018), is a memory architecture for navigation in unseen environments. It stores the environment as a graph whose nodes are observations and whose edges record which observations are connected, with no metric information, and it uses a learned network to decide which stored node matches the current view. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

The architecture was inspired by landmark-based navigation in animals. Its authors split the memory into two parts. The first is a non-parametric graph, which is simply a set of places and their connections. The second is a parametric deep network, which takes an observation and retrieves the matching node. Because the graph holds no distances or coordinates, the agent navigates by moving between places it has seen, not by following a metric map (Savinov et al., 2018).

The paper's headline result is that, given only five minutes of footage of a previously unseen maze, the agent builds a topological map and reaches goals across test environments with an average success rate about three times that of the best baseline.

## Problem

Metric navigation needs accurate mapping, localisation and planning, and it is sensitive to small changes in the environment. A method that needs only the connectivity between places can be built quickly from a video of the environment and can tolerate imprecise positions. The question is whether a learned retrieval network can identify places reliably enough for this to work.

## Core idea

Build the graph from a walkthrough, adding an edge between consecutive frames and between frames that a learned network judges to be visual shortcuts. To navigate, localise the current view and the goal in the graph, find the shortest path between them, and move toward the furthest node on that path that still looks similar to the current view.

## Equation or algorithm

The method has three learned or computed parts:

1. **Memory graph.** Each node stores an observation, two consecutive RGB frames at 160 by 120 pixels. The walkthrough is subsampled by a factor of four. Consecutive nodes are connected. Visual shortcuts are added where the retrieval network reports that two observations are far apart in time but look similar, with a threshold chosen so that about 2,000 shortcuts are created.
2. **Retrieval network.** A Siamese network with ResNet-18 encoders produces a 512-dimensional embedding for each observation. The two embeddings are concatenated and passed through fully connected layers, and a two-way softmax predicts whether the observations are temporally close. It is trained self-supervised with cross-entropy. Positive pairs are at most 20 steps apart, and negative pairs are at least 100 steps apart.
3. **Locomotion network and planning.** A second network takes the current observation and the next waypoint observation and outputs a softmax over seven discrete actions: no-op, forward, backward, strafe left, strafe right, turn left and turn right. The agent localises itself in the graph, finds the shortest path with Dijkstra's algorithm, and chooses as its waypoint the furthest node on the path, within a short window of steps, whose similarity to the current view exceeds a threshold.

## Results

The paper evaluates the agent on seven test mazes, with success counted as reaching the goal within 5,000 steps (Savinov et al., 2018, Table 1). SPTM reaches the goal in all trials on each test, a mean of 100%. The best baseline, a goal-agnostic LSTM, reaches a mean of 33.9%. The ratio of 100 to 33.9 is about 2.95, which the paper describes as the SPTM rate being three times higher.

## Limitations

- **Discrete actions.** The locomotion network chooses from seven fixed moves, so the agent cannot produce smooth velocities, and this limits how it can respond to dynamics.
- **Prior exploration.** The graph must be built from a walkthrough of the environment before the agent can navigate in it.
- **No metric information.** The graph stores connectivity only, so the agent does not know how far away a goal is, and it cannot plan around distances.
- **Controlled environments.** The reported experiments are in mazes. Results in larger, changing outdoor scenes are not part of the paper's evaluation.

## Connections

- [ViNG](ving.md) builds on this idea. It replaces the retrieval network with a learned temporal-distance function, and it adds a learned pose predictor that drives a controller.
- [Visual teach-and-repeat](visual-teach-and-repeat.md) is the classical alternative. It also stores a route, but it tracks the route with odometry rather than with a learned retrieval network.
- [World models](../../../theory/models/world-models/index.md) cover predictive models of the environment, which are an alternative to a stored graph.

## Open questions

- Whether learned retrieval stays reliable when the environment changes between the walkthrough and the navigation run.
- How to add metric information to the graph without losing its robustness to imprecise positions.

## References

- Savinov, N., Dosovitskiy, A. & Koltun, V. (2018). *Semi-parametric Topological Memory for Navigation*. arXiv. https://arxiv.org/abs/1803.00653 — Introduces the topological memory, the retrieval network and the planning method, with the maze results quoted above.
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N. & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — Extends the topological graph with learned temporal distance and a learned controller.
- Furgale, P. & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — The classical teach-and-repeat system that stores a route and tracks it with odometry.
- Krajník, T., Majer, F., Halodová, L. & Vintr, T. (2017). *Navigation without localisation: reliable teach and repeat based on the convergence theorem*. arXiv. https://arxiv.org/abs/1711.05348 — Replays a taught motion and uses the camera only to correct heading.
- Dall'Osto, D., Fischer, T. & Milford, M. (2020). *Fast and Robust Bio-inspired Teach and Repeat Navigation*. arXiv. https://arxiv.org/abs/2010.11326 — An asynchronous teach-and-repeat formulation that fully uses odometry.
