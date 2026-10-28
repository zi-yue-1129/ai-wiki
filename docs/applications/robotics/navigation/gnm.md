---
status: complete
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/models/world-models
tags:
  - robotics
  - navigation
  - foundation model
aliases:
  - GNM
  - General Navigation Model
  - 通用導航模型
---

# GNM: General Navigation Model

GNM, introduced by Shah, Sridhar, Bhorkar, Hirose and Levine (2022), is a single goal-conditioned navigation model trained on data from six different robots. It takes the current observation and a goal image, and it predicts a short sequence of normalised waypoints. Its main lesson concerns the action representation: waypoints scaled to each robot's top speed transfer across platforms better than raw velocities. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

Navigation policies are usually trained on the data of one robot, and they degrade when the platform changes. GNM asks whether data from many distinct but structurally similar robots can be pooled into one model. The authors identify two design choices that make pooling work: using temporal context, and a standardised action space. They report that an omnipolicy trained on heterogeneous data outperforms policies trained on any single dataset, and that it can be deployed on robots not in the training set (Shah et al., 2022).

## Problem

A vision-based navigation policy needs data, and collecting it on one robot is slow. Data from different robots has different cameras, speeds and dynamics, so naively pooling it can confuse the model. The question is which representation of the action makes trajectories from different robots comparable, and what else the model must see to use them well.

## Core idea

Standardise the action space. Each waypoint is scaled by the robot's top speed, so that a unit of motion means the same fraction of what the robot can do, whatever its size. The model also sees a short history of past frames, which supplies the context needed for manoeuvres that a single image does not disambiguate. One network is trained on all robots together.

## Equation or algorithm

The policy has two heads, trained jointly by supervised learning:

1. **Visual encoders.** Separate MobileNetV2 encoders process the current observation, with its context frames, and the goal image. The two embeddings are concatenated and passed through three fully connected layers.
2. **Temporal distance.** One head predicts the normalised temporal distance to the goal. It is trained on positive and negative pairs.
3. **Normalised waypoints.** The second head predicts five future waypoints, each as a relative position and a yaw change, scaled by the robot's top speed. It is trained only on positive pairs with a regression loss.

The paper uses five past observations as context. The exact loss weighting between the two heads is not stated in the text read for this page.

## Results

On the action-space comparison, the authors evaluate on ten environments with a LoCoBot. Success rates are reported for easy and moderate environments (Shah et al., 2022, Table V):

| Output space | Easy | Moderate |
|---|---|---|
| Velocities | 0.73 | 0.54 |
| Raw waypoints | 0.42 | 0.26 |
| Normalised waypoints | 1.00 | 0.95 |

Table II compares GNM with GS and RECON, the single-robot baselines, on four robots: the LoCoBot, the DJI Tello, the Vizbot and the Clearpath Jackal (Shah et al., 2022, Table II). The values are mean success rates.

| Method | LoCoBot | DJI Tello | Vizbot | Jackal |
|---|---|---|---|---|
| GS | 0.26 | 0.21 | 0.51 | 0.31 |
| RECON | 0.62 | 0.79 | 0.26 | 0.68 |
| GNM | 0.96 | 0.99 | 0.93 | 0.94 |

The paper's caption states that the shared policy outperforms the best single-robot policy for each robot. The paper does not report a head-to-head comparison with ViNG.

## Limitations

- The model is trained by imitation, and it inherits the limitations of behaviour cloning, including sensitivity to the distribution of the demonstrations.
- The normalisation needs each robot's top speed, which must be known for every new platform.
- The text and Table I give different counts of datasets and hours of data, so take those figures from the paper's table when they matter.

## Connections

- [ViNG](ving.md) is the earlier method from the same line of work. It uses a graph of observations and predicts relative pose on a single robot.
- [ViNT](vint.md) is a larger transformer successor trained on more datasets.
- [NoMaD](nomad.md) replaces the regression head with a diffusion model over actions and adds goal-agnostic exploration.
- [Visual teach-and-repeat](visual-teach-and-repeat.md) is the classical method that needs no learned policy.

## Open questions

- Whether a normalised representation holds up for robots whose control interface is not a planar velocity.
- How much robot-specific data is needed to adapt the shared model to a new platform reliably.

## References

- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N. & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — The source of the shared model, the standardised action space and the output-space comparison.
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N. & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — A transformer successor that scales the same idea to more data and adds temporal-distance and waypoint outputs.
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N. & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — The single-robot predecessor that combines a learned policy with a topological graph.
- Sridhar, A., Shah, D., Glossop, C. & Levine, S. (2023). *NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration*. arXiv. https://arxiv.org/abs/2310.07896 — A diffusion-based successor for goal-conditioned navigation and exploration.
