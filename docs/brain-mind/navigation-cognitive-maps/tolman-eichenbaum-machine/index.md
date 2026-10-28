---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- navigation
- memory
- representation learning
aliases:
  - Tolman-Eichenbaum 機器
  - Tolman–Eichenbaum Machine
  - TEM
---

# Tolman–Eichenbaum Machine (Whittington et al., 2020)

The Tolman–Eichenbaum Machine (TEM) is a model of the hippocampal–entorhinal system that treats spatial navigation and relational memory as one problem. Its main proposal is that a single structured representation supports both, and that grid-like and place-like units emerge from learning it.

This page is part of [Spatial Navigation and Cognitive Maps](../index.md). It covers one method in detail; the wider idea of cognitive maps is on that page.

## Overview

Animals remember places, and they also remember how things relate: which item follows which, or which objects share a context. These two kinds of memory are often studied separately. TEM proposes that they rely on one generalisable structure. Once that structure is learned, it can be reused in a new environment, so the animal does not have to learn the whole layout again.

## Key concepts

- **Relational memory**: knowledge of how items, places or events are linked, not only what each one is.
- **Structural knowledge**: a code for the shape of relations that holds across environments. In TEM this lives mainly in the entorhinal component.
- **Generalisation**: applying learned structure to a new environment or task.
- **Remapping**: a change in the place-cell code when the environment changes.

## Problem

The hippocampal–entorhinal system is important for both spatial and relational memory tasks. The open question is what computation links these two roles, and how the system generalises across environments without relearning everything. Without a shared computation, the two roles would look like unrelated functions of the same brain area.

## Core idea

TEM proposes that entorhinal cells form a basis that describes structural knowledge, and that hippocampal cells link this basis to sensory representations. Structure is kept fixed across environments. For each new environment, the model learns how sensory input maps onto that shared structure. The authors present this as a mechanistic account of how the hippocampus supports generalisation.

## Equation or algorithm

TEM is a neural network trained by prediction, and it is not summarised by one equation. The outline below summarises the model's main steps; the paper's methods give the details:

1. Present the model with a sequence of observations and movements in an environment.
2. The entorhinal-like component builds a structural code for the relations in the sequence.
3. The hippocampal-like component binds that code to the current sensory input, forming a memory of the event.
4. Train the network to predict upcoming observations from these memories. The structural code is kept across environments.
5. After training, inspect the units. Check the cell types that appear, and test remapping and generalisation in new settings.

The full architecture and training details are in the paper. This page gives the outline only.

## Results

The results below are from the abstract of the earlier bioRxiv preprint of the same work (Whittington et al., 2019). The published Cell article extends the preprint, so its claims should be checked against that version.

- The model proposes that medial entorhinal cells form a basis describing structural knowledge, and that hippocampal cells link this basis to sensory representations.
- After learning, its entorhinal-like units include grid, band, border and object-vector cells. The grid-like part of this is discussed on the [grid-like units page](../../neuroai/grid-like-units/index.md).
- Its hippocampal-like units include place and landmark cells, which remap between environments.
- The model predicts that remapping is not random: structural knowledge is preserved across environments. The authors confirm this in simultaneously recorded place and grid cells.
- The model also predicts empirically recorded representations in complex non-spatial tasks.

## Limitations

- **Model, not measurement.** The model's units resemble real cell types, but resemblance does not show that the same computation happens in the brain.
- **Design choices.** The outcome depends on the architecture and training the authors chose. The [NeuroAI page](../../neuroai/index.md) notes that similar grid-like results can depend on design choices.
- **Scope.** The model is built around sequences of observations and movements. Many aspects of memory and navigation are outside its scope.

## Connections

- **Cognitive map**: TEM gives one concrete account of the cognitive-map idea. See [Spatial Navigation and Cognitive Maps](../index.md).
- **Memory**: the hippocampal and entorhinal roles in memory are on [Memory & Learning in the Brain](../../memory-learning/index.md). TEM links the spatial and relational parts of that picture. Grid-like codes for conceptual, non-spatial knowledge have also been reported in humans (Constantinescu et al., 2016).
- **Place cells**: the hippocampal side of the model is the place-cell story of [Place cells and the cognitive-map hypothesis](../place-cells/index.md).
- **AI**: a shared structure that transfers to new environments is the kind of idea discussed for [World Models & Embodied AI](../../../theory/models/world-models/index.md).

## Applications

- **Hypothesis generation**: TEM generates predictions that can be checked against recordings, such as whether hippocampal remapping keeps structural knowledge fixed across environments.
- **Structured generalisation in AI**: the idea that learned structure should carry over to new environments connects TEM to work on world models. See the [world-models page](../../../theory/models/world-models/index.md).

## Open questions

- **Is the structure the same as the brain's?** TEM proposes that entorhinal cells encode structure. Whether they do so in the way the model assumes is still being tested.
- **How is the structure learned and held fixed?** The model's stability across environments depends on details of learning that are still debated.
- **How far does the account reach?** Behrens et al. (2018) discuss cognitive maps as a general way of organising knowledge, and how far TEM extends beyond space is open.

## References

### Seminal papers

- Whittington, J. C. R. et al. (2020). The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation. *Cell*. https://doi.org/10.1016/j.cell.2020.10.024 — Proposes the TEM and its account of how one structure supports spatial and relational memory and generalisation.
- Whittington, J. C. R., Muller, T., Mark, S., Chen, G., Barry, C. & Burgess, N. (2019). The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation. *bioRxiv* (preprint). https://doi.org/10.1101/770495 — The earlier preprint of the same work. Its abstract is the source for the Results section.
- Hafting, T. et al. (2005). Microstructure of a spatial map in the entorhinal cortex. *Nature*. https://doi.org/10.1038/nature03721 — Describes grid cells in the entorhinal cortex, the cell type TEM reproduces.

### Surveys and textbooks

- Behrens, T. E. J. et al. (2018). What Is a Cognitive Map? Organizing Knowledge for Flexible Behavior. *Neuron*. https://doi.org/10.1016/j.neuron.2018.10.002 — Review of cognitive maps and their extension to abstract knowledge, the framework TEM builds on.
- Moser, E. I., Kropff, E. & Moser, M.-B. (2008). Place Cells, Grid Cells, and the Brain's Spatial Representation System. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.31.061307.090723 — Reviews how place cells and grid cells, as parts of one circuit, may represent places and routes during behaviour and memory.

### Articles and documentation

- Constantinescu, A. O., O'Reilly, J. X. & Behrens, T. E. J. (2016). Organizing conceptual knowledge in humans with a gridlike code. *Science*. https://doi.org/10.1126/science.aaf0941 — Reports gridlike neural representation of conceptual space in several brain regions, including the entorhinal cortex.
