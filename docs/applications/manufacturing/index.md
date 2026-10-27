---
related:
- models/computer-vision
- applications/robotics
- engineering/hardware
- brain-mind/snn-neuromorphic
---

# Manufacturing & Industry

## Landscape

| Area | Methods | Value |
|---|---|---|
| Visual quality inspection | CNNs, anomaly detection (PatchCore, PaDiM), few-shot defect detection | Detect scratches, cracks, misalignments faster and more consistently |
| Predictive maintenance | Time-series models on vibration, temperature, current; remaining-useful-life estimation | Reduce unplanned downtime |
| Process optimisation | Bayesian optimisation, RL, surrogate models of processes | Yield, energy, throughput |
| Digital twins | Simulation models synchronised with sensor data | What-if analysis, virtual commissioning |
| Supply chain and planning | Demand forecasting, inventory optimisation, scheduling | Resilience and cost |
| Robotics and automation | Flexible picking, assembly, collaborative robots | See [Robotics](../robotics/index.md) |
| Generative design | Topology optimisation, generative CAD | Lighter, stronger parts |
| Knowledge capture | LLM assistants over manuals, maintenance logs, SOPs | Reduce dependence on retiring experts |

## Semiconductors and electronics

- **Chip design**: RL-assisted floorplanning (Mirhoseini et al., 2021 — and the subsequent debate over its claims), ML-driven EDA tools for placement, routing and verification; LLMs generating RTL
- **Fab yield**: wafer-map defect classification, virtual metrology, process-control models
- **Lithography**: computational lithography accelerated with GPUs and ML

## Practical challenges

- **Few defect examples**: defects are rare → unsupervised anomaly detection, synthetic data, few-shot methods
- **Domain shift**: new product lines, lighting, sensor changes
- **Edge deployment**: real-time inference on factory hardware; low-power options include [neuromorphic and spiking approaches](../../brain-mind/snn-neuromorphic/index.md)
- **Data silos and OT/IT integration**
- **Explainability for operators** and safety certification

## Resources

- MVTec Anomaly Detection dataset (MVTec AD)
- NASA C-MAPSS turbofan degradation dataset; PHM Society data challenges
- Lee et al., industrial AI and cyber-physical systems literature
- [anomalib](https://github.com/openvinotoolkit/anomalib) open-source library
