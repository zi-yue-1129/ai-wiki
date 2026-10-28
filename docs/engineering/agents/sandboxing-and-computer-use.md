---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/agents
tags:
  - agents
  - security
  - computer use
aliases:
  - Sandboxing
  - Computer-Use Agents
  - Computer Use
  - 沙箱
  - 電腦操作代理
---

# Sandboxing and computer-use agents

A computer-use agent operates software the way a person does, by reading the screen and issuing clicks, keystrokes and scrolls. Sandboxing limits what such an agent can reach, so that a mistake or an attack cannot spread beyond the task.

This page is part of [Agent Engineering](index.md).

## Overview

Many tasks have no API. A computer-use agent can still work with them by observing the screen and acting through the same input devices a person would use. The same power means that the agent can read private files, send messages and change settings. Sandboxing is the set of controls that keeps those powers within the task.

## Key concepts

- **Computer-use loop:** the agent observes a screenshot or accessibility tree, a model chooses an action, the action is executed, and the new state is observed.
- **Sandbox:** an isolated environment, usually a container or virtual machine, with its own file system and processes.
- **Least privilege:** giving the agent only the files, accounts and network access the task needs.
- **Egress allow-list:** a list of network destinations the sandbox may contact.
- **Scoped, short-lived credentials:** access tokens limited to one task and expiring soon after.
- **Confirmation step:** a human approval before an action that cannot be undone, such as a payment or a deletion.

## How it works

A typical deployment combines several layers. The agent runs inside a virtual machine or container, so that a crash or a malicious action affects only that instance. Its file system is limited to a working directory, and its network access goes through an allow-list. Credentials are issued for the session and revoked afterwards. Every action and screenshot is logged, so that a reviewer can reconstruct what happened, and a kill switch stops the run.

Screen-based control is also slow and error-prone. Small layout changes, pop-up windows and unexpected dialogue boxes can all lead the agent astray, so the loop usually checks the result of each action before taking the next.

## Evaluating computer-use agents

OSWorld (Xie et al., 2024) provides a real computer environment in which multimodal agents attempt open-ended tasks, rather than tasks confined to one application. WebArena (Zhou et al., 2023) provides a set of realistic, reproducible websites in four domains for web agents. Both are used to measure whether an agent completes a task, and they also show how far current agents remain from reliable use. See [Agent evaluation](agent-evaluation.md).

## Security

Screen content is untrusted. A web page, an email or a document shown to the agent can contain instructions that the agent may follow, which is the indirect prompt injection risk described by Greshake et al. (2023). The Model Context Protocol specification states the same principle for tools: users must understand and consent to what a tool does, and the host must obtain explicit consent before invoking one (see [Tool calling and MCP](tool-calling-and-mcp.md)).

Practical defences include limiting the agent's permissions, separating instructions from observed content in the prompt, confirming irreversible actions, and monitoring the run (see [LLM Application Security](../llm-security/index.md)).

## Limitations

- **Benchmarks cover only part of real use.** A benchmark environment is a simplified copy of the software it models.
- **Sandboxes can be imperfect.** A flaw in the sandbox itself, or a permission granted too widely, undoes the protection.
- **Perception errors.** The agent can misread a screen, especially small or dense text.
- **Cost and latency.** Each step needs a model call and a fresh screenshot.

## Connections

- The general framing of agents is on [AI Agents](../../theory/models/agents/index.md).
- Security of applications built on models is on [LLM Application Security](../llm-security/index.md).
- Classical security practice, such as threat modelling and isolation, is on [Cybersecurity](../../applications/cybersecurity/index.md).

## Applications

- **Testing software** by running scripted flows through the user interface.
- **Filling forms** in legacy systems that have no API.
- **Accessibility assistance**, where an agent operates an interface on behalf of a user with a motor or visual impairment. OSWorld's authors cite accessibility and productivity as the motivation for this kind of agent.

## Open questions

- Which permissions can be granted safely, and how should they be shown to the user?
- Can agents reliably tell instructions from data on a screen?
- How should evaluation account for the cost of running a sandbox at scale?

## References

### Seminal papers

- Xie, T. et al. (2024). OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments. arXiv. https://arxiv.org/abs/2404.07972 — A scalable, real computer environment for evaluating multimodal agents on open-ended tasks.
- Zhou, S. et al. (2023). WebArena: A Realistic Web Environment for Building Autonomous Agents. arXiv. https://arxiv.org/abs/2307.13854 — Reproducible websites in four domains for building and testing web agents.
- Greshake, K. et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. arXiv. https://arxiv.org/abs/2302.12173 — Shows that content an application processes can carry instructions that the model follows.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering their construction, applications and open challenges.

### Articles and documentation

- Model Context Protocol. *Specification, revision 2025-06-18*. https://modelcontextprotocol.io/specification/2025-06-18 — States the consent and tool-safety principles that apply to agents acting on a user's behalf.
