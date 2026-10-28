---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/agents
  - engineering/llm-security
  - theory/evaluation/benchmarks/reasoning-agents
tags:
  - agents
  - engineering
aliases:
  - Agent Engineering
  - Agentic Systems Engineering
  - 代理工程
  - AI 代理工程
---

# Agent engineering

Agent engineering is the practice of building systems in which a language model takes actions: it calls tools, works in an environment, coordinates with other agents, and is evaluated and monitored in production. The model is one component. Most of the engineering effort goes into the interfaces, the controls and the measurements around it.

## Overview

The [AI Agents](../../theory/models/agents/index.md) page describes what an agent is. This section covers how to build one that can be trusted with real actions. An agent that only answers questions needs a prompt and a test set. An agent that acts needs a defined set of tools, a boundary on what those tools can reach, a way to split work among agents when one is not enough, a benchmark that measures outcomes rather than text, and a record of what happened in each run.

## Key concepts

- **Harness:** the code that runs the model in a loop, passes it tools and observations, and stops the loop.
- **Environment:** the systems the agent can observe and change, such as a file system, a browser or an API.
- **Trajectory:** the record of one run, from the first request to the final state.
- **Control:** a permission, confirmation or limit that bounds what the agent may do.

## How it works

A typical agent loop observes the current state, asks the model for the next action, executes the action through a tool, and records the result. The loop ends when a goal is met, a limit is reached or a person intervenes. Each stage has an engineering concern. Tool design determines what the model can ask for. Sandboxing determines what a bad action can reach. Orchestration determines how work is split. Evaluation determines whether the loop succeeds. Observability determines whether a failure can be explained afterwards.

## Key methods

The section has five pages, each covering one part of the work. Each compares a set of approaches, so that a reader can choose among them.

- [Tool calling and the Model Context Protocol](tool-calling-and-mcp.md): how a model requests actions and how a standard protocol connects tools to applications.
- [Sandboxing and computer-use agents](sandboxing-and-computer-use.md): how an agent that operates software through the screen is isolated and kept within its permissions.
- [Multi-agent orchestration patterns](multi-agent-orchestration.md): orchestrator, pipeline, conversational group and simulated society, with their costs.
- [Agent evaluation](agent-evaluation.md): benchmarks that check end states and the reliability and cost measures used alongside them.
- [Agent observability and tracing](agent-observability.md): recording spans and traces so that runs can be debugged, monitored and audited.

## Connections

- The theory of agents, including planning and memory, is on [AI Agents](../../theory/models/agents/index.md).
- Agents that read untrusted content face the risks in [LLM Application Security](../llm-security/index.md).
- Retrieval is often one of an agent's tools; see [Retrieval-Augmented Generation](../rag/index.md).
- Benchmarks for reasoning and agents are on [Reasoning and Agent Benchmarks](../../theory/evaluation/benchmarks/reasoning-agents/index.md).

## Applications

- **Software engineering agents** that read a repository, edit files and run tests.
- **Customer-operations agents** that look up accounts and carry out approved changes.
- **Research assistants** that search, read sources and draft summaries with citations.

## Open questions

- Which agent designs remain reliable over long tasks with many tools?
- How should responsibility be shared among a person, an agent and the systems it changes?
- How can the cost of an agent be predicted before it runs?

## References

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering their construction, applications and open challenges.
- Kapoor, S. et al. (2024). AI Agents That Matter. arXiv. https://arxiv.org/abs/2407.01502 — Argues that agent evaluation should report cost alongside accuracy.

### Seminal papers

- Yao, S. et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR. https://arxiv.org/abs/2210.03629 — Interleaves reasoning and actions so that a model can plan and update its steps from tool results.
- Schick, T. et al. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. arXiv. https://arxiv.org/abs/2302.04761 — Trains a model to decide when and how to call external tools.
- Wu, Q. et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv. https://arxiv.org/abs/2308.08155 — A framework for applications built from conversing agents.

### Articles and documentation

- Model Context Protocol. *Specification, revision 2025-06-18*. https://modelcontextprotocol.io/specification/2025-06-18 — The open protocol for connecting models to tools, data and prompts.
