---
related:
- theory/paradigms/supervised/index.md
- applications/autonomous-driving
tags:
  - transfer learning
  - multi-task learning
  - shared representations
---

# Multi-task Learning

Multi-task learning trains one model on several related tasks at once, so that the tasks share representations. Shared structure can improve generalisation on each task, especially when some tasks have little labelled data. The difficulty is deciding how much to share and how to balance the tasks against each other.

## Overview

The two basic architectures are hard parameter sharing, where most layers are shared and each task has its own head, and soft parameter sharing, where each task has its own network and the networks are encouraged to stay similar. Training combines the per-task losses, so the weighting of those losses matters a great deal.

## Sharing and balancing

- **Hard sharing**: a shared trunk with task-specific heads. Simple and efficient, but tasks can interfere when they conflict.
- **Soft sharing and learned sharing**: learn how much each task uses from the others, for example with cross-stitch units that mix features between task networks.
- **Loss weighting**: set task weights by hand, by gradient normalisation, or by learned uncertainty, which lets the model choose its own balance.
- **Task grouping**: decide which tasks to learn together, since some tasks help each other and others hurt.

## Connections

Multi-task learning is a form of [supervised learning](../../supervised/index.md) with several outputs. Its shared encoders are close to the representations of [fine-tuning and adaptation](../fine-tuning-and-adaptation/index.md), and it can be combined with [self-supervised](../../self-supervised/index.md) auxiliary tasks.

## Applications

Joint detection and segmentation in autonomous driving, multilingual language models that share one encoder across languages, and clinical models that predict several outcomes from the same records.

## Open questions

Negative transfer between tasks is common, and it is hard to tell in advance which tasks should be combined. Balancing losses remains heuristic, and gains over single-task baselines are sometimes small once the baselines are well tuned.

## References

### Seminal papers

- Caruana (1997), "Multitask learning", Machine Learning. https://www.doi.org/10.1023/A:1007379606734 — Establishes shared representations as a way to improve generalisation across related tasks.
- Misra, Shrivastava, Gupta & Hebert (2016), "Cross-stitch networks for multi-task learning", CVPR, arXiv:1604.03539 — Learns how much each task network shares features with the others, using cross-stitch units.
- Kendall, Gal & Cipolla (2018), "Multi-task learning using uncertainty to weigh losses for scene geometry and semantics", CVPR, arXiv:1705.07115 — Weighs task losses by learned homoscedastic uncertainty, so the balance is set automatically.
- Standley, Zamir, Chen, Guibas, Malik & Savarese (2020), "Which tasks should be learned together in multi-task learning?", ICML, arXiv:1905.07553 — Measures which task pairs help each other and which hurt, to guide task grouping.

### Surveys and textbooks

- Ruder (2017), "An overview of multi-task learning in deep neural networks", arXiv:1706.05098 — Survey of hard and soft parameter sharing in deep networks, with practical guidance.
- Zhang & Yang (2017), "A survey on multi-task learning", arXiv:1707.08114 — Broad survey of multi-task formulations, including relationship learning and task grouping.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Zhang & Yang (2021), "A survey on multi-task learning", IEEE Transactions on Knowledge and Data Engineering. No link checked.
