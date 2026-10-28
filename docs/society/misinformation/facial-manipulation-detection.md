---
status: complete
last_reviewed: 2026-10-28
aliases:
  - 人臉操縱偵測
  - FaceForensics++
  - Facial manipulation detection
---

# Facial Manipulation Detection (FaceForensics++)

!!! info "Part of Misinformation & Deepfakes"
    This method page belongs to [Misinformation & Deepfakes](index.md). It explains one benchmark in detail; the parent page compares it with other responses.

Rössler et al. (2019) built FaceForensics++, a public benchmark for detecting manipulated facial images and video. It covers four manipulation methods and includes variations in compression, so that detectors can be tested under realistic conditions. Its test labels are held back on a server, so that results can be compared fairly on the same data.

## Overview

Face-swap and face-reenactment tools can produce convincing fake video. Detection research needs data that is large, varied and labelled, and it has to be compared on shared data to be meaningful. FaceForensics++ supplies both, and it became a common yardstick for detectors.

## Key concepts

- **Face manipulation**: an edit that replaces or moves a person's face in an image or video, such as a face swap or a reenactment.
- **Compression artefacts**: distortions from video compression, which can hide traces that detectors rely on.
- **Hidden test set**: a test split whose labels are not released, so that a method cannot be tuned on it directly.

## Problem

Detection needs data that is large, varied and labelled, but manipulated video is hard to collect at scale, and detectors trained on one set of fakes often fail on others. The problem is to build a benchmark that makes detector comparison fair.

## How the benchmark works

1. **Manipulate.** Apply four methods (DeepFakes, Face2Face, FaceSwap and NeuralTextures) to the same source footage.
2. **Vary the conditions.** Compress the manipulations at random compression levels and sizes, so that detectors are not tested only on clean files.
3. **Hide the test set.** Keep the labels of the benchmark test data on a server, so that results are submitted rather than tuned locally.
4. **Train and compare.** Train detectors on the labelled data and report results on the held-out split. The paper compares automated detectors with human observers.

The paper also limits submissions, to one every two weeks from a single submitter, to reduce overfitting to the test set.

## Key methods

FaceForensics++ is a benchmark rather than a single detector, so its methods are the four manipulation techniques it includes. Each technique produces fakes that differ in how they are made.

- **DeepFakes, FaceSwap**: face-swap methods that replace one identity with another.
- **Face2Face**: facial reenactment, which transfers the expressions of one person onto another.
- **NeuralTextures**: a method that learns neural textures to render the manipulated face.

## Results

The abstract reports a database of more than 1.8 million manipulated images, which it says is over an order of magnitude larger than comparable public forgery datasets. It states that a detector using domain-specific knowledge reaches unprecedented accuracy and clearly outperforms human observers. It gives no single numeric detection accuracy in the abstract, so the numbers should be read from the paper's tables.

## Limitations

- **Four methods.** The benchmark covers four manipulation methods. Detectors trained on it may not transfer to newer generators, which the field has continued to produce.
- **Arms race.** A benchmark fixes the conditions at one point in time. New generation methods and new compression pipelines can make the detectors out of date.
- **Human comparison.** The result that detectors beat human observers does not say that detectors are reliable enough to act on alone, because false positives harm real people.

## Variants and more variants

- **Benchmark-trained detectors**: the detectors in the paper are trained on this data and compared on its held-out split.
- **Provenance**: a different approach that records authenticity at creation, such as C2PA, covered in the connections below.

## Connections

- Detection is one response to fakes. Provenance standards such as C2PA take the opposite approach, recording authenticity at creation. See [Misinformation & Deepfakes](index.md).
- The spread of false content, which detection does not address, is covered on [How False News Spreads](spread-of-false-news.md).
- Synthetic faces also raise privacy questions, covered in [Privacy and Data Protection](../privacy/index.md).

## Applications

- Screening uploaded video on platforms, with human review of flagged cases.
- Research benchmarking, where the same split allows detectors to be compared directly.

## Open questions

- How should detectors be evaluated for generators that were not in the training data?
- Can detection keep pace with generation, or will provenance have to carry most of the load?
- How should detection errors be weighed against the harm of wrongly labelling real footage as fake?

## References

### Seminal papers

- Rössler, A., Cozzolino, D., Verdoliva, L., Riess, C., Thies, J. & Nießner, M. (2019). FaceForensics++: Learning to Detect Manipulated Facial Images. arXiv. https://arxiv.org/abs/1901.08971 — The benchmark described on this page, with four manipulation methods, compression variations and a held-out test set.
- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359, 1146–1151. https://doi.org/10.1126/science.aap9559 — Shows that false content spreads widely through human sharing, which detection alone does not stop.
- Chesney, B. & Citron, D. (2019). Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — Legal analysis of deepfake harms, including the case for going beyond detection.

### Articles and documentation

- C2PA. *Content Credentials: C2PA Technical Specification*. https://spec.c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html — The technical specification for signed provenance records, an alternative to detection after publication.
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — The official text of the AI Act. This page does not summarise its transparency rules for synthetic content.
