---
status: draft
last_reviewed: 2026-10-28
---

# AlexNet (Krizhevsky, Sutskever & Hinton, 2012)

A large deep convolutional network trained on GPUs, using non-saturating neurons and a new regularisation method.

## Problem

Classify 1.3 million high-resolution ImageNet images into 1,000 classes, where earlier systems fell well short.

## Core idea

A large deep convolutional network trained on GPUs. It uses non-saturating neurons to speed up training and a new regularisation method for the fully connected layers to reduce overfitting.

## Architecture

Five convolutional layers, some followed by max-pooling, and two fully connected layers ending in a 1,000-way softmax, with about 60 million parameters.

## Results

On the LSVRC-2010 test data, top-1 and top-5 error rates of 39.7% and 18.9%, which the authors describe as considerably better than the previous state of the art.

## Limitations

The evidence is one network on a 2010 benchmark. Training relied on a large labelled dataset and GPU compute, which were not common at the time.

## Connections

- Parent topic: [Deep Learning](../index.md)
- Other method on this topic: [ResNet, in the CNN section](../../models/cnn/backbones-and-scaling/resnet/index.md)

## References

### Seminal papers

- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet paper, whose ImageNet result started the modern deep-learning era.
- He, K., et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — Residual connections that make very deep networks trainable.
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization*. arXiv. https://arxiv.org/abs/1412.6980 — The Adam optimiser, still a default choice for training many neural networks.
- Zhang, C., et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — Shows that networks can fit random labels, challenging classical explanations of how deep models generalise.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — The standard textbook on the mathematics and practice of deep learning, free online.
- Zhang, A., Lipton, Z. C., Li, M. & Smola, A. J. *Dive into Deep Learning*. https://d2l.ai/ — An interactive online textbook with runnable code, useful for hands-on practice.
