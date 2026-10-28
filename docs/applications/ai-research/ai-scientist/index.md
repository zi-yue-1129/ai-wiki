---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/science
  - engineering/evaluation
tags:
  - agents
  - evaluation
aliases:
  - The AI Scientist
  - AI 科學家
  - 全自動科學發現
---

# The AI Scientist (Lu et al. 2024)

The AI Scientist is a pipeline that runs the whole cycle of machine-learning research, from generating an idea to writing a paper that an automated reviewer then scores. Chris Lu and colleagues reported it in 2024. It is one of the three landmark methods on the parent page [AI for AI Research](../index.md).

## Overview

Earlier research assistants helped with one step at a time: brainstorming, drafting code or summarising results. The AI Scientist was built to run all of these steps and to repeat them. The authors describe the goal as bringing AI agents to "the entire research process of AI itself" (Lu et al., 2024). They applied the system to three subfields of machine learning: diffusion modelling, transformer-based language modelling and learning dynamics.

The method is interesting for two reasons. It shows that a whole research paper can be produced by a loop of language-model calls and code execution. It also tries to make the output judgeable at scale, by pairing the writing step with an automated reviewer. Its literature-review counterpart is [OpenScholar](../openscholar/index.md), and its self-modifying counterpart is the [Darwin Gödel Machine](../darwin-godel-machine/index.md). Lab automation and AI scientists in other fields are covered in [Scientific Discovery](../../science/index.md).

## Key concepts

- **Idea generation**: a language model proposes new research directions, which are then developed into concrete experiments.
- **Experiment code**: the system writes and modifies code, runs the experiments and visualises the results.
- **Automated reviewer**: a language model that reads a finished paper and scores it in the style of a conference review. The authors designed and validated it against human scores.
- **Open-ended loop**: the process can repeat, so later ideas build on earlier results, which the authors describe as developing ideas in an open-ended fashion.

## How it works

The system runs the following steps for each idea:

1. Generate a research idea and a plan for testing it.
2. Write and modify code, run the experiments and produce plots of the results.
3. Describe the findings by writing a full scientific paper.
4. Give the paper to the automated reviewer, which simulates a review process and returns scores.
5. If the scores and the results are worth extending, repeat from step 1 with the new results as context.

The output of one pass is a paper and a set of review scores. It is not a verified finding. The review step makes it possible to compare many outputs cheaply, but it does not replace an expert check.

## Results

The abstract reports that each idea was implemented and developed into a full paper for less than $15 per paper, under the authors' setup. The authors state that their automated reviewer achieved near-human performance in evaluating paper scores. By that reviewer's judgement, some generated papers exceeded the acceptance threshold of a top machine-learning conference. The acceptance claim therefore rests on the automated reviewer, and not on a human program committee.

## Limitations

- **Self-judged evaluation.** The headline claim depends on the system's own reviewer. Agreement with human scores is a measure of similarity, not proof that a paper is correct or novel.
- **Narrow scope.** The paper tests three subfields of machine learning, where experiments run on a computer and are cheap to repeat. Fields that depend on slow or physical experiments are not covered.
- **Cost figure.** The cost of less than $15 per paper depends on the models and prices used at the time, and will change.
- **Unattended code.** A system that writes and runs its own code needs strict isolation. See [sandboxing and computer use](../../../engineering/agents/sandboxing-and-computer-use/index.md).
- **Surface quality.** A paper can read well while its claims are thin or wrong. Messeri and Crockett (2024) warn that AI tools can give researchers an illusion of understanding.

## Open questions

- Does the automated reviewer keep tracking human judgement as generated papers become more novel?
- Do results produced this way replicate when other researchers repeat them?
- How much of the quality comes from the human-designed experiment setup, and how much from the language model?

## References

### Seminal papers

- Lu, C. et al. (2024). The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv. https://arxiv.org/abs/2408.06292 — Introduces a pipeline that generates ideas, writes code, runs experiments and writes papers, scored by an automated reviewer.
- Boiko, D. A. et al. (2023). Autonomous chemical research with large language models. *Nature*. https://doi.org/10.1038/s41586-023-06792-0 — Describes Coscientist, a GPT-4 system that plans and performs chemistry experiments using tools.

### Articles and documentation

- Gottweis, J. et al. (2025). Accelerating scientific discovery with Co-Scientist. arXiv. https://arxiv.org/abs/2502.18864 — Multi-agent system built on Gemini that generates and refines research hypotheses, validated in three biomedical applications.
- Schmidgall, S. et al. (2025). Agent Laboratory: Using LLM Agents as Research Assistants. arXiv. https://arxiv.org/abs/2501.04227 — Framework that takes a human-provided research idea and works through the research process with LLM agents.
- Messeri, L. & Crockett, M. J. (2024). Artificial intelligence and illusions of understanding in scientific research. *Nature*. https://doi.org/10.1038/s41586-024-07146-0 — Commentary on how AI tools can make researchers feel they understand more than they do.
