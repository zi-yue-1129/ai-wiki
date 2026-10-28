---
status: complete
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- navigation
- reinforcement learning
aliases:
  - 網格狀單元
  - Grid cells
  - Grid-like units
---

# Grid-like units in a navigating network (Banino et al., 2018)

A recurrent agent trained only to navigate develops units whose firing forms a hexagonal grid over space, similar to the grid cells found in the mammalian entorhinal cortex. The result suggests that grid-like codes can arise from the demands of navigation alone.

This page is part of [NeuroAI](../index.md). It covers one method in detail.

## Overview

Animals find their way with an internal sense of where they are. In the rat brain, grid cells in the entorhinal cortex fire at many locations arranged in a regular hexagonal pattern. Banino et al. asked whether a neural network trained to navigate would learn a similar code, without being told to.

## Key concepts

- **Grid cell**: a neuron that fires at many locations in an environment, with the locations forming a regular triangular or hexagonal lattice.
- **Path integration**: estimating position by accumulating self-motion signals, such as velocity, over time.
- **Vector-based navigation**: finding the way to a goal by using a stored representation of the direction and distance to it.
- **Recurrent agent**: a network whose hidden state carries information from one time step to the next, so it can integrate motion over time.

## Problem

Do grid-like representations, which the brain uses for location, arise when a network is trained only to navigate? Earlier models had built grid patterns in by design. The question was whether they would emerge from the task.

## Core idea

Train a recurrent agent to navigate virtual environments to goal locations, using velocity and visual inputs and reinforcement learning. The paper reports that grid-like units emerge in the agent's hidden layer, without being built in. The authors also show that units with this structure help the agent navigate by vectors, which a grid-based code makes possible.

## Method

1. Give the agent velocity and visual input from a simulated environment.
2. Train it with reinforcement learning to reach goal locations.
3. Inspect its hidden units for hexagonal firing patterns over the environment.
4. Test whether the units support navigation to goals placed at new locations.

## Results

The paper reports that a subset of the agent's hidden units has grid-like firing, with the regular lattice seen in biological grid cells. It also reports that the agent navigates to goals by vectors, and that the grid-like code supports this. The results come from simulated environments and a specific architecture, and the paper does not give a single benchmark score for them.

## Limitations

- **Simple, artificial environments.** The agent and its environments are simple, so the result does not show how grid-like codes scale to natural navigation.
- **Design choices matter.** The network architecture, the inputs and the training setup all affect whether grid-like units emerge, and a different design may not produce them.
- **Biology is not fully reproduced.** Biological grid cells sit alongside other spatial cell types, such as head-direction and border cells, which this study does not address directly.

## Connections

- **Spatial cognition**: the biological side of this question, and the related place and grid cells, are in [Neuroscience Basics](../../neuroscience/index.md).
- **Reinforcement learning**: the agent is trained with reinforcement learning, the framework covered in [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).
- **Performance-optimised networks**: a related NeuroAI approach that compares trained networks with brain data is [Performance-Optimised Networks Predict Visual Cortex](../performance-optimised-networks/index.md).

## Applications

- **Robotics and navigation**: grid-like representations are studied as a compact way to encode location and plan routes for mobile robots and agents.
- **Neuroscience hypotheses**: trained networks offer a testable model of how grid codes could arise, which experiments can then check.

## Open questions

- **Which training pressures give rise to grid codes?** The paper shows one set of conditions, and the general rule is not established.
- **How do grid cells interact with other spatial cells in the brain?** Models that include head-direction and border signals are an active research area.
- **Do artificial grid units match biology in detail?** The lattice spacing and firing properties of model units can be compared with recorded grid cells, and the comparison is still being made.

## References

### Seminal papers

- Banino, A., et al. (2018). Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — Shows that grid-like units emerge in a recurrent agent trained to navigate, and that the code supports vector-based navigation.
- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that deep networks trained for object recognition predict neural responses in higher visual cortex, an early example of comparing trained networks with brain data.

### Surveys and reviews

- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M. (2017). Neuroscience-Inspired Artificial Intelligence. *Neuron*. https://doi.org/10.1016/j.neuron.2017.06.011 — The classic review of how neuroscience has inspired AI, and how AI can test ideas about the brain.
- Richards, B. A., et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — Argues for studying the brain through objective functions, learning rules and architectures.
- Schrimpf, M., et al. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Shows that next-word-prediction language models predict brain responses in the language network, and that better prediction goes with better brain fit.
