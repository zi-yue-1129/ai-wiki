---
status: complete
last_reviewed: 2026-10-28
aliases:
  - 錯誤信念測驗
  - False-belief tests
---

# False-Belief Tests on Language Models (Kosinski 2023)

Kosinski asked whether large language models pass false-belief tasks, the standard test of theory of mind in children, and how their performance depends on model size. The paper tested eleven models and reported that performance rises sharply with size and generation. The parent topic is [Psychology & AI](../index.md).

## Problem

Do large language models solve false-belief tasks, and does success depend on model size? Children reliably pass these tasks by around age four, so they serve as a benchmark that is hard to pass by chance.

## Core idea

Each scenario has a character whose belief about an object or location differs from the facts, and the model is asked what the character will think or do. A correct answer requires tracking the character's belief, not the true state of the world. Each task is written in eight scenario variants with 16 prompts in total, and a task counts as solved only if the model answers all 16 correctly.

## Procedure

1. Write a false-belief scenario: a protagonist holds a belief that the world has since contradicted.
2. Ask a question that can only be answered correctly by tracking the protagonist's belief.
3. Repeat across the eight variants, giving 16 prompts per task.
4. Score each model, count a task as solved only when all 16 answers are correct, and compare models of different sizes and generations.

## Results

The abstract reports that eleven models were tested. The smaller and older models solved none of the tasks. GPT-3-davinci-003 and ChatGPT-3.5-turbo each solved about 20%, and ChatGPT-4 solved 75%, a level the author compares with six-year-old children in earlier studies.

## Limitations

- Passing the test does not show that a model has mental states. The author treats the spontaneous emergence of theory of mind as a possibility, not a finding.
- Later studies found the results fragile. Small rewordings can reverse reported successes (Ullman, 2023), and adversarial tests show inconsistent social reasoning (Shapira et al., 2023).
- Sap et al. (2022) report that GPT-3 scores well below human accuracy on related social tasks, so the picture depends on the benchmark.

## Connections

- The chimpanzee test that defined the term is in [Chimpanzee theory-of-mind test](../chimpanzee-theory-of-mind/index.md).
- The debate about whether these models have theory of mind is summarised in the [Theory of mind](../index.md) section of the parent page.

## References

### Seminal papers

- Kosinski, M. (2023). Evaluating Large Language Models in Theory of Mind Tasks. arXiv. https://arxiv.org/abs/2302.02083 — Tests eleven language models on false-belief tasks; ChatGPT-4 solves about 75% of them.
- Ullman, T. (2023). Large Language Models Fail on Trivial Alterations to Theory-of-Mind Tasks. arXiv. https://arxiv.org/abs/2302.08399 — Small changes that keep the same principles reverse reported LLM successes on theory-of-mind tasks.
- Sap, M. et al. (2022). Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs. arXiv. https://arxiv.org/abs/2210.13312 — Finds that GPT-3 scores well below human accuracy on social and theory-of-mind questions.
- Shapira, N. et al. (2023). Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large Language Models. arXiv. https://arxiv.org/abs/2305.14763 — Adversarial tests show that LLM social reasoning is inconsistent and may rely on shallow heuristics.
- Rabinowitz, N. C. et al. (2018). Machine Theory of Mind. arXiv. https://arxiv.org/abs/1802.07740 — ToMnet, a meta-learned network that models other agents and passes a Sally–Anne false-belief test in gridworlds.
