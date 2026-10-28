---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - architecture
  - sparse models
  - scaling
aliases:
  - Switch Transformer
  - Switch layer
  - 開關 Transformer
---

# Switch Transformer

The Switch Transformer routes each token to a single expert, rather than to several. Fedus, Zoph and Shazeer (2021) showed that this simpler routing keeps the compute per token constant while the number of parameters grows to the trillion scale, and reported large pre-training speed-ups over dense T5 models. The parent overview is [Mixture of Experts](index.md).

## Overview

Earlier sparse layers used the top-k gate, with k of two or more, which increases compute and complicates the routing. Switch keeps the sparse idea and reduces k to one. The authors call this the Switch layer.

## Problem

Top-k routing with k of two or more multiplies the compute per token and adds complexity in the communication and the batching. The question is whether a single-expert choice is enough to get the capacity benefit of sparsity, without its cost.

## Core idea

For each token, a router produces a probability over the experts and sends the token to the highest-probability expert only. The expert's output is scaled by that probability, so the router still receives a gradient signal. Each token therefore uses one expert's parameters and the same compute as a dense layer of that size.

## Algorithm

For a token representation \(x\) and a router weight matrix \(W_r\), the router computes \(p = \mathrm{softmax}(W_r x)\), chooses \(i = \arg\max_j p_j\), and outputs \(p_i\, E_i(x)\). The paper uses a load-balancing loss to encourage the router to spread tokens across experts, and a capacity limit per expert.

## Key results

The abstract reports that the sparse models reach up to trillion-parameter scale, and that they achieve up to a 7× increase in pre-training speed with the same computational resources, compared with T5-Base and T5-Large. The trillion-parameter models achieve a 4× speed-up over T5-XXL. It also states that large sparse models can be trained in lower-precision bfloat16 formats for the first time.

## Limitations

- The top-1 choice is discrete, so the router's decisions are not differentiable, and the gradient reaches it only through the scaling by the chosen probability.
- Each token sees only one expert per layer, which can limit how much the layer can combine knowledge from several specialists.
- Parameter memory still grows with the number of experts, even though compute does not.

## Connections

- [Mixture of Experts](index.md) is the overview, where this single-expert routing sits beside the top-k designs.
- [Sparsely-gated MoE](sparsely-gated.md) uses the top-k gate that this paper simplifies.
- [Mixtral](mixtral.md) uses top-2 routing instead of top-1.
- [Transformer](../transformer/index.md) is the architecture the feed-forward block belongs to.

## Applications

- Pre-training very large language models where compute per token must stay fixed.
- Large-scale multilingual pre-training, where the paper's speed-ups matter most.

## Open questions

- Does the top-1 choice limit quality for tasks that need several specialists at once, and how does it compare with top-2 at equal compute?
- How should capacity limits be set so that dropped tokens do not harm training?

## References

### Seminal papers

- Fedus, W., Zoph, B. & Shazeer, N. (2022). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. JMLR 23. https://www.jmlr.org/papers/v23/21-0998.html — Routes each token to a single expert and reports up to 7× pre-training speed-up at constant compute per token.
- Shazeer, N., et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. ICLR 2017. https://arxiv.org/abs/1701.06538 — The top-k sparse gate that this paper simplifies.
- Jacobs, R. A., Jordan, M. I., Nowlan, S. J. & Hinton, G. E. (1991). Adaptive Mixtures of Local Experts. *Neural Computation*, 3(1), 79–87. https://doi.org/10.1162/neco.1991.3.1.79 — The original mixture of experts, with a dense gating network.
- Lepikhin, D., et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv. https://arxiv.org/abs/2006.16668 — Sparse experts at Transformer scale with automatic sharding, a setting that Switch's simpler routing also targets.
- Jiang, A. Q., et al. (2024). *Mixtral of Experts*. arXiv. https://arxiv.org/abs/2401.04088 — A later sparse Transformer that uses top-2 routing, for comparison.

### Surveys and textbooks

- Fedus, W., Dean, J. & Zoph, B. (2022). *A Review of Sparse Expert Models in Deep Learning*. arXiv. https://arxiv.org/abs/2209.01667 — Review of sparse expert models and the common algorithms behind them.
