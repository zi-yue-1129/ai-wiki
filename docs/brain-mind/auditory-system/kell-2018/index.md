---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- perception
- speech
aliases:
  - 任務最佳化神經網路
  - 聽覺皮層的深度網路模型
  - Task-Optimized Neural Network
  - Kell et al. 2018
---

# Task-optimised networks model auditory cortex (Kell et al., 2018)

A deep network trained only on speech and music tasks reproduces human listening behaviour and predicts responses in auditory cortex, with its layers roughly matching the cortical hierarchy.

This page is one method in [The Auditory System](../index.md). It is the auditory counterpart of [Performance-Optimised Networks (Yamins et al., 2014)](../../visual-perception/yamins-2014/index.md).

## Overview

A model of the auditory cortex should behave like a listener and respond like the brain. Kell et al. (2018) tested whether a network built for everyday sound tasks could do both without being fitted to brain data. The network was trained to recognise words in speech and to classify the genre of music. Its behaviour was then compared with human listeners, and its internal layers with fMRI responses in the cortex.

## Problem

Hand-designed models of auditory cortex, such as spectrotemporal filter models, capture some of the responses to natural sound, but they are built from assumptions about which features matter. The question was whether features learned from a real task would match the human auditory system without those assumptions, and whether they would also match the arrangement of cortical areas.

## Core idea

The network is trained on a task that listeners perform, not on recordings from the brain. Its input is a cochlea-like representation of sound. After training, the learned features are compared with people and with brain data, using the same test sounds. After seven shared layers, the network splits into a word branch and a genre branch.

## Equation or algorithm

1. **Input.** Each 2-second clip is turned into a cochleagram with 211 filters, with centre frequencies from 30 to 7860 Hz. The result is resized to 256 by 256.
2. **Architecture.** The network has twelve layers. The first seven are shared, and the network then branches into two sets of five task-specific layers, one for words and one for genre.
3. **Training.** The word task is a 587-way classification of the word at the midpoint of a two-second clip. The clips use words from TIMIT and WSJ, mixed with background sounds at a mean signal-to-noise ratio of 3 dB (auditory scenes and speech babble) or 6 dB (music). The genre task is a 41-way classification of two-second music clips, with noise mixed in at a mean signal-to-noise ratio of 12 dB.
4. **Evaluation.** For each layer, a linear encoding model predicts fMRI responses to the test sounds, and the variance explained is compared across regions.

A fully separate pair of networks would have nearly twice as many parameters.

## Results

- **Behaviour.** On word recognition, the network's accuracy across background types and signal-to-noise ratios matched that of 18 listeners (r² = 0.92). A simple measure of distortion in the cochleagram explained much less (r² = 0.37).
- **Music genre.** Accuracy was roughly human-level, and the pattern of errors correlated with human confusions. This task showed the largest mismatches.
- **Brain fit.** Across auditory cortex, the trained network explained 69.9% of the variance in fMRI responses to 165 natural sounds from 8 participants. The spectrotemporal filter baseline explained 55.1%. The same architecture with random weights did worse than both.
- **Hierarchy.** Primary (tonotopic) cortex was best predicted by intermediate layers. Beyond the core, deeper layers gave the best predictions, although pitch- and music-selective voxels were predicted about equally well by intermediate and deep layers.

## Limitations

- **Imperfect match.** The network matched human genre judgements only partly, which the authors connect to listeners' cultural experience.
- **Unexplained variance.** The network did not explain all reliable voxel variance. The model is feedforward, with no recurrence or feedback.
- **Weak evidence for the primate layout.** The data did not clearly show the three-stage core, belt and parabelt hierarchy seen in non-human primates.
- **Learning.** The network was trained on more than two and a half million labelled examples per task, far more than people appear to need to learn words, and its learning procedure differs from biological learning.
- **Measurement.** fMRI has limited temporal resolution, and the model has no realistic temporal dynamics or behavioural state.

## Connections

- **Visual counterpart**: the same logic, a task-trained network compared with cortex, was first tested for vision in [Performance-Optimised Networks (Yamins et al., 2014)](../../visual-perception/yamins-2014/index.md).
- **Baseline**: the spectrotemporal model it is compared with is the other method on this topic. See [Multiresolution Spectrotemporal Model (Chi et al., 2005)](../chi-2005/index.md).
- **NeuroAI**: the auditory row of the task-optimised paradigm is on the [NeuroAI](../../neuroai/index.md) page.
- **Speech**: the word task links to the speech models in [Speech & Audio](../../../theory/models/speech/index.md), and to the cortical speech pathways in [Hickok & Poeppel's dual-stream model](../../language-in-brain/hickok-poeppel-2007/index.md).

## Applications

- **Testing auditory hypotheses**: researchers can ask which tasks produce a given cortical layout, and which features are needed to match human errors.
- **Task-driven accounts**: human-like errors emerged in the network without training on human errors. This supports the view that some listening behaviour follows from the task itself, though it remains a research claim that needs further tests.

## Open questions

- **Which tasks?** Kell et al. (2018) used two tasks. Whether other tasks, such as sound localisation or speaker identity, would change the layers that match cortex is unknown.
- **Feedback and attention.** The feedforward design leaves out feedback and attention, which may explain the unexplained variance.
- **Cultural effects.** The genre mismatch suggests that some human listening depends on experience that the training data did not include.

## References

### Seminal papers

- Kell, A. J. E., Yamins, D. L. K., Shook, E. N., Norman-Haignere, S. V. & McDermott, J. H. (2018). A task-optimized neural network replicates human auditory behavior, predicts brain responses, and reveals a cortical processing hierarchy. *Neuron*. https://doi.org/10.1016/j.neuron.2018.03.044 — The original paper. It trains a network on word and genre tasks and compares it with human behaviour and auditory cortex fMRI.
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — The visual precursor of the task-optimised approach, which predicts neural responses in higher visual cortex.
- Chi, T., Ru, P. & Shamma, S. A. (2005). Multiresolution spectrotemporal analysis of complex sounds. *Journal of the Acoustical Society of America*. https://doi.org/10.1121/1.1945807 — The spectrotemporal baseline that this study compares the network with, which proposes a unified multiresolution representation.

### Surveys and textbooks

- Hickok, G. & Poeppel, D. (2007). The cortical organization of speech processing. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2113 — Background on the cortical speech pathways that the speech branch may resemble.
- Robles, L. & Ruggero, M. A. (2001). Mechanics of the mammalian cochlea. *Physiological Reviews*. https://doi.org/10.1152/physrev.2001.81.3.1305 — Reviews cochlear mechanics: travelling waves, tonotopic place coding and outer hair cell amplification, the biology behind cochlea-like inputs.
- Rauschecker, J. P. & Scott, S. K. (2009). Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*. https://doi.org/10.1038/nn.2331 — Reviews maps and streams in auditory cortex, drawing on nonhuman primate work and its bearing on human speech processing.
