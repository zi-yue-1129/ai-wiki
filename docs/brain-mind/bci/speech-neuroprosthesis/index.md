---
status: complete
last_reviewed: 2026-10-28
---

# Speech neuroprosthesis (Willett et al., 2023)

A recurrent neural network decodes phoneme probabilities from speech-related motor cortex, and a language model turns them into text. In one participant with amyotrophic lateral sclerosis, the system decoded attempted speech at 62 words per minute.

## Overview

Some people lose the ability to speak intelligibly. Amyotrophic lateral sclerosis (ALS) and brainstem stroke are two causes. Their brains can still produce the signals for speech, even though the muscles of the mouth, tongue and larynx no longer carry out the movement. A **speech brain-computer interface** (BCI) tries to read those signals and turn them into words. The aim is communication at a rate that approaches conversation. The abstract of the study compares its result with about 160 words per minute, the approximate speed of natural conversation.

This page covers the study by Willett and colleagues, which records from intracortical microelectrode arrays and decodes attempted speech into text. The [BCI overview](../index.md) covers the other recording methods and the history of the field. The [neural reach-and-grasp](../neural-reach-and-grasp/index.md) study uses the same kind of recordings to control a limb rather than to produce speech.

## Key concepts

- **Speech motor cortex**: the cortical areas that plan the movements of the lips, tongue, jaw and larynx. The paper decodes from the ventral premotor cortex (area 6v).
- **Phoneme**: the smallest unit of sound that distinguishes one word from another, such as the /p/ in "pat" and the /b/ in "bat".
- **Intracortical microelectrode array**: a small implanted chip with many electrodes that record the spiking activity of nearby neurons.
- **Recurrent neural network (RNN)**: a network whose hidden state carries information from earlier inputs forward, so that it can use the history of a signal. See [Recurrent Neural Networks](../../../theory/models/rnn/index.md).
- **Language model**: a model that assigns probabilities to word sequences, so that a decoder can prefer sentences that are likely in the language.
- **Word error rate (WER)**: the share of words that the decoder gets wrong, after aligning the output with the intended sentence.

## Problem

Can a person who can no longer speak intelligibly communicate quickly by decoding the neural activity that goes with speech? The authors note that earlier demonstrations had not reached accuracies high enough for unconstrained sentences from a large vocabulary. A useful system therefore has to handle sentences the user chooses, not a fixed list of commands, and it must do so with enough accuracy to be practical.

## Core idea

The pipeline has three stages, described in the study's text.

First, intracortical arrays record the spiking activity of neurons in the speech-related motor cortex while the participant tries to speak. Second, a recurrent network with gated recurrent units reads this activity over time. At each 80-millisecond time step, it outputs the probability that each phoneme is being spoken. Third, these probabilities are combined with a language model to infer the most probable sequence of words.

The separation of roles matters. The network handles the noisy mapping from neural activity to sounds, and the language model supplies knowledge of which word sequences are plausible. Errors that the neural decoder makes can then be corrected by the language model, as in speech recognition from audio.

## Equation or algorithm

The steps below follow the pipeline described in the study. The exact network layout and the language-model combination are given in the paper's methods, which this page does not reproduce in full.

A recurrent network keeps a hidden state $\mathbf{h}_t$ that summarises the signal so far. In generic form, with neural features $\mathbf{x}_t$ for time step $t$:

$$\mathbf{h}_t = f(\mathbf{h}_{t-1}, \mathbf{x}_t), \qquad \mathbf{p}_t = \operatorname{softmax}(W\mathbf{h}_t + \mathbf{b})$$

Here $\mathbf{p}_t$ is the vector of phoneme probabilities for the time step, and $f$ is the recurrent update. The procedure is:

1. Record spiking activity from the speech-related motor cortex while the participant attempts to speak.
2. Pass the neural features through the recurrent network, which outputs phoneme probabilities at each 80-millisecond step.
3. Combine the phoneme probabilities with a language model to find the most probable word sequence.
4. Output the resulting text.

The study used two language models of different sizes. The large-vocabulary model has 125,000 words and is a trigram model, which estimates each word from the two words before it. A smaller model with 50 words was also used.

## Results

The abstract reports results with two vocabulary sizes. On a 50-word vocabulary, the participant achieved a 9.1% word error rate, which the authors describe as 2.7 times fewer errors than the previous state-of-the-art speech BCI. On a 125,000-word vocabulary, the word error rate was 23.8%, which the authors describe as the first successful demonstration, to their knowledge, of large-vocabulary decoding.

The participant's attempted speech was decoded at 62 words per minute, which the authors report as 3.4 times the previous record and close to the speed of natural conversation, about 160 words per minute. The abstract also reports that the neural code for speech is spatially intermixed, so that accurate decoding is possible from a small region of cortex.

