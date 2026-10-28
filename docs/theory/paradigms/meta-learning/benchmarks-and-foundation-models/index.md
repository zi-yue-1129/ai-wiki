---
related:
- theory/models/llm/index.md
- theory/paradigms/transfer/index.md
tags:
  - meta-learning
  - few-shot learning
  - in-context learning
  - benchmarks
---

# Benchmarks and Foundation Models

This subtopic covers the benchmarks used to measure few-shot learning and the way large pre-trained models have changed the problem. Early work used small handwritten-character and image datasets. Large language models now perform few-shot learning through in-context examples, which raises new questions about what meta-learning should mean.

## Overview

Few-shot benchmarks split classes into base and novel sets, then measure accuracy on novel classes given a few labelled examples. Careful evaluation matters, because differences between methods are often small and depend on the backbone, the training schedule and the test protocol.

## Benchmarks

- **Omniglot**: handwritten characters from many alphabets, used in the first concept-learning studies.
- **miniImageNet and tieredImageNet**: small subsets of ImageNet with disjoint base and novel classes, the standard image benchmarks for episodic training.
- **Cross-domain benchmarks**: test whether methods trained on one domain transfer to very different images, which exposes the limits of episodic training.

## Foundation models

Large language models perform few-shot learning by conditioning on examples in the prompt, without any gradient update. This in-context learning is a form of meta-learning that is learned implicitly from very large pre-training corpora. Strong fixed backbones can also match specialised few-shot methods, which has led to re-evaluating what the meta-learning stage actually contributes.

## Connections

Benchmark results depend on the [supervised learning](../../supervised/index.md) pipeline used for the backbone, and on the [transfer](../../transfer/index.md) methods that fine-tune it. The in-context view links to [large language models](../../../models/llm/index.md).

## Applications

Evaluating medical or industrial classifiers before data collection, testing whether a language model can adapt to new tasks from a few examples, and comparing new meta-learning methods fairly.

## Open questions

Benchmarks saturate and can reward dataset-specific tricks. It is not clear whether episodic training is still needed when backbones are very strong, and in-context learning is poorly understood in theory.

## References

### Seminal papers

- Lake, Salakhutdinov & Tenenbaum (2015), "Human-level concept learning through probabilistic program induction", Science. https://cbmm.mit.edu/publications/human-level-concept-learning-through-probabilistic-program-induction — Introduces the Omniglot concept-learning task and a Bayesian program-induction model.
- Vinyals et al. (2016), "Matching networks for one shot learning", NeurIPS, arXiv:1606.04080 — Introduces the episodic protocol and the miniImageNet one-shot benchmark used in the field.
- Brown et al. (2020), "Language models are few-shot learners", NeurIPS, arXiv:2005.14165 — Shows that a large language model performs few-shot tasks from examples in the prompt, without gradient updates.
- Chen, Liu, Kira, Wang & Huang (2019), "A closer look at few-shot classification", ICLR, arXiv:1904.04232 — Shows that a simple baseline with standard training matches many episodic methods.

### Surveys and textbooks

- Hospedales, Antoniou, Micaelli & Storkey (2021), "Meta-learning in neural networks: a survey", IEEE TPAMI, arXiv:2004.05439 — Survey that reviews the benchmarks and the evaluation practice used in the field.

### Lectures and videos

- Finn, CS 330: Deep Multi-Task and Meta Learning, Stanford University. https://cs330.stanford.edu — Course with lectures on multi-task and meta-learning, including few-shot methods and their evaluation.

### Articles and documentation

No further entries for this page.

## Further reading

- Wang, Yao, Kwok & Ni (2020), "Generalizing from a few examples: a survey on few-shot learning", ACM Computing Surveys. No link checked.
