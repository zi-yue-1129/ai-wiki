---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/speech
tags:
- neuroscience
- perception
aliases:
  - Formisano 2003
  - 鏡像對稱音調拓撲圖
  - Tonotopic mapping
  - Mirror-symmetric tonotopic maps
---

# Tonotopic Maps from fMRI (Formisano et al. 2003)

Formisano et al. (2003) used functional MRI to map which sound frequencies human primary auditory cortex responds to most strongly. They report mirror-symmetric tonotopic maps, meaning that the frequency gradient reverses direction at a border between two areas. The paper is a landmark of non-invasive auditory mapping.

This page is part of [Hearing and the Auditory System](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## Overview

Tonotopy, the orderly arrangement of neurons by preferred frequency, was established in animals with electrodes placed in the brain. Such recordings are rarely possible in people, so the human auditory cortex needed non-invasive methods. Functional MRI measures blood-oxygen changes that follow neural activity, and so it can show where in the cortex a sound produces a response.

Formisano et al. applied this to primary auditory cortex, the first cortical area to receive input from the thalamus. The question was whether frequency preference changes in an orderly way across this area, and how that order is arranged.

## Key concepts

- **Tonotopy**: a systematic mapping of frequency preference onto position in the brain.
- **Best frequency**: the frequency that drives a given site's response most strongly.
- **Gradient reversal**: a border across which the frequency order runs in the opposite direction. Two areas on either side form a mirror-symmetric pair.
- **BOLD signal**: the blood-oxygen-level-dependent contrast that fMRI measures. It is indirect and slow, following neural activity over several seconds.
- **Voxel**: the small cube of brain tissue that is the unit of fMRI measurement. Each voxel contains many neurons.

## How it works

1. Present sounds that cover a range of frequencies, in sequences that step through the range over time, while the participant lies in the scanner.
2. For each voxel in the auditory cortex, record the BOLD response over the sequence.
3. Estimate each voxel's best frequency. If $\beta_v(f)$ is the response of voxel $v$ to frequency $f$, the best frequency is $f^*_v = \arg\max_f \beta_v(f)$.
4. Plot the best frequency across the cortical surface and look for orderly gradients.
5. Find where a gradient reverses, and check whether the regions on either side form a mirror-symmetric pair of maps.

The last step matters most. A single gradient shows that frequency is ordered across the cortex. A reversal shows that the order forms two maps.

## Results

The paper reports two tonotopic maps in human primary auditory cortex whose frequency gradients run in opposite directions and meet at a shared border. This mirror-symmetric arrangement, rather than a single continuous map, is the main finding. The figures are in the paper, and this page describes the result qualitatively.

Later human mapping work builds on this approach. Moerel et al. (2014) review how tonotopic maps, together with anatomy, are used to identify auditory areas.

## Limitations

- **Indirect signal.** A voxel averages many neurons with different preferences, so the map shows dominant tuning rather than the full range of preferences.
- **Spatial precision.** The location of a border depends on scan resolution and on analysis choices such as the response threshold.
- **Stimulus choice.** Pure tones and frequency sweeps are simpler than everyday sounds. The map describes how frequency is organised, not how speech or music is handled.
- **Individual variation.** The layout of auditory cortex differs between people, so a group map is an approximation for any one person.

## Open questions

- **How many areas are there?** The exact number, extent and borders of human auditory fields are still being refined.
- **How does the cochlea's frequency order relate to the cortical one?** Dallos (1992) describes how outer hair cells sharpen the cochlea's mechanical frequency order, but how that order is carried to the cortical map is less clear.
- **Is tonotopy the main organising principle?** Frequency is not the only property auditory cortex represents, and whether the maps are its main organisation remains open.

## References

### Seminal papers

- Formisano, E., Kim, D.-S., Di Salle, F., van de Moortele, P.-F., Ugurbil, K. & Goebel, R. (2003). Mirror-Symmetric Tonotopic Maps in Human Primary Auditory Cortex. *Neuron*. https://doi.org/10.1016/S0896-6273(03)00669-X — Uses fMRI with frequency-varying sounds to map human primary auditory cortex and reports mirror-symmetric tonotopic maps.
- Kaas, J. H. & Hackett, T. A. (2000). Subdivisions of auditory cortex and processing streams in primates. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.97.22.11793 — Describes how primate auditory cortex is subdivided into areas and processing streams.
- Dallos, P. (1992). The active cochlea. *The Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.12-12-04575.1992 — Reviews the active cochlea, in which outer hair cells amplify the response and sharpen tuning.

### Surveys and textbooks

- Moerel, M., De Martino, F. & Formisano, E. (2014). An anatomical and functional topography of human auditory cortical areas. *Frontiers in Neuroscience*. https://doi.org/10.3389/fnins.2014.00225 — Reviews how anatomy and functional maps, including tonotopy, delineate human auditory areas.
- Rauschecker, J. P. & Scott, S. K. (2009). Maps and streams in the auditory cortex: nonhuman primates illuminate human speech processing. *Nature Neuroscience*. https://doi.org/10.1038/nn.2331 — Argues from primate work that auditory cortex has anterior and posterior streams built on such maps.
