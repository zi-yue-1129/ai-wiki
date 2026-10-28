---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - optimization
  - weight decay
  - scaling
aliases:
  - AdamW weight decay scaling
  - AdamW 權重衰減縮放
---

# Weight Decay Scaling for AdamW

Wang and Aitchison (2024) ask how the AdamW weight decay should change when the model or the dataset grows. Their main finding is that the optimal timescale of the weights, measured in epochs, stays roughly constant as the model and dataset change, so the decay has to rise with model size and fall with dataset size. The parent subtopic is [Weight-Norm Dynamics](index.md), and the optimiser is [AdamW](../adaptive/adamw.md).

## Overview

Under AdamW, the weights behave like an exponential moving average of past updates. The timescale of this average is \(\tau = 1/(\eta\lambda)\) iterations, where \(\eta\) is the learning rate and \(\lambda\) the decay. A large \(\tau\) keeps old updates in the weights, and a small \(\tau\) forgets them quickly. Whether a given \(\tau\) is good depends on how many iterations one epoch takes, so the natural unit for the timescale is the epoch.

## Problem

Practitioners often transfer a decay value from one model or dataset size to another, and the value that worked at one scale can perform poorly at another. The paper asks how the optimal decay scales with model and dataset size, so that a single rule can guide the choice across sizes.

## Core idea

The paper's main finding is that the optimal timescale, measured in epochs, is roughly constant as the model and dataset change. If that holds, the decay follows directly from the learning rate and the number of iterations per epoch. The paper's directions are that the optimal weight decay should increase as the model size grows, and should fall as the dataset size grows.

## How it works

1. Fix a target timescale \(\tau\) in epochs, based on a small-scale sweep.
2. Convert it to iterations, using the number of steps per epoch for the target setting.
3. Set \(\lambda = 1/(\eta \tau_{\text{iters}})\), so that the decay matches the learning rate in use.
4. Check the rule again when the schedule, the learning-rate parameterisation or the training length changes, since the finding was established for the settings studied.

## Results

The paper reports that the optimal timescale, measured in epochs, is roughly constant as the model and dataset size change. It also reports that the optimal decay increases with model size and decreases with dataset size. The sweeps and figures should be checked in the paper before any numeric value is reused.

## Limitations

- The rule is derived from sweeps over a fixed training recipe. It does not establish the optimal timescale for every schedule, and schedules that change \(\eta\) over time, such as warm-up, may change the appropriate \(\tau\).
- The claim that the timescale is constant in epochs is an empirical finding over the settings studied, not a theorem for all architectures.
- The paper assumes that the learning rate is set with μP (maximal update parameterisation), so the rule applies most directly in that setting.
- Decay is only one of several knobs. Its effect on attention stability is covered separately on the [QK-normalisation](../../models/transformer/qk-norm.md) page.

## Connections

- [Weight-Norm Dynamics](index.md) places this result next to the equilibrium analysis.
- [Rotational equilibrium](rotational-equilibrium.md) gives the timescale \(1/(\eta\lambda)\) in steps on which this rule is based.
- [AdamW](../adaptive/adamw.md) defines the decoupled decay that the rule sets.
- [Learning-rate schedules](../learning-rate-schedules.md) matter here because the decay is tied to the learning rate in use.

## Open questions

- Whether the constant-timescale rule holds for very large models trained for a fixed number of tokens rather than epochs.
- How the rule should change when the schedule is not constant, such as with cosine decay or with long warm-up.

## References

- Wang, X., & Aitchison, L. (2024). *How to Set AdamW's Weight Decay as You Scale Model and Dataset Size*. arXiv:2405.13698. https://arxiv.org/abs/2405.13698 — the source of the epoch-timescale finding and the scaling directions for weight decay.
- Loshchilov, I., & Hutter, F. (2019). *Decoupled Weight Decay Regularization*. ICLR 2019. https://arxiv.org/abs/1711.05101 — defines the decoupled decay that the rule adjusts.
- Kosson, A., Messmer, B., & Jaggi, M. (2023). *Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks*. arXiv:2305.17212. https://arxiv.org/abs/2305.17212 — gives the timescale \(1/(\eta\lambda)\) in steps.
- Li, Z., & Arora, S. (2019). *An Exponential Learning Rate Schedule for Deep Learning*. ICLR 2020. https://arxiv.org/abs/1910.07454 — shows that weight decay with normalisation is equivalent to SGD under an exponentially increasing learning rate.
- Wortsman, M., Liu, P. J., Xiao, L., et al. (2023). *Small-scale proxies for large-scale Transformer training instabilities*. arXiv:2309.14322. https://arxiv.org/abs/2309.14322 — tests warm-up, weight decay and μParam as mitigations at small scale.
