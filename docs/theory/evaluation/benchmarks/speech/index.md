---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - speech
aliases:
  - Speech benchmarks
  - 語音基準
---

# Speech Benchmarks

Speech benchmarks test automatic speech recognition, which turns audio into text. Scores are usually word error rate on a fixed test set, so results are comparable only when the split, the text normalisation and the decoding setup match.

## Overview

Early end-to-end speech systems were trained on large amounts of transcribed speech and judged on a few standard test sets. Deep Speech, for example, replaced hand-engineered pipelines with a single recurrent network trained end to end. The authors report 16.0% error on the Switchboard Hub5'00 test set, and they note that the system handled noisy environments better than widely used commercial systems at the time (Hannun et al., 2014). Connectionist temporal classification, a training objective that aligns unsegmented audio with text, is the mechanism that made such models trainable without frame-level labels (Graves et al., 2006).

LibriSpeech provided a public, open test set built from public-domain audiobook recordings, so that systems could be compared on the same speech (Panayotov et al., 2015). Later work asked how well such scores transfer. Whisper was trained on 680,000 hours of multilingual and multitask transcripts from the internet, and its authors report that it generalises to standard benchmarks without fine-tuning and approaches human accuracy and robustness (Radford et al., 2022).

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [LibriSpeech](librispeech.md) | Transcribing read English audiobook speech | Word error rate on clean and other test sets |

LibriSpeech is the main benchmark in this family. Its clean and harder (other) test sets separate performance on easier and more difficult speech, so the two numbers should be reported together.

## Key concepts

- **Word error rate (WER)**: the number of word substitutions, deletions and insertions needed to match the reference, divided by the number of reference words.
- **Normalisation**: rules for casing, punctuation and numbers applied to both reference and hypothesis before scoring.
- **Zero-shot transfer**: testing a model on a benchmark without training on that benchmark's data, which large web-trained models can achieve (Radford et al., 2022).

## How it works

A recogniser produces a transcript for each audio file in the test set. The transcript and the reference text are normalised in the same way, aligned, and scored by WER over all test utterances. Decoding choices, such as the language model used during decoding and the beam width, change the score, so they belong to the protocol.

## Common issues

- **Normalisation.** Word error rate depends on how punctuation, casing and numbers are normalised before comparison, so the normalisation must be reported.
- **Domain shift.** Read audiobook speech differs from conversation, accents and noisy recordings, so a low error rate on one set does not carry over to others (Radford et al., 2022).
- **Training overlap.** Large web-scale training sets can contain recordings close to the test material, so the history of the test set matters.
- **Test-set noise.** Small differences in WER can fall within the variation of a single test set, so differences between close systems need a significance check.

## Connections

- [Language](../language/index.md) covers the text-only counterparts, where the same normalisation and contamination questions arise.
- [Speech models](../../../models/speech/index.md) describes the systems these benchmarks evaluate.
- [Auditory system](../../../../brain-mind/auditory-system/index.md) describes how people recognise speech, the comparison that neural benchmarks sometimes make for hearing models.

## Open questions

- How to measure the robustness of speech systems across accents, languages and conditions with benchmarks that do not reward memorising one test set.
- Whether word error rate captures what listeners find important, such as meaning, or only a surface match to the reference.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Protocols](../../protocols/index.md) covers splits and reporting.

## References

### Seminal papers

- Graves, A., Fernández, S., Gomez, F. & Schmidhuber, J. (2006). *Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks*. ICML 2006. https://doi.org/10.1145/1143844.1143891 — Introduces the CTC loss, a training objective used by many speech recognisers.
- Hannun, A. et al. (2014). *Deep Speech: Scaling up end-to-end speech recognition*. arXiv. https://arxiv.org/abs/1412.5567 — Shows end-to-end recognition trained on large amounts of speech, with 16.0% error on Switchboard Hub5'00.
- Panayotov, V., Chen, G., Povey, D. & Khudanpur, S. (2015). *Librispeech: An ASR corpus based on public domain audio books*. ICASSP 2015. https://doi.org/10.1109/ICASSP.2015.7178964 — Introduces the public-domain audiobook corpus and its test sets.

### Articles and documentation

- Radford, A. et al. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv. https://arxiv.org/abs/2212.04356 — Trains on 680,000 hours of web transcripts and reports zero-shot results across benchmarks.
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
