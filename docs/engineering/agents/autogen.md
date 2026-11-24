---
status: draft
last_reviewed: 2026-11-18
related:
  - theory/models/agents
tags:
  - agents
  - multi-agent
  - conversation
aliases:
  - AutoGen
  - Microsoft AutoGen
  - Conversable agents
  - 對話式代理
  - 多代理對話
---

# AutoGen (Wu et al., 2023)

AutoGen is a framework for building language-model applications from *conversable agents*: agents that send messages to one another, and whose replies can come from a language model, a human, a tool, or a mix of these. Wu et al. (2023) describe the framework and report experiments on mathematics, question answering, text-based household tasks and coding.

This page is one of the named methods behind the conversational-group pattern in [Multi-agent orchestration patterns](multi-agent-orchestration.md). It is part of [Agent Engineering](index.md).

## Overview

Before a framework of this kind, a developer who wanted several models to cooperate wrote the message passing, the turn order and the stop rule by hand for each application. AutoGen turns these into reusable parts. A developer changes the pattern by adjusting settings in code or a system message, rather than rewriting the control flow. The paper's examples use the same small set of agent types for very different tasks.

## Problem

Many useful tasks need several capabilities at once: reasoning, running code, looking up documents, and asking a person when information is missing. The paper addresses how to combine these in one application without a separate control program for each. Its question is whether a conversation among agents, with suitable roles and stop rules, can do work that would otherwise need a custom pipeline.

## Core idea

Each agent has a role, receives messages, keeps context from them, and produces replies through a common interface (send, receive and generate_reply). Capabilities may come from a language model, a human, a tool, or a combination. The paper's built-in types are:

- **ConversableAgent**, the base class, which by default can use language models, humans and tools.
- **AssistantAgent**, an LLM-backed agent given a system message for writing code and fixing errors.
- **UserProxyAgent**, an agent that asks a human for input, executes code another agent proposes, and makes function calls.
- **GroupChatManager**, which selects the next speaker and broadcasts that speaker's reply to the other agents.

When an agent receives a message, it calls generate_reply and sends the reply back, unless a termination condition holds. The paper calls this a decentralised mechanism: the exchange is driven by the agents' own replies, so no separate control plane is needed. Developers can register custom reply functions, for example to have one agent consult another before it answers the sender.

## Equation or algorithm

The procedure is a message loop rather than an equation:

1. Create agents with roles and capabilities: a model, a person, a tool, or a mix.
2. Send an initial message to one agent.
3. The receiving agent calls generate_reply. This may query a model, ask a person, run code or call a function.
4. Send the reply to the next agent. In a group chat, the manager picks the next speaker and broadcasts the reply.
5. Repeat until a termination condition holds: a maximum number of automatic replies, a condition written in code, or a reply containing a stop word. The default assistant prompt in the paper tells the agent to reply "TERMINATE" when finished.

Control can be written in natural language, in code, or in both. In code, a developer sets termination conditions, the human-input mode, the maximum number of automatic replies and any custom reply functions. Static flows use a fixed order of agents. Dynamic flows use custom reply functions, function calls chosen by the model, or a GroupChatManager.

## Results

On ALFWorld, a benchmark of text-based household tasks, the paper reports success rates averaged over three attempts. The three-agent ALFChat setup reached 69%, the two-agent setup 54%, and ReAct 54%. The best of three attempts gave 77%, 63% and 66%. In the per-task table, the three-agent setup scored 41% on the "Pick 2" task type, against 24% for ReAct on average.

On the MATH benchmark, the paper reports 69.48% for AutoGen on the full 5,000-problem test set, against 55.18% for GPT-4 alone. The paper also reports a retrieval-augmented question-answering scenario on Natural Questions, a coding scenario modelled on OptiGuide-style tasks, a dynamic group-chat pilot, and a chess scenario. The ALFWorld and MATH comparisons are the most systematic of these. The rest are demonstrations with less formal measurement.

## Limitations

- **Narrow evaluation.** The results come from a handful of scenarios and mostly from GPT-3.5 and GPT-4 models. Several scenarios are illustrations rather than measurements.
- **Cost.** Each agent adds model calls, and long conversations add tokens. The ALFWorld comparison averages over attempts, so it does not show how the gain compares with a single agent given the same token budget.
- **Termination is a design burden.** The developer has to set maximum reply counts or termination conditions, or the conversation can run longer than intended.
- **Human oversight is a choice.** Human input is configurable, and the paper recommends keeping humans in the loop at all times during development. The developer must make that choice.
- **Current status.** The stable documentation of the AutoGen project states that it "has been archived and is no longer actively maintained by Microsoft" (checked on 2026-11-18). The paper describes the design, so anyone adopting the software should first check its present status.

## Connections

- The alternative of a fixed role pipeline is [MetaGPT](metagpt.md), which ties each role to a predefined document.
- ReAct is the single-agent baseline in the ALFWorld comparison; see [ReAct](react.md).
- Conversation logs from these systems are the raw material for the tracing discussed in [Agent observability](agent-observability.md).
- The general framing of agents is on [AI Agents](../../theory/models/agents/index.md).

## Applications

- **Coding assistants**, in which one agent writes code, a user proxy runs it, and any errors are returned for revision.
- **Question answering over documents**, where an agent asks follow-up retrieval questions before it answers.
- **Human-supervised workflows**, in which a person approves each step before a tool acts.

## Open questions

- How much of a multi-agent gain comes from the division of roles, and how much from extra attempts and tokens?
- Which termination rules remain reliable in open-ended group conversations?
- Which conversation patterns generalise across tasks, and which are tuned to a single benchmark?

## References

### Seminal papers

- Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. arXiv. https://arxiv.org/abs/2308.08155 — The framework, its agent types and its conversation programming model, along with the experiments reported on this page.
- Yao, S. et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. https://arxiv.org/abs/2210.03629 — The single-agent reason-and-act method used as the baseline on ALFWorld.
- Shridhar, M. et al. (2020). *ALFWorld: Aligning Text and Embodied Environments for Interactive Learning*. arXiv. https://arxiv.org/abs/2010.03768 — The text-world benchmark of household tasks used in the paper's comparison.
- Hong, S. et al. (2023). *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*. arXiv; published at ICLR 2024. https://arxiv.org/abs/2308.00352 — A role-based framework with fixed intermediate documents, the main alternative to conversation-based design.

### Surveys and textbooks

- Xi, Z. et al. (2023). *The Rise and Potential of Large Language Model Based Agents: A Survey*. arXiv. https://arxiv.org/abs/2309.07864 — Survey of LLM-based agents across single-agent, multi-agent and human-agent settings.

### Articles and documentation

- Microsoft. *AutoGen documentation (stable)*. https://microsoft.github.io/autogen/stable/ — The project's own documentation. It states that the project has been archived and is no longer actively maintained.
