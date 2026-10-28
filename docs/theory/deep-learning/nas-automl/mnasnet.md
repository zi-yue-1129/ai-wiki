---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/nas-automl
tags:
  - neural architecture search
  - hardware-aware design
  - mobile networks
aliases:
  - MnasNet
  - Platform-aware neural architecture search
  - 行動端平台感知架構搜尋
---

# MnasNet: platform-aware architecture search (Tan et al., 2019)

MnasNet searches for mobile image classifiers with a reward that combines accuracy with latency measured on a real phone, rather than with a proxy such as FLOPS. Its search space is factorised into blocks, so that layers in different parts of the network can differ. Part of [Neural architecture search](index.md).

## Overview

Mobile networks have to be small and fast as well as accurate, and the trade-off is hard to balance by hand. Earlier architecture search used a cost proxy such as the number of multiply–adds, which is often a poor predictor of speed on a phone. Tan, Chen, Pang, Vasudevan, Sandler, Howard and Le (2019) put the measured inference latency on a target phone directly into the search objective. They also propose a search space that allows layers in different parts of a network to differ, to encourage layer diversity.

## Key concepts

- **Latency**: the measured time of one inference on the target phone, not a proxy.
- **Reward**: the score that drives the controller, combining accuracy with a latency penalty.
- **Factorised hierarchical search space**: a network split into blocks, where each block has its own choice of layers.
- **Target latency**: the latency budget that the reward penalises when a candidate exceeds it.

## Problem

How can an architecture search find a mobile classifier that gives a good accuracy–latency trade-off on a real device, when the latency of a model cannot be read off its operation count?

## How it works

A reinforcement-learning controller samples a candidate architecture from the search space. The candidate is trained, its accuracy is measured on the validation set, and its latency is measured by running it on a phone. The reward combines the two as a weighted product,

\[
\mathrm{reward}(m) = \mathrm{ACC}(m) \times \left[\frac{\mathrm{LAT}(m)}{T}\right]^{w},
\]

where \(\mathrm{LAT}(m)\) is the measured latency, \(T\) is the target latency and \(w\) is an exponent that controls how strongly latency is penalised. The controller is updated to increase the expected reward.

## Key methods

This page covers one method: a reinforcement-learning search whose reward is accuracy times a latency ratio, measured on a phone, over a factorised block-based search space.

1. Sample a candidate from the factorised search space.
2. Train it and measure its validation accuracy.
3. Measure its latency on the target phone.
4. Compute the reward and update the controller.

## Variants

- **Strength of the latency penalty**: the exponent \(w\) sets how strongly latency is penalised, from a gentle trade-off to a near-hard constraint.
- **Other target devices** change the latency measurement, and so the models that the search finds.
- **Transfer to other tasks**: the architectures found for classification are reused for object detection in the paper.

## Results and limits

- On ImageNet, Tan et al. (2019) report a top-1 accuracy of 75.2% with 78 ms latency on a Pixel phone. They describe this as 1.8 times faster than MobileNetV2 with 0.5% higher accuracy, and 2.3 times faster than NASNet with 1.2% higher accuracy.
- The paper reports better mAP than MobileNets for COCO object detection.
- Latency is measured on one phone, so the best architecture can change with the device.
- The reward depends on the choice of target latency and exponent, and a poor choice can favour an architecture that is fast on paper but not in practice.

## Applications

- **Mobile image classification**, where the device latency is a hard requirement.
- **Edge deployment** of vision models on hardware with a known latency profile.
- **Object detection backbones**, using the architectures found for classification.

## Open questions

- How well do architectures tuned for one phone transfer to other hardware, or to future hardware?
- Can latency be predicted accurately enough to avoid measuring every candidate on a device?

## Connections

- Parent topic: [Neural architecture search](index.md)
- Differentiable alternative: [DARTS](darts.md)
- Reinforcement-learning search it builds on: Zoph and Le (2017), cited on the [parent page](index.md)

## References

### Seminal papers

- Tan, M., Chen, B., Pang, R., Vasudevan, V., Sandler, M., Howard, A. & Le, Q. V. (2019). MnasNet: Platform-Aware Neural Architecture Search for Mobile. In *CVPR 2019*. arXiv:1807.11626. https://arxiv.org/abs/1807.11626 — Puts measured phone latency into the reward for architecture search, and reports accuracy–latency results on ImageNet.
- Sandler, M., Howard, A., Zhu, M., Zhmoginov, A. & Chen, L.-C. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks. In *CVPR 2018*. arXiv:1801.04381. https://arxiv.org/abs/1801.04381 — The hand-designed mobile baseline against which MnasNet reports its speed-up.
- Zoph, B., Vasudevan, V., Shlens, J. & Le, Q. V. (2018). Learning Transferable Architectures for Scalable Image Recognition. In *CVPR 2018*. arXiv:1707.07012. https://arxiv.org/abs/1707.07012 — The NASNet search space and model, the second baseline in the MnasNet comparison.
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — The reinforcement-learning search that MnasNet extends with a latency-aware reward.

### Surveys and textbooks

- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — Survey that places hardware-aware search among the search objectives.
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — Differentiable alternative that does not measure latency in its search.
- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V. (2019). Regularized Evolution for Image Classifier Architecture Search. In *Proceedings of the AAAI Conference on Artificial Intelligence* 33, 4780–4789. https://doi.org/10.1609/aaai.v33i01.33014780 — Evolutionary alternative whose objective is accuracy alone.
