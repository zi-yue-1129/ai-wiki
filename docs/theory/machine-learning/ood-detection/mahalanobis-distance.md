---
status: complete
last_reviewed: 2026-10-30
related:
  - theory/machine-learning/ood-detection
tags:
  - out-of-distribution detection
  - feature space
  - Gaussian model
aliases:
  - Mahalanobis distance detector
  - 馬氏距離偵測器
  - Mahalanobis distance
---

# Mahalanobis Distance Detector

The detector of Lee et al. fits class means and a shared covariance to pretrained neural features, then scores proximity to the closest class.[^lee] Part of [Out-of-distribution detection](index.md).

## Fitting the feature statistics

Let $z_i=f(x_i)\in\mathbb R^d$ be a training feature, $y_i$ its label, $C$ the number of classes and $N_c$ the number of examples in class $c$. The paper's maximum-likelihood estimates are[^lee]

$$
\hat\mu_c=\frac{1}{N_c}\sum_{i:y_i=c}z_i,\qquad
\hat\Sigma=\frac{1}{N}\sum_{c=1}^{C}\sum_{i:y_i=c}
(z_i-\hat\mu_c)(z_i-\hat\mu_c)^\top.
$$

Each residual is centred on its **own class mean**, not the global mean. Otherwise, distances between class centres would also contribute to the covariance. Here the $1/N$ denominator specifies the maximum-likelihood convention; changing it rescales squared distances and therefore changes numerical thresholds.

The Gaussian model is an assumption about the representation, not proof that features have that distribution. A neural classifier's ability to fit labels does not by itself establish a good density model.

## Distance, squared distance and score

Keep three quantities distinct:

$$
D_c^2(x)=(f(x)-\hat\mu_c)^\top\hat\Sigma^{-1}
(f(x)-\hat\mu_c),\qquad
D_{\min}^2(x)=\min_c D_c^2(x),\qquad
M(x)=-D_{\min}^2(x).
$$

The quadratic form is a **squared** Mahalanobis distance. SciPy's distance function returns its square root and expects the inverse covariance as its third argument.[^scipy] Passing the covariance itself, or treating that return value as a squared distance, implements a different calculation.

For positive-definite covariance, $D_{\min}^2$ is nonnegative and $M$ is nonpositive. A score closer to zero indicates proximity to some class. Accepting when $M>\tau$ is equivalent to accepting when $D_{\min}^2<-\tau$; a rejection rule must not mix these directions.

This is also why the score should not be presented as a probability. Its magnitude depends on the representation, covariance estimator and convention. A value of $-2$ does not mean a negative probability, nor does a score near zero prove that the input belongs to the training distribution.

### Worked example

Take two class means $\mu_1=(0,0)$ and $\mu_2=(4,0)$, and covariance $\Sigma=\operatorname{diag}(4,1)$. For a feature $z=(a,b)$,

$$
D_1^2=\frac{a^2}{4}+b^2,\qquad
D_2^2=\frac{(a-4)^2}{4}+b^2.
$$

| Feature | $D_1^2$ | $D_2^2$ | $M$ | Decision at $\tau=-3$ |
|---|---|---|---|---|
| $(2,1)$ | 2 | 2 | -2 | Accept |
| $(0,2)$ | 4 | 8 | -4 | Reject |

The threshold and numbers are illustrative, not model measurements. A displacement of two units along the first axis contributes $1$ to squared distance; the same displacement along the second contributes $4$. The covariance changes the geometry rather than simply measuring ordinary Euclidean length. At a tie, either nearest-class index gives the same unperturbed score.

## Input preprocessing and multiple layers

Algorithm 1 selects the nearest class at each layer, takes an input-gradient step intended to **reduce squared distance**, then recomputes the maximum negative distance. Layer scores are combined with logistic-regression weights fitted on validation samples.[^lee] With the selected class held fixed for differentiation, the step is

$$
\tilde x_\ell=x-\varepsilon\operatorname{sign}
\left(\nabla_xD_{\ell,\hat c}^2(x)\right).
$$

