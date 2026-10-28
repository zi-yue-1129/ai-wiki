---
status: draft
last_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - probing
  - controls
aliases:
  - 控制任務
  - 選擇性
  - Control tasks
  - Selectivity
---

# Control tasks and selectivity

!!! info "Part of Probing classifiers"
    This method page belongs to [Probing classifiers and representation analysis](probing.md). It explains the method in detail; the parent page compares it with the other probing methods.

A control task is a probing task whose labels are random, assigned per word type, so that only the probe itself can learn them. Selectivity is the probe's accuracy on the real linguistic task minus its accuracy on the control task. Hewitt and Liang (2019) proposed both so that a high probe score can be read as evidence of what the representation encodes, rather than of what the probe can memorise.

## Problem

A probe that scores well on a linguistic task may have learned the task, or it may have memorised information from a flexible classifier. Accuracy alone does not separate the two. The problem is to measure how much of the probe's score comes from the representation.

## Core idea

Build a control task by giving every word type a random output label. A representation that encodes the linguistic property should score high on the real task and low on the control task. A probe that scores high on both is memorising rather than reading the representation. Selectivity records the gap between the two scores.

## Equation

For a linguistic task \(T\) and its control \(C\), the selectivity of a probe is

\[
\mathrm{Sel} = \mathrm{Acc}_T - \mathrm{Acc}_C.
\]

Probes are compared by selectivity rather than by raw accuracy, which places each result in the context of the probe's capacity.

## Results

The paper argues that selectivity places linguistic task accuracy in context with a probe's capacity to memorise word-type labels. The authors argue that probes which report high accuracy on linguistic tasks can also memorise word-type labels, so accuracy alone overstates what a representation contains.

## Limitations

- **Design dependence.** The control task must be built carefully, because a poorly designed control can be too easy or too hard for the probe.
- **Probe family.** Selectivity depends on the probe family being compared, so the same representation can receive different scores under different families.
- **Scope.** Selectivity says whether the probe reads a property beyond memorisation; it does not show that the model uses the property.

## References

### Seminal papers

- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — Introduces control tasks and selectivity to separate probe memorisation from encoded information.
- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. *arXiv preprint*. https://arxiv.org/abs/1610.01644 — The linear-probe method on which control tasks are built.
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — A probing study that reports on syntactic structure in contextual embeddings.

### Surveys and textbooks

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — Reviews probing methods, including the design of controls, and their limitations.
- Li, K. et al. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — Pairs a probe with interventions, a different check on what a representation is used for.
