---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/agents
tags:
  - agents
  - multi-agent
  - orchestration
aliases:
  - Multi-Agent Orchestration
  - Multi-Agent Systems
  - LLM Multi-Agent
  - 多代理編排
  - 多代理系統
---

# Multi-agent orchestration patterns

Multi-agent orchestration arranges several language-model agents, each with a role, so that they can finish a task together. The design question is how work is divided, how agents pass information, and when the group stops.

This page is part of [Agent Engineering](index.md).

## Overview

A single agent with many tools can often do a task. Splitting the work across agents helps when the subtasks need different instructions, different tools or separate context windows. The cost is coordination. Each extra agent adds model calls, latency and a new place where errors can enter. The field is young and most patterns are described in framework papers rather than tested in controlled comparisons.

## Key concepts

- **Role:** the instructions, tools and expected output of one agent, such as planner, coder or reviewer.
- **Orchestrator (router):** an agent or fixed program that decides which agent acts next.
- **Handoff:** the transfer of control and context from one agent to another.
- **Shared state:** a common store, such as a document or a message log, that agents read and write.
- **Termination condition:** the rule that ends the exchange, such as a passing test, a maximum number of turns or a human decision.

## How it works

Four patterns recur in the literature and in frameworks.

1. **Orchestrator.** A planner splits the task, routes each part to a specialist and merges the results. This is the easiest pattern to inspect, because all messages pass through one point.
2. **Sequential pipeline.** Each agent transforms the previous output, for example from a requirement to a design, then to code and tests. MetaGPT (Hong et al., 2023) encodes standardised operating procedures from software teams into prompt sequences for each role.
3. **Conversational group.** Agents talk in a shared thread until a termination condition holds. AutoGen (Wu et al., 2023) is a framework for building applications from conversable agents that can combine language models, human input and tools, and whose conversation patterns can be set in code or natural language.
4. **Simulated society.** Agents live in a shared simulated world or act as communicating partners. Generative Agents (Park et al., 2023) simulate interactive agents as a model of human behaviour, and CAMEL (Li et al., 2023) studies communicative agents in a society of language models.

## Trade-offs

- **Cost and latency.** Each agent adds model calls to every step, and conversational patterns can grow long.
- **Error cascades.** Chaining models without structure lets an early mistake spread. MetaGPT's authors attribute logic inconsistencies in multi-agent systems to cascading hallucinations from naive chaining, and their remedy is structured procedures.
- **Hard to evaluate.** Success depends on the whole group. See [Agent evaluation](agent-evaluation.md) for the measures that exist.
- **Hidden coordination.** Shared state and message logs must be traced to find out why a decision was made. See [Agent observability](agent-observability.md).

## Connections

- Multi-agent learning in reinforcement learning, including agents that learn to communicate, is on [Multi-Agent Reinforcement Learning](../../theory/paradigms/reinforcement-learning/multi-agent-rl/index.md).
- A loose analogy links shared-state orchestration to the broadcast account of [Global Workspace](../../brain-mind/consciousness/global-workspace/index.md) in cognitive science. The analogy is a design comparison, not evidence about either system.
- The general agent framing is on [AI Agents](../../theory/models/agents/index.md).

## Applications

- **Software development** with planner, coder, tester and reviewer roles.
- **Research assistance**, where one agent searches, another reads and a third writes a summary.
- **Customer operations**, where a router sends each request to a specialist with its own tools.

## Open questions

- When does a group of agents outperform one agent with the same budget?
- What makes termination reliable in open-ended conversation?
- How should responsibility be divided when an error comes from one agent's output in a shared state?

## References

### Seminal papers

- Wu, Q. et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv. https://arxiv.org/abs/2308.08155 — A framework for building applications from conversable agents, with human input and tools.
- Hong, S. et al. (2023). MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework. arXiv. https://arxiv.org/abs/2308.00352 — Encodes standardised operating procedures into prompt sequences for role-based agents, and reports the error cascade of naive chaining.
- Li, G. et al. (2023). CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society. arXiv. https://arxiv.org/abs/2303.17760 — Studies communicative agents that cooperate in a society of language models.
- Park, J. S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv. https://arxiv.org/abs/2304.03442 — Simulates interactive agents in a shared environment, as a model of human behaviour.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering their construction, applications and open challenges.
