---
status: draft
last_reviewed: 2026-10-28
---

# Speech neuroprosthesis (Willett et al., 2023)

A recurrent network decodes phoneme probabilities from speech motor cortex to produce text.

## Problem

Can a person who cannot speak communicate quickly by decoding the neural activity that goes with speech?

## Core idea

An intracortical array records speech motor cortex. A recurrent neural network decodes phoneme probabilities from the activity in each time window, and a language model turns those probabilities into the most likely word sequence.

## Equation or algorithm


  1. Record neural activity while the participant attempts to speak.
  2. Decode phoneme probabilities with a recurrent network.
  3. Use a language model to choose the most likely word sequence.

## Results

The paper reports decoding attempted speech at rates of tens of words per minute, with large vocabularies.

## Limitations

The results come from a small number of participants and need replication over longer periods. The decoder is trained on each participant's recordings.

## Connections

- Parent topic: [Brain-Computer Interfaces & Neural Decoding](../index.md)
- Other method on this topic: [Neural Reach and Grasp](../neural-reach-and-grasp/index.md)

## References

### Seminal papers

- Wolpaw, J. R., Birbaumer, N., McFarland, D. J., Pfurtscheller, G. & Vaughan, T. M. (2002). Brain–computer interfaces for communication and control. *Clinical Neurophysiology*. https://doi.org/10.1016/S1388-2457(02)00057-3 — Early review defining the BCI as a system that translates brain signals into commands, with a focus on communication for people with severe disabilities.
- Hochberg, L. R., et al. (2006). Neuronal ensemble control of prosthetic devices by a human with tetraplegia. *Nature*. https://doi.org/10.1038/nature04970 — Shows that a person with tetraplegia can control a cursor and other devices with an intracortical array.
- Hochberg, L. R., et al. (2012). Reach and grasp by people with tetraplegia using a neurally controlled robotic arm. *Nature*. https://doi.org/10.1038/nature11076 — Shows that participants can reach for and grasp objects with a robotic arm controlled from motor cortex.
- Willett, F. R., et al. (2023). A high-performance speech neuroprosthesis. *Nature*. https://doi.org/10.1038/s41586-023-06377-x — Decodes attempted speech from speech motor cortex at high rates, using a recurrent network and a language model.
- Moses, D. A., et al. (2021). Neuroprosthesis for Decoding Speech in a Paralyzed Person with Anarthria. *New England Journal of Medicine*. https://doi.org/10.1056/NEJMoa2027540 — Decodes sentences from brain activity recorded with electrocorticography in a person who cannot speak.
