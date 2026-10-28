---
status: draft
last_reviewed: 2026-10-28
related:
  - society/privacy
tags:
  - security
  - training data
  - backdoors
aliases:
  - Data Poisoning
  - Backdoor Attacks
  - 資料投毒
  - 後門攻擊
---

# Data poisoning and backdoor attacks

Data poisoning inserts malicious examples into a model's training data so that the model behaves as the attacker wants at test time. A backdoor is a poisoning attack in which the behaviour is triggered only by a specific input pattern, so the model looks normal otherwise. Because web-scraped data is used at scale, the attack surface is large and hard to audit.

This page is part of [LLM Application Security](index.md).

## Overview

Training data for modern models is collected from many sources, and most of it is never inspected one example at a time. An attacker who can publish content that will be scraped can therefore influence what a model learns. The consequence may be a classifier that accepts a particular phrase, a code model that suggests insecure patterns, or a model that behaves normally until a trigger appears.

## Key concepts

- **Poisoning:** adding or changing training examples to change the model's behaviour.
- **Backdoor:** a hidden behaviour that is activated by a trigger in the input.
- **Clean-label attack:** a poisoned example whose label looks correct to a human reviewer.
- **Targeted versus untargeted:** whether the attack aims at one input or at overall performance.
- **Web-scale poisoning:** attacks that place content where it will be collected by a dataset crawler.

## How it works

Trigger-based backdoors were shown first in image models. Gu et al. (2017) showed how a model trained on data with a trigger pattern, such as a small patch, can be backdoored, and described the risk of outsourced training. Chen et al. (2017) applied targeted backdoor attacks through data poisoning to face recognition, a security-critical setting. Shafahi et al. (2018) introduced clean-label poisoning, in which the poisoned examples keep their correct labels and still shift the model's prediction on one target input.

For language models, Wallace et al. (2021) study concealed poisoning, in which small changes to the training data let an adversary control predictions when a trigger phrase is present, while the changes stay hard to notice. Carlini et al. (2023) show that poisoning web-scale training datasets is practical, and that content can be placed where crawlers collect it for a set of popular datasets.

## Limitations

- **Hard to detect.** A backdoored model can pass ordinary tests, because the trigger is rare in normal inputs.
- **Depends on data share.** The effect depends on how much of the data the attacker controls and how the training is run.
- **Evidence varies by setting.** Many results come from images or from controlled text tasks, and transfer to large language models is not uniform across attacks.

## Defences

Defences include controlling data provenance, deduplicating and filtering training corpora, detecting outlier examples, testing models with varied triggers, and auditing models after training. None of these is complete, so data provenance and a clear record of training sources are the first line of defence. The privacy side of training data is covered in [Training-data extraction](../../society/privacy/training-data-extraction.md).

## Connections

- Membership and extraction risks concern what a model reveals about its training data; see [Membership inference](../../society/privacy/membership-inference.md).
- Copyright and training data, including memorisation, are on [Copyright and AI](../../society/copyright/index.md).
- The threats to applications built on models are on [LLM Application Security](index.md).

## Applications

- Auditing a classifier or code assistant for triggers before deployment.
- Choosing sources for a training corpus with provenance checks.

## Open questions

- Can poisoning be detected in a trained model without knowing the trigger?
- How much clean data is needed to dilute a poisoned subset?

## References

### Seminal papers

- Gu, T., Dolan-Gavitt, B. & Garg, S. (2017). BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain. arXiv. https://arxiv.org/abs/1708.06733 — Shows that a model trained with a trigger pattern in its data can be backdoored, and raises the risk of outsourced training.
- Chen, X. et al. (2017). Targeted Backdoor Attacks on Deep Learning Systems Using Data Poisoning. arXiv. https://arxiv.org/abs/1712.05526 — Applies targeted backdoor poisoning to security-critical systems such as face recognition.
- Shafahi, A. et al. (2018). Poison Frogs! Targeted Clean-Label Poisoning Attacks on Neural Networks. arXiv. https://arxiv.org/abs/1804.00792 — Introduces clean-label poisoning, in which poisoned examples keep their correct labels.
- Wallace, E. et al. (2021). Concealed Data Poisoning Attacks on NLP Models. NAACL. https://arxiv.org/abs/2010.12563 — Shows concealed poisoning of language models, where a trigger phrase controls the prediction.
- Carlini, N. et al. (2023). Poisoning Web-Scale Training Datasets is Practical. arXiv. https://arxiv.org/abs/2302.10149 — Shows that web-scale datasets can be poisoned in practice, by placing content that crawlers collect.
