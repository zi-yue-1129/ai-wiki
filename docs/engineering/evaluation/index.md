---
related:
- theory/machine-learning
- brain-mind/psychology
- society/safety-alignment
- applications/software
---

# Evaluation & Benchmarks

Evaluation measures how an AI system behaves under specified conditions. A benchmark provides a shared comparison task; an application evaluation asks whether the whole system meets its users' needs. A leaderboard alone cannot establish usefulness in every setting.[^validity]

Metric definitions, statistical uncertainty and evaluation protocols are covered in the Theory section, in [Evaluation](../../theory/evaluation/index.md). This page shows how to apply them to language models and applications.

## Major benchmarks (as reference points)

These examples are a starting catalogue, not a ranking of current models. Record the benchmark version, evaluation date and protocol with every result.

| Area | Benchmarks | Interpretation |
|---|---|---|
| General knowledge | MMLU, MMLU-Pro | Check subject and language coverage |
| Hard expert questions | GPQA Diamond, Humanity's Last Exam | Record task selection and tool access |
| Math | GSM8K, MATH, AIME, FrontierMath | Record answer checking and attempt budgets |
| Code | HumanEval, SWE-bench Verified, LiveCodeBench | See [Software Development](../../applications/software/index.md) |
| Reasoning / abstraction | ARC-AGI-1/2 | Check separation of development and test tasks |
| Agents | GAIA, WebArena, OSWorld, τ-bench, Terminal-Bench | Record tool permissions and failure handling |
| Long context | Needle-in-a-haystack, RULER, LongBench | Retrieval ≠ reasoning over long inputs |
| Multimodal | MMMU, MathVista, Video-MME | |
| Chinese / Traditional Chinese | C-Eval, CMMLU, TMMLU+ | |
| Human preference | Chatbot Arena | Rater population and presentation affect interpretation |
| Safety | HarmBench, StrongREJECT, WMDP, dangerous-capability evals | See [Safety & Alignment](../../society/safety-alignment/index.md) |

## Designing an evaluation protocol

### Define the task and the decision

Write the intended use, target population and failure costs before selecting a metric. A document assistant might need correct answers, supporting evidence and appropriate abstention when evidence is missing. A single preference score does not test all three. HELM illustrates evaluation across multiple scenarios and dimensions, including accuracy, robustness and efficiency.[^helm]

For supervised metrics and validation methods, see [Evaluation and Validation](../../theory/paradigms/supervised/evaluation-and-validation/index.md). Here the focus is the surrounding system: prompts, retrieval, tools, graders and reporting.

### Separate development from final testing

Use development examples to change prompts, choose models and tune retrieval. Reserve a test set for the final comparison; repeatedly selecting improvements on it turns it into development data. Match the split to deployment: keep each person's or group's observations together when evaluating new groups, and preserve time order for forecasting.[^splits]

Fit learned preprocessing, such as scaling or feature selection, only on training data. Pipelines keep these operations inside training folds; preprocessing the entire dataset before splitting leaks information.[^leakage] For language models, record what is known about training overlap. Holding out an application set does not prove that a pretrained model has never encountered its content.

### Freeze the comparison conditions

Keep a run record with the model identifier, dataset version, evaluation code revision, prompt template, demonstrations, sampling settings, attempt limits and token budget. For tool-using systems, include the retrieval corpus snapshot, tool versions, permissions and environment. Record grader versions, rubrics, timeouts and how invalid outputs are scored.

This is a practical reporting checklist. Systems with different tools or budgets are different configured systems; describe that distinction in the result. Retain per-example outputs and failures alongside averages. Inspect provides composable datasets, execution, scoring and evaluation logs.[^inspect]

## Checking graders and uncertainty

Use deterministic checks where a task has explicit criteria: exact answers, schema validation or executable tests. Passing a schema check establishes format, not factual correctness.

An **LLM-as-judge** grades outputs using another language model and a rubric. Zheng et al. document position, verbosity and self-enhancement biases, as well as reasoning limitations.[^judge] Compare judgments with a human-rated sample, inspect disagreements and swap answer order in pairwise comparisons to diagnose position effects. Agreement on one dataset does not guarantee agreement in another domain or language. When a rubric changes, rescore the baseline too.

