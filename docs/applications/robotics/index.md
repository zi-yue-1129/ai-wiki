---
related:
- models/world-models
- foundations/paradigms/imitation
- foundations/paradigms/reinforcement-learning
- applications/manufacturing
- applications/autonomous-driving
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

## Learning-based robotics

| Approach | Examples |
|---|---|
| Reinforcement learning in simulation + sim-to-real | Legged locomotion (ANYmal, Unitree), dexterous in-hand manipulation (OpenAI's Rubik's cube, 2019), drone racing beating human champions (Kaufmann et al., 2023) |
| Imitation learning from teleoperation | ALOHA, Diffusion Policy, ACT — see [Imitation Learning](../../foundations/paradigms/imitation/index.md) |
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
