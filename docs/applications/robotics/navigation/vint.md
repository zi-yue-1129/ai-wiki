---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
tags:
  - robotics
  - navigation
  - foundation model
  - transformer
aliases:
  - ViNT
  - Visual Navigation Transformer
  - 視覺導航 Transformer
---

# ViNT: A Foundation Model for Visual Navigation

ViNT, introduced by Shah, Sridhar, Dashora, Stachowicz, Black, Hirose and Levine (2023), is a transformer policy for visual navigation trained on a large mixture of robot driving datasets. It predicts a temporal distance and a short sequence of future waypoints from past frames and a goal image. A topological graph of images supplies the subgoals, and the policy is then fine-tuned to new tasks with modest data. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

ViNT has two parts. A pretrained transformer encodes a short history of frames together with the goal, and two heads produce a temporal distance estimate and future waypoints. At run time, a graph of stored images is searched for a path, the next node serves as the subgoal, and the policy's waypoints are followed by a receding-horizon controller.

## Problem

Earlier navigation policies were trained on one robot or one environment, and they needed much new data for each setting. The paper asks whether a large, diverse training set and a transformer architecture yield a single model that transfers to new robots and tasks with little additional data.

## Core idea

Scale the data and the model together, and predict outputs that are useful for both planning and control. The temporal distance head gives a planning signal across the graph, and the waypoint head gives the control signal. The model is trained on data that mixes many robots, which the paper argues is needed for broad generalisation.

## How it works

1. Train the transformer on a mixture of navigation datasets from different robots, predicting temporal distance and future waypoints.
2. Build a topological graph of images for the target environment, and search it for a path to the goal.
3. Take the next node on the path as the subgoal, and run the policy with the current frame history.
4. Follow the predicted waypoints with a PD controller, replanning as new frames arrive.
5. To adapt to a new task, fine-tune on a small amount of task data.

## Results

The paper reports that the model trains on more than a hundred hours of data and has about 31 million parameters, and that it navigates routes of hundreds of metres to over a kilometre in the authors' real-world tests. It reports that adapting the model to new tasks with one to two hours of data improves success substantially. The ablation against random subgoal selection shows that graph-based subgoals matter. The exact numbers should be checked in the paper's tables.

## Limitations

- The model is large, so running it on small onboard computers requires an accelerator that not every platform carries.
- A topological graph built from one traversal is essentially a chain, which limits the choice of subgoals.
- Success on new tasks depends on the amount and quality of the adaptation data, which the paper reports only for its own setups.

## Connections

- [GNM](gnm.md) is the predecessor that introduced the shared model and the normalised waypoint output.
- [NoMaD](nomad.md) is a later variant that uses a diffusion policy and goal masking.
- [ViNG](ving.md) gives the temporal distance and graph planning that ViNT uses.

## Open questions

- How far a single foundation model can cover environments with very different appearance and layout.
- Whether the adaptation data needed for a new task can be reduced further with self-supervised pretraining on unlabelled video.

## References

- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — the source of the transformer policy, the graph planner and the adaptation results.
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — the shared model and output-space comparison that ViNT builds on.
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — the temporal distance and graph planning approach.
- Savinov, N., Dosovitskiy, A., & Koltun, V. (2018). *Semi-parametric topological memory for navigation*. ICLR 2018. arXiv:1803.00653. https://arxiv.org/abs/1803.00653 — the topological memory used for subgoal selection.
- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv:2310.07896. https://arxiv.org/abs/2310.07896 — a later policy in the same family.
