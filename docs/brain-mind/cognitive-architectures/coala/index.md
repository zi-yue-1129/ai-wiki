---
status: complete
last_reviewed: 2026-10-28
---

# CoALA: cognitive architectures for language agents (Sumers et al., 2023)

CoALA is a conceptual framework for describing language agents, built on large language models, by their modular memory, their set of internal and external actions, and a repeated decision cycle that chooses among those actions.

## Overview

A **language agent** is a system that uses a large language model as a core component and acts on the world, for example by answering questions with search, following instructions in a text game, or controlling a robot. Language agents have shown strong results, but the field has built many of them one at a time, with different memory schemes, action sets and control loops. The result is a body of work that is hard to compare.

CoALA, proposed by Sumers, Yao, Narasimhan and Griffiths, borrows from the history of cognitive science and symbolic artificial intelligence to give those agents a common vocabulary. Its authors draw on cognitive architectures, which are long-standing computational models of the mind, to describe how an agent stores information, what it can do, and how it decides. The framework is then used to survey and organise existing agents and to suggest directions for building new ones.

This page is one of the [Cognitive Architectures](../index.md) pages. It is the language-agent counterpart of the classic architecture [ACT-R](../act-r/index.md).

## Key concepts

- **Language agent**: a system whose decisions are made by a language model, which can call external tools or environments.
- **Working memory**: the short-term store of the agent's current perceptual input, goals and results of intermediate reasoning.
- **Long-term memory**: three stores in CoALA: procedural memory, which holds the rules and skills that determine behaviour; semantic memory, which holds facts about the world and the agent; and episodic memory, which holds records of past experience.
- **Grounding**: an external action that interacts with an environment, such as controlling a robot, navigating a website, or communicating with a person.
- **Retrieval, reasoning and learning**: the three kinds of internal action. Retrieval reads from long-term memory into working memory. Reasoning updates working memory with the help of the language model. Learning writes new content to long-term memory.
- **Decision cycle**: the repeated loop in which the agent proposes candidate actions, evaluates and selects one, and executes it.

## Problem

The authors observe that language agents built on large language models have achieved substantial empirical success, yet there is no systematic framework for organising them and planning future development. Without one, it is hard to say what a given agent remembers, what it can do, or where it differs from others.

CoALA addresses this gap by describing any language agent along three dimensions: its information storage (memory), its action space (internal and external), and its decision-making procedure. The abstract states that the framework is used to survey a large body of recent work and to identify actionable directions for more capable agents.

## Core idea

CoALA describes a language agent as a production-system-like loop with four parts.

The first part is **modular memory**. Working memory holds what the agent is currently dealing with. Long-term memory is split into procedural memory, which stores the rules that can be applied to working memory, semantic memory, which stores facts, and episodic memory, which stores past experience. These categories are borrowed from cognitive architectures such as Soar, whose productions live in long-term memory and act on working memory.

The second part is the **action space**. External actions interact with environments, through grounding. Internal actions interact with memory and are of three kinds: retrieval, reasoning and learning. This distinction matters because a language agent can change its own memory and reasoning without touching the outside world.

The third part is the **decision cycle**. In each cycle, the agent can use reasoning and retrieval to plan. Planning proposes, evaluates and selects an action, and the selected action is then executed. Execution may be a grounding action, such as a call to an external API, or a learning action, such as writing an experience to episodic memory.

## Equation or algorithm

CoALA is a framework rather than a learning algorithm, so the steps below describe the decision cycle as the paper lays it out, not a procedure with equations.

1. **Observe.** An observation from the environment is made and written into working memory.
2. **Retrieve and reason.** The agent reads relevant items from long-term memory into working memory and uses reasoning to interpret the situation. Reasoning and retrieval can be applied flexibly, and their sub-stages can interleave or iterate.
3. **Propose, evaluate and select.** The agent generates one or more candidate actions, evaluates them, and selects one. The paper describes these as the proposal, evaluation and selection sub-stages of the planning stage.
4. **Execute.** The selected action is applied. It may be an external grounding action, such as an API call, or an internal learning action, such as a write to episodic memory.
5. **Repeat.** The cycle continues with the next observation.

The paper also notes that a cycle of this kind is an abstraction. Real agents may implement one step in several ways, and some of the steps may be merged.

## Results

CoALA reports no new agent and no benchmark results. Its evidence is the organisation of existing work. In its Table 2, the paper casts several recent language agents into the framework and compares their internal mechanisms.

For example, SayCan grounds a language model to robotic interactions in a kitchen, and its long-term memory is procedural only. Its action space is external only, with a fixed set of 551 grounding skills. ReAct interleaves reasoning and acting in digital environments such as a Wikipedia API and a text game. It has no semantic or episodic memory, and its decision cycle uses a single reasoning action, with no separate evaluation or selection stage. Generative Agents retrieves episodic memories by recency, importance and relevance. Table 2 gives the paper's own summary of these methods.

