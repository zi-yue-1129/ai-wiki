---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning
  - brain-mind/neuroai
tags:
  - optimization
  - deep learning
aliases:
  - 反向模式自動微分
  - 反向傳播
  - Reverse-mode AD
  - Backpropagation
---

# Reverse-Mode Automatic Differentiation

Reverse-mode automatic differentiation computes the gradient of a scalar output with respect to all of a program's inputs. It does this with one forward pass that stores intermediate values and one backward sweep. Applied to a neural network, it is the algorithm known as backpropagation. It is the second basic mode of [automatic differentiation](../index.md).

## Overview

Reverse mode runs the chain rule backwards. Rather than pushing a change in one input forward, it pulls the sensitivity of the output back through each operation, one adjoint at a time: $\bar v_j = \partial f / \partial v_j$. The product it computes is a vector-Jacobian product. One backward sweep serves all inputs at once, so reverse mode suits a function with many inputs and one output, such as a training loss. Baydin and colleagues (2022) describe backpropagation as a special case of AD, alongside forward mode.

## Key concepts

- **Adjoint** $\bar v$: the derivative of the output with respect to an intermediate value.
- **Tape**: the forward-pass record of operations and their inputs, read in reverse.
- **VJP rule**: for each operation, the rule mapping output adjoints to input adjoints. For $z = Wx$, $\bar x = W^{\top}\bar z$ and $\bar W = \bar z\,x^{\top}$.
- **Accumulation**: a value used by several operations receives the sum of their contributions.

## How it works

The adjoint of each value is the sum over the operations that consume it:

$$\bar v_j = \sum_{k \,:\, v_j \text{ is an input of } v_k} \bar v_k \,\frac{\partial v_k}{\partial v_j}$$

The algorithm has four steps:

1. **Forward pass**: evaluate the program in order, storing each intermediate value and the operation that produced it.
2. **Seed**: set the output adjoint to $\bar y = 1$ for a scalar loss, and all other adjoints to zero.
3. **Backward sweep**: for each operation from last to first, add $\bar v_k\,\partial v_k/\partial v_j$ to the adjoint of each of its inputs $v_j$.
4. **Read off**: the adjoints of the inputs, or of the parameters, form the gradient.

On the example from the [overview](../index.md), the sweep gives $\bar x = 2.584$ and $\bar y = 2$ in one pass. For a scalar output, the gradient costs a small constant multiple of the forward evaluation, however many inputs there are. Griewank and Walther (2008) describe this as the cheap gradient principle.

The stored values are the price: memory grows with the forward computation, and in-place operations can overwrite values the backward pass needs.

## Results

Evidence for reverse mode comes from three kinds of result, none quoted from a benchmark table here:

- Rumelhart and colleagues (1986) showed on small tasks that gradient backpropagation lets hidden units learn internal representations.
- Chen and colleagues (2016) show that memory can be traded for recomputation. Their abstract reports cutting a 1,000-layer residual network from 48 GB to 7 GB, with about 30% more running time.
- Chen and colleagues (2018) show that the adjoint method backpropagates through an ODE solver at constant memory cost.

## Limitations

- **Memory** grows with the forward computation, which is why checkpointing is needed for deep models.
- **Many outputs are costly.** A full Jacobian of a function with many outputs needs one backward pass per output, so forward mode can be cheaper there.
- **Non-differentiable operations** such as spike thresholds or sampling need surrogates or estimators; see [surrogate gradients](../../../../brain-mind/snn-neuromorphic/surrogate-gradients/index.md).
- **Biological plausibility.** Exact reverse mode needs the transposed forward weights in the backward pass. Lillicrap and colleagues (2016) show that random fixed feedback weights can avoid this, but the question remains open.

## Open questions

- What is the best trade-off between checkpointing, recomputation and memory at very large scale?
- Do graph-free, functional formulations such as Elliott's (2018) give practical gains in parallel execution?
- Can local learning rules approximate reverse mode without transported weights?

## References

### Seminal papers

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*. https://doi.org/10.1038/323533a0 — Popularises backpropagation for multilayer networks, the reverse-mode method used to train deep networks.
- Pearlmutter, B. A. & Siskind, J. M. (2008). Reverse-mode AD in a functional framework. *ACM Transactions on Programming Languages and Systems*. https://doi.org/10.1145/1330017.1330018 — Expresses reverse-mode AD in a functional language, including higher-order functions.
- Elliott, C. (2018). The simple essence of automatic differentiation. ICFP 2018. https://arxiv.org/abs/1804.00746 — Derives a graph-free, tape-free reverse-mode AD algorithm from a short specification.
- Chen, T., Xu, B., Zhang, C. & Guestrin, C. (2016). Training Deep Nets with Sublinear Memory Cost. https://arxiv.org/abs/1604.06174 — Gradient checkpointing, which trades recomputation for memory to train very deep networks.
- Lillicrap, T. P., Cownden, D., Tweed, D. B. & Akerman, C. J. (2016). Random synaptic feedback weights support error backpropagation for deep learning. *Nature Communications*. https://doi.org/10.1038/ncomms13276 — Argues that random fixed feedback weights can replace the transposed forward weights in error backpropagation.

### Surveys and textbooks

- Baydin, A. G., Pearlmutter, B. A., Radul, A. A. & Siskind, J. M. (2015/2018). Automatic differentiation in machine learning: a survey. *Journal of Machine Learning Research*. https://arxiv.org/abs/1502.05767 — Survey that defines the main differentiation techniques and their relationships, with backpropagation as the reverse-mode case.
- Griewank, A. & Walther, A. (2008). *Evaluating Derivatives*. SIAM. https://doi.org/10.1137/1.9780898717761 — Standard reference on reverse mode, checkpointing and the cheap gradient principle.
- Baydin, A. G., Pearlmutter, B. A., Syme, D., Wood, F. & Torr, P. (2022). Gradients without Backpropagation. https://arxiv.org/abs/2202.08587 — Explains backpropagation as a special case of AD alongside forward mode, and proposes forward gradients as an alternative.

### Articles and documentation

- Paszke, A. et al. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. NeurIPS. https://arxiv.org/abs/1912.01703 — Describes PyTorch's design, a Python-first framework whose runtime includes the autograd engine that implements reverse mode.
