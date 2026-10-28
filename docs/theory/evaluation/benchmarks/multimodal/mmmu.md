---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - multimodal
---

# MMMU

MMMU (Massive Multi-discipline Multimodal Understanding and Reasoning) evaluates multimodal models on college-level questions that combine images with text. It contains 11.5K questions taken from college exams, quizzes and textbooks, across six disciplines, 30 subjects and 183 subfields (Yue et al., 2023).

## Task and data

Each question includes one or more images such as charts, diagrams, maps, tables, music sheets or chemical structures, and asks a question that needs both perception and subject knowledge. The paper describes 30 heterogeneous image types, which is what separates it from earlier captioning and question-answering sets (Yue et al., 2023).

## Protocol and metric

The metric is **accuracy** over the questions, reported overall and per discipline. The score mixes two skills, reading the image and knowing the subject, so a low score can come from either. Prompting and answer extraction are part of the protocol and must be reported.

## What it shows

The benchmark was built to test advanced perception and deliberate reasoning together, rather than recognition alone (Yue et al., 2023). Its college-level content means that scores track how well a system combines what it sees with domain knowledge.

## Limitations

- **Mixed signal.** Errors cannot be attributed to perception or knowledge from the score alone.
- **Answer format.** Multiple-choice and open-ended items are scored differently, so a single number hides the mix.
- **Language priors.** A model can sometimes answer from the text without using the image, which inflates its score.

## Related

- [VQA v2](vqa-v2.md) is an earlier visual question-answering benchmark built to counter language priors.
- [MMLU](../language/mmlu.md) is the text-only knowledge benchmark that MMMU parallels.
- [Multimodal family overview](index.md) compares the benchmarks in this area.

## References

### Seminal papers

- Yue, X. et al. (2023). *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI*. arXiv. https://arxiv.org/abs/2311.16502 — Introduces the 11.5K college-level multimodal questions and their disciplines.
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — The text-only multi-subject benchmark that MMMU is modelled on.

### Articles and documentation

- Goyal, Y. et al. (2016). *Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. arXiv. https://arxiv.org/abs/1612.00837 — Shows that language priors inflate visual question-answering scores.
- Antol, S. et al. (2015). *VQA: Visual Question Answering*. arXiv. https://arxiv.org/abs/1505.00468 — Defines open-ended visual question answering and its automatic evaluation.

### Additional sources

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Describes a broad benchmark design that includes multimodal tasks.
