---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- perception
- speech
aliases:
  - 多解析度頻譜時間模型
  - 頻譜時間感受野
  - Spectrotemporal Model
  - Chi et al. 2005
---

# Multiresolution spectrotemporal model (Chi et al., 2005)

A computational model of central auditory processing that represents sound jointly by its spectral and temporal structure, at several resolutions at once.

This page is one method in [The Auditory System](../index.md). It is the hand-designed counterpart of the trained networks on [Task-Optimised Networks (Kell et al., 2018)](../kell-2018/index.md).

## Overview

Sound changes across frequency and across time, and the auditory system needs both. A spectrogram shows frequency over time, but it does not directly show the patterns that matter to the cortex, such as how quickly a sound's loudness changes or how finely its spectrum is structured. Chi, Ru and Shamma (2005) proposed one model that represents both kinds of structure together.

## Problem

Earlier auditory representations often treated spectral and temporal features separately, or built each for a single task. The question was whether a single, principled representation could capture both aspects of complex sounds, such as speech and music, while staying close to what is known about the auditory pathway.

## Core idea

The model starts from a cochlea-like spectrogram of the sound. It then applies a bank of filters at several resolutions. Each filter responds to a particular spectral scale (how fine a pattern is across frequency) and a particular temporal rate (how fast it changes over time). The output is a unified multiresolution representation of the sound. The model is built from psychoacoustic and neurophysiological findings from the early and central auditory stages. Its fidelity is tested by reconstructing sound from the representation, which shows how much of the signal the features retain.

## Equation or algorithm

1. **Peripheral analysis.** Compute a time-frequency spectrogram of the sound, as the cochlea does with its frequency channels.
2. **Central analysis.** Convolve the spectrogram with a bank of filters. Each filter is tuned to one spectral scale and one temporal rate, and filters span several resolutions.
3. **Representation.** Use the filter outputs as a time-varying map over scale and rate. This is the unified representation.
4. **Reconstruction.** Invert the representation to resynthesise sound. Compare the result with the original to assess how much information the features keep.

The paper gives the full mathematical form of how a complex signal passes through each stage, and it relates these stages to other auditory processing models.

## Results

The paper's central results concern the representation itself. It shows that the model can resynthesise sound from its features, which tests the representation's fidelity, and it assesses how much each feature contributes to what is perceived. Earlier, simpler versions of the approach had been checked against speech intelligibility and monaural phase sensitivity. The abstract gives no numerical benchmark, so this page does not quote one.

## Limitations

- **Fixed design.** The filters are chosen by design, not learned from data. The model therefore cannot adapt to the statistics of the sounds it hears.
- **Descriptive, not predictive, of cortex.** The model describes the representation. It does not by itself say how well a population of neurons would respond.
- **Comparison with data.** In the study that followed, a spectrotemporal filter model explained less fMRI variance across auditory cortex than a trained network (55.1% against 69.9%). Hand-designed features may therefore miss some response structure that learning captures (Kell et al., 2018).
- **Scope.** The abstract makes no explicit claim about cortex. The model is inspired by central auditory stages, so any link to cortex is an inference.

## Connections

- **Cochlear front end**: the model starts from a spectrogram of the kind produced by the cochlea. See [The Auditory System](../index.md).
- **Trained alternative**: the same question, what features best describe auditory cortex, is answered by learned features in [Task-Optimised Networks](../kell-2018/index.md).
- **Receptive fields**: tuning to specific patterns of frequency and time parallels the receptive-field idea in [Receptive Fields in Visual Cortex](../../neuroscience/receptive-fields-hubel-wiesel/index.md).
- **Sparse coding**: efficient, selective representations of natural signals are discussed in [Sparse Coding](../../computational-neuroscience/sparse-coding/index.md).

## Applications

- **Sound analysis**: spectrotemporal representations are used in audio analysis, where some features are easier to see than in a plain spectrogram.
- **Auditory research**: models of this kind are used as a reference when testing whether a neural response depends on spectral or temporal structure.

## Open questions

- **Which resolutions does the cortex use?** The set of spectral scales and temporal rates needed to match cortical tuning is still a matter of study.
- **Learned or fixed?** Whether a learned front end would give a better fit to cortex than a designed one, as in Kell et al. (2018), is not settled.
- **Speech in noise.** Whether the representation separates overlapping talkers, rather than just describing a single sound, remains open.

## References

### Seminal papers

- Chi, T., Ru, P. & Shamma, S. A. (2005). Multiresolution spectrotemporal analysis of complex sounds. *Journal of the Acoustical Society of America*. https://doi.org/10.1121/1.1945807 — The original paper. It proposes a unified multiresolution representation of spectral and temporal features, with reconstruction tests.
- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H. (2018). A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy. *Neuron*. https://doi.org/10.1016/j.neuron.2018.03.044 — Compares a trained network with a spectrotemporal filter model on auditory cortex fMRI.

### Surveys and textbooks

- Robles, L. & Ruggero, M. A. (2001). Mechanics of the mammalian cochlea. *Physiological Reviews*. https://doi.org/10.1152/physrev.2001.81.3.1305 — Review of the cochlear processing that supplies the spectrogram-like input to central models.
