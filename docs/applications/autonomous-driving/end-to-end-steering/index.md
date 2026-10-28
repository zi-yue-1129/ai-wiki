---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 端到端駕駛
  - End-to-end driving
---

# End-to-End Steering from Pixels (Bojarski et al. 2016)

Bojarski and colleagues at NVIDIA trained a convolutional network to map pixels from one front-facing camera directly to steering commands. The network learned from recordings of human driving, without hand-designed perception or planning modules. The parent topic is [Autonomous Driving & Transport](../index.md).

## Problem

Self-driving systems were usually built as separate modules for perception, planning and control, each designed by hand. The question was whether one network could learn the whole mapping from raw camera pixels to steering, using human driving as its only supervision.

## Core idea

A convolutional network takes the image from one front-facing camera and outputs a steering command. Because it is trained on a human driver's recordings, the link between the scene and the steering is learned rather than programmed. The paper's claim is that this minimal supervision is enough for the system to drive in a range of settings.

## Procedure

1. Record front-camera images together with the steering angle the human driver used.
2. Train a convolutional network to predict the steering command from each image.
3. Run the trained network in the car, setting steering from the live camera feed.

## Results

The abstract reports that the system learns to drive on local roads with or without lane markings, on highways, in parking lots and on unpaved roads. It reports an operating rate of 30 frames per second. It gives no safety or error-rate figures, so those need the full paper.

## Limitations

- The abstract does not explain why the network chooses a given steering command, which limits how it can be checked.
- Learning from human driving also means the system can copy human errors.
- The network is a single mapping from one camera view. Route commands, learning by trial and error, and testing in simulation are handled by later work, listed below.

## Connections

- The same end-to-end idea is applied to robotic manipulation in [Hand-eye coordination for grasping](../../robotics/hand-eye-grasping/index.md).
- Imitation from human demonstrations is covered in [Imitation Learning](../../../theory/paradigms/imitation/index.md).

## References

### Seminal papers

- Bojarski, M. et al. (2016). End to End Learning for Self-Driving Cars. arXiv. https://arxiv.org/abs/1604.07316 — A convolutional network maps pixels from one front camera to steering commands, trained on human driving data.
- Codevilla, F. et al. (2018). End-to-end Driving via Conditional Imitation Learning. arXiv. https://arxiv.org/abs/1710.02410 — Conditions an imitation-learned driving policy on high-level commands, such as which turn to take at an intersection.
- Kendall, A. et al. (2018). Learning to Drive in a Day. arXiv. https://arxiv.org/abs/1807.00412 — Deep reinforcement learning for lane following, learning on a real vehicle from a single monocular camera in a few episodes.
- Bansal, M., Krizhevsky, A. & Ogale, A. (2018). ChauffeurNet: Learning to Drive by Imitating the Best and Synthesizing the Worst. arXiv. https://arxiv.org/abs/1812.03079 — Imitation learning made more robust with synthesised perturbations and penalties for collisions.

### Articles and documentation

- Dosovitskiy, A. et al. (2017). CARLA: An Open Urban Driving Simulator. arXiv. https://arxiv.org/abs/1711.03938 — An open simulator with city layouts, vehicles and configurable sensors, for training and testing driving systems.
