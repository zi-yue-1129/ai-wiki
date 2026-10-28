---
status: draft
last_reviewed: 2026-10-28
---

# Reach and grasp with a neurally controlled arm (Hochberg et al., 2012)

A decoder turns motor-cortex spiking activity into movements of a robotic arm.

## Problem

Can a person with tetraplegia use a robotic arm to reach and grasp objects, using signals from their own motor cortex?

## Core idea

Intracortical microelectrode arrays record spiking activity from motor cortex. A decoder maps that activity to the arm's movement, and the participant corrects the movement from visual feedback in a closed loop.

## Equation or algorithm


  1. Record spiking activity of motor cortex neurons while the participant attempts movements.
  2. Fit a decoder from that activity to the arm's velocity or position.
  3. Run the decoder in closed loop, so the participant can correct the arm from what they see.

## Results

Participants with tetraplegia reached for and grasped objects with the robotic arm, showing that decoded neural signals can control a multi-joint limb.

## Limitations

The study involved a small number of participants. The arm moved more slowly than a natural limb, and the stability of the implants over years and the need for recalibration remain open problems.

## Connections

- Parent topic: [Brain-Computer Interfaces & Neural Decoding](../index.md)
- Other method on this topic: [Speech Neuroprosthesis](../speech-neuroprosthesis/index.md)

## References

### Seminal papers

- Wolpaw, J. R., Birbaumer, N., McFarland, D. J., Pfurtscheller, G. & Vaughan, T. M. (2002). Brain–computer interfaces for communication and control. *Clinical Neurophysiology*. https://doi.org/10.1016/S1388-2457(02)00057-3 — Early review defining the BCI as a system that translates brain signals into commands, with a focus on communication for people with severe disabilities.
- Hochberg, L. R., et al. (2006). Neuronal ensemble control of prosthetic devices by a human with tetraplegia. *Nature*. https://doi.org/10.1038/nature04970 — Shows that a person with tetraplegia can control a cursor and other devices with an intracortical array.
- Hochberg, L. R., et al. (2012). Reach and grasp by people with tetraplegia using a neurally controlled robotic arm. *Nature*. https://doi.org/10.1038/nature11076 — Shows that participants can reach for and grasp objects with a robotic arm controlled from motor cortex.
- Willett, F. R., et al. (2023). A high-performance speech neuroprosthesis. *Nature*. https://doi.org/10.1038/s41586-023-06377-x — Decodes attempted speech from speech motor cortex at high rates, using a recurrent network and a language model.
- Moses, D. A., et al. (2021). Neuroprosthesis for Decoding Speech in a Paralyzed Person with Anarthria. *New England Journal of Medicine*. https://doi.org/10.1056/NEJMoa2027540 — Decodes sentences from brain activity recorded with electrocorticography in a person who cannot speak.