The contribution of the paper is therefore a shared vocabulary and a way to compare agents, not a measured improvement in performance.

## Limitations

- **Descriptive, not evaluated.** A framework describes agents; it does not test which design performs better. The paper's categories are therefore not evidence about performance.
- **Categories may blur.** The framework classifies agents by their components. Real systems may not separate those components cleanly, so a classification can involve judgement.
- **Planning depth.** The decision cycle is described at a high level, and the paper notes that tree search and similar methods are one way to address the short planning horizon of autoregressive generation.
- **Open questions in the paper.** Section 7 of the paper lists open questions in cognitive science and AI that the framework does not settle.

## Key methods

- [ACT-R](../act-r/index.md): a cognitive architecture built to model human cognition. CoALA borrows the general idea of an architecture, not the ACT-R mechanisms.
- Soar: a production-system architecture whose decision loop CoALA uses as its main example of a cognitive architecture. Its productions match working memory and the best match is applied.
- ReAct (Yao et al., 2022): a language agent that interleaves reasoning traces with actions. CoALA classifies it as the simplest agent that uses both internal and external actions.
- Generative Agents (Park et al., 2023): a language agent with an episodic memory that is retrieved by recency, importance and relevance, and that reflects on its experience.

## Connections

- Parent topic: [Cognitive Architectures](../index.md)
- Other method on this topic: [ACT-R](../act-r/index.md)
- [AI Agents](../../../theory/models/agents/index.md): the general class of systems that perceive and act toward goals, of which CoALA's language agents are one kind.
- [Large Language Models](../../../theory/models/llm/index.md): the language model at the centre of each agent in CoALA.
- [Reasoning](../../../theory/models/reasoning/index.md): the reasoning and planning actions that the decision cycle relies on.
- [Memory & Learning in the Brain](../../memory-learning/index.md): the human memory categories that CoALA's working, episodic and semantic memories borrow from.
- [Building machines that learn and think like people](../../cognitive-science/building-machines-like-people/index.md): Lake and colleagues argue that human-like learning needs causal models, intuitive theories and compositionality, which sets a high bar for language agents.

The brain angle is a set of borrowed distinctions. CoALA takes its working memory and its episodic and semantic memories from cognitive science, and it treats the choice of action as a decision process, as cognitive architectures do.

## Applications

- **Robotics**: SayCan, as described in the paper, grounds a language model in robot interactions, for example by selecting from a set of skills in a kitchen.
- **Games and simulated worlds**: Voyager and Generative Agents use memory and retrieval in simulated environments.
- **Digital tasks**: ReAct interacts with an online encyclopedia API and a text game to complete tasks that need both reasoning and acting.
- **Agent design**: the paper's Section 6 suggests steps for building future language agents, using its three dimensions as a checklist.

## Open questions

- **Which learning actions?** The paper points out that writing experience to memory is a form of learning, but it is not yet clear which kinds of learning language agents should do, or how often.
- **How deep should planning go?** One-step decisions are easy to implement, but multi-step planning is more capable, and the best way to get it is not settled.
- **Where does grounding end?** The line between internal reasoning and external action is clearer in the framework than in real systems.
- **General intelligence.** The abstract frames a path toward language-based general intelligence as an open direction, and it is not yet clear how far current agents can travel along it.

## References

### Seminal papers

- Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L. (2023). Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — Proposes CoALA, a framework that describes a language agent by its modular memory, its internal and external actions, and its decision cycle.
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. & Cao, Y. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. arXiv. https://arxiv.org/abs/2210.03629 — Interleaves reasoning traces and task-specific actions in a language model, letting each guide the other in interactive tasks.
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P. & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv. https://arxiv.org/abs/2304.03442 — Describes language-model agents with a memory stream, reflection and retrieval, used to simulate believable human behaviour.
- Laird, J. E., Lebiere, C. & Rosenbloom, P. S. (2017). A Standard Model of the Mind: Toward a Common Computational Framework Across Artificial Intelligence, Cognitive Science, Neuroscience, and Robotics. *AI Magazine*. https://doi.org/10.1609/aimag.v38i4.2744 — Proposes a community consensus model of the mind synthesised from three cognitive architectures, the tradition on which CoALA draws.

### Surveys and textbooks

- Ritter, F. E., Tehranchi, F. & Oury, J. D. (2019). ACT-R: A cognitive architecture for modeling cognition. *WIREs Cognitive Science*. https://doi.org/10.1002/wcs.1488 — Reviews one of the best-known cognitive architectures, its history, its theory of cognition as a program, and its applications.
