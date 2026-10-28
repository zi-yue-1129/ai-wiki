---
status: complete
last_reviewed: 2026-10-28
tags:
  - auditory cortex
  - spectrotemporal receptive field
  - computational neuroscience
aliases:
  - Multiresolution spectrotemporal model
  - 多解析度頻譜時間模型
---

# Multiresolution spectrotemporal model (Chi et al., 2005)

A computational model of central auditory processing that represents sound jointly by its spectral and temporal structure, at several resolutions at once.

This page is one method in [The Auditory System](../index.md). It is the hand-designed counterpart of the trained networks on [Task-Optimised Networks (Kell et al., 2018)](../kell-2018/index.md).

## Overview

Sound changes across frequency and across time, and the auditory system needs both. A spectrogram shows frequency over time, but it does not directly show the patterns that matter to the cortex, such as how quickly a sound's loudness changes or how finely its spectrum is structured. Chi, Ru and Shamma (2005) proposed one model that represents both kinds of structure together.

## Problem

The question was whether a single, principled representation could capture both the spectral and the temporal aspects of complex sounds, such as speech and music, while staying close to what is known about the early and central auditory system. Simplified versions of the model had already been used to assess speech intelligibility and monaural phase sensitivity. The 2005 paper gives a fuller mathematical formulation and shows how a signal passes through each stage.

## Core idea

The model has two parts. A cochlea-like front end produces a spectrogram of the sound. A central stage then analyses that spectrogram with filters tuned to two properties: the **spectral scale**, how fine a pattern is across frequency (in cycles per octave), and the **temporal rate**, how fast it changes over time (in hertz). Together these give one unified multiresolution representation of the sound's spectral and temporal features. The authors also show how to reconstruct sound from this representation, which tests how much of the signal the features keep.

## Equation or algorithm

1. **Peripheral analysis.** Pass the sound through a bank of 128 overlapping constant-Q bandpass filters, with centre frequencies spaced at 24 per octave over 5.3 octaves. Apply a lateral-inhibition derivative, half-wave rectification and integration with an 8 ms time constant to obtain the auditory spectrogram.
2. **Central analysis.** Convolve the spectrogram with a set of spectro-temporal filters. The paper gives an example range of 1 to 300 Hz for the rates and 0.25 to 8 cycles per octave for the scales. The reconstruction experiments use rates up to 32 Hz and scales up to 8 cycles per octave.
3. **Representation.** The cortical output is four-dimensional, over time, frequency, scale and rate. For display, it is integrated over time to give a three-dimensional form.
4. **Reconstruction.** Invert the representation to resynthesise sound from the auditory spectrogram and from the cortical representation. Compare the result with the original and with listeners' performance.

The paper's filter bandwidths are similar to those of Dau's model, but the two differ in how the temporal modulations from different spectral channels are combined. Dau's model is separable, while this model is not.

## Results

The paper's evidence concerns the representation itself, measured by reconstruction and by intelligibility tests.

- Resynthesised speech reaches a perceptual quality score (PESQ) of about 4.0, in the "toll quality" range.
- Filtering out temporal modulations around 4 Hz makes intelligibility marginal.
- Intelligibility persists when the scale filters are as broad as 0.5 to 1 cycle per octave. Losing sharp spectral features reduces intelligibility gradually, starting roughly where filters become wider than the critical bandwidth, about 3 cycles per octave.
- Reconstructions from magnitude alone are described as completely intelligible, but the authors also report distortions, and note that the quality of the reconstructed sounds is not very good.
- The model's intelligibility measure and listeners' scores deviate from each other in places.

## Limitations

- **Fixed design.** The filters are chosen by design, not learned from data, so the model cannot adapt to the statistics of the sounds it hears.
- **Not a biophysical model.** The authors state that "the model we describe is not biophysical in spirit". It is a computational realisation of the stages, not a description of the neurons in them.
- **Less explanatory power than a trained model.** In the study that followed, a spectrotemporal filter model explained less fMRI variance across auditory cortex than a trained network (median 55.1% against 69.9%). Hand-designed features may therefore miss some response structure that learning captures ([Kell et al., 2018](../kell-2018/index.md)).
- **Reconstruction is imperfect.** The distortions in resynthesised sound mean the representation discards or alters some information.

## Connections

- **Cochlear front end**: the model starts from a spectrogram of the kind produced by the cochlea. See [The Auditory System](../index.md).
- **Trained alternative**: the same question, what features best describe auditory cortex, is answered by learned features in [Task-Optimised Networks](../kell-2018/index.md).
- **Receptive fields**: tuning to specific patterns of frequency and time parallels the receptive-field idea in [Receptive Fields in Visual Cortex](../../neuroscience/receptive-fields-hubel-wiesel/index.md).
- **Sparse coding**: efficient, selective representations of natural signals are discussed in [Sparse Coding](../../computational-neuroscience/sparse-coding/index.md).

## Applications

- **Model comparison**: Kell et al. (2018) used a spectrotemporal filter model of this kind as the commonly used baseline when comparing trained networks with cortical fMRI responses.

## Open questions

- **Which resolutions does the cortex use?** The set of spectral scales and temporal rates needed to match cortical tuning is still a matter of study.
- **Learned or fixed?** Whether a learned front end would give a better fit to cortex than a designed one, as in Kell et al. (2018), is not settled.
- **Speech in noise.** Whether the representation separates overlapping talkers, rather than just describing a single sound, remains open.

## References

### Seminal papers

- Chi, T., Ru, P. & Shamma, S. A. (2005). Multiresolution spectrotemporal analysis of complex sounds. *Journal of the Acoustical Society of America*, 118(2), 887–906. https://doi.org/10.1121/1.1945807 — The original paper. It proposes a unified multiresolution representation of spectral and temporal features, with reconstruction tests and intelligibility results.
- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H. (2018). A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy. *Neuron*, 98(3), 630–644. https://doi.org/10.1016/j.neuron.2018.03.044 — Compares a trained network with a spectrotemporal filter model on auditory cortex fMRI.
- Theunissen, F. E., Sen, K. & Doupe, A. J. (2000). Spectral-Temporal Receptive Fields of Nonlinear Auditory Neurons Obtained Using Natural Sounds. *The Journal of Neuroscience*, 20(6), 2315–2331. https://doi.org/10.1523/JNEUROSCI.20-06-02315.2000 — Introduces spectro-temporal receptive fields estimated from natural sounds, the receptive-field framework that spectrotemporal models such as this one build on.

### Surveys and textbooks

- Robles, L. & Ruggero, M. A. (2001). Mechanics of the Mammalian Cochlea. *Physiological Reviews*, 81(3), 1305–1352. https://doi.org/10.1152/physrev.2001.81.3.1305 — Review of cochlear mechanics, the front end on which the spectrogram stage is based.
- Rauschecker, J. P. & Scott, S. K. (2009). Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*, 12(6), 718–724. https://doi.org/10.1038/nn.2331 — Review of maps and streams in auditory cortex, drawing on nonhuman primate work and its bearing on speech.