Increasing $M$ and increasing $D^2$ are opposite operations. A multi-layer implementation must also distinguish one perturbed input per layer from a single shared perturbation.

The backbone weights need not be retrained, but fitting feature statistics and fitting a validation detector are separate operations. Describing the full ensemble as requiring only stored training means omits the validation stage. Report whether tuning uses actual OOD examples or a surrogate negative set.

## Numerical conditioning

Sharing covariance does not guarantee a stable inverse. Empirical covariance can be ill-conditioned or singular; scikit-learn discusses shrinkage toward a scaled identity as one remedy.[^covariance] For example,

$$
\Sigma_\alpha=(1-\alpha)\hat\Sigma+
\alpha\frac{\operatorname{tr}(\hat\Sigma)}{d}I.
$$

Here $0\leq\alpha\leq1$. This is a possible implementation choice, not a claim that Lee et al. prescribe this regularisation. Record $\alpha$ and the estimator. When the average variance is positive and $\alpha>0$, the identity term lifts zero eigenvalues; if all residual variance is zero, that expression alone cannot do so.

For an invertible covariance, solving $\Sigma v=z-\mu_c$ and computing $(z-\mu_c)^\top v$ gives the same quadratic form as multiplying by the inverse. A pseudoinverse changes how null-space directions are treated, so it should not silently replace an inverse in a reproduction.

## Reported result and scope

Table 5 reports **90.8% TNR at 95% TPR** for CIFAR-10/DenseNet against SVHN, versus 40.2% for the softmax baseline and 86.2% for ODIN, with ID/OOD validation tuning.[^lee] TNR measures rejected OOD inputs; it is not class accuracy.

The comparisons concern the stated data, model and tuning protocol, not a guarantee against every distribution shift or adaptive attack.

## Connections and evaluation checklist

The maximum-softmax baseline uses output probabilities,[^baseline] while [ODIN](odin.md) adds temperature scaling and input perturbations to that output score.[^odin] The feature detector instead uses the geometry of internal representations.

For a reproducible comparison, document:

1. The checkpoint, feature layers, pooling and input preprocessing.
2. Which labelled data fit means and covariance, and which data tune the detector.
3. Covariance estimation, regularisation and numerical solver.
4. Score direction, squared-versus-root convention, threshold and positive class.
5. Whether preprocessing and layer combination are enabled, and their inference cost.
6. Per-shift results, false rejection of familiar inputs, and the action taken after rejection.

These are practical reporting choices. A useful screening flag still needs an independently evaluated fallback, such as abstention or human review. Recompute and revalidate the feature statistics when changing the representation rather than assuming an old numerical threshold transfers.

[^lee]: Lee et al. (2018), equations 1–2, Algorithm 1, Section 2.2 and Table 5; see References.
[^scipy]: SciPy's Mahalanobis distance definition and parameter documentation; see References.
[^covariance]: scikit-learn, empirical and shrunk covariance sections; see References.
[^baseline]: Hendrycks & Gimpel (2017), abstract; see References.
[^odin]: Liang et al. (2018), abstract; see References.

## References

- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. NeurIPS. https://arxiv.org/abs/1807.03888 — Defines feature statistics, negative-distance scoring, input preprocessing and the validation-fitted feature ensemble.
- Hendrycks, D. & Gimpel, K. (2017). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. ICLR. https://arxiv.org/abs/1610.02136 — Introduces maximum softmax probability as a baseline for detecting errors and unfamiliar inputs.
- Liang, S., Li, Y. & Srikant, R. (2018). *Enhancing the Reliability of Out-of-distribution Image Detection in Neural Networks*. ICLR. https://arxiv.org/abs/1706.02690 — Introduces temperature scaling and input perturbation for softmax-based OOD detection.
- SciPy contributors. *scipy.spatial.distance.mahalanobis*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.mahalanobis.html — Specifies the square-root distance convention and the inverse-covariance argument of the API.
- scikit-learn contributors. *Covariance estimation*. https://scikit-learn.org/stable/modules/covariance.html — Explains empirical covariance, numerical inversion problems and shrinkage covariance estimators.
