---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/probabilistic
tags:
  - uncertainty
  - deep learning
aliases:
  - 蒙地卡羅丟棄法
  - MC Dropout
  - Monte Carlo dropout
---

# MC Dropout

MC dropout keeps dropout switched on when a trained network makes predictions. It runs several stochastic forward passes and uses their spread as an estimate of the model's uncertainty. Gal and Ghahramani (2016) showed that this procedure has a Bayesian interpretation. It is one of the methods compared on the [uncertainty and calibration](../index.md) page.

## Overview

Dropout randomly sets a fraction of a network's units to zero during training, which reduces overfitting. At test time it is normally switched off, so the network returns one deterministic answer. Gal and Ghahramani's abstract describes a different use of the same network. They cast dropout training in deep networks as approximate Bayesian inference in deep Gaussian processes, and the result gives tools to model uncertainty with dropout networks. It works with existing dropout networks, and the authors argue that it does not sacrifice computational complexity or test accuracy.

## Key concepts

- **Dropout mask.** A random vector of zeros and ones, drawn for each forward pass, that decides which units are active.
- **Stochastic forward pass.** A prediction made with one sampled mask. Repeating it with different masks gives a distribution of predictions for the same input.
- **Approximate posterior.** The paper interprets each sampled set of masks as a sample from an approximate posterior over the network's weights, which is why the spread can be read as model uncertainty.
- **Epistemic uncertainty.** The part of the uncertainty that the method targets. Noise in the data, the aleatoric part, is not captured unless it is modelled separately.

## How it works

Let \(f(x; \hat{W}_t)\) be the network's output for input \(x\) when dropout masks are sampled, and let \(T\) be the number of passes. The predictive mean and the sample variance are

\[
\hat{\mu}(x) = \frac{1}{T}\sum_{t=1}^{T} f(x; \hat{W}_t), \qquad
\widehat{\operatorname{Var}}(x) = \frac{1}{T}\sum_{t=1}^{T}\big(f(x; \hat{W}_t) - \hat{\mu}(x)\big)^2.
\]

For regression, the paper adds an observation-noise term to the variance. For classification, the sampled probabilities are averaged, and the entropy of the average is a common uncertainty score.

1. Train an ordinary network with dropout in the layers the method uses.
2. For a new input, keep dropout active and sample \(T\) masks.
3. Run one forward pass per mask to obtain \(T\) predictions.
4. Report the average as the prediction and the spread as the uncertainty.

## Results

The abstract reports a considerable improvement in predictive log-likelihood and RMSE over existing state-of-the-art methods, on regression and classification tasks, with MNIST as an example. It also reports that dropout's uncertainty was used in deep reinforcement learning. These are qualitative summaries here. The exact numbers are in the paper and were not re-run for this page.

## Limitations

- **Crude approximation.** The approximate posterior is restricted, so the spread is an approximation whose quality depends on the architecture and on how dropout is applied.
- **Dropout rate.** The rate is a hyperparameter, and it changes the uncertainty estimates as well as the accuracy. Theory gives only limited guidance on choosing it.
- **Cost at inference.** The method needs \(T\) forward passes for every prediction, which is cheap for small networks and expensive for large ones.
- **Partial picture.** The method captures epistemic uncertainty. Kendall and Gal (2017) add a separately learned aleatoric term to obtain both.

## Open questions

- How should the dropout rate and its placement be chosen so that uncertainty, not only accuracy, is good?
- Does dropout-based uncertainty stay reliable on inputs far from the training data? Benchmarks under dataset shift, such as Ovadia et al. (2019), are the usual test.
- How does MC dropout compare with a true posterior, and with the ensemble view of Wilson and Izmailov (2020)?

## Connections

MC dropout is a practical instance of the variational approach described on the [probabilistic methods](../../../probabilistic/index.md) page, and it is the single-network counterpart of [deep ensembles](../deep-ensembles/index.md). Knill and Pouget (2004) argue that the brain can be described as performing approximate Bayesian inference. Sampling-based views of inference are one way that idea can be modelled, but MC dropout is an engineering approximation and not a model of neural noise.

## References

### Seminal papers

- Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. ICML. https://arxiv.org/abs/1506.02142 — Shows that dropout training can be read as approximate Bayesian inference, and gives a way to estimate uncertainty from a trained dropout network.
- Kendall, A. & Gal, Y. (2017). What uncertainties do we need in Bayesian deep learning for computer vision? NeurIPS. https://arxiv.org/abs/1703.04977 — Combines Bayesian dropout for epistemic uncertainty with a learned aleatoric term in vision tasks.
- Blundell, C., Cornebise, J., Kavukcuoglu, K. & Wierstra, D. (2015). Weight uncertainty in neural networks. ICML. https://arxiv.org/abs/1505.05424 — Bayes by Backprop, the variational alternative that learns a distribution over weights directly.
- Knill, D. C. & Pouget, A. (2004). The Bayesian brain: the role of uncertainty in neural coding and computation. *Trends in Neurosciences*. https://doi.org/10.1016/j.tins.2004.10.007 — Review arguing that the brain represents uncertainty and performs approximately Bayesian computation.

### Surveys and textbooks

- Wilson, A. G. & Izmailov, P. (2020). Bayesian deep learning and a probabilistic perspective of generalization. NeurIPS. https://arxiv.org/abs/2002.08791 — Discusses Bayesian marginalisation in deep networks and why it improves calibration.
- Gawlikowski, J. et al. (2021). A survey of uncertainty in deep neural networks. arXiv. https://arxiv.org/abs/2107.03342 — Surveys uncertainty estimation methods for deep networks.

### Articles and documentation

- Ovadia, Y. et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. NeurIPS. https://arxiv.org/abs/1906.02530 — Large benchmark that tests predictive uncertainty methods, including approximate Bayesian ones, under dataset shift.
