---
status: complete
last_reviewed: 2026-10-31
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

Randomized smoothing defines a classifier through predictions on noisy inputs. Gaussian smoothing gives a local $\ell_2$ robustness certificate for that **smoothed classifier**, not automatically for the original classifier.[^cohen] Part of [Adversarial examples and robustness](index.md).

## The classifier being certified

For a base classifier $f$ and noise standard deviation $\sigma>0$, define

$$
g(x)=\arg\max_c \Pr_{\eta}[f(x+\eta)=c],
\qquad \eta\sim\mathcal N(0,\sigma^2 I).
$$

This is an ideal probability-based definition. A finite collection of noisy predictions only estimates it. In a multiclass problem, the most probable class need not have probability above one half; a strict majority is a sufficient condition used by a simple certification procedure, not the definition of $g$.

The object being preserved is the label returned by $g$. Neither an individual noisy evaluation of $f$ nor the unmodified prediction $f(x)$ has to remain unchanged.

## Probability bounds and radius

Let $c_A$ be the candidate class. The theorem needs a **lower bound** $\underline p_A$ for its probability and an **upper bound** $\overline p_B$ for every competing class:[^cohen]

$$
\Pr[f(x+\eta)=c_A]\geq\underline p_A
>\overline p_B\geq
\max_{c\neq c_A}\Pr[f(x+\eta)=c].
$$

With nondegenerate bounds, the positive radius is

$$
R=\frac{\sigma}{2}
\left(\Phi^{-1}(\underline p_A)-\Phi^{-1}(\overline p_B)\right),
\qquad
g(x+\delta)=c_A\quad\text{for all }\|\delta\|_2<R.
$$

Here $\Phi$ is the standard normal cumulative distribution function, and $\Phi^{-1}$ is its inverse; SciPy exposes that inverse as the normal distribution's percent-point function.[^normal]

Using a lower bound for the runner-up would be unsafe: subtracting a value that is too small can inflate the radius. Similarly, the theorem states a **strict** inequality on perturbation norm; it does not generally establish what happens exactly on the boundary.

## Estimating a certificate with samples

Cohen et al.'s procedure first selects a class using pilot samples, then uses a fresh sample to lower-bound its probability. If $\underline p_A>1/2$, setting $\overline p_B=1-\underline p_A$ gives[^cohen]

$$
R=\sigma\Phi^{-1}(\underline p_A).
$$

Otherwise, this procedure abstains. Abstention means that the procedure did not return a certificate; it is not an adversarial example or proof of non-robustness.

A practical implementation should distinguish these steps:

1. Draw $n_0$ independent Gaussian perturbations and choose a candidate class.
2. Draw $n$ fresh perturbations and count the candidate's $k$ occurrences.
3. Compute a one-sided $(1-\alpha)$ lower confidence bound on its binomial probability.
4. Return the candidate and positive radius only if that bound exceeds one half.

The observed fraction $k/n$ is a point estimate, not a confidence bound. SciPy documents Clopper–Pearson exact binomial intervals; the implementation must request the intended one-sided coverage rather than silently using a default two-sided interval.[^binomial]

For a fixed input, the theorem is deterministic once valid probability bounds are supplied. The sampling procedure can return an invalid certificate with probability at most $\alpha$ under its assumptions.[^cohen] This does not mean that only $1-\alpha$ of perturbations inside the ball are covered. Nor is $\alpha$ a probability that the class label is correct. Repeated certification calls do not automatically give a simultaneous guarantee over all tested inputs.

## Worked radius examples

Take $\sigma=0.25$ and suppose the following are valid lower bounds, not raw vote fractions:

| $\underline p_A$ | $\Phi^{-1}(\underline p_A)$, approximately | Radius | Simple procedure |
|---|---|---|---|
| 0.60 | 0.2533 | 0.0633 | Certify |
| 0.90 | 1.2816 | 0.3204 | Certify |
| 0.50 | 0 | No positive radius | Abstain |

These are direct calculations, not benchmark measurements. The larger bound leaves less probability available to all competing classes together.

Even unanimous finite samples should not be treated as probability one. For $n$ successes out of $n$ trials, the exact one-sided lower bound satisfies

$$
\underline p_A=\alpha^{1/n}.
$$

