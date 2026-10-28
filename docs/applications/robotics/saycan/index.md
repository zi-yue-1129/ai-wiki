---
status: complete
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

The robot has a library of pretrained skills. Each skill has a value function, which the paper treats as an affordance function: the probability that the skill succeeds from the current state. SayCan multiplies the language model's score for a skill by that affordance. The language model supplies the task-level plan, while the skills and their value functions ground that plan in the physical scene.

## Equation

Let *i* be the instruction, *s* the current state, and ℓπ the language description of skill π. The language model gives p(ℓπ | i), and the affordance function gives p(cπ | s, ℓπ), the probability that skill π completes successfully from s. SayCan selects

π* = argmax over π of p(cπ | s, ℓπ) · p(ℓπ | i).

The paper's Algorithm 1 computes this as the product of the affordance and LLM scores, then takes the argmax. In the undiscounted, sparse-reward case, a value function corresponds to an affordance function (Sec. 2).

## Procedure

1. Given the instruction and the current state, score every candidate skill by its language-model probability times its affordance.
2. Execute the highest-scoring skill, add its description to the plan so far, and repeat.
3. Stop when the terminate action is chosen.

## Results

Evaluation uses 101 instructions, which the paper calls "101 real-world robotic tasks", grouped into seven families of 15, 15, 15, 15, 11, 15 and 15 instructions (Table 1). The robot is an Everyday Robots mobile manipulator with a 7-degree-of-freedom arm (Sec. 5). The total row of Table 2 reports:

| System | Planning success | Execution success |
|---|---|---|
| PaLM-SayCan, mock kitchen | 84% | 74% |
| PaLM-SayCan, real kitchen | 81% | 60% |
| No value-function grounding | 67% | not reported in the total row |
| Generative baseline | 74% | not reported in the total row |
| BC NL | not reported in the total row | 0% |
| BC USE | not reported in the total row | 9% |

Moving from the mock kitchen to the real kitchen drops planning by 3 points and execution by 14 points (Sec. 5.1). FLAN-SayCan reaches 70% planning and 61% execution, against 84% and 74% for PaLM-SayCan (Table 3). The authors attribute 65% of errors to the language model and 35% to affordance failures (Sec. 5.1). The introduction says grounding "nearly doubles" performance over the non-grounded baselines. The planning gap in Table 2 (84% against 67% and 74%) is smaller than that phrase suggests, so the table numbers are the ones to quote.

## Limitations

- **Skill library:** the paper proposes 551 skills, but uses a subset of those "most amenable" to composition. The range and capability of the skills is the main bottleneck (Sec. 4, Sec. 8).
- **Data cost:** behavioural cloning used 68,000 teleoperated demonstrations, and the authors collected 276,000 autonomous episodes, of which about 12,000 were successful. Reinforcement learning used MT-Opt in simulation, for about 100 hours on 16 TPUv3 chips (App. C.2).
- **Language model errors:** the system struggles with negation and ambiguous references. Most long-horizon failures are early termination by the language model (Sec. 5.1). The authors expect it to inherit the biases and limits of its training data (Sec. 8).
- **Limited feedback:** feedback reaches the planner only through the value functions at the current step. The system cannot easily react when a skill fails despite a high value, so some failures go undetected (Sec. 5.2, Sec. 8).
- **Scope of evaluation:** the experiments use the authors' robot and skill set.

## Follow-up work

- **Inner Monologue (Huang et al. 2022)** adds natural-language feedback from the environment, such as success detection, scene description and human interaction, to LLM planning. It does this without additional training, and it targets the feedback limitation above.
- **Connection to learning:** the skills and their affordances are learned with behavioural cloning and reinforcement learning, which relates to [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).

## Connections

- The language model side of the method is covered in [LLMs](../../../theory/models/llm/index.md).
- The skill-learning side is covered in [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).

## References

### Seminal papers

- Ahn, M. et al. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 — Combines a language model with learned affordance functions for pretrained robot skills, evaluated on 101 real-world instructions.
- Huang, W. et al. (2022). Inner Monologue: Embodied Reasoning through Planning with Language Models. arXiv. https://arxiv.org/abs/2207.05608 — Feeds natural-language feedback from the environment back into LLM planning for robots, without additional training.
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — A transformer policy trained on a large real-robot dataset for real-world control.

### Surveys and textbooks

- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — Survey of reinforcement learning applied to robots.
- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — Report on the capabilities, technical principles and risks of foundation models, with robotics among the application areas.
