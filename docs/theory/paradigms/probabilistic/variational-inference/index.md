---
status: complete
last_reviewed: 2026-11-18
related:
  - theory/math/probability-statistics
  - theory/paradigms/unsupervised/density-and-generative-models/vae
tags:
  - probabilistic models
  - approximate inference
  - bayesian
aliases:
  - 變分推論
  - Variational Bayes
  - Variational inference
  - ELBO
---

# Variational Inference

Variational inference (VI) approximates a hard-to-compute posterior distribution by seeking a close distribution in a simpler, tractable family. It turns inference into optimisation by maximising the evidence lower bound (ELBO). Part of [Probabilistic & Bayesian methods](../index.md).[^blei]

## Overview

Bayesian inference asks for the posterior $p(z\mid x)$ over latent variables $z$ given data $x$. Computing it needs the evidence $p(x)=\int p(x,z)\,dz$, which can be an intractable integral. Variational inference chooses a family $\mathcal{Q}$ of candidate distributions and seeks

$$
q^\star = \underset{q\in\mathcal{Q}}{\arg\min}\,
\mathrm{KL}\!\left(q(z)\,\|\,p(z\mid x)\right).
$$

This KL divergence averages the log density ratio under $q$. Its direction matters because exchanging the two distributions changes the objective. The accuracy of VI depends on the family and on how well the optimisation finds its best member.[^blei]

## Key concepts

- **Evidence** $p(x)$ is the normalising constant in Bayes' rule.
- **Variational family** $\mathcal{Q}$ is the set of candidate distributions. Mean-field families factorise over variables or blocks. Richer families can capture more dependence.
- **ELBO** is an objective computable from the joint model $p(x,z)$ and the approximation $q(z)$.
- **Amortised inference** uses a shared network to produce an approximate posterior for each observation.[^vae]

## How it works

### From posterior divergence to an objective

Assume $0<p(x)<\infty$ and finite expectations, with $q$ assigning mass only where the posterior has support. Substituting $p(z\mid x)=p(x,z)/p(x)$ into the KL divergence gives[^blei]

$$
\begin{aligned}
\mathrm{KL}(q\|p(z\mid x))
&= \mathbb{E}_q[\log q(z)-\log p(x,z)] + \log p(x),\\
\mathcal{L}(q)
&= \mathbb{E}_q[\log p(x,z)]-\mathbb{E}_q[\log q(z)],\\
\log p(x)
&= \mathcal{L}(q)+\mathrm{KL}(q\|p(z\mid x)).
\end{aligned}
$$

Since KL divergence is nonnegative, $\mathcal{L}(q)\leq\log p(x)$. For a fixed model and observation, increasing the exact ELBO reduces the posterior KL by the same amount. The evidence term drops out of the optimisation. The expectations in the ELBO may still need analytic work or Monte Carlo estimates.[^bbvi]

### A Gaussian example with a known answer

Consider the illustrative model $z\sim\mathcal{N}(0,1)$ and $x\mid z\sim\mathcal{N}(z,1)$, with observed $x=2$. Here $\mathcal{N}(m,v)$ denotes a Gaussian with mean $m$ and **variance** $v$. Completing the square in the joint density gives $p(z\mid x=2)=\mathcal{N}(1,1/2)$, and integrating out $z$ gives $p(x)=\mathcal{N}(x;0,2)$.

For $q(z)=\mathcal{N}(m,s^2)$ with $s>0$, the KL divergence to this posterior is

$$
\mathrm{KL}(q\|p(z\mid x=2))
=\frac{1}{2}\left[
\frac{s^2+(m-1)^2}{1/2}-1+\log\frac{1/2}{s^2}
\right].
$$

The log evidence is fixed at $\log p(2)=-\tfrac12\log(4\pi)-1\approx-2.2655$. Using natural logarithms, the identity above yields these values.

| Candidate $q$ | Posterior KL | ELBO |
|---|---:|---:|
| $\mathcal{N}(0,1)$ | $1.1534$ | $-3.4189$ |
| $\mathcal{N}(1,1)$ | $0.1534$ | $-2.4189$ |
| $\mathcal{N}(1,1/2)$ | $0$ | $-2.2655$ |

These are hand-calculated candidate distributions. First matching the mean and then the variance raises the ELBO to the log evidence. This family contains the exact posterior, so its optimum has zero approximation error. Harder models may have a posterior outside the chosen family.

### Optimise the variational parameters

Three choices define a variational method: the family of $q$, how the ELBO is optimised, and whether parameters are fitted separately for each observation or shared across a dataset.

For differentiable continuous models, reparameterisation can express a Gaussian draw as $z=\mu+\sigma\odot\epsilon$, where $\epsilon\sim\mathcal{N}(0,I)$ and $\odot$ means elementwise multiplication. This permits gradients through the sampled value.[^vae] Score-function estimators provide another route under the required regularity conditions, and variance reduction helps make them practical.[^bbvi]

## Key methods

