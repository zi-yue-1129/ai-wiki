---
status: draft
last_reviewed: 2026-11-27
related:
  - theory/models/agents
tags:
  - agents
  - observability
  - monitoring
aliases:
  - Agent Observability
  - Agent Tracing
  - LLM Tracing
  - LLM observability
  - 代理可觀測性
  - 代理追蹤
---

# Agent observability and tracing

Agent observability is the practice of recording enough of an agent's run to debug it, evaluate it and monitor it in production. A trace records each model call, tool call and decision in order, so that a failed task can be reconstructed step by step.

This page is part of [Agent Engineering](index.md).

## Overview

An agent's behaviour is spread over many steps and many components, and the final output rarely shows where a run went wrong. Observability makes the run inspectable. It answers questions such as which tool was called, with which arguments, what came back, how many tokens were used and how long each step took. The same records support cost tracking, incident review and comparison of two agent versions.

Tracing is an established idea in distributed systems. Dapper (Sigelman et al., 2010), Google's production tracing system, was built around two requirements, ubiquitous deployment and continuous monitoring, and three goals: low overhead, application-level transparency and scalability. Agent tracing applies the same trace-and-span model to a chain of model and tool calls.

## Key concepts

- **Trace:** the complete record of one task, from request to result.
- **Span:** one unit of work inside a trace, such as a model call or a tool call. The OpenTelemetry agent conventions give each agent operation a span with a name and a kind (see How it works below).
- **Event:** a timestamped note attached to a span, such as an error or a user confirmation.
- **Metric:** an aggregate over many runs, such as token count, latency, cost or error rate.
- **Redaction:** removing personal data or secrets from prompts and tool results before they are stored.

## How it works

Each model call, tool call, retrieval and agent step is wrapped as a span, and spans are nested so that the whole run forms a tree. Attributes record the model name, the token counts and the tool arguments. The spans are exported to a backend, where they can be searched, plotted or sampled. Traces also support replay: a failed run can be re-executed step by step to find the step where it diverged, and traces can be graded automatically, as described on [Agent evaluation](agent-evaluation.md).

The OpenTelemetry project publishes semantic conventions for generative AI. Its agent span conventions, which are in Development status, define a create-agent span (kind CLIENT) and an invoke-agent span (kind INTERNAL). The invoke-agent span carries the operation name, the agent name when it is available, and a conversation identifier when the application has one. The conventions have moved to a separate repository and may change, so an implementation should pin the version it uses.

## Key methods

Two landmark approaches frame the topic. Each has its own page, with the problem, the mechanism, the measured results and the limitations.

- [Dapper](dapper.md) (distributed tracing, 2010): a trace as a tree of spans, made affordable by sampling. Agent tracing inherits its model, but its overhead figures come from web-search services rather than from agents.
- [AgentOps](agentops.md) (Dong, Lu & Zhu, 2024): a taxonomy of the artifacts and data an agent system should trace across its lifecycle. It reports no experiments.

The OpenTelemetry agent-span conventions are a specification rather than a method with its own results, so they are described under How it works.

## Privacy and security

Prompts, retrieved documents and tool results may contain personal data, credentials or confidential text. Traces that store them become a new data store with its own risks. Good practice is to redact sensitive fields before export, set a retention period, restrict who can read traces, and record tool calls for audit. These records also support the least-privilege and confirmation controls described on [LLM Application Security](../llm-security/index.md).

## Limitations

- **Volume.** Full traces of long runs are large, and sampling reduces the cost but can miss rare failures.
- **Interpretation.** A trace shows what happened, not why the model chose an action. Explaining the choice needs other methods.
- **Standards in flux.** Conventions can change between versions, so dashboards built on them need maintenance.
- **Privacy trade-off.** The more that is recorded for debugging, the more sensitive data is stored.
- **Evidence.** The tracing overhead figures were measured on Google's services in 2010, and the AgentOps taxonomy has not been measured in use. The cost of tracing agent workloads needs its own measurement.

## Connections

- Evaluation uses the same trajectories as observability; see [Agent evaluation](agent-evaluation.md).
- The Model Context Protocol specification lists logging among its additional utilities, which gives servers a standard way to report events; see [Tool calling and MCP](tool-calling-and-mcp.md).
- Monitoring as a defence against injection is covered in [LLM Application Security](../llm-security/index.md).

## Applications

- **Debugging loops**, where an agent repeats the same tool call without progress.
- **Cost tracking** by task type, model or user group.
- **Incident review** after a harmful action, using the recorded steps.
- **Comparing versions** of an agent on live traffic, with traces as evidence.

## Open questions

- What is the right balance between detailed traces and privacy?
- How can traces explain a model's choice, not only record it?
- Which metrics best predict that an agent will fail on a new task?

## References

### Articles and documentation

- OpenTelemetry. *Semantic Conventions for GenAI agent and framework spans*. https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md — Defines the create-agent and invoke-agent spans and their attributes. The page is marked Development, so check the current version before pinning.
- Model Context Protocol. *Specification, revision 2025-06-18*. https://modelcontextprotocol.io/specification/2025-06-18 — Lists logging among the protocol's additional utilities.

### Seminal papers

- Sigelman, B. H. et al. (2010). *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*. Google technical report dapper-2010-1. https://research.google.com/archive/papers/dapper-2010-1.pdf — Describes the trace, span and annotation model and the overhead figures of the production system.
- Dong, L., Lu, Q. & Zhu, L. (2024). *AgentOps: Enabling Observability of LLM Agents*. arXiv. https://arxiv.org/abs/2411.05285 — The taxonomy of artifacts and data to trace across an agent's lifecycle, discussed on the AgentOps page. The abstract page shows the current title.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering their construction, applications and open challenges.
