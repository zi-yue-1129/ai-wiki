---
status: draft
last_reviewed: 2026-11-03
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

### Named methods

- [ReAct](react.md): reasoning and acting in one interleaved sequence.
- [Reflexion](reflexion.md): verbal reflection across attempts, stored in memory.
- [Toolformer](toolformer.md): tool calls learned from the model's own text.
- [Voyager](voyager.md): an agent that builds a library of executable skills while exploring Minecraft.
- [SWE-agent](swe-agent.md): an agent-computer interface for resolving software issues.

## Execution contracts and state transitions

A useful way to specify an agent is as a state machine rather than a chat transcript. At iteration `t`, the harness maintains a task state `s_t`, selects a permitted action `a_t`, receives an observation `o_{t+1}`, and updates the state. The model proposes actions; the harness determines whether an action is valid and whether it can execute. This separation is essential because an LLM-generated instruction is not an authorization.

An execution contract defines the initial inputs, allowed tools, permission scope, expected outputs, stop conditions and recovery behavior. It should distinguish a *proposed* tool call from a *committed* external effect. For example, a coding agent can prepare a patch without permission to push it; a support agent can draft a refund without permission to issue it. Explicit boundaries make the workflow inspectable and allow the same model to run with different privileges.

### Worked example: a repository repair agent

Suppose an agent must fix a failing unit test in a repository. A defensible execution sequence is:

1. **Observe:** read the failing test, relevant source files and repository status through read-only tools. Record the starting commit and test command.
2. **Plan:** identify a narrow hypothesis and propose the smallest edit. The plan is provisional; subsequent tool results may invalidate it.
3. **Authorize:** check that the target path is writable and that the requested command belongs to an approved execution profile. A model's explanation cannot bypass this gate.
4. **Act:** apply a patch inside a disposable workspace, with CPU, time and filesystem limits.
5. **Verify:** run the targeted test, then appropriate regression tests. Capture exit codes, diagnostics and the resulting diff.
6. **Commit or stop:** present the verified patch for review. If tests fail or the step budget is exhausted, preserve the failure evidence rather than reporting success.

This is an illustrative engineering workflow, not an algorithm shown to guarantee correctness in the cited research. It is intentionally narrower than a fully autonomous agent: approval of an edit and approval of a push are different decisions. The distinction also prevents a successful test run from being mistaken for permission to publish changes.

## Reliability and failure containment

A model may choose a valid tool with invalid arguments, repeat a side-effecting call after a timeout, or interpret untrusted output as an instruction. Those failures require controls at different layers. JSON-schema validation checks structure, while application validation checks semantic constraints such as account ownership, path allowlists and date ranges. A timeout does not establish whether a remote operation committed; retrying a payment or file deletion without an idempotency key can duplicate effects.

Tool results should be tagged with their provenance and treated as observations, not policy. A retrieved page that says “ignore previous instructions” must not gain authority merely because it was returned by a search tool. Sandboxing reduces the consequences of unsafe execution but does not by itself prevent a privileged API from making an unauthorized change. The dedicated [sandboxing chapter](sandboxing-and-computer-use.md) describes containment, while [tool calling](tool-calling-and-mcp.md) covers protocol boundaries.

A production harness also needs an explicit budget: maximum iterations, token and monetary cost, wall-clock deadline, number of external requests and an escalation policy. The stop condition should be evaluated by application code, not solely by asking the model whether it is finished. When a task cannot be verified, the final result should distinguish “attempted,” “tested,” “partially completed,” and “externally confirmed.”

## Evaluation protocol

Evaluate an agent against *environment outcomes*, not just fluent answers. A repository agent's success criterion might be that hidden tests pass without modifying prohibited files. For a customer-support agent, the criterion may include correct account selection, authorized changes and no duplicate refunds. Each task should have a reproducible initial state and a machine-checkable or independently reviewed end state.

Report success rate together with median and tail latency, tool-call count, cost per successful task, policy violations and recovery behavior. A lower-cost system with slightly lower raw accuracy may be preferable when the operational constraints are strict. Kapoor et al. argue that benchmark design must account for cost, reproducibility and overfitting rather than ranking systems on accuracy alone.

To separate model capability from harness effects, hold the task set and available tools fixed while varying orchestration or prompting. Run multiple seeds or repeated trials where sampling is stochastic. Record model version, tool schemas, permission policy, dataset version and evaluator implementation. A single successful trajectory is evidence of one execution, not a reliability estimate.

## Observability and incident review

A useful trace connects the user request, model invocation, tool proposal, authorization decision, tool execution, returned observation and final artifact. Record timestamps, latency, error categories and correlation identifiers. Do not log secrets or sensitive tool payloads indiscriminately: redact or minimize them before persistence. A trace should make it possible to answer *which external effect occurred*, *which principal authorized it* and *what the model observed beforehand*.

Post-incident review should distinguish a model selection error from a harness authorization failure, a tool implementation defect and an evaluator mistake. These failure classes imply different remedies. Better prompting may reduce bad proposals, but cannot substitute for a server-side permission check. Likewise, adding more agents may increase coordination overhead without improving task outcomes; the [orchestration chapter](multi-agent-orchestration.md) compares the trade-offs.

## Human oversight and cognitive analogies

Agent memory is often described by analogy to human working and long-term memory, but a persisted scratchpad is not evidence that an agent has human-like memory mechanisms. The useful engineering distinction is between transient execution context, durable task records and externally retrieved knowledge. Each has different freshness, privacy and corruption risks. Human operators should be able to inspect and correct durable state, particularly when it influences future tool calls.

An approval interface should expose the concrete action, target resource and likely consequence rather than a vague “continue” button. For irreversible operations, a human should confirm the actual parameters after validation. This is a design principle for accountable systems, not a claim that human review alone eliminates automation risk.

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
