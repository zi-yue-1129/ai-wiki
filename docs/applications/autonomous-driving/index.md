---
related:
- models/computer-vision
- models/world-models
- foundations/paradigms/imitation
- applications/robotics
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
