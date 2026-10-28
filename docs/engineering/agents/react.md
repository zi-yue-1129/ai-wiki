---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/agents
tags:
  - agents
  - reasoning
  - tool use
aliases:
  - ReAct
  - Reasoning and Acting
  - 推理與行動
---

# ReAct (Yao et al., 2022)

ReAct is a prompting method in which a language model writes its reasoning and its actions in one interleaved sequence. The reasoning helps the model plan and revise, and the actions let it query external sources. Yao et al. (2022) introduced it and showed gains on question answering, fact checking and two interactive decision-making benchmarks.

This page is part of [Agent Engineering](index.md). It is one of the named methods behind [Tool calling and the Model Context Protocol](tool-calling-and-mcp.md).

## Overview

Before ReAct, reasoning and acting were usually studied separately. Chain-of-thought prompting (Wei et al., 2022) elicits reasoning steps but does not consult anything outside the model, so errors in those steps are not corrected by evidence. Action-only approaches can gather facts but do not explain how they plan to use them. ReAct joins the two in one sequence.

## Problem

A model that answers from memory alone hallucinates, and a chain of reasoning that never checks its facts can carry an early error through every later step. The question the paper addresses is how a model can gather information from an environment while keeping the reasoning that tells it what to look for next.

## Core idea

At each step the model writes a short thought, which is a piece of reasoning about the current state, and then an action, which is a call to an external source or the environment. The observation returned by the action is added to the context, and the next thought uses it. The thoughts help the model induce, track and update its plan and handle exceptions. The actions let it reach knowledge or state that is not in its weights. The paper applies this to a simple Wikipedia API for question answering and fact verification.

## Equation or algorithm

The procedure is a loop over three kinds of text:

1. Write a thought about what is known and what to do next.
2. Write an action from the allowed action set, and execute it.
3. Append the observation returned by the environment, and return to step 1 until the model issues a final answer.

The examples in the prompt show all three kinds of text, so the model learns the pattern from a small number of demonstrations.

## Results

The abstract reports that ReAct overcomes hallucination and error propagation on HotpotQA and FEVER, and that it generates trajectories that are more interpretable than baselines without reasoning traces. On two interactive decision-making benchmarks, ALFWorld and WebShop, it outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples.

## Limitations

- **Dependence on the environment.** The gains depend on the quality of the external source. A poor search result or a wrong observation can still mislead the model.
- **Prompt-based.** The method works through the prompt, and the paper's comparisons use a small number of examples. Later agents often train or fine-tune models on trajectories instead.
- **Interpretability is a claim about traces.** Readable traces make a run easier to inspect, but they do not prove that the stated reasoning caused the action.
- **Cost.** Each step adds a model call and an observation to the context, so long episodes grow expensive.

## Connections

- The reinforcement-learning view of acting in an environment, which ReAct does without learning weights, is on [Reinforcement Learning](../../theory/paradigms/reinforcement-learning/index.md).
- Reflexion extends the loop with verbal feedback across trials; see [Reflexion](reflexion.md).
- Toolformer learns when to call tools instead of prompting for them; see [Toolformer](toolformer.md).
- Evaluation environments built for this kind of agent include [WebArena](../../theory/evaluation/benchmarks/reasoning-agents/webarena.md).

## Applications

- Question answering systems that search a knowledge base during reasoning.
- Web and household task agents that interleave observation with planning.

## Open questions

- Can a model keep its thoughts faithful to its actions when the environment is noisy?
- Does the interleaving still help when the model is trained rather than prompted?

## References

### Seminal papers

- Yao, S. et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR. https://arxiv.org/abs/2210.03629 — Introduces ReAct and reports results on HotpotQA, FEVER, ALFWorld and WebShop.
- Wei, J. et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS. https://arxiv.org/abs/2201.11903 — Shows that writing intermediate reasoning steps improves complex reasoning, the baseline ReAct extends.
- Shridhar, M. et al. (2021). ALFWorld: Aligning Text and Embodied Environments for Interactive Learning. ICLR. https://arxiv.org/abs/2010.03768 — A text-based household environment in which agents act and observe, one of ReAct's test benches.
- Yao, S. et al. (2022). WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents. NeurIPS. https://arxiv.org/abs/2207.01206 — A simulated online shopping environment for grounded language agents, the second ReAct test bench.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, placing reasoning-and-acting methods in context.
