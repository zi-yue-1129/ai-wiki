---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 人臉操縱偵測
  - FaceForensics++
  - Facial manipulation detection
---

# Facial Manipulation Detection (FaceForensics++)

!!! info "Part of Misinformation & Deepfakes"
    This method page belongs to [Misinformation & Deepfakes](index.md). It explains one benchmark in detail; the parent page compares it with other responses.

Rössler et al. (2019) built FaceForensics++, a large benchmark for detecting manipulated facial images and video. It covers four manipulation methods and includes variations in compression, so that detectors can be tested under realistic conditions. The benchmark makes it possible to compare detectors on the same data.

## Problem

Face-swap and face-reenactment tools can produce convincing fake video. Detection needs data that is large, varied and labelled, but manipulated video is hard to collect at scale, and detectors trained on one set of fakes often fail on others. The problem is to build a benchmark that makes detector comparison fair.

## Core idea

Generate manipulated videos with several methods from one source dataset, apply the same compression levels that real platforms use, keep a hidden test set so results cannot be tuned on it, and then train and compare detectors on the same split.

## How the benchmark works

1. **Manipulate.** Apply four methods (DeepFakes, Face2Face, FaceSwap and NeuralTextures) to the same source footage.
2. **Vary the conditions.** Compress the videos at several levels and at more than one size, so that detectors are not tested only on clean files.
3. **Hide the test set.** Keep a test split that is not released, to limit overfitting to the benchmark.
4. **Train and compare.** Train detectors on the labelled data and report results on the held-out split, including automated detectors and human observers.

## Results

The abstract reports a database of more than 1.8 million manipulated images, which it says is over an order of magnitude larger than comparable public forgery datasets. It states that a detector using domain-specific knowledge reaches high accuracy and clearly outperforms human observers. It gives no numeric detection accuracy, so the numbers should be read from the paper's tables.

## Limitations

- **Four methods.** The benchmark covers four manipulation methods. Detectors trained on it may not transfer to newer generators, which the field has continued to produce.
- **Arms race.** A benchmark fixes the conditions at one point in time. New generation methods and new compression pipelines can make the detectors out of date.
- **Human comparison.** The result that detectors beat human observers does not say that detectors are reliable enough to act on alone, because false positives harm real people.

## Connections

- Detection is one response to fakes. Provenance standards such as C2PA take the opposite approach, recording authenticity at creation. See [Misinformation & Deepfakes](index.md).
- The spread of false content, which detection does not address, is covered on [How False News Spreads](spread-of-false-news.md).
- Synthetic faces also raise privacy questions, covered in [Privacy and Data Protection](../privacy/index.md).

## Open questions

- How should detectors be evaluated for generators that were not in the training data?
- Can detection keep pace with generation, or will provenance have to carry most of the load?
- How should detection errors be weighed against the harm of wrongly labelling real footage as fake?

## References

### Seminal papers

- Rössler, A., Cozzolino, D., Verdoliva, L., Riess, C., Thies, J. & Nießner, M. (2019). FaceForensics++: Learning to detect manipulated facial images. *ICCV*. https://arxiv.org/abs/1901.08971 — The benchmark described on this page, with four manipulation methods and a hidden test set.
- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359, 1146–1151. https://politics.media.mit.edu/papers/Vosoughi_Science.pdf — Shows that false content spreads widely through human sharing, which detection alone does not stop.
- Chesney, B. & Citron, D. (2019). Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — Legal analysis of deepfake harms, including the case for going beyond detection.

### Articles and documentation

- C2PA. *Content Credentials specification*. https://c2pa.org/ — A signed provenance standard, an alternative to detection after publication.
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — The official text of the AI Act. This page does not summarise its transparency rules for synthetic content.
