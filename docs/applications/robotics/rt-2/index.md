---
status: complete
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

RT-2 co-fine-tunes a web-pretrained vision-language model on robot trajectories together with general vision-language tasks, such as visual question answering. Robot actions are written as text tokens, so they share a format with language. The authors call such models vision-language-action (VLA) models.

## Procedure

1. Start from a vision-language model pretrained on web-scale image and text data. The paper uses PaLI-X and PaLM-E.
2. **Action representation:** each action is 8 integers. They are a terminate flag, the 6-DoF end-effector displacement and the gripper extension. Each continuous dimension is discretised into 256 uniform bins, and the integers are written as text tokens.
3. **Co-fine-tuning:** train on robot data and web vision-language data together. The robot share of the mixture is about 50% for RT-2-PaLI-X and about 66% for RT-2-PaLM-E (App. B).
4. At run time, generate action tokens from the camera image and instruction, then decode them into robot commands. Decoding is restricted to valid action tokens on robot-action prompts.

## Results

The main generalisation results are success rates on the authors' robot (Table 4, App. H.1). Averages are over the unseen object, background and environment settings.

| Model | Seen tasks | Unseen average |
|---|---|---|
| R3M | 45 | 12 |
| VC-1 | 63 | 10 |
| RT-1 | 92 | 32 |
| MOO | 75 | 35 |
| RT-2-PaLI-X-55B | 91 | 62 |
| RT-2-PaLM-E-12B | 93 | 62 |

The text describes RT-2 as about 2x better than RT-1 and MOO on unseen settings, and about 6x better than the other baselines (Sec. 4.1). For emergent skills, the 55B PaLI-X model averages 60% overall against 17% for RT-1, which the authors call more than 3x the next best baseline (Table 5, Sec. 4.2). In the simulated Language-Table benchmark, RT-2-PaLI-3B scores 90 ± 10, against 74 ± 13 for RT-1 (Table 1).

A chain-of-thought variant of RT-2-PaLM-E, with a short plan step before the action tokens, is shown only through qualitative examples (Sec. 4.4). No success rate is reported for it.

The paper's ablation shows that co-fine-tuning matters most at the largest scale. At 55B it averages 63 against 52 for fine-tuning alone (Table 6). Table 4 gives 62 for the same model, so the two tables differ by one point.

## Limitations

- **No new motions:** the robot does not acquire new physical motions from web data. Its skills stay within the distribution of the robot dataset (Sec. 5).
- **Compute and speed:** the authors report high computational cost. The 55B model runs at 1–3 Hz and the 5B model at about 5 Hz (Sec. 3.3). Real-time inference "may become a major bottleneck" for high-frequency control (Sec. 5; App. G).
- **Few available backbones:** only a small number of general-purpose vision-language models can be used to build RT-2 (App. G).
- **Failure cases:** poor grasps on specific parts such as handles, novel motions such as wiping, dexterous motions such as folding a towel, and extended multi-step reasoning (App. G).
- **Scope of evaluation:** the experiments use the authors' robot and task family.

## Connections

- Vision-language models are covered in [Multimodal Models](../../../theory/models/multimodal/index.md).
- The language-model side is covered in [Large Language Models](../../../theory/models/llm/index.md).
- The same idea appears in an open model: [OpenVLA](../openvla/index.md).

## References

### Seminal papers

- Brohan, A. et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv. https://arxiv.org/abs/2307.15818 — Co-fine-tunes web-pretrained vision-language models on robot trajectories and web data, writing actions as text tokens.
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — The transformer robot policy that RT-2 is compared against, trained on a large real-robot dataset.
- Open X-Embodiment Collaboration (2023). Open X-Embodiment: Robotic Learning Datasets and RT-X Models. arXiv. https://arxiv.org/abs/2310.08864 — A shared robot dataset covering 22 robot embodiments, and RT-X models trained on it, including RT-2-X.
- Black, K. et al. (2024). π0: A Vision-Language-Action Flow Model for General Robot Control. arXiv. https://arxiv.org/abs/2410.24164 — A later generalist robot policy built on a vision-language model and described as a vision-language-action flow model.

### Surveys and textbooks

- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — Report on the capabilities, technical principles and risks of foundation models, with robotics among the application areas.
