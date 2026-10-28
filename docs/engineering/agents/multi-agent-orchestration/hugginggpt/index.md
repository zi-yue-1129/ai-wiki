---
status: draft
last_reviewed: 2026-10-28
tags:
- engineering
- agents
- tools
aliases:
- HuggingGPT
- 規劃者與工作者
- 規劃與委派代理人
- Planner-worker agents
---

# HuggingGPT

HuggingGPT (Shen et al., 2023) uses a large language model as a planner. It splits a user request into subtasks, assigns each subtask to a specialist model from the Hugging Face hub, runs the models and writes a final answer from their outputs. It is the planner-worker method on the [Multi-Agent Orchestration](../index.md) page.

## Overview

Many AI tasks need several specialist models at once. A single request may combine them, for example by detecting a pose in a photo and then generating a new image with that pose. Shen et al. propose that a language model should act as the controller: it reads the request, decides which models to use and in what order, and uses language as the interface between them.

The design separates deciding *what* to do and in *which order* from doing each part with the most suitable tool. The planner does not perform the specialist tasks itself.

## Key concepts

- **Planner**: the language model that parses the request into tasks and their dependencies.
- **Workers**: the specialist models, each described by a short text summary of its function.
- **Task graph**: the plan. The paper treats requests as directed acyclic graphs, so one task can use another's output as input.

## How it works

The paper describes four stages, each run as a prompt to the language model:

1. **Task planning.** The planner turns the request into a list of tasks, each with an identifier and the identifiers of the tasks it depends on.
2. **Model selection.** For each task, the planner picks a model from the candidates whose descriptions match the task type.
3. **Task execution.** The chosen models run in dependency order, and each output is stored for the tasks that need it.
4. **Response generation.** The planner reads the request, the plan, the chosen models and their outputs, and writes a reply that gives the answer and the process.

In the authors' example, pose detection runs first and its output conditions the image generation, so the planner must get that dependency right.

## Key methods

[MetaGPT](../metagpt/index.md) gives agents fixed roles, and [Multi-Agent Debate](../debate/index.md) gives them none. [ReAct](../../react/index.md) is the single-agent loop that planning systems extend.

## Results

The paper's main evidence is a set of demonstrations and an evaluation of the planning stage, since the quality of the plan limits everything after it. The authors measure planning on three kinds of request: single tasks, sequential tasks and graph tasks. With GPT-3.5 as planner, single-task planning reaches an accuracy score of 52.62.[^1] On graph tasks, a GPT-4 critic judges the plan correct with a score of 50.48 for GPT-3.5, against 13.14 for Alpaca-7b and 19.17 for Vicuna-7b, which shows the gap between the stronger and weaker planners.[^2] The paper does not report end-to-end accuracy on a standard benchmark.

## Limitations

- **Single point of failure.** A wrong plan propagates to every later step. A wrong model choice yields an output of the wrong kind.
- **Modest planning scores.** The reported planning accuracy for GPT-3.5 is about half, so a planner of this kind is far from reliable on complex requests. The authors' human-annotated set is small, 46 complex requests, and the other labels come from GPT-4.[^2]
- **Dependence on descriptions.** Model choice depends on the function text that each model carries. Poor descriptions lead to poor choices.

## Open questions

- **Plan checking.** Can the planner verify its own plan, or does a second model need to? The paper leaves this open.
- **Re-planning.** When a step fails, the plan has to be revised. How and when to do that is a practical question.

## Connections

Planning before acting is also the idea behind Plan-and-Solve prompting, which asks a model to devise a plan and then carry it out (Wang et al., 2023). In more recent systems, a lead agent plans, tracks progress and re-plans while it directs specialist agents, as in Magentic-One (Fourney et al., 2024). The cognitive view is close to the goal module of [ACT-R](../../../../brain-mind/cognitive-architectures/act-r/index.md), which holds the current objective and sets subgoals for the other modules.

## References

### Seminal papers

- Shen, Y. et al. (2023). *HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face*. arXiv. https://arxiv.org/abs/2303.17580 — A language model plans tasks, selects specialist models from Hugging Face and writes the final answer from their outputs.
- Wang, L. et al. (2023). *Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models*. arXiv. https://arxiv.org/abs/2305.04091 — Asks a model to devise a plan of subtasks before carrying them out, reducing missing-step errors in zero-shot reasoning.

### Surveys and textbooks

- Guo, T. et al. (2024). *Large Language Model based Multi-Agents: A Survey of Progress and Challenges*. arXiv. https://arxiv.org/abs/2402.01680 — Survey of LLM-based multi-agent systems, covering agent profiles, communication and the mechanisms behind them.

### Articles and documentation

- Fourney, A. et al. (2024). *Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks*. arXiv. https://arxiv.org/abs/2411.04468 — An orchestrator agent plans, tracks progress and re-plans while directing specialist agents for web, file and code tasks.
- Anthropic (2025). *How we built our multi-agent research system*. Anthropic Engineering. https://www.anthropic.com/engineering/multi-agent-research-system — A lead agent creates subagents for separate research tasks and combines their results, a planner-worker design in production.
- Kim, Y. et al. (2025). *Towards a Science of Scaling Agent Systems*. arXiv. https://arxiv.org/abs/2512.08296 — Shows that centralised coordination limits error propagation better than independent agents, depending on the task.

[^1]: Shen et al. (2023), Table 3 (single-task planning), https://arxiv.org/abs/2303.17580 — Accuracy of task planning with GPT-3.5, Alpaca-7b and Vicuna-7b.
[^2]: Shen et al. (2023), Table 5 (graph tasks) and the dataset description, https://arxiv.org/abs/2303.17580 — GPT-4 critic scores for graph-task planning, and the size and labelling of the human-annotated set.