- [Mean-field variational inference](mean-field.md) factorises $q$ and supports coordinate updates, with closed-form updates available in conjugate models.[^jordan]
- [Stochastic variational inference](stochastic-variational-inference.md) uses data mini-batches to update a global approximation, scaling inference to large datasets.[^svi]
- [Variational autoencoders](../../unsupervised/density-and-generative-models/vae/index.md) use an encoder to produce $q_\phi(z\mid x)$ and a decoder to model observations.[^vae]

## Connections

- [Probability and statistics](../../../math/probability-statistics/index.md) gives the posterior, evidence and KL divergence that the method uses.
- [Markov chain Monte Carlo](../mcmc/index.md) approximates posterior expectations with samples. Its accuracy depends on mixing and finite-run error. VI's accuracy depends on the family and optimisation, and the computational tradeoff varies by model.[^blei]
- [Neuroscience–AI connections](../../../../brain-mind/neuroai/index.md) discusses probabilistic approaches to studying the brain and mind.

## Applications

- **Topic models** use VI for scalable posterior approximation in latent Dirichlet allocation and related models.[^svi]
- **Generative models** use amortised VI to learn latent-variable models and infer codes for observations.[^vae]
- **Bayesian deep learning** uses approximate posteriors over network weights to represent uncertainty.[^blei]

## Limitations and open questions

- **Family and optimisation error.** A restricted family limits the best achievable ELBO. Local optima and incomplete optimisation can leave an additional gap. A rising stochastic estimate of the ELBO needs interpretation alongside its sampling noise.[^blei][^bbvi]
- **Uncertainty.** Mean-field approximations discard dependencies between factors and can underestimate marginal variances. The amount depends on the posterior and family, as the exact Gaussian fit above illustrates.[^blei]
- **Amortisation.** For a fixed model and family, let $q_x^\star$ maximise the ELBO separately for observation $x$. The gap for an encoder output $q_\phi(z\mid x)$ decomposes as[^cremer]

$$
\log p(x)-\mathcal{L}(q_\phi)
=
\underbrace{\log p(x)-\mathcal{L}(q_x^\star)}_{\text{approximation gap}}
+
\underbrace{\mathcal{L}(q_x^\star)-\mathcal{L}(q_\phi)}_{\text{amortisation gap}}.
$$

A more expressive family can reduce the first gap, while fitting each observation better addresses the second. Estimating these gaps in practice is difficult when the evidence and the optimum within the family are unavailable.[^cremer]

[^blei]: Blei et al. (2017), §§2.1–2.4 and 5, explain the KL objective, ELBO, mean-field restrictions and inference tradeoffs.
[^jordan]: Jordan et al. (1999), §§6–7, develop factorised approximations and variational parameter updates in graphical models.
[^vae]: Kingma & Welling (2014), §§2–3, introduce the inference network and reparameterised gradient estimator.
[^bbvi]: Ranganath et al. (2014), §§2–3, derive score-function gradients and variance-reduction methods for ELBO optimisation.
[^svi]: Hoffman et al. (2013), §§2–3, develop stochastic inference for models with global and local latent variables, including topic models.
[^cremer]: Cremer et al. (2018), §3.1, define the approximation and amortisation gaps for a fixed generative model.

## References

### Seminal papers

- Jordan, M. I., Ghahramani, Z., Jaakkola, T. S. & Saul, L. K. (1999). An introduction to variational methods for graphical models. *Machine Learning* 37(2), 183–233. https://people.eecs.berkeley.edu/~jordan/papers/variational-intro.pdf — Introduces variational methods for graphical models, including the bound and mean-field updates.
- Kingma, D. P. & Welling, M. (2014). Auto-encoding variational Bayes. *ICLR*. arXiv:1312.6114. https://arxiv.org/abs/1312.6114 — Introduces the VAE, an amortised VI method with the reparameterisation trick.
- Ranganath, R., Gerrish, S. & Blei, D. M. (2014). Black box variational inference. *AISTATS*. https://proceedings.mlr.press/v33/ranganath14.html — Gives a general gradient estimator for the ELBO that applies to models without conjugacy.
- Hoffman, M. D., Blei, D. M., Wang, C. & Paisley, J. (2013). Stochastic variational inference. *Journal of Machine Learning Research* 14. https://www.jmlr.org/papers/v14/hoffman13a.html — Scales VI to large datasets with stochastic natural-gradient updates.

- Cremer, C., Li, X. & Duvenaud, D. (2018). *Inference Suboptimality in Variational Autoencoders*. ICML. https://proceedings.mlr.press/v80/cremer18a.html — Separates approximation and amortisation gaps and studies their effects in variational autoencoders.

### Surveys and textbooks

- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2017). Variational inference: a review for statisticians. *Journal of the American Statistical Association* 112(518), 859–877. https://arxiv.org/abs/1601.00670 — Review of VI that explains the ELBO, mean-field and stochastic methods for statisticians.
- Wainwright, M. J. & Jordan, M. I. (2008). Graphical models, exponential families, and variational inference. *Foundations and Trends in Machine Learning*. https://nowpublishers.com/article/Details/MAL-001 — Monograph linking variational methods to exponential families and log-partition functions.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers VI alongside sampling-based inference.
