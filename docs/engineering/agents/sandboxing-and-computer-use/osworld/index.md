---
status: draft
last_reviewed: 2026-10-28
tags:
- agents
- tools
- evaluation
aliases:
- OSWorld
- 開放式電腦任務
- Open-ended computer tasks
---

# OSWorld: Benchmarking Computer-Use Agents in Real Environments

OSWorld (Xie et al., 2024) is an execution-based environment and benchmark for agents that operate a real computer. Each task runs inside a virtual machine that can be reset to a saved state, and the agent sees the screen and acts with mouse and keyboard. It is one of three landmark methods on the [Sandboxing and Computer-Use Agents](../index.md) page, and it is the reference point there for screenshot-based agents.

## Overview

The authors argue that earlier benchmarks either lack an interactive environment or are limited to particular applications or domains. Real computer work moves between applications and files, so a single-application test misses much of it.

OSWorld supplies a real operating system, Ubuntu for its main benchmark, and defines each task as a starting configuration, an instruction and an evaluation script. The script inspects the resulting state, such as files or cookies, to decide success, so an answer that merely looks right in text does not count.

## Key concepts

- **Virtual machine snapshot**: a saved state of the operating system that can be restored before each run. The paper notes that the virtual machine prevents irreversible damage to the real host machine.
- **Observation**: what the agent receives. OSWorld allows a screenshot, an accessibility (a11y) tree, or both.
- **Action space**: executable `pyautogui` code, which lets an agent click, type, drag and press key combinations, together with three special actions: WAIT, FAIL and DONE.
- **Execution-based evaluation**: a per-task script that checks the final state of the machine, rather than comparing text to a reference.
- **GUI grounding**: turning a visual target into exact coordinates on the screen. The paper identifies this as a main source of failure.

## How it works

The interaction loop is as follows:

1. Restore the virtual machine from its snapshot and apply the task configuration, such as downloading files or opening an application.
2. Give the agent the instruction and its observation at step $t$, a screenshot $o_t$, an accessibility tree, or both.
3. The agent emits either a block of `pyautogui` code, or one of WAIT, FAIL and DONE.
4. The simulator runs the code in the virtual machine, and returns the new state and observation $o_{t+1}$.
5. Steps 2 to 4 repeat until the agent emits DONE or FAIL, or reaches the step limit, which is 15 in the paper's experiments.
6. The task's evaluation script inspects the machine and assigns a score between 0 and 1.

The benchmark contains 369 tasks on Ubuntu, covering web and desktop applications, file input and output, and workflows across several applications. A further 43 tasks are provided for Windows.

## Results

- **Overall.** Humans complete more than 72 percent of the tasks. The best model tested reaches 12.24 percent. The abstract reports these figures.
- **Multi-application workflows.** The highest baseline score on these tasks is 6.57 percent, according to the introduction.
- **Observation settings.** With GPT-4V, screenshot-only input gives the lowest overall result, 5.26 percent. Adding the accessibility tree or Set-of-Mark annotations helps some models and hurts others.
- **Input size and history.** Higher screenshot resolution and a longer trajectory history each improve results, and the paper reports that these can roughly double success in some settings.
- **Failure analysis.** Models struggle to predict precise coordinates from screenshots, repeat actions, get distracted by unexpected windows and lack knowledge of basic interface conventions.

The figures are those reported in the paper's abstract and tables. They describe models of 2024, and later systems have improved on them.

## Limitations

- **Platform bias.** The main benchmark is on Ubuntu. The Windows set is smaller and used for analysis.
- **Step limit.** A 15-step cap may cut off tasks that a person would finish, although the authors say it is enough for most tasks.
- **Desktop input only.** The action space is mouse and keyboard events, so touch gestures on mobile systems are outside the benchmark.

## Open questions

- **Grounding.** The gap between models and humans is largest in locating elements. Whether higher-resolution vision, better training or a combination with structured interface data closes it is unresolved.
- **Safety.** A virtual machine lets dangerous actions be tested without real harm, but a deployed agent on a personal machine lacks that protection.
- **Generalisation.** Success on a fixed set of 369 tasks may not indicate performance on unseen applications. The authors' own future-work list concentrates on GUI grounding, interaction knowledge and higher-resolution input.

## References

### Seminal papers

- Xie, T. et al. (2024). *OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments*. arXiv. https://arxiv.org/abs/2404.07972 — Introduces an execution-based environment and benchmark of 369 computer tasks across operating systems, with per-task evaluation scripts.
- Zhou, S. et al. (2023). *WebArena: A Realistic Web Environment for Building Autonomous Agents*. arXiv. https://arxiv.org/abs/2307.13854 — Self-hosted, reproducible websites for web agents, the browser-based precursor of OSWorld's sandboxed approach.
- Koh, J. Y. et al. (2024). *VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks*. arXiv. https://arxiv.org/abs/2401.13649 — Visual web benchmark that OSWorld's annotated-screenshot setting follows.
- Hong, W. et al. (2023). *CogAgent: A Visual Language Model for GUI Agents*. arXiv. https://arxiv.org/abs/2312.08914 — Visual language model that navigates PC and Android interfaces using screenshots alone.

### Surveys and textbooks

- Wang, L. et al. (2023). *A Survey on Large Language Model based Autonomous Agents*. arXiv. https://arxiv.org/abs/2308.11432 — Survey of LLM agents, which places computer-use agents within the broader set of perception, memory and action modules.

### Articles and documentation

- Anthropic (2024). *Computer use, Claude 3.5 Sonnet, and Claude 3.5 Haiku*. Anthropic News. https://www.anthropic.com/news/3-5-models-and-computer-use — Announces a beta in which a model reads screenshots and returns mouse and keyboard actions for the developer's software to perform.
- Anthropic (n.d.). *Computer use tool*. Claude Platform documentation. https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool — Documents the screenshot-and-action loop and advises running it in an isolated environment.
