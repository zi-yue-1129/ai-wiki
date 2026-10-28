---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/multimodal
  - theory/models/llm
aliases:
  - RT-2
  - Vision-language-action model
  - 視覺語言動作模型
---

# RT-2: Vision-Language-Action Models (Brohan et al. 2023)

Brohan and colleagues asked whether a vision-language model pretrained on web data can control a robot directly. Their answer is RT-2, which writes robot actions as text tokens, so one model handles both language and control. This page covers that paper; the parent topic is [Robotics](../index.md).

## Problem

Robots trained only on robot data know little about the objects, concepts and reasoning that everyday tasks need. Large vision-language models know a great deal, but they output text, not motor commands.

## Core idea

RT-2 fine-tunes a web-pretrained vision-language model on robot trajectories together with general vision-language tasks, such as visual question answering. Robot actions are written as text tokens, so they share a format with language. The authors call such models vision-language-action (VLA) models.

## Procedure

1. Start from a vision-language model pretrained on large amounts of web data.
2. Fine-tune it on robot trajectories, with actions written as text tokens, alongside general vision-language data.
3. At run time, generate action tokens from the camera image and the instruction, then decode them into robot commands.

## Results

The summary of the paper reports about 6,000 trials. RT-2 generalised better to new objects than robot-only training, followed commands that were absent from its robot data, and handled basic reasoning. With chain-of-thought prompting it also worked through multi-step problems. The per-task figures need the full paper.

## Limitations

- The paper's evaluations are on the authors' robot setup and task family.
- Training and running a model of this size needs large computing resources.
- Writing actions as text ties control to the language model's output format; the paper's results do not show how this affects control speed.

## Connections

- Vision-language models are covered in [Multimodal Models](../../../theory/models/multimodal/index.md).
- The language-model side is covered in [Large Language Models](../../../theory/models/llm/index.md).
- Later open models in the same family: [OpenVLA](../openvla/index.md).

## References

### Seminal papers

- Brohan, A. et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv. https://arxiv.org/abs/2307.15818 — Fine-tunes web-pretrained vision-language models on robot data, writing actions as text tokens.
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — The transformer robot policy that RT-2 builds on, trained on large real-robot data.
- Padalkar, A. et al. (2023). Open X-Embodiment: Robotic Learning Datasets and RT-X Models. arXiv. https://arxiv.org/abs/2310.08864 — Shared robot datasets from 22 robots and RT-X models trained on them.
- Black, K. et al. (2024). π0: A Vision-Language-Action Flow Model for General Robot Control. arXiv. https://arxiv.org/abs/2410.24164 — A later robot foundation model that pairs a vision-language backbone with flow matching.

### Surveys and textbooks

- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — Report on foundation models, including robotics as an application area.
