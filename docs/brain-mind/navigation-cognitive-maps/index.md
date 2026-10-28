---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- theory/models/world-models
tags:
- neuroscience
- navigation
- cognitive maps
- representation learning
aliases:
  - 空間導航與認知地圖
  - 認知地圖
  - 空間導航
  - Spatial navigation
  - Cognitive maps
  - Cognitive map
  - Place cells
---

# Spatial Navigation and Cognitive Maps

Animals find their way by building internal representations of where they are and how places connect. The idea that these representations form a **cognitive map**, a model of the environment that supports planning and novel shortcuts, links navigation to memory and decision making. The same idea appears in AI, where agents learn models of their world and build representations that can be reused when goals change.

This page is the overview. Each method has its own page, listed under [Key methods](#key-methods).

## Overview

A central question is how the brain turns movement and sensory input into a sense of place. Three kinds of cell have been studied most in rodents:

| Cell type | Where | What it signals |
|---|---|---|
| Place cell | Hippocampus | The animal is in one particular location |
| Head-direction cell | Limbic and nearby areas | The head points in one particular direction |
| Grid-like unit | Entorhinal cortex | Many locations on a regular lattice, giving a metric for distance |

The grid-like units are covered in detail on [Grid-like units in a navigating network](../neuroai/grid-like-units/index.md), so this page does not repeat that material.

The cognitive-map idea is older than these recordings. Tolman (1948) introduced the term cognitive map in a paper on rats and people. A map of that kind would allow an animal to work out a route it had never taken. The later question is which neural structures hold such a map, and what form it takes.

## Key concepts

- **Place cell**: a hippocampal neuron that fires strongly when the animal is in a specific part of an environment, called its place field.
- **Head-direction cell**: a neuron whose firing depends on the direction the head faces, not on location (Taube et al., 1990).
- **Cognitive map**: an internal representation of the layout of an environment, or of the relations between items, used for flexible behaviour.
- **Path integration**: estimating one's position from self-motion, without relying on landmarks.
- **Successor representation (SR)**: a description of a state by the future states it tends to lead to. See [Successor representation](successor-representation/index.md).
- **Tolman–Eichenbaum Machine (TEM)**: a model that links spatial and relational memory through a shared, structured representation. See [Tolman–Eichenbaum Machine](tolman-eichenbaum-machine/index.md).

## How it works

Head-direction cells fire according to the animal's heading. Their signal and its origins are reviewed by Taube (2007). The computational side is covered on [Computational Neuroscience](../computational-neuroscience/index.md). Path integration can estimate position without landmarks, and landmarks can correct the error that accumulates.

## Key methods

- [Tolman–Eichenbaum Machine (Whittington et al., 2020)](tolman-eichenbaum-machine/index.md): treats spatial navigation and relational memory as one problem, and produces grid-like and place-like units from a shared structure.
- [Successor representation (Dayan, 1993)](successor-representation/index.md): stores expected future occupancy of states, so that the structure of transitions is kept apart from the reward at each state.
- [Place cells and the cognitive-map hypothesis (O'Keefe & Dostrovsky, 1971)](place-cells/index.md): unit recordings from freely moving rats, and the proposal, in its title, that the hippocampus is a spatial map.

## Connections

- **Memory**: the hippocampus is central to both episodic memory and navigation. [Memory & Learning in the Brain](../memory-learning/index.md) covers the wider picture, and [Complementary Learning Systems](../memory-learning/complementary-learning-systems/index.md) explains how fast hippocampal learning relates to slow cortical learning.
- **Planning and decisions**: a cognitive map allows planning, which is the model-based strategy described on [Model-Based vs Model-Free Control](../decision-reward/model-based-vs-model-free/index.md). The overall role of planning in choice is on [Decision Making, Dopamine & Reward](../decision-reward/index.md).
- **Reinforcement learning**: the successor representation is built from temporal-difference learning, the same family of updates that dopamine is thought to signal (Gershman, 2018, reviews the SR's computational logic). See [Reinforcement Learning](../../theory/paradigms/reinforcement-learning/index.md) and [Dopamine Reward Prediction Error](../neuroscience/dopamine-reward-prediction-error/index.md).
- **Predictive processing**: the predictive-map idea is related to the view that the brain is a prediction machine, covered on [Predictive Coding & Free Energy](../predictive-coding/index.md).
- **AI**: learned world models and map-like representations in agents are covered on [World Models & Embodied AI](../../theory/models/world-models/index.md). For the broader NeuroAI picture, see [NeuroAI](../neuroai/index.md).

## Applications

- **Modelling human learning**: Momennejad et al. (2017) tested the successor representation in two behavioural studies with humans, looking at how choices respond to changes in the sequence of events and to changes in rewards.
- **Trained navigation agents**: whether grid-like units can emerge in artificial agents trained only to navigate is discussed on the [grid-like units page](../neuroai/grid-like-units/index.md).

## Open questions

- **How general is the map?** The TEM proposal suggests one structure serves both space and relational knowledge. Behrens et al. (2018) discuss cognitive maps as a way of organising knowledge in general, not only physical space, but the extent of this is still debated.
- **What do place cells encode?** Some accounts treat place cells as a map of position. Stachenfeld et al. (2017) propose a predictive map instead.
- **Does the grid code depend on design choices?** The emergence of grid-like units in trained agents is debated, as the [NeuroAI page](../neuroai/index.md) notes.
- **Do biological and artificial navigators share mechanisms?** Matching behaviour or cell types does not, on its own, show that the mechanism is the same.

## References

### Seminal papers

- O'Keefe, J. & Dostrovsky, J. (1971). The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat. *Brain Research*. https://doi.org/10.1016/0006-8993(71)90358-1 — Preliminary evidence from unit activity in a freely moving rat, with the proposal, in its title, that the hippocampus is a spatial map.
- Tolman, E. C. (1948). Cognitive maps in rats and men. *Psychological Review*. https://doi.org/10.1037/h0061626 — Introduces the term cognitive map in a paper on rats and people, the origin of the idea used on this page.
- Taube, J. S., Muller, R. U. & Ranck, J. B. (1990). Head-direction cells recorded from the postsubiculum in freely moving rats. I. Description and quantitative analysis. *Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.10-02-00420.1990 — Describes cells whose firing depends on head direction in the postsubiculum.
- Hafting, T. et al. (2005). Microstructure of a spatial map in the entorhinal cortex. *Nature*. https://doi.org/10.1038/nature03721 — Describes grid cells in the entorhinal cortex. Included for context; the grid-cell detail is on the grid-like units page.
- Dayan, P. (1993). Improving generalization for temporal difference learning: the successor representation. *Neural Computation*. https://doi.org/10.1162/neco.1993.5.4.613 — Shows how temporal-difference machinery can learn representations in which each state is described by its successors.
- Whittington, J. C. R. et al. (2020). The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation. *Cell*. https://doi.org/10.1016/j.cell.2020.10.024 — Proposes a model in which hippocampal and entorhinal structure supports spatial and relational memory together.
- Stachenfeld, K. L., Botvinick, M. M. & Gershman, S. J. (2017). The hippocampus as a predictive map. *Nature Neuroscience*. https://doi.org/10.1038/nn.4650 — Proposes, drawing on reinforcement learning, that the hippocampus represents space as a predictive map.

### Surveys and textbooks

- Behrens, T. E. J. et al. (2018). What Is a Cognitive Map? Organizing Knowledge for Flexible Behavior. *Neuron*. https://doi.org/10.1016/j.neuron.2018.10.002 — Review of cognitive maps, including their extension beyond physical space.
- Gershman, S. J. (2018). The Successor Representation: Its Computational Logic and Neural Substrates. *Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.0151-18.2018 — Review of the computational logic of the successor representation and the evidence for it in the brain.
- Taube, J. S. (2007). The Head Direction Signal: Origins and Sensory-Motor Integration. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.29.051605.112854 — Review of where the head-direction signal comes from and how it is combined with movement.

### Articles and documentation

- Momennejad, I. et al. (2017). The successor representation in human reinforcement learning. *Nature Human Behaviour*. https://doi.org/10.1038/s41562-017-0180-8 — Applies the successor representation to human reinforcement learning.
