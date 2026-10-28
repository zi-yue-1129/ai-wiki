---
status: complete
last_reviewed: 2026-10-28
related:
  - society/privacy
tags:
  - security
  - model theft
  - APIs
aliases:
  - Model Extraction
  - Model Stealing
  - Model Theft
  - 模型萃取
  - 模型竊取
---

# Model extraction and theft

Model extraction is an attack in which someone who can only query a model reconstructs a copy of its behaviour, or part of its internals, from the answers. The copy can compete with the original, reveal confidential design choices, or serve as a base for other attacks. The risk is highest for models that are deployed behind a public API.

This page is part of [LLM Application Security](index.md). It concerns the model itself. The privacy risk of recovering training data is covered in [Training-data extraction](../../society/privacy/training-data-extraction.md).

## Overview

A model exposed through an API reveals its function with every answer. An attacker who sends enough queries and records the outputs can train a second model to imitate the first. The method is closely related to knowledge distillation, which is a legitimate way to compress a model, and the difference lies in whether the teacher's owner has agreed to it.

## Key concepts

- **Victim model:** the deployed model whose behaviour is being copied.
- **Query access:** the attacker can send inputs and see outputs, but not the weights.
- **Surrogate model:** the copy trained on the victim's answers.
- **Functionality stealing:** copying what the model does, without copying its weights.
- **Parameter recovery:** recovering part of the model's internal structure from its outputs.

## How it works

The basic procedure has three steps. The attacker chooses inputs, often from a related public dataset. The attacker records the victim's outputs, such as labels or probabilities. The attacker trains a surrogate on the input-output pairs. The surrogate can then approximate the victim on new inputs.

Tramèr et al. (2016) describe extraction of machine learning models through prediction APIs. Orekondy et al. (2019) show that an adversary with black-box access can steal the functionality of image classifiers using natural images that the adversary chooses. Krishna et al. (2020) study extraction of BERT-based APIs, where an adversary with only query access rebuilds a local copy. Carlini et al. (2024) show a different kind of attack: they recover the embedding projection layer of production language models, up to symmetries, with typical API access, and report a cost below twenty US dollars for their attack. Hinton et al. (2015) introduced distillation, the training of a smaller model on a larger model's outputs, which underlies much of the same mechanism.

## Limitations

- **Imperfect copies.** A surrogate usually approximates the victim on common inputs and fails on rare ones.
- **Defences trade off with utility.** Rate limits, output rounding and output perturbation reduce extraction, but they also reduce the value of the API.
- **Evidence is mostly from smaller settings.** Many extraction results come from classifiers or specific model families, and the cost for frontier models changes as their size and access change.

## Defences

Common measures include rate limits and anomaly detection on query patterns, reducing the detail of the outputs, watermarking outputs so that copies can be traced (see [Watermarking](watermarking.md)), and contractual terms that forbid training on outputs. No measure is complete, and the choice depends on how much the output needs to reveal.

## Connections

- The privacy side of model outputs, including recovery of training data, is on [Training-data extraction](../../society/privacy/training-data-extraction.md).
- Membership inference, which asks whether a record was in the training data, is on [Membership inference](../../society/privacy/membership-inference.md).
- The threats to applications built on models are on [LLM Application Security](index.md).

## Applications

- Auditing a deployed API for leakage of its behaviour under different query budgets.
- Tracing outputs that have been copied, using watermarks.

## Open questions

- How much of a frontier model's behaviour can be copied with a given query budget?
- Which defences keep an API useful while raising the cost of extraction?

## References

### Seminal papers

- Tramèr, F. et al. (2016). Stealing Machine Learning Models via Prediction APIs. arXiv. https://arxiv.org/abs/1609.02943 — Shows that models served through prediction APIs can be extracted from their answers.
- Orekondy, T., Schiele, B. & Fritz, M. (2019). Knockoff Nets: Stealing Functionality of Black-Box Models. CVPR. https://arxiv.org/abs/1812.02766 — Steals the functionality of black-box image classifiers with natural images chosen by the attacker.
- Krishna, K. et al. (2020). Thieves on Sesame Street! Model Extraction of BERT-based APIs. ICLR. https://arxiv.org/abs/1910.12366 — Reconstructs a local copy of BERT-based APIs using query access alone.
- Carlini, N. et al. (2024). Stealing Part of a Production Language Model. ICML. https://arxiv.org/abs/2403.06634 — Recovers the embedding projection layer of production language models for a small cost.
- Hinton, G., Vinyals, O. & Dean, J. (2015). Distilling the Knowledge in a Neural Network. arXiv. https://arxiv.org/abs/1503.02531 — Introduces distillation, training a small model on a larger model's outputs.
