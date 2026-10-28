---
related:
- theory/models/computer-vision
- applications/robotics
- engineering/hardware
- brain-mind/snn-neuromorphic
aliases:
  - 製造業
  - 工業
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

- **Chip design**: RL-assisted floorplanning (Mirhoseini et al., 2021), ML-driven EDA tools for placement, routing and verification; LLMs generating RTL
- **Fab yield**: wafer-map defect classification, virtual metrology, process-control models
- **Lithography**: computational lithography accelerated with GPUs and ML

## Practical challenges

- **Few defect examples**: defects are rare → unsupervised anomaly detection, synthetic data, few-shot methods
- **Domain shift**: new product lines, lighting, sensor changes
- **Edge deployment**: real-time inference on factory hardware; low-power options include [neuromorphic and spiking approaches](../../brain-mind/snn-neuromorphic/index.md)
- **Data silos and OT/IT integration**
- **Explainability for operators** and safety certification

## Key methods

Three methods are most relevant here. Each links to the page that explains it.

- [Anomaly detection](../../theory/paradigms/unsupervised/anomaly-detection/index.md): PatchCore and PaDiM score defects against the distribution of normal parts, which suits rare defects (Roth et al., 2021; Defard et al., 2020).
- [Residual CNNs](../../theory/models/cnn/backbones-and-scaling/resnet/index.md): backbones for visual quality inspection and defect classification (He et al., 2016).
- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md): the architecture behind LLM assistants over manuals and maintenance logs (Vaswani et al., 2017).

## References

### Seminal papers

- Roth et al. (2021). Towards Total Recall in Industrial Anomaly Detection. arXiv. https://arxiv.org/abs/2106.08265 — PatchCore scores anomalies by comparing patch features with a memory bank of normal patches.
- Defard et al. (2020). PaDiM: a Patch Distribution Modeling Framework for Anomaly Detection and Localization. arXiv. https://arxiv.org/abs/2011.08785 — PaDiM models the distribution of normal patch features for anomaly localisation.
- Bergmann et al. (2019). MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection. CVPR. https://doi.org/10.1109/CVPR.2019.00982 — Benchmark dataset of industrial images for unsupervised defect detection.
- Mirhoseini et al. (2021). A graph placement methodology for fast chip design. *Nature*. https://doi.org/10.1038/s41586-021-03544-w — Reinforcement learning for chip floorplanning, the basis of the chip-design claim above.
- He, K. et al. (2016). Deep Residual Learning for Image Recognition. CVPR. https://doi.org/10.1109/CVPR.2016.90 — Residual connections that make very deep CNNs trainable.
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, built on multi-head self-attention.
