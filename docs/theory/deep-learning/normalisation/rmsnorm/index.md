---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/llm
  - theory/models/transformer
tags:
  - normalisation
  - transformers
  - efficient inference
aliases:
  - RMS Normalization
  - Root Mean Square Layer Normalization
  - RMSNorm
  - 均方根正規化
---

# Root Mean Square Layer Normalisation (RMSNorm)

RMSNorm normalises a layer's summed inputs by their root mean square alone, without subtracting the mean. Zhang and Sennrich introduced it in 2019 as a cheaper variant of [layer normalisation](../../../models/mlp/layer-normalisation/index.md). It is now a common choice in large language models. It is one of the methods described on the parent [normalisation layers](../index.md) page.

## Overview

Layer normalisation does two things: it re-centres the summed inputs of a layer by subtracting their mean, and it re-scales them by their standard deviation. Zhang and Sennrich hypothesised that re-scaling invariance is the reason for layer normalisation's success, and that re-centring is dispensable. Dropping it saves computation, and the method keeps the scale control that normalisation provides.

The method is most relevant to Transformers and recurrent networks, where layer normalisation runs at every sub-layer and at every time step. Large language models in the LLaMA family use RMSNorm in this way, applied to the input of each sub-layer.

## Key concepts

- **Re-centring and re-scaling.** Re-centring makes the mean of a layer's inputs zero. Re-scaling makes their spread fixed. Layer normalisation applies both; RMSNorm applies only the second.
- **Root mean square.** The square root of the average of the squared values. For zero-mean data this equals the standard deviation, but without the mean subtraction it does not depend on the centre of the data.
- **Gain.** A learned per-unit scale that restores the freedom to change the output magnitude.
- **Pre-normalisation.** Applying the normaliser to the input of each sub-layer, inside the residual branch. This is the placement used with RMSNorm in LLaMA; see the [parent page](../index.md) for the pre-norm and post-norm comparison.

## How it works

Let \(a\) be the vector of \(n\) summed inputs to a layer, with \(a_i\) the value for unit \(i\). The RMS normalisation is:

\[
\mathrm{RMS}(a) = \sqrt{\frac{1}{n}\sum_{i=1}^{n} a_i^2}, \qquad
\bar{a}_i = \frac{a_i}{\mathrm{RMS}(a)}\, g_i,
\]

where \(g\) is a learned gain for each unit. Compared with layer normalisation, the mean \(\mu\) is no longer computed and subtracted. The algorithm is:

1. Compute the mean of the squared inputs.
2. Take the square root to get the RMS.
3. Divide each input by the RMS.
4. Multiply each result by its gain \(g_i\).

The paper also proposes partial RMSNorm, written pRMSNorm, which estimates the RMS from a fraction \(p\) of the summed inputs. This reduces the cost further, at the price of a biased estimate of the RMS.

## Results

According to the abstract of Zhang and Sennrich (2019), RMSNorm achieves performance comparable to layer normalisation across several tasks and different network architectures, and it reduces running time by 7% to 64%, depending on the model. The experiments cover a GRU-based recurrent translation model and a self-attention Transformer, both on WMT14 English–German translation, along with other architectures. For the Transformer, the paper reports that training without any normalisation fails, and that RMSNorm reaches BLEU scores comparable to layer normalisation. The speed-up figures are reported for the paper's own implementations and setups, and were not re-run for this page.

## Limitations

- **Not invariant to all re-centring.** The paper notes that RMSNorm is not invariant to all re-centring operations, which layer normalisation is. Where the mean of the inputs carries information or shifts across inputs, the two methods can behave differently.
- **Speed depends on implementation.** The reported running-time reduction reflects the cost of the operations on the hardware and code used in the paper. The same saving may be smaller or larger elsewhere.
- **Evidence at scale.** The paper's experiments are on smaller models than current language models. Its later use in large models is evidence, but not a controlled comparison at that scale.

## Open questions

- **Does re-centring matter at scale?** Whether losing re-centring invariance affects training or quality in very large models, or only in some architectures, is not settled.
- **How small can \(p\) be?** How much of the inputs pRMSNorm can use before the estimate becomes too inaccurate to help is a question for further study.
- **Algorithmic or implementation gain?** It is not always clear how much of a speed advantage comes from the formula and how much from the fused kernels used to compute it.

## References

### Seminal papers

- Zhang, B. & Sennrich, R. (2019). "Root Mean Square Layer Normalization". arXiv:1910.07467 — Proposes RMSNorm, which drops the re-centring of layer normalisation, and reports comparable results at lower cost.
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). "Layer Normalization". arXiv:1607.06450 — The layer normalisation method that RMSNorm simplifies, normalising over the features of each example.
- Xiong, R., et al. (2020). "On Layer Normalization in the Transformer Architecture". arXiv:2002.04745 — Analyses where layer normalisation is placed in Transformers and why pre-norm placement trains more stably.

### Surveys and textbooks

- Huang, L., et al. (2020). "Normalization Techniques in Training DNNs: Methodology, Analysis and Application". arXiv:2009.12836 — A survey that places RMSNorm alongside the other normalisation methods in a common taxonomy.


### Articles and documentation

- Touvron, H., et al. (2023). "LLaMA: Open and Efficient Foundation Language Models". arXiv:2302.13971 — Describes a family of language models that normalise the input of each sub-layer with RMSNorm.
- Nguyen, T. Q. & Salazar, J. (2019). "Transformers without Tears: Improving the Normalization of Self-Attention". arXiv:1910.05895 — Compares normalisation placements and variants for Transformer training, including pre-norm settings.
