---
related:
  - theory/optimization
  - theory/paradigms/reinforcement-learning
  - applications/autonomous-driving
aliases:
  - 物流
  - 供應鏈
  - 供應鏈管理
---

# Logistics and Supply Chain

Logistics turns forecasts into movement: which goods go where, on which vehicle, at what time, with what stock on hand. AI helps at three levels. It predicts demand and disruption, it solves routing and scheduling problems that are too large for exact methods, and it guides robots and vehicles inside warehouses and ports.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Demand forecasting | Gradient-boosted trees, probabilistic recurrent and transformer forecasters | Forecasts must be probabilistic to drive inventory decisions |
| Inventory and replenishment | Newsvendor-style optimisation with learned demand distributions | Forecast error and lead time both matter |
| Routing and scheduling | Learned construction heuristics, neural combinatorial optimisation, classical solvers with learned components | Vehicle routing, delivery sequencing, crew scheduling |
| Warehouse robotics | Picking and sorting robots, learned grasping, fleet coordination | See [Robotics](../robotics/index.md) |
| Port and freight operations | Berth scheduling, container tracking, customs risk scoring | Often data-sharing limited |
| Resilience and shortage prediction | Network models of supplier dependencies; early-warning signals | Hard to validate until a disruption happens |

## Why it is hard

- **Combinatorial size**: routing and scheduling problems grow faster than any exact method can handle at national scale.
- **Forecasts drive decisions**: a forecast that is accurate on average can still lead to stock-outs in the tails, so calibration matters as much as accuracy.
- **Fragmented data**: suppliers, carriers and warehouses rarely share data in one system.
- **Regime change**: pandemics, strikes and trade rules break historical patterns.

## Key methods

- [Graph neural networks](../../theory/models/gnn/index.md): model supplier and transport networks as graphs, useful for resilience analysis.
- [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md): learns dispatching and inventory policies by trial in simulation, then transfers them to operations.
- [Sim-to-real transfer](../../theory/paradigms/transfer/sim-to-real/index.md): a policy learned in a simulated warehouse or fleet must be adapted before it works on real hardware.
- [Streaming and concept drift](../../theory/paradigms/online/streaming-and-concept-drift/index.md): demand models that keep updating as conditions shift.

## Connections

- The optimisation methods behind routing and scheduling are on the [Optimisation](../../theory/optimization/index.md) page.
- Autonomous vehicles and transport networks are covered in [Autonomous Driving & Transport](../autonomous-driving/index.md).
- Manufacturing planning shares many of the same forecasting and scheduling methods. See [Manufacturing & Industry](../manufacturing/index.md).

## Applications

- Demand forecasting and inventory planning in retail and manufacturing
- Last-mile delivery routing and dispatch
- Warehouse picking and sorting robots
- Port scheduling and container risk screening
- Early warning of supplier shortages

## Risks and limits

- **Brittle optimisation**: solutions tuned to a historical network can fail when a route closes or a supplier stops.
- **Bullwhip effects**: many firms using similar forecasting models can amplify ordering swings.
- **Labour and safety**: automated warehouses change task design and injury profiles, which need monitoring.
- **Benchmarks**: many neural routing results are on synthetic instances; performance on real road networks and constraints can differ.

## Open questions

- How well learned routing heuristics scale to the side constraints (time windows, capacities, regulations) that real operations impose.
- How firms should share data to improve resilience without exposing commercial secrets.

## References

### Seminal papers

- Kool, W., van Hoof, H. & Welling, M. (2019). Attention, Learn to Solve Routing Problems! *ICLR*. https://arxiv.org/abs/1803.08475 — Trains an attention model with reinforcement learning to construct solutions to routing problems, the basis of many neural routing solvers.
- Vinyals, O., Fortunato, M. & Jaitly, N. (2015). Pointer Networks. arXiv. https://arxiv.org/abs/1506.03134 — Introduces a sequence model whose outputs point to input positions, a natural fit for ordering problems such as routing.
- Bello, I. et al. (2016). Neural Combinatorial Optimization with Reinforcement Learning. arXiv. https://arxiv.org/abs/1611.09940 — Learns a neural policy for the travelling salesman problem with reinforcement learning, without hand-designed heuristics.
- Salinas, D. et al. (2020). DeepAR: Probabilistic forecasting with autoregressive recurrent networks. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2019.07.001 — Produces probabilistic demand forecasts across many related time series, a common setting in supply chains.

### Surveys and textbooks

- Bengio, Y., Lodi, A. & Prouvost, A. (2021). Machine learning for combinatorial optimization: A methodological tour d'horizon. *European Journal of Operational Research*. https://doi.org/10.1016/j.ejor.2020.07.063 — Survey of how machine learning is used inside and alongside combinatorial optimisation solvers.
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2021.11.013 — Reports on a large retail demand forecasting competition, comparing statistical and machine learning methods.
