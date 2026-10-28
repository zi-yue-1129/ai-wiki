---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- representation learning
aliases:
  - 網格細胞
  - Hafting et al. 2005
  - Grid Cells
---

# Grid Cells (Hafting et al., 2005)

Hafting et al. (2005) recorded neurons in the medial entorhinal cortex of rats and found cells whose firing fields repeat at the points of a regular triangular lattice spanning the whole enclosure. The result added a second, geometric spatial code beside the hippocampal place map, and it became a basis for much of the work on path integration. It is one method behind [Spatial Navigation and Cognitive Maps](../index.md).

## Overview

Place cells in the hippocampus fire in single places, as shown by O'Keefe and Dostrovsky (1971), covered on the [Place Cells](../place-cells/index.md) page. Much of the hippocampus's spatial input comes through the entorhinal cortex, the cortical region next to it. Hafting and colleagues recorded from the medial part of that region, the MEC, in rats that foraged freely in an open enclosure.

The cells differed from place cells. Each grid cell had several firing fields, not one, and the fields were arranged in a regular pattern close to a hexagon of equal spacing that covered the whole enclosure. The title, "Microstructure of a spatial map", reflects this: the entorhinal cortex contains a fine-grained, metric map of space.

## Key concepts

- **Grid field**: one of the several firing fields of a grid cell.
- **Lattice**: the regular arrangement of grid fields. In the paper it is roughly triangular, which is a hexagonal pattern.
- **Spacing and orientation**: the distance between neighbouring fields and the angle of the lattice. Both vary from cell to cell.
- **Path integration**: estimating position by integrating self-motion. Grid cells are a leading candidate for its neural substrate (McNaughton et al., 2006).

## How it works

The study can be read as a numbered procedure:

1. Implant electrodes in the medial entorhinal cortex and let rats forage in an open enclosure.
2. Record single units while tracking the rat's position, and plot each unit's spikes over its path.
3. Build a firing-rate map for each unit, and look for units with several fields.
4. Check whether the fields lie on a regular lattice, and describe each cell by its spacing and orientation.

A common idealised model describes a grid field as the sum of three cosine waves whose wave vectors point 60 degrees apart. With phases $\phi_j$ and wave vectors $\mathbf{k}_j$, the firing rate is

$$
\lambda(\mathbf{x}) = \max\Bigl(0,\; \textstyle\sum_{j=1}^{3} \cos(\mathbf{k}_j \cdot \mathbf{x} + \phi_j)\Bigr)
$$

This is a modelling convention used in later work, not a formula taken from the 2005 paper. It captures the periodic, hexagonal layout, and the spacing is set by the length of the wave vectors.
## Results

The main evidence is the firing maps of individual entorhinal units recorded in rats in an open enclosure. Many units had multiple firing fields, and each unit's fields formed a regular lattice that covered the enclosure. Neighbouring cells differed in lattice spacing and orientation. The paper's full text was not accessible for this page, and the Crossref record has no abstract, so this section describes the result only qualitatively. No numbers are quoted.

## Limitations

- The study used a small number of animals in simple enclosures. How grid patterns change with the shape or size of the environment is a question for later work.
- The lattice describes the firing maps. The paper does not establish what grid cells are used for. A grid code could support path integration, but it could serve other purposes too.

## Open questions

- **Where does the lattice come from?** Attractor models propose that connectivity produces the pattern, while learning-based models propose that experience shapes it. Trained networks show grid-like units (Banino et al., 2018; Cueva & Wei, 2018), but the result depends on the training setup, and it is unclear which of its features matter for the brain.
- **What sets the spacing?** Grid cells often share a spacing and orientation with neighbouring cells, and the reason is still debated (Moser et al., 2008).
- **What is the grid code for?** Path integration is the main candidate, but the same structure might also index memories or organise non-spatial knowledge. The [Tolman–Eichenbaum Machine](../tolman-eichenbaum-machine/index.md) takes the second view.

## Connections

Grid cells and place cells form a pair: grid cells give a metric code of the environment, and place cells use it together with sensory landmarks. Trained networks that reproduce grid-like units are covered on the [Grid-Like Units](../../neuroai/grid-like-units/index.md) page.
## References

### Seminal papers

- Hafting, T., Fyhn, M., Molden, S., Moser, M.-B. & Moser, E. I. (2005). Microstructure of a spatial map in the entorhinal cortex. *Nature*. https://doi.org/10.1038/nature03721 — Reports grid cells in the medial entorhinal cortex, whose firing fields form a regular triangular lattice across an open enclosure.
- O'Keefe, J. & Dostrovsky, J. (1971). The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat. *Brain Research*. https://doi.org/10.1016/0006-8993(71)90358-1 — The place-cell study that established the hippocampal spatial code, which grid cells feed into.
- Cueva, C. J. & Wei, X.-X. (2018). Emergence of grid-like representations by training recurrent neural networks to perform spatial localization. arXiv. https://arxiv.org/abs/1803.07770 — Shows that recurrent networks trained for spatial localisation develop grid-like tuning.
- Banino, A. et al. (2018). Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — Shows that grid-like units emerge in a recurrent agent trained to navigate, and help it navigate by vectors.

### Surveys and textbooks

- Moser, E. I., Kropff, E. & Moser, M.-B. (2008). Place cells, grid cells, and the brain's spatial representation system. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.31.061307.090723 — Reviews grid cells and their relation to place cells and the wider spatial system.
- McNaughton, B. L. et al. (2006). Path integration and the neural basis of the 'cognitive map'. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn1932 — Reviews how grid cells and related cells may carry out path integration in the entorhinal–hippocampal system.
