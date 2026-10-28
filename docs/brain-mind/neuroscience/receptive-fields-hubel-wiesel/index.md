---
status: complete
last_reviewed: 2026-10-28
related:
- theory/models/cnn
tags:
- neuroscience
- vision
aliases:
  - 視覺皮質的感受野
  - Receptive Fields in Visual Cortex
  - Hubel and Wiesel
---

# Single-neuron recording in visual cortex (Hubel & Wiesel, 1962)

Single-neuron recordings in cat visual cortex show cells that respond to oriented edges, and cells that respond to such edges across a wider region. This two-level pattern is the biological starting point for the hierarchical feature detectors used in convolutional networks.

This page is part of [Neuroscience Basics](../index.md). It covers one landmark study in detail.

## Overview

Light falling on the retina is a grid of brightness values, with no edges or shapes labelled. Hubel and Wiesel asked how the visual cortex turns that input into the features we see. Their answer was that individual neurons each respond to a small, specific pattern, and that neurons higher up combine these patterns into larger ones.

## Key concepts

- **Receptive field**: the region of the visual field in which a stimulus changes a neuron's firing.
- **Simple cell**: a neuron with separate on and off subregions, which responds to an edge at a preferred orientation and position.
- **Complex cell**: a neuron that responds to an edge at a preferred orientation anywhere inside a larger region, without a fixed position.
- **Orientation selectivity**: the neuron's firing depends strongly on the angle of an edge, which is the feature the cell detects.

## Problem

How does the visual cortex build representations of edges and shapes from light falling on the retina? Before this work, the receptive fields of cells in the cortex were largely unknown, so it was unclear what features the cortex computed.

## Core idea

Record single neurons in the primary visual cortex of anaesthetised cats while presenting spots and bars of light at different positions and orientations. The cells were then sorted by their response pattern: simple cells, with fixed on and off regions, and complex cells, which pool over a wider region. The authors proposed that complex cells receive input from several simple cells with the same orientation preference, which builds a larger, position-tolerant feature from smaller, position-specific ones.

## Method

1. Present a stimulus, such as a bar of light, at a given position and orientation.
2. Record the spikes of the neuron.
3. Map the receptive field from the responses, marking its on and off regions.
4. Classify the cell as simple or complex from its response pattern.

## Results

The study found orientation-selective cells in the cat primary visual cortex, arranged in the simple and complex classes described above. The reported hierarchy, in which complex cells pool the outputs of simple cells, is the idea that later inspired hierarchical feature detectors in computer vision. The paper is a qualitative description of recorded cells, not a fitted model with numerical benchmarks.

## Limitations

- **Anaesthetised cats.** The recordings were made under anaesthesia, which may change the responses of cortical cells compared with an awake animal.
- **A simplified hierarchy.** Later work found that cortical cells are more varied than two categories suggest, and that the response of a complex cell is not purely a sum of simple-cell outputs.
- **Visual cortex only.** The study does not show how these features are used for recognition, which is a question for later work on object representations.

## Connections

- **Convolutional networks**: a convolutional layer that detects the same local feature at every position is a computational version of the simple-to-complex idea. See [Convolutional Neural Networks](../../../theory/models/cnn/index.md).
- **Visual perception in the brain**: the same object-recognition question is studied in [Visual Perception](../../visual-perception/index.md), including deep networks that predict neural responses in higher visual areas.
- **Parent topic**: [Neuroscience Basics](../index.md).

## Applications

- **Vision models**: the hierarchy of local feature detectors pooled into larger ones is a design principle in convolutional networks used for image classification and detection.
- **Clinical vision research**: receptive-field mapping is used in studies of visual disorders, to locate where in the visual pathway a deficit arises. This is a research use, not a clinical procedure described here.

## Open questions

- **How general is the simple-complex split?** Cortical cells vary more than two categories, and the boundaries between them are debated.
- **How do these features support recognition?** Receptive fields explain the local feature detectors, but not how they combine into object identity.
- **How do deep networks compare?** Comparing model units with recorded neurons is an active research area, covered in [Visual Perception](../../visual-perception/index.md).

## References

### Seminal papers

- Hubel, D. H. & Wiesel, T. N. (1959). Receptive fields of single neurones in the cat's striate cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1959.sp006308 — The first recordings of receptive fields in cat striate cortex, which introduced the on and off regions of the cell types.
- Hubel, D. H. & Wiesel, T. N. (1962). Receptive fields, binocular interaction and functional architecture in the cat's visual cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1962.sp006837 — Discovers orientation-selective simple and complex cells, the biological inspiration for hierarchical vision models.

- Hubel, D. H. & Wiesel, T. N. (1968). Receptive fields and functional architecture of monkey striate cortex. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1968.sp008455 — Extends the receptive-field results to the monkey, and describes the columnar organisation of orientation preference.
- Fukushima, K. (1980). Neocognitron: A self-organizing neural network model for a mechanism of pattern recognition unaffected by shift in position. *Biological Cybernetics*. https://doi.org/10.1007/BF00344251 — A hierarchical network of simple and complex layers, built on the Hubel and Wiesel cell types, that is an early ancestor of convolutional networks.

### Surveys and textbooks

- Neuroscience Online: An Electronic Textbook for the Neurosciences. Department of Neurobiology and Anatomy, UTHealth McGovern Medical School. https://nba.uth.tmc.edu/neuroscience/ — A free, open-access electronic textbook for the neurosciences.
- Felleman, D. J. & Van Essen, D. C. (1991). Distributed hierarchical processing in the primate cerebral cortex. *Cerebral Cortex*. https://doi.org/10.1093/cercor/1.1.1 — Maps the hierarchy of visual areas in the primate cortex, which extends the simple-to-complex idea beyond V1.
