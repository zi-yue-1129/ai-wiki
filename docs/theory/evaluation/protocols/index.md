---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - statistics
---

# Evaluation Protocols

A protocol defines how the data is divided, which comparisons are made, and how uncertainty is reported. Protocol mistakes often change a conclusion more than the choice of metric does.

## Methods

Each method has its own page.

| Method | Used for |
|---|---|
| [Cross-validation](methods/cross-validation.md) | Estimating generalisation from several splits |
| [Paired bootstrap](methods/paired-bootstrap.md) | Intervals for the difference between two methods |
| [LLM as judge](methods/llm-as-judge.md) | Scoring open-ended outputs with a model |
| [MT-Bench](methods/mt-bench.md) | Pairwise judging with swapped order, and its agreement with human experts |
| [Length-controlled AlpacaEval](methods/length-controlled-alpacaeval.md) | Correcting an automatic judge's preference for longer answers |
| [Human evaluation](methods/human-evaluation.md) | Judging outputs with people, with agreement reported |
| [Elo rating and arenas](methods/elo-rating.md) | Ranking systems from pairwise outcomes |
| [Contamination detection](methods/contamination-detection.md) | Checking whether benchmark items were in training data |

## Splitting the data

- **Train, validation and test.** Tune on validation and report on test once.
- **Cross-validation** averages over several splits. Use stratified folds when classes are imbalanced.
- **Group and time splits.** Keep all examples from one patient, user or conversation in the same fold. For forecasting, validate only on data later than the training data.
- **Keep the test set out of decisions.** Once a test set guides model choices, it is development data, and a new test set is needed for the final claim.

The scikit-learn guide on cross-validation describes these splits (see References).

## Avoiding leakage

- Fit preprocessing, such as scaling or feature selection, only on the training data. Pipelines enforce this; preprocessing the whole dataset before splitting leaks information.
- Remove duplicates that appear in more than one split.
- For language models, record what is known about overlap between the test items and the training corpus. Holding out an application set does not prove a pretrained model has never seen its content.

## Comparing methods fairly

- **Fix the conditions.** Each method should get the same split, data budget and tuning effort. Giving one method more tuning is a common source of false conclusions.
- **Compare on the same examples.** Paired comparisons are more sensitive than comparing two independent averages.
- **Keep a run record.** Store the model version, dataset version, prompt, random seeds and attempt limits with every result. Tools such as Inspect and lm-evaluation-harness are built around this practice (see References).

## Reporting uncertainty

Report the number of examples as well as the score. On 100 tasks, moving from 80 to 82 correct answers adds two successes, which alone does not show a better system.

A **paired bootstrap** resamples matched examples together to estimate the uncertainty of a difference between two methods (SciPy documents this option). Choose the resampling unit to match how the data depends on itself: several turns in one conversation are not independent examples. Training randomness is a separate source of variation, so repeat training with several seeds when the claim depends on it.

## Judges and human raters

An **LLM judge** scores outputs against a rubric. Zheng et al. (2023) document position, verbosity and self-preference biases. Good practice is to compare the judge with a human-rated sample, swap the order of answers in pairwise comparisons, and rescore the baseline whenever the rubric changes.

For **human evaluation**, report who the raters were, what instructions they received and how well they agreed with one another. Without these, the result cannot be repeated.

## What a benchmark score can show

A benchmark is a shared task with a fixed scoring rule. Its score shows how a system performs on that task, under that protocol. It does not show performance on every task that resembles it. Liang et al. (2022) argue for evaluating across scenarios and metrics together, so that trade-offs such as accuracy against robustness or cost become visible. Raji et al. (2021) discuss the limits of claims that go beyond what a benchmark measures.

## Open issues

Contamination is hard to detect when the training data is closed. Evaluating agents, which act over many steps with tools, needs protocols that record the environment as well as the answer. Statistical methods for comparing many methods on many benchmarks at once are still less settled than the single-benchmark case.

## Tools

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) runs shared language-model evaluation tasks. [Inspect](https://inspect.aisi.org.uk/) provides composable datasets, solvers, scorers and evaluation logs.

## References

### Seminal papers

- Raji, I. D. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims based on benchmark performance.
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. https://arxiv.org/abs/2211.09110 — Evaluates language models across scenarios and metrics to expose capability gaps and trade-offs.
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. https://arxiv.org/abs/2306.05685 — Studies model-based judging, its agreement with humans and its biases.

### Articles and documentation

- scikit-learn contributors. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — Explains held-out testing, model selection, group splits and time-aware evaluation.
- scikit-learn contributors. *Common pitfalls and recommended practices*. https://scikit-learn.org/stable/common_pitfalls.html — Demonstrates preprocessing leakage and how pipelines restrict fitting to training data.
- SciPy contributors. *scipy.stats.bootstrap*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html — Describes bootstrap confidence intervals and paired resampling for matched observations.
- UK AI Security Institute and Meridian Labs. *Inspect*. https://inspect.aisi.org.uk/ — Documents composable datasets, solvers, scorers, agent evaluations and evaluation logs.
- EleutherAI. *Language Model Evaluation Harness*. https://github.com/EleutherAI/lm-evaluation-harness — Provides reusable language-model evaluation tasks, configuration and execution tooling.
