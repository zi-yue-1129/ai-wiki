---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/flow
tags:
  - flow matching
  - optimal transport
  - minibatch
aliases:
  - OT-CFM
  - Minibatch optimal transport
  - 小批次最優傳輸流匹配
---

# Minibatch OT Flow Matching

Minibatch OT flow matching, or OT-CFM, comes from Tong et al. (2024). It keeps the conditional flow matching objective but changes how noise samples and data points are paired. Within each training minibatch it solves an optimal transport problem between the two sets, and it trains on the pairs given by the transport plan. The result is straighter flows that are more stable to train, with an inexpensive approximation to optimal transport.

## Overview

Conditional flow matching pairs each data point with an independent noise sample. Independent pairing gives conditional paths that can cross, so the regression target has high variance. The authors report that OT-CFM creates simpler flows, which lead to faster inference and more stable training. Pairing within a minibatch by optimal transport keeps the cost of the pairing step local to the batch, which is what makes it practical for large datasets.

## Key concepts

- **Minibatch transport plan**: an optimal transport plan between a batch of noise samples \(x_0\) and a batch of data samples \(x_1\), usually computed with a squared Euclidean cost.
- **Conditional path**: a Gaussian around the linear interpolation \(\mu_t = t\,x_1 + (1-t)\,x_0\) with a small standard deviation \(\sigma\).
- **Regression target**: the direction \(x_1 - x_0\) of the paired points.

## How it works

For each training batch, the method:

1. Draws source points \(x_0\) and target points \(x_1\).
2. Solves an optimal transport problem between the two batches to get a transport plan over pairs.
3. Resamples the pairs \((x_0, x_1)\) from that plan instead of pairing them independently.
4. Samples \(t\sim\mathcal U[0,1]\) and a point \(x\) from a Gaussian around \(\mu_t\) with standard deviation \(\sigma\).
5. Regresses \(v_\theta(t, x)\) onto \(x_1 - x_0\) with a squared-error loss.

The optimal transport batch need not match the optimisation batch size. When the transport batch covers the full support, the method recovers exact optimal transport between the two distributions. With a batch size of one, the method reduces to standard conditional flow matching.

## Key methods

### Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport (Tong et al., 2024)

- **Problem:** independent pairing in conditional flow matching produces high-variance regression targets and curved flows, so sampling needs more steps and training is slower.
- **Core idea:** resample the noise-data pairs according to an optimal transport plan computed on each minibatch. The objective keeps the conditional form of flow matching.
- **Equation or algorithm:** the regression of \(v_\theta(t, x)\) onto \(x_1 - x_0\), where \(x\) is drawn from a Gaussian around \(\mu_t\) and \((x_0, x_1)\) come from the minibatch transport plan. The loss is the squared error of this regression.
- **Results:** the abstract states that OT-CFM creates simpler flows that are more stable to train and lead to faster inference. The paper reports that on CIFAR-10 it performs significantly better with a small number of function evaluations. For the same number of training steps it reaches better validation performance than conditional flow matching, which the authors attribute to lower objective variance.
- **Limitations:** the minibatch transport plan is an approximation, and exact optimal transport needs a batch that covers the full support. Solving the assignment adds cost to each batch. The reported gains come from image benchmarks, and the paper does not claim them for all data types.

## Connections

- [Conditional flow matching](conditional-flow-matching.md) is the objective this method keeps, with a different pairing rule.
- [Rectified flow](rectified-flow.md) straightens paths by reflow, which is an alternative to changing the pairing.
- [Stochastic interpolants](stochastic-interpolants.md) give the general framework in which the choice of coupling and interpolant can be compared.
- For the optimal transport background, see Peyré and Cuturi (2019) in the references below.

## Open questions

- How large the minibatch needs to be before the approximation to optimal transport stops improving.
- Whether the variance reduction carries over to very high-resolution or non-image data.

## References

### Seminal papers

- Tong, A., Fatras, K., Malkin, N., Huguet, G., Zhang, Y., Rector-Brooks, J., Wolf, G. & Bengio, Y. (2024). *Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport*. TMLR. https://arxiv.org/abs/2302.00482 — Introduces minibatch OT pairing and the OT-CFM objective described on this page.
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — The conditional flow matching objective that OT-CFM modifies.
- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv. https://arxiv.org/abs/2209.03003 — An alternative route to straight paths, through reflow.
- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — The interpolant framework within which the coupling choice can be analysed.

### Optimal transport background

- Peyré, G. & Cuturi, M. (2019). *Computational Optimal Transport*. arXiv. https://arxiv.org/abs/1803.00567 — Introduces the computational methods behind the optimal transport plans used in minibatch pairing.
