---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
  - brain-mind/visual-perception
tags:
  - evaluation
  - benchmarks
  - neuroscience
aliases:
  - Neuroscience benchmarks
  - 神經科學基準
---

# Neuroscience Benchmarks

Neuroscience benchmarks test how closely a model's internal responses match measured neural or behavioural data. They ask a different question from accuracy: a model can classify images well and still represent them differently from the brain.

## Overview

The idea behind these benchmarks predates the current generation of models. Yamins et al. (2014) showed that hierarchical models optimised for object recognition predict responses in higher visual cortex, which made the comparison between networks and neural recordings a practical question. Brain-Score turned that comparison into a shared benchmark: a model's internal layers are mapped to recorded neural sites and to human behavioural data on object images, and the models are ranked by how well they predict held-out data (Schrimpf et al., 2018). The same kind of comparison was later applied to language-processing areas, relating language models to responses in the brain's language network (Schrimpf et al., 2021).

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [Brain-Score](brain-score.md) | Predicting neural and behavioural responses to object images | Predictivity of held-out neural and behavioural data |

Brain-Score is the main benchmark in this family, and its page describes the datasets and scoring in detail. A high score means that a model's representation is similar to the recorded data under the mapping used. It does not show that the model computes the same way the brain does.

## Key concepts

- **Neural site**: a recorded location, such as a population of neurons in a cortical area, whose responses a model must predict.
- **Predictivity**: how well a model's responses, mapped to the recorded sites, explain held-out data, typically with a linear regression fitted on other images.
- **Representational similarity**: comparing two systems by the similarity structure of their responses to the same stimuli, rather than by matching individual units (Kriegeskorte, 2008).

## How it works

A model is run on the same images shown to an animal or person. Its activations at chosen layers are mapped to the recorded data, most often with a linear regression fitted on part of the data and tested on the rest. The score is the predictivity on the held-out part, reported for each area and for behavioural data. Because the mapping is fitted, the regression method and the choice of layer must be reported along with the number.

## Common issues

- **Mapping choice.** The score depends on how model units are mapped to neural sites, so the regression and the layer must be reported.
- **Limited recordings.** Few sites and images give wide uncertainty, so small differences between models are not reliable.
- **Similarity is not mechanism.** A high score shows that representations are similar on the test, not that the model works the same way as the brain.
- **Narrow stimuli.** Object images and short sentences are a small part of what the brain does, so a benchmark built on them says little about other functions.

## Connections

- [Visual perception](../../../../brain-mind/visual-perception/index.md) describes how the brain recognises objects, the target that the vision-model comparison aims at. The [Yamins et al. (2014) page](../../../../brain-mind/visual-perception/yamins-2014/index.md) covers the study that started this line of work.
- [Receptive fields](../../../../brain-mind/neuroscience/receptive-fields-hubel-wiesel/index.md) explain the hierarchical cortical organisation that these models are compared with.
- [Vision](../vision/index.md) covers the image benchmarks that models are trained on.

## Open questions

- Whether a model that scores highly on several neural datasets has learned the same computation as the brain, or only a similar mapping from stimulus to response.
- How to extend the comparison beyond vision and language to decisions, memory and motor control, where recordings are harder to collect.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Protocols](../../protocols/index.md) covers splits and reporting.

## References

### Seminal papers

- Yamins, D. L. K. et al. (2014). *Performance-optimized hierarchical models predict neural responses in higher visual cortex*. PNAS. https://doi.org/10.1073/pnas.1403112111 — Shows that object-recognition models predict responses in higher visual cortex.
- Kriegeskorte, N. (2008). *Representational similarity analysis – connecting the branches of systems neuroscience*. Frontiers in Systems Neuroscience. https://doi.org/10.3389/neuro.06.004.2008 — Introduces comparing systems by the similarity structure of their responses.
- Kell, A. J. E. et al. (2018). *A Task-Optimized Neural Network Replicates Human Auditory Behavior, Predicts Brain Responses, and Reveals a Cortical Processing Hierarchy*. Neuron. https://doi.org/10.1016/j.neuron.2018.03.044 — Applies the same task-optimised comparison to auditory cortex and human behaviour.

### Articles and documentation

- Schrimpf, M. et al. (2018). *Brain-Score: Which Artificial Neural Network for Object Recognition is most Brain-Like?* bioRxiv. https://doi.org/10.1101/407007 — Introduces the benchmark and its neural and behavioural scores.
- Schrimpf, M. et al. (2021). *The neural architecture of language: Integrative modeling converges on predictive processing*. PNAS. https://doi.org/10.1073/pnas.2105646118 — Extends the same framework to language-processing areas.
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
