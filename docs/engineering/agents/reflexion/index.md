---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/reinforcement-learning
- brain-mind/memory-learning
tags:
- engineering
- agents
- reinforcement learning
aliases:
- 語言式強化學習
- Verbal reinforcement learning
- 語言式反思
---

# Reflexion: Language Agents with Verbal Reinforcement Learning

Reflexion (Shinn et al., 2023) improves a language agent without updating its weights. After a failed attempt, the agent writes a verbal reflection on what went wrong, stores it in memory and conditions its next attempt on the stored reflections. It is the second landmark method on the [Agent Engineering](../index.md) page.

## Overview

Reinforcement learning normally improves an agent by adjusting its parameters over many trials. Fine-tuning a large model for each task is costly, and a scalar reward says little about why an attempt failed. Reflexion uses language as the feedback channel: the agent explains its failure in words and reads that explanation before trying again. The paper tests this on decision making, question answering and code generation.

## Key concepts

- **Actor**: the language model that produces actions or text, conditioned on its memory. The paper tries a reasoning-only actor and [ReAct](../react/index.md).
- **Evaluator**: scores a trajectory. The paper uses exact-match grading for reasoning, heuristics for decision tasks, unit tests for code, and in some settings another language model.
- **Self-reflection model**: a language model that reads a failed trajectory and its score, then writes a short lesson.
- **Memory**: the current trajectory is short-term memory, and the stored reflections are long-term memory. The paper keeps long-term memory to a window of about one to three reflections, to respect context limits.

## How it works

The paper's Algorithm 1 proceeds as follows:

1. Run the actor once, score the trajectory with the evaluator, and write an initial reflection into memory.
2. While the evaluator does not pass the trajectory and the trial limit has not been reached, run the actor again with the memory in its prompt.
3. Score the new trajectory and generate a self-reflection from it.
4. Append the reflection to memory and return to step 2.

The paper writes the agent's policy as $\pi_\theta$ with $\theta = \{M_a, \text{mem}\}$, where $M_a$ is the actor model. The model weights stay fixed, and learning happens in the memory alone.

## Results

- **Code generation.** The abstract reports 91 percent pass@1 on HumanEval, against 80 percent for the GPT-4 baseline.[^1]
- **ALFWorld.** ReAct with Reflexion completes 130 of 134 tasks. ReAct alone stops improving between trials 6 and 7, while Reflexion keeps learning over 12 consecutive trials.[^2]
- **Summary.** The paper summarises its gains over strong baselines as 22 percent on ALFWorld, 20 percent on HotpotQA and 11 percent on HumanEval.

The paper also reports a weaker result: on MBPP Python, Reflexion trailed the GPT-4 baseline.

## Limitations

- **Local optima.** The authors describe Reflexion as policy optimisation in natural language, which can settle into poor solutions.
- **Bounded memory.** The sliding window limits what is remembered. The authors suggest vector or SQL stores as future work.
- **Self-generated tests.** For code, the model writes its own unit tests, which can pass on wrong code. The false-positive rate, the chance that code fails after passing the tests, was 16.3 percent on MBPP Python and 1.4 percent on HumanEval Python.[^3]
- **Hard-to-test functions.** Non-deterministic, impure, hardware-dependent or concurrent functions are difficult to check with input-output tests.
- **Cost.** Each trial is a full run of the agent, so gains must be weighed against latency and cost.

## Open questions

- **Quality of reflections.** A wrong lesson can persist in memory and steer later trials. How to detect and retire such lessons is unclear.
- **Quality of the signal.** When the evaluator is a language model, its mistakes become the agent's mistakes.
- **Memory design.** Beyond a small window, how should lessons be stored, retrieved and merged across tasks?
- **Transfer.** Whether reflections from one task help on other tasks is an open empirical question.

## References

### Seminal papers

- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. arXiv. https://arxiv.org/abs/2303.11366 — The paper introducing Reflexion, with results on ALFWorld, HotpotQA, HumanEval and MBPP.
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — The reasoning-and-acting actor that the decision-making experiments use.
- Shridhar, M. et al. (2020). *ALFWorld: Aligning Text and Embodied Environments for Interactive Learning*. arXiv. https://arxiv.org/abs/2010.03768 — The text-based household environment on which the decision-making results are reported.
- Yang, Z. et al. (2018). *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering*. arXiv. https://arxiv.org/abs/1809.09600 — The multi-hop question answering dataset used in the reasoning experiments.
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces HumanEval, Python programming problems specified by docstrings and scored for functional correctness.
- Austin, J. et al. (2021). *Program Synthesis with Large Language Models*. arXiv. https://arxiv.org/abs/2108.07732 — Introduces the MBPP benchmark of short Python programming tasks.
- Park, J. S. et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv. https://arxiv.org/abs/2304.03442 — Simulated characters that synthesise reflections from stored experiences and use them to plan, a related use of reflection in memory.

### Articles and documentation

- Anthropic (2026). *Demystifying evals for AI agents*. Anthropic Engineering. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — Describes graders and transcripts for agent evaluation, which bears on the evaluator design that Reflexion depends on.

[^1]: Shinn et al. (2023), abstract of the Reflexion paper, https://arxiv.org/abs/2303.11366 — Source of the 91 percent pass@1 on HumanEval and the 80 percent GPT-4 comparison.
[^2]: Shinn et al. (2023), ALFWorld results in the Reflexion paper, https://arxiv.org/abs/2303.11366 — Source of the 130 of 134 completed tasks and the comparison with ReAct alone over trials.
[^3]: Shinn et al. (2023), analysis of self-generated unit tests in the Reflexion paper, https://arxiv.org/abs/2303.11366 — Source of the false-positive rates on MBPP Python and HumanEval Python.
