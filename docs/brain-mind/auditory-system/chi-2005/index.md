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

The question was whether a single, principled representation could capture both the spectral and the temporal aspects of complex sounds, such as speech and music, while staying close to what is known about the auditory pathway.

## Core idea

The model starts from a cochlea-like spectrogram of the sound. It then applies a bank of filters at several resolutions. Each filter, an idealised spectro-temporal receptive field, responds to a particular spectral scale (how fine a pattern is across frequency) and a particular temporal rate (how fast it changes over time). The output is a unified multiresolution representation of the sound. The model is built from psychoacoustic and neurophysiological findings from the early and central auditory stages. Its fidelity is tested by reconstructing sound from the representation, which shows how much of the signal the features retain.

## Equation or algorithm

1. **Peripheral analysis.** Compute a time-frequency spectrogram of the sound, using a bank of overlapping constant-Q frequency channels.
2. **Central analysis.** Convolve the spectrogram with a bank of filters. Each filter is tuned to one spectral scale and one temporal rate, and filters span several resolutions.
3. **Representation.** The filter outputs form a four-dimensional representation over time, frequency, scale and rate. The paper integrates it over time to give a three-dimensional form.
4. **Reconstruction.** Invert the representation to resynthesise sound. Compare the result with the original to assess how much information the features keep.

The paper gives the full mathematical form of how a complex signal passes through each stage, and it relates these stages to other auditory processing models.

## Results

The paper's results concern the representation itself. Reconstruction tests show that some resynthesised speech is completely intelligible, that losing spectrally sharp features gradually reduces intelligibility, and that some reconstruction algorithms still produce distortions. Earlier, simpler versions of the approach had been checked against speech intelligibility and monaural phase sensitivity. The abstract gives no numerical benchmark, so this page does not quote one.

## Limitations

- **Fixed design.** The filters are chosen by design, not learned from data. The model therefore cannot adapt to the statistics of the sounds it hears.
- **Descriptive, not predictive, of cortex.** The model describes the representation. It does not by itself say how well a population of neurons would respond.
- **Comparison with data.** In the study that followed, a spectrotemporal filter model explained less fMRI variance across auditory cortex than a trained network (55.1% against 69.9%). Hand-designed features may therefore miss some response structure that learning captures (Kell et al., 2018).
- **Scope.** The abstract makes no explicit claim about cortex, and the paper describes the model as "not biophysical in spirit". Any link to specific cortical neurons is therefore an inference.

## Connections

- **Cochlear front end**: the model starts from a spectrogram of the kind produced by the cochlea. See [The Auditory System](../index.md).
- **Trained alternative**: the same question, what features best describe auditory cortex, is answered by learned features in [Task-Optimised Networks](../kell-2018/index.md).
- **Receptive fields**: tuning to specific patterns of frequency and time parallels the receptive-field idea in [Receptive Fields in Visual Cortex](../../neuroscience/receptive-fields-hubel-wiesel/index.md).
- **Sparse coding**: efficient, selective representations of natural signals are discussed in [Sparse Coding](../../computational-neuroscience/sparse-coding/index.md).

## Applications

- **Model comparison**: Kell et al. (2018) used a spectrotemporal filter model of this kind as the baseline when comparing trained networks with cortical fMRI responses.

## Open questions

- **Which resolutions does the cortex use?** The set of spectral scales and temporal rates needed to match cortical tuning is still a matter of study.
- **Learned or fixed?** Whether a learned front end would give a better fit to cortex than a designed one, as in Kell et al. (2018), is not settled.
- **Speech in noise.** Whether the representation separates overlapping talkers, rather than just describing a single sound, remains open.

## References

### Seminal papers

- Chi, T., Ru, P. & Shamma, S. A. (2005). Multiresolution spectrotemporal analysis of complex sounds. *Journal of the Acoustical Society of America*. https://doi.org/10.1121/1.1945807 — The original paper. It proposes a unified multiresolution representation of spectral and temporal features, with reconstruction tests.
- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H. (2018). A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy. *Neuron*. https://doi.org/10.1016/j.neuron.2018.03.044 — Compares a trained network with a spectrotemporal filter model on auditory cortex fMRI.
- Theunissen, F. E., Sen, K. & Doupe, A. J. (2000). Spectral-Temporal Receptive Fields of Nonlinear Auditory Neurons Obtained Using Natural Sounds. *The Journal of Neuroscience*. https://doi.org/10.1523/jneurosci.20-06-02315.2000 — Shows that spectro-temporal receptive fields estimated from birdsong predict auditory neuron responses better than fields estimated from random tone pips.

### Surveys and textbooks

- Robles, L. & Ruggero, M. A. (2001). Mechanics of the mammalian cochlea. *Physiological Reviews*. https://doi.org/10.1152/physrev.2001.81.3.1305 — Reviews cochlear mechanics: travelling waves, tonotopic place coding and outer hair cell amplification.
- Rauschecker, J. P. & Scott, S. K. (2009). Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*. https://doi.org/10.1038/nn.2331 — Reviews maps and streams in auditory cortex, drawing on nonhuman primate work and its bearing on human speech processing.
