---
related:
  - engineering/agents
  - theory/models/llm
  - theory/models/reasoning
tags:
  - agents
  - large language models
  - survey
last_reviewed: 2026-11-01
aliases:
  - The Rise and Potential of Large Language Model Based Agents
  - LLM-based agents survey
  - 基於大型語言模型的智能體綜述
---

# The Rise and Potential of Large Language Model Based Agents (Xi et al., 2023)

Xi, Chen, Guo and colleagues (2023) survey AI agents built on large language models. They propose a general conceptual framework in which an LLM acts as the brain of an agent, supported by perception and action modules, and they use it to organise the applications, the evaluation, and the open problems of LLM-based agents (Xi et al., 2023).

## Overview

The abstract frames the problem as a long pursuit of AI that matches or surpasses human ability, with agents seen as a promising vehicle. Earlier agent work focused on algorithms or training strategies for particular tasks. The survey argues that the community lacked a general and powerful model to serve as a starting point for designing agents, and it proposes large language models as that starting point (Xi et al., 2023).

## Key concepts

- **Agent**: an entity that senses its environment, makes decisions and takes actions (Xi et al., 2023, abstract).
- **Brain**: the controller that stores knowledge and memory and handles reasoning, planning and decisions. The paper calls it the core of an AI agent (Section 3).
- **Perception**: the module that takes in multimodal input, such as text, images and audio, and turns it into a form the brain can use (Section 3.2).
- **Action**: the module that carries out decisions through text output, tool use and embodied action (Section 3.3).

## The conceptual framework

The paper's framework has three parts. The brain (Section 3.1) covers natural language interaction, knowledge, memory, reasoning and planning, and transferability and generalisation. Perception (Section 3.2) converts input from several modalities into the brain's representation. Action (Section 3.3) covers text output, tool use and embodied action (Section 3.3.3). The survey stresses that the agent operates in a loop, repeating perception, reasoning and action so that it can receive feedback from the environment (Section 3).

This decomposition is the survey's main organising device. It lets a reader ask which module a particular system depends on, and which module limits it.

## Applications

The paper groups applications into three scenarios (Section 4):

- **Single-agent** deployment (Section 4.1), which the survey organises by task-oriented, innovation-oriented and lifecycle-oriented use.
- **Multi-agent** interaction (Section 4.2), in which agents cooperate for complementary skills or compete adversarially to advance (Section 4.2.1 and 4.2.2). The survey names software development as a multi-agent example (Section 2.2).
- **Human-agent cooperation** (Section 4.3), which the survey describes through an instructor-executor paradigm and an equal-partnership paradigm.

## Evaluation

The introduction says the survey reviews evaluation along four dimensions: utility, sociability, values, and the ability to continually evolve (Section 1). The evaluation section, Section 6.2, is the place to look for the detailed protocols. The survey's discussion of hallucination also notes that an agent's brain may generate content that conflicts with the source or with factual information, which limits its use in factually rigorous tasks (Section 3.1.2).

## Challenges

The survey lists several open problems (Sections 3.1.2 and 6):

- **Hallucination.** Generated content can conflict with facts, and this limits use in factually demanding tasks (Section 3.1.2).
- **Knowledge.** Acquired knowledge can become outdated or be incorrect from the start. Retraining is costly, and it can cause catastrophic forgetting, so the survey covers knowledge editing as an alternative (Section 3.1.2).
- **Safety and trustworthiness.** Adversarial robustness, trustworthiness and other risks (Section 6.3). The survey notes that LLMs are susceptible to adversarial attacks (Section 3.3.2).
- **Scaling agent counts.** Pre-determined and dynamic scaling of the number of agents (Section 6.4).
- **Open problems.** Whether LLM-based agents are a path to general intelligence, and the step from virtual simulated environments to physical ones (Section 6.5).

## Connections

- [ReAct](../../../engineering/agents/react.md) interleaves reasoning and acting, which is one way to realise the brain and action modules.
- [Toolformer](../../../engineering/agents/toolformer.md) and [Voyager](../../../engineering/agents/voyager.md) are concrete systems in the action and tool-use parts of the framework.
- [Reflexion](../../../engineering/agents/reflexion.md) adds feedback from the environment to the agent loop.
- [Chain-of-thought prompting](../reasoning/chain-of-thought.md) is the reasoning technique that many LLM-based agents build on.
- [Indirect prompt injection](../../../engineering/llm-security/indirect-prompt-injection.md) describes a security risk that arises when an agent reads untrusted content.

## Applications

The survey's applications are software development, scientific research and other tasks that need tools and multi-step planning (Sections 2.2 and 4). Its framework applies to any system in which a language model must decide, use tools and act over several steps.

## Open questions

- How to evaluate agents on utility and sociability together, and how to measure the values they act on.
- Whether an LLM-based brain is enough for general intelligence, or whether other components are needed.

## References

### Seminal papers

- Xi, Z., Chen, W., Guo, X. et al. (2023). *The Rise and Potential of Large Language Model Based Agents: A Survey*. arXiv. https://arxiv.org/abs/2309.07864 — A survey that proposes the brain, perception and action framework for LLM-based agents, with the applications and open problems discussed on this page.
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — Interleaves reasoning traces with actions in a single language model loop.
- Schick, T. et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv. https://arxiv.org/abs/2302.04761 — Trains a language model to decide when and how to call external tools.
- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. arXiv. https://arxiv.org/abs/2303.11366 — Improves an agent across attempts with verbal reinforcement learning.
- Park, J. S. et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv. https://arxiv.org/abs/2304.03442 — Agents that simulate human behaviour in an interactive setting, an example of the brain module at work.

### Surveys and related work

- Wang, G. et al. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models*. arXiv. https://arxiv.org/abs/2305.16291 — An embodied agent for open-ended exploration with large language models, an example of embodied action.
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. arXiv. https://arxiv.org/abs/2302.12173 — Shows how instructions hidden in data can take control of an LLM-integrated application.
