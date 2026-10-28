---
related:
- theory/models/world-models
- theory/paradigms/imitation
- theory/paradigms/reinforcement-learning
- applications/manufacturing
- applications/autonomous-driving
aliases:
  - 機器人
  - 機器人學
  - Robotics
---

# Robotics

## The classic stack

```mermaid
flowchart LR
  S[Sensors: cameras, LiDAR, force, IMU] --> P[Perception & state estimation]
  P --> M[Mapping & localisation SLAM]
  M --> PL[Task & motion planning]
  PL --> C[Control]
  C --> A[Actuators]
```

Classical robotics uses explicit models: kinematics, dynamics, SLAM, sampling-based planners (RRT, PRM), optimal and model-predictive control. Learning increasingly replaces or augments each block.

## Key methods

One landmark method anchors the learning discussion below. Its full write-up is on its own page.

### Hand-eye coordination for grasping (Levine et al. 2016)

- **Overview:** A convolutional network predicts grasp success from a monocular image and servos the gripper, without calibration. It is trained on over 800,000 grasp attempts.
- **Comparison:** Learns from very large real-world data. The alternative of simulation-based training, which avoids collecting real data, is covered in the references on the method page. The abstract gives no grasp success rate.
- **Full write-up:** [Hand-eye coordination for grasping](hand-eye-grasping/index.md)

## Learning-based robotics

| Approach | Examples |
|---|---|
| Reinforcement learning in simulation + sim-to-real | Legged locomotion (ANYmal, Unitree), dexterous in-hand manipulation (OpenAI's Rubik's cube, 2019), drone racing beating human champions (Kaufmann et al., 2023) |
| Imitation learning from teleoperation | ALOHA, Diffusion Policy, ACT — see [Imitation Learning](../../theory/paradigms/imitation/index.md) |
| Vision-language-action models | RT-2, OpenVLA, π0/π0.5, Gemini Robotics, GR00T |
| LLMs as planners | SayCan, Code as Policies — language models choose and sequence skills |
| World models | Learned dynamics for planning (Dreamer, video world models) |
| Cross-embodiment data | Open X-Embodiment, DROID |

## Domains

| Domain | Status |
|---|---|
| Industrial arms | Mature for structured tasks; AI adds flexibility (bin picking, inspection) |
| Warehouses and logistics | Large fleets of mobile robots; picking remains hard but improving |
| Surgical robots | Teleoperated systems widespread; autonomy research (autonomous suturing, cholecystectomy steps in ex vivo studies) |
| Legged robots | Commercial quadrupeds for inspection |
| Humanoids | Many companies (Figure, Agility, Tesla Optimus, Unitree, UBTech, 1X, Apptronik, Boston Dynamics) piloting in factories and homes; reliability and cost are open questions |
| Agriculture | Harvesting, weeding (see [Agriculture](../agriculture/index.md)) |
| Domestic and assistive | Vacuuming mature; general household manipulation still early |
| Space and field robotics | Planetary rovers, underwater, disaster response |

## Open problems

- **Data scarcity** compared to text and images
- **Generalisation** to new objects, scenes, embodiments
- **Dexterity and touch**: tactile sensing and fine manipulation
- **Long-horizon reliability**: 99% per step isn't enough
- **Safety** around people; certification
- **Evaluation**: real-world benchmarks are hard to reproduce

## Neuroscience links

Motor control research — internal forward and inverse models (cerebellum), optimal feedback control (Todorov & Jordan, 2002), central pattern generators for locomotion, motor synergies — has long informed robotics, and robots are used as physical testbeds for theories of sensorimotor learning.

## Resources

- Lynch & Park, *Modern Robotics* (free online + Coursera)
- Siciliano & Khatib (eds.), *Springer Handbook of Robotics*
- Thrun, Burgard & Fox, *Probabilistic Robotics*
- [MuJoCo](https://mujoco.org/), [Isaac Lab](https://isaac-sim.github.io/IsaacLab/), [ROS 2](https://docs.ros.org/), [LeRobot](https://github.com/huggingface/lerobot)

## References

### Seminal papers

- Levine, S. et al. (2016). Learning Hand-Eye Coordination for Robotic Grasping with Deep Learning and Large-Scale Data Collection. arXiv. https://arxiv.org/abs/1603.02199 — Predicts grasp success from monocular images and servos the gripper, trained on over 800,000 grasp attempts.
- Levine, S., Finn, C., Darrell, T. & Abbeel, P. (2015). End-to-End Training of Deep Visuomotor Policies. arXiv. https://arxiv.org/abs/1504.00702 — Trains convolutional policies that map raw camera images to motor torques, learning perception and control together.
- Pinto, L. & Gupta, A. (2015). Supersizing Self-supervision: Learning to Grasp from 50K Tries and 700 Robot Hours. arXiv. https://arxiv.org/abs/1509.06825 — Self-supervised grasp learning from about 50,000 trials, arguing that scale reduces overfitting.
- Tobin, J. et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World. arXiv. https://arxiv.org/abs/1703.06907 — Detectors trained on randomised simulated images transfer to real objects and grasping.
- Kalashnikov, D. et al. (2018). QT-Opt: Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation. arXiv. https://arxiv.org/abs/1806.10293 — Self-supervised reinforcement learning for vision-based grasping, with over 580,000 real grasp attempts and 96% success on unseen objects.
