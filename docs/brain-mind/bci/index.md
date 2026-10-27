---
related:
- applications/healthcare
- society/ethics
---

# Brain-Computer Interfaces & Neural Decoding

A **brain-computer interface (BCI)** records brain activity, decodes it, and uses it to control a device or communicate — or delivers signals back into the nervous system. AI decoders have driven most recent progress.

## Recording modalities

| Modality | Invasiveness | Signal quality | Typical use |
|---|---|---|---|
| EEG | Non-invasive | Low spatial resolution, noisy | P300 spellers, SSVEP, motor imagery, neurofeedback, consumer headsets |
| fNIRS | Non-invasive | Slow hemodynamics | Research, simple communication |
| MEG / OPM-MEG | Non-invasive | Good temporal resolution; costly (OPM sensors are wearable) | Research decoding |
| fMRI | Non-invasive | Good spatial, slow | Research decoding of images and language |
| ECoG / stereo-EEG | Surgical, on or in the brain | High quality | Speech decoding, epilepsy monitoring |
| Endovascular (Stentrode) | Via blood vessels | Moderate | Texting and computer control |
| Intracortical microelectrode arrays (Utah array, Neuralink, Paradromics, etc.) | Penetrating | Single-neuron resolution | Cursor, robotic arm, handwriting, speech |

## Milestones

| Year | Achievement |
|---|---|
| 1970s | Vidal coins "brain-computer interface" |
| 1988 | P300 speller (Farwell & Donchin) |
| 2006 | BrainGate: a person with tetraplegia controls a cursor with an intracortical array (Hochberg et al.) |
| 2012 | People control robotic arms to reach and grasp |
| 2016–2021 | Restoration of touch via intracortical microstimulation |
| 2021 | Handwriting BCI: imagined handwriting decoded at ~90 characters/min (Willett et al., *Nature*) |
| 2023 | Speech neuroprostheses at ~62–78 words/min with large vocabularies, including a digital avatar voice (Willett et al.; Metzger et al., *Nature*) |
| 2023 | "Digital bridge" between brain and spinal cord restores walking (Lorach et al., *Nature*) |
| 2024 | Speech BCI with ~97% accuracy using a personalised synthesised voice (Card et al., *NEJM*); first Neuralink human implants |
| 2025 | Near-real-time streaming brain-to-voice synthesis with low latency (Littlejohn et al.; Wairagkar et al.) |

## What AI contributes

- **Sequence models** (RNNs, Transformers) map neural activity to phonemes, characters or motor commands
- **Language models** correct decoding errors — the same trick as in speech recognition
- **Self-supervised pre-training** across sessions and people (neural foundation models such as POYO and NDT variants) reduces recalibration
- **Generative models** reconstruct images and sound from brain activity
- **Closed-loop adaptation** handles non-stationary recordings

## Decoding perception and thought (non-invasive)

- **Images from fMRI**: Stable Diffusion conditioned on brain activity reconstructs viewed images (Takagi & Nishimoto, 2023); MindEye and successors improved fidelity using the Natural Scenes Dataset
- **Language from fMRI**: semantic decoders reconstruct the gist of heard or imagined stories (Tang, LeBel, Jain & Huth, 2023, *Nature Neuroscience*) — they required the participant's cooperation and extensive per-person training data
- **MEG decoding** of images and speech in real time (Meta AI, 2023)

!!! warning "Not mind reading"
    Current non-invasive decoders are subject-specific, need hours of calibration, reconstruct semantic gist rather than exact thoughts, and fail when participants resist. Still, rapid progress motivates **neural privacy** protections.

## Clinical and consumer applications

- Communication for people with ALS, locked-in syndrome, brainstem stroke
- Motor restoration: robotic arms, functional electrical stimulation, spinal-cord bridges
- Sensory restoration: cochlear implants (the most successful neural interface), retinal and cortical visual prostheses
- **Deep brain stimulation** for Parkinson's disease, with adaptive (closed-loop) DBS approved in some regions
- Neurofeedback (evidence quality varies), sleep and attention monitoring with consumer EEG

## Ethics: neurorights

- **Mental privacy**: neural data can reveal health conditions and mental states
- **Cognitive liberty and identity**: stimulation may change mood or personality
- **Agency**: who is responsible for actions mediated by a decoder?
- **Equity and abandonment**: what happens when a company stops supporting an implant?
- **Regulation**: Chile amended its constitution to protect neural data (2021); Colorado and California added neural data to privacy laws (2024); UNESCO adopted a Recommendation on the Ethics of Neurotechnology (2025)

## Resources

- Wolpaw & Wolpaw, *Brain-Computer Interfaces: Principles and Practice*
- [BCI Society](https://bcisociety.org/)
- [MNE-Python](https://mne.tools/), [MOABB](https://moabb.neurotechx.com/) (benchmarks), [BrainFlow](https://brainflow.org/)
- [NeuroTechX](https://neurotechx.com/) community
- Yuste et al. (2017), "Four ethical priorities for neurotechnologies and AI", *Nature*
