---
status: draft
last_reviewed: 2026-11-27
tags:
  - distributed tracing
  - observability
aliases:
  - Dapper
  - Dapper tracing
  - Dapper 分散式追蹤系統
---

# Dapper

Dapper is the distributed tracing infrastructure that Google described in 2010. It records how a request moves through many services, and it was designed to run continuously on a very large system. The trace, span and annotation model it introduced is the model that [agent observability](agent-observability.md) reuses for chains of model and tool calls. Dapper itself is not an agent tool.

## Problem

The paper starts from two fundamental requirements: ubiquitous deployment and continuous monitoring. It states three design goals. Tracing must have low overhead, with a negligible performance impact on running services. It must be application-level transparent, so that programmers need not be aware of the tracing system. And it must scale to Google's services and clusters.

## Core idea

A Dapper trace is a tree of nested remote calls. Each node is a span, a basic unit of work with a span id and a parent id. Spans without a parent id are root spans, and all spans of one request share a trace id. Each span is also a timestamped record of its start and end times, its timing data for remote calls, and zero or more application-specific annotations. The paper bounds the annotation volume of each span. Ids are probabilistically unique 64-bit integers, so the tree can be rebuilt from the recorded spans.

## Mechanism

Sampling is what makes always-on tracing affordable. The first production version recorded about one trace for every 1024 candidate requests, and the paper cites sampling rates as low as 0.01 percent for high-traffic services. It states that sampling is needed to avoid latency degradation. A per-host daemon collects the span records, and the paper reports that the daemon never used more than 0.3 percent of one core.

## Results

The overhead results come from a web-search cluster, where the authors measured latency and throughput at several sampling rates.

- Tracing every request (sampling 1/1) raised average latency by 16.3 percent and lowered throughput by 1.48 percent.
- At 1/16 sampling, latency rose by 2.12 percent and throughput changed by −0.08 percent.
- At 1/1024 sampling, latency changed by −0.20 percent and throughput by −0.06 percent.

The paper gives experimental errors of 2.5 percent for latency and 0.15 percent for throughput, and it says that sampling frequencies below 1/16 fall within that error. Other figures from the paper: creating and destroying a root span took 204 nanoseconds on average and a non-root span took 176 nanoseconds, on a 2.2 GHz x86 server. An unsampled annotation cost about 9 nanoseconds and a sampled annotation about 40 nanoseconds. A span record averaged 426 bytes, and collection was less than 0.01 percent of network traffic.

## Limitations

- The overhead measurements come from one web-search cluster inside Google, so they do not establish costs for other workloads.
- Sampling trades completeness for cost. At 1/1024, a rare failure may leave no trace at all. This is an inference from the sampling rates, not a result the paper reports.
- The model records calls and their timing. It does not record why a component made a decision, which an agent trace also needs.

Other approaches address the same problem differently. The Mystery Machine infers how a request executed from existing component logs. Pivot Tracing adds instrumentation at runtime and joins the events it collects. Canopy is Facebook's later end-to-end tracing system. The References list each of them.

## Connections

- [Agent observability and tracing](agent-observability.md) applies this model to agent runs.
- [AgentOps](agentops.md) proposes which agent artifacts should be traced on top of it.

## References

### Seminal papers

- Sigelman, B. H. et al. (2010). *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*. Google technical report dapper-2010-1. https://research.google.com/archive/papers/dapper-2010-1.pdf — The paper that introduces the trace, span and annotation model and reports the overhead of the production system.
- Chow, M., Meisner, D., Flinn, J., Peek, D. & Wenisch, T. F. (2014). *The Mystery Machine: End-to-end Performance Analysis of Large-scale Internet Services*. OSDI '14. https://www.usenix.org/conference/osdi14/technical-sessions/presentation/chow — Builds a model of request execution from existing component logs, as an alternative to instrumentation.
- Mace, J., Roelke, R. & Fonseca, R. (2015). *Pivot Tracing: Dynamic Causal Monitoring for Distributed Systems*. SOSP '15. https://cs.brown.edu/~jcmace/papers/mace15pivot.pdf — Combines dynamic instrumentation with a happened-before join to correlate events across components at runtime.
- Kaldor, J., Mace, J., Bejda, M. et al. (2017). *Canopy: An End-to-End Performance Tracing And Analysis System*. SOSP '17. https://cs.brown.edu/~jcmace/papers/kaldor2017canopy.pdf — Describes Facebook's end-to-end performance tracing infrastructure.

### Articles and documentation

- OpenTelemetry. *Semantic Conventions for GenAI agent and framework spans*. https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md — The span conventions that apply the trace model to agent operations. The page is marked Development.
