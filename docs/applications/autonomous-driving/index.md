---
related:
- theory/models/computer-vision
- theory/models/world-models
- theory/paradigms/imitation
- applications/robotics
aliases:
  - 自動駕駛
  - 自駕車
  - Autonomous driving
---

# Autonomous Driving & Transport

## SAE levels of driving automation

| Level | Name | Who drives |
|---|---|---|
| 0 | No automation | Human |
| 1 | Driver assistance (adaptive cruise *or* lane keeping) | Human, with help |
| 2 | Partial automation (both together) | Human must supervise constantly |
| 3 | Conditional automation | System, in limited conditions; human must take over on request |
| 4 | High automation | System, within a defined operational design domain (ODD); no human fallback needed |
| 5 | Full automation | System, everywhere |

## State of the field (2026)

- **Robotaxis (Level 4)**: Waymo operates fully driverless paid service in several US cities and has driven well over 100 million rider-only miles; Baidu Apollo Go, Pony.ai and WeRide operate large driverless fleets in China; others are expanding in the Middle East and elsewhere
- **Safety data**: Waymo's peer-reviewed comparisons report substantially fewer injury-causing crashes than human benchmarks in the same areas (e.g. Kusano et al., 2024–2025)
- **Level 2/2+ driver assistance** is widespread (Tesla FSD (Supervised), GM Super Cruise, Mobileye, Chinese automakers' highway and urban navigation-on-autopilot systems)
- **Trucking and logistics**: driverless trucking pilots on highways (e.g. Aurora in Texas, 2025)
- Setbacks: Cruise halted operations after a 2023 pedestrian-dragging incident and was later wound down by GM

## Key methods

### End-to-end steering from pixels (Bojarski et al. 2016)

- **Problem:** Self-driving systems have usually been built from separate perception, planning and control modules, each designed by hand. Can one network learn to drive directly from raw camera pixels, using recordings of human driving as its only supervision?
- **Core idea:** A convolutional network takes the image from one front-facing camera and outputs a steering command. It is trained on recordings of a human driver, so the link between the scene and the steering is learned rather than programmed.
- **Equation or algorithm:**
  1. Record front-camera images together with the steering angle the human driver used.
  2. Train a convolutional network to predict the steering command from each image.
  3. Run the trained network in the car, setting steering from the live camera feed.
- **Results:** The abstract reports that the system learns to drive on local roads with or without lane markings, on highways, in parking lots and on unpaved roads, and that it operates at 30 frames per second. It gives no safety or error-rate figures, so those need the full paper.
- **Limitations:** The abstract does not explain why the network chooses a given steering command, which limits how it can be checked. Learning from human driving also means the system can copy human errors. The later papers in the references below address route commands, reinforcement learning and simulated testing.

## Technical approaches

| Approach | Description |
|---|---|
| Modular pipeline | Perception → prediction → planning → control, with HD maps; interpretable, dominant in robotaxis |
| End-to-end learning | Neural network maps sensors to trajectory, trained largely by imitation of human driving |
| Hybrid | Learned components plus rule-based safety layers |
| Sensor choice | Camera-only vs camera + radar + LiDAR fusion |
| Simulation and world models | Generate rare and dangerous scenarios; closed-loop testing |

Key AI components: 3D object detection, bird's-eye-view (BEV) representations, occupancy networks, motion forecasting of other agents, behaviour planning, and vision-language models for reasoning about unusual situations.

## The long tail

The hardest problems are rare events: unusual objects, emergency vehicles, construction zones, ambiguous human gestures, adverse weather. Validation requires billions of miles of equivalent evidence, so simulation, scenario-based testing and safety cases (ISO 26262, ISO 21448 SOTIF, UL 4600) are essential.

## Beyond cars

- Traffic signal optimisation and congestion prediction
- Route optimisation and fleet management (vehicle routing problems)
- Railway and aviation: predictive maintenance, air-traffic flow, autopilots
- Maritime autonomy and drone delivery

## Human factors

Level 2 and 3 systems create **automation complacency**: drivers disengage attention yet must intervene in seconds. Investigations by the NTSB into fatal crashes have repeatedly cited over-reliance and inadequate driver monitoring.

## Resources

- Waymo, Mobileye and Aurora safety reports
- [nuScenes](https://www.nuscenes.org/), [Waymo Open Dataset](https://waymo.com/open/), [Argoverse](https://www.argoverse.org/)
- [CARLA](https://carla.org/) simulator, [nuPlan](https://www.nuscenes.org/nuplan)
- Koopman, *How Safe Is Safe Enough?*

## References

### Seminal papers

- Bojarski, M. et al. (2016). End to End Learning for Self-Driving Cars. arXiv. https://arxiv.org/abs/1604.07316 — A convolutional network maps pixels from one front camera to steering commands, trained on human driving data.
- Codevilla, F. et al. (2018). End-to-end Driving via Conditional Imitation Learning. arXiv. https://arxiv.org/abs/1710.02410 — Conditions an imitation-learned driving policy on high-level commands, such as which turn to take at an intersection.
- Kendall, A. et al. (2018). Learning to Drive in a Day. arXiv. https://arxiv.org/abs/1807.00412 — Deep reinforcement learning for lane following, learning on a real vehicle from a single monocular camera in a few episodes.
- Bansal, M., Krizhevsky, A. & Ogale, A. (2018). ChauffeurNet: Learning to Drive by Imitating the Best and Synthesizing the Worst. arXiv. https://arxiv.org/abs/1812.03079 — Imitation learning made more robust with synthesised perturbations and penalties for collisions.

### Articles and documentation

- Dosovitskiy, A. et al. (2017). CARLA: An Open Urban Driving Simulator. arXiv. https://arxiv.org/abs/1711.03938 — An open simulator with city layouts, vehicles and configurable sensors, for training and testing driving systems.
