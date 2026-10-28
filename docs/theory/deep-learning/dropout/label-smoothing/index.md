---
status: draft
last_reviewed: 2026-10-28
tags:
  - regularisation
  - loss functions
  - deep learning
aliases:
  - Label Smoothing
  - 標籤平滑
---

# Label Smoothing

Label smoothing replaces the one-hot target of each training example with a softened distribution that gives a small share of probability to every class. It is a deterministic change to the training signal rather than a random one. It sits on the parent [dropout and stochastic regularisation](../index.md) page because, like dropout, it stops the network from becoming overconfident on its training data.

## Overview

A classifier trained with cross-entropy and one-hot targets is asked to put all of its probability on the correct class. The loss keeps decreasing as the logit of the correct class grows relative to the others, so the network is pushed towards very large and very confident outputs. Szegedy et al. (2015) introduced label smoothing as a regulariser for an image classifier. Instead of the target 1 for the correct class and 0 for the rest, they used a target that gives the correct class slightly less than 1 and spreads the remainder evenly over all classes.

The idea is now used across tasks. Müller, Kornblith and Hinton (2019) list image classification, language translation and speech recognition among the areas where label smoothing is used, and they study what it does to the learned representations.

## Key concepts

- **One-hot target.** A target vector with a 1 for the correct class and 0 elsewhere.
- **Smoothing parameter.** The amount \(\varepsilon\) of probability moved from the correct class to the uniform distribution.
- **Calibration.** The agreement between a model's stated confidence and how often it is correct. Overconfident networks are poorly calibrated. See the [probabilistic methods](../../../paradigms/probabilistic/index.md) overview for the wider context.
- **Teacher and student.** In knowledge distillation, a teacher network produces soft outputs that a student network is trained to match.

## How it works

For \(K\) classes and a training example with correct class \(y\), the smoothed target is

\[
y^{\mathrm{LS}}_k = (1-\varepsilon)\,\mathbf{1}[k=y] + \frac{\varepsilon}{K}.
\]

Training uses the usual cross-entropy loss against \(y^{\mathrm{LS}}\). Because cross-entropy is linear in the target, the loss equals \((1-\varepsilon)\) times the ordinary loss on the correct class, plus \(\varepsilon\) times the average of \(-\log p_k\) over all classes. The second term penalises the network for placing all of its probability on one class.

The procedure is:

1. Choose a smoothing parameter \(\varepsilon\) between 0 and 1.
2. Replace each one-hot target with the smoothed target.
3. Train as usual with cross-entropy against the smoothed targets.
4. At inference, make predictions as usual. The network is not told about smoothing and the predictions are no longer pushed to extreme confidence.

## Results

Müller et al. (2019) report, from their abstract, that soft targets of this kind improve generalisation and learning speed in multi-class networks. They also report that label smoothing improves calibration, which in turn can improve beam search in translation. Their key finding is a limitation: when a teacher network is trained with label smoothing, distilling it into a student is much less effective. The abstract attributes this to label smoothing changing the representations learned by the penultimate layer. The results in Szegedy et al. (2015) are reported in that paper, and this page does not repeat its figures.

## Limitations

- **Information loss.** Müller et al. visualise how label smoothing makes the representations of training examples from the same class form tight clusters. This removes information about how classes resemble one another, which distillation needs.
- **Uniform treatment of wrong classes.** Smoothing spreads probability evenly over all wrong classes, so a cat is treated as equally wrong when the label is dog and when it is a truck. Semantic similarity is ignored.
- **One more hyperparameter.** The value of \(\varepsilon\) matters, and its best value depends on the task and model.
- **Benefit varies.** Improvements in generalisation and calibration are task-dependent, and the gains do not transfer uniformly to every setting.

## Open questions

- **Why does clustering help one thing and hurt another?** Müller et al. offer a visual account of why label smoothing helps generalisation and calibration but harms distillation. A full theory is missing.
- **Can smoothing respect class structure?** Replacing the uniform distribution with one that reflects similarity between classes is a natural extension, and its effects are an open question.
- **How does it combine with mixup?** [Mixup and CutMix](../mixup/index.md) also produce soft targets, so the two methods overlap, and their joint effect is not fully mapped.

## Connections

Label smoothing is closely related to [mixup](../mixup/index.md), which also trains on soft targets. Its link to distillation connects it to the [knowledge distillation](../../../model-compression/knowledge-distillation/index.md) page, since both use soft outputs as training targets. Calibration is a probabilistic property, so the topic connects to the [probabilistic methods](../../../paradigms/probabilistic/index.md) overview. For the brain, the link is indirect: the question of how much confidence a system should express is common to perception and to machine learning, but this page does not claim a biological mechanism. See the [parent topic](../index.md).

## Applications

- **Image classification.** Szegedy et al. introduced the method for an image classifier, and it has since been used in many classifiers.
- **Machine translation.** Müller et al. list language translation among its uses. Vaswani et al. (2017) train the Transformer with label smoothing among their regularisers.
- **Speech recognition.** Müller et al. list speech recognition among the areas where label smoothing is used.

## References

### Seminal papers

- Szegedy, C. et al. (2015). *Rethinking the Inception Architecture for Computer Vision*. arXiv. https://arxiv.org/abs/1512.00567 — The paper itself: redesigns an image classifier for efficiency and regularisation, and introduces label smoothing for its classifier.
- Müller, R., Kornblith, S. & Hinton, G. (2019). *When Does Label Smoothing Help?* arXiv. https://arxiv.org/abs/1906.02629 — Shows that label smoothing improves generalisation and calibration, but makes distillation from a smoothed teacher less effective.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv. https://arxiv.org/abs/1503.02531 — Shows that the soft outputs of an ensemble can be distilled into a single network, the setting in which label smoothing's side effect matters.
- Zhang, H. et al. (2017). *mixup: Beyond Empirical Risk Minimization*. arXiv. https://arxiv.org/abs/1710.09412 — Trains on mixed examples and labels, another way of producing soft targets.

### Articles and documentation

- Vaswani, A. et al. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, which is trained with label smoothing among its regularisers.
