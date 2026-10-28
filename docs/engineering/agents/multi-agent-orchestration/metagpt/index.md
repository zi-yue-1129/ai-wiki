---
status: draft
last_reviewed: 2026-10-28
tags:
- engineering
- agents
- reasoning
aliases:
- MetaGPT
- 角色團隊代理人
- 標準作業程序代理人
- Role-based multi-agent teams
---

# MetaGPT

MetaGPT (Hong et al., 2023) is a multi-agent framework in which language model agents take fixed professional roles, such as product manager, architect, project manager and engineer, and pass structured documents along an assembly line governed by standardised operating procedures. It is the role-based method on the [Multi-Agent Orchestration](../index.md) page.

## Overview

Chained model calls with no structure pass each step's errors to the next, and the final output can be inconsistent. Hong et al. argue that human organisations avoid this by dividing work among specialists and by fixing how their output is handed on. MetaGPT copies that arrangement: a role tells an agent what to produce, and a procedure tells it what it receives and what it must check.

Earlier role-based systems such as CAMEL (Li et al., 2023) and ChatDev (Qian et al., 2023) let agents converse freely. MetaGPT replaces free conversation with documents and checkpoints.

## Key concepts

- **Role**: a profile, a goal and a set of permitted outputs for one agent. A product manager writes requirements, an architect writes the design, an engineer writes code.
- **Standardised operating procedure (SOP)**: the sequence of steps and documents that a role follows, written as prompts. The authors encode SOPs from human software practice.
- **Assembly line**: the pipeline in which each role's output is the next role's input.
- **Structured message**: a typed document, such as a requirements file or an interface description, in place of free-form chat.

## How it works

The pipeline for a software task runs roughly as follows:

1. A product-manager agent turns the user's request into a requirements document.
2. An architect agent turns the requirements into a system design, with data structures and interfaces.
3. A project-manager agent splits the design into tasks and assigns them.
4. Engineer agents write code files for their tasks.
5. Each step can check its input against the documents from earlier steps, and an execution step can run the code and feed errors back.

The authors describe the procedure as a meta-programming framework: the SOPs are written as prompt sequences, so the workflow is itself a program that the agents execute.

## Key methods

Unlike [Multi-Agent Debate](../debate/index.md), which uses equal peers, MetaGPT fixes each agent's role in advance. For delegation by a single planner, see [HuggingGPT](../hugginggpt/index.md).

## Results

On the SoftwareDev benchmark that the authors use, MetaGPT is compared with ChatDev. The results in their Table 1 show the following for the full MetaGPT system against ChatDev.[^1]

- **Executability** (graded from 1 to 4): 3.75 against 2.25 for ChatDev.
- **Total lines of code**: 251.4 against 77.5.
- **Human revision cost**: 0.83 against 2.5, lower is better.
- **Tokens per line of code**: 124.3 against 248.9.

MetaGPT also uses more tokens in total, 31,255 against 19,292 for ChatDev, so its gains are not free. Without the executable feedback loop the score is 3.67, so much of the gain comes from roles and documents.

## Limitations

- **Cost.** Documents, reviews and retries multiply the tokens spent. Efficiency per line of code can improve even as total cost rises.
- **Fixed workflow.** The SOP is written in advance by people, so the system can only be as flexible as the procedure it encodes. Tasks without a known workflow fit badly.
- **Narrow evaluation.** The main results come from software development. Whether the same gains hold for research, writing or analysis is not shown in the paper.
- **Failure modes remain.** A study of failures in several multi-agent frameworks finds that many come from specification and inter-agent misalignment, which structured documents reduce but do not remove (Cemri et al., 2025).[^2]

## Open questions

- **Role design.** Roles, their number and their split of duties are chosen by hand, and methods for testing them are immature.
- **Generality.** Whether SOP-driven pipelines transfer to tasks with uncertain or changing structure is unclear.

## Connections

Dividing work into roles resembles the specialised modules of classic cognitive architectures. In [ACT-R](../../../../brain-mind/cognitive-architectures/act-r/index.md), separate modules such as vision, motor control and memory communicate through limited buffers, and the role-based pattern is a loose analogue of that design at the level of agents. For the broader view, see [Cognitive Architectures](../../../../brain-mind/cognitive-architectures/index.md).

## References

### Seminal papers

- Hong, S. et al. (2023). *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*. arXiv. https://arxiv.org/abs/2308.00352 — Introduces role-based agents that follow standardised operating procedures and pass structured documents along an assembly line.
- Li, G. et al. (2023). *CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society*. arXiv. https://arxiv.org/abs/2303.17760 — Role-playing agents guided by inception prompts, used to study cooperation between communicating agents.
- Qian, C. et al. (2023). *ChatDev: Communicative Agents for Software Development*. arXiv. https://arxiv.org/abs/2307.07924 — A chat-based software company of agents for design, coding and testing, the main baseline against which MetaGPT is compared.

### Surveys and textbooks

- Guo, T. et al. (2024). *Large Language Model based Multi-Agents: A Survey of Progress and Challenges*. arXiv. https://arxiv.org/abs/2402.01680 — Survey of LLM-based multi-agent systems, including how agent profiles and communication are designed.

### Articles and documentation

- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv. https://arxiv.org/abs/2503.13657 — Taxonomy of 14 failure modes in multi-agent systems, grouped into system design, inter-agent misalignment and task verification.
- Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. arXiv. https://arxiv.org/abs/2308.08155 — Open-source framework for building agents that converse to complete tasks, a common platform for role-based designs.

[^1]: Hong et al. (2023), Table 1 (statistical analysis on SoftwareDev), https://arxiv.org/abs/2308.00352 — Executability, code size, revision cost, token usage and tokens per line for ChatDev and MetaGPT.
[^2]: Cemri et al. (2025), taxonomy abstract, https://arxiv.org/abs/2503.13657 — Source of the three failure categories, cited as the basis for the limitation.
