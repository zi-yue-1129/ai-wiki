---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- representation learning
aliases:
  - 位置細胞
  - O'Keefe and Dostrovsky 1971
  - Place Cells
---

# Place Cells (O'Keefe & Dostrovsky, 1971)

O'Keefe and Dostrovsky (1971) recorded single neurons in the hippocampus of rats that were free to move around an enclosure. Some cells fired only when the animal was in one part of the enclosure. The paper proposed that the hippocampus holds a map of space, and it is the starting point for the place-cell evidence on [Spatial Navigation and Cognitive Maps](../index.md).

## Overview

Before this study, the hippocampus was known to matter for memory, but little was known about what its neurons represented. O'Keefe and Dostrovsky recorded the activity of individual units while the rat moved, and tracked its position at the same time. For many units the answer to "where is this cell active?" was a restricted region, and different units had different regions.

The title states the interpretation: the hippocampus works as a spatial map. Each cell marks one location, and the population as a whole covers the environment. The idea was later taken up in the wider cognitive-map account, which goes back to Tolman (1948) and is described on the parent page.

## Key concepts

- **Place cell**: a hippocampal neuron whose firing is tied to a location in the environment.
- **Place field**: the region of the environment in which a place cell is active.
- **Population code**: a representation spread across many neurons, in which each neuron contributes part of the information, such as which place the animal occupies.
- **Remapping**: a change in which cells fire where when the environment changes. It shows that the map is tied to the environment, not only to the animal's movements.

## How it works

The study can be read as a numbered procedure:

1. Implant an electrode in the rat hippocampus and let the animal move freely in an enclosure with visual cues.
2. Record the spikes of single units while the rat moves, and track its position at the same time, so each spike is matched to a location.
3. For each unit, build a map of firing rate against location, and find the region where the rate is high. This region is the place field.
4. A unit with a single, restricted field is a place cell.

In notation, let $\lambda_i(\mathbf{x})$ be the mean firing rate of unit $i$ at location $\mathbf{x}$. A place cell has a $\lambda_i$ that is high in one region and low elsewhere. The population response at $\mathbf{x}$ is $\mathbf{r}(\mathbf{x}) = (\lambda_1(\mathbf{x}), \dots, \lambda_N(\mathbf{x}))$. If different units have different fields, each location produces a distinct pattern, which makes $\mathbf{r}(\mathbf{x})$ a usable code for position.

## Results

The main evidence is the set of firing maps from individual hippocampal units recorded while rats explored an enclosure. Many units were active in a restricted area, and the areas differed from one unit to the next, so the population covered the enclosure. The paper's full text was not accessible for this page, and the Crossref record has no abstract, so this section describes the result only qualitatively. No numbers are quoted.

## Limitations

- The recordings came from a few rats in a simple enclosure. The paper is a preliminary report, and some of its claims go beyond the data.
- A unit whose firing is restricted to a place correlates with location. That alone does not show the cell is used for navigation. Further tests, such as lesion and behavioural experiments, are needed.
- Place fields depend on sensory cues and experience. Reading the hippocampus as a fixed map does not explain how the map is learned or updated.
- Place cells are only part of the spatial code. Grid cells carry a different, geometric code, covered on the [Grid Cells](../grid-cells/index.md) page.

## Open questions

- **Where do place fields come from?** One view is that they are formed from grid-cell input and sensory landmarks. Another is that the place code is learned directly from experience. The [Tolman–Eichenbaum Machine](../tolman-eichenbaum-machine/index.md) is one model that tries to unify these ideas.
- **Do place cells encode anything beyond space?** The Tolman–Eichenbaum Machine proposes that hippocampal cells also represent non-spatial relations, and it tests this against recordings from non-spatial tasks. How far this extends is still debated.
- **How stable is the map?** Place fields can change between sessions and between environments. The mechanisms that keep the code consistent over long periods are not fully understood.

## Connections

The companion method is [Grid Cells](../grid-cells/index.md), whose firing is proposed to provide a metric input to place cells (Moser et al., 2008). The hippocampal side of the memory story is in [Memory & Learning in the Brain](../../memory-learning/index.md), and the replay of place-cell sequences during sleep is covered in [Hippocampal Replay](../../sleep-and-consolidation/hippocampal-replay/index.md).

## References

### Seminal papers

- O'Keefe, J. & Dostrovsky, J. (1971). The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat. *Brain Research*. https://doi.org/10.1016/0006-8993(71)90358-1 — Reports hippocampal units in freely moving rats that fire when the animal is in a particular place, and proposes that the hippocampus is a spatial map.
- Tolman, E. C. (1948). Cognitive maps in rats and men. *Psychological Review*. https://doi.org/10.1037/h0061626 — Argues that rats in mazes acquire a map-like knowledge of the environment, the idea that place-cell work later made physiological.
- Hafting, T., Fyhn, M., Molden, S., Moser, M.-B. & Moser, E. I. (2005). Microstructure of a spatial map in the entorhinal cortex. *Nature*. https://doi.org/10.1038/nature03721 — Reports grid cells in the medial entorhinal cortex, the input region proposed to supply place cells with a metric code.

### Surveys and textbooks

- Moser, E. I., Kropff, E. & Moser, M.-B. (2008). Place cells, grid cells, and the brain's spatial representation system. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.31.061307.090723 — Reviews place cells alongside grid and related cells, and how they together represent space.
- McNaughton, B. L. et al. (2006). Path integration and the neural basis of the 'cognitive map'. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn1932 — Reviews how self-motion signals can be integrated to maintain the hippocampal map of the environment.
