---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/mlops
- engineering/hardware
- theory/models/transformer/kv-cache
tags:
- model compression
- quantisation
- low-precision inference
aliases:
  - Quantization
  - Quantisation
  - Post-training quantisation
  - 量化
  - 量子化
---

# Quantisation

Quantisation stores and computes with numbers that use fewer bits, such as 8-bit integers, 4-bit integers or 8-bit floating point, in place of 16- or 32-bit floats. It is the most widely deployed form of [model compression](../index.md), because it reduces memory and often speeds up matrix multiplication on hardware built for low precision.

## Overview

Uniform affine quantisation maps a real value \(x\) to a \(b\)-bit integer \(q\):

\[
q = \operatorname{clip}\!\left(\operatorname{round}\!\left(\frac{x}{s}\right) + z,\ 0,\ 2^b - 1\right), \qquad \hat{x} = s\,(q - z)
\]

where \(s\) is a scale and \(z\) a zero point. Choosing \(s\) from the range of the values sets the rounding error. Using one scale per tensor is cheap but sensitive to outliers. Per-channel scales, or per-group scales over blocks of 32 to 128 values, are more accurate and are standard for weights in large language models.

## Key concepts

- **Weight-only versus weight-and-activation quantisation.** Weight-only methods keep activations in 16 bits, which saves memory but not much compute. Quantising activations as well allows integer matrix multiplication, but activations contain outliers that make this harder.
- **Post-training quantisation (PTQ).** The model is quantised after training, using a small calibration set to pick scales. It needs no training run.
- **Quantisation-aware training (QAT).** Rounding is simulated during training. Gradients pass through the rounding with a straight-through estimator, so the weights adapt to the grid.
- **Outliers.** A small number of channels in large transformers carry values much larger than the rest. Handling them is the central difficulty of low-bit quantisation.
- **Number formats.** INT8 and INT4 use integer arithmetic. FP8 and FP4 keep a floating-point exponent, which handles a wide range of values better and is supported by recent accelerators; see [AI hardware](../../../engineering/hardware/index.md).

## How it works

Quantising a single layer with weights \(W\) and calibration inputs \(X\) means choosing quantised weights \(\hat{W}\) that minimise the output error \(\lVert WX - \hat{W}X \rVert^2\), not the weight error. Modern PTQ methods exploit this. Three approaches are shown below, each with its own key idea.

## Key methods

### LLM.int8() (Dettmers et al., 2022)

- **Problem:** Large transformers develop a few hidden-state dimensions with very large magnitudes. Quantising everything to 8 bits degrades quality sharply once a model is large enough, so the model does not fit in memory at full quality.
- **Core idea:** Split each matrix multiplication. The few outlier dimensions are computed in 16-bit precision, and the rest in 8-bit integers with vector-wise scales. The method is called mixed-precision decomposition.
- **Equation or algorithm:** The product of the input \(X\) and weights \(W\) is written as a sum over normal dimensions, quantised to int8, plus a sum over outlier dimensions computed in fp16. Each row of \(X\) and column of \(W\) has its own scale.
- **Results:** The abstract reports that the method cuts the memory needed for inference by half while keeping full-precision performance.
- **Limitations:** Mixed-precision decomposition adds overhead for the outlier path, and the method targets 8-bit precision. Lower-bit inference needs other methods.

### GPTQ (Frantar et al., 2022)

- **Problem:** Rounding each weight to the nearest grid value, as in round-to-nearest quantisation, ignores the effect of the rounding on the other weights. At 3 or 4 bits the error accumulates and quality drops.
- **Core idea:** Quantise the weights of one layer one column at a time. After each column is rounded, the rounding error is compensated by updating the not-yet-quantised columns, using approximate second-order information from the calibration inputs.
- **Equation or algorithm:** The method follows the optimal brain quantisation framework, which uses the inverse Hessian \(H^{-1}\) of the layer's squared error to decide which weight to round and how to update the rest. GPTQ makes this efficient for models with billions of parameters by processing columns in blocks and using a Cholesky decomposition.
- **Results:** The abstract reports that GPTQ can quantise GPT models with 175 billion parameters in about four GPU hours, reducing the weights to 3 or 4 bits.
- **Limitations:** Calibration uses a small dataset, so the result depends on how well it matches the target domain. Speed-ups during inference require kernels that support the packed format.

