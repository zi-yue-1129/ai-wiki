---
status: complete
last_reviewed: 2026-10-28
---

# AlexNet (Krizhevsky, Sutskever & Hinton, 2012)

A large deep convolutional network trained on GPUs, using non-saturating (ReLU) neurons and dropout regularisation. It set a new state of the art on ImageNet classification, and it is often cited as a starting point for the modern deep-learning era in computer vision.

## Overview

The paper reports that its network was considerably better than the previous state of the art on the LSVRC-2010 benchmark. It showed that a deep convolutional network, trained on a large labelled dataset with GPUs, could classify ImageNet far more accurately than the systems it was compared against. The paper is short, but its choices, ReLU units, dropout, GPU training and data augmentation, were picked up by most later vision models.

## Key concepts

- **Convolutional layer**: a layer that applies learned filters across the image, sharing weights over positions.
- **Non-saturating neuron (ReLU)**: an activation, max(0, x), whose gradient does not vanish for large positive inputs, so it trains faster than saturating units such as tanh.
- **Dropout**: during training, each hidden unit is set to zero with probability 0.5, which discourages co-adaptation of units.
- **Top-1 and top-5 error**: the fraction of test images whose correct label is not the top prediction, or not among the top five.

## Problem

Classify the 1.3 million high-resolution ImageNet training images into 1,000 classes, where earlier systems fell well short.

## Core idea

Use a large deep convolutional network trained on GPUs. Non-saturating neurons speed up training, and dropout in the fully connected layers reduces overfitting.

## Architecture

The network has eight learned layers: five convolutional and three fully connected. The last fully connected layer is a 1,000-way softmax. The network has about 60 million parameters and 500,000 neurons, according to the abstract.

## Key methods

AlexNet has two named components of its own. Each is compared here with the alternatives the paper replaced.

- **ReLU non-linearity**: replaces tanh or sigmoid units. The paper reports that deep convolutional networks with ReLUs train several times faster than their tanh equivalents.
- **Dropout in the fully connected layers**: applied to the first two fully connected layers with probability 0.5. Its alternatives at the time were weight decay alone, which the paper does not use to replace dropout.

## Results

On the LSVRC-2010 test data, the network reached top-1 and top-5 error rates of 39.7% and 18.9%. The abstract describes this as considerably better than the previous state of the art.

## Limitations

- The evidence is one network on one 2010 benchmark. Its margin over other systems is reported for that setting only.
- Training relied on a large labelled dataset and GPU compute, which were not common at the time.
- The architecture is large for its time. The paper's design choices, such as the layer sizes, were later simplified and improved by deeper networks, including [ResNet](../resnet/index.md).

## Variants and more variants

- **Deeper successors**: VGG and ResNet kept the convolutional idea and added depth. The [ResNet](../resnet/index.md) page covers the residual-connection version.
- **Regularisation alternatives**: later models often replaced dropout with batch normalisation or weight decay in parts of the network.

## Connections

- Parent topic: [Backbones and Scaling](../index.md)
- Other method on this topic: [ResNet](../resnet/index.md)
- The optimiser most often used to train networks like this is [Adam](https://arxiv.org/abs/1412.6980), cited below.

## Applications

- Image classification, the task AlexNet was built for, and the basis for transfer learning in vision.
- Feature extraction: the convolutional layers, pre-trained on ImageNet, are reused as features for other image tasks.

## Open questions

- Which parts of AlexNet's design were essential, and which were artefacts of the 2012 hardware?
- How much does the ImageNet pre-training help when the target task has a very different image distribution?

## References

### Seminal papers

- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet paper, with the 39.7% and 18.9% test error rates and the 60-million-parameter network.
- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — Residual connections, which the abstract says make very deep networks easier to optimise and able to gain accuracy from increased depth.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — The Adam optimiser, first published at ICLR 2015 and widely used to train neural networks.
- Zhang, C., et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — Shows that networks easily fit random labels, which challenges classical explanations of how deep models generalise.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — A standard textbook on the mathematics and practice of deep learning, free online.
- Zhang, A., Lipton, Z. C., Li, M. & Smola, A. J. *Dive into Deep Learning*. https://d2l.ai/ — An interactive online textbook in which each section is an executable notebook, useful for hands-on practice.
