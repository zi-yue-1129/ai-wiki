---
status: complete
last_reviewed: 2026-10-28
---

# Reach and grasp with a neurally controlled arm (Hochberg et al., 2012)

A decoder turns motor-cortex activity recorded from implanted electrodes into movements of a robotic arm, and two people with long-standing tetraplegia used it to reach for and grasp objects.

## Overview

Spinal cord injury, brainstem stroke and motor neuron diseases such as amyotrophic lateral sclerosis (ALS) can leave a person unable to move their limbs while much of the brain is still intact. The motor cortex, the part of the cerebral cortex that plans and sends movement commands, may keep producing those commands even when the route to the muscles is cut. A brain-computer interface (BCI) tries to read the commands directly and use them to drive a device instead. The [BCI overview](../index.md) covers the recording methods and the history of the field.

This page covers one landmark study. Hochberg and colleagues showed that people with long-standing tetraplegia could use signals from their own motor cortex to control a multi-joint robotic arm, and use it to reach for and grasp objects. The study is a proof of feasibility: it asks whether the approach can work at all in people, not whether it is ready for daily use.

## Key concepts

- **Tetraplegia**: paralysis that affects all four limbs and usually the trunk, most often after an injury to the cervical spinal cord.
- **Motor cortex**: the region of the cerebral cortex that plans and sends commands for voluntary movement. See [Neuroscience Basics](../../neuroscience/index.md).
- **Microelectrode array**: a small implanted chip with many electrodes that records the activity of neurons close to them.
- **Spiking activity**: the brief electrical impulses, called action potentials, that neurons send. Counting spikes in short time windows gives a signal a computer can use.
- **Decoder**: a mathematical mapping from recorded neural activity to a control signal, such as the velocity or position of the arm.
- **Closed loop**: a setup in which the user sees the effect of the decoded movement and can adjust what they try next.

## Problem

Can a person who has been paralysed for years use signals from their own motor cortex to control a robotic arm that reaches and grasps objects?

The problem has three parts. First, a robotic arm with several joints moves in three dimensions, so the decoder must control several degrees of freedom at once rather than a single pointer. Second, the recordings come from a limited set of neurons, so the signal is noisy and incomplete, and the decoder has to make the most of it. Third, the arm has to be controlled well enough to complete a task that a person would actually want to do, such as bringing a drink to the mouth.

## Core idea

Hochberg and colleagues recorded signals from motor-cortex neurons in two participants with long-standing tetraplegia. A decoder converted these signals into commands for a robotic arm. The participants then used the arm to move through a wide three-dimensional space, and one of them used it to drink from a bottle. In short, the neural activity that once drove the person's own limbs was re-routed to drive an external device.

The abstract of the paper states that the robotic reaching and grasping was slower and less accurate than an able-bodied person's movement. The claim the paper makes is that a small neural sample can already support useful control of a complex device. That is a claim about feasibility and about the kind of control possible, not about speed.

## Equation or algorithm

The paper's exact decoder is described in its methods section, which this page does not reproduce. The general scheme behind such decoders is a regression from neural activity to movement. As an illustration, a linear decoder predicts the arm's velocity from the number of spikes in each time bin:

$$\mathbf{v}_t = W\,\mathbf{x}_t + \mathbf{b}$$

Here $\mathbf{x}_t$ is the vector of spike counts from all recorded neurons in time bin $t$, $\mathbf{v}_t$ is the commanded arm velocity, and $W$ and $\mathbf{b}$ are parameters fitted from recorded data. The procedure runs as follows:

1. Record spiking activity from motor-cortex neurons while the participant tries to make movements.
2. Count spikes in short time bins to build the feature vector $\mathbf{x}_t$ for each bin.
3. Fit the decoder parameters so that the decoded velocity matches the movement the participant intended.
4. Run the decoder on the robotic arm, so the participant sees each movement and keeps adjusting their attempts.

Step 4 is what makes the system closed loop: the participant's view of the arm is part of the control.

## Results

According to the paper's abstract, two people with long-standing tetraplegia controlled the robotic arm through a wide three-dimensional space. One of them, implanted several years earlier, used the arm to drink from a bottle. The reaching and grasping were slower and less accurate than an able-bodied person's movements.

The paper's main result is therefore qualitative: people with tetraplegia can gain useful multidimensional control of a complex device from a small sample of motor-cortex neurons. This page gives no numbers beyond the qualitative statements above, because the figures were not read for this version.

