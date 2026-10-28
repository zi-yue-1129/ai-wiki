---
related:
- foundations/paradigms/self-supervised/index.md
- engineering/training/index.md
tags:
  - transfer learning
  - fine-tuning
  - parameter-efficient fine-tuning
---

# Fine-tuning and Adaptation

Fine-tuning starts from a model trained on a large source task and continues training on a smaller target task. It is the most common form of transfer in practice. The main decisions are which layers to update, how large the learning rate should be for each layer, and whether to update all parameters or only a small set.

## Overview

Early layers of a deep network tend to learn generic features, while later layers become specific to the source task. Fine-tuning therefore usually keeps the early layers, adapts the later ones and adds a new output head. How much to change depends on how similar the tasks are and how much labelled target data is available.

## Strategies

- **Linear probe**: freeze the backbone and train only a new head. Cheap, and a good test of how useful the representation is.
- **Full fine-tuning**: update every parameter with a small learning rate. Works well with enough data.
- **Gradual unfreezing and discriminative learning rates**: unfreeze layers from the top down and use smaller learning rates for earlier layers, which reduces catastrophic forgetting of the source task.
- **Parameter-efficient fine-tuning (PEFT)**: train small added modules such as adapters, or low-rank updates such as LoRA, while the pre-trained weights stay frozen. This makes it practical to serve many tasks from one large model.

## Connections

Fine-tuning builds on representations learned by [self-supervised learning](../../self-supervised/index.md), where pre-training uses no labels. Training costs and infrastructure are covered in [training and fine-tuning](../../../../engineering/training/index.md). Adapting a pre-trained model to a shifted input distribution is the subject of [domain adaptation](../domain-adaptation/index.md).

## Applications

Image classifiers fine-tuned from ImageNet models for medical imaging, language models adapted to a company's support tickets, and per-customer adapters that share a single base model.

## Open questions

Fine-tuning can erase useful source knowledge, and it is hard to predict in advance which layers or hyperparameters will transfer best. Parameter-efficient methods are cheap but can underperform full fine-tuning on distant tasks.

## References

### Seminal papers

- Yosinski, Clune, Bengio & Lipson (2014), "How transferable are features in deep neural networks?", NeurIPS, arXiv:1411.1792 — Measures how generic and task-specific features in each layer transfer between tasks.
- Howard & Ruder (2018), "Universal language model fine-tuning for text classification", ACL, arXiv:1801.06146 — ULMFiT, which introduces discriminative learning rates and gradual unfreezing for language models.
- Houlsby et al. (2019), "Parameter-efficient transfer learning for NLP", ICML, arXiv:1902.00751 — Adapter modules that match full fine-tuning while training only a small fraction of the parameters.
- Hu et al. (2022), "LoRA: low-rank adaptation of large language models", ICLR, arXiv:2106.09685 — Low-rank updates to frozen weights, now a standard parameter-efficient method.

### Surveys and textbooks

- Pan & Yang (2010), "A survey on transfer learning", IEEE Transactions on Knowledge and Data Engineering. https://www.cse.ust.hk/~qyang/Docs/2009/tkde_transfer_learning.pdf — Survey that defines transfer settings and the taxonomy used across the field.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Ruder (2019), "Neural transfer learning for natural language processing", PhD thesis, NUI Galway. No link checked.
