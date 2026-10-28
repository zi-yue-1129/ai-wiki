---
status: complete
last_reviewed: 2026-10-28
related:
  - society/copyright
tags:
  - security
  - provenance
  - detection
aliases:
  - Watermarking
  - LLM Watermark
  - Text Watermark
  - 浮水印
  - 語言模型浮水印
---

# Watermarking model output

Watermarking embeds a statistical signal in generated text, so that a detector can later tell that a passage came from a particular model. The signal is meant to be invisible to readers and detectable from a short span of tokens. Watermarks are a provenance tool, and they are weaker than a promise of detection: a determined person can often remove or rewrite the signal.

This page is part of [LLM Application Security](index.md).

## Overview

As generated text becomes fluent, people and platforms want to know where it came from. Two broad approaches exist. Passive detection classifies a passage after the fact, from its style or its statistics. Watermarking changes the generation itself, so that the output carries evidence of its source. Watermarking requires the model's owner to cooperate, while passive detection does not. The two approaches have different failure modes.

## Key concepts

- **Watermark:** a statistical bias introduced into generation, which a detector can test for.
- **Detector:** the procedure that decides whether a passage carries the watermark, usually with a false-positive rate set in advance.
- **Robustness:** whether the watermark survives edits, paraphrase or translation.
- **Undetectability:** whether the watermarked text is indistinguishable from ordinary text to someone without the key.

## How it works

Watermarking methods typically modify the probability distribution used when sampling each token. A secret key and the preceding tokens determine a subset of tokens that are favoured. Over a passage, the favoured tokens appear more often than chance, and a detector with the key tests for this excess. Kirchenbauer et al. (2023) propose a watermarking framework for proprietary language models, in which the signal is embedded with little loss of quality and detected from a short span of tokens. Christ et al. (2023) ask whether a watermark can be undetectable while still being detectable with the key, and study the question formally. Zhao et al. (2023) study watermarks that stay robust under edits, with provable guarantees for the detector.

Passive detection is also studied. Mitchell et al. (2023) propose DetectGPT, which decides whether a passage came from a model using its log probabilities, without training a classifier or watermarking. Sadasivan et al. (2023) ask whether AI-generated text can be reliably detected at all.

## Limitations

- **Removal by rewriting.** Krishna et al. (2023) show that paraphrasing can evade several detectors, including a watermark, and that a retrieval-based defence works better against paraphrase.
- **Open models.** A watermark applies only where the generator is controlled by the provider, and open-weight models can be run without it.
- **False positives.** Detectors must keep the rate of wrongly flagged human text low, which limits how weak a signal they can use.
- **Scope.** Watermarks for text do not solve attribution for images, audio or edited content.

## Connections

- Watermarks can help trace copies made through an API; see [Model extraction and theft](model-extraction.md).
- Questions of ownership and reuse of generated and training content are covered on [Copyright and AI](../../society/copyright/index.md).
- The threats to applications built on models are on [LLM Application Security](index.md).

## Applications

- Provenance labels on platforms that host generated text.
- Detection of mass-produced content, where a detector's error rate is acceptable.

## Open questions

- Can a watermark survive aggressive paraphrase without raising the false-positive rate?
- How should detection be used in settings, such as education, where a wrong flag has serious consequences?

## References

### Seminal papers

- Kirchenbauer, J. et al. (2023). A Watermark for Large Language Models. ICML. https://arxiv.org/abs/2301.10226 — Proposes a watermarking framework for language models that is detectable from a short span of tokens.
- Christ, M., Gunn, S. & Zamir, O. (2023). Undetectable Watermarks for Language Models. arXiv. https://arxiv.org/abs/2306.09194 — Studies watermarks that are undetectable without the key, and their formal guarantees.
- Zhao, X. et al. (2023). Provable Robust Watermarking for AI-Generated Text. arXiv. https://arxiv.org/abs/2306.17439 — Proposes watermarks that stay robust under edits, with a provable detector.
- Mitchell, E. et al. (2023). DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature. ICML. https://arxiv.org/abs/2301.11305 — A passive detector based on the curvature of a model's log probabilities, without a watermark.
- Krishna, K. et al. (2023). Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense. arXiv. https://arxiv.org/abs/2303.13408 — Shows that paraphrasing evades several detectors, including watermarking.
- Sadasivan, V. S. et al. (2023). Can AI-Generated Text be Reliably Detected? arXiv. https://arxiv.org/abs/2303.11156 — Examines whether AI-generated text can be reliably detected.