Report the example count, score definition and uncertainty. Moving from 80 to 82 correct answers on 100 tasks is two additional successes; it does not alone establish better performance on the target population. A paired bootstrap resamples matching example indices together to estimate uncertainty in a score difference; SciPy documents this option.[^bootstrap] Choose a resampling unit consistent with the data: turns in one conversation are not automatically independent conversations. State assumptions and the interval method; intervals cannot fix an unrepresentative test set.

Also report important task, language and user-group slices, latency, cost and failure cases. Improvements on one dimension may accompany regressions on another.[^helm]

## Pitfalls

- **Contamination**: test items leak into training data — use held-out, dynamic or private sets
- **Saturation**: benchmarks stop discriminating once models near the ceiling
- **Goodhart's law**: optimising for a benchmark erodes its meaning
- **Prompt sensitivity**: small format changes swing scores; report settings
- **Statistical noise**: report confidence intervals; small test sets mislead
- **Construct validity**: does the benchmark measure what its score is claimed to represent?[^validity]
- **Benchmarks ≠ real-world usefulness**

## Evaluating your own application

1. **Write down what good looks like** for real user tasks
2. **Build development and held-out sets** from realistic inputs, including edge cases, missing evidence and adversarial ones; justify coverage and sample size for the decision
3. **Choose graders**:
    - Exact match / unit tests / programmatic checks where possible
    - **LLM-as-judge** with a rubric — validate against human ratings; watch for position, verbosity and self-preference biases
    - Human review for high-stakes or subjective qualities
4. **Track regressions** on every change (prompt, model, retrieval settings)
5. **Monitor in production** with sampled reviews and user feedback

## Methods from psychology and measurement science

- **Item response theory** to estimate model ability and item difficulty
- **Reliability and validity** concepts from psychometrics
- **Controlled experiments** and counterbalancing (e.g. swapping answer order to detect position bias)[^judge]
- **Cognitive-science-style probing** to test specific capacities (see [Psychology & AI](../../brain-mind/psychology/index.md))

## Tools

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) provides shared language-model evaluation tasks and configurations; [HELM](https://crfm.stanford.edu/helm/) supports multi-scenario, multi-metric evaluation; [Inspect](https://inspect.aisi.org.uk/) provides composable tasks, scorers, agents and logs.

[^validity]: Raji et al. (2021), listed in References.
[^helm]: Liang et al. (2022), listed in References.
[^splits]: scikit-learn, *Cross-validation: evaluating estimator performance*, listed in References.
[^leakage]: scikit-learn, *Common pitfalls and recommended practices*, listed in References.
[^inspect]: Inspect documentation, listed in References.
[^judge]: Zheng et al. (2023), listed in References.
[^bootstrap]: SciPy, *scipy.stats.bootstrap*, listed in References.

## References

### Research papers

- Raji, I. D. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims based on benchmark performance.
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. https://arxiv.org/abs/2211.09110 — Evaluates language models across scenarios and metrics to expose capability gaps and trade-offs.
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. https://arxiv.org/abs/2306.05685 — Studies model-based judging, human agreement and biases in open-ended assistant evaluation.

### Articles and documentation

- scikit-learn contributors. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — Explains held-out testing, model selection, group splits and time-aware evaluation.
- scikit-learn contributors. *Common pitfalls and recommended practices*. https://scikit-learn.org/stable/common_pitfalls.html — Demonstrates preprocessing leakage and how pipelines restrict fitting to training data.
- SciPy contributors. *scipy.stats.bootstrap*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html — Describes bootstrap confidence intervals and paired resampling for matched observations.
- UK AI Security Institute and Meridian Labs. *Inspect*. https://inspect.aisi.org.uk/ — Documents composable datasets, solvers, scorers, agent evaluations and evaluation logs.
- EleutherAI. *Language Model Evaluation Harness*. https://github.com/EleutherAI/lm-evaluation-harness — Provides reusable language-model evaluation tasks, configuration and execution tooling.
