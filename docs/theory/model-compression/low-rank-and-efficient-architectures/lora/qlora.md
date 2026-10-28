---
status: complete
last_reviewed: 2026-10-28
related:
- engineering/training
- theory/model-compression/quantisation
tags:
- model compression
- quantisation
- low-rank factorisation
- fine-tuning
- large language models
aliases:
  - QLoRA
  - Quantized Low-Rank Adaptation
  - 量化低秩適應
---

# QLoRA

QLoRA fine-tunes a large model by training LoRA adapters on top of a base model whose frozen weights are stored in 4 bits. Dettmers et al. (2023) report that this reduces the memory needed to fine-tune a 65-billion-parameter model to under 48 GB, so that it fits on one GPU, while matching 16-bit full fine-tuning on the smaller-model benchmarks they test. It is a variant of [LoRA](index.md) that depends on [quantisation](../../quantisation/index.md) of the base model.

## Problem

LoRA cuts the number of trainable parameters, but the frozen base model still has to sit in memory at its full 16-bit size. For a 65-billion-parameter model, that base alone is more than the memory of a single 48 GB GPU, so fine-tuning needs several accelerators. Quantising the base to 4 bits would shrink it, but a plain 4-bit model loses accuracy, and the gradients have to pass through it to reach the adapters.

## Key concepts

- **4-bit NormalFloat (NF4):** a 4-bit data type for the base weights. Its levels are the quantiles of a standard normal distribution, rescaled into a fixed range, so that each level covers about the same number of weights. The set is asymmetric so that zero is represented exactly.
- **Double quantisation:** the scaling constants used by quantisation take memory too, so the paper quantises those constants as well. The paper reports a saving of about 0.37 bits per parameter.
- **Paged optimisers:** optimiser state is held in NVIDIA unified memory, which moves it between GPU and CPU memory when the GPU runs short. This absorbs the memory spikes that long sequences cause.

## How it works

The base model's weights are stored in NF4 and frozen. Each adapted layer computes the output of the 4-bit base weights, dequantised for the matrix multiplication, plus the LoRA update, and gradients flow back through the frozen 4-bit model into the adapters. Only the adapters are trained and stored in higher precision. Double quantisation and paged optimisers reduce the memory of the constants and of the optimiser state, respectively.

The paper finetunes more than 1,000 models across 8 instruction datasets, with LLaMA and T5 models, including sizes of 33 and 65 billion parameters.

## Results

The abstract reports that the method makes it possible to fine-tune a 65-billion-parameter model on a single 48 GB GPU while preserving full 16-bit fine-tuning performance. The best model family, Guanaco, reaches 99.3% of ChatGPT's performance level on the Vicuna benchmark, according to the paper, and needs about 24 hours of fine-tuning on one GPU.

The body reports that on GLUE and Super-NaturalInstructions, with RoBERTa and T5 models up to 3 billion parameters, 4-bit adapter fine-tuning matched 16-bit full fine-tuning. On MMLU with LLaMA models from 7 to 65 billion parameters, NF4 with double quantisation matched 16-bit LoRA. The 4-bit floating-point variant trailed by about one percentage point.

## Limitations

- **Larger scales are not fully shown.** The authors did not show that QLoRA fully matches 16-bit fine-tuning at the 33 and 65 billion scales, citing resource costs.
- **Narrow evaluation.** The evaluation is limited to MMLU, the Vicuna benchmark and the OA benchmark, so generalisation to other tasks is untested, and the responsible-AI analysis is limited.
- **One bit width and one adapter method.** The main experiments test only 4-bit storage and LoRA.
- **Chatbot focus.** The study centres on instruction tuning and chatbot performance. The authors argue that current chatbot benchmarks are not reliable for measuring chatbot quality, which limits how far the reported comparisons carry.

## Open questions

- **Gap at the largest scales.** Whether 4-bit adapter fine-tuning matches 16-bit fine-tuning at 33 and 65 billion parameters, and on tasks beyond instruction tuning, is not settled by the paper.
- **When paging slows training.** The paper leaves open when paged optimisers slow training, and reports only that they matched the speed of regular optimisers for a 65-billion-parameter model at batch size 16.

## Connections

QLoRA is LoRA applied to a quantised base, so the adapter mathematics on the [LoRA](index.md) page applies unchanged. Its memory saving comes from the number formats in [quantisation](../../quantisation/index.md), and the fine-tuning practice it serves is described under [training](../../../../engineering/training/index.md). The memory it saves is the bandwidth and capacity cost discussed in [memory hierarchy and bandwidth](../../../../engineering/hardware/memory-hierarchy/index.md).

## References

### Seminal papers

- Dettmers, T., Pagnoni, A., Holtzman, A., Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314. https://arxiv.org/abs/2305.14314 — Fine-tunes LoRA adapters on a 4-bit frozen base, making a 65-billion-parameter model trainable on one 48 GB GPU.
- Hu, E. J., et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank updates on frozen weights, the method QLoRA extends.

### Surveys and textbooks

- Gholami, A., Kim, S., Dong, Z., Yao, Z., Mahoney, M. W., Keutzer, K. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Surveys the quantisation methods that QLoRA's base-model storage builds on.

### Articles and documentation

- Krishnamoorthi, R. (2018). *Quantizing deep convolutional networks for efficient inference: A whitepaper*. arXiv:1806.08342. https://arxiv.org/abs/1806.08342 — Reports that per-channel 8-bit quantisation keeps classification accuracy within 2% of floating-point networks across many CNN architectures, the post-training counterpart of storing the base in low bits.
- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is the primary bottleneck for AI serving, the pressure that storing the base in 4 bits relieves.
