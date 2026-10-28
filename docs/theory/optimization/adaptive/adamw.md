---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/loss-functions-and-optimization
  - theory/deep-learning
tags:
  - optimization
  - weight decay
aliases:
  - AdamW 最佳化器
  - 解耦權重衰減
  - AdamW
  - Decoupled weight decay
---

# AdamW

AdamW is Adam with decoupled weight decay. It applies the weight-decay penalty directly to the parameters, outside the adaptive step, instead of adding an L2 term to the gradient. Loshchilov and Hutter (2017, published at ICLR 2019) showed that this difference matters for adaptive methods, and AdamW is now common for training Transformer models. The family overview is on the [Adaptive Methods](index.md) page, and the method it modifies is [Adam](adam.md).

## Overview

In plain SGD, adding an L2 penalty \(\frac{\lambda}{2}\|\theta\|^2\) to the loss and taking a gradient step is the same as weight decay with factor \(\eta\lambda\). Loshchilov and Hutter observed that this equivalence breaks under Adam. The L2 term enters the gradient, so Adam divides it by the root of the second moment. Parameters with large gradients then receive less decay, which is the opposite of what the regulariser intends.

## Key concepts

- **L2 regularisation**: a penalty added to the loss, whose gradient is then scaled by the optimiser.
- **Weight decay**: a shrinkage of the parameters at each step, applied outside the gradient.
- **Decoupling**: applying the decay with its own coefficient \(\lambda\), independent of the adaptive denominator.
- **Learning-rate independence**: the paper reports that with decoupled decay, the best decay factor is largely independent of the learning rate, so the two can be tuned separately.

## How it works

With \(\hat m_t\) and \(\hat v_t\) defined as in [Adam](adam.md), the AdamW update is

\[
\theta_t = \theta_{t-1} - \eta\left(\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon} + \lambda\,\theta_{t-1}\right)
\]

The decay term \(\lambda\theta_{t-1}\) is added after the adaptive step, so it is not divided by \(\sqrt{\hat v_t}\). Adam with L2 regularisation would instead put \(\lambda\theta_{t-1}\) inside the gradient \(g_t\), and the adaptive scaling would weaken it for parameters with large gradients.

## Key methods

### Decoupled Weight Decay Regularization (Loshchilov & Hutter, 2017/2019)

- **Problem:** for adaptive methods, adding an L2 penalty to the loss is not the same as weight decay. The penalty is rescaled by the adaptive denominator, so regularisation weakens for parameters with large gradients.
- **Core idea:** apply weight decay directly to the parameters, outside the adaptive step, so the decay factor is decoupled from the gradient scaling.
- **Equation or algorithm:** the update above, with \(\lambda\) the decay coefficient.
- **Results:** the abstract reports that decoupled decay substantially improves Adam's generalisation and lets it compete with SGD with momentum on image classification. It gives no specific numbers in the abstract.
- **Limitations:** the paper's evidence comes mainly from image classification, and its advantage on other tasks depends on tuning. AdamW is widely used for Transformer models, where the gain over Adam with L2 regularisation depends on the setup.

## Connections

- [Adam](adam.md) is the optimiser this method modifies.
- [Loss functions and optimisation](../../paradigms/supervised/loss-functions-and-optimization/index.md) explains weight decay as a penalty on the loss.
- [SGD and momentum](../sgd-and-momentum/index.md) is the setting where L2 and weight decay coincide.

## Applications

- Pre-training and fine-tuning of Transformer language models and vision Transformers.
- Default optimiser setting in many open-source training recipes.

## Open questions

- How much of AdamW's advantage over Adam with L2 holds beyond image and language models?
- Is there an automatic rule that sets the decay coefficient from the learning rate?

## References

### Seminal papers

- Loshchilov, I. & Hutter, F. (2019). Decoupled Weight Decay Regularization. ICLR. https://arxiv.org/abs/1711.05101 — Shows that L2 regularisation and weight decay differ under adaptive methods and proposes AdamW.
- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. ICLR. https://arxiv.org/abs/1412.6980 — The base optimiser that AdamW modifies.
- Wilson, A. C., Roelofs, R., Stern, M., Srebro, N. & Recht, B. (2017). The Marginal Value of Adaptive Gradient Methods in Machine Learning. NeurIPS. https://proceedings.neurips.cc/paper_files/paper/2017/hash/81b3833e2504647f9d794f7d7b9bf341-Abstract.html — Shows that adaptive methods can find solutions that generalise worse than SGD, the gap that decoupled decay addresses.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, including adaptive variants and their trade-offs.
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Chapter 7 on regularisation. MIT Press. https://www.deeplearningbook.org/ — Textbook treatment of weight decay as a regulariser, free online.