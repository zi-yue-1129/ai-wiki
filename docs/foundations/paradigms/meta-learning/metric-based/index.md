---
related:
- foundations/paradigms/supervised/instance-based-and-probabilistic/index.md
tags:
  - meta-learning
  - few-shot learning
  - metric learning
---

# Metric-based Few-shot Learning

Metric-based few-shot learning classifies a new example by comparing it with labelled support examples in a learned embedding space. Training uses many small episodes, each made of a few labelled examples per class and some queries, so that the embedding learns to separate new classes without retraining the classifier.

## Overview

A network embeds all inputs. A class is represented by its support examples, for instance by their average embedding, and a query is assigned to the nearest class under a distance or a learned similarity. Because the comparison happens at test time, new classes need no new weights.

## Main methods

- **Matching networks**: classify by attention over the support set, with a soft nearest-neighbour rule.
- **Prototypical networks**: represent each class by the mean of its embeddings and use squared Euclidean distance.
- **Relation networks**: learn the similarity function itself with a small network, rather than fixing it as a distance.
- **Graph-based few-shot learning**: treat the support and query examples as a graph and propagate labels through it.

## Connections

Metric learning is closely related to the [instance-based methods](../../supervised/instance-based-and-probabilistic/index.md) of supervised learning, such as nearest neighbours, but the embedding is learned across episodes. The baseline comparisons in the benchmark subtopic show that a well-trained standard classifier often matches these methods.

## Applications

Recognising new species or product categories from a few photographs, character recognition for new scripts, and medical image classification where rare conditions have only a few labelled cases.

## Open questions

Metric methods assume that the embedding separates classes well after training on a few base classes, which often fails when the new classes are far from the base classes. Performance also depends on the episode design used during training.

## References

### Seminal papers

- Vinyals, Blundell, Lillicrap, Kavukcuoglu & Wierstra (2016), "Matching networks for one shot learning", NeurIPS, arXiv:1606.04080 — Introduces attention over a labelled support set, trained on episodes that mimic test conditions.
- Snell, Swersky & Zemel (2017), "Prototypical networks for few-shot learning", NeurIPS, arXiv:1703.05175 — Represents each class by the mean of its embeddings, a simple method that works well in practice.
- Sung et al. (2018), "Learning to compare: relation network for few-shot learning", CVPR, arXiv:1711.06025 — Learns the similarity function itself with a small network applied to pairs of embeddings.
- Garcia & Bruna (2018), "Few-shot learning with graph neural networks", ICLR, arXiv:1711.04043 — Propagates labels through a graph built over support and query examples.

### Surveys and textbooks

- Hospedales, Antoniou, Micaelli & Storkey (2021), "Meta-learning in neural networks: a survey", IEEE TPAMI, arXiv:2004.05439 — Survey that compares metric-based methods with the other meta-learning families.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Koch, Zemel & Salakhutdinov (2015), "Siamese neural networks for one-shot image recognition", ICML deep learning workshop. No link checked.
