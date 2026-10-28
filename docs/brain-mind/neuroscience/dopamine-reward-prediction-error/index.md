---
status: draft
last_reviewed: 2026-10-28
---

# Dopamine reward prediction error (Schultz, Dayan & Montague, 1997)

Dopamine neurons signal the difference between the reward expected and the reward received.

## Problem

What do midbrain dopamine neurons signal while an animal learns about rewards?

## Core idea

Dopamine neurons respond to unexpected rewards, and as learning proceeds the response moves to the earliest predictive cue. The pattern matches a temporal-difference error, the difference between the reward received and the reward predicted.

## Equation or algorithm

In modern notation, \(\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)\).

## Results

In monkeys, dopamine firing rose to unexpected rewards, shifted to the predictive cue after learning, and dipped when an expected reward was omitted.

## Limitations

Recordings came from a limited number of monkeys and tasks. Later work debated whether dopamine signals only prediction error or also salience and other information.

## Connections

- Parent topic: [Neuroscience Basics](../index.md)
- Other method on this topic: [Receptive Fields in Visual Cortex](../receptive-fields-hubel-wiesel/index.md)

## References

### Seminal papers

- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — Discovers orientation-selective simple and complex cells, the biological inspiration for hierarchical vision models.
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neurons signal reward prediction errors, linking reinforcement learning to the brain.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2787 — Proposes that brains minimise prediction error, a unifying framework for perception, action and learning.
- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that deep networks trained for object recognition predict neural responses in higher visual cortex.

### Surveys and textbooks

- Neuroscience Online: An Electronic Textbook for the Neurosciences. Department of Neurobiology and Anatomy, UTHealth McGovern Medical School. https://nba.uth.tmc.edu/neuroscience/ — A free, open-access electronic textbook for the neurosciences.