## Limitations

- **Two participants.** The results show that the approach can work in these people. They say little about how the approach performs across the wide range of people with tetraplegia.
- **Speed and accuracy.** The arm moved more slowly and less accurately than a natural limb, so the device is not yet a substitute for everyday movement.
- **Long-term use.** The sources read for this page do not address how long implanted arrays keep producing usable signals, or how often a decoder must be recalibrated.
- **Scope of the decoder.** Because the paper's decoder details are not reproduced here, the general scheme above should be read as an illustration of the approach rather than the exact method used in the study.

## Key methods

- [Speech Neuroprosthesis (Willett et al., 2023)](../speech-neuroprosthesis/index.md): records the same kind of intracortical signals, but decodes attempted speech and uses a language model to turn decoded sounds into text.
- Speech synthesis from ECoG (Anumanchipalli, Chartier & Chang, 2019): uses electrodes placed on the cortical surface rather than penetrating arrays, and decodes speech sounds rather than controlling a limb.
- Noninvasive BCIs, such as EEG and near-infrared spectroscopy: avoid surgery, but their signals are less precise, as the review by Chaudhary and colleagues (2016) describes.

## Connections

- Parent topic: [Brain-Computer Interfaces & Neural Decoding](../index.md)
- Other method on this topic: [Speech Neuroprosthesis](../speech-neuroprosthesis/index.md)
- [Neuroscience Basics](../../neuroscience/index.md): the motor cortex and the spiking neurons that the arrays record.
- [Computational Neuroscience](../../computational-neuroscience/index.md): neural coding, the idea that patterns of spikes carry information about movement, which a decoder relies on.
- [Neuroimaging & Recording Methods](../../neuroimaging-methods/index.md): compares implanted electrodes with noninvasive recordings, the trade-off that separates the methods above.

The brain-side idea is that a decoder can work only if activity in motor cortex carries information about intended movement. The study tests this idea in people whose limbs no longer respond to that activity.

## Applications

- **Assistive robotics**: restoring reaching and grasping for people with paralysis, as demonstrated in the study.
- **Communication and control**: Chaudhary and colleagues review BCIs for people with ALS, stroke and spinal cord injury.
- **Rehabilitation**: the same review distinguishes assistive control from rehabilitative uses that aim to restore neural function.

## Open questions

- **Scale.** How well do these results carry over to more participants, with different injuries and different implant sites?
- **Performance.** How close can decoded control get to natural speed and precision, and which parts of the gap come from the decoder and which from the arm?
- **Stability.** How long do implanted arrays keep recording usable signals, and how often must the decoder be recalibrated?
- **Noninvasive routes.** Can recordings that avoid surgery support multi-joint control of this kind?

## References

### Seminal papers

- Hochberg, L. R., et al. (2012). Reach and grasp by people with tetraplegia using a neurally controlled robotic arm. *Nature*. https://doi.org/10.1038/nature11076 — The study this page describes: two people with long-standing tetraplegia control a robotic arm through a three-dimensional space using motor-cortex signals.
- Willett, F. R., et al. (2023). A high-performance speech neuroprosthesis. *Nature*. https://doi.org/10.1038/s41586-023-06377-x — A speech-to-text BCI that decodes attempted speech from intracortical arrays using a recurrent network and a language model.
- Anumanchipalli, G. K., Chartier, J. & Chang, E. F. (2019). Speech synthesis from neural decoding of spoken sentences. *Nature*. https://doi.org/10.1038/s41586-019-1119-1 — Decodes cortical activity from electrodes on the surface into articulatory movements and then into audible speech.

### Surveys and textbooks

- Nicolas-Alonso, L. F. & Gomez-Gil, J. (2012). Brain Computer Interfaces, a Review. *Sensors*. https://doi.org/10.3390/s120201211 — Reviews BCI systems step by step, covering signal acquisition, preprocessing, feature extraction, classification and the control interface.
- Chaudhary, U., Birbaumer, N. & Ramos-Murguialday, A. (2016). Brain–computer interfaces for communication and rehabilitation. *Nature Reviews Neurology*. https://doi.org/10.1038/nrneurol.2016.113 — Reviews BCIs for communication and rehabilitation, with invasive and noninvasive recording and patient groups such as ALS, stroke and spinal cord injury.
