---
status: draft
last_reviewed: 2026-11-18
related:
  - theory/models/agents
tags:
  - agents
  - multi-agent
  - software engineering
aliases:
  - MetaGPT
  - Meta Programming
  - 標準作業程序代理
  - 元程式設計多代理框架
---

# MetaGPT (Hong et al., 2023)

MetaGPT is a multi-agent framework that gives language-model agents the roles of a software company: a product manager, an architect, a project manager, an engineer and a QA engineer. Each role produces a defined document, and the documents pass along a pipeline. Hong et al. (2023) report that this structure reaches higher Pass@1 scores on the HumanEval and MBPP code benchmarks than the code models they compare against. The paper was published at ICLR 2024.

This page is one of the named methods behind the sequential-pipeline pattern in [Multi-agent orchestration patterns](multi-agent-orchestration.md). It is part of [Agent Engineering](index.md).

## Overview

Software development suits a pipeline because the work already divides into stages with recognisable outputs: a requirement, a design, a plan, code and tests. MetaGPT takes that division from human practice and gives each stage to one agent. The paper's central claim is that structured intermediate documents stop errors from accumulating along the chain.

## Problem

Language models chained without structure can produce results that contradict one another, because an early error is carried forward and amplified. The abstract attributes the failure of earlier systems on complex tasks to "logic inconsistencies due to cascading hallucinations caused by naively chaining LLMs." The paper asks how a group of agents can handle a complex task while each step's output stays checkable.

## Core idea

The authors encode standardised operating procedures (SOPs), the written routines that human teams follow, as prompt sequences. Each role has a required output:

- The **product manager** writes a product requirements document (PRD) with user stories and a requirement pool.
- The **architect** turns the PRD into file lists, data structures, interface definitions and a sequence-flow diagram.
- The **project manager** splits the design into a task list, with each code file as one task.
- The **engineer** implements the assigned classes and functions, writes unit tests, runs them and debugs.
- The **QA engineer** writes test cases to enforce code quality.

The paper calls this an assembly-line paradigm. The intermediate documents act as a contract between roles: each agent receives a defined input and must produce a defined output.

## Equation or algorithm

The procedure is a fixed sequence of steps:

1. Receive a one-line requirement from the user.
2. The product manager produces the PRD.
3. The architect produces the system design.
4. The project manager produces the task list, with one task per code file.
5. The engineer implements each file, writes unit tests, executes them and revises the code from the results.
6. The QA engineer writes test cases.
7. The output is the set of documents and code that together form the software solution.

Step 5 is where executable feedback enters. The authors remove it in an ablation to measure its effect.

## Results

On HumanEval (164 tasks) and MBPP, measured with Pass@1, MetaGPT scored 85.9% and 87.7%. Without executable feedback it scored 81.7% and 82.3%, so feedback added 4.2 and 5.4 points. The paper reports higher figures than the code models in its comparison.

The margin over a strong single model is smaller. The authors' own single-agent GPT-4 runs on HumanEval scored 72.4% with a direct API call, and 80.0% to 81.2% with an added system prompt or better answer parsing. Much of the gap to earlier systems therefore depends on how the baseline is run.

On the paper's SoftwareDev comparison, MetaGPT scored 3.75 on executability against 2.25 for ChatDev, and its human revision cost was 0.83 against 2.5. It also used more tokens: 31,255 against 19,292.

## Limitations

- **Scope of roles.** The authors state that the system cannot fully cater to scenarios such as UI and front-end work, because it has no agents or multimodal tools for them.
- **Complex requirements.** Despite producing more code than comparable frameworks, the authors acknowledge that it remains hard to meet the diverse, complex requirements of real applications.
- **Interruption.** A key challenge for users is interrupting an agent's running process or setting checkpoints.
- **Self-improvement.** The self-improvement mechanism changes only role constraints, not the communication interfaces between roles (appendix A.1). Each project also runs independently.
- **Narrow benchmarks.** HumanEval and MBPP test short, function-level programs. Their scores do not measure delivery of a whole software project.
- **Cost.** The SoftwareDev token counts show that a structured role pipeline can use more tokens than the alternatives.

## Connections

- The conversation-based alternative is [AutoGen](autogen.md), where the flow comes from message exchange rather than from fixed roles.
- A single-agent software engineer that works on repository issues is [SWE-agent](swe-agent.md).
- The general framing of agents is on [AI Agents](../../theory/models/agents/index.md).

## Applications

- **Prototype generation** from a short requirement, with the design documents reviewed before the code is accepted.
- **Engineering documentation**, where requirement and design documents are drafted for human review.

## Open questions

- Do SOPs written for software development transfer to other domains, such as hardware design or research?
- How should a person intervene in a long pipeline without breaking the shared documents?
- What happens when requirements change in the middle of the pipeline?

## References

### Seminal papers

- Hong, S. et al. (2023). *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*. arXiv; published at ICLR 2024. https://arxiv.org/abs/2308.00352 — Assigns software-company roles to agents, encodes SOPs as prompts, and reports HumanEval and MBPP results with and without executable feedback.
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces HumanEval, a benchmark of program synthesis from docstrings.
- Austin, J. et al. (2021). *Program Synthesis with Large Language Models*. arXiv. https://arxiv.org/abs/2108.07732 — Introduces MBPP, a benchmark of short Python programs written from plain-language descriptions.
- Qian, C. et al. (2023). *ChatDev: Communicative Agents for Software Development*. arXiv. https://arxiv.org/abs/2307.07924 — A role-based software-development framework that the paper compares against.
- Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. arXiv. https://arxiv.org/abs/2308.08155 — The conversation-based alternative to fixed role pipelines.

### Surveys and textbooks

- Xi, Z. et al. (2023). *The Rise and Potential of Large Language Model Based Agents: A Survey*. arXiv. https://arxiv.org/abs/2309.07864 — Survey of LLM-based agents, including multi-agent collaboration.
