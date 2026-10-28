---
status: complete
last_reviewed: 2026-10-28
tags:
  - class imbalance
  - loss functions
  - long-tailed learning
aliases:
  - class-balanced loss
  - 類別平衡損失
  - 有效樣本數
---

# Class-Balanced Loss

Class-balanced loss reweights each class's contribution to the training loss by how many samples the class has. Cui et al. (2019) make the weight depend on the *effective number* of samples rather than the raw count, because a class's extra samples add less new information as the class grows.

## Problem

In long-tailed data sets, a few head classes have many samples and many tail classes have few. A model trained with plain cross-entropy can reach high accuracy by favouring the head classes, while recall on the tail stays poor. The usual fix, inverse-frequency weighting, can over-weight tail classes when their samples are near-duplicates.

## Core idea

Cui et al. model each class's samples as drawn from a set of small neighbourhoods, so the samples of a class overlap. The expected number of distinct samples is then

$$E_n = \frac{1 - \beta^n}{1 - \beta},$$

where $n$ is the number of samples in the class and $\beta \in [0, 1)$ is a hyperparameter. The class weight is set proportional to $1/E_n$, which gives the class-balanced loss.

## How it works

1. Count the samples $n_c$ in each class $c$.
2. Compute the effective number $E_{n_c}$ with a chosen $\beta$.
3. Set the class weight $w_c \propto 1/E_{n_c}$, normalised so the weights sum to the number of classes.
4. Train with the weighted cross-entropy, or with a focal variant.

As $\beta \to 1$, the effective number approaches the raw count, so the weights approach inverse frequency. For small $\beta$ the weights approach uniform.

## Results

Cui et al. evaluate on artificially long-tailed CIFAR splits and on the real-world iNaturalist 2017 and 2018 datasets, and check the method on ImageNet (ILSVRC 2012) as a set that is not long-tailed. They report that the best $\beta$ depends on the data set, and that data sets with different imbalance factors tend to have different and smaller optimal values. On CIFAR-100, only small values of $\beta$ improve performance, while larger values degrade it. The exact numbers are in the paper's tables.

## Limitations

- **The tuning parameter.** Performance depends on $\beta$. On CIFAR-100 the paper finds that larger values degrade performance.
- **Reweighting from the start.** Reweighting from the first epoch can under-fit tail classes. Cao et al. (2019) address this by deferring the reweighting to a later stage of training.
- **Scope.** The method is for classification. Its extension to regression targets is different, see [logit adjustment](logit-adjustment.md) for a post-hoc alternative.

## Connections

Class-balanced loss is one of several ways to handle imbalance by changing the training objective. Others change the decision rule after training, as in [logit adjustment](logit-adjustment.md). The imbalance question matters for [imitation learning](../../imitation/index.md) too, where rare but important actions can be swamped by common ones. The metrics that expose imbalance are in [evaluation and validation](../evaluation-and-validation/index.md).

## Applications

Long-tailed image recognition, medical imaging with rare findings, and any classification task where common classes dominate the data.

## Open questions

How to choose the effective-number parameter without tuning on the test distribution, and how the weighting interacts with representation learning, which Kang et al. (2020) study by separating the representation from the classifier.

## References

### Seminal papers

- Cui, Y., Jia, M., Lin, T.-Y., Song, Y. & Belongie, S. (2019). *Class-Balanced Loss Based on Effective Number of Samples*. CVPR 2019. https://openaccess.thecvf.com/content_CVPR_2019/html/Cui_Class-Balanced_Loss_Based_on_Effective_Number_of_Samples_CVPR_2019_paper.html — Introduces the effective-number weighting and the class-balanced loss. The arXiv version is [arXiv:1901.05555](https://arxiv.org/abs/1901.05555).
- Cao, K., Wei, C., Gaidon, A., Arechiga, N. & Ma, T. (2019). *Learning Imbalanced Datasets with Label-Distribution-Aware Margin Loss*. NeurIPS 2019. https://proceedings.neurips.cc/paper/2019/hash/621461af90cadfdaf0e8d4cc25129f91-Abstract.html — Shows that reweighting from the start can hurt tail classes, and proposes margins plus deferred reweighting.

### Articles and preprints

- Menon, A. K. et al. (2021). *Long-tail Learning via Logit Adjustment*. ICLR 2021. https://arxiv.org/abs/2007.07314 — Shows that a post-hoc adjustment of logits by class frequency can be a consistent alternative to reweighting.
- Kang, B. et al. (2020). *Decoupling Representation and Classifier for Long-Tailed Recognition*. ICLR 2020. https://arxiv.org/abs/1910.09217 — Finds that instance-balanced sampling learns better representations and that rebalancing the classifier alone is enough.
- Ren, J. et al. (2022). *Balanced MSE for Imbalanced Visual Regression*. CVPR 2022. https://openaccess.thecvf.com/content/CVPR2022/html/Ren_Balanced_MSE_for_Imbalanced_Visual_Regression_CVPR_2022_paper.html — Extends the balancing idea to regression with a likelihood-based correction.
