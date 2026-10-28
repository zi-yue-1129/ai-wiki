---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- representation learning
aliases:
  - Tolman-Eichenbaum Machine
  - TEM
  - Whittington et al. 2020
---

# Tolman–Eichenbaum Machine (Whittington et al., 2020)

The Tolman–Eichenbaum Machine (TEM) is a model by Whittington et al. (2020) in which one hippocampal–entorhinal system supports both spatial navigation and relational memory. Its central claim is that the two are one problem: learning how things are related, from experience, produces place-like and grid-like codes as a by-product. It is one method behind [Spatial Navigation and Cognitive Maps](../index.md).

## Overview

The hippocampus is needed for spatial navigation, and it is also needed for relational memory: knowing how items, events or states relate to one another, not only what each one is. Tolman's cognitive map (Tolman, 1948) is a relational idea, while grid and place cells were found as spatial codes.
TEM unifies them. The medial entorhinal cortex represents structural knowledge, the relations among states that are shared across situations, and the hippocampus binds these structural codes to sensory content. The shared structural code lets the model generalise to new environments.

## Key concepts

- **Relational memory**: knowledge of how items or states are connected, which allows inferences that were never directly experienced.
- **Structural code**: a representation of the relations among states, independent of what the states look like. TEM proposes that entorhinal cells carry it.
- **Sensory code**: the content of an experience, such as what is seen at a location. TEM proposes that the hippocampus binds it to the structural code.
- **Remapping**: a change in hippocampal firing when the sensory content of an environment changes. TEM treats remapping as a change of content over a structure that is kept.

## How it works

TEM is a generative model trained to predict what it will observe next. The steps below simplify the paper's architecture.

1. At each step, an entorhinal-like code $g_t$ is updated from the previous code and the action taken, $g_t = f(g_{t-1}, a_t)$, so that $g$ tracks the animal's place in the learned structure.
2. The current observation $x_t$ is bound to $g_t$ to form a hippocampal-like code $p_t$, which is written into an associative memory.
3. To predict the observation, the model retrieves stored memories whose structural codes resemble the current one, and reads out the sensory content linked to them.
4. Parameters are learned by reducing prediction error over sequences of experience, across many environments that share the same relational structure. The loss has the form $\mathcal{L} = -\sum_t \log p_\theta(x_t \mid \text{memory retrieved at } t)$.

## Results

The summary below is taken from the abstract of the paper's preprint (Whittington et al., 2019). After learning, units in the entorhinal-like code resemble grid cells, along with band, border and object-vector cells. Units in the hippocampal-like code resemble place and landmark cells, and they remap between environments. The model also predicts recorded representations in complex non-spatial tasks. Its most distinctive prediction is that remapping is not random: structural knowledge is kept across environments, and the paper reports this confirmed in simultaneously recorded place and grid cells. The evidence comes from simulations and recorded neural data.
## Limitations

- TEM is a computational theory, and its mapping onto the brain is partly by analogy.- The tasks are simplified and the environments simulated. Generalisation across real, varied experience has not been shown in the same detail.
- Reproducing some cell types does not establish that the model is correct. Other trained networks also develop grid-like units, as the [Grid-Like Units](../../neuroai/grid-like-units/index.md) page describes.

## Open questions

- **Is the brain's structural code the same for space and non-spatial relations?** Behrens et al. (2018) argue that it may be, and TEM is one concrete version of that claim.
- **How is a new structure learned from few experiences?** How the brain forms a structural code from a single exposure is less clear.
- **How does TEM relate to the successor representation?** The successor representation proposes a predictive, map-like code for the hippocampus (Stachenfeld et al., 2017). How that code relates to TEM's structural code has not been fully worked out.
- **Which predictions can be tested directly?** Structure-preserving remapping is one prediction the paper reports as confirmed. Its other predictions need targeted experiments.

## Connections

TEM builds on the grid and place cell findings, covered on the [Place Cells](../place-cells/index.md) and [Grid Cells](../grid-cells/index.md) pages. It connects to [Memory & Learning in the Brain](../../memory-learning/index.md) and, through its interest in relational structure, to [Model-Based Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/model-based-rl/index.md).

## References

### Seminal papers

- Whittington, J. C. R. et al. (2020). The Tolman-Eichenbaum Machine: Unifying space and relational memory through generalization in the hippocampal formation. *Cell*. https://doi.org/10.1016/j.cell.2020.10.024 — Proposes one model in which entorhinal and hippocampal codes support both spatial and relational memory through generalisation.
- Whittington, J. C. R. et al. (2019). The Tolman-Eichenbaum Machine: Unifying space and relational memory through generalisation in the hippocampal formation. bioRxiv preprint. https://doi.org/10.1101/770495 — The preprint of the same work, the source of the results summarised here.
- Tolman, E. C. (1948). Cognitive maps in rats and men. *Psychological Review*. https://doi.org/10.1037/h0061626 — Argues that rats in mazes acquire a map-like knowledge of the environment, the idea that TEM extends to relational memory.
- Stachenfeld, K. L., Botvinick, M. M. & Gershman, S. J. (2017). The hippocampus as a predictive map. *Nature Neuroscience*. https://doi.org/10.1038/nn.4650 — Proposes that place fields can be read as a successor-like predictive map.
- Banino, A. et al. (2018). Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — Shows that grid-like units emerge in a recurrent agent trained to navigate, and help it navigate by vectors.

### Surveys and textbooks

- Behrens, T. E. J. et al. (2018). What Is a Cognitive Map? Organizing Knowledge for Flexible Behavior. *Neuron*. https://doi.org/10.1016/j.neuron.2018.10.002 — Argues that cognitive maps organise knowledge in general, not only space, and reviews the supporting evidence.
