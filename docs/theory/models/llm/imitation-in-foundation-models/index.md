---
related:
- theory/paradigms/imitation
- theory/paradigms/reinforcement-learning/learning-from-human-feedback
- applications/robotics
tags:
  - imitation learning
  - foundation models
  - supervised fine-tuning
  - vision-language-action
---

# Imitation in Foundation Models

Large pre-trained models are shaped by imitation at two stages. Pre-training on human-written text is a form of large-scale imitation, and supervised fine-tuning on curated demonstrations is literal [behavioural cloning](../../../paradigms/imitation/behavioural-cloning/index.md) of text. The same recipe now trains robot policies from web-scale and teleoperated data, which is why imitation has moved from a niche robotics method to a central training stage.

## Overview

Three patterns recur. Language models learn to imitate demonstrations written by people, then learn preferences from comparisons that go beyond imitation. Vision-language-action models map images and instructions to robot actions, using large amounts of demonstration data. Action-chunking and diffusion policies model the multi-modal demonstrations that these models must reproduce.

## Language models

Supervised fine-tuning on human-written responses is the first step of instruction tuning. The InstructGPT pipeline (Ouyang et al., 2022) adds a reward model trained on rankings and optimises the policy with reinforcement learning, so the final model goes beyond what the demonstrators wrote. Summarisation work shows the same pattern in a clearer setting: models trained on human comparisons outperform models trained only on demonstrations (Stiennon et al., 2020). See [learning from human feedback](../../../paradigms/reinforcement-learning/learning-from-human-feedback/index.md) for the reward-model side.

## Robot foundation models

RT-2 co-fine-tunes a large vision-language model on robot demonstrations, turning web knowledge into robot actions and generalising to new objects and instructions (Brohan et al., 2023). RT-1 showed earlier that a transformer trained on large demonstration datasets can handle hundreds of tasks (Brohan et al., 2022). These systems are trained with behavioural cloning at scale, and their generalisation depends on the diversity of the demonstrations.

## Action chunking and diffusion policies

Predicting short sequences of actions rather than single steps reduces compounding errors and keeps behaviour coherent (Zhao et al., 2023). Diffusion policies model the full distribution of plausible actions, which handles demonstrations with several valid solutions (Chi et al., 2023). Both ideas are now common in robot foundation models.

## Connections

The language-model side connects to the parent [large language models](../index.md) page and to the reward-learning methods in [reinforcement learning](../../../paradigms/reinforcement-learning/index.md). The robot side connects to [applications: robotics](../../../../applications/robotics/index.md). Because the imitation stage often comes first, the quality and coverage of demonstrations usually limit what the final model can do.

## Applications

Instruction-following chat assistants, robot manipulation with natural-language commands, household robots trained on teleoperation, and cross-embodiment policies that share one model across robot types.

## Open questions

Scaling demonstration data is expensive, and it is unclear how far imitation can go without reinforcement or other feedback. Imitated behaviour inherits the biases and errors of its demonstrators, and robot foundation models still struggle with long-horizon tasks and unseen physical conditions.

## References

### Seminal papers

- Ouyang et al. (2022), "Training language models to follow instructions with human feedback", NeurIPS, [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) — InstructGPT, which combines supervised fine-tuning on demonstrations with reward-model reinforcement learning.
- Stiennon et al. (2020), "Learning to summarize from human feedback", NeurIPS, [arXiv:2009.01325](https://arxiv.org/abs/2009.01325) — Shows that learning from human comparisons outperforms learning from demonstrations alone for summarisation.
- Brohan et al. (2023), "RT-2: vision-language-action models transfer web knowledge to robotic control", [arXiv:2307.15818](https://arxiv.org/abs/2307.15818) — Co-fine-tunes a vision-language model on robot demonstrations to produce robot actions.
- Brohan et al. (2022), "RT-1: robotics transformer for real-world control at scale", [arXiv:2212.06817](https://arxiv.org/abs/2212.06817) — A transformer trained on large-scale demonstrations for hundreds of real-world tasks.
- Zhao, Kumar, Levine & Finn (2023), "Learning fine-grained bimanual manipulation with low-cost hardware", RSS, [arXiv:2304.13705](https://arxiv.org/abs/2304.13705) — ACT, which predicts action chunks from demonstrations.

### Surveys and textbooks

- Osa et al. (2018), "An algorithmic perspective on imitation learning", [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — Survey of imitation methods that the foundation-model approaches build on.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Chi et al. (2023), "Diffusion Policy: visuomotor policy learning via action diffusion", RSS, [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) — Diffusion-based action generation for visuomotor imitation.
