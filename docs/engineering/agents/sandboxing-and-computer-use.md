---
status: draft
last_reviewed: 2026-11-01
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

## Threat model and trust boundaries

The first design decision is not which model controls the desktop, but which principal is allowed to perform each operation. The user supplies the objective; the model proposes actions; a separate policy-enforcing executor decides whether an action is permitted. Text found on a web page, in a repository or in a screenshot is **task data**, not a source of authority. Greshake et al. demonstrate why this distinction matters: attacker-controlled retrieved content can redirect an LLM-integrated application toward unintended tool calls.

A useful threat model separates four assets: **private information** (documents, credentials and browser state), **integrity** (files, messages and account settings), **availability** (CPU time, rate limits and network traffic), and **audit evidence** (the record needed to investigate a run). It also separates four adversaries or failure sources: malicious remote content, compromised tool or browser extensions, an overprivileged agent, and ordinary model or interface errors. These cases require different mitigations. A prompt asking the model to ignore hostile instructions is not an operating-system access control.

For example, suppose an agent must download a public invoice and extract a total. The website might display a forged instruction asking the agent to upload the local password store. The executor should make that upload impossible even if the model attempts it: the password store is not mounted, the outbound destination is not allowed, and the upload operation is not in the approved capability set. Logging the attempted action supports investigation, but logging alone does not prevent disclosure.

## Isolation choices and their limits

| Boundary | What it isolates | Important residual risk |
|---|---|---|
| Separate browser profile | Cookies, history and browser preferences | Shared host files and network remain reachable through other tools |
| Rootless container with restricted mounts | Processes and a selected filesystem view | Kernel sharing, overly broad mounts and inherited secrets |
| Disposable virtual machine | Guest operating system and its process tree | Hypervisor flaws, host integrations and authorized network destinations |
| Remote task-specific service | A narrow API capability instead of a general desktop | Incorrect authorization in the service and overly broad API scopes |

These are **engineering patterns**, not interchangeable guarantees. A container is not automatically a secure sandbox; a VM does not make authorized exfiltration harmless. Isolation must be paired with identity, authorization and outbound controls. For a workflow that only needs to read one document, a narrow read-only API is preferable to giving an agent a desktop with unrestricted file access.

## Key methods

- **Capability-scoped execution:** issue narrowly scoped operations, paths and credentials for a single task; reject requests outside that scope before execution.
- **Disposable environment execution:** start each run from a known image and reset mutable state afterwards, reducing cross-run contamination without eliminating external side effects.
- **Human-gated transactions:** present the exact recipient, amount, destination or deletion target to a person before committing a high-impact action.
- **State-verified interaction:** after each click or command, compare the observed application state with the expected transition rather than assuming success.

These methods address different failure modes and are often combined. Unlike a named research algorithm, they describe implementation controls; detailed agent benchmarks and their methods are covered on [Agent evaluation](agent-evaluation.md).

## A practical execution protocol

1. **Prepare:** provision a fresh environment with an explicit filesystem manifest, permitted network destinations, account scopes, maximum steps, time budget and an emergency-stop channel.
2. **Observe:** capture the screen or accessibility tree, identify the current application and label external content as untrusted observations.
3. **Propose:** have the model return a structured action with arguments and a stated expected result. Do not treat the model's own justification as authorization.
4. **Authorize:** validate the action against an independent policy. For high-impact operations, obtain a human confirmation bound to the concrete parameters, not a generic approval of the whole session.
5. **Execute and verify:** perform the permitted action, inspect the resulting state, and stop or recover on unexpected dialogs, changed targets or ambiguous outcomes.
6. **Record and dispose:** preserve a minimal audit trail with timestamps, tool arguments, decisions and redacted evidence; revoke credentials and destroy the temporary environment.

The **time-of-check/time-of-use** problem is especially important for GUI automation. A button or recipient field can change between observation and click. Where possible, re-check the target immediately before a consequential operation, and verify the resulting server-side state. Repeated clicks are not necessarily safe: sending a message or transferring funds may be non-idempotent. A retry policy should distinguish read-only actions from operations that create external effects.

## Evaluation beyond task success

Task-completion benchmarks such as OSWorld and WebArena measure whether an agent reaches a specified end state, but that metric alone cannot establish whether the agent stayed within its authority. OSWorld's published benchmark contains 369 tasks across desktop and web applications; WebArena uses reproducible websites in four domains. Their published baseline results are tied to particular model versions and should not be interpreted as current universal capability ceilings.

A deployment evaluation should report **task success**, **policy-violation attempts**, **successful unauthorized effects**, **human intervention rate**, **recovery rate**, **wall-clock latency** and **cost per successful task**. Construct tests in which a legitimate task includes malicious text in a webpage, document or tool response. A safe outcome is not merely refusal to quote the malicious text: the executor must also prevent disallowed tool operations. Run both clean and adversarial tasks to detect the trade-off between security and legitimate completion.

Evidence retention is itself a privacy decision. Screenshots may contain personal data and session tokens; traces should be access-controlled, redacted where possible, and retained only as long as required for debugging or accountability.

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
