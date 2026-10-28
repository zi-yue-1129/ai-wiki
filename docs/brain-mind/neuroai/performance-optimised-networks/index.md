---
status: complete
last_reviewed: 2026-10-28
related:
- theory/models/cnn
tags:
- neuroscience
- vision
- neuroai
aliases:
  - Performance-Optimised Networks Predict IT Cortex
  - Yamins 2014
  - 效能最佳化網路預測皮質
---

# Performance-optimised networks predict visual cortex (Yamins et al., 2014)

Deep convolutional networks that are optimised for object recognition predict the responses of neurons in the higher visual cortex of monkeys. The better a model is at recognising objects, the better it tends to predict these responses, which links engineering performance to a biological fit.

This page is part of [NeuroAI](../index.md). It covers one method in detail.

## Overview

Visual cortex is hard to model directly, because many candidate models fit the early stages roughly but differ in the later ones. Yamins et al. asked which family of computational models best accounts for the responses in the ventral visual stream, which runs through areas V4 and inferior temporal (IT) cortex to support object recognition. Their answer depended on optimising the models for the task that the brain is thought to perform.

## Key concepts

- **Ventral visual stream**: the pathway from primary visual cortex through V4 to IT cortex, which carries object information.
- **Task-optimised model**: a network whose weights are trained for a task, such as object categorisation, rather than fitted to the neural data directly.
- **Predictivity**: how well the features of a model, mapped to recorded responses, predict the activity of neurons on new images.
- **Hierarchical model**: a stack of layers in which each layer builds on the one below, so that higher layers have larger receptive fields.

## Problem

Which computational models of the ventral visual stream best predict neural responses in higher visual cortex? Earlier models were built by hand or fitted to neural data, and it was unclear whether good object recognition by itself gives a good fit to the brain.

## Core idea

Optimise deep convolutional networks for object recognition, then test how well their features predict recorded responses in V4 and IT. The paper compares many architectures, and the central result is that performance on object categorisation tracks how well a model predicts IT responses. The best-performing models predict these responses better than earlier, less optimised ones.

## Method

1. Train a family of hierarchical convolutional networks to categorise objects in images.
2. Select the models by their performance on the object-recognition task.
3. Record responses from neurons in V4 and IT of macaque monkeys to a set of images.
4. Map the model's features to the neural responses, and score how well the mapping predicts responses to natural images. The abstract does not specify the mapping method.

## Results

The paper reports that object-recognition performance across the tested models tracks how well they predict IT responses. It also reports that the best-performing models predict these responses better than earlier models that were less optimised for the task. The paper's results come from a fixed set of images and recording sites, and this page does not quote numerical scores, because the figures should be read from the paper itself.

## Limitations

- **Prediction is not mechanism.** A model that predicts a neural population well has not shown that the brain computes its features in the same way.
- **A fixed stimulus set.** The test used a particular set of images and recording sites, so the result may depend on those choices.
- **A limited model family.** The comparison covers convolutional hierarchies, and other architectures may predict the same data differently.

## Connections

- **Convolutional networks**: the models tested are convolutional, as covered in [Convolutional Neural Networks](../../../theory/models/cnn/index.md).
- **Visual perception**: the biological side of object recognition is on [Visual Perception](../../visual-perception/index.md), including the simple-to-complex hierarchy studied by [Hubel & Wiesel](../../neuroscience/receptive-fields-hubel-wiesel/index.md).
- **Parent topic**: [NeuroAI](../index.md). Another method on this topic is [Grid-Like Units in a Navigating Network](../grid-like-units/index.md).

## Applications

- **Model selection for neuroscience**: predictivity on neural data is used to choose among candidate models of the visual system.
- **Engineering insight**: the finding that task performance and brain fit go together is one reason vision models are compared with neural data.

## Open questions

- **Does the link hold beyond IT?** Early and intermediate areas may need different models, and the link to V4 is less clear-cut.
- **Which features matter?** Predictivity does not say which parts of a trained network are responsible for the match.
- **How much does the training data matter?** Models trained on different image sets may predict neural responses differently, and this is under study.

## References

### Seminal papers

- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that deep networks trained for object recognition predict neural responses in higher visual cortex, and that better recognition goes with better prediction.
- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). ImageNet Classification with Deep Convolutional Neural Networks. *Advances in Neural Information Processing Systems 25*. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The convolutional network that made deep models practical for large-scale object recognition.
- Cadieu, C. F., et al. (2014). Deep Neural Networks Rival the Representation of Primate IT Cortex for Core Visual Object Recognition. *PLoS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1003963 — Reports that deep networks trained for object recognition match the representation of IT cortex, a finding made in parallel with the Yamins et al. study.

### Surveys and reviews

- Kriegeskorte, N. (2008). Matching categorical object representations in inferior temporal cortex of man and monkey. *Neuron*. https://doi.org/10.1016/j.neuron.2008.10.043 — Introduces representational similarity analysis, the method used to compare model and brain representations.
- Schrimpf, M., et al. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Shows that next-word-prediction language models predict brain responses in the language network, and that better prediction goes with better brain fit.
