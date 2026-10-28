---
status: draft
last_reviewed: 2026-10-28
---

# Single-neuron recording in visual cortex (Hubel & Wiesel, 1962)

Single-neuron recordings in cat visual cortex show cells that respond to oriented edges.

## Problem

How the visual cortex builds representations of edges and shapes from light falling on the retina.

## Core idea

Record single neurons in the visual cortex of anaesthetised cats while presenting spots and bars of light at different positions and orientations. Neurons were sorted into simple cells, with separate on and off subregions that respond to edges at a preferred orientation, and complex cells, which respond to such an edge anywhere in a larger region.

## Equation or algorithm


  1. Present a stimulus at a given position and orientation.
  2. Record the spikes of the neuron.
  3. Map the receptive field from the responses.
  4. Classify the cell by its response pattern.

## Results

Complex cells appear to pool the outputs of simple cells, a hierarchy that inspired hierarchical convolutional vision models.

## Limitations

The experiments used anaesthetised cats, and the hierarchy is a model that later work found more varied than the two cell types suggest.

## Connections

- Parent topic: [Neuroscience Basics](../index.md)
- Other method on this topic: [Dopamine Reward Prediction Error](../dopamine-reward-prediction-error/index.md)

## References

### Seminal papers

- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — Discovers orientation-selective simple and complex cells, the biological inspiration for hierarchical vision models.
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neurons signal reward prediction errors, linking reinforcement learning to the brain.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2787 — Proposes that brains minimise prediction error, a unifying framework for perception, action and learning.
- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that deep networks trained for object recognition predict neural responses in higher visual cortex.

### Surveys and textbooks

- Neuroscience Online: An Electronic Textbook for the Neurosciences. Department of Neurobiology and Anatomy, UTHealth McGovern Medical School. https://nba.uth.tmc.edu/neuroscience/ — A free, open-access electronic textbook for the neurosciences.
