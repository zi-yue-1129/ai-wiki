---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- data-free distillation
aliases:
  - Data-free distillation
  - Zero-shot knowledge distillation
  - 無資料蒸餾
  - 零樣本知識蒸餾
---

# Data-Free Knowledge Distillation

Data-free distillation compresses a teacher without access to its training data. The student is trained on synthetic inputs generated from the teacher, which makes distillation possible when the data are private, too large to share, or no longer available.

## Overview

The standard distillation recipe assumes that the student can be trained on real inputs. In many practical cases this is not so: a model may be released without its training set, or the data may be protected. Data-free methods synthesise inputs that the teacher finds representative, usually by optimising random noise so that the teacher's internal statistics match what it would have seen on real data. The student is then distilled on these synthetic samples in the usual way.

## Key concepts

- **Synthetic samples.** Inputs generated from the teacher, not drawn from a dataset.
- **Teacher statistics.** Quantities such as batch-normalisation running means and variances, which summarise the training distribution and can guide synthesis.
- **Surrogate data.** Samples that approximate the training data for the purpose of distillation, without reproducing any real example.
- **Coverage.** Whether the synthetic samples span the regions of input space where the student must perform well.

## Comparison of methods

| Method | How the inputs are obtained | Domain | Page |
| --- | --- | --- | --- |
| Zero-shot KD | Optimised from noise to make the teacher confident and diverse | Image classification | [Zero-shot KD](zero-shot-kd/index.md) |
| Sequence-level KD | Teacher beam-search outputs for the source sentences, which are still real | Translation | [Sequence-level KD](../llm-distillation/sequence-level/index.md) |

Zero-shot KD is fully data-free, since it uses no real inputs at all. Sequence-level distillation is only partly data-free, because it still needs source sentences, and it is listed here because it removes the need for the target side of the dataset.

## Trade-offs

- **Privacy and access versus cost.** Data-free methods remove the need for data, but synthesis adds compute, and the surrogate data may miss important regions of the input space.
- **Fidelity.** Synthetic data may reproduce the teacher's errors, and the student cannot exceed the teacher's knowledge.
- **Licensing.** Using a model's outputs to train another model may be restricted by its terms of use, which vary by provider.

## More variants and open issues

- **Open issue:** how to synthesise data for language models, where discrete tokens are harder to optimise than continuous images.
- **Open issue:** how much of the teacher's data-dependent behaviour can be recovered from synthetic samples.
- **Variant:** [LLM distillation](../llm-distillation/index.md), where the teacher generates the training data for the student.

## Connections

Data-free distillation touches privacy, which is discussed in the [ethics](../../../../society/ethics/index.md) and [governance](../../../../society/governance/index.md) pages, and the training pipelines in [training and fine-tuning](../../../../engineering/training/index.md). Synthesising inputs from a trained network resembles the way the brain replays patterns during rest, a parallel discussed in [memory and learning](../../../../brain-mind/memory-learning/index.md).

## References

### Seminal papers

- Nayak, G. K., Mopuri, K. R., Shaj, V., Babu, R. V., Chakraborty, A. (2019). *Zero-Shot Knowledge Distillation in Deep Networks*. arXiv:1905.08114. https://arxiv.org/abs/1905.08114 — Distils a network from synthetic samples, reaching performance competitive with real training data.
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — Trains on the teacher's own outputs, giving a student about 10 times faster than its teacher.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The standard distillation objective, which assumes a training set that data-free methods replace.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation settings, including those without data.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Distils BERT from teacher outputs and hidden states, the standard reference for language-model distillation.
