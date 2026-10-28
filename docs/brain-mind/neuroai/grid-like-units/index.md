---
status: draft
last_reviewed: 2026-10-28
---

# Grid-like units in a navigating network (Banino et al., 2018)

A recurrent agent trained to navigate develops grid-like units.

## Problem

Do grid-like representations, which the brain uses for location, arise when a network is trained only to navigate?

## Core idea

Train a recurrent agent to navigate virtual environments to goal locations, using velocity and visual inputs, with reinforcement learning. The paper reports that grid-like units emerge in the agent's hidden layer, without being built in, and that they help the agent navigate by vectors.

## Equation or algorithm


  1. Give the agent velocity and visual input.
  2. Train it with reinforcement learning to reach goals.
  3. Inspect its hidden units for hexagonal firing patterns.

## Limitations

The agent and its environments are simple and artificial. The design-choice caveats in the table above apply to this result.

## Connections

- Parent topic: [NeuroAI](../index.md)
- Other method on this topic: [Performance-Optimised Networks Predict Visual Cortex](../performance-optimised-networks/index.md)

## References

### Seminal papers

- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that deep networks trained for object recognition predict neural responses in higher visual cortex.
- Banino, A., et al. (2018). Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — Shows that grid-like units emerge in a recurrent agent trained to navigate.
- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M. (2017). Neuroscience-Inspired Artificial Intelligence. *Neuron*. https://doi.org/10.1016/j.neuron.2017.06.011 — The classic review of how neuroscience has inspired AI, and how AI can test ideas about the brain.
- Richards, B. A., et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — Argues for studying the brain through objective functions, learning rules and architectures.

### Surveys and textbooks

- Schrimpf, M., et al. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Shows that next-word-prediction language models predict brain responses in the language network, and that better prediction goes with better brain fit.
