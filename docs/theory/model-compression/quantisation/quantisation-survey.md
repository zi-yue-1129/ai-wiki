---
related:
  - theory/model-compression/pruning
  - engineering/hardware/co-design
tags:
  - model compression
  - quantisation
  - inference
last_reviewed: 2026-11-01
aliases:
  - A Survey of Quantization Methods
  - Gholami quantisation survey
  - 神經網路量化方法綜述
---

# A Survey of Quantization Methods (Gholami et al., 2021)

Gholami, Kim, Dong and colleagues (2021) survey how neural network values can be represented with fewer bits, and how to keep accuracy while doing so. The survey is one of the standard entry points to quantisation. It covers the number formats, the two main ways of training or adjusting a quantised model, and the speed-ups that integer arithmetic can deliver (Gholami et al., 2021).

## Overview

Quantisation maps real-valued weights and activations to a small set of discrete levels. The survey frames the problem as a question about representation: how to spread continuous values over a fixed set of numbers so that the number of bits is small and the computation remains accurate. Memory and computation are the reasons to care. Fewer bits mean less data to move, and integer arithmetic can be faster than floating point on suitable hardware (Gholami et al., 2021).

## Key concepts

- **Uniform affine quantisation**: the paper writes a real value as an integer times a scale S, shifted by an integer zero point Z. The scale is set from a clipping range [α, β] and the bit width b, as S = (β − α)/(2^b − 1) (Section III-C).
- **Post-training quantisation (PTQ)**: quantise a trained model without retraining. It needs only a small calibration set (Section III-G.2).
- **Quantisation-aware training (QAT)**: simulate quantisation during training, so the weights are quantised after each gradient update (Section III-G.1).
- **Zero-shot quantisation**: quantise with no access to training or validation data (Section III-G.3).

## How it works

The survey separates the choice of numerical format from the choice of training procedure. For the format, it describes uniform affine quantisation and the effect of choosing the clipping range. For the procedure, it contrasts PTQ and QAT.

QAT retrains the model, and the paper names the computational cost of that retraining as its main drawback. The paper says the investment is likely to be worth it when a model will be deployed for a long time, and it notes that some models have a short lifetime (Section III-G.1). PTQ avoids retraining, and the paper says it often comes at a cost in accuracy compared with QAT (Section III-G.2).

## Key methods

Compare the families briefly, and read each method's own page for detail:

- [Post-training quantisation](post-training/index.md): calibrate a trained model without retraining, including methods built for large language models.
- [Quantisation-aware training](quantisation-aware-training/index.md): train with quantisation in the loop.
- [Integer-only inference](quantisation-aware-training/integer-only-inference/index.md): run the whole network in integer arithmetic.
- [Mixed precision](mixed-precision/index.md): choose the bit width layer by layer.

## Evidence and results

The abstract states that quantisation can represent values with four bits or less, and that reductions of four to eight times are often realised in practice. Section I says that performance can be kept at four times compression or more with INT8 and lower precision (Gholami et al., 2021).

For INT8, the paper says it is straightforward to deploy many models without losing accuracy (Section VI). Its hardware results report INT8 speed-ups of 3.89, 3.32 and 5.02 times for popular vision models on an NVIDIA GTX 1080, and up to 4.0 times faster inference than FP32 for BERT (Section VII).

## Limitations

- **Accuracy at low bit widths.** The survey notes that PTQ often comes at a cost in accuracy compared with QAT, so the choice depends on the budget for retraining and on how much accuracy is at stake.
- **Hardware dependence.** The speed-up figures come from particular hardware and kernels. An integer format helps only if the target runs it efficiently.
- **Formula conventions.** The paper's sign convention for the zero point differs between its quantisation and dequantisation equations, so readers should check the convention before reusing the formulas.

## Connections

- [Pruning and sparsity](../pruning/index.md) reduce the number of values, while quantisation reduces the precision of each value. The two can be combined.
- [Hardware co-design](../../../engineering/hardware/co-design/index.md) covers why integer and low-precision formats matter for accelerators.

## Applications

The survey is motivated by the memory and compute limits of constrained devices. Its hardware results concern vision models and BERT (Gholami et al., 2021).

## Open questions

- How far precision can drop before accuracy fails for a given architecture, without retraining.
- Which combination of format, calibration and training gives the best accuracy per byte for language models.

## References

### Seminal papers

- Gholami, A., Kim, S., Dong, Z., Yao, Z., Mahoney, M. W. & Keutzer, K. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv. https://arxiv.org/abs/2103.13630 — A survey of number formats, PTQ and QAT, and the hardware speed-ups discussed on this page.
- Jacob, B., Kligys, S., Chen, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv. https://arxiv.org/abs/1712.05877 — Integer-only inference with quantisation-aware training.
- Banner, R., Nahshan, Y. & Hoffer, E. (2018). *Post-training 4-bit quantization of convolution networks for rapid-deployment*. arXiv. https://arxiv.org/abs/1810.05723 — Post-training quantisation at four bits for convolutional networks.
- Dettmers, T., Lewis, M., Belkada, Y. & Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv. https://arxiv.org/abs/2208.07339 — Eight-bit matrix multiplication for large transformers.
- Frantar, E., Ashkboos, S., Hoefler, T. & Alistarh, D. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv. https://arxiv.org/abs/2210.17323 — Post-training quantisation for large language models at low bit widths.

### Surveys and white papers

- Nagel, M. et al. (2021). *A White Paper on Neural Network Quantization*. arXiv. https://arxiv.org/abs/2106.08295 — A white paper on PTQ and QAT methods for neural network quantisation.
