---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/mlops
- engineering/training
- engineering/hardware
- theory/models/transformer/kv-cache
- brain-mind/neuroscience
tags:
- model compression
- efficiency
- deployment
aliases:
  - Model Compression
  - 模型壓縮
  - 模型压缩
---

# Model Compression

Model compression reduces the memory, computation, energy or latency that a trained model needs, while keeping as much of its behaviour as possible. It matters because a model that is accurate in a data centre may be too large for a phone, too slow for a car's control loop, or too expensive to serve to millions of users.

## Overview

A trained network is usually over-parameterised. Many weights contribute little to its outputs, and many values are stored with more precision than the task needs. Compression exploits this redundancy in four main ways:

| Family | What is reduced | Typical trade-off | Page |
|---|---|---|---|
| Quantisation | Bits per number (weights, activations, cache) | Rounding error; needs calibration | [Quantisation](quantisation/index.md) |
| Pruning | Number of weights, channels or heads | Accuracy loss at high sparsity; speed-up depends on hardware | [Pruning](pruning/index.md) |
| Knowledge distillation | Size of the model itself | Student quality bounded by teacher and data | [Knowledge distillation](knowledge-distillation/index.md) |
| Low-rank factorisation | Parameters in large matrices | Loss when weight matrices have high effective rank | [Low-rank factorisation and efficient architectures](low-rank-and-efficient-architectures/index.md) |

Compression is usually applied **after** training, which is called post-training compression. Training-aware methods, such as quantisation-aware training or distillation, change the training run itself and usually recover more quality at the same size. Efficient architecture design, such as depthwise-separable convolutions or grouped-query attention, is a related but different strategy: it chooses a small model before training rather than shrinking a large one.

## Key concepts

- **Compression ratio**: original size divided by compressed size. A reported ratio is meaningful only with the accuracy it preserved.
- **Accuracy–size frontier**: the set of models that cannot be made smaller without losing accuracy. Papers compare methods by how far they push this frontier.
- **Structured versus unstructured**: unstructured methods remove individual values and leave irregular sparsity; structured methods remove whole channels, heads or blocks, which dense hardware can exploit directly.
- **Hardware dependence**: a 90% sparse matrix is only faster if the hardware and software can skip the zeros. Savings in parameters and savings in latency are different numbers.
- **Calibration data**: post-training methods estimate statistics from a small sample of inputs. Its size and similarity to deployment data affect the result.
- **Composition**: methods combine. Han et al. (2016) stacked pruning, quantisation and entropy coding in one pipeline.

## How it works

Most methods share a loop: score the importance of each part of the model, remove or round the least important parts, then repair the damage. The repair step is what separates a method that works at large compression from one that does not. It may be fine-tuning on labelled data, reconstruction of each layer's output on a small calibration set, or simple distillation from the original model.

### Low-rank factorisation

The method pages for this family, covering truncated SVD, low-rank filter expansion and LoRA, are under [low-rank factorisation and efficient architectures](low-rank-and-efficient-architectures/index.md).

A weight matrix \(W \in \mathbb{R}^{m \times n}\) can be approximated by the product of two thinner matrices, \(W \approx UV\) with \(U \in \mathbb{R}^{m \times r}\) and \(V \in \mathbb{R}^{r \times n}\). The truncated singular value decomposition gives the best rank-\(r\) approximation in the Frobenius norm. The parameter count falls from \(mn\) to \(r(m+n)\), which is a saving whenever \(r\) is small relative to the dimensions.

Low-rank compression works only when the matrix is close to low rank. Many trained layers are, but the approximation error can grow quickly for the layers that matter most. Low-rank adaptation (LoRA) uses the same mathematics during fine-tuning, to learn a small update \(BA\) on top of frozen weights. LoRA does not compress the base model, and it is covered under [training and fine-tuning](../../engineering/training/index.md).

### Efficient architectures

Some models are designed to be small from the start. MobileNet replaced standard convolutions with depthwise-separable ones. Multi-query and grouped-query attention share keys and values across heads to shrink the [KV cache](../../theory/models/transformer/kv-cache/index.md). Mixture-of-experts layers keep total parameters large while activating only a few per token. These are architectural choices, so they belong with the model families under [Models](../models/index.md).

## Composed pipelines

Methods are often combined in one pipeline. [Deep Compression](deep-compression/index.md) chains pruning, codebook quantisation and Huffman coding, and its page sets out the stages, the storage results and their limits.

## Connections

Compression links to [MLOps and deployment](../../engineering/mlops/index.md), where serving cost and quantised models are chosen in practice, and to [AI hardware](../../engineering/hardware/index.md), because the precision formats and sparsity patterns that chips support decide which methods pay off. The [KV cache](../../theory/models/transformer/kv-cache/index.md) is compressed by many of the same ideas.

The brain offers an analogy. Developing neural systems overproduce synapses and then eliminate many of them, and the brain runs on noisy, low-precision components. Whether these facts explain why biological computation is efficient is an open question; see [neuroscience](../../brain-mind/neuroscience/index.md) and the [information-theory](../../theory/information-theory/index.md) view of efficient coding.

## Applications

- **On-device models.** Quantised language and vision models run on laptops and phones, where memory and battery are limited.
- **Serving at scale.** Providers serve large models at lower cost by using low-bit weights, sparse kernels and distilled models for easy requests.
- **Embedded and robotic systems.** Perception models run within the power and latency budgets of vehicles and drones.
- **Scientific computing.** Surrogate models are compressed so that simulations can run on modest hardware.

## Open questions

- **Evaluation beyond perplexity.** Compressed models can keep perplexity while losing reasoning, long-context retrieval or calibration. Benchmarks that measure these are still limited.
- **Compression of reasoning models.** How much of a long chain of reasoning survives quantisation or pruning is not well measured.
- **Combining methods.** The best ordering and interaction of quantisation, pruning and distillation is largely empirical.
- **Hardware support.** Unstructured sparsity offers large parameter savings but few speed-ups on current accelerators.

## References

### Seminal papers

- Han, S., Mao, H., Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR. https://arxiv.org/abs/1510.00149 — Combines pruning, codebook quantisation and Huffman coding, reporting 35 to 49 times storage reduction.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — Introduces training a small model on the soft outputs of a large one.
- Jacob, B., et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Quantisation-aware training with integer-only inference, the basis of many deployment pipelines.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — A broad survey of sparsity methods across training and inference.
- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews numerical precision reduction and its trade-offs.
- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation by knowledge type, training scheme and application.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Shows that simple magnitude pruning matches or beats more complex sparsity methods on large tasks.
- Dettmers, T., et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS. https://arxiv.org/abs/2208.07339 — Mixed-precision 8-bit inference for large language models, covered in the quantisation page.
