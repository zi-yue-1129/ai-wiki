---
status: draft
last_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - attribution
aliases:
  - 顯著性圖
  - 梯度顯著性
  - Saliency maps
  - Gradient-based saliency
---

# Saliency maps

!!! info "Part of Feature attribution"
    This method page belongs to [Feature attribution](feature-attribution.md). It explains the method in detail; the overview compares it with the other methods.

A saliency map shows how strongly each input pixel affects a network's score for one class. It is computed from the gradient of that score with respect to the input, so one backward pass is enough. Simonyan, Vedaldi and Zisserman (2014) introduced the technique for image classifiers.

## Problem

A convolutional network labels an image, but its decision is hard to inspect. Which pixels does the decision depend on, and is the network attending to the object or to its surroundings? The problem is to produce a map that answers this for one image and one class.

## Core idea

Take the gradient of the class score with respect to the input image. Pixels where a small change would move the score most are the most salient. The paper describes two visualisation techniques based on this gradient; the class saliency map is specific to a given image and class.

## Equation

For a class \(c\) with score \(S_c(I)\) and an image \(I\), the map takes the magnitude of the gradient at each pixel:

\[
M_c(I)_{ij} = \left|\frac{\partial S_c}{\partial I_{ij}}\right|.
\]

## Results

The paper presents saliency maps as visualisations of individual images rather than as a benchmark. Whether the maps are faithful to the model is a separate question, which later work tests directly (see Limitations).

## Limitations

- **Sanity.** Adebayo et al. (2018) report that some existing saliency methods are independent of both the model and the data-generating process, so a visually plausible map is not evidence that it reflects what the model learned.
- **Local slope.** A gradient gives the score's slope at the input, not the total effect of a pixel. Integrated gradients was proposed to address this (Sundararajan et al., 2017).
- **Visual reading.** Maps are often judged by eye, which makes it easy to read in what one expects to see.

## References

### Seminal papers

- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. *ICLR 2014 Workshop*. https://arxiv.org/abs/1312.6034 — Introduces gradient-based visualisations, including the class saliency map.
- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — Proposes integrated gradients as a fix for the limits of plain gradients.
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). Learning Important Features Through Propagating Activation Differences. *Proceedings of ICML 2017*. https://arxiv.org/abs/1704.02685 — Proposes DeepLIFT, which propagates activation differences from a reference rather than raw gradients.

### Surveys and textbooks

- Adebayo, J. et al. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — Tests saliency methods and finds that some are independent of the model and the data.
- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. https://christophm.github.io/interpretable-ml-book/ — Free online book covering gradient-based and other attribution methods with worked examples.
