---
related:
- foundations/paradigms/continual/index.md
tags:
  - meta-learning
  - memory-augmented networks
  - hypernetworks
---

# Memory- and Model-based Meta-learning

Memory- and model-based meta-learning encodes the adaptation procedure inside the model itself. Instead of running gradient steps at test time, the model reads a support set into an external memory, into attention weights or into generated parameters, and produces a prediction in one forward pass.

## Overview

These methods are often called black-box meta-learners. The learned network acts as the learning algorithm, so adaptation is a forward computation. This makes them fast at test time, but the learned algorithm can be harder to interpret and may not generalise to tasks unlike those seen during meta-training.

## Main approaches

- **Memory-augmented networks**: use an external memory with read and write operations, so that the model can store task information and retrieve it when a related example appears.
- **Attentive meta-learners**: combine temporal convolution and attention over the sequence of examples, which lets the model learn a learning procedure.
- **Hypernetworks**: a small network generates the weights of a larger one, which allows task-specific parameters to be produced from a task description or support set.
- **Fast weights and meta networks**: a slow network produces fast weights that are updated from each example, so that the model adapts within the forward pass.

## Connections

The black-box view is a different route to the same goal as [optimisation-based meta-learning](../optimisation-based/index.md). Memory and fast-weight ideas are closely related to continual learning, where a system must store and reuse knowledge over time, see [continual learning](../../continual/index.md).

## Applications

Few-shot classification, personalised language and recommendation models that read a short user history, and control policies that infer task parameters from recent experience.

## Open questions

The learned learning algorithms are hard to analyse, and they can fail on tasks that differ from those in meta-training. Memory size and the cost of attention limit how many examples a model can use at once.

## References

### Seminal papers

- Santoro, Bartunov, Botvinick, Wierstra & Lillicrap (2016), "Meta-learning with memory-augmented neural networks", ICML. https://proceedings.mlr.press/v48/santoro16.html — Uses an external memory with learned read and write operations for one-shot learning.
- Mishra, Rohaninejad, Chen & Abbeel (2018), "A simple neural attentive meta-learner", ICLR, arXiv:1707.03141 — Combines temporal convolution and attention to learn a general-purpose learning procedure.
- Munkhdalai & Yu (2017), "Meta networks", ICML, arXiv:1703.00837 — Uses fast weights generated from each example, so that the model adapts within a forward pass.
- Ha, Dai & Le (2017), "HyperNetworks", ICLR, arXiv:1609.09106 — A network that generates the weights of another network, a general tool for task-specific parameters.

### Surveys and textbooks

- Hospedales, Antoniou, Micaelli & Storkey (2021), "Meta-learning in neural networks: a survey", IEEE TPAMI, arXiv:2004.05439 — Survey that describes memory-based and black-box approaches alongside gradient-based ones.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Graves, Wayne & Danihelka (2014), "Neural Turing machines", arXiv:1410.5401. No link checked.
