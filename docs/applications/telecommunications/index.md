---
related:
- theory/paradigms/unsupervised/autoencoders-and-representations
- theory/paradigms/reinforcement-learning
- theory/paradigms/federated
- engineering/on-device-edge
aliases:
  - 電信
  - 通訊
  - Telecom
---

# Telecommunications

Telecom networks are large, real-time systems that carry traffic, adapt radio resources every few milliseconds and are operated by people who need to understand every fault. AI is used at three layers: the radio physical layer (signal processing), network management (scheduling, planning and fault detection), and customer-facing and operational knowledge work. The most mature uses are in network operations; the physical-layer work is largely at research stage.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Physical layer | Neural receivers, channel estimation, end-to-end learned communication | Research-stage; compared against well-understood signal processing |
| Radio resource management | Reinforcement learning for power, spectrum and scheduling decisions | Promising in simulation; hard to validate on live networks |
| Traffic and mobility prediction | Time-series and graph models over base-station and user data | Used for capacity planning and energy saving |
| Fault and anomaly detection | Unsupervised detection on alarms, KPIs and logs | Reduces alarm floods; false positives matter |
| Self-organising networks | Automated tuning of base-station parameters | Standardised in mobile networks, with safety limits |
| Edge intelligence | Splitting model training and inference between devices and edge servers | Driven by latency and privacy requirements |
| Customer service and operations knowledge | Language models over standards, manuals and tickets | Telecom questions need precise, up-to-date answers |

## Why telecom is demanding

- **Hard real-time limits.** Decisions must be made within milliseconds, which pushes models onto devices or edge servers.
- **Strict reliability.** A mistake can take down service for many users, so changes need safe rollout and rollback.
- **Standards.** Many interfaces are defined by standards bodies, which shapes what can be deployed and how it is tested.
- **Heterogeneous data.** Logs, alarms, radio measurements and billing records come in different formats and rates.

## Key methods

Four method families cover most of the field. Each links to the page that explains it.

- [Autoencoders and learned representations](../../theory/paradigms/unsupervised/autoencoders-and-representations/index.md): learning a compact representation of signals, the idea behind end-to-end learned communication (O'Shea & Hoydis, 2017).
- [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md): sequential decisions for scheduling and resource allocation, first shown for cluster scheduling by Mao et al. (2016).
- [Federated learning](../../theory/paradigms/federated/index.md): training across many devices or base stations without moving raw data to one place.
- [Large language models](../../theory/models/llm/index.md): answering questions over standards and operational documents; TeleQnA (Maatouk et al., 2023) is a benchmark for this.

## Connections

Edge deployment of models is covered in [On-Device & Edge AI](../../engineering/on-device-edge/index.md). The fault-detection side uses [Anomaly Detection](../../theory/paradigms/unsupervised/anomaly-detection/index.md), and the shared network with cybersecurity is covered in [Cybersecurity](../cybersecurity/index.md).

## Applications

- Predicting traffic and adjusting base-station settings to save energy at quiet hours.
- Detecting faults from alarm and performance data so that operators see the likely root cause, not hundreds of separate alarms.
- Learned receivers and channel estimators tested against classical designs in simulation.
- Question-answering assistants for engineers, grounded in standards and internal documentation.

## Open questions

- Can learned physical-layer components be shown to be as reliable as classical designs under all conditions they will face?
- How should reinforcement-learning controllers be tested safely on live networks?
- Can language models stay accurate as standards change, without frequent retraining?
- How should data from many operators be shared for training without exposing commercial information?

## References

### Seminal papers

- O'Shea, T. & Hoydis, J. (2017). An Introduction to Deep Learning for the Physical Layer. *IEEE Transactions on Cognitive Communications and Networking*. https://doi.org/10.1109/TCCN.2017.2758370 — Shows that an autoencoder can learn a communication system end to end, with transmitter and receiver as one neural network.
- Mao, H., Alizadeh, M., Menache, I. & Kandula, S. (2016). Resource Management with Deep Reinforcement Learning. *Proceedings of the 15th ACM Workshop on Hot Topics in Networks*. https://doi.org/10.1145/3005745.3005750 — Applies deep reinforcement learning to scheduling and resource allocation in computer clusters, an early template for network control.
- Maatouk, A., Ayed, F., Piovesan, N., De Domenico, A., Debbah, M. & Luo, Z.-Q. (2023). TeleQnA: A Benchmark Dataset to Assess Large Language Models Telecommunications Knowledge. arXiv. https://arxiv.org/abs/2310.15051 — A benchmark of telecommunications questions for testing the knowledge of large language models.

### Surveys and textbooks

- Zhang, C., Patras, P. & Haddadi, H. (2019). Deep Learning in Mobile and Wireless Networking: A Survey. *IEEE Communications Surveys & Tutorials*. https://doi.org/10.1109/COMST.2019.2904897 — A survey of deep learning across mobile and wireless networking tasks, including traffic, mobility and resource allocation.
- Qin, Z., Ye, H., Li, G. Y. & Juang, B.-H. F. (2019). Deep Learning in Physical Layer Communications. *IEEE Wireless Communications*. https://doi.org/10.1109/MWC.2019.1800601 — Reviews deep learning for physical-layer tasks such as channel estimation, signal detection and decoding.

### Articles and documentation

- Zhou, Z., Chen, X., Li, E., Zeng, L., Luo, K. & Zhang, J. (2019). Edge Intelligence: Paving the Last Mile of Artificial Intelligence With Edge Computing. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2019.2918951 — Surveys how model training and inference are split between devices and edge servers.
