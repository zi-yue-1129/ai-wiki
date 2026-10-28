---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/agents
- theory/models/reasoning/chain-of-thought.md
tags:
- engineering
- agents
- reasoning
aliases:
- ReAct
- 推理與行動
- Reasoning and Acting
---

# ReAct: Reasoning and Acting in Language Models

ReAct (Yao et al., 2022) prompts a frozen language model to write its reasoning as text between its actions. Each thought guides the next action, and each observation from the environment corrects the next thought. It is one of two landmark methods on the [Agent Engineering](../index.md) page.

## Overview

Two strands of work ran apart. Chain-of-thought prompting let models reason in text, but without outside information that reasoning could drift into invented facts. Other work let models act in an environment, but without explicit planning an agent could lose track of its subgoals. ReAct asks whether one prompt can combine the two.

## Key concepts

- **Thought**: a free-text reasoning step that does not change the environment, such as a plan, a subgoal or a note about an exception.
- **Action**: a step that queries or changes the environment, such as a search or a game command.
- **Observation**: the text the environment returns after an action.
- **Context**: everything the model has seen so far. Each new step is generated from it.
- **Few-shot trajectories**: example runs written by people and placed in the prompt before the new task.

## How it works

The paper describes an agent that, at each time step, receives an observation $o_t$ and chooses an action $a_t$ from a policy $\pi(a_t \mid c_t)$, where $c_t = (o_1, a_1, \dots, o_{t-1}, a_{t-1}, o_t)$ is the context. ReAct enlarges the action space to $\hat{\mathcal{A}} = \mathcal{A} \cup \mathcal{L}$, where $\mathcal{L}$ is the space of language. A thought $\hat{a}_t \in \mathcal{L}$ produces no observation. It only extends the context, $c_{t+1} = (c_t, \hat{a}_t)$, so that later steps can use it.

In practice the loop runs as follows:

1. Build a prompt with a few worked examples of thought, action and observation sequences, followed by the new task.
2. Ask the frozen model for its next output, which may be a thought or an action.
3. If the output is an action, execute it and append the observation to the context. In question answering the actions were a Wikipedia search, a lookup in the current page and a finish action.
4. Repeat until the finish action appears or a step limit is reached.

In question answering, thoughts and actions alternate. In decision tasks with many actions, the model decides where thoughts are useful. Nothing in the format requires reasoning before each action, so the examples carry much of the behaviour.

## Results

The main experiments use a frozen 540-billion-parameter language model prompted with few-shot examples.

- **Question answering (HotpotQA).** ReAct beats the acting-only baseline. Against chain-of-thought it is slightly worse on exact match, 27.4 against 29.4,[^1] but it is more grounded in retrieved text. Hallucination was chain-of-thought's main failure in the authors' sample.
- **Decision making (ALFWorld).** The best ReAct trial reaches an average success rate of 71 percent. The best acting-only trial reaches 45 percent, and BUTLER, an imitation-learning agent from the ALFWorld paper, reaches 37 percent.[^2]
- **Fine-tuning.** With about 3,000 training examples, fine-tuned ReAct becomes the best of the four methods compared on HotpotQA. Under prompting alone at smaller scales it was the weakest.

## Limitations

- **Rigid structure.** The interleaved format limits free reasoning, and on HotpotQA the authors count more reasoning errors than for chain-of-thought.
- **Looping.** The model sometimes repeats earlier thoughts and actions instead of leaving the loop. The authors suspect the greedy decoding they used contributed.
- **Search quality.** Uninformative searches made up 23 percent of the error cases studied, and they derail the reasoning that follows.[^3]
- **Controlled environments.** Text-based and sandboxed tasks say little about open-ended, real systems.
- **No learning across attempts.** ReAct does not use a failed attempt to change the next one. [Reflexion](../reflexion/index.md) addresses that gap.

## Open questions

- **When to think, when to act.** The paper leaves this to the model. Whether a better policy can be learned or specified is open.
- **Reasoning-trained models.** Many current models reason at length before answering. How much of ReAct's gain remains when that reasoning is internal is an empirical question.
- **Prompting or training.** The fine-tuning results suggest that learning from trajectories generalises better, but the evidence covers few tasks.

## References

### Seminal papers

- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — The paper introducing ReAct, with experiments on question answering and interactive decision tasks.
- Shridhar, M. et al. (2020). *ALFWorld: Aligning Text and Embodied Environments for Interactive Learning*. arXiv. https://arxiv.org/abs/2010.03768 — The text-based household environment used for the decision experiments, which also introduces the BUTLER agent.
- Yang, Z. et al. (2018). *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering*. arXiv. https://arxiv.org/abs/1809.09600 — The multi-hop question answering dataset on which the question-answering experiments run.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Introduces chain-of-thought prompting, the reasoning-only baseline that ReAct extends with actions.

### Surveys and textbooks

- Wang, L. et al. (2023). *A Survey on Large Language Model based Autonomous Agents*. arXiv. https://arxiv.org/abs/2308.11432 — Survey of LLM agents covering memory, planning and action, the setting in which ReAct-style loops are used.

### Articles and documentation

- Anthropic (2024). *Building effective AI agents*. Anthropic Engineering. https://www.anthropic.com/engineering/building-effective-agents — Practical guidance on building agent loops of this kind, and on when a simpler workflow is preferable.

[^1]: Yao et al. (2022), Table 1 of the ReAct paper, https://arxiv.org/abs/2210.03629 — HotpotQA prompting results giving the exact-match figures quoted here.
[^2]: Yao et al. (2022), ALFWorld results, https://arxiv.org/abs/2210.03629 — Success rates of the best ReAct, acting-only and BUTLER trials.
[^3]: Yao et al. (2022), error analysis, https://arxiv.org/abs/2210.03629 — Share of sampled error cases attributed to uninformative search.
