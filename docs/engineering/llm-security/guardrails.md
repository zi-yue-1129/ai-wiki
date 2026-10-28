---
status: draft
last_reviewed: 2026-10-28
related:
  - society/safety-alignment
tags:
  - security
  - safety
  - filtering
aliases:
  - Guardrails
  - Output Filtering
  - Content Moderation
  - 護欄
  - 輸出過濾
---

# Guardrails and output filtering

Guardrails are checks placed around a language model. They screen what goes into the model and what comes out of it, classify content against a policy, or constrain the conversation to a set of allowed paths. They are a system-level control, complementary to the safety training inside the model.

This page is part of [LLM Application Security](index.md).

## Overview

Training a model to refuse harmful requests changes the model's behaviour, but the behaviour is not guaranteed. An application that needs stronger control adds independent checks outside the model. The check can sit on the input, on the output, or on the actions the model may take. Because a guard can be wrong in either direction, its design is a trade-off between blocking harm and blocking legitimate use.

## Key concepts

- **Input guard:** a check on what the user or retrieved content sends to the model.
- **Output filter:** a check on what the model returns before it reaches the user or a tool.
- **Classifier guard:** a model trained to label content against a risk taxonomy.
- **Programmable rails:** rules that define allowed topics, dialogue paths or response styles.
- **Structural control:** a limit that does not depend on judging text, such as an allow-list of tools or a confirmation step.

## How it works

A typical pipeline screens the input, passes accepted inputs to the model, screens the output, and returns a safe reply or a refusal. Classifier guards are themselves language models. Inan et al. (2023) describe Llama Guard, an LLM-based safeguard for both prompts and responses, built around a safety risk taxonomy. Rebedea et al. (2023) describe NeMo Guardrails, a toolkit in which developers write programmable rails that control a conversational system's topics, dialogue paths and outputs.

Structural controls complement classifiers. An agent that cannot send email without a confirmation step is protected even if a classifier misses an instruction to send it.

## Limitations

- **Adaptive attackers.** Guards are tested against known attacks, and new phrasings can pass them. See [Jailbreaks and red-teaming](jailbreaks-and-red-teaming.md).
- **Errors in both directions.** A strict filter blocks legitimate content, and a lenient one misses harm.
- **Indirect content.** A guard that checks the user's message does not see instructions hidden in a retrieved document. Greshake et al. (2023) describe this case for integrated applications.
- **Latency and cost.** Each check adds a call, and a classifier guard is itself a model to run and maintain.
- **Guards are not training.** A guard filters behaviour from outside the model. The model's own training for harmlessness, described in [Constitutional AI](../../society/safety-alignment/index.md), is a separate layer.

## Connections

- The threat model that guards address is on [LLM Application Security](index.md).
- Refusals and their failure are covered on [Jailbreaks and red-teaming](jailbreaks-and-red-teaming.md).
- Model-level training for harmlessness is on [Safety & Alignment](../../society/safety-alignment/index.md).

## Applications

- Customer-facing chat systems that must stay on topic and avoid unsafe advice.
- Moderation of user-generated content on platforms that use language models.
- Enterprise assistants that restrict which data and actions a model can reach.

## Open questions

- How should a guard's false-positive rate be set for a given application?
- Can classifier guards be made robust to adaptive attacks without retraining each time?

## References

### Seminal papers

- Inan, H. et al. (2023). Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations. arXiv. https://arxiv.org/abs/2312.06674 — A classifier safeguard for prompts and responses, built around a safety risk taxonomy.
- Rebedea, T. et al. (2023). NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails. arXiv. https://arxiv.org/abs/2310.10501 — A toolkit for adding programmable rails that control the topics, dialogue paths and outputs of an LLM application.
- Bai, Y. et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv. https://arxiv.org/abs/2212.08073 — Trains a harmless assistant through self-improvement guided by written principles, a model-level alternative to external guards.
- Greshake, K. et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. arXiv. https://arxiv.org/abs/2302.12173 — Shows how instructions in retrieved content can bypass input checks on the user's message.
- Wei, A., Haghtalab, N. & Steinhardt, J. (2023). Jailbroken: How Does LLM Safety Training Fail? arXiv. https://arxiv.org/abs/2307.02483 — Analyses why safety training can fail, which bears on how much external guards must do.
