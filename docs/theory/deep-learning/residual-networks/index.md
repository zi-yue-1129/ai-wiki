---
status: draft
last_reviewed: 2026-10-28
---

# Residual networks (He et al., 2015)

Each block learns a residual function of its input and adds the input back through a shortcut, so passing the signal through unchanged is easy.

## Problem

Very deep networks are hard to optimise, so adding layers stops helping.

## Core idea

Each block learns a residual function of its input and adds the input back through a shortcut. Passing the signal through unchanged is then easy to learn.

## Equation or algorithm

For a block with input \(x\),

\[
y = \mathcal{F}(x, \{W_i\}) + x
\]

## Results

Networks up to 152 layers deep, about eight times deeper than VGG nets with lower complexity. An ensemble of these networks reached 3.57% error on the ImageNet test set and won first place in the ILSVRC 2015 classification task.

## Limitations

The 3.57% figure comes from an ensemble, not a single network. The identity shortcut is a design choice the paper motivates, not one it proves optimal.

## Connections

- Parent topic: [Deep Learning](../index.md)
- Other method on this topic: [AlexNet](../alexnet/index.md)

## References

### Seminal papers

- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet paper, whose ImageNet result started the modern deep-learning era.
- He, K., et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — Residual connections that make very deep networks trainable.
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization*. arXiv. https://arxiv.org/abs/1412.6980 — The Adam optimiser, still a default choice for training many neural networks.
- Zhang, C., et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — Shows that networks can fit random labels, challenging classical explanations of how deep models generalise.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — The standard textbook on the mathematics and practice of deep learning, free online.
- Zhang, A., Lipton, Z. C., Li, M. & Smola, A. J. *Dive into Deep Learning*. https://d2l.ai/ — An interactive online textbook with runnable code, useful for hands-on practice.
