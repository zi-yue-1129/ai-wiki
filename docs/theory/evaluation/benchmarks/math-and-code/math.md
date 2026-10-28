---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# MATH

MATH is a dataset of 12,500 competition mathematics problems, each with a full step-by-step solution. The solutions can be used to teach models to write derivations, and the paper also contributes an auxiliary pre-training dataset (Hendrycks et al., 2021).

## Task and data

Each problem asks for a short final answer, such as a number or an expression. The problems come from mathematics competitions and cover several subjects at several difficulty levels. The step-by-step solutions make it possible to supervise intermediate reasoning (Hendrycks et al., 2021).

## Protocol and metric

The metric is **final-answer accuracy**. The final answer is compared with the reference after normalisation, so equivalent forms that a checker does not recognise are scored as wrong. The protocol should state the normalisation rules and whether solutions are sampled or greedy.

## What it shows

Even large Transformers reached only modest accuracy, and the authors argue that increasing model size and training budget alone would be impractical for strong mathematical reasoning if the observed trends continue (Hendrycks et al., 2021). Lightman et al. (2023) later trained reward models with step-level labels and evaluated them on a subset of MATH.

## Limitations

- **Answer checking.** Equivalent answers in different forms can be marked wrong, and a correct answer with an unusual form is hard to verify automatically.
- **Contamination.** Competition problems and their solutions are widely published.
- **Distance from research mathematics.** Competition problems have short, known solutions. Open research problems have no reference answer.

## Related

- [GSM8K](gsm8k.md) is an easier benchmark of grade-school word problems.
- [Math and code family overview](index.md) compares the benchmarks in this area.

## References

### Seminal papers

- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — Introduces the 12,500 problems, their solutions and the auxiliary pre-training data.
- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv. https://arxiv.org/abs/2110.14168 — The easier benchmark that motivated the verifier approach to math reasoning.

### Articles and documentation

- Lightman, H. et al. (2023). *Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — Trains process-supervised reward models and evaluates them on a subset of MATH.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Intermediate reasoning steps that improve performance on math benchmarks.

### Additional sources

- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — Introduces the pass@k metric for code generation, a related way of scoring generated solutions.
