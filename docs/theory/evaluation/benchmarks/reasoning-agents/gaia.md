---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reasoning-agents
---

# GAIA

GAIA (General AI Assistants) is a benchmark of real-world questions that need reasoning, multimodal understanding, web browsing and tool use. The questions are simple for a person but hard for most AI systems. The authors report that human respondents scored 92%, against 15% for GPT-4 equipped with plugins (Mialon et al., 2023).

## Task and data

Each question needs several abilities together, such as finding a fact on the web, reading an attached file or image, and combining the results into one answer. The benchmark is built to avoid tasks where models already beat people, such as specialist exams, and to test whether an assistant can handle an ordinary request with several steps (Mialon et al., 2023).

## Protocol and metric

Answers are short and checkable, so the metric is **exact-match accuracy** after normalisation. The test answers are held back, and results are submitted rather than computed locally. The score depends on the tools the system is allowed to use, so the tool set must be reported with the score.

## What it shows

The gap between people and the best systems at release is the main finding. It suggests that a system's ability on expert exams does not carry over to tasks that require routine tool use and web navigation (Mialon et al., 2023).

## Limitations

- **Live web.** Pages change over time, so the same question can have a different answer later. Results need the date of the run.
- **Small public split.** Few questions are public, so most reported results come from a held-out set that teams cannot inspect.
- **Tool access.** A system with a search engine and a browser is not comparable with one without them, even if the model is the same.

## Related

- [WebArena](webarena.md) tests agents in a controlled web environment rather than the open web.
- [ARC-AGI](arc-agi.md) tests rule acquisition from examples.
- [Reasoning and agents family overview](index.md) compares the benchmarks in this area.

## References

### Seminal papers

- Mialon, G. et al. (2023). *GAIA: a benchmark for General AI Assistants*. arXiv. https://arxiv.org/abs/2311.12983 — Introduces the real-world questions and the human-versus-system comparison.
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Argues that benchmarks should measure skill acquisition rather than task performance.

### Articles and documentation

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — In-context prompting, the usual setting for models evaluated on tool-use questions.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Intermediate reasoning steps that multi-step questions often rely on.

### Additional sources

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Discusses how benchmark design should separate learned knowledge from ability.
