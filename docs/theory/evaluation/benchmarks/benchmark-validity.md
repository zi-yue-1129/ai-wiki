---
related:
  - engineering/evaluation
  - society/ethics
tags:
  - evaluation
  - benchmarks
  - construct validity
  - ethics
last_reviewed: 2026-11-01
aliases:
  - AI and the Everything in the Whole Wide World Benchmark
  - Benchmark validity
  - 基準的構念效度
  - 基準批判
---

# Benchmark Validity: "AI and the Everything in the Whole Wide World Benchmark" (Raji et al., 2021)

Raji, Bender and Paullada (2021) argue that a small set of influential AI benchmarks is treated as a measure of general progress, and that this reading lacks construct validity. A benchmark can show that a system does well on a finite, specific set of tasks, but the paper argues that the claim to general capability is not supported by that evidence (Raji et al., 2021).

## Overview

Several subfields rely on a few benchmarks as stand-ins for common problems, and the field treats these as milestones on the way to flexible, general AI systems. State-of-the-art results on them are read as progress toward those goals. The paper examines the limits of this practice, and asks what a benchmark can actually support as evidence (Raji et al., 2021).

The title is a deliberately exaggerated image. The authors say that the imagined "general" benchmark does not exist, because each real benchmark is finite, specific and contextual (Section 4).

## Key concepts

- **Construct validity**: whether a test measures the property it claims to measure. A benchmark has construct validity for a capability only if its tasks represent that capability well.
- **Benchmark as stand-in**: a dataset used in place of a broad goal, such as general object recognition or general language understanding (Section 3).
- **Aggregate metric**: a single number that can hide differences between tasks, between groups of users, or between kinds of error.

## The argument

The authors identify three groups of validity problems. Each group is discussed in Section 4 of the paper.

**Limited task design.** Tasks are often chosen for convenience or heuristics rather than systematically. Linguistic competence is also conflated with world knowledge and commonsense reasoning, which text-only tasks cannot fully test (Sections 4.1.1 and 4.1.2).

**De-contextualised data and reporting.** Datasets are closed and bounded in time, and they can be skewed toward particular contexts. No dataset is neutral, and English-only benchmarks reflect the values and languages of their creators (Sections 4.2.1 and 4.2.2).

**Inappropriate community use.** Chasing state-of-the-art scores favours incremental gains, and aggregate metrics hide meaningful differences. Benchmark scores are also used to justify real-world applications for which they were not designed, and subgroup failures can be hidden inside an aggregate result (Sections 4.3.1 to 4.3.3).

## Recommendations

The authors do not argue that benchmarks should be made larger or more general. Adding more tasks does not solve the construct validity problem. They recommend:

- Presenting benchmarks as evaluations of concrete, well-scoped and contextualised tasks (Section 5).
- Using test suites, audits and adversarial testing (Appendix A.1).
- Analysing system outputs, including error, disaggregated and counterfactual analysis (Appendix A.2).
- Running ablation tests and measuring properties such as energy use, memory and stability (Appendix A.3 and A.4).
- Reporting performance on socially salient data slices alongside the full test set (Appendix A.2).

The authors describe benchmarking as surveying a landscape, rather than winning a contest (Section 6).

## Connections

- [ImageNet](vision/imagenet.md) and [ImageNetV2](vision/imagenet-v2.md) show the test-set fitting problem: a score on the original test set may partly reflect how that set was collected.
- [GLUE](language/glue.md) is one of the benchmarks the paper discusses, as a multi-task benchmark whose combined score can hide task-level differences (Wang et al., 2018).
- Model cards and datasheets for datasets are proposals for documenting what a model or dataset is for, which addresses the context problem the paper raises (Mitchell et al., 2019; Gebru et al., 2018).

## Applications

The paper's recommendations apply when a team reports a benchmark score as evidence of readiness for a product or a population. The disaggregated evaluation that the authors recommend is the kind of analysis that revealed intersectional accuracy gaps in commercial gender classifiers (Buolamwini & Gebru, 2018).

## Open questions

- Which capabilities can a benchmark measure with construct validity, and how can a team show that its tasks represent the capability.
- How to report progress on broad capabilities without relying on a single headline benchmark.

## References

### Seminal papers

- Raji, I. D., Bender, E. M. & Paullada, A. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — A position paper on the construct validity of influential AI benchmarks, with the validity problems and recommendations discussed on this page.
- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — A multi-task benchmark whose combined score is one of the stand-ins the paper examines.
- Russakovsky, O. et al. (2014). *ImageNet Large Scale Visual Recognition Challenge*. arXiv. https://arxiv.org/abs/1409.0575 — A benchmark whose test set is discussed in relation to the paper's arguments.
- Buolamwini, J. & Gebru, T. (2018). *Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification*. PMLR 81:77–91. https://proceedings.mlr.press/v81/buolamwini18a.html — Disaggregated evaluation that finds intersectional accuracy disparities hidden by aggregate scores.

### Documentation and critique

- Gebru, T. et al. (2018). *Datasheets for Datasets*. arXiv. https://arxiv.org/abs/1803.09010 — A proposal to document a dataset's motivation, composition and recommended uses.
- Mitchell, M. et al. (2019). *Model Cards for Model Reporting*. FAT* '19, pp. 220–229. https://doi.org/10.1145/3287560.3287596 — A proposal to document a model's intended use and evaluation.
- Bender, E. M., Gebru, T., McMillan-Major, A. & Shmitchell, S. (2021). *On the Dangers of Stochastic Parrots* FAccT '21, pp. 610–623. https://doi.org/10.1145/3442188.3445922 — A critique of the scale and documentation of large language models.
