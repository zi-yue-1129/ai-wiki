---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - multimodal
aliases:
  - Multimodal benchmarks
  - 多模態基準
---

# Multimodal Benchmarks

Multimodal benchmarks test whether a model can combine what it sees with what it knows. The benchmarks in this family differ in what they stress: VQA v2 checks whether the image is used at all, and MMMU checks expert reasoning over images.

## Overview

Visual question answering (VQA) asks a system to answer a free-form, open-ended natural-language question about an image. The authors wanted questions that target different parts of an image and need more than a generic caption, and they built a dataset of about 0.25 million images, 0.76 million questions and 10 million answers (Agrawal et al., 2015). Because many answers are short, the task can still be scored automatically.

The first dataset had a serious flaw: a model could often answer from the question text alone. VQA v2 addresses this by pairing each question with two similar images that have different answers, so that the image must matter (Goyal et al., 2016). The paper describes the balanced dataset as having about twice the number of image-question pairs of the original. GQA follows the same concern and generates 22 million reasoning questions from scene graphs, with functional programs that control the answer distribution and reduce question bias (Hudson & Manning, 2019).

MMMU moves to expert knowledge. It contains 11.5K questions from college exams, quizzes and textbooks, across six disciplines, 30 subjects and 183 subfields, using 30 kinds of image such as charts, diagrams, maps and chemical structures. The authors report that GPT-4V reached 56% and Gemini Ultra 59%, which left substantial room for improvement (Yue et al., 2023).

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [VQA v2](vqa-v2.md) | Short open-ended answers about an image | Agreement with human answers |
| [MMMU](mmmu.md) | College-level questions with images | Accuracy, overall and per discipline |

The two benchmarks test different skills. VQA v2 is mostly about perception and grounding in simple questions. MMMU is about perception plus subject knowledge plus multi-step reasoning, so a low score can come from any of the three.

## Key concepts

- **Language prior**: a systematic answer tendency that a model learns from the question text, without looking at the image.
- **Balanced pair**: two images that look alike but give different answers to the same question, used to test whether the model reads the image.
- **Scene graph**: a structured description of objects, attributes and relations in an image, used by GQA to generate questions.

## How it works

A model receives an image and a question, usually in a text prompt, and produces an answer that is compared with the reference. Multiple-choice questions, as in MMMU, can be scored by exact match against the correct option. Open-ended answers need a normalisation step and an agreement measure against several human answers.

## Common issues

- **Language priors.** A model can answer from the question alone, which inflates scores. Balanced data counters this (Goyal et al., 2016).
- **Mixed signal.** Scores on expert questions combine perception with knowledge and reasoning, so errors are hard to attribute to one cause (Yue et al., 2023).
- **Saturation.** Recent systems score high on the older sets, which pushes new benchmarks toward harder questions.
- **Image diversity.** A benchmark that uses mostly one kind of image, such as natural photographs, says little about charts or diagrams.

## Connections

- [Vision](../vision/index.md) covers the image-only benchmarks that these tasks extend.
- [Language](../language/index.md) covers the text-only counterparts.
- [Visual perception](../../../../brain-mind/visual-perception/index.md) describes how the brain combines what it sees with prior knowledge, the question VQA raises for models.

## Open questions

- Whether multimodal benchmarks measure visual understanding or mainly the language ability of the model that reads the image.
- How to design benchmarks where a text-only model cannot score well, and to report that check with the score.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Reasoning and agents](../reasoning-agents/index.md) covers the multi-step tasks that some multimodal systems are also tested on.

## References

### Seminal papers

- Agrawal, A. et al. (2015). *VQA: Visual Question Answering*. arXiv. https://arxiv.org/abs/1505.00468 — Defines open-ended visual question answering and introduces the first large VQA dataset.
- Goyal, Y. et al. (2016). *Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. arXiv. https://arxiv.org/abs/1612.00837 — Shows that language priors inflate scores and introduces the balanced VQA v2 dataset.
- Hudson, D. A. & Manning, C. D. (2019). *GQA: A New Dataset for Real-World Visual Reasoning and Compositional Question Answering*. arXiv. https://arxiv.org/abs/1902.09506 — Generates 22 million compositional questions from scene graphs and controls answer-distribution bias.

### Articles and documentation

- Yue, X. et al. (2023). *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI*. arXiv. https://arxiv.org/abs/2311.16502 — Introduces 11.5K college-level questions across six disciplines and reports GPT-4V and Gemini Ultra results.
- Radford, A. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision*. arXiv. https://arxiv.org/abs/2103.00020 — Learns visual models from natural-language supervision, a widely used starting point for multimodal systems.
