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

OpenVLA combines a Llama 2 language backbone with a visual encoder built from DINOv2 and SigLIP features. It is trained on 970k real-world robot demonstrations. RT-2-X has 55 billion parameters, and the paper reports that OpenVLA outperforms it by 16.5% absolute success rate across 29 tasks, with about seven times fewer parameters.

## Procedure

1. Train the model on 970k real-world robot demonstrations, starting from the language and vision backbones.
2. Fine-tune it for a new robot or task. The paper reports that LoRA at rank 32 reaches about the same success as full fine-tuning while training about 1.4% of the parameters, although its experiments run on A100 GPUs.
3. Serve the model with quantisation: 4-bit weights matched bfloat16 performance at 7.0 GB rather than 16.8 GB.

## Results

The paper reports a 16.5% absolute success advantage over RT-2-X across 29 tasks, and clear gains on BridgeData V2 (70.6% against 50.6%). RT-2-X remains stronger on semantic generalisation, and the two are comparable on the Google robot. The LoRA and quantisation results are in the paper's Tables 1 and 2.

## Limitations

- The results are on the benchmarks and robots the authors tested.
- RT-2-X is stronger on semantic generalisation, so the advantage depends on the task.
- The paper's fine-tuning experiments run on A100 GPUs, not consumer hardware.
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
