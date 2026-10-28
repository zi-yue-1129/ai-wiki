---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning
  - theory/models/transformer
  - start/history/expert-systems-and-winters
tags:
  - history
  - deep learning
  - large language models
aliases:
  - 深度學習革命
  - 深度學習發展
  - Deep learning revolution
---

# History: the deep-learning revolution (2006–present)

From the mid-2000s, neural networks with many layers went from a niche research topic to the core method of AI. Their success depended on methods that trained deep models, on large labelled and unlabelled datasets, and on hardware that made large experiments affordable. This page follows the main steps, from deep belief networks through AlexNet, sequence models, AlphaGo, Transformers and the era of large language models. It also notes how each step changed the field's institutions, not only its methods.

## Overview

The revival began with a method for training deep networks layer by layer. Hinton, Osindero and Teh showed that a deep belief network could be trained with a greedy, layer-wise procedure, and that the resulting model could then be fine-tuned [(Hinton, Osindero and Teh, 2006)](https://doi.org/10.1162/neco.2006.18.7.1527). The approach was an early sign that depth could be made trainable again. Within a few years, the emphasis moved from pretraining to large supervised networks, trained with improved optimisers and activations on large data.

## Key steps

- **Deep belief nets (2006)**: layer-wise pretraining made deep models trainable in practice [(Hinton et al., 2006)](https://doi.org/10.1162/neco.2006.18.7.1527).
- **ImageNet and AlexNet (2012)**: a deep convolutional network trained on ImageNet produced a large jump in image classification. The paper showed the value of scale in data and computation [(Krizhevsky, Sutskever and Hinton, 2012)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html).
- **Sequence-to-sequence learning (2014)**: an encoder-decoder network learned to map one sequence to another, such as translating a sentence from English to French [(Sutskever, Vinyals and Le, 2014)](https://arxiv.org/abs/1409.3215).
- **Attention (2014)**: learning to align source and target words in translation removed the bottleneck of a single fixed-length vector [(Bahdanau, Cho and Bengio, 2014)](https://arxiv.org/abs/1409.0473).
- **AlphaGo (2016)**: a combination of deep networks and tree search played the game of Go at a level that had been out of reach for computers [(Silver et al., 2016)](https://doi.org/10.1038/nature16961).
- **Transformers (2017)**: an attention-only architecture became the default for sequence modelling and later for many other tasks [(Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762).
- **Large language models (2020 onward)**: scaling a Transformer language model with large data and parameters gave few-shot learning from prompts. The GPT-3 report, for example, described a model with 175 billion parameters [(Brown et al., 2020)](https://arxiv.org/abs/2005.14165).

## How the field changed

The revolution changed how the field was organised, not only what it did. Benchmarks such as ImageNet made progress visible and shared, and they set a pattern in which a common dataset defines a community. Open-source frameworks lowered the cost of experimentation. PyTorch, for example, was introduced as a library that combined usability with speed [(Paszke et al., 2019)](https://arxiv.org/abs/1912.01703). Large industrial labs took on research at a scale that universities could seldom match, and the cost of training began to shape who could work at the frontier.

Deep learning also brought new roles and new questions. Research increasingly depended on large engineering teams and on access to compute, and that dependence is a theme of later pages on [Compute governance](../../../society/governance/compute-governance.md).

## Connections

The earlier steps are told in the [expert-systems and winters chapter](../expert-systems-and-winters/index.md). The methods are covered in [Deep learning](../../../theory/deep-learning/index.md) and [Transformers](../../../theory/models/transformer/index.md). The timeline in the [History of AI](../index.md) overview gives the dates in one place.

## Applications

Deep learning now underlies speech recognition, translation, image analysis, drug discovery, and recommendation and search systems. Many of these applications came from transfer of methods across tasks, rather than from separate research programmes.

## Open questions

- Which of the gains from scale will continue, and which will saturate?
- How far did the shift to large labs change which research questions get asked?
- What institutional changes, such as shared benchmarks or open releases, help the field judge progress?

## References

### Seminal papers

- Hinton, Osindero and Teh, *A Fast Learning Algorithm for Deep Belief Nets*, Neural Computation (2006). https://doi.org/10.1162/neco.2006.18.7.1527 — Introduces a layer-wise procedure for training deep belief networks.
- Krizhevsky, Sutskever and Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, NeurIPS (2012). https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — The AlexNet paper, a deep convolutional network trained on ImageNet.
- Sutskever, Vinyals and Le, *Sequence to Sequence Learning with Neural Networks* (2014). https://arxiv.org/abs/1409.3215 — An encoder-decoder model for sequence transduction.
- Bahdanau, Cho and Bengio, *Neural Machine Translation by Jointly Learning to Align and Translate* (2014). https://arxiv.org/abs/1409.0473 — Introduces attention for neural machine translation.
- Silver et al., *Mastering the game of Go with deep neural networks and tree search*, Nature (2016). https://doi.org/10.1038/nature16961 — The AlphaGo paper, combining deep networks with tree search to play Go.
- Vaswani et al., *Attention Is All You Need* (2017). https://arxiv.org/abs/1706.03762 — Introduces the Transformer, an attention-only architecture for sequence modelling.
- Brown et al., *Language Models are Few-Shot Learners* (2020). https://arxiv.org/abs/2005.14165 — The GPT-3 report, with the 175 billion parameter figure.

### Surveys and textbooks

- LeCun, Bengio and Hinton, *Deep learning*, Nature (2015). https://doi.org/10.1038/nature14539 — A review of the field's core ideas by three of its central figures.

### Articles and documentation

- Paszke et al., *PyTorch: An Imperative Style, High-Performance Deep Learning Library* (2019). https://arxiv.org/abs/1912.01703 — Describes a widely used framework and its design goals.
