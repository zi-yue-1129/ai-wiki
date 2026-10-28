---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - architecture
  - sparse models
  - conditional computation
aliases:
  - Sparsely-gated mixture of experts
  - Outrageously large neural networks
  - 稀疏閘控混合專家
---

# Sparsely-Gated Mixture of Experts

Shazeer et al. (2017) introduced a sparsely-gated mixture-of-experts layer with up to thousands of expert networks, of which a trainable gate selects only a few for each example. They applied it convolutionally between stacked LSTM layers, with up to 137 billion parameters in the layer. The parent overview is [Mixture of Experts](index.md).

## Overview

The paper showed that conditional computation, where each example uses only part of the network, can raise model capacity by a large factor. Its gated design became the template that later sparse Transformers build on.

## Problem

Model quality usually improves with the number of parameters, but compute and memory also grow with that number, because every parameter is used for every example. Dense models therefore limit capacity. The question is whether a layer can hold many parameters while using only a small part of them for each input.

## Core idea

Replace a dense layer by a set of experts and a gating network. The gate outputs a score for each expert, keeps only the largest few, and sums the outputs of those experts weighted by their gate values. Experts that are not selected do no work for that example.

## Algorithm

For an input \(x\), the layer computes

\[
y = \sum_{i \in \mathrm{TopK}(G(x))} G(x)_i\, E_i(x),
\]

where \(E_i\) is the \(i\)-th expert and \(G(x)\) is the gate's output vector, with all entries outside the top \(k\) set to zero. The gate and the experts are trained jointly by gradient descent, and the gate's sparsity keeps the cost of the layer close to that of a small network.

## Key results

The abstract reports a mixture of experts with up to 137 billion parameters, applied convolutionally between stacked LSTM layers. It claims greater than a thousandfold improvement in model capacity. The abstract does not give specific perplexity or BLEU scores, so this page quotes none.

## Limitations

- Experts can become unevenly used, with the gate favouring a few of them. Balancing terms are needed to prevent this.
- The experts must be spread across devices, so the layer depends on communication between them, which limits scaling in practice.
- The gains were shown for LSTM-based language and translation models, and the transfer to Transformers came later with other designs.

## Connections

- [Mixture of Experts](index.md) is the overview, where this paper's gated design sits beside the original adaptive mixtures and the later routing variants.
- [Switch Transformer](switch-transformer.md) simplifies this gate to a single expert per token.
- [Mixtral](mixtral.md) uses a top-2 gate in a Transformer.
- [Transformer](../transformer/index.md) is the architecture into which the layer was later adopted.

## Applications

- Language modelling and translation at scales that dense networks could not reach at the same cost.

## Open questions

- Which balancing terms give experts the most specialisation without idle capacity?
- How does the top-k choice trade quality against communication cost at large scale?

## References

### Seminal papers

- Shazeer, N., Mirhoseini, A., Maziarz, K., Davis, A., Le, Q., Hinton, G. & Dean, J. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. ICLR 2017. https://arxiv.org/abs/1701.06538 — Introduces a sparsely gated mixture of experts with up to 137 billion parameters, raising capacity with modest efficiency loss.
- Jacobs, R. A., Jordan, M. I., Nowlan, S. J. & Hinton, G. E. (1991). Adaptive Mixtures of Local Experts. *Neural Computation*, 3(1), 79–87. https://doi.org/10.1162/neco.1991.3.1.79 — The dense gated mixture that this layer makes sparse.
- Lepikhin, D., et al. (2020). *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*. arXiv. https://arxiv.org/abs/2006.16668 — Applies sparsely gated experts to Transformer translation at more than 600 billion parameters.
- Fedus, W., Zoph, B. & Shazeer, N. (2022). *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. JMLR 23. https://www.jmlr.org/papers/v23/21-0998.html — Simplifies the top-k gate to a single expert per token.
- Jiang, A. Q., et al. (2024). *Mixtral of Experts*. arXiv. https://arxiv.org/abs/2401.04088 — An open-weight sparse Transformer with eight experts, two active per token.

### Surveys and textbooks

- Fedus, W., Dean, J. & Zoph, B. (2022). *A Review of Sparse Expert Models in Deep Learning*. arXiv. https://arxiv.org/abs/2209.01667 — Review of sparse expert models and the common algorithms behind them.
