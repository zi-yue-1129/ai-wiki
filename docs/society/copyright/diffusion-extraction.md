---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 從擴散模型萃取訓練資料
  - Training data extraction
---

# Extracting Training Data from Diffusion Models

!!! info "Part of Copyright & IP"
    This method page belongs to [Copyright & IP](index.md). It explains one study in detail; the parent page compares it with others.

Carlini et al. (2023) showed that training images can be extracted from trained diffusion models. Their pipeline produced over a thousand training examples from state-of-the-art models. This is evidence that memorisation in image models is not rare, and it bears on both copyright and privacy.

## Problem

Diffusion models are trained on large image collections, which can include private photographs and copyrighted works. If a model stores enough of its training data, an outside user may be able to recover that data by querying the model. The question is whether this can be done in practice, at a scale that matters.

## Core idea

Use a generate-and-filter pipeline. Generate many images from the model, then keep only the outputs that look like copies of training images. The filter is applied after generation, so the pipeline needs only sampling access to the model and a way to compare outputs with training data.

## How the method works

1. **Generate.** Sample a large number of images from the model.
2. **Filter.** Score each generated image by how closely it resembles known training data, and keep the highest-scoring candidates.
3. **Verify.** Check each candidate against the training data to confirm that it is a copy rather than a loose similarity.

The abstract describes the approach as generate-and-filter. The exact scoring and verification steps are in the paper and should be read before reuse.

## Results

The abstract reports that the pipeline extracts "over a thousand training examples from state-of-the-art models". It does not give separate counts for each model, and it does not say how many generated images were examined. The headline number therefore shows that extraction happens at scale, but it does not give a rate that can be compared across models or settings.

## Limitations

- **No per-model breakdown.** The abstract gives one total across models, so the result cannot be attributed to a specific system from the abstract alone.
- **Unknown denominator.** Without the number of generated images examined, the extraction rate is unknown.
- **Filtering choices.** The result depends on the filter. A different threshold or verification rule would change what is counted as extracted.

## Connections

- The companion study on copying by visual similarity is on the [Data replication in diffusion models](data-replication.md) page.
- The same memorisation mechanism appears in text models. See [Privacy and Data Protection](../privacy/index.md) for the text-model study and for differential privacy as a defence.
- Extraction of copyrighted works is one of the questions in [Copyright & IP](index.md) and in [Law, Policy & Governance](../governance/index.md).

## Open questions

- How many generated images must be examined to estimate an extraction rate that is comparable across models?
- Which training images are most at risk, and does duplication explain most of the risk?
- Do defences such as deduplication or differential privacy remove extraction, or only reduce it?

## References

### Seminal papers

- Carlini, N. et al. (2023). Extracting training data from diffusion models. arXiv:2301.13188. https://arxiv.org/abs/2301.13188 — The study described on this page, with a generate-and-filter pipeline that extracts over a thousand training examples.
- Somepalli, G., Singla, V., Goldblum, M., Geiping, J. & Goldstein, T. (2022). Diffusion art or digital forgery? Investigating data replication in diffusion models. arXiv:2212.03860. https://arxiv.org/abs/2212.03860 — A companion study on replication in diffusion models, with its own limits on what it shows.
