---
status: complete
last_reviewed: 2026-10-28
related:
- theory/models/transformer
- brain-mind/attention-brain-machine
tags:
- attention
- vision
- reinforcement learning
aliases:
  - 循環視覺注意力
  - Recurrent Models of Visual Attention
  - RAM
---

# Recurrent models of visual attention (Mnih et al., 2014)

The recurrent attention model (RAM) is a network that looks at an image one glimpse at a time. At each step it chooses where to look next, accumulates what it sees in a recurrent memory, and decides what to output. The location choice is not differentiable, so the model is trained with reinforcement learning, which makes it an early example of learned, goal-directed visual attention.

This page is part of [Attention in Brain & Machine](../index.md). It covers one model in detail.

## Overview

Biological vision does not process a whole scene at once. The eyes move, and attention selects a few locations for detailed processing. Mnih et al. asked whether a network could learn this selection itself, given only a classification signal, instead of processing every pixel. The answer was a model that learns where to look for a task.

## Key concepts

- **Glimpse**: a small, high-resolution patch of the image, centred on a chosen location, with lower resolution further from the centre.
- **Location policy**: the part of the network that chooses where to look next.
- **Recurrent core**: a hidden state that accumulates information across glimpses, so the model can integrate what it has seen.
- **Reinforcement learning for location**: the location choice samples a stochastic action, so it is trained with a reward signal rather than backpropagation alone.

## Problem

Processing a full high-resolution image is expensive, and a model that sees everything at once does not choose what matters. Hard attention, which selects a discrete location, cannot be trained by ordinary gradient descent, because sampling a location blocks the gradient. The question was how to train a model that attends to a few locations and still learns the task.

## Core idea

At each step, the network takes a glimpse at its current location, updates a recurrent state, and outputs a location for the next glimpse together with a classification at the end. Location choices are sampled from a distribution, and the model is trained with the REINFORCE policy-gradient method, using the correctness of its final classification as the reward. Other parts of the network are trained with ordinary backpropagation.

## Method

1. Take a low-resolution, wide-field glimpse at the current location, and encode it.
2. Update a recurrent state from the glimpse and the previous state.
3. Sample the next location from a policy that depends on the state.
4. Repeat for a fixed number of glimpses, then output a classification.
5. Train the classifier with backpropagation and the location policy with REINFORCE, using a reward for the final decision.

## Results

The paper reports that the model learns to attend to the relevant part of an image and classifies accurately on the tasks it tests, including a translated-MNIST task and a dynamic-control task. Its efficiency comes from processing a few glimpses instead of the whole image. The paper's numbers should be read from the paper itself; this page does not quote them.

## Limitations

- **High-variance training.** Reinforcement-learning gradients for the location policy are noisy, so training is slower and less stable than standard supervised learning.
- **Simple tasks.** The main experiments use small, controlled datasets, so the transfer to natural images is limited.
- **Fixed number of glimpses.** The model takes a set number of looks, which does not match the flexible, stopping-based attention seen in people.

## Connections

- **Biased competition and saliency**: the biological and bottom-up accounts of selection are on [Biased Competition](../biased-competition/index.md) and [Saliency Map](../saliency-map/index.md).
- **Transformer attention**: soft attention, which weights all inputs rather than choosing a location, is the mechanism of the [Transformer](../../../theory/models/transformer/index.md).
- **Reinforcement learning**: the location policy is trained with the same policy-gradient family covered in [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).
- **Parent topic**: [Attention in Brain & Machine](../index.md).

## Applications

- **Efficient vision**: learning where to look can reduce the computation needed for large images.
- **Robotics and active vision**: choosing where to look is central to robots that move their sensors to gather information.

## Open questions

- **Can hard attention scale?** Training stability is the main obstacle to using location choices in large models.
- **How do learned looks compare with human eye movements?** The match to human scanpaths is a research question rather than a result of the original paper.

## References

### Seminal papers

- Mnih, V., Heess, N., Graves, A. & Kavukcuoglu, K. (2014). Recurrent Models of Visual Attention. *Advances in Neural Information Processing Systems 27*. https://arxiv.org/abs/1406.6247 — Introduces the recurrent attention model, which chooses glimpse locations with a learned, reinforcement-trained policy.
- Ba, J., Mnih, V. & Kavukcuoglu, K. (2015). Multiple Object Recognition with Visual Attention. *International Conference on Learning Representations*. https://arxiv.org/abs/1412.7755 — Extends glimpse-based attention to recognising several objects in one image.
- Vaswani, A., et al. (2017). Attention Is All You Need. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1706.03762 — Introduces soft attention in the transformer, the differentiable alternative to choosing locations.

### Surveys and reviews

- Desimone, R. & Duncan, J. (1995). Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.ne.18.030195.001205 — Reviews how attention selects among competing stimuli in the visual system, the biological side of the question this model addresses.
- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M. (2017). Neuroscience-Inspired Artificial Intelligence. *Neuron*. https://doi.org/10.1016/j.neuron.2017.06.011 — A review of how neuroscience has inspired AI, including attention and selective processing.
- Itti, L., Koch, C. & Niebur, E. (1998). A model of saliency-based visual attention for rapid scene analysis. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. https://doi.org/10.1109/34.730558 — The bottom-up saliency model, which selects locations from feature contrast rather than from a learned policy.
