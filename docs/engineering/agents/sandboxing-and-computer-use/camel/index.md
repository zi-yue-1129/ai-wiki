---
status: draft
last_reviewed: 2026-10-28
tags:
- agents
- security
- tools
aliases:
- CaMeL
- 以設計防禦提示注入
- Defeating prompt injections by design
---

# CaMeL: Defeating Prompt Injections by Design

CaMeL (Debenedetti et al., 2025) is a defence for LLM agents that does not rely on the model to ignore injected instructions. It places a layer of ordinary software around the model, which takes the control flow and the data flow of a task from the trusted user request and checks each tool call against security policies. It is one of three landmark methods on the [Sandboxing and Computer-Use Agents](../index.md) page, and it is the clearest example there of a permission model that isolates side effects.

## Overview

Prompt injection occurs when an agent reads untrusted content, such as a web page or a tool result, that contains instructions it then follows. Earlier defences mostly worked on the model itself, with delimiters, reminders or training. They can reduce attacks but give no guarantee, and new attacks regularly get past them.

CaMeL changes the question. Instead of asking whether the model can resist injected text, it asks whether injected text can reach the parts of the system that matter. An agent's behaviour has two parts. The *control flow* is the sequence of steps the agent will take. The *data flow* is where each value comes from and where it goes. Injections can corrupt either one. CaMeL fixes the control flow from the trusted request, so untrusted data cannot decide which tool runs, and it tracks the data flow so that policies can block values from reaching tools they should not reach.

## Key concepts

- **Privileged LLM (P-LLM)**: a model that sees only the user's query and writes a plan as Python code. It never sees the content of tool outputs.
- **Quarantined LLM (Q-LLM)**: a model that parses untrusted text into a structured form. It has no tool access, so an injection that reaches it cannot take an action directly.
- **Capability**: a tag attached to each value, recording where the value came from and who may read it.
- **Security policy**: a function that decides whether a tool call is allowed given the capabilities of its inputs.
- **Interpreter**: a custom Python interpreter that runs the plan, records the data-flow graph, and checks policies before executing each tool.

## How it works

The paper follows the Dual-LLM pattern, in which a privileged model plans and a quarantined model reads, and adds an interpreter to enforce the separation. The loop works as follows:

1. The P-LLM receives the user query and the available tools, including the Q-LLM as a callable function, and writes Python code that expresses the plan.
2. The interpreter runs the code. Each tool output is stored in a variable, and the tool attaches capabilities describing its source and readers.
3. When the plan needs to extract information from untrusted text, it calls the Q-LLM, specifying the expected output schema. The Q-LLM returns structured values only.
4. Before a tool is called, the interpreter collects the capabilities of the variables the call depends on, using the data-flow graph, and applies the policies. The call runs if it is allowed and is blocked if not.
5. If the Q-LLM reports that it lacks the information needed, the interpreter raises an error and the P-LLM is asked for different code.

The P-LLM never sees tool outputs, so an injected instruction can change values but not the plan's steps, and those values are checked by policy before they reach a state-changing tool.

## Results

- **AgentDojo.** The abstract reports that CaMeL solves 77 percent of tasks with provable security, against 84 percent for an undefended system. The gap is the cost of the defence in task success.
- **Without policies.** Even with no security policies, CaMeL lowers successful attacks for every model tested, from 300 to 0 for one of them. Two injection tasks, in the banking and travel suites, still succeed in some runs.
- **Utility.** Across most suites utility stays close to native tool calling, and the travel suite shows a larger drop.

## Limitations

- **Non-goals.** CaMeL does not defend against attacks that leave the control and data flow unchanged, such as a summary that misstates an email. The paper suggests showing a value's origin in the interface to help users notice such cases.
- **Human involvement.** The system is not fully autonomous. When a query is ambiguous, the user may need to clarify the intended flows.
- **Policy effort.** Policies must be written, and they can be fine-grained, as a calendar example in the paper shows.

## Open questions

- **Who writes the policies.** Policies may come from the platform, the application or the user, and the right division is not settled.
- **Graphical interfaces.** CaMeL assumes structured tool outputs. Whether its ideas transfer to screenshot-based agents, discussed on the [sandboxing topic page](../index.md), is open.
- **Residual attacks.** The remaining successful attacks show that even a design-based defence has gaps.

## References

### Seminal papers

- Debenedetti, E. et al. (2025). *Defeating Prompt Injections by Design*. arXiv. https://arxiv.org/abs/2503.18813 — Proposes CaMeL, which separates control and data flow and enforces capability-based security policies when tools are called.
- Debenedetti, E. et al. (2024). *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*. arXiv. https://arxiv.org/abs/2406.13352 — Benchmark environment with 97 tool-using tasks and 629 security test cases, used to evaluate CaMeL.
- Greshake, K. et al. (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. arXiv. https://arxiv.org/abs/2302.12173 — Shows that instructions in retrieved data can hijack LLM-integrated applications, the threat CaMeL is designed against.
- Lampson, B. W. (1973). *A note on the confinement problem*. Communications of the ACM. https://doi.org/10.1145/362375.362389 — Defines the confinement problem, the older question of how to stop a program leaking information, which information-flow control addresses.
- Saltzer, J. H. & Schroeder, M. D. (1975). *The protection of information in computer systems*. Proceedings of the IEEE. https://doi.org/10.1109/PROC.1975.9939 — Classic statement of protection principles, including least privilege, on which later access-control designs build.

