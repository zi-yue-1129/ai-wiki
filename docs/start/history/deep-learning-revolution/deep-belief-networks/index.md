---
status: draft
last_reviewed: 2026-10-28
tags:
  - deep learning
  - generative models
  - unsupervised learning
aliases:
  - 深度信念網路
  - 深度信念網絡
  - Deep belief networks
  - Deep belief nets
  - DBN
  - 受限玻爾茲曼機
  - Restricted Boltzmann machine
  - 貪婪逐層預訓練
---

# Deep Belief Networks (Hinton, Osindero & Teh, 2006)

A deep belief network is a stack of latent-variable layers trained one layer at a time, each layer learning from the output of the layer below. The 2006 paper that introduced the procedure is usually taken as the starting point of the revival described in the [deep learning revolution](../index.md) chapter.

## Overview

Gradient-based training of networks with several hidden layers, started from random weights, often worked poorly before 2006. The lower layers received weak learning signals, and in the experiments of Glorot and Bengio (2010) deeper networks performed worse than shallower ones. No reliable remedy was widely accepted. The earlier history is in the [backpropagation revival](../../expert-systems-and-winters/backpropagation-revival/index.md) chapter.

Hinton, Osindero and Teh proposed a different route. Each layer is first learned as a generative model of the layer below, greedily. Only then is the whole network adjusted for the task (Hinton et al., 2006). A companion paper applied the same idea to deep autoencoders, which learned low-dimensional codes better than principal components analysis on the data it studied (Hinton and Salakhutdinov, 2006).

## Key concepts

- **Restricted Boltzmann machine (RBM)**: a two-layer model with visible units for the data and hidden units for the learned features. Connections run only between the layers.
- **Contrastive divergence**: a fast approximate learning rule for RBMs, which replaces the exact gradient with a short sampling chain (Hinton, 2002).
- **Greedy layer-wise pretraining**: training one layer at a time while the layers below are held fixed.
- **Complementary priors**: priors over the hidden layers chosen to cancel the "explaining away" effect, so the posterior factorises.

## How it works

An RBM with visible vector $\mathbf{v}$ and hidden vector $\mathbf{h}$ assigns each configuration an energy

$$
E(\mathbf{v}, \mathbf{h}) = -\mathbf{a}^\top \mathbf{v} - \mathbf{b}^\top \mathbf{h} - \mathbf{v}^\top W \mathbf{h},
\qquad
P(\mathbf{v}, \mathbf{h}) = \frac{e^{-E(\mathbf{v}, \mathbf{h})}}{Z}.
$$

With no connections inside a layer, all units of one layer can be sampled at once given the other layer, which keeps learning cheap. The one-step contrastive divergence update compares statistics measured on the data with those measured after one reconstruction:

$$
\Delta W \propto \langle \mathbf{v}\mathbf{h}^\top \rangle_{\text{data}} - \langle \mathbf{v}\mathbf{h}^\top \rangle_{\text{reconstruction}}.
$$

For three hidden layers, the paper's final model is directed in its lower layers and undirected in its top two:

$$
P(\mathbf{v}, \mathbf{h}^1, \mathbf{h}^2, \mathbf{h}^3) = P(\mathbf{h}^2, \mathbf{h}^3)\, P(\mathbf{h}^1 \mid \mathbf{h}^2)\, P(\mathbf{v} \mid \mathbf{h}^1).
$$

Training proceeds as follows:

1. Train an RBM with the data as its visible layer and the first hidden layer as its hidden layer.
2. Freeze its weights and compute the first hidden layer's activations for every training example.
3. Use those activations as the data for a second RBM, and train it in the same way.
4. Repeat for the desired number of layers. The top two layers are kept as an undirected RBM.
5. Fine-tune all weights jointly with a contrastive version of the wake-sleep procedure.


## Results

The paper evaluates a three-hidden-layer network on images of handwritten digits and their labels. According to the authors, the model is a good generative model of the joint distribution of images and labels, and it classifies digits better than the best discriminative learning algorithms of the time.

These are small benchmark tasks, described here qualitatively; the numbers belong to the full papers.

## Limitations

- **Cost.** Sampling each RBM and making several passes over the data make pretraining slow.
- **Role of pretraining.** Better initialisation (Glorot and Bengio, 2010), [batch normalisation](../../../../theory/deep-learning/normalisation/batch-normalisation/index.md) and [dropout](../../../../theory/deep-learning/dropout/index.md) later allowed deep networks to be trained directly, which reduced the need for greedy pretraining.
- **Scale.** The evidence comes from small datasets, not the large image tasks described on the [ImageNet](../imagenet/index.md) page.

## Open questions

- Why did layer-wise pretraining help? Bengio et al. (2006) discuss the role of intermediate representations; the question is only partly settled.
- Unsupervised pretraining returned in the language models that followed the [Transformer](../../../../theory/models/transformer/attention-is-all-you-need/index.md). Is it the same principle?

## Connections

As a generative model with a hierarchy of features, it invites comparison with hierarchical models of the visual cortex (see [NeuroAI](../../../../brain-mind/neuroai/index.md)). The companion autoencoder work is described in [autoencoders and representations](../../../../theory/paradigms/unsupervised/autoencoders-and-representations/index.md).

## References

### Seminal papers

- Hinton, G. E., Osindero, S. & Teh, Y.-W. (2006). A fast learning algorithm for deep belief nets. *Neural Computation*. https://doi.org/10.1162/neco.2006.18.7.1527 — Introduces greedy layer-wise training of deep belief nets.
- Hinton, G. E. & Salakhutdinov, R. R. (2006). Reducing the dimensionality of data with neural networks. *Science*. https://doi.org/10.1126/science.1127647 — Shows that pretrained deep autoencoders learn better low-dimensional codes than principal components analysis.
- Bengio, Y., Lamblin, P., Popovici, D. & Larochelle, H. (2006). Greedy layer-wise training of deep networks. *Advances in Neural Information Processing Systems 19*. https://proceedings.neurips.cc/paper/2006/hash/5da713a690c067105aeb2fae32403405-Abstract.html — Extends greedy layer-wise pretraining beyond RBMs to other layer types.
- Hinton, G. E. (2002). Training products of experts by minimizing contrastive divergence. *Neural Computation*. https://doi.org/10.1162/089976602760128018 — Introduces contrastive divergence, the approximate rule that made RBMs practical to train.

### Surveys and textbooks

- Bengio, Y. (2009). Learning deep architectures for AI. *Foundations and Trends in Machine Learning*. https://doi.org/10.1561/2200000006 — Monograph on deep architectures and how to train them layer by layer.
- LeCun, Y., Bengio, Y. & Hinton, G. (2015). Deep learning. *Nature*. https://doi.org/10.1038/nature14539 — Review by three founders of the field of multi-layer representation learning.

### Articles and documentation

- Glorot, X. & Bengio, Y. (2010). Understanding the difficulty of training deep feedforward neural networks. *Proceedings of AISTATS 2010*. https://proceedings.mlr.press/v9/glorot10a.html — Analyses why deep feedforward networks train poorly and proposes a better initialisation.
