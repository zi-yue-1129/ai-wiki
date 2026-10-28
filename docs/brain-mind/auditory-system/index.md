---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- theory/models/speech
tags:
- neuroscience
- perception
- speech
aliases:
  - 聽覺系統
  - 聽覺皮層
  - 耳蝸
  - 音調拓撲
  - Auditory System
  - Auditory Cortex
  - Cochlea
  - Tonotopy
---

# The Auditory System

Hearing turns pressure waves in the air into the speech, music and warnings that people use every day. This page covers how the cochlea and the auditory cortex do that, and how deep networks trained on sound are now used as models of the cortex. It is the hearing counterpart of [Perception and the Visual System](../visual-perception/index.md).

## Overview

Sound reaches the ear as a single fluctuating pressure signal, yet listeners pick out words from one voice in a noisy room, recognise a melody, and locate a sound in space. The auditory system has to split that mixture into sources and recover what each one is. Its early stages break sound into frequency bands, and later stages extract features such as pitch, phonemes and voice identity. [Neuroscience Basics](../neuroscience/index.md) covers the recording methods used to study these stages.

## Key concepts

- **Cochlea**: the spiral organ of the inner ear. Its membrane and hair cells convert sound vibration into neural firing, with each position tuned to a different frequency.
- **Tonotopy**: an orderly map of frequency across a structure. Neighbouring places respond to neighbouring frequencies.
- **Spectrogram (cochleagram)**: a time-by-frequency picture of sound. Many auditory models start from one.
- **Auditory hierarchy**: a sequence of stages, from the primary auditory cortex to surrounding non-primary areas, that respond to increasingly complex sound features.
- **Cocktail party problem**: the task of following one talker among others. It is a classic test of speech in noise.

## Core ideas

1. **The cochlea sorts sound by frequency.** The basilar membrane carries a travelling wave that peaks at a place set by frequency. High frequencies peak near the base and low frequencies near the apex. Outer hair cells add active amplification, which sharpens tuning for quiet sounds (Robles & Ruggero, 2001).
2. **Frequency maps continue into cortex.** Human primary auditory cortex contains two mirror-symmetric tonotopic maps (Formisano et al., 2003).
3. **Beyond the core, areas specialise.** Non-primary regions include areas selective for pitch, music and speech (Kell et al., 2018). Rauschecker and Scott (2009) review maps and streams in auditory cortex, drawing on nonhuman primate work. Hickok and Poeppel (2007) review how speech processing is organised in the cortex.
4. **The cortex follows the attended voice.** Cherry (1953) studied listeners' recognition of speech when two speech signals were presented together. Recordings from non-primary human auditory cortex encode features of the attended speaker in a two-talker mixture (Mesgarani & Chang, 2012). This suggests that attention shapes what the cortex encodes, not only what the ear receives.
5. **Trained networks show a cortical-like hierarchy.** A deep network trained only to recognise words and music genres reproduces human-like behaviour and predicts fMRI responses better than a spectrotemporal filter model. Its intermediate layers best predict primary cortex, and its deeper layers best predict non-primary regions (Kell et al., 2018).

## How it works

Sound enters the cochlea and is filtered into overlapping frequency channels. Hair cells convert each channel's motion into spikes in the auditory nerve. The signal then passes through the brainstem to the thalamus and to primary auditory cortex. Each stage keeps part of the frequency map and adds features that depend on timing, such as the rate at which loudness changes.

Speech in noise is the hard case. The mixture of voices overlaps in frequency and time, so the system must separate them using cues such as pitch, timing and location, and attention. The [biased competition](../attention-brain-machine/biased-competition/index.md) account of attention describes a related mechanism in vision.

## Key methods

Each method has its own page. This list is only a comparison.

- [Task-optimised networks (Kell et al., 2018)](kell-2018/index.md): trains a deep network on speech and music tasks, then tests its fit to behaviour and to brain responses, without training it on brain data.
- [Multiresolution spectrotemporal model (Chi et al., 2005)](chi-2005/index.md): a hand-designed model of cortical analysis that represents sound by its spectral and temporal structure. It is the kind of model that trained networks are compared against.

