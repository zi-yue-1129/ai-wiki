---
status: complete
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- response-based distillation
aliases:
  - Hinton distillation
  - Distilling the knowledge in a neural network
  - 欣頓蒸餾
---

# Hinton Distillation

Hinton, Vinyals and Dean's 2015 paper is the origin of modern knowledge distillation. It trains a small model on the softened outputs of a large teacher, so that the student learns the relative probabilities of wrong answers as well as the correct label. Their recipe is the standard objective that the other [response-based](../index.md) methods build on.

## Problem

Ensembles of networks are the most accurate models, but they are too expensive to deploy. A single model that captures the ensemble's knowledge is needed, and it has to be cheap enough to run in production.

## Core idea

Train the small model on the teacher's softened outputs. A temperature \(T\) spreads the teacher's probabilities, so the near-miss classes become visible to the student. Those near-miss classes carry information about how the classes relate, for example that a picture of a 7 is more like a 1 than a 0 is. The student is also trained on the true labels, so the soft targets act as an extra signal rather than a replacement.

## Equation or algorithm

The combined loss is

\[
\mathcal{L} = (1-\alpha)\, \mathrm{CE}(y, \sigma(z_s)) + \alpha\, T^2\, \mathrm{KL}\!\left(\sigma(z_t/T)\,\Vert\,\sigma(z_s/T)\right)
\]

where \(z_s\) and \(z_t\) are the student and teacher logits, \(\sigma\) is the softmax, \(T\) is the temperature and \(\alpha\) weights the two terms. The factor \(T^2\) keeps the gradient sizes comparable across temperatures.

The paper also gives a useful analysis. When the temperature is high relative to the logit magnitudes, the gradient of the soft-target term with respect to each student logit \(z_i\) is approximately

\[
\frac{\partial \mathcal{L}}{\partial z_i} \approx \frac{1}{N T^2}\,(z_i - v_i)
\]

where \(v_i\) are the teacher logits and \(N\) is the number of classes. Under the paper's zero-mean assumption on the logits, distillation at high temperature is therefore equivalent to matching the student's logits to the teacher's. The paper also proposes a specialist ensemble: one generalist model plus many specialists, each trained on a subset of confusable classes. Unlike a mixture of experts, the specialists can be trained quickly and in parallel.

## Results

On MNIST the paper reports the following test errors:

- An 800-unit baseline without regularisation: 146 errors.
- The same 800-unit architecture trained on the large teacher's soft targets at temperature 20: 74 errors.
- The large, heavily regularised teacher network itself: 67 errors.

The abstract also reports a significant improvement to a heavily used commercial acoustic model when the ensemble's knowledge is distilled into one network. The figures for that experiment are in the full paper.

## Limitations

The method needs the teacher's outputs on the training inputs, which is expensive for large teachers. The temperature is a hyperparameter that has to be searched, and the experiments are small by today's standards: the results above are on MNIST, with one commercial speech system as the other application.

## Open issues and related variants

- **Temperature choice.** The best temperature depends on the task and is usually found by search. The paper's gradient analysis holds only in the high-temperature limit.
- **Feature targets.** Hinton's method matches outputs only. [FitNets](../../feature-based/fitnets/index.md) adds intermediate hints, and [attention transfer](../../feature-based/attention-transfer/index.md) moves knowledge through intermediate attention maps.
- **Language models.** [DistilBERT](../distilbert/index.md) applies the same objective during language-model pretraining.

## Connections

The objective is the basis of the distillation used across [training](../../../../../engineering/training/index.md) and deployment. The idea that a student learns from a teacher's graded beliefs has an analogy in how learners absorb the nuances of a teacher's answers; see [cognitive science](../../../../../brain-mind/cognitive-science/index.md).

## References

### Seminal papers

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The temperature-softened distillation objective, the high-temperature logit-matching analysis, the MNIST results and the specialist ensemble.
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Adds intermediate hint targets to output distillation; a deep student with about ten times fewer parameters surpasses a larger teacher on CIFAR-10.
- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Applies the soft-target objective during BERT pretraining; about 40% smaller and 60% faster while keeping about 97% of BERT's language understanding.

### Surveys and textbooks

- Gou, J., Yu, B., Maybank, S. J., Tao, D. (2021). *Knowledge Distillation: A Survey*. arXiv:2006.05525. https://arxiv.org/abs/2006.05525 — Survey of distillation methods; the arXiv page lists the published version at https://doi.org/10.1007/s11263-021-01453-z. Surveys output-based distillation as the starting point of the field.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — Finds that a student's performance drops when its teacher is much larger, and proposes an intermediate teacher assistant.
