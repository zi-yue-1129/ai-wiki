---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics
  - theory/models/world-models
  - theory/paradigms/imitation
tags:
  - robotics
  - navigation
  - visual navigation
  - image goals
aliases:
  - Visual navigation
  - Image-goal navigation
  - 視覺導航
---

# Navigation with Visual Goals

A robot can be told where to go in several ways: by coordinates on a map, by a language instruction, or by showing it an image of the destination. This subtopic covers the last case, in which a camera image of the goal, or of a waypoint along the way, is the only specification. Two lines of work meet here. Visual teach-and-repeat is the classical version, in which the robot first drives a route and later replays it. Learned image-goal navigation generalises that idea with a topological memory of images and a policy trained on large collections of robot driving data.

## Overview

A typical learned system stores a set of images as a graph, with edges between frames that are close in space or time. To reach a goal, it finds a path through the graph, takes the next image as a subgoal, and outputs a motion that moves the robot toward it. The policy that does this predicts discrete actions, relative waypoints, velocities, or a distribution over action sequences, depending on the method.

Teach-and-repeat avoids a learned policy altogether. It tracks the taught route with odometry or a replayed motion profile, and it corrects heading from images. The learned methods replace the tracker with a network, and they use a graph to decide where to go next.

## Key methods

Each method has its own page. The overview and comparison here are brief.

| Method | Output of the policy | Memory | What it changes |
|---|---|---|---|
| [Visual teach-and-repeat](visual-teach-and-repeat.md) (classical) | Path tracking on lateral and heading error | The taught route, as local submaps or keyframes | Steering from signed errors computed against the stored route, with no learned policy |
| [SPTM](sptm.md) (Savinov et al., 2018) | One of seven discrete actions | A topological graph of frames, with visual shortcuts | A learned retrieval network for localisation, and a discrete locomotion network |
| [ViNG](ving.md) (Shah et al., 2021) | Relative pose to a waypoint, with a hand-designed controller | A graph of offline observations, weighted by a learned temporal distance | A learned distance for graph search, and a learned pose predictor |
| [GNM](gnm.md) (Shah et al., 2022) | Normalised waypoints | One model shared across robots and datasets | Waypoint outputs, compared with velocity outputs in the paper |
| [ViNT](vint.md) (Shah et al., 2023) | Five future waypoints and a temporal distance | Diffusion subgoal proposals, searched with an A*-like method | A transformer with about 31 million parameters, adaptable with little data |
| [NoMaD](nomad.md) (Sridhar et al., 2023) | Action sequences sampled from a diffusion model | Goal masking, so the same model can explore without a goal | One policy for goal-conditioned navigation and undirected exploration |

The rows differ in what the policy outputs, and the papers that compare output spaces report the following. In ViNG, the waypoint method scores 0.81 at a 50-metre goal distance, against 0.70 for a waypoint variant with discrete outputs and 0.40 for predicting actions directly (Shah et al., 2021, Table II). In GNM, normalised waypoints score 1.00 and 0.95 on the LoCoBot in the easy and moderate settings, against 0.73 and 0.54 for velocity outputs (Shah et al., 2022, Table V). These comparisons are within each paper and on different tasks, so they should not be read as one ranking.

## Connections

- [Robotics](../index.md) places navigation among the other robotic tasks in the wiki.
- [Behavioural cloning](../../../theory/paradigms/imitation/behavioural-cloning/index.md) is the training setting for most learned navigation policies.
- [World models](../../../theory/models/world-models/index.md) cover the predictive models that some of these methods use for planning.

## Open questions

- Whether a single shared model across robots, as in GNM and ViNT, transfers to platforms with very different dynamics, such as aerial and legged robots.
- How well graphs built from one traversal hold up when the environment changes, which is the setting of classical teach-and-repeat.

## References

- Furgale, P., & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — the canonical topometric teach-and-repeat system, built on odometry and submaps.
- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric Topological Memory for Navigation*. arXiv. https://arxiv.org/abs/1803.00653 — introduces the topological image memory and the learned locomotion network.
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — learns temporal distance and relative pose for goal-image navigation.
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — trains one navigation model across robots and compares output spaces.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — a transformer foundation model for visual navigation, with diffusion subgoal proposals.
- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration*. arXiv. https://arxiv.org/abs/2310.07896 — a diffusion policy with goal masking for goal-conditioned navigation and exploration.