### AWQ (Lin et al., 2023)

- **Problem:** Weights that matter most are not the largest in magnitude. Quantising all weights uniformly loses accuracy on the few channels that carry large activations.
- **Core idea:** Identify salient channels from activation statistics, not weight magnitude. Scale those channels up before quantisation, so that their relative rounding error falls. The inverse scale is absorbed into the previous operation, so the network is mathematically unchanged in full precision.
- **Equation or algorithm:** For a channel with scale \(s\), the layer computes \((W\,\mathrm{diag}(s)) \cdot (\mathrm{diag}(s)^{-1}X)\). The scales are chosen by a grid search that minimises the output error on calibration data.
- **Results:** The authors report that protecting only about 1% of salient weights greatly reduces quantisation error. The paper received the best paper award at MLSys 2024.
- **Limitations:** The search for scales costs calibration time. Like other PTQ methods, it targets weight-only quantisation, so activations stay at higher precision.

## Related methods

- **Integer-only inference** (Jacob et al., 2017): quantisation-aware training that makes every operation in a convolutional network integer-valued. It is the basis of many mobile deployment toolchains.
- **SmoothQuant** (Xiao et al., 2022): moves the difficulty of activation outliers into the weights by a per-channel scaling, so that both weights and activations can be quantised to 8 bits. The abstract reports up to 1.56 times speed-up and 2 times memory reduction for large language models with negligible accuracy loss.
- **KV-cache quantisation**: stores the attention cache in fewer bits. See [KV cache management](../../../theory/models/transformer/kv-cache/index.md).

## Variants

Each method family has its own page with key methods and open issues:

- [Quantisation-aware training](quantisation-aware-training/index.md): learned step size and integer-only inference.
- [Binary and ternary](binary-and-ternary/index.md): BinaryConnect, XNOR-Net and ternary weight networks.
- [Mixed precision](mixed-precision/index.md): choosing bit-widths per layer with Hessian-based sensitivity.

## Trade-offs

- **Bits versus quality.** Going from 8 to 4 bits roughly halves memory again, but quality loss grows and depends on the task. Reasoning and long-context tasks are often the first to degrade.
- **Calibration cost versus accuracy.** PTQ is cheap but limited; QAT recovers more accuracy at the price of a training run.
- **Format versus hardware.** A format that saves memory may not speed up inference unless the chip and kernel library support it.

## Connections

Quantisation is a standard step in [serving large models](../../../engineering/mlops/index.md) and underlies the QLoRA fine-tuning method in [training](../../../engineering/training/index.md). The number formats it uses are set by [hardware](../../../engineering/hardware/index.md). Low-precision and noisy computation also appears in neuroscience, where neurons transmit information with limited precision; the question of how much precision a useful system needs is shared by both fields.

## Applications

- **Local language models** run quantised weights on consumer laptops and phones.
- **Cloud inference** serves more concurrent users per GPU at lower cost.
- **Embedded vision** runs detectors on small chips for robotics and cameras.

## Open questions

- **Four bits and below.** Quality at 2 and 3 bits, especially for reasoning, is still an active research area.
- **Outliers in activations.** Methods differ in how they treat outliers in keys, values and activations, and no single rule is clearly best.
- **Evaluation.** Small drops in benchmark scores can hide large changes in behaviour, such as refusal or calibration. Better tests are needed.
- **Training-time quantisation at scale.** Quantisation-aware pre-training of very large models is harder to tune than post-training methods.

## References

### Seminal papers

- Jacob, B., et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Quantisation-aware training that keeps every operation in integer arithmetic, the basis of many mobile deployments.
- Dettmers, T., Lewis, M., Belkada, Y., Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS. https://arxiv.org/abs/2208.07339 — Mixed-precision 8-bit inference that keeps outlier dimensions in 16 bits.
- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. ICLR 2023. https://arxiv.org/abs/2210.17323 — Layer-wise, second-order error compensation for 3 and 4 bit weights.
- Lin, J., et al. (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. MLSys 2024. https://arxiv.org/abs/2306.00978 — Chooses per-channel scales from activation statistics to protect salient weights.
- Xiao, G., et al. (2022). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. arXiv:2211.10438. https://arxiv.org/abs/2211.10438 — Migrates activation outliers into weights so that both can be 8-bit.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews precision reduction methods and their trade-offs.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
