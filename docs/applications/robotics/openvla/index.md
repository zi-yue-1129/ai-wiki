---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/multimodal
  - theory/models/llm
aliases:
  - OpenVLA
  - 開放視覺語言動作模型
---

# OpenVLA (Kim et al. 2024)

Kim and colleagues released OpenVLA, an open-source vision-language-action model with 7 billion parameters. The aim was a model that researchers can inspect, fine-tune and run, not only a closed system. This page covers that paper; the parent topic is [Robotics](../index.md).

## Problem

The strongest robot vision-language-action models were closed, so most labs could not study, adapt or serve them. The question was whether an open model could match a much larger closed one.

## Core idea

OpenVLA combines a Llama 2 language backbone with a visual encoder built from DINOv2 and SigLIP features. It is trained on roughly a million real-world robot demonstrations. The authors report that it outperforms the closed RT-2-X model, which the paper describes as much larger, on multi-task manipulation across many tasks and robot types.

## Procedure

1. Train the model on about a million real-world robot demonstrations, with the language and vision backbones.
2. Fine-tune it for a new robot or task. The paper reports low-rank adaptation (LoRA), which can run on consumer GPUs.
3. Serve the model efficiently with quantisation, so it can run on modest hardware.

## Results

The summary of the paper reports better multi-task performance than RT-2-X across many tasks and robot types. It also reports fine-tuning on consumer GPUs and efficient serving. Per-task numbers need the full paper.

## Limitations

- The results are on the benchmarks and robots the authors tested.
- The summary does not show how well the model handles tasks far from its training data.
- Fine-tuning and serving are cheaper than training, but still need engineering effort.

## Connections

- The closed model it is compared with is [RT-2](../rt-2/index.md).
- The vision-language side is covered in [Multimodal Models](../../../theory/models/multimodal/index.md).
- The language-model backbone is covered in [Large Language Models](../../../theory/models/llm/index.md).

## References

### Seminal papers

- Kim, M. J. et al. (2024). OpenVLA: An Open-Source Vision-Language-Action Model. arXiv. https://arxiv.org/abs/2406.09246 — A 7-billion-parameter open robot control model, released with checkpoints and code.
- Brohan, A. et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv. https://arxiv.org/abs/2307.15818 — The closed vision-language-action model that OpenVLA is compared with.
- Padalkar, A. et al. (2023). Open X-Embodiment: Robotic Learning Datasets and RT-X Models. arXiv. https://arxiv.org/abs/2310.08864 — Shared robot datasets from 22 robots, the kind of data used for cross-robot training.
- Black, K. et al. (2024). π0: A Vision-Language-Action Flow Model for General Robot Control. arXiv. https://arxiv.org/abs/2410.24164 — A later robot foundation model, for comparison with open alternatives.

### Surveys and textbooks

- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — Report on foundation models and the case for shared base models.
