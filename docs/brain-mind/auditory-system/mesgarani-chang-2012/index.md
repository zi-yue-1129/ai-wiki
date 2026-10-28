---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/speech
tags:
- neuroscience
- perception
- language
aliases:
  - Mesgarani & Chang 2012
  - 注意說話者的解碼
  - Attended-speaker decoding
  - Cocktail party neural decoding
---

# Attended-Speaker Decoding from the Cortex (Mesgarani & Chang 2012)

Mesgarani and Chang (2012) recorded cortical activity while listeners heard two talkers at once, and reported that the cortex represents the attended talker more strongly than the ignored one. Their method reconstructs the speech a listener attends to from the neural signal, so selective attention in a mixture becomes measurable. This page is part of [Hearing and the Auditory System](../index.md), which gives the overview; this page covers the method and its evidence.

## Overview

Following one talker in a crowd is the cocktail-party problem. Cherry (1953) ran early experiments with two simultaneous speech signals, which made the problem a subject for controlled study.[^1] The neuroscience question was whether the brain's representation of the attended talker differs from its representation of the other.

Mesgarani and Chang addressed it by recording the cortex directly. They used electrodes on the surface of the superior temporal gyrus, an area known to process speech, in patients being monitored for epilepsy surgery. Participants heard mixtures of two talkers and were told which one to attend. The recordings were then analysed to see which talker the neural signal reflected.

## Key concepts

- **Selective attention**: the ability to focus processing on one source among several.
- **Electrocorticography (ECoG)**: recording from electrodes on the exposed cortical surface. Its signal is more localised than a scalp recording.
- **Decoder**: a model that maps neural activity to a stimulus feature. A linear decoder is the simplest form.
- **Speech mixture**: two talkers' speech added together, so their spectrograms overlap in time and frequency.

## How it works

1. Record ECoG over the superior temporal gyrus while a participant hears a single talker. Use the high-frequency part of the neural signal, which tracks local population activity.
2. Fit a linear decoder that maps lagged neural activity to the speech spectrogram. With $r_k(t)$ the activity at electrode $k$ and $S_f(t)$ the spectrogram at frequency $f$, the model is $\hat{S}_f(t) = \sum_{k,\tau} w_{k,\tau,f}\, r_k(t-\tau)$, with the weights fitted by regression.
3. Present two talkers at once, with the participant attending to one.
4. Apply the decoder to the neural activity recorded during the mixture, producing a reconstructed spectrogram.
5. Compare the reconstruction with the spectrograms of the attended and the ignored talker. The closer match shows which talker dominates the cortical representation.

The decoder is trained on single talkers, so any preference for the attended talker must come from the neural signal during the mixture.

## Results

The paper reports that the reconstruction during a mixture follows the attended talker more closely than the ignored one, so the cortical representation of the mixture is dominated by the attended talker. The figures and statistics are in the paper. This page describes the result qualitatively.

The result turns a behavioural idea into a measurable change in cortical activity, and it gives a direct way to ask where in the pathway selection happens.

## Limitations

- **Small sample.** The recordings come from a few patients, and electrode positions were set for clinical reasons, not for the research question.
- **Controlled conditions.** The decoder was trained on single talkers, and the mixtures were fixed and attention was cued explicitly. Generalisation to other voices, levels and natural listening is untested here.
- **Readout, not mechanism.** The method shows which talker is represented, not how attention changes the representation.

## Open questions

- **Does attention enhance the attended talker, suppress the other, or both?** Answering this needs a neutral baseline, which the design does not provide.
- **Where in the pathway does selection happen?** The recordings are from cortex, downstream of the brainstem. Whether selection already occurs earlier is open.
- **Can the readout scale to natural settings?** Many talkers, varying noise and everyday listening remain to be tested.

## References

### Seminal papers

- Mesgarani, N. & Chang, E. F. (2012). Selective cortical representation of attended speaker in multi-talker speech perception. *Nature*. https://doi.org/10.1038/nature11020 — Records cortical activity during talker mixtures and shows that the attended talker dominates the representation.
- Cherry, E. C. (1953). Some Experiments on the Recognition of Speech, with One and with Two Ears. *The Journal of the Acoustical Society of America*. https://doi.org/10.1121/1.1907229 — Early experiments on recognising speech when two speech signals are presented together.
- Mesgarani, N., Cheung, C., Johnson, K. & Chang, E. F. (2014). Phonetic Feature Encoding in Human Superior Temporal Gyrus. *Science*. https://doi.org/10.1126/science.1245994 — Records speech responses from the superior temporal gyrus and shows how they encode phonetic features.

### Surveys and textbooks

- Mattys, S. L., Davis, M. H., Bradlow, A. R. & Scott, S. K. (2012). Speech recognition in adverse conditions: A review. *Language and Cognitive Processes*. https://doi.org/10.1080/01690965.2012.705006 — Reviews how listeners recognise speech in noise and which processes compensate.
- Rauschecker, J. P. & Scott, S. K. (2009). Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*. https://doi.org/10.1038/nn.2331 — Argues from primate work that auditory cortex has anterior and posterior streams.

### Articles and documentation

- Wang, D. & Chen, J. (2018). Supervised Speech Separation Based on Deep Learning: An Overview. arXiv. https://arxiv.org/abs/1708.07524 — Surveys deep-learning methods that select a target talker from background interference.

[^1]: Cherry's experiments presented two speech signals at once, and different signals to the two ears, and interpreted listeners' responses statistically.
