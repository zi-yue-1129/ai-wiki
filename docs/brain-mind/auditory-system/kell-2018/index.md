---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/cnn
tags:
- neuroscience
- perception
- language
aliases:
  - Kell 2018
  - 任務最佳化聽覺網路
  - Task-Optimized Neural Network
  - Task-optimised auditory network
---

# Task-Optimised Deep Networks for Hearing (Kell et al. 2018)

Kell et al. (2018) trained a deep neural network on everyday audio tasks, then compared it with human listeners and with human auditory cortex. They report that the network behaves like people on the tasks, that its responses predict auditory cortical activity, and that its stages form a cortex-like hierarchy. The paper is the auditory counterpart of [Yamins et al. 2014](../../visual-perception/yamins-2014/index.md) and a landmark of [NeuroAI](../../neuroai/index.md).

This page is part of [Hearing and the Auditory System](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## Overview

Much of what is known about the auditory cortex comes from simple sounds such as pure tones and noise bursts. These reveal tuning, but not how the system handles speech and music. Kell et al. asked a question parallel to the one Yamins et al. (2014) asked for vision: if a deep network is trained on the tasks people perform with sound, does its internal organisation come to resemble the auditory system?

## Key concepts

- **Task optimisation**: choosing a model's parameters by training it on a task, rather than by fitting it to neural recordings.
- **Cochleagram**: a time-frequency representation of sound that imitates the cochlea's frequency analysis. It is the network's input.
- **Encoding model**: a linear mapping from a model's internal units to the response of one recording site, fitted on some sounds and tested on others.
- **Hierarchy of stages**: the network's layers, read from input to output. The comparison asks which stage best matches which cortical area.

## How it works

1. **Input.** Each sound is converted into a cochleagram.
2. **Training.** A convolutional network with several stages is trained on several audio tasks at once, such as recognising words and speakers and classifying environmental sounds.
3. **Behavioural test.** The trained network is given the tasks that human listeners perform, including tasks in background noise. Its pattern of errors is compared with human performance.
4. **Neural test.** For each recording site, an encoding model is fitted from each stage to the site's response, using one set of sounds, and tested on sounds held out from fitting. The best-predicting stage is taken as the one that most closely matches that site.

The encoding step is a linear regression. If $h_\ell(x)$ is the activity of stage $\ell$ for sound $x$, the prediction for site $v$ is $\hat{r}_v(x) = \mathbf{w}_v^\top h_\ell(x)$, with a separate weight vector $\mathbf{w}_v$ for each site.

## Results

The title summarises three findings. The trained network reproduces aspects of human auditory behaviour, including its pattern of errors. Its internal stages predict responses in human auditory cortex to sounds not used in fitting. And the stages line up with a cortical hierarchy: the paper reports a progression in which earlier stages match primary auditory cortex and later stages match regions beyond it.

The quantitative results are in the paper. This page describes them qualitatively and does not quote figures.

## Limitations

- **Dependence on tasks.** The network's organisation depends on what it was trained to do, so the match reflects both its architecture and the chosen tasks.
- **Coarse neural data.** Human recordings average many neurons over space and time, so the comparison describes population responses, not what individual neurons compute.
- **Similarity is not mechanism.** Predicting cortical responses does not show that the brain uses the same computations.
- **Limited stimuli.** The comparison used a finite set of sounds, and generalisation to other voices and listening conditions is a question for later work.

## Open questions

- **Which tasks give a cortex-like hierarchy?** Kell and McDermott (2019) review how task constraints shape learned representations. Which tasks the human auditory system is optimised for is still debated.
- **Does the match hold at finer scales?** Testing the same models against single-neuron recordings would show whether the correspondence holds at the level of circuits.
- **How far does it extend to noisy speech?** Mattys et al. (2012) show that listeners cope with a wider range of adverse conditions than most models are tested on.

## References

### Seminal papers

- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H. (2018). A Task-Optimized Neural Network Replicates Human Auditory Behavior, Predicts Brain Responses, and Reveals a Cortical Processing Hierarchy. *Neuron*. https://doi.org/10.1016/j.neuron.2018.03.044 — Trains a deep network on audio tasks and shows that it matches human listening, predicts cortical responses and has a cortex-like hierarchy.
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.1403112111 — Shows that a network selected for object recognition predicts responses in V4 and inferior temporal cortex.

### Surveys and textbooks

- Kell, A. J. E. & McDermott, J. H. (2019). Deep neural network models of sensory systems: windows onto the role of task constraints. *Current Opinion in Neurobiology*. https://doi.org/10.1016/j.conb.2019.02.003 — Reviews how the tasks a network is trained on shape its sensory representations, and what that means for brain models.
- Yamins, D. L. K. & DiCarlo, J. J. (2016). Using goal-driven deep learning models to understand sensory cortex. *Nature Neuroscience*. https://doi.org/10.1038/nn.4244 — Argues that goal-optimised networks can serve as models of sensory cortex, and how to test them.
- Mattys, S. L., Davis, M. H., Bradlow, A. R. & Scott, S. K. (2012). Speech recognition in adverse conditions: A review. *Language and Cognitive Processes*. https://doi.org/10.1080/01690965.2012.705006 — Reviews how listeners recognise speech in noise and which processes compensate.

### Articles and documentation

- Wang, D. & Chen, J. (2018). Supervised Speech Separation Based on Deep Learning: An Overview. arXiv. https://arxiv.org/abs/1708.07524 — Surveys deep-learning methods that separate target speech from background noise.
