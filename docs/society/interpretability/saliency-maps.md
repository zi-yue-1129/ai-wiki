---
status: complete
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

A saliency map shows how strongly each input pixel affects a network's score for one class. It is computed from the gradient of that score with respect to the input, so one backward pass is enough. Simonyan, Vedaldi and Zisserman (2014) introduced the technique for image classifiers.

## Problem

A convolutional network labels an image, but its decision is hard to inspect. Which pixels does the decision depend on, and is the network attending to the object or to its surroundings? The problem is to produce a map that answers this for one image and one class.

## Core idea

Take the gradient of the class score with respect to the input image. Pixels where a small change would move the score most are the most salient. The paper describes two visualisation techniques based on this gradient. The class saliency map is specific to a given image and class.

## Equation

For a class $c$ with score $S_c(I)$ and an image $I$, the map takes the magnitude of the gradient at each pixel:

$$
M_c(I)_{ij} = \left|\frac{\partial S_c}{\partial I_{ij}}\right|.
$$

## Results

The paper presents saliency maps as visualisations of individual images, computed from one backward pass per image. It also evaluates a saliency-based weakly supervised object-localisation pipeline on ILSVRC 2013, which measures localisation performance. That is separate from explanation faithfulness: whether the maps reflect the model's computation is a different question, which later work tests directly (see Limitations).

## Limitations

- **Sanity.** Adebayo et al. (2018) report that some existing saliency methods are independent of both the model and the data-generating process, so a visually plausible map is not evidence that it reflects what the model learned. Their tests also show that Guided BackProp keeps much of its appearance when higher-layer weights are randomised.
- **Local slope.** A gradient gives the score's slope at the input, not the total effect of a pixel. Integrated gradients was proposed to address this (Sundararajan et al., 2017).
- **Visual reading.** Maps are often judged by eye, which makes it easy to read in what one expects to see.

## Connections

Saliency maps are the simplest gradient-based member of [feature attribution](feature-attribution.md). [Integrated gradients](integrated-gradients.md) accumulates gradients along a path to fix the local-slope problem, and DeepLIFT (Shrikumar et al., 2017) replaces gradients with differences from a reference activation. Gradient methods need access to the model's internals, which separates them from the model-agnostic [LIME](lime.md) and from Kernel SHAP, which needs only predictions. For the convolutional architectures on which these maps were first shown, see the [interpretability overview](index.md).

## Applications

- Checking whether an image classifier looks at the object or at a background cue, such as a watermark.
- Localising evidence in medical images for review by a clinician, with the caveats above.
- Comparing two models on the same images to see whether their evidence differs.

## Open questions

- Which gradient-based maps pass sanity checks across architectures and tasks?
- How should saliency be evaluated quantitatively, without relying on visual inspection?
- How far does a gradient at the input reflect the model's computation rather than its local shape?

## References

### Seminal papers

- Simonyan, K., Vedaldi, A. & Zisserman, A. (2014). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. arXiv:1312.6034. https://arxiv.org/abs/1312.6034 — Introduces gradient-based visualisations, including the class saliency map.
- Sundararajan, M., Taly, A. & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *Proceedings of ICML 2017*. https://arxiv.org/abs/1703.01365 — Proposes integrated gradients as a fix for the limits of plain gradients.
- Shrikumar, A., Greenside, P. & Kundaje, A. (2017). Learning Important Features Through Propagating Activation Differences. *Proceedings of ICML 2017*. https://arxiv.org/abs/1704.02685 — Proposes DeepLIFT, which propagates activation differences from a reference rather than raw gradients.

### Surveys and textbooks

- Adebayo, J. et al. (2018). Sanity Checks for Saliency Maps. *Advances in Neural Information Processing Systems 31*. https://arxiv.org/abs/1810.03292 — Tests saliency methods and finds that some are independent of the model and the data.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1705.07874 — Places DeepLIFT and several other attribution methods in one additive framework.

## Further learning

- Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*, 3rd edition. [Free online book](https://christophm.github.io/interpretable-ml-book/), with worked examples of gradient-based attribution.
