---
status: draft
last_reviewed: 2026-10-28
tags:
- engineering
- agents
- reasoning
aliases:
- 多代理人辯論
- 多智慧體辯論
- Multi-agent debate
- Society of minds
---

# Multi-Agent Debate

Multi-agent debate (Du et al., 2023) runs several instances of a language model that each state an answer with its reasoning, read the others' arguments over a few rounds and revise their own answers before a final answer is chosen. It is one of three landmark methods on the [Multi-Agent Orchestration](../index.md) page, and the simplest of them, since no agent holds a role or a plan.

## Overview

A language model can be wrong and confident at the same time, and asking it to reflect on its own answer often reinforces the mistake. Liang et al. (2023) call this *degeneration of thought*: once a model has settled on an answer, self-reflection rarely dislodges it, even when the answer is wrong.

Debate changes the setting: several agents answer independently, so their errors differ, and later rounds expose flaws each would miss in its own text. Du et al. called the result a "society of minds". The method needs no fine-tuning and works with black-box models.

## Key concepts

- **Debater**: one model instance, prompted to answer and to justify the answer. Debaters may be copies of one model or different models.
- **Round**: one exchange in which every debater reads the previous answers and writes a new one.
- **Convergence**: the point at which the debaters agree. A debate can stop there, or run for a fixed number of rounds.
- **Judge**: in some variants a separate agent reads the debate and decides. Liang et al. use this form.
- **Majority vote**: the simplest way to combine answers, used as the baseline in the main experiments.

## How it works

In a simplified form, with $N$ debaters and $R$ rounds:

1. Give each debater the question and ask for an answer with its reasoning. In the first round the debaters do not see each other.
2. In round $r$, give each debater the question and the other debaters' answers from round $r-1$, and ask it to consider them and write an updated answer.
3. Repeat step 2 until the answers agree or $R$ rounds have passed.
4. Return the answer most debaters give at the end, or the judge's decision in the judge variant.

Du et al. used three debaters and two rounds in their main reasoning experiments, and report that accuracy rises as either number grows.

## Key methods

This page covers one method. For the alternatives, see [MetaGPT](../metagpt/index.md) for role-based teams and [HuggingGPT](../hugginggpt/index.md) for planner-worker delegation.

## Results

Du et al. test arithmetic, grade-school maths (GSM8K), chess move prediction, factual biographies and MMLU. In their main reasoning table, a single agent scores 67.0 percent on arithmetic, majority voting over three agents 69.0 percent and debate 81.8 percent. On grade-school maths the three figures are 77.0, 81.0 and 85.0 percent.[^1] On factuality, debate raises the biography score from 66.0 for a single agent to 73.8, and the MMLU score from 63.9 to 71.1.[^2] In the same table a single agent that reflects on its own answer scores 57.7 on MMLU, below its plain answer, which fits the degeneration-of-thought explanation.

## Limitations

- **Cost.** Each round multiplies the model calls and lengthens the context every debater reads. The paper calls the method more computationally expensive than other prompting techniques.[^1]
- **Long transcripts.** The authors observed that as debates grew longer, models struggled to process the whole transcript and attended mainly to the latest messages.
- **Agreement is not correctness.** Debates usually reached one answer, but it was not always right. Consensus can hide a shared error.
- **Shared blind spots.** Copies of one model may share the same gaps in knowledge.

## Open questions

- **Matched budgets.** Answers sampled from one model at the same cost can also be combined by vote. How much of debate's advantage survives an equal token budget is not settled by the 2023 results.
- **Judges.** Whether a judge improves on the agents' own consensus, and how often it is itself persuaded by a wrong argument, is still under study.
- **Where it helps.** Later work finds that the benefit of adding agents depends on the task structure (Kim et al., 2025). Where debate sits on that map is open.

## References

### Seminal papers

- Du, Y. et al. (2023). *Improving Factuality and Reasoning in Language Models through Multiagent Debate*. arXiv. https://arxiv.org/abs/2305.14325 — Introduces multi-round debate between language model instances, with results on arithmetic, grade-school maths, chess, biographies and MMLU.
- Liang, T. et al. (2023). *Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate*. arXiv. https://arxiv.org/abs/2305.19118 — Names the degeneration-of-thought problem in self-reflection and proposes a debate between agents managed by a judge.
- Wang, X. et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv. https://arxiv.org/abs/2203.11171 — Samples several reasoning paths and keeps the most consistent answer, the single-model analogue of voting among debaters.

### Surveys and textbooks

- Guo, T. et al. (2024). *Large Language Model based Multi-Agents: A Survey of Progress and Challenges*. arXiv. https://arxiv.org/abs/2402.01680 — Survey of LLM-based multi-agent systems, covering agent profiles, communication and the mechanisms behind their gains.

### Articles and documentation

- Anthropic (2025). *How we built our multi-agent research system*. Anthropic Engineering. https://www.anthropic.com/engineering/multi-agent-research-system — Describes a production multi-agent system and its token costs relative to single-agent chat.
- Kim, Y. et al. (2025). *Towards a Science of Scaling Agent Systems*. arXiv. https://arxiv.org/abs/2512.08296 — Controlled comparison of single-agent and multi-agent architectures, showing that the benefit depends on the structure of the task.

[^1]: Du et al. (2023), Table 1 and the limitations discussion, https://arxiv.org/abs/2305.14325 — Arithmetic, grade-school maths and chess results for single agent, majority vote and debate, with three agents and two rounds.
[^2]: Du et al. (2023), Table 2, https://arxiv.org/abs/2305.14325 — Factuality scores on biographies and MMLU for single agent, single agent with reflection and debate.
