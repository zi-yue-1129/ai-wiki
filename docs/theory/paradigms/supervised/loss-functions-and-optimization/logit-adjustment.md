---
status: draft
last_reviewed: 2026-10-28
tags:
  - class imbalance
  - loss functions
  - long-tailed learning
aliases:
  - logit adjustment
  - 邏輯調整
  - 長尾學習
---

# Logit Adjustment

Logit adjustment handles class imbalance by shifting the model's output scores by a term that depends on the class prior. It can be applied after training, which leaves the learned model unchanged, or built into the training loss. Menon et al. (2021) show it is a consistent correction for balanced error, where reweighting the loss is not.

## Problem

A classifier trained on long-tailed data learns scores that favour the head classes, because those classes dominate the training signal. The classical remedy, reweighting the loss by class frequency, changes the training objective, and the paper argues that reweighting has limited effect when the training data can be fitted perfectly. What is needed is a correction that targets the decision rule.

## Core idea

Menon et al. add an offset $\log \pi_y$ to each class's logit, where $\pi_y$ is the class prior. Subtracting the log-prior from the logits before choosing the largest score makes the decision rule behave as if the classes were balanced. The method changes the margin between rare and dominant labels rather than the learned features.

## How it works

1. Estimate the class priors $\pi_y$ from the training labels.
2. Post-hoc: at test time, predict $\arg\max_y \left( f_y(x) - \tau \log \pi_y \right)$, where $\tau$ is a scalar tuned on validation data.
3. In-training: use a loss that includes the log-prior offset, so the learned logits already include the adjustment.

The post-hoc version needs no retraining and only one scalar per class in the prior.

## Results

Menon et al. evaluate the method on long-tailed benchmarks, including CIFAR and iNaturalist splits, measuring balanced error. The numbers depend on the setting and are reported in the paper; check them there before use.

## Limitations

- **Calibration.** The correction assumes that the scores are calibrated log-probabilities. Scores from a regression or ranking objective do not satisfy this, so the offset does not apply directly.
- **Scalar tuning.** The temperature-like scalar $\tau$ must be tuned on held-out data that reflects the target balance.
- **Priors must be known.** The priors come from the training set. If the test distribution differs, the offset has to be changed.

## Connections

Logit adjustment is the post-hoc counterpart to [class-balanced loss](class-balanced-loss.md), which changes the training objective. Both target long-tailed classification. The decision threshold it shifts is also the subject of cost-sensitive classification, where asymmetric error costs are handled the same way. For how imbalance shows up in metrics, see [evaluation and validation](../evaluation-and-validation/index.md).

## Applications

Long-tailed image recognition, species classification from camera traps, and any task where a rare class is costly to miss.

## Open questions

How to extend the correction to outputs that are not calibrated probabilities, and whether a single offset per class remains sufficient when the imbalance changes across the input space.

## References

### Seminal papers

- Menon, A. K., Jayasumana, S., Rawat, A. S., Jain, H., Veit, A. & Kumar, S. (2021). *Long-tail Learning via Logit Adjustment*. ICLR 2021. https://arxiv.org/abs/2007.07314 — Shows that a consistent correction for balanced error is a logit offset by the class prior, applied post-hoc or in the loss.
- Cui, Y. et al. (2019). *Class-Balanced Loss Based on Effective Number of Samples*. CVPR 2019. https://openaccess.thecvf.com/content_CVPR_2019/html/Cui_Class-Balanced_Loss_Based_on_Effective_Number_of_Samples_CVPR_2019_paper.html — The class-reweighting baseline that logit adjustment is compared with.

### Articles and preprints

- Cao, K. et al. (2019). *Learning Imbalanced Datasets with Label-Distribution-Aware Margin Loss*. NeurIPS 2019. https://proceedings.neurips.cc/paper/2019/hash/621461af90cadfdaf0e8d4cc25129f91-Abstract.html — Uses margins that depend on class frequency, a related approach that also changes the decision boundary.
- Kang, B. et al. (2020). *Decoupling Representation and Classifier for Long-Tailed Recognition*. ICLR 2020. https://arxiv.org/abs/1910.09217 — Separates representation learning from classifier learning, and shows that classifier-side rebalancing is effective.
- Ren, J. et al. (2022). *Balanced MSE for Imbalanced Visual Regression*. CVPR 2022. https://openaccess.thecvf.com/content/CVPR2022/html/Ren_Balanced_MSE_for_Imbalanced_Visual_Regression_CVPR_2022_paper.html — Corrects an MSE loss for the training label distribution, the regression analogue of the balancing idea.
