---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/machine-learning/adversarial-robustness
tags:
  - certified robustness
  - adversarial examples
  - smoothing
aliases:
  - 隨機平滑
  - Randomized smoothing
  - Certified robustness
---

# Randomized Smoothing

Randomized smoothing turns any base classifier into a smoothed classifier by taking a majority vote over noisy copies of the input. Cohen et al. (2019) showed that, under Gaussian noise, the vote gives a certified \(\ell_2\) radius within which the prediction cannot change. Part of [Adversarial examples and robustness](index.md).

## Overview

Most defences give only empirical robustness, which can be broken by a better attack. Certified methods give a guarantee for every input. Randomized smoothing is the most scalable certified method for large networks, because it needs only sampling and a base classifier, not a special network architecture.

## Key concepts

- **Smoothed classifier**: \(g(x)=\arg\max_c \mathbb{P}_{\eta}[f(x+\eta)=c]\), where \(\eta\) is Gaussian noise.
- **Certified radius**: a distance \(R\) such that \(g(x+\delta)=g(x)\) for all \(\|\delta\|_2\le R\).
- **Noise level \(\sigma\)**: the scale of the Gaussian noise, which trades clean accuracy against the radius.
- **Confidence bound**: the certificate holds with high probability because the vote is estimated from samples.

## How it works

Let \(p_A\) be the probability that the base classifier outputs the most likely class \(c_A\) under noise, and \(p_B\) a lower bound on the runner-up. Cohen et al. (2019) show that the smoothed prediction is certified within the radius

\[
R=\frac{\sigma}{2}\big(\Phi^{-1}(p_A)-\Phi^{-1}(p_B)\big),
\]

where \(\Phi^{-1}\) is the inverse standard normal CDF. The probabilities are estimated by sampling, with a confidence bound that accounts for the sampling error. The base classifier is usually trained with Gaussian noise augmentation, so that it is accurate on noisy inputs.

## Variants

- **Different noise distributions** change which norm the certificate covers, and this is an active research direction.
- **Adaptive sampling** spends more samples on inputs near the decision boundary, which tightens the bounds for a given compute budget.
- **Denoised smoothing** puts a denoiser in front of a standard classifier to improve accuracy on noisy inputs.

## Results and limits

- The method scales to large image networks, and it gives certified accuracy at non-trivial radii on ImageNet-scale benchmarks (Cohen et al., 2019).
- The radius is limited by the noise level. Large radii need large noise, which reduces clean accuracy.
- Certificates hold for \(\ell_2\) perturbations with the chosen noise. They do not directly cover other threat models.
- Certification is expensive at inference time, because many noisy samples are needed for each prediction.

## Applications

- **Certified image classifiers** with guarantees for small \(\ell_2\) perturbations.
- **Benchmarks for certified methods**, where radius and certified accuracy are standard metrics.
- **Robustness in safety-critical vision**, where a guarantee is preferred over an empirical claim.

## Open questions

- Certified radii are small for practical accuracy levels, and improving the trade-off is an active area.
- Extending the guarantee beyond \(\ell_2\) and to structured inputs, such as text or graphs, is harder.

## References

### Seminal papers

- Cohen, J., Rosenfeld, E. & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97. https://proceedings.mlr.press/v97/cohen19c.html — Gives the certified \(\ell_2\) radius for a Gaussian-smoothed classifier.
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — Introduces the adversarial examples that certified methods aim to rule out.
- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — Empirical robustness, the baseline that certification is compared with.

### Surveys and textbooks

- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — Motivates certified guarantees by showing that empirical defences can be broken.
- Tsipras, D., Santurkar, S., Engstrom, L., Turner, A. & Madry, A. (2019). Robustness may be at odds with accuracy. In *International Conference on Learning Representations*. arXiv:1805.12152. https://arxiv.org/abs/1805.12152 — Discusses the accuracy cost that certification with noise also pays.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; background on robustness and certification.
