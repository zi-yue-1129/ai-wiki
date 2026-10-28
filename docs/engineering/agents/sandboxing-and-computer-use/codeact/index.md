---
status: draft
last_reviewed: 2026-10-28
tags:
- agents
- tools
- security
aliases:
- CodeAct
- 可執行程式碼動作
- Executable code actions
---

# CodeAct: Executable Code Actions for LLM Agents

CodeAct (Wang et al., 2024) makes the action an LLM agent takes a piece of executable Python, run by an interpreter, instead of a JSON call or a line of text. The interpreter gives one bounded place to run and observe the agent's actions, which is why the method matters for sandboxing. It is one of three landmark methods on the [Sandboxing and Computer-Use Agents](../index.md) page.

## Overview

Most tool-using agents express each action in a fixed format: a JSON object naming a tool and its arguments, or a line of text that a parser maps to a function. This is simple, but the possible actions are limited to the tools the developer has defined. Combining tools is also awkward. Passing one tool's output into another, or repeating a call for each item in a list, takes a separate model turn for every step.

CodeAct replaces these formats with a single action space: executable Python. A tool call becomes a function call in code, a repeated call becomes a loop, and a value returned by one tool can be stored in a variable and used by the next. The agent sends code, the interpreter runs it, and the result returns to the agent as an observation.

## Key concepts

- **Action space**: the set of things the agent may do in one step. CodeAct makes this the set of Python programs.
- **Control flow**: loops and conditionals, which let one action process many items.
- **Data flow**: values held in variables, so that one step's output feeds the next without a round trip through the model's text.
- **Interpreter**: the Python process that runs the code. It is where actions are executed, observed and, when needed, restricted.
- **Multi-turn revision**: the agent may read an error or result and emit a corrected action.

## How it works

Each episode follows a loop:

1. The agent receives the user's request, with the available tools described as Python functions.
2. The model writes a code block that expresses its next action or set of actions.
3. The interpreter executes the code, capturing output, return values and error messages.
4. The captured output is appended to the conversation as an observation.
5. The model writes further code, revises earlier code after an error, or gives a final answer. The loop ends at a final answer or after a maximum number of turns.

The authors evaluate on M³ToolEval, a benchmark of problems that need several tools in combination, and on API-Bank, which tests atomic tool calls. On M³ToolEval a solution counts as successful when the answer matches the reference, and the paper also reports the average number of turns. The authors further build CodeActAgent, an open-source model fine-tuned from Llama 2 and Mistral on CodeActInstruct, a set of 7,000 multi-turn interactions in which actions are code. They report that this training improves agent tasks without removing general ability.

## Results

- **M³ToolEval.** Across 17 evaluated LLMs, CodeAct gives a higher success rate than the JSON or text baselines for 12 of them. The abstract reports up to a 20 percent higher success rate, and the text reports up to 30 percent fewer actions. The gains widen as the models become more capable.
- **API-Bank.** On atomic tool calls the picture is mixed. The paper's table shows that the best format varies with the model.
- **CodeActAgent.** The fine-tuned model shows limited ability to revise its actions after error messages. The paper presents it as an early prototype.

The main quantitative claims are taken from the paper's abstract and results text.

## Limitations

- **Prototype status.** The authors note that CodeActAgent may hallucinate, for example by describing the value of a variable it never printed.
- **Trust in execution.** Because the agent runs code, safety depends on the sandbox around the interpreter. The paper notes that an agent with free code execution could in the worst case break out of its sandbox, and calls for better safety mechanisms.
- **Benchmark scope.** The benchmarks are tool-use problems with known answers, not open-ended work on a real system with side effects.

## Open questions

- **Where to place the boundary.** A richer action space requires more careful restriction of the interpreter. Whether file, network and process limits can be expressed so that the model cannot route around them is an open engineering question, discussed on the [sandboxing topic page](../index.md).
- **Verifying code before running it.** Code can be inspected statically, checked against a policy or run in a dry-run mode. Which of these catches the failures that matter is not settled.
- **Self-improvement.** The authors suggest that agents could learn from their own mistakes through extended environment interaction. Whether this works without weakening the safeguards around execution is unknown.

## References

### Seminal papers

- Wang, X. et al. (2024). *Executable Code Actions Elicit Better LLM Agents*. arXiv. https://arxiv.org/abs/2402.01030 — Introduces CodeAct, which uses executable Python as the unified action space for LLM agents, with evaluations on 17 LLMs.
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — Introduces the reasoning-and-acting loop, whose actions use fixed text formats, against which CodeAct is compared.

### Surveys and textbooks

- Wang, L. et al. (2023). *A Survey on Large Language Model based Autonomous Agents*. arXiv. https://arxiv.org/abs/2308.11432 — Survey of LLM agents covering the tools and action formats that CodeAct proposes to replace.

### Articles and documentation

- Anthropic (2024). *Building effective AI agents*. Anthropic Engineering. https://www.anthropic.com/engineering/building-effective-agents — Practical guidance on agent loops and tools, and on when a simpler workflow is preferable to an autonomous agent.
- Anthropic (2025). *Making Claude Code safer with sandboxing*. Anthropic Engineering. https://www.anthropic.com/engineering/claude-code-sandboxing — Describes how a coding agent that executes commands is confined by file-system and network boundaries.