## Connections

- **Visual system**: the same question, whether networks trained for a task predict cortex, was first tested in vision. See [Performance-Optimised Networks (Yamins et al., 2014)](../visual-perception/yamins-2014/index.md).
- **NeuroAI**: the auditory case is one row of the task-optimised paradigm on the [NeuroAI](../neuroai/index.md) page.
- **Language**: the speech stream links to [Hickok & Poeppel's dual-stream model](../language-in-brain/hickok-poeppel-2007/index.md) and to [Language in the Brain](../language-in-brain/index.md).
- **Attention**: the cocktail party problem is an attention problem, covered in [Attention and the Brain](../attention-brain-machine/index.md).
- **Neuroimaging**: several human results here come from fMRI, whose limits are described in [BOLD fMRI](../neuroimaging-methods/bold-fmri/index.md).
- **Receptive fields**: auditory neurons have receptive fields in time and frequency. The visual case is in [Receptive Fields in Visual Cortex](../neuroscience/receptive-fields-hubel-wiesel/index.md).

## Applications

- **Hearing aids and cochlear implants**: these replace or amplify the cochlea's frequency analysis. Their design depends on the cochlear mechanics above.
- **Speech technology**: speech recognition systems and their front ends use spectrogram-based features, the same representation that auditory models start from. See [Speech & Audio](../../theory/models/speech/index.md).
- **Speech neuroprostheses**: decoding speech-related brain signals to restore communication is covered in [Speech Neuroprosthesis](../bci/speech-neuroprosthesis/index.md).

## Open questions

- **How far does the similarity go?** The match to the cortical hierarchy is partial. The network leaves some reliable responses unexplained, and its final layers predict cortex poorly.
- **Which tasks shape the hierarchy?** Kell et al. (2018) used two tasks. Whether other tasks, such as sound localisation or speaker identity, would change the layers that match cortex is unclear.
- **How do listeners separate voices?** The cortical mechanisms that select one talker, and how attention changes them, are still being mapped.
- **How do humans learn from so little data?** The networks were trained on millions of labelled examples, far more explicit supervision than people usually receive for hearing.

## References

### Seminal papers

- Cherry, E. C. (1953). Some experiments on the recognition of speech, with one and with two ears. *Journal of the Acoustical Society of America*. https://doi.org/10.1121/1.1907229 — Studies listeners' recognition of speech when two speech signals are presented together, and when different signals reach each ear.
- Formisano, E., Kim, D.-S., Di Salle, F., van de Moortele, P.-F., Ugurbil, K. & Goebel, R. (2003). Mirror-symmetric tonotopic maps in human primary auditory cortex. *Neuron*. https://doi.org/10.1016/S0896-6273(03)00669-X — Reports two mirror-symmetric tonotopic frequency maps in human primary auditory cortex.
- Mesgarani, N. & Chang, E. F. (2012). Selective cortical representation of attended speaker in multi-talker speech perception. *Nature*. https://doi.org/10.1038/nature11020 — Shows that recordings from non-primary human auditory cortex encode features of the attended speaker in a two-talker mixture.
- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H. (2018). A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy. *Neuron*. https://doi.org/10.1016/j.neuron.2018.03.044 — Trains a network on speech and music tasks and compares it with human behaviour and auditory cortex fMRI.

### Surveys and textbooks

- Robles, L. & Ruggero, M. A. (2001). Mechanics of the mammalian cochlea. *Physiological Reviews*. https://doi.org/10.1152/physrev.2001.81.3.1305 — Review of cochlear mechanics: travelling waves, tonotopic place coding and outer hair cell amplification.
- Rauschecker, J. P. & Scott, S. K. (2009). Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*. https://doi.org/10.1038/nn.2331 — Reviews maps and streams in auditory cortex, drawing on nonhuman primate work and its bearing on human speech processing.
- Hickok, G. & Poeppel, D. (2007). The cortical organization of speech processing. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2113 — A review of how speech processing is organised across the cortex.
