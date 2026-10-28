---
status: draft
last_reviewed: 2026-10-28
tags:
  - architecture
  - efficient inference
  - search
aliases:
  - MnasNet
  - Platform-Aware NAS
  - Hardware-aware neural architecture search
  - 平台感知神經架構搜尋
---

# MnasNet: Platform-Aware Neural Architecture Search (Tan et al., 2018)

MnasNet, by Tan et al. (2018), searches for mobile convolutional networks with a reward that includes the latency measured on a real phone, rather than a proxy such as the number of multiply-adds. It is one of the clearest examples of [hardware-aware neural architecture search](../index.md), and its search space was reused for the baseline of [EfficientNet](../../../models/cnn/backbones-and-scaling/efficientnet/index.md).

## Overview

Mobile vision models must be small, fast and accurate, and balancing these trade-offs by hand is difficult. Earlier search methods often used a proxy for speed, usually FLOPS, which is only loosely related to real inference time on a phone. Tan et al. measured latency directly on a phone and built that measurement into the search objective.

The result, MnasNet-A1, reached 75.2% top-1 accuracy on ImageNet at 78 ms per image on a Pixel 1 phone, with 3.9M parameters and 312M multiply-adds (Table 1 of the paper).

## Key concepts

- **Factorised hierarchical search space.** The network is divided into blocks with fixed input resolutions and filter sizes. Within each block the search chooses the operations and connections of one layer and how many times it repeats, so early and late blocks can differ.
- **Measured latency.** Each sampled model runs on the big CPU core of a Pixel 1 phone, with batch size one, to measure its latency.
- **Weighted product objective.** Accuracy and latency are combined in one score. The authors chose this over a hard constraint because it is easy to customise and gives a range of trade-offs.
- **Pareto front.** One search yields several models along the accuracy and latency frontier. MnasNet-A2 and MnasNet-A3 come from the same search at different latencies.

## How it works

The search uses a recurrent controller trained with proximal policy optimisation (PPO), in four stages.

1. **Sample.** The controller predicts a sequence of tokens that specifies a model in the factorised space.
2. **Train and measure.** The model is trained on the target task with a shortened schedule, which gives its accuracy \(\mathrm{ACC}(m)\). Its latency \(\mathrm{LAT}(m)\) is measured on the phone.
3. **Reward.** The reward is

\[
\text{maximise} \quad \mathrm{ACC}(m) \times \left(\frac{\mathrm{LAT}(m)}{T}\right)^{w}, \qquad w = \begin{cases} \alpha, & \mathrm{LAT}(m) \le T \\ \beta, & \mathrm{LAT}(m) > T \end{cases}
\]

where \(T\) is the target latency. The paper uses \(T = 75\) ms and \(\alpha = \beta = -0.07\). With equal exponents, the penalty for exceeding the target is smooth rather than a hard cut-off, so the controller treats the target as a soft constraint.

4. **Update.** The controller is updated with PPO to maximise the expected reward, and the loop repeats.

The search sampled about 8,000 models and took 4.5 days on 64 TPUv2 devices. The top 15 were then trained on full ImageNet.

## Results

The models in Table 1 of the paper compare as follows on ImageNet.

| Model | Search | Parameters | Mult-adds | Top-1 | Latency (Pixel 1) |
|---|---|---|---|---|---|
| MobileNetV2 (1.4×) | manual | 6.9M | 585M | 74.7% | 143 ms |
| AmoebaNet-A | automated | 5.1M | 555M | 74.5% | 190 ms |
| MnasNet-A1 | automated | 3.9M | 312M | 75.2% | 78 ms |
| MnasNet-A3 | automated | 5.2M | 403M | 76.7% | 103 ms |

MnasNet-A1 is more than twice as fast as the searched AmoebaNet-A in the table, and more accurate than the hand-designed MobileNetV2 at roughly half its latency. MnasNet-A3, from the same search, is the most accurate model shown, at 103 ms. The paper also compares a hard latency constraint with the soft one used here. The hard version concentrates the search on models faster than the target, while the soft version samples a range of latencies and yields several Pareto models.

## Limitations

- **One device.** Latency was measured on a single phone model. The search is tuned to that device, and a model that is fast on one device may not be fast on another.
- **Search cost.** Measuring every sampled model on a phone is slow, and the search still needed 4.5 days on 64 accelerators.
- **Hand-set trade-off.** The exponents \(\alpha\) and \(\beta\) are chosen by the authors, so the preference between accuracy and speed is not learned by the search.

## Open questions

- **Proxy latency.** How well do latency measurements transfer between phones and accelerators? EfficientNet's search reused the space but optimised FLOPS, so the two papers answer different questions about speed.
- **Cheaper search.** Can latency be predicted from a model's structure, so that the phone need not run each candidate? This would cut cost but add a source of error.
- **Reward design.** Is a single weighted product the right way to combine accuracy and speed? The paper argues that it is practical.

## References

### Seminal papers

- Tan, M., et al. (2018). *MnasNet: Platform-Aware Neural Architecture Search for Mobile*. arXiv:1807.11626. https://arxiv.org/abs/1807.11626 — The paper itself: a reward that includes phone latency, producing mobile CNNs that trade accuracy against speed.
- Tan, M. & Le, Q. V. (2019). *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*. arXiv:1905.11946. https://arxiv.org/abs/1905.11946 — Reuses the MnasNet search space for a baseline network, then scales it with a compound rule.
- Zoph, B. & Le, Q. V. (2016). *Neural Architecture Search with Reinforcement Learning*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — The RNN controller trained with reinforcement learning, the ancestor of MnasNet's controller.

### Surveys and textbooks

- Elsken, T., Metzen, J. H. & Hutter, F. (2018). *Neural Architecture Search: A Survey*. arXiv:1808.05377. https://arxiv.org/abs/1808.05377 — Organises NAS by search space, search strategy and performance estimation.

### Articles and documentation

- Yang, A., Esperança, P. M. & Carlucci, F. M. (2019). *NAS evaluation is frustratingly hard*. arXiv:1912.12522. https://arxiv.org/abs/1912.12522 — Argues that NAS results are hard to compare across protocols, a point that also applies to latency-aware comparisons.