For example, $n=100$ and $\alpha=0.001$ give $\underline p_A\approx0.9333$ and $R\approx0.3751$ at $\sigma=0.25$. The bound follows by solving $p^n=\alpha$: unanimity is still possible when the true probability is below one. Using the plug-in estimate one would incorrectly suggest an infinite radius.

## Reported results and related developments

Cohen et al.'s Table 1 reports **49% approximate certified accuracy on ImageNet at radius 0.5**, using $\sigma=0.25$.[^cohen] Certified accuracy counts correct predictions with sufficient returned radius, rather than the fraction certified among only accepted examples. The result is historical and tied to that evaluation setup.

Salman et al. (2019) study adversarial training adapted to smoothed classifiers.[^adversarial] Salman et al. (2020) instead prepend a trained denoiser to a pretrained classifier before smoothing.[^denoised] The denoiser becomes part of the base mapping; leaving the classifier's weights fixed does not mean the overall procedure needs no training.

## Scope and evaluation

A certificate establishes local label stability, not correctness, semantic similarity or robustness to every attack type. An $\ell_2$ ball does not directly certify rotations, patches, arbitrary distribution shifts or discrete edits to text.

Record the input coordinate system, normalisation, complete base mapping, noise distribution and $\sigma$. Preprocessing can be part of $f$, but changing the noise law requires a matching theorem. A radius stated in normalised coordinates should not silently be presented as a raw-pixel radius.

Also report $n_0$, $n$, $\alpha$, the confidence-bound method, abstention rate, accuracy and runtime. Keep noisy sample independence and class selection explicit. When comparing training methods, use matched sampling budgets and specify whether runtime includes certification or only prediction.

Increasing $\sigma$ changes the distribution seen by $f$, so a larger multiplier in the radius formula does not by itself guarantee a larger useful certificate. The probability bounds and classification performance must be re-evaluated.

## Variants

- **Different noise distributions** change which norm the certificate covers, and this is an active research direction.
- **Adaptive sampling** spends more samples on inputs near the decision boundary, which tightens the bounds for a given compute budget.
- **Denoised smoothing** puts a denoiser in front of a standard classifier to improve accuracy on noisy inputs.

## Applications

- **Certified image classifiers** with guarantees for small $\ell_2$ perturbations.
- **Benchmarks for certified methods**, where radius and certified accuracy are standard metrics.
- **Robustness in safety-critical vision**, where a guarantee is preferred over an empirical claim.

## Open questions

- Certified radii are small for practical accuracy levels, and improving the trade-off is an active area.
- Extending the guarantee beyond $\ell_2$ and to structured inputs, such as text or graphs, is harder.

[^cohen]: Cohen, Rosenfeld & Kolter (2019), Theorem 1, Section 3.2.2, Proposition 2 and Table 1; see References.
[^normal]: SciPy, normal distribution CDF and percent-point function; see References.
[^binomial]: SciPy, exact binomial proportion confidence intervals; see References.
[^adversarial]: Salman et al. (2019), abstract; see References.
[^denoised]: Salman et al. (2020), abstract; see References.

## References

- Cohen, J., Rosenfeld, E. & Kolter, J. Z. (2019). *Certified Adversarial Robustness via Randomized Smoothing*. ICML, PMLR 97:1310–1320. https://proceedings.mlr.press/v97/cohen19c.html — Establishes the Gaussian smoothing certificate and a sampling procedure with controlled failure probability.
- Salman, H. et al. (2019). *Provably Robust Deep Learning via Adversarially Trained Smoothed Classifiers*. NeurIPS. https://arxiv.org/abs/1906.04584 — Studies adversarial training designed to improve the certified robustness of smoothed classifiers.
- Salman, H., Sun, M., Yang, G., Kapoor, A. & Kolter, J. Z. (2020). *Denoised Smoothing: A Provable Defense for Pretrained Classifiers*. https://arxiv.org/abs/2003.01908 — Uses a trained denoiser before a pretrained classifier as the base mapping for smoothing.
- SciPy contributors. *BinomTestResult.proportion_ci*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html — Documents exact Clopper–Pearson and alternative confidence intervals for binomial proportions.
- SciPy contributors. *scipy.stats.norm*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html — Specifies standard-normal distribution functions, including the inverse CDF used in radius calculations.
