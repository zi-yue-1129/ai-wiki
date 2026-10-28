---
related:
- applications/robotics
- foundations/paradigms/reinforcement-learning/index.md
tags:
  - transfer learning
  - sim-to-real
  - domain randomisation
---

# Sim-to-real Transfer

Sim-to-real transfer trains a model in simulation, where data is cheap and safe to collect, and then runs it in the physical world. The gap between simulated and real sensors and dynamics usually makes the transferred model fail, so most sim-to-real methods focus on making the model robust to that gap.

## Overview

Simulation is an approximation. Visual appearance, contact physics, actuator delays and sensor noise all differ from the real world. Methods either make the simulator more realistic, adapt the model to the real domain, or randomise the simulator so widely that the real world looks like one more sample.

## Methods

- **Domain randomisation**: vary textures, lighting and camera pose during training so that the policy or detector learns features that hold across variations (Tobin et al., 2017).
- **Dynamics randomisation**: vary masses, friction and motor parameters so that a control policy learns to adapt to unknown real dynamics (Peng et al., 2018).
- **Real-to-sim and system identification**: measure the real system and tune the simulator to match it, reducing the gap before training.
- **Domain adaptation**: align features between simulated and real images, as in [domain adaptation](../domain-adaptation/index.md).

## Connections

Sim-to-real is most common in [reinforcement learning](../../reinforcement-learning/index.md), where policies need many trials that would be unsafe on hardware. It also depends on the adaptation methods in [domain adaptation](../domain-adaptation/index.md). Robotics applications are described in [robotics](../../../../applications/robotics/index.md).

## Applications

Quadruped and humanoid locomotion, dexterous in-hand manipulation, drone flight from rendered images, and industrial inspection with synthetic training data.

## Open questions

Randomisation can make policies overly conservative, and it is hard to know which parameters to randomise. Real-world evaluation remains expensive, and simulators are still poor models of deformable objects and fine contact.

## References

### Seminal papers

- Tobin, Fong, Ray, Schneider, Zaremba & Abbeel (2017), "Domain randomization for transferring deep neural networks from simulation to the real world", IROS, arXiv:1703.06907 — Randomises rendering in simulation so that real images look like one more training sample.
- Peng, Andrychowicz, Zaremba & Abbeel (2018), "Sim-to-real transfer of robotic control with dynamics randomization", ICRA, arXiv:1710.06537 — Randomises physical parameters so that a control policy adapts to unknown real dynamics.
- Sadeghi & Levine (2017), "CAD2RL: real single-image flight without a single real image", RSS, arXiv:1611.04201 — Trains drone flight policies entirely in rendered CAD scenes and flies them in the real world.
- Tan et al. (2018), "Sim-to-real: learning agile locomotion for quadruped robots", RSS, arXiv:1804.10332 — Quadruped locomotion learned in simulation with actuator modelling, transferred to hardware.

### Surveys and textbooks

- Zhao, Queralta & Westerlund (2020), "Sim-to-real transfer in deep reinforcement learning for robotics: a survey", arXiv:2009.13303 — Survey of methods for closing the simulation gap in deep RL for robots.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Rusu et al. (2017), "Sim-to-real robot learning from pixels with progressive nets", CoRL. No link checked.
