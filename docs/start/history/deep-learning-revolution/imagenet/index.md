---
status: draft
last_reviewed: 2026-10-28
tags:
  - computer vision
  - benchmarks
  - supervised learning
aliases:
  - ImageNet
  - ILSVRC
  - ImageNet Large Scale Visual Recognition Challenge
  - 大規模視覺辨識挑戰賽
  - 圖像網路
---

# ImageNet and the ILSVRC Benchmark (Deng et al., 2009; Russakovsky et al., 2015)

ImageNet is a large collection of labelled images organised by a noun hierarchy, and the annual ImageNet Large Scale Visual Recognition Challenge (ILSVRC) built on it. Together they gave deep convolutional networks the labelled data and the shared yardstick that made the 2012 breakthrough measurable. This is the data landmark of the [deep learning revolution](../index.md) chapter.

## Overview

Deng et al. (2009) built ImageNet as a large, hierarchically organised resource for object recognition research. Its categories follow the WordNet hierarchy, so every category sits in a tree of more general and more specific concepts. The challenge then turned the collection into a competition. Russakovsky et al. (2015) describe it as a benchmark in object classification and detection, run annually from 2010 and attracting participation from more than fifty institutions.

Because every team was scored on the same held-out images, results became comparable. The 2012 entry based on a deep convolutional network, [AlexNet](../../../../theory/models/cnn/backbones-and-scaling/alexnet/index.md), won the competition, and the years after it are the period this chapter describes.

## Key concepts

- **Synset**: a set of words that share one meaning. ImageNet's categories are synsets of the WordNet noun hierarchy (Deng et al., 2009).
- **Classification and detection**: classification asks which category an image contains; detection also locates each object (Russakovsky et al., 2015).
- **Top-5 error**: the fraction of test images whose correct label is not among the model's five highest-scoring guesses.
- **Held-out test set**: images withheld from training, so that the score measures generalisation rather than memorisation.

## How it works

Building the dataset involved three steps:

1. Choose categories from the WordNet hierarchy.
2. Collect candidate images for each category from the web.
3. Have human annotators confirm which candidates show the category.

The third step is the expensive one, and Russakovsky et al. (2015) discuss the difficulty of collecting large-scale ground truth annotation.

Each challenge round then ran the same protocol: organisers released labelled training images, withheld test images, and scored each entry's predictions. For a single image $x_i$ with true label $y_i$ and predicted top five labels $\hat{S}_i$, the top-5 error is

$$
\text{top-5 error} = \frac{1}{N}\sum_{i=1}^{N} \mathbf{1}\left[\, y_i \notin \hat{S}_i \,\right].
$$

## Results

Russakovsky et al. (2015) describe the advances in object recognition that the benchmark made possible, and compare computer vision accuracy with human accuracy. The 2012 deep convolutional entry changed the competition, and the [AlexNet](../../../../theory/models/cnn/backbones-and-scaling/alexnet/index.md) page covers its figures.

## Limitations

- **Annotation.** Accurate labels at this scale are hard to collect, and some labels are wrong or ambiguous (Russakovsky et al., 2015).
- **Dataset bias.** A dataset reflects the choices made in collecting it. Torralba and Efros (2011) show how hard it is for classifiers trained on one image dataset to generalise to others.
- **Overfitting to the test set.** After years of reuse, the test sets may be fitted too closely. Recht et al. (2019) build new test sets to check whether classifiers generalise to fresh ImageNet-style data, and they raise this concern directly.
- **Narrow target.** Accuracy on the benchmark does not measure robustness or the other abilities that later models were judged on.

## Open questions

- What does a benchmark score measure once models are trained on much larger and less curated data?
- When a benchmark is saturated, what should replace it, and who should maintain it?
- Do high ImageNet scores reflect the same visual cues that people use? The [Geirhos et al. (2019)](../../../../brain-mind/visual-perception/geirhos-2019/index.md) page discusses texture bias in ImageNet-trained networks.

## Connections

The benchmark connects the field's data to its methods. The networks trained on ImageNet became the backbones of later vision systems (see [convolutional backbones](../../../../theory/models/cnn/backbones-and-scaling/index.md)). They also became tools for neuroscience. Yamins et al. (2014) showed that hierarchical models optimised for object recognition predict neural responses in higher visual cortex, a link discussed in [performance-optimised networks](../../../../brain-mind/neuroai/performance-optimised-networks/index.md). For the earlier route to deep models, see the [deep belief networks](../deep-belief-networks/index.md) page.

## References

### Seminal papers

- Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K. & Fei-Fei, L. (2009). ImageNet: A large-scale hierarchical image database. *2009 IEEE Conference on Computer Vision and Pattern Recognition*. https://doi.org/10.1109/CVPR.2009.5206848 — Introduces ImageNet, a large image database organised by the WordNet hierarchy.
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. *Advances in Neural Information Processing Systems 25*. https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The deep convolutional network that won the 2012 challenge and started the deep-learning era in vision.
- Russakovsky, O., Deng, J., Su, H., Krause, J., Satheesh, S., Ma, S. et al. (2015). ImageNet Large Scale Visual Recognition Challenge. *International Journal of Computer Vision*. https://doi.org/10.1007/s11263-015-0816-y — Describes the creation of the benchmark, the advances it made possible, and lessons from its first years.

### Surveys and textbooks

- Sejnowski, T. J. (2018). *The Deep Learning Revolution*. MIT Press. https://doi.org/10.7551/mitpress/11474.001.0001 — A history of the deep-learning revolution by a neuroscientist who took part in it.

### Articles and documentation

- Torralba, A. & Efros, A. A. (2011). Unbiased look at dataset bias. *CVPR 2011*. https://doi.org/10.1109/CVPR.2011.5995347 — Examines how image datasets are biased and why classifiers trained on one dataset transfer poorly to others.
- Recht, B., Roelofs, R., Schmidt, L. & Shankar, V. (2019). Do ImageNet classifiers generalize to ImageNet? arXiv. https://arxiv.org/abs/1902.10811 — Builds new ImageNet test sets to measure overfitting to repeatedly used benchmark data.
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that hierarchical models optimised for object recognition predict neural responses in higher visual cortex.
