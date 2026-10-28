---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
tags:
  - optimization
  - convergence
  - loss landscape
  - sharpness
aliases:
  - Convergence theory
  - Loss landscapes
  - Sharpness
  - 收斂理論
  - 損失地形
  - 銳度
---

# Convergence, Loss Landscapes and Sharpness

Two questions decide how well an optimiser works. How fast does it reach a point with low loss, and which of the many low-loss points does it reach? The first is answered by convergence theory, which depends on convexity and smoothness. The second is answered by the geometry of the loss landscape, and it matters for generalisation. This subchapter covers both, and the sharpness-aware methods that act on the second.

## Overview

Part of the [Optimisation](index.md) folder. The method pages are [Sharpness-aware minimisation](sharpness-aware-minimisation.md) and, for the flatness-generalisation link, [Sharp minima](sharp-minima.md).

## Key concepts

- **Convexity:** a convex function has no spurious local minima, so every local minimum is global.
- **Smoothness:** the gradient is \(L\)-Lipschitz. It fixes the largest safe step size, \(\eta \le 1/L\).
- **Stationary point:** a point with zero gradient. In non-convex problems, gradient methods reach these, but not all of them are minima.
- **Saddle point:** a stationary point with curvature of both signs. In high dimensions, saddle points are far more common than local minima.
- **Sharpness:** how quickly the loss rises when the parameters move away from a minimum. A flat minimum has low sharpness.

## How it works

For a convex, \(L\)-smooth loss, gradient descent with step \(1/L\) reduces the loss at rate \(O(1/T)\) after \(T\) steps, and linearly if the loss is strongly convex. Stochastic gradients add noise, and the step sizes must decay for convergence in the usual sense (Bottou et al., 2018). These results do not directly apply to deep networks, whose losses are non-convex.

For non-convex losses, the practical question is which stationary points an optimiser reaches. Dauphin et al. (2014) argue that the main difficulty in high dimensions is the proliferation of saddle points, which surround themselves with high error plateaus. Their saddle-free Newton method addresses this with curvature information.

The geometry also bears on generalisation. Keskar et al. (2017) observed that large-batch training tends to find sharper minima, and the link between flatness and generalisation is central to [sharp minima](sharp-minima.md). Dinh et al. (2017) showed that sharpness can be changed by reparametrising the network without changing the function it computes, so sharpness alone cannot explain generalisation.

## Key methods

| Topic | What it addresses | Page |
|---|---|---|
| Convergence for convex and smooth losses | Rate of decrease of the loss | This page (Bottou et al., 2018) |
| Saddle points | Escape from high-error plateaus | Dauphin et al. (2014) |
| Sharpness-aware minimisation (Foret et al., 2021) | Training towards flat neighbourhoods | [SAM](sharpness-aware-minimisation.md) |
| Adaptive sharpness-aware minimisation (Kwon et al., 2021) | Neighbourhoods scaled by weight magnitude, invariant to rescaling | [ASAM](asam.md) |
| Sharp minima and generalisation | Flatness as a predictor | [Sharp minima](sharp-minima.md) |

## Connections

- [Regularisation and weight decay](regularisation-and-weight-decay.md) changes the loss landscape directly, and the flatness it induces is one way it helps generalisation.
- [Large-batch and distributed](large-batch-and-distributed.md) links batch size to the sharpness of the minima found.
- [Second-order methods](second-order.md) use curvature to address saddle points and ill-conditioning.

## Applications

- Choosing a batch size and learning rate by considering the sharpness of the minima that result.
- Training image classifiers with SAM, which has been applied to CIFAR and ImageNet benchmarks.

## Open questions

- Is flatness a cause of generalisation, or a correlate that depends on how the model is parametrised?
- Which practical convergence guarantees carry over from convex problems to deep networks?

## References

### Seminal papers

- Dauphin, Y., Pascanu, R., Gulcehre, C., Cho, K., Ganguli, S. & Bengio, Y. (2014). *Identifying and attacking the saddle point problem in high-dimensional non-convex optimization*. arXiv. https://arxiv.org/abs/1406.2572 — Argues that saddle points, not local minima, are the main difficulty in high-dimensional non-convex optimisation, and proposes the saddle-free Newton method.
- Keskar, N. S., et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR. https://arxiv.org/abs/1609.04836 — Reports that large-batch training finds sharper minima that generalise worse.
- Foret, P., Kleiner, A., Mobahi, H. & Neyshabur, B. (2021). *Sharpness-Aware Minimization for Efficiently Improving Generalization*. arXiv. https://arxiv.org/abs/2010.01412 — Proposes SAM, which minimises the loss in a neighbourhood of the parameters rather than at a single point.
- Dinh, L., Pascanu, R., Bengio, S. & Bengio, Y. (2017). *Sharp Minima Can Generalize For Deep Nets*. arXiv. https://arxiv.org/abs/1703.04933 — Shows that reparametrisation can change the sharpness of a minimum without changing the function or its generalisation, so sharpness is not an invariant measure.
- Li, H., Xu, Z., Taylor, G., Studer, C. & Goldstein, T. (2018). *Visualizing the Loss Landscape of Neural Nets*. NeurIPS. https://arxiv.org/abs/1712.09913 — Visualises loss landscapes, showing how network design changes their geometry.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, including convergence analysis for convex and non-convex problems.
