---
status: complete
last_reviewed: 2026-10-28
related:
  - society/safety-alignment
tags:
  - security
  - safety
  - red teaming
aliases:
  - Jailbreaks
  - Red Teaming
  - 越獄
  - 紅隊測試
---

# Jailbreaks and red-teaming

A jailbreak is an input that makes a language model produce output its safety training was meant to prevent. Red-teaming is the systematic search for such failures, carried out by people or by other models before a system is released. The two are closely linked: red-teaming finds jailbreaks, and each jailbreak suggests a new test.

This page is part of [LLM Application Security](index.md). The alignment side of the same problem is covered in [Safety & Alignment](../../society/safety-alignment/index.md).

## Overview

Safety training teaches a model to refuse certain requests. A jailbreak finds a way around that refusal, for example by wrapping the request in a story, by giving instructions in an unusual format, or by adding a string of text that the model treats as a cue to comply. Unlike prompt injection, which hijacks an application, a jailbreak usually aims at harmful output from the model itself.

## Key concepts

- **Jailbreak:** an input crafted to bypass a model's refusal behaviour.
- **Red-teaming:** structured attempts to make a system fail, to find harms before users do.
- **Attack success rate:** the share of attempts that produce the disallowed output.
- **Transfer:** whether an attack that works on one model also works on another.
- **Automated red-teaming:** a model generates the test inputs, and a classifier or a person judges the outputs.

## How it works

Three families of method recur in the literature. Manual jailbreaks are written by people and shared informally, and they change quickly as models are updated. Optimised attacks search for a text suffix that makes a target model comply; Zou et al. (2023) showed that suffixes found on open models can transfer to others, as described on [Universal adversarial suffixes](universal-adversarial-suffixes.md). Model-driven attacks use an attacker model that proposes prompts and refines them using the target's responses; Chao et al. (2023) report jailbreaks of black-box models within twenty queries.

Red-teaming draws on the same ideas. Perez et al. (2022) used language models to generate test questions at scale and then measured the harmful replies they produced. Ganguli et al. (2022) describe human red-teaming of a model at scale, with measures of harm and lessons from the effort.

## Limitations

- **Evidence is incomplete.** A failed attack does not show that a model is safe, only that the attack did not work.
- **Attacks adapt.** A defence tuned to known jailbreaks can be bypassed by a new phrasing.
- **Measurement is hard.** Judging whether an output is harmful requires a rubric, and disagreements between judges are common.
- **Safety training is not a complete explanation.** Wei et al. (2023) analyse how safety training can fail.

## Defences

No single defence covers all jailbreaks. Practical systems combine stronger model training, system-level checks on inputs and outputs (see [Guardrails and output filtering](guardrails.md)), limits on what the model's outputs can do, and regular red-teaming as models and attacks change. The application-level risks of injected instructions are covered in [Indirect prompt injection](indirect-prompt-injection.md).

## Connections

- Model-level training for harmlessness is described on [Safety & Alignment](../../society/safety-alignment/index.md).
- The threats that matter for applications are on [LLM Application Security](index.md).
- Evaluation practice for safety benchmarks is on [Evaluation & Benchmarks](../evaluation/index.md).

## Applications

- Pre-release safety testing of chat and agent systems.
- Regression tests that reuse known jailbreaks after each model update.

## Open questions

- Can red-teaming give a bound on residual risk, or only a count of failures found?
- How should disclosure of new jailbreaks be handled?

## References

### Seminal papers

- Zou, A. et al. (2023). Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv. https://arxiv.org/abs/2307.15043 — Shows that automatically found suffixes can make aligned models comply with harmful requests, and that they transfer across models.
- Chao, P. et al. (2023). Jailbreaking Black Box Large Language Models in Twenty Queries. arXiv. https://arxiv.org/abs/2310.08419 — Uses an attacker model to refine jailbreak prompts against black-box targets within a small number of queries.
- Perez, E. et al. (2022). Red Teaming Language Models with Language Models. arXiv. https://arxiv.org/abs/2202.03286 — Generates red-team test cases with a language model and measures the harmful replies they elicit.
- Ganguli, D. et al. (2022). Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned. arXiv. https://arxiv.org/abs/2209.07858 — Describes human red-teaming at scale, its measures of harm, and lessons for reducing harms.
- Wei, A., Haghtalab, N. & Steinhardt, J. (2023). Jailbroken: How Does LLM Safety Training Fail? arXiv. https://arxiv.org/abs/2307.02483 — Analyses how safety training can fail against jailbreak attacks.
