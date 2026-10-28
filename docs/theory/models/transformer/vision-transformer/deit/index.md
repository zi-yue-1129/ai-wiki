---
status: draft
last_reviewed: 2026-10-28
tags:
  - computer vision
  - knowledge distillation
  - transfer learning
aliases:
  - DeiT
  - Data-efficient image Transformer
  - 資料高效影像 Transformer
  - Distillation token
---

# DeiT: data-efficient image transformers (Touvron et al., 2020)

DeiT trains a [ViT](../vit/index.md) on ImageNet-1K alone, using a strong augmentation recipe and a distillation token that learns from a convolutional teacher. It belongs to the [Vision Transformer](../index.md) topic, and it answers the data question that the original ViT left open.

## Overview

The original ViT needed JFT-300M, a dataset of about 300 million images, to beat CNNs. DeiT asks whether the same architecture can be trained competitively on ImageNet-1K. The authors start from the ViT design, keep it unchanged, and change only the training recipe and the way the model is supervised. The paper reports that a model of 86M parameters reaches 83.1% top-1 accuracy at 384 × 384 with no external data, trained on a single machine in under three days (Touvron et al., 2020).

## Key concepts

- **Data-efficient training**: the recipe uses AdamW, cosine decay, a lower weight decay than ViT, and strong augmentation. Dropout is removed.
- **Strong augmentation**: the recipe combines RandAugment, mixing-based augmentation, random erasing and stochastic depth. The ablation finds almost every technique helps, and dropout is the exception.
- **Distillation token**: a second learned token, added beside the class token, whose output is trained to match a teacher's prediction rather than the true label.
- **Hard-label distillation**: the teacher's top-1 prediction is used as a target, instead of its full softmax.

## How it works

The architecture is that of ViT with one extra token. The patches and both tokens pass through self-attention together, and the class and distillation tokens produce separate outputs. Distillation uses the teacher's hard decision y_t = argmax_c Z_t(c) as a second target. The loss is

$$
\mathcal{L}^{\text{hardDistill}}_{\text{global}} = \tfrac{1}{2}\,\mathcal{L}_{\text{CE}}(\psi(Z_s), y) + \tfrac{1}{2}\,\mathcal{L}_{\text{CE}}(\psi(Z_s), y_t)
$$

where Z_s and Z_t are the student and teacher logits and ψ is the softmax. The paper compares this with the usual soft distillation, which matches the full softmax with a temperature. Hard labels work better for transformers. At test time the two heads can be combined by late fusion.

The default teacher is a RegNetY-16GF model, also trained on ImageNet-1K with the same recipe, that reaches 82.9% top-1. The paper finds that a convolutional teacher helps more than a transformer teacher, and it suggests that the inductive bias of the teacher passes to the student. The authors cite Abnar et al. (2020) for this explanation.

## Results

The paper's Table 5 reports ImageNet-1K top-1 accuracy at two resolutions. The values below are as reported.

| Model | Resolution 224 | Resolution 384 |
|---|---|---|
| DeiT-B (no distillation) | 81.8 | 83.1 |
| DeiT-B with distillation | 83.4 | 84.5 |
| DeiT-B with distillation, 1000 epochs | 84.2 | 85.2 |

On the distillation comparison in Table 3, hard-label distillation of DeiT-B reaches 83.0% at 224, against 81.8% for soft distillation. The paper reports that the distilled model outperforms ViT-B pre-trained on JFT-300M at 384 (85.2% against 84.15%). Transfer results are on par with competitive CNNs, with DeiT-B reaching 99.1% on CIFAR-10 and 98.4% on Oxford Flowers.

## Limitations

- **Dependence on a teacher.** The best numbers need a strong convolutional teacher, so the recipe does not remove the role of CNNs.
- **Sensitive hyperparameters.** The authors report that transformers are sensitive to learning rate and weight decay, and the recipe depends on several interacting ingredients, including repeated augmentation.
- **Training cost.** The recipe still needs days on GPU hardware, and the best result uses 1000 epochs.
- **Efficiency claim.** The paper reports DeiT-B as slightly below EfficientNet on the speed-accuracy trade-off, and only the distilled model is said to exceed it.

## Open questions

- Why does a convolutional teacher help a transformer student so much? The explanations are about inductive bias, and direct evidence is limited.
- Does the ImageNet-only recipe carry over to dense prediction tasks, where [Swin](../swin/index.md) reports higher detection accuracy than DeiT-S?
- How far do the augmentation gains interact with the choice of optimizer, a question the ablation only partly answers?

## References

### Seminal papers

- Touvron, H., et al. (2020). *Training data-efficient image transformers & distillation through attention*. arXiv; ICML 2021. https://arxiv.org/abs/2012.12877 — The original paper, introducing the ImageNet-only recipe and the distillation token.
- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv; ICLR 2021. https://arxiv.org/abs/2010.11929 — The ViT architecture that DeiT keeps and whose data requirement it addresses.
- Hinton, G., et al. (2015). *Distilling the Knowledge in a Neural Network*. arXiv. https://arxiv.org/abs/1503.02531 — Introduces soft-target knowledge distillation, the baseline that DeiT compares against.
- Abnar, S., et al. (2020). *Transferring Inductive Biases through Knowledge Distillation*. arXiv. https://arxiv.org/abs/2006.00555 — Studies how knowledge distillation transfers a teacher's inductive biases to a student.

### Articles and documentation

- Cubuk, E. D., et al. (2019). *RandAugment: Practical automated data augmentation with a reduced search space*. arXiv. https://arxiv.org/abs/1909.13719 — The augmentation policy that DeiT adopts after its ablation.
- Zhang, H., et al. (2017). *mixup: Beyond Empirical Risk Minimization*. arXiv. https://arxiv.org/abs/1710.09412 — Trains on convex combinations of images and labels, one of the augmentations in the recipe.
- Yun, S., et al. (2019). *CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features*. arXiv. https://arxiv.org/abs/1905.04899 — Cuts and pastes image regions with mixed labels, another augmentation in the recipe.
- Huang, G., et al. (2016). *Deep Networks with Stochastic Depth*. arXiv. https://arxiv.org/abs/1603.09382 — Randomly drops residual blocks during training, used in the recipe for deep transformers.
