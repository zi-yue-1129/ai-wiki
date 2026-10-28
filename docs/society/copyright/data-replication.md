---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 資料重現
  - Data replication
---

# Data Replication in Diffusion Models

!!! info "Part of Copyright & IP"
    This method page belongs to [Copyright & IP](index.md). It explains one study in detail; the parent page compares it with others.

Somepalli et al. (2022) asked whether image diffusion models copy their training images or generalise from them. Their answer is that some models copy in specific cases, and that the amount of copying depends on training choices such as the size and duplication of the training set. The study matters for copyright because direct copying of a protected image is the clearest route to an infringing output.

## Problem

A diffusion model is trained on a large collection of image–caption pairs and learns to generate new images from a text prompt. Its training data often include copyrighted art and photographs. The question is whether the model produces new images that reflect general style and content, or whether it reproduces particular training images closely enough to be a copy.

## Core idea

Generate images from prompts that match training captions, then search the training set for images that closely resemble each generated image. If a generated image has a near-identical match in the training data, the model has replicated that training image. The method turns a vague worry about copying into a measurable search problem.

## How the method works

1. **Choose prompts.** Use captions from the training data, so that the model is asked for content it was trained on.
2. **Generate.** Sample images from the model for each prompt.
3. **Retrieve.** For each generated image, find the most similar training images in a feature space, using a similarity measure.
4. **Inspect.** Review the closest matches to separate real copies from loose resemblance.
5. **Vary the setup.** Study how replication changes with the size of the training set and with how often an image is duplicated.

The abstract does not give every detail of steps 3 to 5. Read the paper before reusing the procedure.

## Results

The abstract reports that some diffusion models, including Stable Diffusion, "blatantly copy" from their training data in specific cases. It also says that replication depends on factors such as training set size and duplication. The abstract does not give an overall replication rate for any model, so the study should not be read as a measure of how often copying happens in practice.

## Limitations

- **No overall rate.** The abstract does not quantify how often replication occurs, so it cannot show the scale of the problem across all outputs.
- **Limited scope.** The abstract lists the datasets used (including Oxford flowers, CelebA, ImageNet and LAION subsets). Results may not extend to other models, datasets or prompting styles.
- **Matching is a judgement.** Deciding that two images are copies depends on a similarity threshold and on manual inspection, which can disagree with a legal test for copying.

## Connections

- The companion method, extraction of training images from a trained model, is on the [Extracting training data from diffusion models](diffusion-extraction.md) page.
- Memorisation of training data is the same mechanism that raises privacy questions. See [Privacy and Data Protection](../privacy/index.md).
- Replication also bears on the legal questions about training and output in [Law, Policy & Governance](../governance/index.md).

## Open questions

- How should a replication rate be measured so that results compare across models?
- Does replication of a training image always count as copying in law, or do the facts of each case matter?
- Can deduplication of training data reduce replication without lowering the quality of the model?

## References

### Seminal papers

- Somepalli, G., Singla, V., Goldblum, M., Geiping, J. & Goldstein, T. (2022). Diffusion art or digital forgery? Investigating data replication in diffusion models. arXiv:2212.03860. https://arxiv.org/abs/2212.03860 — The study described on this page, with examples of direct copying and the effect of training set size and duplication.

- Carlini, N. et al. (2023). Extracting training data from diffusion models. arXiv:2301.13188. https://arxiv.org/abs/2301.13188 — A companion study showing that training images can be extracted from trained diffusion models.
