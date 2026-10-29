---
status: complete
last_reviewed: 2026-10-29
related:
  - theory/machine-learning/ood-detection
tags:
  - out-of-distribution detection
  - temperature scaling
  - softmax
aliases:
  - ODIN
  - Out-of-distribution detector for neural networks
  - 神經網路分布外偵測器
---

# ODIN

ODIN adds temperature scaling and a score-increasing input perturbation to a pretrained classifier's softmax-based out-of-distribution (OOD) detector, without retraining its weights.[^odin] Part of [Out-of-distribution detection](index.md).

## Problem and baseline

An OOD detector decides whether to accept an input as in-distribution (ID); this is different from choosing its class. Hendrycks and Gimpel use the maximum softmax probability as a baseline score. Their experiments show useful separation, not that a high score proves an input is familiar or correctly classified.[^baseline]

## How it works

Let $f_i(x)$ be the logit, or unnormalised class score, for class $i$ among $K$ classes. ODIN uses[^odin]

$$
S_i(x;T)=\frac{\exp(f_i(x)/T)}
{\sum_{j=1}^{K}\exp(f_j(x)/T)},\qquad
\hat y=\arg\max_i f_i(x).
$$

Hold $\hat y$ fixed when differentiating. With $\varepsilon\geq0$, form

$$
\tilde x=x+\varepsilon\,\operatorname{sign}
\left(\nabla_x\log S_{\hat y}(x;T)\right),
\qquad
s(x)=\max_i S_i(\tilde x;T).
$$

Accept as ID when $s(x)>\delta$; otherwise flag OOD. The practical sequence is an initial forward pass, an input-gradient backward pass, then a forward pass on $\tilde x$. The predicted class supplies the gradient target; no ground-truth label is needed. The original image can still supply the classification output.[^odin]

### What increasing temperature actually changes

For fixed logits and positive $T$, dividing by $T$ preserves their ordering. As $T$ increases, the softmax becomes flatter; as $T\to\infty$, every class probability tends to $1/K$. It does **not** spread one input's class probabilities further apart. Guo et al. discuss this softening and the unchanged predicted class in their calibration method.[^calibration]

For example, with two logits $(2,0)$, the maximum probability is about $0.881$ at $T=1$, $0.550$ at $T=10$, and approaches $0.5$. These values follow directly from $1/(1+\exp(-2/T))$. This worked example illustrates the equation, not a measured OOD-detection result.

OOD separation concerns the **distributions of scores across inputs**, rather than the distance between probabilities of classes in one input. Nor is detection the same objective as probability calibration: Guo et al. fit temperature on labelled validation data by negative log-likelihood; a temperature selected for a rejection decision need not make confidence represent correctness frequency.[^calibration]

## Reported result and its scope

Table 2 of Liang et al. reports FPR at 95% TPR falling from **34.7% to 4.3%** for Dense-BC trained on CIFAR-10 against **TinyImageNet (crop)**. Here ID is positive: FPR means OOD inputs incorrectly accepted as ID, not the classifier's class-error rate. The experiments use separate iSUN validation data for tuning.[^odin]

These are historical results for a specified model and dataset pair. They are not a deployment guarantee or a current ranking.

## Reproducing and evaluating a detector

The following is a reporting checklist, not a claim that one parameter setting works for every classifier:

1. Record the checkpoint, input normalisation, image resizing and score convention.
2. Keep tuning data separate from the OOD test set. State which OOD examples were available during tuning.
3. Record $T$, $\varepsilon$ and $\delta$, including the coordinate system in which the perturbation is applied.
4. Compare the full detector with the unmodified softmax baseline under the same data and operating point.
5. Report score distributions, false rejections of ID inputs, false acceptance of OOD inputs and measured runtime.
6. Check different plausible shifts, rather than selecting only the easiest negative dataset.

The threshold expresses a trade-off: lowering it accepts more inputs, potentially retaining more ID inputs while also accepting more OOD inputs. A score is a decision statistic, not a certified probability that the input belongs to the training distribution.

## Connections and alternatives

- **Probability calibration** changes confidence to better reflect correctness frequency; it is distinct from detecting unfamiliar inputs.[^calibration]
- The [Mahalanobis detector](mahalanobis-distance.md) uses distances to class-conditional feature distributions instead of only output probabilities.[^mahalanobis]
- **Energy-based detection** offers another logit-based score. Liu et al. study both scoring a pretrained classifier and training with an energy-based objective; those are distinct experimental settings.[^energy]

These methods are comparison points, rather than evidence that ODIN dominates every alternative.

## Limitations and possible use

A flag could feed an abstention or review workflow, but acceptance does not certify correctness. Input gradients require access beyond a service that returns only labels or probabilities; the perturbation path also costs more than one plain forward pass. Actual latency depends on the model and implementation.

Validation choices, preprocessing and the kinds of negative data used all belong in the evaluation report. A complete deployment decision also needs to specify what happens after rejection, and to test that fallback separately.

[^odin]: Liang et al. (2018), Sections 2–4 and Table 2; see References.
[^baseline]: Hendrycks & Gimpel (2017), abstract; see References.
[^calibration]: Guo et al. (2017), Section 4.2, temperature scaling; see References.
[^mahalanobis]: Lee et al. (2018), abstract; see References.
[^energy]: Liu et al. (2020), abstract; see References.

## References

- Liang, S., Li, Y. & Srikant, R. (2018). *Enhancing the Reliability of Out-of-distribution Image Detection in Neural Networks*. ICLR. https://arxiv.org/abs/1706.02690 — Defines temperature scaling, input preprocessing, the detector and its image-benchmark evaluation.
- Hendrycks, D. & Gimpel, K. (2017). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. ICLR. https://arxiv.org/abs/1610.02136 — Establishes maximum softmax probability as a baseline for error and OOD detection.
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks*. ICML, PMLR 70:1321–1330. https://proceedings.mlr.press/v70/guo17a.html — Explains probability calibration and temperature scaling fitted by validation negative log-likelihood.
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. NeurIPS. https://arxiv.org/abs/1807.03888 — Introduces a feature-based detector using class-conditional Gaussian models and Mahalanobis distance.
- Liu, W., Wang, X., Owens, J. D. & Li, Y. (2020). *Energy-based Out-of-distribution Detection*. https://arxiv.org/abs/2010.03759 — Studies energy scores for pretrained classifiers and energy-based training for OOD detection.
