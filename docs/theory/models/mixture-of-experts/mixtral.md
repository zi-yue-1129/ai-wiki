---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
  - theory/models/llm
tags:
  - architecture
  - sparse models
  - open-weight models
aliases:
  - Mixtral
  - Mixtral 8x7B
  - Mixtral of experts
  - Mixtral 專家模型
---

# Mixtral 8x7B

Mixtral 8x7B is an open-weight sparse Transformer in which each layer has eight feed-forward experts and a router that selects two of them for each token. Jiang et al. (2024) report that it has 47 billion parameters in total but uses only 13 billion of them for each token. The parent overview is [Mixture of Experts](index.md).

## Overview

Mixtral applies the sparse idea to a modern decoder-only Transformer. The model keeps the total size of a much larger dense model, while its per-token compute is close to that of a model with 13 billion parameters.

## Problem

Dense language models of 70 billion parameters are costly to run at inference. The question is whether a sparse model with a similar total capacity can match them at a fraction of the active compute per token.

## Core idea

In each layer, a router scores the eight experts for the current token and sends it to the two highest-scoring ones. Their outputs are combined with the router's normalised weights. Because the choice is per token and per layer, different tokens can use different experts.

## Algorithm

For the hidden state \(h\) of a token, the router computes scores over the eight experts, selects the top two, and returns a weighted sum of their feed-forward outputs. The attention layers are shared across all tokens and are not sparse. The same routing is applied in every layer.

## Key results

The abstract reports that each token has access to 47 billion parameters but uses 13 billion during inference. It says the model vastly outperforms Llama 2 70B on mathematics, code generation and multilingual benchmarks, and that it outperforms or matches Llama 2 70B and GPT-3.5 across all evaluated benchmarks. The abstract gives the comparisons in words, so this page quotes no individual benchmark scores.

## Limitations

- The total parameter count still has to be stored, so memory needs are those of a much larger model, even though compute is lower.
- Serving the model requires moving tokens between experts, which costs communication when experts are spread over devices.
- The results are reported against specific baselines, and the abstract does not give a full training recipe.

## Connections

- [Mixture of Experts](index.md) is the overview where Mixtral's top-2 routing sits beside the top-1 and top-k designs.
- [Switch Transformer](switch-transformer.md) routes to one expert, where Mixtral routes to two.
- [Sparsely-gated MoE](sparsely-gated.md) introduced the top-k gate that Mixtral uses.
- [Large language models](../llm/index.md) is the setting in which Mixtral is one of the best-known open-weight examples.

## Applications

- Open-weight deployment of a large model where per-token compute must stay near that of a smaller model.
- Multilingual and code-generation tasks, where the paper reports the largest gains.

## Open questions

- How much of Mixtral's quality comes from the sparse design, and how much from the training data and recipe?
- How do expert specialisation patterns change with the number of experts and the top-k choice?

## References

### Seminal papers

- Jiang, A. Q., Sablayrolles, A., Roux, A., et al. (2024). *Mixtral of Experts*. arXiv. https://arxiv.org/abs/2401.04088 — An open-weight sparse Transformer with eight experts, two active per token, and 47 billion total parameters.
- Shazeer, N., et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv. https://arxiv.org/abs/1701.06538 — The sparse top-k gate that Mixtral uses in each layer.
- Fedus, W., Zoph, B. & Shazeer, N. (2021). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. arXiv. https://arxiv.org/abs/2101.03961 — Top-1 routing, for comparison with Mixtral's top-2.
- Lepikhin, D., et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv. https://arxiv.org/abs/2006.16668 — Sparse Transformer experts at scale, with automatic sharding.
- Jacobs, R. A., Jordan, M. I., Nowlan, S. J. & Hinton, G. E. (1991). Adaptive Mixtures of Local Experts. *Neural Computation*, 3(1), 79–87. https://doi.org/10.1162/neco.1991.3.1.79 — The original mixture of experts.

### Surveys and textbooks

- Fedus, W., Dean, J. & Zoph, B. (2022). *A Review of Sparse Expert Models in Deep Learning*. arXiv. https://arxiv.org/abs/2209.01667 — Review of sparse expert models and the common algorithms behind them.
