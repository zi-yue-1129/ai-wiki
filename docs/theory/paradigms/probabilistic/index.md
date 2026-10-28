---
related:
- brain-mind/cognitive-science
- applications/mental-health
- theory/paradigms/active
---

# Probabilistic & Bayesian Methods

## Why probability?

The world is uncertain: sensors are noisy, information is incomplete, the future is unknown. Probability is a **consistent language for representing and updating beliefs**.

## Bayesian inference

\[
\underbrace{p(\theta\mid D)}_{\text{posterior}} = \frac{\overbrace{p(D\mid\theta)}^{\text{likelihood}}\;\overbrace{p(\theta)}^{\text{prior}}}{p(D)}
\]

Advantages: natural uncertainty quantification, principled use of prior knowledge, robustness with small data.

## Probabilistic graphical models

Graphs encode conditional dependencies so high-dimensional joint distributions become tractable.

| Type | Graph | Examples |
|---|---|---|
| Bayesian network | Directed acyclic | Medical diagnosis, causal models |
| Markov random field | Undirected | Image segmentation, Ising model |
| Hidden Markov model | Directed chain | Early speech recognition, gene finding |
| Conditional random field | Undirected, conditioned on input | Named-entity recognition |
| Kalman filter | Linear-Gaussian state space | Tracking, navigation |
| Topic model (LDA) | Hierarchical | Document topics |

For the inference algorithms and the historical sequence models in more depth, see [Probabilistic Graphical Models](graphical-models/index.md).

## Inference

- **Exact**: variable elimination, belief propagation (on trees)
- **Approximate**:
    - **Sampling**: [Markov chain Monte Carlo](mcmc/index.md) (Metropolis–Hastings, Gibbs, HMC/NUTS, Langevin dynamics)
    - **Variational inference**: approximate the posterior with a simpler \(q\) by maximising the evidence lower bound (ELBO) — a VAE is amortised variational inference. See [Variational Inference](variational-inference/index.md) for the methods.

## Causal inference

Correlation is not causation. Pearl's ladder of causation:

1. **Association** (seeing): \(p(y\mid x)\)
2. **Intervention** (doing): \(p(y\mid do(x))\)
3. **Counterfactuals** (imagining): what would y have been had x not happened?

Tools: structural causal models, do-calculus, the potential-outcomes framework (Rubin), instrumental variables, difference-in-differences, double machine learning. Essential for using AI in medicine, economics and policy.

## Bayesian deep learning and uncertainty

- Bayesian neural networks, MC dropout, deep ensembles
- **Aleatoric** (data noise) vs **epistemic** (model ignorance) uncertainty
- **Conformal prediction**: distribution-free prediction sets with coverage guarantees; increasingly popular in medical AI
- Gaussian processes: small-data regression and Bayesian optimisation (hyperparameters, experimental design)

## The Bayesian brain

A major idea in cognitive science and neuroscience: **the brain performs (approximate) Bayesian inference**.

- **Perception** combines sensory evidence (likelihood) with experience (prior) — e.g. the "light comes from above" prior shapes how we see shaded bumps and dents.
- **Multisensory integration**: humans weight vision and touch by their reliability, close to the statistical optimum (Ernst & Banks, 2002).
- **Motor control**: people integrate priors with sensory feedback in a Bayesian way (Körding & Wolpert, 2004).
- **Cognitive development**: how children learn causal structure and word meanings from sparse data (Gopnik, Tenenbaum).
- **Predictive coding and the free-energy principle**: see [Cognitive Science](../../../brain-mind/cognitive-science/index.md).
- **Computational psychiatry**: schizophrenia and autism have been modelled as imbalances in the weighting of priors and sensory evidence (see [Mental Health](../../../applications/mental-health/index.md)).

Critiques: "Bayesian" models can be flexible enough to fit almost anything; humans also show systematic departures from optimal inference (see [Psychology & AI](../../../brain-mind/psychology/index.md)). **Resource-rational** analysis (Lieder & Griffiths, 2020) reconciles the two: people approximate Bayesian inference under limited time and computation.

## Probabilistic programming

Write a generative model as a program; the system performs inference: [PyMC](https://www.pymc.io/), [Stan](https://mc-stan.org/), [NumPyro](https://num.pyro.ai/), [Pyro](https://pyro.ai/).

## Resources

- Koller & Friedman, *Probabilistic Graphical Models* (and Coursera course)
- Murphy, *Probabilistic Machine Learning*
- Bishop, *Pattern Recognition and Machine Learning* (free PDF)
- McElreath, *Statistical Rethinking* (lectures free online)
- Pearl & Mackenzie, *The Book of Why*
- Griffiths, Chater & Tenenbaum, *Bayesian Models of Cognition* (2024)

## References

### Seminal papers

- Hoffman, M. D., et al. (2013). *Stochastic Variational Inference*. arXiv. https://arxiv.org/abs/1206.7051 — Scales variational inference to large datasets by optimising the variational objective with stochastic gradients.
- Neal, R. M. (2012). *MCMC using Hamiltonian dynamics*. arXiv. https://arxiv.org/abs/1206.1901 — A tutorial on Hamiltonian Monte Carlo, the sampler behind modern probabilistic programming systems.
- Blei, D. M., et al. (2016). *Variational Inference: A Review for Statisticians*. arXiv. https://arxiv.org/abs/1601.00670 — A clear tutorial on approximating hard posterior distributions by optimisation, with worked examples.

### Surveys and textbooks

- Deisenroth, M. P., Faisal, A. A. & Ong, C. S. *Mathematics for Machine Learning*. https://mml-book.github.io/ — Covers the probability and statistics behind machine learning, with a free PDF from the authors.

### Articles and documentation

- Bingham, E., et al. (2018). *Pyro: Deep Universal Probabilistic Programming*. arXiv. https://arxiv.org/abs/1810.09538 — Describes a probabilistic programming language built on PyTorch, combining deep networks with Bayesian models.
- Carpenter, B., et al. (2015). *The Stan Math Library: Reverse-Mode Automatic Differentiation in C++*. arXiv. https://arxiv.org/abs/1509.07164 — The automatic-differentiation engine that powers Stan, the widely used Bayesian inference system.
