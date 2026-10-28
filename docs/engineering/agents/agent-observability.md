---
status: draft
last_reviewed: 2026-10-28
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
  - 代理可觀測性
  - 代理追蹤
---

# Agent observability and tracing

Agent observability is the practice of recording enough of an agent's run to debug it, evaluate it and monitor it in production. A trace records each model call, tool call and decision in order, so that a failed task can be reconstructed step by step.

This page is part of [Agent Engineering](index.md).

## Overview

An agent's behaviour is spread over many steps and many components, and the final output rarely shows where a run went wrong. Observability makes the run inspectable. It answers questions such as which tool was called, with which arguments, what came back, how many tokens were used and how long each step took. The same records support cost tracking, incident review and comparison of two agent versions.

Tracing is an established idea in distributed systems. Dapper (Sigelman et al., 2010), Google's production tracing system, recorded the path of each request through many services, with low overhead and without requiring changes to the applications it observed. Agent tracing applies the same model to a chain of model and tool calls.

## Key concepts

- **Trace:** the complete record of one task, from request to result.
- **Span:** one unit of work inside a trace, such as a model call or a tool call. The OpenTelemetry concept page describes a span as having a name, start and end times, a parent, and attributes.
- **Event:** a timestamped note attached to a span, such as an error or a user confirmation.
- **Metric:** an aggregate over many runs, such as token count, latency, cost or error rate.
- **Redaction:** removing personal data or secrets from prompts and tool results before they are stored.

## How it works

Each model call, tool call, retrieval and agent step is wrapped as a span, and spans are nested so that the whole run forms a tree. Attributes record the model name, the token counts and the tool arguments. The spans are exported to a backend, where they can be searched, plotted or sampled. Traces also support replay: a failed run can be re-executed step by step to find the step where it diverged, and traces can be graded automatically, as described on [Agent evaluation](agent-evaluation.md).

OpenTelemetry has published semantic conventions for generative AI, which define shared names for spans, metrics and events, including spans for agents and for the Model Context Protocol. The conventions are maintained in a separate repository and may change, so an implementation should pin the version it uses.

## Privacy and security

Prompts, retrieved documents and tool results may contain personal data, credentials or confidential text. Traces that store them become a new data store with its own risks. Good practice is to redact sensitive fields before export, set a retention period, restrict who can read traces, and record tool calls for audit. These records also support the least-privilege and confirmation controls described on [LLM Application Security](../llm-security/index.md).

## Limitations

- **Volume.** Full traces of long runs are large, and sampling reduces the cost but can miss rare failures.
- **Interpretation.** A trace shows what happened, not why the model chose an action. Explaining the choice needs other methods.
- **Standards in flux.** Conventions can change between versions, so dashboards built on them need maintenance.
- **Privacy trade-off.** The more that is recorded for debugging, the more sensitive data is stored.

## Connections

- Evaluation uses the same trajectories as observability; see [Agent evaluation](agent-evaluation.md).
- The Model Context Protocol includes logging among its utilities, which gives servers a standard way to report events; see [Tool calling and MCP](tool-calling-and-mcp.md).
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

- OpenTelemetry. *Semantic conventions for generative AI systems*. https://opentelemetry.io/docs/specs/semconv/gen-ai/ — Shared names for spans, metrics and events of generative AI systems, including agents and MCP. The conventions have moved to the OpenTelemetry semantic conventions repository, so check the current location.
- OpenTelemetry. *Traces*. https://opentelemetry.io/docs/concepts/signals/traces/ — Defines traces and spans and the attributes a span carries.
- Model Context Protocol. *Specification, revision 2025-06-18*. https://modelcontextprotocol.io/specification/2025-06-18 — Includes logging among the protocol's utilities.

### Seminal papers

- Sigelman, B. H. et al. (2010). *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*. Google technical report. https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/ — Describes Google's production tracing system, the origin of many distributed-tracing ideas.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering their construction, applications and open challenges.
