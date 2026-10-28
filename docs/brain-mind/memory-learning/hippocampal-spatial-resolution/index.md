---
status: complete
last_reviewed: 2026-10-28
related:
- brain-mind/memory-learning
- brain-mind/neuroai/grid-like-units
tags:
- neuroscience
- hippocampus
- place cells
- cognitive map
aliases:
  - Hippocampal spatial resolution
  - Place field size
  - 海馬迴的空間解析度
---

# Spatial resolution in the hippocampus

The hippocampus represents space at more than one scale, and the field size of a place cell depends on where it sits, what the animal has experienced, and what it is trying to do. The question is which of these factors allocate resolution, and how much of the variation is structure rather than sampling. The answer is not settled. Some results point to a fixed anatomical gradient, others to learning and reward, and a few show that apparent allocation can come from how the data are counted.

This page is part of [Memory & Learning in the Brain](../index.md). It summarises the evidence in one topic and links to the wider memory and navigation work.

## Overview

A place cell fires when an animal is in a particular region of an environment, and the size of that region is its place field. Entorhinal grid cells, which feed the hippocampus, tile space with fields whose spacing also varies. A recurring idea is that the brain spends more resolution where it matters, so that fields are denser near goals or in areas the animal has learned. This page asks whether the evidence supports that idea, and where it does not.

## Problem

Three questions organise the field:

- Is the scale of spatial representation fixed by anatomy, or does it change with experience?
- Do goals and rewards draw more place fields to themselves?
- Are apparent differences in density real, or do they come from unequal sampling of the environment?

## Findings

### A fixed multi-scale skeleton

Place-field scale grows along the long axis of the hippocampus, from under 1 m dorsally to about 10 m ventrally in rats (Kjelstrup et al., 2008). Grid spacing in the medial entorhinal cortex increases in the same dorsal-to-ventral direction (Brun et al., 2008), and grid cells fall into a small number of discrete modules, with spacing ratios close to 1.4 between neighbours (Stensola et al., 2012). In bats flying through a 200 m tunnel, a single cell can carry fields differing by up to twentyfold, so multi-resolution coding can exist inside one neuron (Eliav et al., 2021).

Some of this structure has been contested. Grid cells in bats show no continuous theta rhythm, which is hard to reconcile with oscillatory-interference models of grid scale (Yartsev et al., 2011). Grid symmetry also depends on the shape of the enclosure (Krupic et al., 2015), so the skeleton is not fully independent of the environment.

### Experience and novelty change field size

Repeated traversal enlarges place fields, and the expansion is asymmetric, extending backward from the direction of travel (Mehta et al., 1997). Grid scale expands in a novel arena and contracts back over tens of minutes (Barry et al., 2012), and it rescales with the size and shape of a familiar environment (Barry et al., 2007). Across seven days, both the number of stably fielded cells and their stability increase (Vaidya et al., 2025). A one-trial mechanism based on dendritic plateau potentials can create a field in a single pass (Bittner et al., 2017).

These findings are often read as tracking novelty and familiarity rather than importance. Grid expansion on first exposure is a signal of novelty, which is different from the value of a goal.

### Goals and rewards over-represent space

Place fields accumulate near a hidden platform in a water maze (Hollup et al., 2001). The entorhinal map shifts toward learned goals (Boccara et al., 2019), and remembered reward locations restructure entorhinal maps so that positional decoding improves near the reward (Butler et al., 2019). Over-representation of the reward zone in CA1 depends on entorhinal input, and inhibiting layer 3 of the entorhinal cortex largely removes it (Grienberger & Magee, 2022). Reorganisation toward a new goal is seen in CA1 but not CA3 (Dupret et al., 2010).

