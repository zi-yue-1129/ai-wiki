---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- navigation
- memory
aliases:
  - 位置細胞
  - Place cells
  - Place cell
  - 認知地圖假說
---

# Place cells and the cognitive-map hypothesis (O'Keefe & Dostrovsky, 1971)

Place cells are hippocampal neurons that fire strongly when an animal is in one particular part of an environment. O'Keefe and Dostrovsky (1971) reported unit recordings from freely moving rats and proposed that the hippocampus holds a spatial map, which gives a neural side to Tolman's cognitive-map idea.

This page is part of [Spatial Navigation and Cognitive Maps](../index.md). It covers one method in detail. The wider picture, including head-direction cells and grid-like units, is on that page.

## Overview

Imagine walking through a room. Some hippocampal neurons become active only when you stand in one spot, and each neuron has a different spot. Together, these neurons could tell the brain where the animal is, and that information could be used to plan a route. The 1971 paper reports unit activity from a rat moving freely in an environment, and its title proposes that the hippocampus is a spatial map.

## Key concepts

- **Place field**: the region of an environment where a place cell fires.
- **Spatial map**: a representation in which the population activity tracks where the animal is.
- **Cognitive map**: Tolman's (1948) term for a map-like representation of an environment, used for flexible behaviour such as finding a new route.
- **Remapping**: a change in which place cells fire, and where, when the environment changes.

## Problem

By the early 1970s, the hippocampus was linked to memory and behaviour, but the question was whether its activity carried spatial information. If it did, the hippocampus could be the neural substrate of a cognitive map. The 1971 paper addressed this with unit recordings from a freely moving rat.

## Core idea

The 1971 paper's title states the proposal: the hippocampus is a spatial map, supported by preliminary unit activity from freely moving rats. The proposal links to Tolman's (1948) cognitive-map idea. If many units are tuned to different places, together they could encode the animal's position and support navigation. The idea is about population coding: a whole set of neurons, each tied to its own place, would carry the spatial information.

## Equation or algorithm

A common simple model describes a place cell's firing rate as a Gaussian bump around a preferred location \(c\):

\(f(x) = r_{\max} \exp\left(-\frac{\lVert x - c \rVert^{2}}{2\sigma^{2}}\right)\)

where \(x\) is the animal's position, \(r_{\max}\) is the peak rate, and \(\sigma\) sets the width of the place field. This is a simplified description used in modelling. Real place fields vary in shape and size, and the paper itself is the primary source for the observations.

## Results

O'Keefe and Dostrovsky (1971) present preliminary evidence from unit activity in the freely moving rat, in support of the proposal that the hippocampus is a spatial map. The report is preliminary, and its claims are limited to the cells and environments the authors studied.

Later work added two points that matter for the map idea. Place cells are part of a wider circuit that includes a second population, grid-like units in the entorhinal cortex (Moser et al., 2008). Grid-like units are covered on the [grid-like units page](../../neuroai/grid-like-units/index.md). And the hippocampus may represent space as a predictive map rather than a simple location code (Stachenfeld et al., 2017).

## Limitations

- **Preliminary report.** The 1971 paper is an early, preliminary report, and its claims are limited to the animals and environments it describes. Later work tested the claims more widely.
- **Location is not all of it.** Place cells may carry information beyond location, and later models include landmark-like and other non-spatial signals. The [Tolman–Eichenbaum Machine](../tolman-eichenbaum-machine/index.md) proposes such a model (Whittington et al., 2020).
- **Stability and remapping.** Whether place fields stay stable or change, and why, is part of the model comparison. The TEM model predicts that remapping is structured rather than random.

## Connections

- **Cognitive map**: place cells are the best-known neural candidate for the cognitive map. See [Spatial Navigation and Cognitive Maps](../index.md).
- **Successor representation**: a predictive map in the hippocampus can be read as an SR over space. See [Successor representation](../successor-representation/index.md).
- **Memory**: place cells replay recent experience during rest and sleep, which links spatial coding to memory. See [Memory & Learning in the Brain](../../memory-learning/index.md).
- **AI**: place-cell maps inspired discussions of learned world models in agents. See [World Models & Embodied AI](../../../theory/models/world-models/index.md).

## Applications

- **Neuroscience of navigation**: place cells are the reference point for studying how the hippocampus represents space.
- **Predictive maps**: Stachenfeld et al. (2017) use the predictive-map view to connect place cells to reinforcement learning. The link to planning and to [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md) is discussed there.

## Open questions

- **What drives place fields?** How much of a place field comes from landmarks, self-motion or internal state is still debated.
- **Map or predictive map?** Whether place cells encode position itself or the future states expected from it is an open question (Stachenfeld et al., 2017).
- **How is the map used?** Place cells provide the spatial code, but how that code supports planning and novel routes is still being studied (Behrens et al., 2018).

## References

### Seminal papers

- O'Keefe, J. & Dostrovsky, J. (1971). The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat. *Brain Research*. https://doi.org/10.1016/0006-8993(71)90358-1 — Preliminary evidence from unit activity in a freely moving rat, with the proposal, in its title, that the hippocampus is a spatial map.
- Tolman, E. C. (1948). Cognitive maps in rats and men. *Psychological Review*. https://doi.org/10.1037/h0061626 — Introduces the term "cognitive map" in a paper on rats and people, the idea that place-cell research later took up.
- Stachenfeld, K. L., Botvinick, M. M. & Gershman, S. J. (2017). The hippocampus as a predictive map. *Nature Neuroscience*. https://doi.org/10.1038/nn.4650 — Proposes, drawing on reinforcement learning, that hippocampal place cells carry a predictive map rather than a purely spatial one.

### Surveys and textbooks

- Behrens, T. E. J. et al. (2018). What Is a Cognitive Map? Organizing Knowledge for Flexible Behavior. *Neuron*. https://doi.org/10.1016/j.neuron.2018.10.002 — Reviews evidence that map-like representations seen in space may be an instance of general mechanisms for organising knowledge.
- Moser, E. I., Kropff, E. & Moser, M.-B. (2008). Place Cells, Grid Cells, and the Brain's Spatial Representation System. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.31.061307.090723 — Reviews how place cells and grid cells, as parts of one circuit, may represent places and routes during behaviour and memory.
