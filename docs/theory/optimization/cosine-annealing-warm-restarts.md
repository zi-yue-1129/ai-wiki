---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - learning rate
aliases:
  - SGDR
  - Cosine annealing
  - Warm restarts
  - 餘弦退火
  - 暖重啟
---

# Cosine Annealing with Warm Restarts

Cosine annealing with warm restarts (SGDR) lowers the learning rate along a half cosine curve, raises it back to its maximum at fixed points, and starts the decay again. Each run is longer than the one before. Loshchilov and Hutter introduced it at ICLR 2017. The parent overview is [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md).

## Overview

A single cosine decay falls smoothly from a high rate to a low one, and it is a common choice. Its weakness is that the rate stays small for most of the late training, so the optimiser cannot leave a region it has settled into. Restarting the rate periodically gives it a chance to move on, and the model at the end of each run can be saved as a snapshot.

## Problem

Training budgets are finite, and the usual decay is fixed before training starts. Loshchilov and Hutter ask whether a schedule with restarts can reach good solutions sooner. They judge schedules by their *anytime* performance, meaning how good the model is at any point in training, not only at the end.

## Core idea

Within run \(i\), the rate falls along a cosine curve from \(\eta^i_{\max}\) to \(\eta^i_{\min}\). At the end of the run it is reset to \(\eta^i_{\max}\), which is the warm restart, and run \(i+1\) begins. Each run is \(T_{\mathrm{mult}}\) times as long as the one before, so the late part of training has longer phases.

### Schedule in motion

<div style="max-width:640px;width:100%" role="group" aria-label="Learning-rate schedule animation">
<div style="width:100%">
<img src="../../assets/concept-animations/sgdr-restart-still.svg" data-motion-src="../../assets/concept-animations/sgdr-restart-motion.svg" style="display:block;width:100%;height:auto" alt="Cosine learning-rate decay over successively longer cycles, with upward resets at each restart.">
</div>
</div>

*Original animation by AI Wiki, CC BY-SA 4.0.*

The moving marker traces a schematic schedule with cycle lengths 1, 2 and 4 and fixed learning-rate bounds. At each restart the rate jumps back to its maximum; the optimizer parameters are **not** reset. Time and rates are normalized illustration values, not measurements from training.

## Algorithm

Let \(T_i\) be the length of run \(i\) in epochs, and let \(T_{\mathrm{cur}}\) be the epochs elapsed since the last restart. The paper updates \(T_{\mathrm{cur}}\) after every batch, so it takes fractional values. The learning rate is

\[
\eta_t = \eta^i_{\min} + \frac{1}{2}\left(\eta^i_{\max} - \eta^i_{\min}\right)\left(1 + \cos\!\left(\frac{T_{\mathrm{cur}}}{T_i}\,\pi\right)\right)
\]

The rate equals \(\eta^i_{\max}\) at a restart and falls to \(\eta^i_{\min}\) at the end of the run. The paper keeps the bounds fixed across restarts and sets \(T_{i+1} = T_{\mathrm{mult}}\, T_i\). A setting with \(T_{\mathrm{mult}} = 1\) gives runs of equal length. The paper takes snapshots at the ends of runs and combines them in an ensemble.

## Results

- **Headline error rates.** With a WRN-28-10 network, the paper reports 3.14% error on CIFAR-10 and 16.21% on CIFAR-100. These figures come from an ensemble of 16 runs with 3 snapshots per run, not from a single model.
- **Single models.** Single-model results are higher. The best single-model CIFAR-10 result in the paper is 3.66% (WRN-28-20, \(T_0 = 200\)), and the best CIFAR-100 single-model result is 18.70% (\(T_0 = 10\), \(T_{\mathrm{mult}} = 2\)). The default WRN-28-10 baseline gets 4.03% and 19.57% with a single snapshot.
- **Speed.** The paper states that SGDR reaches comparable or better results with 2 to 4 times fewer epochs than the default schedule. The default is a 200-epoch budget with the rate multiplied by 0.2 at epochs 60, 120 and 160.
- **Downsampled ImageNet.** On a 32 by 32 version of ImageNet, the paper reports 39.24% top-1 error and 17.17% top-5 error. The authors call this experiment preliminary.

## Limitations

- **Temporary losses.** Restarts often make performance worse for a while, so the paper recommends taking the solution from the end of a run instead of the last iterate.
- **Anytime cost.** The paper notes that the \(T_0 = 200\) setting has the worst anytime performance except in the final epochs.
- **Hand-chosen schedule.** \(T_0\) and \(T_{\mathrm{mult}}\) are set by the experimenter. The paper compares several settings but gives no rule for choosing them for a new budget.
- **Ensemble cost.** The headline numbers need many runs, so the gain is partly a gain from ensembling, and it costs more compute than a single model.
- **Statistics.** The authors say the bolding in their main table is not based on statistical tests, because there are too few runs.

## Variants and related schedules

- **Plain cosine annealing** is one run with no restart. It is the simplest version of the same curve.
- **Cosine restarts with a fixed period** use \(T_{\mathrm{mult}} = 1\), so every run has the same length.
- **Cyclical rates** such as [triangular and triangular2 policies](cyclical-learning-rates.md) also restart the rate, but they use linear ramps between fixed bounds and do not follow a cosine curve.

## Connections

- [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md) places this method beside step decay and cyclical rates.
- [Gradual warm-up](gradual-warm-up.md) is a separate, short ramp at the start of training. Many recipes place a warm-up before a cosine decay, but that combination is a choice in the training recipe, not part of this method.
- [Regularisation and weight decay](regularisation-and-weight-decay.md) interacts with the rate, because the size of each weight update depends on the current rate.

## Open questions

- Does restarting help more with long budgets and large datasets than with short runs?
- Is there a principled rule for choosing \(T_0\) and \(T_{\mathrm{mult}}\) for a given compute budget?

## References

### Seminal papers

- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR 2017. https://arxiv.org/abs/1608.03983 — Proposes cosine annealing with warm restarts, the anytime results on CIFAR-10 and CIFAR-100, and the snapshot ensembles.
- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV 2017, pp. 464–472. doi:[10.1109/WACV.2017.58](https://doi.org/10.1109/WACV.2017.58) — Periodic learning-rate schedule with bounds found by a range test, for comparison with restarts.
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — Gradual warm-up and the linear scaling rule, used in many training recipes that combine warm-up with a decay.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS 2017. https://arxiv.org/abs/1706.03762 — Linear warm-up followed by inverse-square-root decay, a different decay shape used for Transformers.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review, 60(2), 223–311. doi:[10.1137/16M1080173](https://doi.org/10.1137/16M1080173) — Survey of step-size choices and convergence theory for stochastic gradient methods.
