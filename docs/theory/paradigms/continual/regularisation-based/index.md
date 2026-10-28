---
related:
- theory/paradigms/transfer/fine-tuning-and-adaptation/index.md
tags:
  - continual learning
  - catastrophic forgetting
  - regularisation
---

# Regularisation-based Continual Learning

Regularisation-based continual learning limits how far the parameters move when a new task is learned. The aim is to keep the weights that mattered for earlier tasks close to their old values, without storing any old data. The penalty is added to the loss on the new task, so the model trades off new learning against forgetting.

## Overview

Not all weights matter equally. Methods estimate the importance of each parameter for past tasks and penalise changes to important ones more heavily. Some methods estimate importance from the Fisher information, others accumulate it online during training, and others distil the old model's outputs on new data.

## Main methods

- **Elastic weight consolidation (EWC)**: adds a quadratic penalty weighted by an estimate of the Fisher information of each parameter.
- **Synaptic intelligence (SI)**: accumulates each parameter's contribution to the loss change along the training path, which gives importance without a second pass over old data.
- **Learning without forgetting (LwF)**: keeps the old model's outputs on new inputs as a distillation target, so no old data is needed.

## Limits

These methods work well for small sequences of tasks but tend to degrade as the number of tasks grows. The penalty also limits plasticity, so new tasks are learned less well. Results depend strongly on the scenario, for example whether the task identity is known at test time.

## Connections

The quadratic penalty has the same form as a Bayesian prior centred on the old parameters, which links to [meta-learning theory](../../meta-learning/meta-learning-theory/index.md). Distillation is a standard tool from [supervised learning](../../supervised/index.md). Starting from a pre-trained model, as in [fine-tuning](../../transfer/fine-tuning-and-adaptation/index.md), is a common way to reduce forgetting.

## Applications

Updating a recommendation or spam model without retraining from scratch, adding new classes to an image classifier, and adapting a language model to new domains while keeping general skills.

## Open questions

Regularisation alone does not prevent forgetting over long sequences. The importance estimates are approximate, and their quality is hard to check. It is also unclear how well these penalties scale to very large models.

## References

### Seminal papers

- Kirkpatrick et al. (2017), "Overcoming catastrophic forgetting in neural networks", PNAS, [arXiv:1612.00796](https://arxiv.org/abs/1612.00796) — EWC, which protects parameters important to earlier tasks with a Fisher-weighted penalty.
- Zenke, Poole & Ganguli (2017), "Continual learning through synaptic intelligence", ICML, [arXiv:1703.04200](https://arxiv.org/abs/1703.04200) — SI, which estimates parameter importance online during training.
- Li & Hoiem (2016), "Learning without forgetting", ECCV, [arXiv:1606.09282](https://arxiv.org/abs/1606.09282) — LwF, which distils the old model's outputs to keep earlier behaviour without old data.

### Surveys and textbooks

- De Lange et al. (2021), "A continual learning survey: defying forgetting in classification tasks", IEEE TPAMI, [arXiv:1909.08383](https://arxiv.org/abs/1909.08383) — Survey and comparison of regularisation, replay and architecture methods.
- Parisi, Kemker, Part, Kanan & Wermter (2019), "Continual lifelong learning with neural networks: a review", Neural Networks, [arXiv:1802.07569](https://arxiv.org/abs/1802.07569) — Review of continual learning methods and their links to biological learning.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Aljundi et al. (2018), "Memory aware synapses: learning what (not) to forget", ECCV. https://arxiv.org/abs/1711.09601 — Estimates how sensitive the output is to each weight and penalises changes to the sensitive ones.
