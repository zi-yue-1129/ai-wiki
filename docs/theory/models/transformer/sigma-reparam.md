---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization/weight-norm-dynamics
tags:
  - transformer
  - attention
  - reparameterisation
  - training stability
aliases:
  - σReparam
  - Spectral reparameterisation
  - σ 重參數化
---

# σReparam

σReparam reparameterises every linear layer of a Transformer by its spectral norm, multiplied by a learnable scalar. Zhai et al. (2023) use it to prevent attention entropy collapse, which they connect to the spectral norm of the product of the query and key weights. The method removes the need for some of the usual stabilisers, such as pre-normalisation and learning-rate warm-up. The parent overview is [Transformers & Attention](index.md), and the norm analysis it relies on is on the [weight-norm dynamics](../../optimization/weight-norm-dynamics/index.md) page.

## Overview

A linear layer with weight \(W\) is replaced by \(\hat W = \dfrac{\gamma}{\sigma(W)}\,W\), where \(\sigma(W)\) is the largest singular value of \(W\), and \(\gamma\) is a learnable scalar. The spectral norm of \(\hat W\) is then set by \(\gamma\), and not by the scale of \(W\). The parameter that controls the spectral norm is therefore separate from the matrix that does the work.

## Problem

Zhai et al. analyse attention in terms of the matrix \(W_K W_Q^\top\). They prove that the entropy of the attention distribution has a lower bound that falls exponentially as the spectral norm of this product grows. When the norm grows, attention becomes close to a single position, and the training instability coincides with the entropy falling towards zero. Their experiments show that doubling the learning rate drives the entropy close to zero.

## Core idea

Bound the spectral norm of every linear layer directly, rather than only the query and key projections or the output projection. With \(\hat W = (\gamma/\sigma(W))\,W\), the spectral norm of each layer is controlled by a single scalar that the optimiser can learn. The same parameterisation is applied to the query, key, value, output and feed-forward layers.

## How it works

1. For each linear layer, estimate the largest singular value \(\sigma(W)\) with a few steps of power iteration, as in spectral normalisation.
2. Compute the reparameterised weight \(\hat W = (\gamma/\sigma(W))\,W\), with a learnable \(\gamma\) per layer.
3. Use \(\hat W\) in the forward pass, and let the optimiser update \(W\) and \(\gamma\).
4. Monitor the attention entropy during training, since the method is motivated by it.

## Results

The paper reports that σReparam trains a ViT-B on ImageNet to accuracy comparable to DeiT without pre-normalisation, warm-up or weight decay, and that plain spectral normalisation and weight normalisation do worse in the authors' comparison. The exact numbers are in the paper's tables and should be checked there before use.

## Limitations

- The method changes the parameterisation of every linear layer, so it is not a drop-in change for an existing checkpoint.
- The power-iteration estimate of the spectral norm adds a small cost per step, and the paper's comparisons are for specific architectures and tasks.
- Bounding the spectral norm limits the entropy collapse predicted by the theorem, but it does not prove that the attention stays discriminative. The rank collapse analysed by Noci et al. (2022) is a separate failure mode.

## Connections

- [QK-normalisation](qk-norm.md) is the alternative that normalises the query and key vectors instead of the weights.
- [Weight-norm dynamics](../../optimization/weight-norm-dynamics/index.md) explains why the norm of a layer keeps changing during training.
- [Transformers & Attention](index.md) describes the attention block whose entropy the method protects.

## Open questions

- Whether a learned scalar per layer is enough for very large models, or whether the scalar must be tuned per layer.
- How the parameterisation interacts with the weight decay used at large scale, given that the spectral norm is no longer set by the weight norm.

## References

- Zhai, S., Likhomanenko, T., Littwin, E., et al. (2023). *Stabilizing Transformer Training by Preventing Attention Entropy Collapse*. ICML 2023, PMLR 202:40770–40803. https://proceedings.mlr.press/v202/zhai23a.html — introduces σReparam and the attention-entropy bound.
- Dehghani, M., Djolonga, J., Mustafa, B., et al. (2023). *Scaling Vision Transformers to 22 Billion Parameters*. ICML 2023, PMLR 202:7480–7512. https://proceedings.mlr.press/v202/dehghani23a.html — a different stabilising change for the same problem, query-key normalisation.
- Wortsman, M., Liu, P. J., Xiao, L., et al. (2023). *Small-scale proxies for large-scale Transformer training instabilities*. arXiv:2309.14322. https://arxiv.org/abs/2309.14322 — tests attention-logit and output-logit instabilities at small scale.
- Noci, L., Anagnostidis, S., Biggio, L., et al. (2022). *Signal Propagation in Transformers: Theoretical Perspectives and the Role of Rank Collapse*. arXiv:2206.03126. https://arxiv.org/abs/2206.03126 — analyses rank collapse, a failure that bounding norms does not remove.
- Xiong, R., Yang, Y., He, D., et al. (2020). *On Layer Normalization in the Transformer Architecture*. ICML 2020. https://arxiv.org/abs/2002.04745 — studies the placement of normalisation, which σReparam partly replaces.
