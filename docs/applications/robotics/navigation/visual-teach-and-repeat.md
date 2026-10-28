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

The stored route is a chain of local submaps or keyframes, each linked to the next by a relative transform. The robot localises itself against the nearest submap and tracks the path with a controller that uses the lateral and heading error from the current view. Because the error is measured relative to the stored map, the method does not need GPS or a global frame.

## Problem

A route can be long, and the environment changes between the teaching run and the repeat. The robot must follow the taught path accurately, keep its position estimate from drifting, and cope with changes in lighting and appearance. These demands were the reason for topometric maps: they keep the local error small without requiring a globally consistent metric map.

## Core idea

Localise relative to the teach data and steer using a signed error. Furgale and Barfoot localise against overlapping submaps and control the robot with a path tracker on the metric lateral and heading errors. Krajník and colleagues take a simpler route: they replay the taught velocities indexed by distance travelled, and use the image only to correct heading.

## How it works

1. During teaching, record images and relative motion along the route, and build local submaps or a chain of keyframes.
2. During repeat, estimate the robot's position relative to the nearest stored submap, using feature matching.
3. Compute the lateral and heading error, and steer to reduce them.
4. In the replay variant, follow the taught motion profile by distance, and apply a correction from the image-based heading estimate.

## Results

Furgale and Barfoot report long-range field trials on a rover, with autonomous repeats over many kilometres and without GPS. Krajník et al. (2010) report bearing-only navigation over more than a kilometre with a mean position error below 0.3 m on their trials. Krajník et al. (2018) report that visual heading correction alone could not follow sharp turns, because features left the field of view, and that replaying the taught motion together with the visual correction converged on the path. The figures should be checked in the papers before reuse.

## Limitations

- Odometry drift grows with distance, so systems rely on a reliable distance estimate to decide when to turn.
- Image features can be lost on sharp turns or in featureless areas, which is why replay with a motion profile is often combined with vision.
- A single traversal stores one appearance. Long-term use across lighting and season needs multi-session or learned image registration, as in Rozsypálek et al. (2023).

## Connections

- [Navigation with Visual Goals](index.md) places teach-and-repeat next to learned image-goal navigation.
- [SPTM](sptm.md) is a learned topological alternative that replaces the odometric tracker with a network.
- [Robotics](../index.md) covers the wider estimation and control problems behind the local localisation step.

## Open questions

- How teach-and-repeat should handle changes in the environment that happen between the teach and repeat runs, beyond small appearance changes.
- Whether learned image registration can match the accuracy of geometric localisation on very long routes.

## References

- Furgale, P., & Barfoot, T. D. (2010). *Visual teach and repeat for long-range rover autonomy*. Journal of Field Robotics, 27(5), 534–560. https://doi.org/10.1002/rob.20342 — the canonical topometric teach-and-repeat system, built on odometry and submaps.
- Krajník, T., Faigl, J., Vonásek, V., Košnar, K., Kulich, M., & Přeučil, L. (2010). *Simple yet stable bearing-only navigation*. Journal of Field Robotics, 27(5), 511–533. https://doi.org/10.1002/rob.20354 — bearing-only map-and-replay with odometric segment ends.
- Krajník, T., Majer, F., Halodová, L., & Vintr, T. (2018). *Navigation without localisation: Reliable teach and repeat based on the convergence theorem*. IROS 2018. arXiv:1711.05348. https://arxiv.org/abs/1711.05348 — replays a taught motion profile and corrects it with vision.
- Dall'Osto, D., Fischer, T., & Milford, M. (2021). *Fast and robust bio-inspired teach and repeat navigation*. IROS 2021. arXiv:2010.11326. https://arxiv.org/abs/2010.11326 — odometry-driven teach-and-repeat with separate orientation and along-path corrections.
- Rozsypálek, Z., Rouček, T., Vintr, T., & Krajník, T. (2023). *Multidimensional particle filter for long-term visual teach and repeat in changing environments*. IEEE Robotics and Automation Letters, 8, 1951–1958. https://doi.org/10.1109/LRA.2023.3244418 — joint filtering of distance, lateral offset and heading across changing conditions.
