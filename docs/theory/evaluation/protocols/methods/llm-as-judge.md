---
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - llm-as-judge
---

# LLM as Judge

LLM-as-judge is an evaluation protocol in which a language model scores another model's outputs against a written rubric or compares two outputs directly. It makes open-ended answers measurable at a scale that human raters cannot reach, but the judge has its own biases, so its scores must be checked against people (Zheng et al., 2023).

## Procedure

The protocol has three parts: a rubric that defines what a good answer is, a judge prompt that asks for a score or a preference, and a parser that turns the reply into a number. Pairwise comparison asks the judge which of two answers is better, and single-answer grading assigns each answer a score on a fixed scale (Zheng et al., 2023).

## Known biases

Zheng et al. (2023) report position bias, where the judge favours the first answer in a pair, verbosity bias, where longer answers score higher, and self-preference, where a judge favours answers in its own style. Swapping the order of the two answers and averaging both verdicts reduces position bias, and checking against a human-rated sample reveals the rest.

## Reporting

Report the judge model and version, the exact rubric and prompt, the order-swap policy, the agreement with human raters on a stated sample, and the number of judgements per item. A change to the rubric or the judge changes the score, so the baseline must be rescored.

## Limitations

- **Circularity.** A judge trained with the same preferences it is asked to apply can reward its own style.
- **Narrow rubrics.** A judge can be consistent and still measure the wrong thing.
- **Cost and drift.** Hosted judge models change over time, so results need the version and the date.

## Related

- [Protocols overview](../index.md) lists the other protocol methods.
- [Elo rating and arenas](elo-rating.md) aggregates preferences from many judgements.
- [Human evaluation](human-evaluation.md) provides the reference judgements that a judge must match.

## References

### Seminal papers

- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. arXiv. https://arxiv.org/abs/2306.05685 — Studies model-based judging, its agreement with humans and its position and verbosity biases.

### Articles and documentation

- Chiang, W.-L. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. arXiv. https://arxiv.org/abs/2403.04132 — Combines human pairwise preferences with model-based judging in a public platform.
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics to expose trade-offs.

### Additional sources

- Gehrmann, S. et al. (2022). *Repairing the Cracked Foundation: A Survey of Obstacles in Evaluation Practices for Generated Text*. arXiv. https://arxiv.org/abs/2202.06935 — Surveys evaluation practice for generated text and the validity problems it raises.
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
