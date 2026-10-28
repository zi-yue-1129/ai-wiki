---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
tags:
  - robotics
  - navigation
  - teach and repeat
  - visual odometry
aliases:
  - Visual teach and repeat
  - VT&R
  - 視覺教學與重播
---

# Visual Teach-and-Repeat

Visual teach-and-repeat (VT&R) is a family of methods in which a robot is first driven along a route under human control, and it stores what it sees. Later it drives the same route on its own by comparing the current camera view with the stored one. Furgale and Barfoot (2010) gave the canonical topometric form of the method. The parent subtopic is [Navigation with Visual Goals](index.md).

## Overview

The stored route is a chain of local submaps or keyframes, each linked to the next by a relative transform. The robot localises itself against the nearby part of that chain and steers to follow the taught path. Because the error is measured relative to the stored route, the method does not need GPS or a global map frame.

## Problem

A route can be long, and the environment changes between the teaching run and the repeat. The robot must follow the taught path accurately, keep its position estimate from drifting, and cope with changes in lighting and appearance. Topometric maps address this by keeping the local error small without requiring a globally consistent metric map.

## Core idea

Localise relative to the teach data and steer using a signed error. Furgale and Barfoot localise against overlapping submaps and control the robot with a path tracker on the lateral and heading error. Krajník and colleagues take a simpler route. In their 2017 formulation, the robot replays the velocities it recorded during teaching, indexed by distance travelled, and the camera is used only to correct heading. Their abstract reports that the resulting error does not diverge over a route.

## Equation or algorithm

The core quantities are the lateral offset and the heading error of the robot relative to the taught path, both measured against the stored data. A controller then reduces these errors. The papers give the exact control laws, and this page does not reproduce them.

For the replay variant, the procedure is:

1. During teaching, record images and the motion along the route.
2. During repeat, replay the recorded velocities, indexed by distance travelled.
3. Use the image to estimate the heading correction, and apply it to the replayed motion.

The Krajník 2010 bearing-only method stores a map of places and their bearings, and it moves between segment endpoints that are defined by odometry. Dall'Osto et al. (2020) describe an asynchronous teach-and-repeat formulation built on odometry.

## Results

The papers report field tests, and their specific numbers should be checked in the sources before reuse. Furgale and Barfoot report long-range field trials on a rover. Krajník et al. (2017) report, in their abstract, that replaying the learned velocities and correcting heading with the camera keeps the error from diverging. Rozsypálek et al. (2023) report results for long-term repeats across changing conditions, which is the main setting of their multidimensional particle filter.

## Limitations

- Odometry drift grows with distance, so systems rely on a reliable distance estimate to decide when to turn.
- Image features can be lost on sharp turns or in featureless areas, which is why replay with a motion profile is often combined with vision.
- A single traversal stores one appearance. Long-term use across lighting and season needs filtering or registration that tolerates change, which is the focus of Rozsypálek et al. (2023).

## Variants

- **Topometric submap teach-and-repeat** (Furgale and Barfoot, 2010): local submaps linked by relative transforms, with path tracking on metric errors.
- **Bearing-only teach-and-repeat** (Krajník et al., 2010): a map of bearings, with odometric segment endpoints.
- **Replay with visual heading correction** (Krajník et al., 2017): taught velocities replayed by distance, with the camera correcting heading.
- **Asynchronous odometry-based teach-and-repeat** (Dall'Osto et al., 2020): an asynchronous formulation built on odometry.
- **Multidimensional particle filter for long-term repeat** (Rozsypálek et al., 2023): a filter across changing conditions.

## Connections

- [Navigation with Visual Goals](index.md) places teach-and-repeat next to learned image-goal navigation.
- [SPTM](sptm.md) is a learned topological alternative that replaces the odometric tracker with a network.
- [ViNG](ving.md) learns the distance and pose that a teach-and-repeat tracker would otherwise compute from odometry.

## Open questions

- How teach-and-repeat should handle changes in the environment that happen between the teach and repeat runs, beyond small appearance changes.
- Whether learned image registration can match the accuracy of geometric localisation on very long routes.

## References

- Furgale, P., & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — the canonical topometric teach-and-repeat system, built on odometry and submaps.
- Krajník, T., Faigl, J., Vonásek, V., Košnar, K., Kulich, M., & Přeučil, L. (2010). *Simple yet stable bearing-only navigation*. Journal of Field Robotics, 27(5), 511–533. https://doi.org/10.1002/rob.20354 — bearing-only map-and-replay with odometric segment endpoints.
- Krajník, T., Majer, F., Halodová, L., & Vintr, T. (2017). *Navigation without localisation: reliable teach and repeat based on the convergence theorem*. arXiv. https://arxiv.org/abs/1711.05348 — replays learned velocities and uses the camera to correct heading.
- Dall'Osto, D., Fischer, T., & Milford, M. (2020). *Fast and Robust Bio-inspired Teach and Repeat Navigation*. arXiv. https://arxiv.org/abs/2010.11326 — an odometry-driven, asynchronous teach-and-repeat formulation.
- Rozsypálek, Z., Rouček, T., Vintr, T., & Krajník, T. (2023). *Multidimensional Particle Filter for Long-Term Visual Teach and Repeat in Changing Environments*. IEEE Robotics and Automation Letters, 8(4), 1951–1958. https://doi.org/10.1109/LRA.2023.3244418 — a filter for long-term repeats across changing conditions.
