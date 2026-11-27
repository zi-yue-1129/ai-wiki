---
status: draft
last_reviewed: 2026-11-27
related:
  - theory/models/agents
tags:
  - agents
  - observability
  - LLMOps
aliases:
  - AgentOps
  - Enabling Observability of LLM Agents
  - AgentOps taxonomy
  - 代理運維
---

# AgentOps

AgentOps refers to the operations tooling for LLM agents: the systems that trace, monitor and evaluate an agent from development to production. Dong, Lu and Zhu (2024) describe which artifacts and data such tooling should record. Their paper is a taxonomy rather than a system, and it reports no experiments.

## Problem

Observability tools for language models record prompts and model calls. The paper asks which artifacts and data an agent system should trace across its whole lifecycle, so that the agent can be observed from development through production. Its authors also note that existing platforms do not specifically cover the agent's execution steps, such as planning, reasoning and memory.

## Core idea

The authors review existing AgentOps and LLM observability tools, including AgentOps, Langfuse, LangSmith, Arize and Datadog, and organise what they record into a taxonomy. As the sections of the paper present it, the categories are: an agent creation registry; context enhancement, such as in-context learning and retrieval; prompts; guardrails; agent execution, covering planning, reasoning, memory and workflow; evaluation and feedback; tracing, with sessions, traces and spans; and monitoring, with metrics and their dimensions.

Two framing points matter for reading the paper. Debugging appears only as a future aim in the conclusion, not as a component. Compliance, citing the EU AI Act, is given as a motivation rather than as a component.

## Equation or algorithm

The paper gives no algorithm or equation. Its contribution is a classification that tells a builder which artifacts to log and at what level of detail.

## Results

The paper reports no experiments, benchmarks or measurements of tools or agents. Its results are the taxonomy itself, built from the review of existing tools.

## Limitations

In its threats-to-validity section, the authors name four limits. The review may have missed relevant tools. The overview may not cover every data attribute that concerns AI agents. Existing platforms do not cover the agent execution steps. And the links between traces across the lifecycle, and the interactions between steps, are left to future work.

The paper has been posted under two titles. The first version was called *A Taxonomy of AgentOps for Enabling Observability of Foundation Model based Agents*. The current abstract page gives *AgentOps: Enabling Observability of LLM Agents*.

## Connections

- [Agent observability and tracing](agent-observability.md) explains the trace and span records that the taxonomy assumes.
- [Dapper](dapper.md) gives the older model of traces and spans that agent tracing reuses.
- [Agent evaluation](agent-evaluation.md) covers the evaluation records that the taxonomy also lists.

## References

### Seminal papers

- Dong, L., Lu, Q. & Zhu, L. (2024). *AgentOps: Enabling Observability of LLM Agents*. arXiv. https://arxiv.org/abs/2411.05285 — The taxonomy discussed on this page. The abstract page shows the current title.
- Sigelman, B. H. et al. (2010). *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*. Google technical report dapper-2010-1. https://research.google.com/archive/papers/dapper-2010-1.pdf — The trace and span model that agent tracing reuses.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering their construction, applications and open challenges.

### Articles and documentation

- OpenTelemetry. *Semantic Conventions for GenAI agent and framework spans*. https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md — Span conventions for agent operations. The page is marked Development.
- Model Context Protocol. *Specification, revision 2025-06-18*. https://modelcontextprotocol.io/specification/2025-06-18 — Lists logging among the protocol's additional utilities.