Goal coding also takes a vector form. Cells are tuned to goal direction and distance in bats (Sarel et al., 2017), and place-cell vector fields converge on the goal (Ormond & O'Keefe, 2022). The latter study found that only a small fraction of place cells had goal-directed fields during foraging, which means the goal signal depends on the task.

### Contradicting evidence

When reward delivery is decoupled from the goal location, field centres do not accumulate near the goal, and firing rates in goal zones match control zones (Duvelle et al., 2019). This is the strongest counterexample to a simple reward account, and it also rules out a particular occupancy artefact, because the animal behaves the same way in both conditions.

Terrain shape is another driver that does not depend on where the animal went. Fields elongate parallel to terrain contours, and a boundary-vector-cell model reproduces this (Grieves et al., 2026). The lesson is that field placement can follow structure in the environment as well as the animal's behaviour.

### Measurement

Estimating field density is itself a source of bias. Naive spatial-information estimates are biased upward when samples are few, so the bias is worst where sampling is lowest (Sheintuch et al., 2022). The authors of a study that reported accumulation at preferred locations acknowledged that oversampling could explain part of the effect (Mamad et al., 2017). Any comparison of density across regions or conditions therefore needs an occupancy-matched or surrogate-normalised control.

## Evidence summary

| Claim | Main support | Main limit |
|---|---|---|
| Scale gradient along the long axis | Rat recordings on linear tracks and grid-cell recordings | Bat recordings in a tunnel show a different scale range |
| Experience enlarges fields | Repeated-traversal and novelty studies | Expansion is reported on first exposure, which may reflect novelty rather than use |
| Goals draw fields | Water maze, reward-locked recordings, causal inhibition | Decoupled reward delivery does not reproduce the accumulation |
| Terrain shapes fields | A recent study of fields on uneven ground | Relies on one main study so far |

## Open issues

- Whether allocation is a property of single cells, of populations, or of both. Eliav et al. (2021) show several scales within one cell, but how populations combine these scales is not settled.
- How much of the goal effect is reward, attention or planning. Duvelle et al. (2019) suggest that reward delivery alone does not drive accumulation, which leaves the role of the goal location and task demands open.
- How to separate real allocation from sampling artefacts in practice. The measurement studies give tools, but many papers still use uncorrected counts.

## Connections

- [Memory & Learning in the Brain](../index.md) covers the systems and plasticity side of memory.
- [Grid-like units in navigating networks](../../neuroai/grid-like-units/index.md) describes how the same kind of spatial code appears in artificial networks.

## References

- Kjelstrup, K. B., Solstad, T., Brun, V. H., Hafting, T., Leutgeb, S., Witter, M. P., Moser, E. I., & Moser, M.-B. (2008). Finite scale of spatial representation in the hippocampus. *Science*, 321(5885), 140–143. https://doi.org/10.1126/science.1157086 — Shows that place-field scale rises along the long axis of the hippocampus.
- Stensola, H., Stensola, T., Solstad, T., Frøland, K., Moser, M.-B., & Moser, E. I. (2012). The entorhinal grid map is discretized. *Nature*, 492(7427), 72–78. https://doi.org/10.1038/nature11649 — Reports that grid cells fall into a small number of discrete modules.
- Brun, V. H., Solstad, T., Kjelstrup, K. B., Fyhn, M., Witter, M. P., Moser, E. I., & Moser, M.-B. (2008). Progressive increase in grid scale from dorsal to ventral medial entorhinal cortex. *Hippocampus*, 18(12), 1200–1212. https://doi.org/10.1002/hipo.20504 — Documents grid spacing increasing with distance from the dorsal border.
- Eliav, T., Maimon, S. R., Aljadeff, J., Tsodyks, M., Ginosar, G., Las, L., & Ulanovsky, N. (2021). Multiscale representation of very large environments in the hippocampus of flying bats. *Science*, 372(6545), eabg4020. https://doi.org/10.1126/science.abg4020 — Shows that a single neuron can carry place fields at several scales.
- Mehta, M. R., Barnes, C. A., & McNaughton, B. L. (1997). Experience-dependent, asymmetric expansion of hippocampal place fields. *PNAS*, 94(16), 8918–8921. https://doi.org/10.1073/pnas.94.16.8918 — Shows that repeated traversal enlarges fields asymmetrically within a few laps.
- Yartsev, M. M., Witter, M. P., & Ulanovsky, N. (2011). Grid cells without theta oscillations in the entorhinal cortex of bats. *Nature*, 479(7371), 103–107. https://doi.org/10.1038/nature10583 — Shows normal grid cells in bats without continuous theta, which challenges oscillatory models of grid scale.
- Krupic, J., Bauza, M., Burton, S., Barry, C., & O'Keefe, J. (2015). Grid cell symmetry is shaped by environmental geometry. *Nature*, 518(7538), 232–235. https://doi.org/10.1038/nature14153 — Shows that grid symmetry and scale depend on enclosure geometry.
- Barry, C., Hayman, R., Burgess, N., & Jeffery, K. J. (2007). Experience-dependent rescaling of entorhinal grids. *Nature Neuroscience*, 10(6), 682–684. https://doi.org/10.1038/nn1905 — Shows grid scale rescaling with the size and shape of a familiar environment.
- Barry, C., Ginzberg, L. L., O'Keefe, J., & Burgess, N. (2012). Grid cell firing patterns signal environmental novelty by expansion. *PNAS*, 109(43), 17687–17692. https://doi.org/10.1073/pnas.1209918109 — Shows grid scale expanding in a novel arena and then contracting.
- Bittner, K. C., Milstein, A. D., Grienberger, C., Romani, S., & Magee, J. C. (2017). Behavioral time scale synaptic plasticity underlies CA1 place fields. *Science*, 357(6355), 1033–1036. https://doi.org/10.1126/science.aan3846 — Shows that a single plateau potential can create a place field in one trial.
- Hollup, S. A., Molden, S., Donnett, J. G., Moser, M.-B., & Moser, E. I. (2001). Accumulation of hippocampal place fields at the goal location in an annular watermaze task. *Journal of Neuroscience*, 21(5), 1635–1644. https://doi.org/10.1523/JNEUROSCI.21-05-01635.2001 — Reports more place-field peaks near the hidden platform than expected.
- Vaidya, S. P., Li, G., Chitwood, R. A., Li, Y., & Magee, J. C. (2025). Formation of an expanding memory representation in the hippocampus. *Nature Neuroscience*, 28(7), 1510–1518. https://doi.org/10.1038/s41593-025-01986-3 — Shows that stably fielded cells and their stability both grow over seven days.
- Dupret, D., O'Neill, J., Pleydell-Bouverie, B., & Csicsvari, J. (2010). The reorganization and reactivation of hippocampal maps predict spatial memory performance. *Nature Neuroscience*, 13(8), 995–1002. https://doi.org/10.1038/nn.2599 — Shows that CA1 reorganises toward new goals and that this predicts memory performance.
- Sarel, A., Finkelstein, A., Las, L., & Ulanovsky, N. (2017). Vectorial representation of spatial goals in the hippocampus of bats. *Science*, 355(6321), 176–180. https://doi.org/10.1126/science.aak9589 — Shows hippocampal neurons tuned to the direction and distance of goals.
- Boccara, C. N., Nardin, M., Stella, F., O'Neill, J., & Csicsvari, J. (2019). The entorhinal cognitive map is attracted to goals. *Science*, 363(6434), 1443–1447. https://doi.org/10.1126/science.aav4837 — Shows grid fields shifting toward learned goals.
- Butler, W. N., Hardcastle, K., & Giocomo, L. M. (2019). Remembered reward locations restructure entorhinal spatial maps. *Science*, 363(6434), 1447–1452. https://doi.org/10.1126/science.aav5297 — Links restructured entorhinal maps to better decoding near the reward.
- Grienberger, C., & Magee, J. C. (2022). Entorhinal cortex directs learning-related changes in CA1 representations. *Nature*, 611(7936), 554–562. https://doi.org/10.1038/s41586-022-05378-6 — Shows that CA1 reward-zone over-representation depends on entorhinal input.
- Ormond, J., & O'Keefe, J. (2022). Hippocampal place cells have goal-oriented vector fields during navigation. *Nature*, 607(7920), 741–746. https://doi.org/10.1038/s41586-022-04913-9 — Shows that place-cell vector fields converge on goals during navigation.
- Duvelle, É., Grieves, R. M., Hok, V., Poucet, B., Arleo, A., Jeffery, K. J., & Save, E. (2019). Insensitivity of place cells to the value of spatial goals in a two-choice flexible navigation task. *Journal of Neuroscience*, 39(13), 2522–2541. https://doi.org/10.1523/JNEUROSCI.1578-18.2018 — Finds no field accumulation when reward delivery is decoupled from the goal.
- Sheintuch, L., Rubin, A., & Ziv, Y. (2022). Bias-free estimation of information content in temporally sparse neuronal activity. *PLOS Computational Biology*, 18(2), e1009832. https://doi.org/10.1371/journal.pcbi.1009832 — Shows that naive information estimates are biased upward at low sample sizes.
- Mamad, O., Stumpp, L., McNamara, H. M., Ramakrishnan, C., Deisseroth, K., Reilly, R. B., & Tsanov, M. (2017). Place field assembly distribution encodes preferred locations. *PLOS Biology*, 15(9), e2002365. https://doi.org/10.1371/journal.pbio.2002365 — Reports accumulation at preferred locations and discusses oversampling as a confound.
- Grieves, R. M., Duvelle, É., & Taube, J. S. (2026). Hippocampal place cells map terrain geometry independently of behavior. *Science Advances*, 12(23), eadz9893. https://doi.org/10.1126/sciadv.adz9893 — Shows that fields follow terrain contours rather than the animal's movement biases.
