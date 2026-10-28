---
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - human-evaluation
---

# Human Evaluation

Human evaluation asks people to judge system outputs directly, for example on fluency, correctness or preference. It is the reference against which automatic metrics and model judges are checked, but it is only useful when the raters, the instructions and the agreement between raters are reported (Gehrmann et al., 2022).

## Procedure

Raters receive instructions and a rating scale, usually with worked examples, and each item is rated by several people. Pairwise preference, where raters choose between two outputs, is often more reliable than an absolute scale. The sample of items should be drawn to represent the use case, not chosen to favour one system.

## Agreement

Inter-rater agreement shows whether the judgements are consistent enough to mean something. Common statistics include Cohen's kappa for two raters and Krippendorff's alpha for several, and they should be reported with the number of items and raters. Low agreement suggests the rubric is unclear, not that the raters are careless.

## Reporting

Report who the raters were and how they were recruited, what they were paid or instructed, the scale and the instructions, the number of items and ratings, the agreement statistic and how disagreements were resolved. Without these, the result cannot be repeated.

## Limitations

- **Cost.** Human ratings are slow and expensive, so samples are small and intervals are wide.
- **Rater effects.** Expertise, fatigue and the order of items can change the judgements.
- **Validity.** A rating scale captures what it asks for, and a fluent answer can still be wrong.

## Related

- [LLM as judge](llm-as-judge.md) is checked against human ratings like these.
- [Elo rating and arenas](elo-rating.md) aggregates human pairwise preferences.

## References

### Seminal papers

- Gehrmann, S. et al. (2022). *Repairing the Cracked Foundation: A Survey of Obstacles in Evaluation Practices for Generated Text*. arXiv. https://arxiv.org/abs/2202.06935 — Surveys evaluation practice for generated text, including the reporting problems of human evaluation.

### Articles and documentation

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Evaluates models across scenarios and metrics, with human judgements alongside automatic ones.
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. arXiv. https://arxiv.org/abs/2306.05685 — Compares model-based judges with human preferences.

### Additional sources

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
