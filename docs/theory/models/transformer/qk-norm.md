---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization/weight-norm-dynamics
tags:
  - transformer
  - attention
  - normalisation
  - training stability
aliases:
  - QK-norm
  - QK normalisation
  - QK 正規化
---

# QK-Normalisation

QK-normalisation applies a layer normalisation to the queries and keys of each attention head before their dot product. It bounds the attention logits regardless of how large the query and key weights become. Dehghani et al. (2023) introduced it as a stability fix for training Vision Transformers at 22 billion parameters. The parent overview is [Transformers & Attention](index.md), and the broader norm-growth problem is on the [weight-norm dynamics](../../optimization/weight-norm-dynamics/index.md) page.

## Overview

In standard scaled dot-product attention, the logits are \(QK^\top/\sqrt{d_k}\). If the weights that produce \(Q\) and \(K\) grow, the logits grow with them, and the softmax can become nearly one-hot. Once that happens, the gradients to the attention parameters become very small or very unstable. QK-normalisation inserts a normalisation on \(Q\) and \(K\) so that the logits depend on the direction of the vectors, not their length.

## Problem

Dehghani et al. report that, when training very large Vision Transformers, the attention logits grew without control. The softmax then concentrated on a few positions, and training diverged. The paper's remedy is the normalisation described below.

## Core idea

Apply a layer normalisation to the query and key vectors of each head before the dot product, so that \(\text{softmax}\!\left(\text{LN}(Q)\,\text{LN}(K)^\top/\sqrt{d_k}\right)\). The normalisation removes the scale of \(Q\) and \(K\) from the logits, so the logits no longer grow with the weight norms that produce them.

## How it works

1. Project the input to queries, keys and values as usual.
2. Apply a layer normalisation to each head's queries and to each head's keys, with its own learnable gain and bias.
3. Compute the scaled dot product of the normalised queries and keys, then the softmax, as in standard attention.
4. Leave the value projection and the rest of the block unchanged.

The modification is local to attention, and the cost is one normalisation per head for queries and keys.

## Results

Wortsman et al. (2023) test the mechanism at small scale. They report that adding query-key layer normalisation makes the attention logits stay bounded, and that it raises the largest learning rate that trains stably. Their experiments separate attention-logit growth from output-logit divergence, and QK-normalisation addresses the first but not the second. The exact sweep figures should be taken from the paper.

## Limitations

- QK-normalisation bounds the attention logits, but it does not bound the norms of the output projection or the feed-forward layers. Those can keep growing, as the weight-norm analysis predicts.
- The bound is on the logit scale, and the attention can still collapse in rank or entropy. Zhai et al. (2023) link collapse to the spectral norm of the query-key product, and Noci et al. (2022) to rank collapse of the token representations.
- The reported benefit is mainly training stability. Claims about final accuracy depend on the experiments in each paper and should be checked there.

## Connections

- [Transformers & Attention](index.md) describes the attention block that QK-normalisation changes.
- [σReparam](sigma-reparam.md) is the alternative that reparameterises every linear layer by its spectral norm.
- [Weight-norm dynamics](../../optimization/weight-norm-dynamics/index.md) covers the norm growth that QK-normalisation does not address on its own.
- [Attention variants](attention-variants/index.md) covers changes to the attention operation for efficiency.

## Open questions

- Whether query-key normalisation is enough in very long-context models, where the logits are summed over many more positions.
- How the normalisation interacts with rotary position encodings, which act on the same query and key vectors.

## References

- Dehghani, M., Djolonga, J., Mustafa, B., et al. (2023). *Scaling Vision Transformers to 22 Billion Parameters*. ICML 2023, PMLR 202:7480–7512. https://proceedings.mlr.press/v202/dehghani23a.html — introduces query-key layer normalisation for large Vision Transformers.
- Wortsman, M., Liu, P. J., Xiao, L., et al. (2023). *Small-scale proxies for large-scale Transformer training instabilities*. arXiv:2309.14322. https://arxiv.org/abs/2309.14322 — tests query-key normalisation and other remedies at small scale.
- Zhai, S., Likhomanenko, T., Littwin, E., et al. (2023). *Stabilizing Transformer Training by Preventing Attention Entropy Collapse*. ICML 2023, PMLR 202:40770–40803. https://proceedings.mlr.press/v202/zhai23a.html — links attention collapse to the spectral norm of the query-key product.
- Noci, L., Anagnostidis, S., Biggio, L., et al. (2022). *Signal Propagation in Transformers: Theoretical Perspectives and the Role of Rank Collapse*. arXiv:2206.03126. https://arxiv.org/abs/2206.03126 — analyses rank collapse in stacked attention and its effect on gradients.
- Xiong, R., Yang, Y., He, D., et al. (2020). *On Layer Normalization in the Transformer Architecture*. arXiv:2002.04745. https://arxiv.org/abs/2002.04745 — studies where normalisation should sit in the Transformer block.
