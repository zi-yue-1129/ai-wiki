---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
  - generalisation
last_reviewed: 2026-11-01
aliases:
  - ImageNetV2
  - ImageNet V2
  - Do ImageNet Classifiers Generalize to ImageNet?
  - ImageNet 第二版測試集
  - ImageNet 再收集測試集
---

# ImageNetV2

ImageNetV2 is a new test set for ImageNet, collected by repeating the original data-collection process. Recht et al. (2019) built it to ask whether the accuracy that image classifiers reach on the standard ImageNet validation set carries over to images collected in the same way. Their answer was that it mostly does, but every model scores lower on the new set (Recht et al., 2019).

## Task and data

The task is the same as [ImageNet](imagenet.md): assign one of 1,000 labels to a photograph. The new test set has 10,000 images, with ten images per class. The authors also built a new CIFAR-10 test set of 2,000 images (Recht et al., 2019).

Recht et al. follow the original dataset creation process. They draw ten images per class from a large candidate pool, and the choice of images is governed by how often each candidate was selected in the original process. Three sampling strategies produce three test sets, which differ in how closely they follow that original selection frequency (Recht et al., 2019).

## Protocol and metric

The metric is top-1 accuracy, as in the original benchmark. What changes is the test set. The authors estimated, for each candidate image, how often it had been selected in the original process, and used that selection frequency to choose which images to keep. The three sets are:

- **MatchedFrequency.** Images are sampled so that the selection frequency of each class matches the original distribution. The average selection frequency is 0.73, and the average top-1 change is −11.8%.
- **Threshold 0.7.** Only images with a selection frequency of at least 0.7 are kept. The average frequency is 0.85, and the average top-1 change is −3.2%.
- **TopImages.** The ten most frequently selected images per class are kept. The average frequency is 0.93, and the average top-1 change is +2.1%.

The main comparison uses the MatchedFrequency set, which is the closest to the original validation set (Recht et al., 2019).

## What it shows

The models in the study scored lower on the new set than on the original one. The best model, a PNASNet, dropped from 82.9% to 72.2% top-1, and its rank fell from first to third. Representative models dropped by similar amounts. ResNet-152 fell from 78.3% to 67.0%, and AlexNet from 56.5% to 44.0% (Recht et al., 2019).

Two observations matter more than the size of the drop. First, the authors find that the drop is not caused by adaptivity, meaning repeated use of the old test set to select models. Second, accuracy gains on the original set carried over to the new set. The authors suggest that the remaining drop reflects a limit on generalisation to slightly harder images (Recht et al., 2019).

The TopImages result is informative as well. Keeping the images with the highest selection frequency made the set easier, and accuracy rose slightly. The difficulty of a test set therefore depends on which images are sampled, not only on the classes.

## Connections

- [ImageNet](imagenet.md) is the benchmark that ImageNetV2 replicates. The two should be compared on the same metric and the same training data.
- [Benchmarks overview](../index.md) lists the other vision and language benchmarks, and the test-set fitting problem appears there too.
- Robustness to synthetic corruptions is a different test. Hendrycks and Dietterich (2019) introduce ImageNet-C for it and report negligible changes in relative corruption robustness from AlexNet to ResNet.
- Taori et al. (2020) study natural distribution shifts across 204 ImageNet models and find that robustness to synthetic shifts transfers poorly to natural ones.
- [Accuracy](../../metrics/classification/accuracy.md) is the metric used on all of these test sets.

## Applications

ImageNetV2 can serve as a second check on a classifier's ImageNet score. A model that scores well on the original validation set but poorly on the new one may have fitted the collection process rather than the visual concept.

## Open questions

- How much of the gap between the original and new test sets reflects image difficulty, and how much reflects other differences in how the images were chosen. The authors' explanation of harder images is a hypothesis, and it is not measured directly.
- Whether the correlation between in-distribution and out-of-distribution accuracy holds across all new test sets. Miller et al. (2021) find a strong correlation across many shifts, but they also report cases where it is weaker.
- How to build fresh test sets that remain representative after many models have been compared on them.

## References

### Seminal papers

- Recht, B., Roelofs, R., Schmidt, L. & Shankar, V. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Re-collects test sets for CIFAR-10 and ImageNet and measures the accuracy drop of many models.
- Deng, J. et al. (2009). *ImageNet: A large-scale hierarchical image database*. CVPR, pp. 248–255. https://doi.org/10.1109/CVPR.2009.5206848 — The original database that ImageNetV2 replicates.
- Russakovsky, O. et al. (2014). *ImageNet Large Scale Visual Recognition Challenge*. arXiv (2014). https://arxiv.org/abs/1409.0575 — Describes the challenge built on the database and the lessons from its first years.

### Surveys and benchmarks

- Hendrycks, D. & Dietterich, T. (2019). *Benchmarking Neural Network Robustness to Common Corruptions and Perturbations*. arXiv. https://arxiv.org/abs/1903.12261 — ImageNet-C, a benchmark of synthetic corruptions for measuring robustness.
- Taori, R. et al. (2020). *Measuring Robustness to Natural Distribution Shifts in Image Classification*. arXiv (2020). https://arxiv.org/abs/2007.00644 — Evaluates 204 ImageNet models on 213 natural test conditions and finds little transfer from synthetic robustness.
- Miller, J. et al. (2021). *Accuracy on the Line: On the Strong Correlation Between Out-of-Distribution and In-Distribution Generalization*. arXiv (2021). https://arxiv.org/abs/2107.04649 — Shows a strong correlation between in-distribution and out-of-distribution accuracy across many models and shifts, including ImageNet variants.
