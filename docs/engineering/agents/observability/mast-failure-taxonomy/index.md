---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/evaluation
- theory/models/agents
tags:
- engineering
- agents
- evaluation
aliases:
- MAST
- 多代理人系統失敗分類
- Multi-Agent System Failure Taxonomy
- multi-agent failure taxonomy
---

# MAST: A Failure Taxonomy for Multi-Agent Systems

MAST (Multi-Agent System Failure Taxonomy) is a list of 14 failure modes, grouped into three categories, for explaining why a multi-agent LLM system fails. Cemri et al. (2025) built it from annotated execution traces and paired it with an LLM annotator for labelling new traces. It is one of the key methods on the [Agent Observability and Tracing](../index.md) page.

## Overview

A multi-agent system gives several language-model agents distinct roles, such as planner, coder and reviewer, and lets them converse to finish a task. Their advantage over a single agent is often small. Cemri et al. report failure rates from 41% to 86.7% across seven open-source systems.[^1] Before a team can fix such failures it has to name them, and failure reports were often ad hoc, such as "the agents got confused", which cannot be compared across systems.

MAST provides a shared vocabulary: defined failure modes, each illustrated by examples, that annotators can apply to any trace. A failure is a run in which the system does not achieve its intended objective.

## Key concepts

- **Execution trace**: the full text of one run, including every message between agents and every tool result. The authors' traces average more than 15,000 lines, which makes hand labelling slow.
- **Failure mode**: a named, defined way that a run goes wrong, such as Step Repetition (1.3), Premature Termination (3.1) or Reasoning–Action Mismatch (2.6).
- **Category**: *system design issues* covers how roles, history and termination are specified. *Inter-agent misalignment* covers how agents interact, such as withholding information. *Task verification* covers how the result is checked, either too little or incorrectly.
- **Grounded theory**: the qualitative method used to derive the taxonomy. Categories come from close reading of the data rather than from a fixed list.
- **Cohen's κ**: an agreement statistic for two annotators that corrects for chance, $\kappa = (p_o - p_e)/(1 - p_e)$.

## How it works

The method runs in seven steps.

1. **Collect traces** from popular multi-agent frameworks on coding, math and general agent tasks.
2. **Open coding** on more than 150 traces from five open-source frameworks, with six expert annotators.
3. **Agreement check.** Three annotators label 15 traces independently, then refine the definitions until κ reaches 0.88.
4. **Taxonomy.** The result is 14 failure modes in three categories, each with a definition and examples.
5. **LLM annotator.** A reasoning model (OpenAI's o1) receives a trace, the MAST definitions and few-shot examples, and returns the failure modes it finds.
6. **Validation** against held-out human labels, and then on two frameworks and two benchmarks not used to build the taxonomy.
7. **Scaled labelling** of the full dataset, released as MAST-Data.

The core is the annotation procedure and the agreement test that checks whether each definition is clear enough to apply consistently.

## Results

The main evidence is the labelled dataset and the agreement figures, not a benchmark score.

- **Dataset.** MAST-Data contains 1,642 annotated traces from seven frameworks, run with GPT-4-series and Claude-series models.
- **Agreement.** Human annotators reached κ = 0.88 while building the taxonomy, and κ = 0.79 on traces from two further systems and benchmarks.
- **LLM annotator.** With few-shot examples, o1 matched the held-out human labels with 94% accuracy and κ = 0.77. Without examples it reached 89% accuracy and κ = 0.58.[^2]
- **Interventions.** In one ChatDev case, letting the CEO agent have the final say raised task success by 9.4%. On a 32-task ChatDev benchmark, an improved prompt raised accuracy from 25.0% to 34.4%, and a redesigned topology to 40.6%. In the AG2 case with GPT-4, the improved prompt helped significantly, but the topology change did not (Wilcoxon p = 0.4).[^2]

## Limitations

- **Coverage.** The authors do not claim the taxonomy covers every failure pattern.
- **Annotator dependence.** The scaled labels come from one reasoning model, and its agreement without examples was far lower, so the labels depend on prompt and model choice.
- **Partial fixes.** The case-study changes helped, but not every failure mode was resolved.
- **Labels are not causes.** A label says what went wrong, not which agent or step caused it. A mode can also appear at several pipeline stages.

## Open questions

- Does the taxonomy transfer to other systems, tasks and later models?
- Can labels support causal attribution? Zhang et al. (2025) found that automated judges identified the responsible agent far more often than the decisive error step. The best method reached 53.5% agent-level and 14.2% step-level accuracy.[^3]
- When is a workflow change more effective than a prompt change? The two case studies point in different directions.

## References

### Seminal papers

- Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?*. arXiv. https://arxiv.org/abs/2503.13657 — Introduces MAST and MAST-Data, with 1,642 annotated traces from seven multi-agent frameworks and an LLM annotator.
- Zhang, S. et al. (2025). *Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems*. arXiv. https://arxiv.org/abs/2505.00212 — Introduces the Who&When dataset of failure logs from 127 multi-agent systems and compares three methods for finding the responsible agent and step.
- Qian, C. et al. (2023). *ChatDev: Communicative Agents for Software Development*. arXiv. https://arxiv.org/abs/2307.07924 — Multi-agent framework that simulates a software company with role-specific agents, one of the systems whose traces MAST analyses.
- Wu, Q. et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. arXiv. https://arxiv.org/abs/2308.08155 — Open-source framework for building applications from conversing agents; MAST studies its later version, AG2.

### Articles and documentation

- Anthropic (2024). *Building effective AI agents*. Anthropic Engineering. https://www.anthropic.com/engineering/building-effective-agents — Notes that agents can compound errors and recommends extensive testing in sandboxed environments.

[^1]: Cemri et al. (2025), Section 1, https://arxiv.org/abs/2503.13657
[^2]: Cemri et al. (2025), Table 2 and Appendix H, https://arxiv.org/abs/2503.13657
[^3]: Zhang et al. (2025), abstract and Table 1, https://arxiv.org/abs/2505.00212
