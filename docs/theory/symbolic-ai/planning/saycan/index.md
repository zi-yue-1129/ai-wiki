---
status: draft
last_reviewed: 2026-10-28
tags:
  - planning
  - large language models
  - reasoning
aliases:
  - SayCan
  - Do As I Can, Not As I Say
  - 說到做到
  - 語言模型機器人規劃
  - Language model grounding
  - 語言落地
---

# SayCan

SayCan is a method that lets a large language model plan for a robot. The language model proposes which skill to use next, and a set of learned value functions estimates whether each skill is feasible in the robot's current scene. The robot chooses the skill that scores highest on both, carries it out, and repeats until the instruction is complete. It was introduced by Michael Ahn and colleagues at Google in 2022, and it is the language-based landmark in the [automated planning overview](../index.md).

## Overview

A language model knows how tasks are usually done. Asked how to clean up a spill, it can write a sensible sequence of steps. Those steps may not be possible for a particular robot in a particular room, because the robot may lack a sponge, be unable to reach the spill or be holding something else.

SayCan combines the two sources. The language model judges which steps help the instruction, and the skill value functions judge which steps can be done from the current observation. Neither is enough alone.

## Key concepts

- **Skill**: a short, pretrained robot behaviour with a natural-language name, such as "pick up the sponge".
- **Language-model score**: the probability the model assigns to a skill as the next step, given the instruction and the steps taken so far.
- **Affordance (value function)**: a learned estimate of the probability that a skill will succeed from the current observation.

## How it works

Let $i$ be the instruction, $\ell$ the steps taken so far and $s$ the current observation. For each candidate skill $a$, the robot forms a score from the language-model probability of the skill and its value function. The robot then selects

$$
a^{*} = \arg\max_{a} \; p_{\text{LLM}}(a \mid i, \ell)\; \cdot\; V_a(s),
$$

where $V_a(s)$ is the estimated probability that skill $a$ succeeds from state $s$. The procedure is as follows.

1. Read the instruction and set the list of completed steps to empty.
2. Ask the language model for the probability of each skill in the library, given the instruction and the steps so far.
3. Ask each skill's value function for its success estimate from the current observation.
4. Multiply the two scores, choose the skill with the highest product, and execute it.
5. Append the executed skill to the steps so far, and return to step 2 until the model signals that the task is complete.

A skill is chosen only when the model finds it useful and the robot finds it possible. Later work such as Inner Monologue adds closed-loop feedback from the environment to the same kind of loop.[^3]

## Results

The paper evaluates the method on real-world robot tasks, with long-horizon instructions in abstract natural language, carried out by a mobile manipulator. The abstract reports that the approach completes these instructions and that real-world grounding is needed. Success rates are not quoted here.[^2]

## Limitations

- **Fixed skill library.** The robot can only do what its skills allow. A plan that needs a missing skill cannot be completed, however sensible the language model's text.
- **Cost of value functions.** Each skill needs a trained value function, which must be retrained when the robot or environment changes.
- **Dependence on both parts.** A poor language-model score can pick a possible but unhelpful skill, and the loop is slower than a precomputed plan.

## Open questions

- Does closed-loop feedback, as explored in later work, make plans more reliable in situations the skills were not built for?[^3]
- Language models alone plan poorly, so how much grounding is needed in general settings?[^4]

## Connections

SayCan treats skills as the primitive actions of a plan, a structure that [SHOP2](../shop2/index.md) uses in a more rigid form. It relies on the knowledge in [large language models](../../../models/llm/index.md), and its value functions are learned, as in [reinforcement learning](../../../paradigms/reinforcement-learning/index.md). Compare [STRIPS](../strips/index.md).

## Applications

- **Mobile manipulation**, where a robot carries out household-style instructions such as cleaning or fetching.[^2]
- **Hybrid planners**, where a language model writes a plan in a formal language and a classical planner solves it, as in LLM+P.[^5]

## References

### Seminal papers

- Ahn, M. et al. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 — Introduces SayCan, which combines a language model's skill scores with learned affordance value functions on a real robot.
- Huang, W., Abbeel, P., Pathak, D. & Mordatch, I. (2022). Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents. arXiv. https://arxiv.org/abs/2201.07207 — Shows that large language models decompose tasks into plans, and that these plans must be translated to admissible actions.

### Articles and documentation

- Huang, W. et al. (2022). Inner Monologue: Embodied Reasoning through Planning with Language Models. arXiv. https://arxiv.org/abs/2207.05608 — Adds closed-loop language feedback from the environment to language-model planning for robots.

### Articles and documentation

- Liu, B. et al. (2023). LLM+P: Empowering Large Language Models with Optimal Planning Proficiency. arXiv. https://arxiv.org/abs/2304.11477 — Converts a language problem into PDDL, solves it with a classical planner and translates the plan back into language.
- Valmeekam, K. et al. (2023). On the Planning Abilities of Large Language Models: A Critical Investigation. arXiv. https://arxiv.org/abs/2305.15771 — Measures the autonomous planning ability of language models and shows gains when they guide an external planner.
- Kambhampati, S. et al. (2024). LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks. arXiv. https://arxiv.org/abs/2402.01817 — Position paper arguing that language models do their best work in loops with external verifiers.

[^1]: Ahn et al. (2022), listed above.
[^2]: Ahn et al. (2022), listed above. The setting and claims follow the paper's abstract. Success rates are not quoted.
[^3]: Huang et al. (2022, Inner Monologue), listed above.
[^4]: Valmeekam et al. (2023), listed above.
[^5]: Liu et al. (2023), listed above.
