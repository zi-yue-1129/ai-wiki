---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 手眼協調
  - Hand-eye coordination
---

# Hand-Eye Coordination for Grasping (Levine et al. 2016)

Levine and colleagues asked whether a robot can learn hand-eye coordination for grasping from raw monocular images, without camera calibration or a known robot pose. The network learns from a very large set of real grasp attempts. This page covers one paper; the parent topic is [Robotics](../index.md).

## Problem

Robotic grasping has usually depended on calibrated cameras and a known robot pose. The question was whether the link between what the camera sees and where the gripper should move could be learned directly from data.

## Core idea

A large convolutional network estimates how likely a proposed gripper motion is to produce a successful grasp. It uses only the camera image, so it needs no calibration and no knowledge of the current robot pose. The trained network then guides the gripper in real time, correcting its motion from the camera.

## Procedure

1. Collect grasp attempts from several robot arms running in parallel, recording each image, the proposed motion and whether the grasp succeeded.
2. Train a convolutional network to predict grasp success from the image and the proposed motion.
3. During execution, use the network to servo the gripper, choosing motions that the network scores as most likely to succeed.

## Results

The training data came from more than 800,000 grasp attempts collected over two months, on between 6 and 14 robot arms that differed in camera placement and hardware. The summary of the paper that we checked reports real-time control, grasping of objects the network was not trained on, and correction of errors through continuous adjustment. It does not give a grasp success rate, so that number needs the full paper.

## Limitations

- The method depends on a very large, costly dataset that few groups can collect.
- The results are for the authors' robot arms and cameras. The abstract does not show transfer to a different robot.
- Methods that avoid collecting real data by training in simulation are covered by the domain randomization work in the references.

## Connections

- The same idea of learning control from raw images appears in autonomous driving, see [End-to-end steering from pixels](../../autonomous-driving/end-to-end-steering/index.md).
- Reinforcement learning for grasping is covered in [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).

## References

### Seminal papers

- Levine, S. et al. (2016). Learning Hand-Eye Coordination for Robotic Grasping with Deep Learning and Large-Scale Data Collection. arXiv. https://arxiv.org/abs/1603.02199 — Predicts grasp success from monocular images and servos the gripper, trained on over 800,000 grasp attempts.
- Levine, S., Finn, C., Darrell, T. & Abbeel, P. (2015). End-to-End Training of Deep Visuomotor Policies. arXiv. https://arxiv.org/abs/1504.00702 — Trains convolutional policies that map raw camera images to motor torques, learning perception and control together.
- Pinto, L. & Gupta, A. (2015). Supersizing Self-supervision: Learning to Grasp from 50K Tries and 700 Robot Hours. arXiv. https://arxiv.org/abs/1509.06825 — Self-supervised grasp learning from about 50,000 trials, which predicts grasp locations from image patches.
- Tobin, J. et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World. arXiv. https://arxiv.org/abs/1703.06907 — Object detectors trained on randomised simulated images transfer to real objects and enable grasping in clutter.
- Kalashnikov, D. et al. (2018). QT-Opt: Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation. arXiv. https://arxiv.org/abs/1806.10293 — Self-supervised reinforcement learning for vision-based grasping, trained on over 580,000 real grasp attempts.
