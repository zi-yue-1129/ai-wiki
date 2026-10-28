---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/agents
tags:
  - agents
  - software engineering
  - interfaces
aliases:
  - SWE-agent
  - Agent-Computer Interface
  - 代理電腦介面
  - 軟體工程代理
---

# SWE-agent (Yang et al., 2024)

SWE-agent is a language-model agent that resolves issues in software repositories. Its main contribution is an agent-computer interface (ACI): a set of commands designed for the model, such as viewing files, editing code and running tests, rather than the raw terminal that human engineers use. Yang et al. (2024) reported that this interface design strongly affects agent performance.

This page is part of [Agent Engineering](index.md). It is one of the named methods in the section, and it shows that the interface is a design variable as well as the model.

## Overview

A software engineering agent must find the relevant code in a large repository, edit files, and check the result by running tests. The paper's baseline gives the model only the default Linux shell. Yang et al. argue that language-model agents are a new category of end user, with their own needs and abilities, and that they benefit from interfaces built for them.

## Problem

The question is how interface design changes what an agent can do. Commands that are too coarse hide the information the model needs, while commands that are too fine make long tasks slow. The paper studies the effect of this design on performance.

## Core idea

The ACI gives the agent a small, documented set of commands designed for a language model rather than a human. According to the abstract, its effect is clearest on creating and editing code files. The design is evaluated by comparing agent behaviour under the custom interface with a shell-only baseline, which shows how the interface shapes the agent's steps and its results.

## Equation or algorithm

The agent runs the standard loop of observation and action:

1. Read the issue and the repository state through the interface.
2. Choose a command, such as searching for a symbol, opening a file or editing lines.
3. Read the command's output, which the interface formats for the model.
4. Run tests, and repeat until the tests pass or the attempt limit is reached.


## Results

The abstract reports a pass@1 rate of 12.5% on SWE-bench and 87.7% on HumanEvalFix, which the authors describe as state of the art on both at the time. The 12.5% is on the full 2,294-task SWE-bench test set. The previous best non-interactive, retrieval-augmented system reached 3.8% on that benchmark, and the custom interface gives a 64% relative increase over the shell-only baseline with GPT-4 Turbo.

## Limitations

- **Benchmark-specific figures.** The results are on SWE-bench and HumanEvalFix. SWE-bench measures resolving real issues, but it does not cover every kind of software work.
- **Model dependence.** The results depend on the language model used, which changes over time.
- **Interface cost.** A custom interface must be designed and maintained for each environment.
- **Safety of execution.** Running tests and programs requires a sandbox, as described on [Sandboxing and computer-use agents](sandboxing-and-computer-use.md).

## Connections

- The benchmark that SWE-agent is evaluated on is [SWE-bench](../../theory/evaluation/benchmarks/math-and-code/swe-bench.md), and the code benchmark HumanEval is on [HumanEval](../../theory/evaluation/benchmarks/math-and-code/humaneval.md).
- The reasoning-and-acting loop it uses is [ReAct](react.md).
- Coding assistants in practice are covered on [AI Coding Assistants](../coding-assistants/index.md).
- Tool protocols that expose such commands to models are on [Tool calling and the Model Context Protocol](tool-calling-and-mcp.md).

## Applications

- Automated issue resolution in open-source repositories.
- Bug fixing and test repair in continuous integration.

## Open questions

- Which interface features matter most, and can they be transferred between software environments?
- How should an agent recover when its interface hides the information it needs?

## References

### Seminal papers

- Yang, J. et al. (2024). SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. NeurIPS. https://doi.org/10.52202/079017-1601 — Introduces SWE-agent and the agent-computer interface, and reports results on SWE-bench and HumanEvalFix.
- Jimenez, C. E. et al. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR. https://arxiv.org/abs/2310.06770 — The benchmark of real GitHub issues used to evaluate the agent.
- Chen, M. et al. (2021). Evaluating Large Language Models Trained on Code. arXiv. https://arxiv.org/abs/2107.03374 — Introduces HumanEval, the code benchmark on which HumanEvalFix builds.
- Yao, S. et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR. https://arxiv.org/abs/2210.03629 — The reasoning-and-acting loop that interactive coding agents follow.

### Surveys and textbooks

- Xi, Z. et al. (2023). The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv. https://arxiv.org/abs/2309.07864 — Broad survey of LLM-based agents, covering their interfaces to tools and environments.
