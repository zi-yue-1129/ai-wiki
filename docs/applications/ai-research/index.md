---
related:
  - theory/models/agents
  - theory/models/llm
  - engineering/coding-assistants
aliases:
  - AI 研究
  - 自動化科學
  - AI 科學家
---

# AI for AI Research

Researchers now use AI to read literature, write and run code, design experiments and draft papers. Some groups have built systems that attempt the whole loop, and benchmarks now measure whether agents can reproduce or extend published research. The idea that AI could speed up its own improvement is discussed as a serious possibility, and as a source of risk.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Literature review and search | Retrieval-augmented question answering over papers | Citation accuracy is the main concern |
| Idea generation | Language models proposing research directions | Human studies find novelty and quality vary |
| Experiment design and execution | Coding agents that write, run and debug experiments | Requires sandboxing and compute budgets |
| End-to-end research agents | Systems that generate ideas, run experiments and write papers | The AI Scientist (Lu et al., 2024) |
| Research-ability benchmarks | Tasks drawn from machine learning engineering and paper replication | MLE-bench, PaperBench |
| Software engineering agents | Agents that resolve real repository issues | SWE-bench (Jimenez et al., 2024) |

## How an automated research loop works

A typical system proposes an idea, writes code to test it, runs the experiment, reads the results and decides what to try next. Some systems also draft a paper and review it. Each step can use a language model, while the experiment runner and the evaluation remain conventional code, so that results can be checked.

## Why it is hard

- **Evaluation is the bottleneck**: judging whether a research idea is good takes expert time, and automatic judges can be fooled.
- **Reproducibility**: agents can report results that do not reproduce, or that depend on a bug in the evaluation.
- **Compute and cost**: each experiment uses resources, and search over many ideas multiplies the cost.
- **Novelty**: an idea that looks new may be close to existing work that the system did not find.

## Key methods

- [LLM-based agents](../../theory/models/agents/index.md): plan, act with tools and observe results in a loop, the core of research agents.
- [Chain-of-thought reasoning](../../theory/models/reasoning/chain-of-thought.md): step-by-step reasoning that research agents use to plan experiments.
- [Large Language Models](../../theory/models/llm/index.md): the language components that read papers and write code.
- [Evaluation & benchmarks](../../engineering/evaluation/index.md): how research ability is measured and where benchmarks mislead.

## Connections

- The coding-agent tools that research groups use are covered in [AI Coding Assistants](../../engineering/coding-assistants/index.md) and [Software Development](../software/index.md).
- Automated science in physical and biological fields is covered in [Scientific Discovery](../science/index.md).
- The debate over recursive self-improvement, and the safety questions it raises, is discussed in [Safety & Alignment](../../society/safety-alignment/index.md).

## Applications

- Literature review and summarisation
- Writing and running experiment code
- Generating and screening research ideas
- Reproducing published results as a check on papers
- Automating machine learning engineering tasks

## Risks and limits

- **Unreliable reporting**: automated papers can contain mistakes that are hard to notice.
- **Evaluation hacking**: an agent that optimises a measurable target can exploit the measurement.
- **Research integrity**: volume of AI-written papers strains peer review.
- **Recursive improvement**: if AI systems can improve AI research, the pace of progress and the need for oversight both change. Experts disagree about how likely and how fast this is.

## Open questions

- Whether AI-generated ideas are more or less novel and useful than those of human researchers, once evaluated under controlled conditions.
- How to design benchmarks for research ability that resist gaming.
- What oversight should apply to systems that run research on their own successors.

## References

### Seminal papers

- Lu, C. et al. (2024). The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv. https://arxiv.org/abs/2408.06292 — Describes a system that generates ideas, writes code, runs experiments and drafts papers end to end.
- Si, C., Yang, D. & Hashimoto, T. (2024). Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers. arXiv. https://arxiv.org/abs/2409.04109 — Compares expert reviews of language-model and human research ideas in a controlled study.
- Jimenez, C. E. et al. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? *ICLR*. https://arxiv.org/abs/2310.06770 — Benchmark of real software issues that measures whether agents can produce working repository fixes.

### Surveys and textbooks

- Chan, J. S. et al. (2024). MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering. arXiv. https://arxiv.org/abs/2410.07095 — Benchmark of machine learning engineering competitions for measuring agent ability on real ML tasks.
- Starace, G. et al. (2025). PaperBench: Evaluating AI's Ability to Replicate AI Research. arXiv. https://arxiv.org/abs/2504.01848 — Benchmark in which agents reproduce results from machine learning papers, graded against author rubrics.
- Huang, Q. et al. (2023). MLAgentBench: Evaluating Language Agents on Machine Learning Experimentation. arXiv. https://arxiv.org/abs/2310.03302 — Benchmark of experimentation tasks for language agents, covering reading, coding and iterating on ML projects.
- Wei, J. et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS*. https://arxiv.org/abs/2201.11903 — Shows that step-by-step reasoning examples substantially improve language model performance on multi-step problems.