These numbers come from one participant with ALS and a single study. They are copied from the abstract and should be read with the limitations below.

## Limitations

- **One participant.** The study is based on a single participant, who was part of a pilot clinical trial. The authors state that the results must be confirmed in additional participants.
- **Still slower than speech.** 62 words per minute is far faster than earlier record speeds, but the abstract places it below the speed of natural conversation.
- **Large vocabulary is still error-prone.** A word error rate of 23.8% means that about one word in four is wrong on the 125,000-word vocabulary. The authors present this as the first successful large-vocabulary demonstration, not as a solved problem.
- **Dependence on the language model.** Decoding quality depends on the language model. The paper's large-vocabulary result uses a fixed trigram model, so the result depends on that model's choice.
- **Long-term behaviour.** The study does not show how stable the decoder is over years of use.

## Key methods

- [Neural Reach and Grasp (Hochberg et al., 2012)](../neural-reach-and-grasp/index.md): uses intracortical recordings to control a robotic arm instead of decoding speech, and does not use a language model.
- Speech synthesis from ECoG (Anumanchipalli, Chartier & Chang, 2019): records from electrodes on the cortical surface and decodes articulatory movements into audible speech, rather than decoding text.
- Other speech-decoding approaches differ in their recording method, output (text or sound), and whether a language model is used. The comparison above is limited to the methods whose sources are listed on this page.

## Connections

- Parent topic: [Brain-Computer Interfaces & Neural Decoding](../index.md)
- Other method on this topic: [Neural Reach and Grasp](../neural-reach-and-grasp/index.md)
- [Language in the Brain](../../language-in-brain/index.md): the speech and language networks of the brain that the recorded signals come from.
- [Recurrent Neural Networks](../../../theory/models/rnn/index.md): the network family used for the decoder, which carries information through time.
- [Speech models](../../../theory/models/speech/index.md) and [Large Language Models](../../../theory/models/llm/index.md): the speech-recognition and language-model ideas that the decoder borrows.
- [Neuroimaging & Recording Methods](../../neuroimaging-methods/index.md): the trade-off between electrodes that sit inside the cortex and recordings that do not.

The brain-side link is the speech motor cortex. The abstract also notes that a detailed articulatory representation of phonemes persists years after paralysis, which the authors describe as encouraging for speech BCIs. This page reports that statement without testing it further.

## Applications

- **Communication aids**: restoring written or spoken communication for people with ALS or other conditions that take away speech, as the study demonstrates.
- **Assistive speech output**: Anumanchipalli and colleagues show that cortical recordings can drive audible speech synthesis, which is a different output route for the same kind of problem.
- **Clinical research**: the study is a step toward clinical speech BCIs, with decoders that have to be checked in more participants before any routine use.

## Open questions

- **Generalisation.** Will the same accuracy hold in other participants, with different injuries, implant locations and speaking habits?
- **Speed and accuracy.** How much of the gap between 62 words per minute and natural speech comes from the decoder, and how much from the language model?
- **Stability.** How long can the decoder work without retraining, and how is performance affected as the recordings change over time?
- **Attempted versus imagined speech.** Whether a similar system could work for people who do not produce any movement, and how this would change the signals.

## References

### Seminal papers

- Willett, F. R., et al. (2023). A high-performance speech neuroprosthesis. *Nature*. https://doi.org/10.1038/s41586-023-06377-x — The study this page describes: speech-to-text decoding from intracortical arrays in a participant with ALS, using a recurrent network and a language model.
- Hochberg, L. R., et al. (2012). Reach and grasp by people with tetraplegia using a neurally controlled robotic arm. *Nature*. https://doi.org/10.1038/nature11076 — The companion study that uses the same kind of intracortical recording to control a robotic arm in people with tetraplegia.
- Anumanchipalli, G. K., Chartier, J. & Chang, E. F. (2019). Speech synthesis from neural decoding of spoken sentences. *Nature*. https://doi.org/10.1038/s41586-019-1119-1 — Decodes cortical activity from surface electrodes into articulatory movements and then into audible speech.

### Surveys and textbooks

- Nicolas-Alonso, L. F. & Gomez-Gil, J. (2012). Brain Computer Interfaces, a Review. *Sensors*. https://doi.org/10.3390/s120201211 — Reviews BCI systems step by step, covering signal acquisition, preprocessing, feature extraction, classification and the control interface.
- Chaudhary, U., Birbaumer, N. & Ramos-Murguialday, A. (2016). Brain–computer interfaces for communication and rehabilitation. *Nature Reviews Neurology*. https://doi.org/10.1038/nrneurol.2016.113 — Reviews BCIs for communication and rehabilitation, with invasive and noninvasive recording and patient groups such as ALS, stroke and spinal cord injury.
