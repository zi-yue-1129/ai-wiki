---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - metrics
---

# Evaluation

Evaluation asks whether a model is good, in what sense, and how far the number can be trusted. This section covers the general theory: which metric answers which question, how to make a fair comparison, and what a benchmark score can and cannot show.

Practical guidance for language models and applications is in [Evaluation & Benchmarks](../../engineering/evaluation/index.md). Lists of named datasets are in [Datasets](../../reference/datasets/index.md).

## Three parts of every result

Every evaluation has three parts:

- a **metric**, a number computed from predictions and true answers;
- a **dataset**, the examples the metric is computed on;
- a **protocol**, which covers how the data is split, what is held out, and how uncertainty is reported.

A result is interpretable only when all three are stated. Changing any one of them, such as the split, the decision threshold or the prompt, can reverse the ranking of two methods.

## Sections

| Page | Core question |
|---|---|
| [Metrics](metrics/index.md) | Which number matches the decision: accuracy, ranking quality, calibration or error size? |
| [Protocols](protocols/index.md) | How do we split data, compare methods and report uncertainty without fooling ourselves? |
| [Benchmarks](benchmarks/index.md) | Which named test measures what, and what can its score show? |

Named benchmarks, grouped by task with one page per benchmark, are in [Benchmarks](benchmarks/index.md). For practical guidance on language-model benchmarks, see [Evaluation & Benchmarks](../../engineering/evaluation/index.md).

## Where the topic already appears

- Supervised metrics and validation are covered in depth in [Evaluation and Validation](../paradigms/supervised/evaluation-and-validation/index.md).
- Few-shot benchmarks are described in [Benchmarks and Foundation Models](../paradigms/meta-learning/benchmarks-and-foundation-models/index.md).
- Evaluation scenarios for continual learning are in [Evaluation and Scenarios](../paradigms/continual/evaluation-and-scenarios/index.md).
- Theory-side evaluation for self-supervised learning is in [Theory and Evaluation](../paradigms/self-supervised/theory-and-evaluation/index.md).

## Key ideas

- **Construct validity.** A score is evidence only for the property it was designed to measure. A high benchmark score does not establish usefulness in every setting (Raji et al., 2021).
- **Held-out data.** A test set is informative only if no decision was made using it. Repeated selection on a test set turns it into development data.
- **Memorisation.** Large networks can fit random labels, so a good training score says little about generalisation (Zhang et al., 2017).
- **Uncertainty.** A gap of a few points on a small test set may be noise. Report the size of the test set and an interval.
- **Comparability.** Two numbers can be compared only when their metrics and protocols match.

## Connections

The psychometric tradition of reliability, validity and item response theory is the older source of many of these ideas. See [Psychology & AI](../../brain-mind/psychology/index.md) for the cognitive side.

## Open questions

Benchmarks saturate, and pre-training data can contain their test items. Scores from model judges inherit the judge's biases. How to evaluate systems that change over time, or that act over many steps, is still unsettled.

## References

### Seminal papers

- Raji, I. D. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims based on benchmark performance.
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. https://arxiv.org/abs/2211.09110 — Evaluates language models across scenarios and metrics to expose capability gaps and trade-offs.
- Zhang, C. et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — Shows that networks can memorise random labels, so held-out tests are essential.

### Articles and documentation

- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. https://arxiv.org/abs/2306.05685 — Studies model-based judging, its agreement with humans and its biases.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Reference for standard metrics and scorers for classification and regression.
