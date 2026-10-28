---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/language-in-brain
tags:
- neuroscience
- methods
aliases:
  - Ogawa 1990
  - BOLD fMRI
  - Blood-oxygen-level-dependent contrast
---

# BOLD fMRI (Ogawa et al. 1990)

Ogawa et al. (1990) showed that magnetic resonance contrast depends on blood oxygenation. Deoxygenated haemoglobin changes the local magnetic signal, so an image can reflect the oxygen state of the blood in a region. Because active neurons draw on local blood supply, these changes track neural activity, and this is the basis of the blood-oxygen-level-dependent (BOLD) signal used in functional MRI.

This page is part of [Neuroimaging and Recording Methods](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Before this work, magnetic resonance could image the brain's structure but not its activity. Researchers wanted a non-invasive signal that changed with neural activity, and that could be measured in a living person without injected agents.

## The approach

The paper used magnetic resonance imaging to measure how the contrast changed with blood oxygenation, under controlled conditions in animals. It showed that the signal depends on the oxygen content of the blood, which gave a route to imaging local changes in activity.

The steps of the method, as later used in functional MRI, are:

1. Acquire repeated magnetic resonance images of the brain while a person performs a task or receives a stimulus.
2. Measure the BOLD contrast in each voxel over time.
3. Model the signal as a delayed, smoothed response to the task, because the blood response lags neural activity by a few seconds.
4. Compare the response across conditions to find regions that change with the task.

Step 3 is where interpretation matters. The delay and shape of the blood response mean the signal is an indirect, slow measure of neural activity.

## Results

The 1990 paper reports that magnetic resonance contrast changes with blood oxygenation, with the effect shown in images under controlled conditions. The results are qualitative in the summary used for this page. Check the full text before quoting figures.

## Limitations

- The BOLD signal is indirect. It reflects changes in blood oxygen, which depend on metabolism, blood flow and vascular response, not on spikes alone.
- The response is slow, with a lag of seconds, so fast neural events are blurred.
- Vascular differences between people and between regions can change the signal without a change in neural activity.

## Connections

- **Coupling to neurons**: whether the BOLD signal follows spiking or synaptic activity is tested on [Logothetis et al. 2001](../fmri-electrophysiology/index.md).
- **Language**: fMRI localisation of language regions, including individual-level methods, is in [Fedorenko et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923), and the language studies that use it are on [Language in the Brain](../../language-in-brain/index.md).
- **Neuroscience background**: the blood supply and neural cells behind the signal are in [Neuroscience Basics](../../neuroscience/index.md).

## Open questions

- **How strongly does the BOLD signal relate to neural spiking?** The coupling depends on the region and the task, and the relation is still being mapped.
- **Can blood-based signals reach finer timing?** The lag of the haemodynamic response limits fMRI, and faster imaging approaches are under study.

## References

### Seminal papers

- Ogawa, S., Lee, T.-M., Kay, A. R. & Tank, D. W. (1990). Brain magnetic resonance imaging with contrast dependent on blood oxygenation. *Proceedings of the National Academy of Sciences*. https://pmc.ncbi.nlm.nih.gov/articles/PMC55275 — Shows that magnetic resonance contrast depends on blood oxygenation, the basis of BOLD fMRI.
- Logothetis, N. K., Pauls, J., Augath, M., Trinath, T. & Oeltermann, A. (2001). Neurophysiological investigation of the basis of the fMRI signal. *Nature*. https://doi.org/10.1038/35084005 — Relates the BOLD signal to electrical activity and spiking.
- Fedorenko, E., Hsieh, P.-J., Nieto-Castañón, A., Whitfield-Gabrieli, S. & Kanwisher, N. (2010). New method for fMRI investigations of language: defining ROIs functionally in individual subjects. *Journal of Neurophysiology*. https://pmc.ncbi.nlm.nih.gov/articles/PMC2934923 — An individual-level fMRI localiser that uses the BOLD signal.

### Articles and primary research

- Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B. & Fedorenko, E. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Uses fMRI responses to sentences as one of its two neural datasets.
- Goldstein, A., Zada, Z., Buchnik, E., Schain, M., Price, A., et al. (2022). Shared computational principles for language processing in humans and deep language models. *Nature Neuroscience*. https://doi.org/10.1038/s41593-022-01026-4 — Compares a faster electrical method, electrocorticography, with the slower blood-based signal.
