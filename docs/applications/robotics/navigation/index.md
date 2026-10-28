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

A typical learned system stores a set of images as a graph, with edges between frames that are close in space or time. To reach a goal, it finds a path through the graph, takes the next image as a subgoal, and outputs a motion that moves the robot toward it. The network that does this either predicts velocities, relative waypoints, or a distribution over actions. Earlier systems chose among a small set of discrete commands, and later ones regress continuous motion.

Teach-and-repeat avoids learning the policy by tracking the taught path with odometry and correcting heading from images. Learned methods replace the tracker with a network, and they use the graph to decide where to go next.

## Key methods

Each method has its own page. The overview and comparison here are brief.

| Method | Output of the policy | Memory | What it changes |
|---|---|---|---|
| [Visual teach-and-repeat](visual-teach-and-repeat.md) (classical) | Path tracking on a metric or odometric error | A taught route of images | Steering from a signed bearing or lateral error, not from image similarity |
| [SPTM](sptm.md) (Savinov et al., 2018) | A discrete action from a pair of images | A topological graph of frames | Learned localisation and a discrete locomotion classifier |
| [ViNG](ving.md) (Shah et al., 2021) | Relative pose to a waypoint | Graph built from offline data | Temporal distance for planning, and pose regression for control |
| [GNM](gnm.md) (Shah et al., 2023) | Normalised waypoints | Shared model across robots | Waypoint outputs succeed where velocity outputs struggle on sharp turns |
| [ViNT](vint.md) (Shah et al., 2023) | Future waypoints and temporal distance | Graph with Dijkstra subgoal selection | A transformer foundation model, adaptable with little data |
| [NoMaD](nomad.md) (Sridhar et al., 2023) | Samples from a diffusion model over actions | Goal-masked, so the same policy also explores | Keeps several modes, such as left and right at a junction |

The table shows a trend. Systems that regress continuous motion usually outperform those that choose from discrete commands on the same task. Hirose et al. (2019) show the same point in a different form: scoring candidate motions through a learned world model in real time was much weaker than a policy trained to imitate the scored behaviour. Planning with a learned predictive model is covered in the [world models](../../../theory/models/world-models/index.md) subtopic.

## Connections

- [Robotics](../index.md) places navigation among the other robotic tasks in the wiki.
- [Behavioural cloning](../../../theory/paradigms/imitation/behavioural-cloning/index.md) is the training setting for most learned navigation policies.
- [World models](../../../theory/models/world-models/index.md) cover the predictive models that some of these methods use for planning.

## Open questions

- Whether a single shared model across robots, as in GNM and ViNT, transfers to platforms with very different dynamics, such as aerial and legged robots.
- How well graphs built from one traversal hold up when the environment changes, which is the setting of classical teach-and-repeat.

## References

- Furgale, P., & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — the canonical topometric teach-and-repeat system.
- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric topological memory for navigation*. ICLR 2018. arXiv:1803.00653. https://arxiv.org/abs/1803.00653 — introduces a topological image memory with a learned locomotion network.
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — learns temporal distance and relative pose for goal-image navigation.
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — trains one navigation model across robots and compares output spaces.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — a transformer policy with a topological graph for navigation.
- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv:2310.07896. https://arxiv.org/abs/2310.07896 — uses a diffusion policy with goal masking for goal-conditioned navigation and exploration.
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep visual MPC-policy learning for navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. arXiv:1903.02749. https://arxiv.org/abs/1903.02749 — compares scoring predicted futures with distilling them into a policy.
