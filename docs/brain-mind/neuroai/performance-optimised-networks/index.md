---
status: draft
last_reviewed: 2026-10-28
---

# Performance-optimised networks predict visual cortex (Yamins et al., 2014)

Networks optimised for object recognition predict neural responses in visual cortex.

## Problem

Which computational models of the ventral visual stream best predict neural responses in higher visual cortex?

## Core idea

Optimise deep convolutional networks for object recognition, then test how well their features predict recorded responses in V4 and IT. The steps are those of the task-optimised paradigm above.

## Results

The paper reports that object-recognition performance across the tested models tracks how well they predict IT responses, and that the best-performing models predict better than earlier, less optimised ones.

## Limitations

A prediction score is not a mechanism. The test used a fixed set of stimuli and recording sites, and the caveats above apply.

## Connections

- Parent topic: [NeuroAI](../index.md)
- Other method on this topic: [Grid-Like Units in Navigating Networks](../grid-like-units/index.md)

## References

### Seminal papers

- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — Shows that deep networks trained for object recognition predict neural responses in higher visual cortex.
- Banino, A., et al. (2018). Vector-based navigation using grid-like representations in artificial agents. *Nature*. https://doi.org/10.1038/s41586-018-0102-6 — Shows that grid-like units emerge in a recurrent agent trained to navigate.
- Hassabis, D., Kumaran, D., Summerfield, C. & Botvinick, M. (2017). Neuroscience-Inspired Artificial Intelligence. *Neuron*. https://doi.org/10.1016/j.neuron.2017.06.011 — The classic review of how neuroscience has inspired AI, and how AI can test ideas about the brain.
- Richards, B. A., et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — Argues for studying the brain through objective functions, learning rules and architectures.

### Surveys and textbooks

- Schrimpf, M., et al. (2021). The neural architecture of language: Integrative modeling converges on predictive processing. *PNAS*. https://doi.org/10.1073/pnas.2105646118 — Shows that next-word-prediction language models predict brain responses in the language network, and that better prediction goes with better brain fit.
