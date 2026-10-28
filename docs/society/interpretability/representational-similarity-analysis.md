---
status: draft
last_reviewed: 2026-10-28
related:
  - society/interpretability
  - brain-mind/neuroai
tags:
  - interpretability
  - neuroscience
  - representations
aliases:
  - 表徵相似度分析
  - RSA
  - Representational similarity analysis
---

# Representational similarity analysis

!!! info "Part of Probing classifiers"
    This method page belongs to [Probing classifiers and representation analysis](probing.md). It explains the method in detail; the parent page compares it with the other probing methods.

Representational similarity analysis (RSA) compares two systems, such as a brain region and a network layer, by the structure of their responses to the same stimuli rather than by matching individual units. Kriegeskorte, Mur and Bandettini (2008) proposed the framework for systems neuroscience, and it is now also used to compare artificial networks with brains.

## Problem

Neural recordings and network activations come in different formats, with different numbers of units, so they cannot be compared unit by unit. The problem is to compare them on a common footing that does not require the units to correspond.

## Core idea

For each system, compute the dissimilarity between every pair of stimulus responses, which gives a representational dissimilarity matrix (RDM). Two systems are similar if their RDMs have similar structure, whatever the number of units in each. The comparison is therefore made between the geometries of the representations.

## Equation

For responses \(r_i\) and \(r_j\) to stimuli \(i\) and \(j\), a common choice of dissimilarity is one minus the correlation between the response patterns:

\[
\mathrm{RDM}_{ij} = 1 - \mathrm{corr}(r_i, r_j).
\]

Two systems are compared by correlating the upper triangles of their RDMs.

## Results

The paper describes the framework and shows that it can relate activity patterns across different measurement modalities, and across subjects and species. It is a framework paper, so its contribution is the method rather than a single measured effect.

## Limitations

- **Stimulus dependence.** The RDM is only defined for the stimuli used, so conclusions depend on the chosen stimulus set.
- **Metric choice.** The dissimilarity measure affects which structure is visible, and different choices can give different answers.
- **Similarity is not mechanism.** Two representations can share geometry without computing the same function.

## References

### Seminal papers

- Kriegeskorte, N., Mur, M. & Bandettini, P. (2008). Representational similarity analysis – connecting the branches of systems neuroscience. *Frontiers in Systems Neuroscience*. https://doi.org/10.3389/neuro.06.004.2008 — Defines RSA for comparing systems through their response geometry.
- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. *arXiv preprint*. https://arxiv.org/abs/1610.01644 — A different way to read layers of a network, against which RSA is often compared.
- Park, K., Choe, Y. J. & Veitch, V. (2023). The Linear Representation Hypothesis and the Geometry of Large Language Models. *arXiv preprint*. https://arxiv.org/abs/2311.03658 — Studies the geometry of concept representations in a language model.

### Surveys and textbooks

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — Reviews probing, one of the main tools for comparing representations with other systems.
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — Shows the need for controls when interpreting how well a representation matches a property.
