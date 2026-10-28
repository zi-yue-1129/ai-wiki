---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/llm
  - theory/paradigms/reinforcement-learning
aliases:
  - SayCan
  - Do As I Can, Not As I Say
  - 語言模型規劃
---

# SayCan (Ahn et al. 2022)

Ahn and colleagues asked how a language model, which knows a great deal about the world but has no physical experience, can guide a robot through a task. Their system, SayCan, lets the language model propose steps while learned value functions check which steps the robot can actually carry out. This page covers that paper; the parent topic is [Robotics](../index.md).

## Problem

A language model can suggest plausible steps for a task, such as "bring me a drink", but it does not know whether the robot can perform them in the current scene. Without that grounding, its plans can be fluent and still infeasible.

## Core idea

The robot has a library of pretrained skills, each with a value function that estimates how likely the skill is to succeed in the current scene. For each candidate skill, SayCan combines the language model's score for the skill with its value. The language model supplies the task-level plan, while the robot's skills and perception ground that plan in the physical environment.

## Procedure

1. List the candidate skills available to the robot.
2. Score each skill by combining the language model's probability for it with its value function.
3. Execute the best skill, observe the result, and repeat until the task is done.

## Results

The summary of the paper reports evaluations on real-world tasks with a mobile manipulator, where the system handles long, abstract natural-language instructions. Quantitative figures need the full paper.

## Limitations

- The skill library fixes what the robot can do. A task outside the library cannot be solved by planning alone.
- The value functions must be learned for each skill, which takes data.
- The paper's evaluations are on the authors' robot and skill set.

## Connections

- A follow-up that adds language feedback during execution, Inner Monologue (Huang et al. 2022), is listed in References.
- Learning skills and value functions relates to [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).

## References

### Seminal papers

- Ahn, M. et al. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 — Combines a language model with learned value functions for pretrained robot skills on real-world tasks.
- Huang, W. et al. (2022). Inner Monologue: Embodied Reasoning through Planning with Language Models. arXiv. https://arxiv.org/abs/2207.05608 — Adds language feedback from the environment to planning with language models, to improve robot task completion.
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — A transformer robot policy trained on large real-robot data, the kind of skill that SayCan can compose.

### Surveys and textbooks

- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — Survey of reinforcement learning for robots, the source of the value-function idea.
- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — Report on foundation models, including the grounding of language models in robotics.
