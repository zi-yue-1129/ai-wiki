---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/vision-transformer
  - theory/paradigms/self-supervised/masked-prediction
tags:
  - computer vision
  - transformers
  - benchmarks
aliases:
  - Segment Anything
  - Segment Anything Model
  - SAM
  - 任意分割模型
---

# Segment Anything

The Segment Anything Model (SAM) is a promptable segmentation model. Given an image and a prompt, such as a point, a box or a rough mask, it returns the masks of the objects that the prompt may refer to, without being trained on the object's class. It was trained on SA-1B, a dataset of over one billion masks collected with a model-in-the-loop data engine, and it transfers to new image distributions without retraining. It is one of the four landmark methods on the [Image Segmentation](../index.md) page.

## Overview

Most segmenters before SAM were trained for a fixed list of classes, so they could not outline an object outside that list without new labelled data. Kirillov et al. defined promptable segmentation as a task instead: the model must return a valid mask for any prompt, and when a prompt is ambiguous it should return several plausible masks. Three requirements follow, namely flexible prompts, real-time responses and ambiguity awareness, and the authors show that a simple architecture meets all three.[^1]

## Key concepts

- **Prompt**: a set of foreground or background points, a box, or a mask. The paper also reports initial experiments with free-form text.
- **Amortised cost**: the image is encoded once, and the resulting embedding is reused by any number of prompts.
- **Ambiguity awareness**: for one prompt, the model outputs several masks, such as a shirt and the person wearing it, each with a predicted IoU score.
- **Zero-shot transfer**: applying the trained model to datasets and tasks that were not seen during training.
- **Data engine**: a loop in which the model helps annotators and then produces masks itself.

## How it works

SAM has three components. The algorithm for a single image and prompt is:

1. Run the **image encoder** once. It is a Vision Transformer pre-trained with masked autoencoding and adapted to high-resolution input, and it outputs an image embedding.
2. **Embed the prompt.** Points and boxes become positional encodings combined with learned tokens; a mask prompt is embedded with convolutions.
3. **Decode.** A lightweight Transformer decoder lets the prompt tokens and the image embedding attend to each other, then outputs three masks and a predicted IoU for each.
4. **Select** the mask with the highest predicted score, or return all three when the prompt is ambiguous.

Training uses a linear combination of two standard mask losses, \(\mathcal{L} = \lambda_{focal}\mathcal{L}_{focal} + \lambda_{dice}\mathcal{L}_{dice}\). Prompts are sampled over 11 simulated interactive rounds per mask, so the model learns to refine its answer as the user adds points. The prompt encoder and mask decoder run in a web browser on a CPU in about 50 milliseconds, which makes interactive use practical.[^2]

## Results

The paper's main evaluation is zero-shot single-point segmentation on a new suite of 23 datasets, scored by mean IoU and by human ratings. Against a strong earlier interactive segmenter, SAM gives higher mIoU on 16 of the 23 datasets, by as much as about 47 IoU points, and its masks receive significantly higher human ratings on the subset studied.[^3] On instance segmentation with boxes from a detector, a fully supervised pipeline remains more accurate than SAM on COCO, and the gap is smaller on a second dataset with higher-quality masks.

## Limitations

The authors note that SAM "can miss fine structures", sometimes hallucinates small disconnected components, and does not draw boundaries as crisply as methods that spend more computation. Dedicated interactive methods can outperform it when many points are given. The paper also reports a bias when segmenting clothing across perceived gender presentation with a single point prompt, and advises caution.

## Open questions

- **Naming.** SAM segments what it is pointed at, but it does not say what the object is. A recognition model could supply the label.
- **Video.** [SAM 2](https://arxiv.org/abs/2408.00714) extends the model to video with a streaming memory, and reports better image accuracy and speed than SAM itself.[^4]
- **Specialised domains.** Whether zero-shot segmentation suffices for medicine, remote sensing or microscopy, or whether it needs domain data, is open. Compare the [U-Net](../unet/index.md) approach of training on domain images.

[^1]: Kirillov et al. (2023), Section 1: the task, model and dataset are defined together, and the model is designed to be promptable and ambiguity-aware.
[^2]: Kirillov et al. (2023), Section 3: the image embedding is computed once, and the prompt encoder and mask decoder run in about 50 ms in a browser on CPU.
[^3]: Kirillov et al. (2023), Section 7.1: the evaluation uses a single foreground point, mIoU, and a human study of mask quality.
[^4]: Ravi et al. (2024), abstract: SAM 2 is more accurate and six times faster than SAM for image segmentation.

## References

### Seminal papers

- Kirillov, A., Mintun, E., Ravi, N., et al. (2023). *Segment Anything*. ICCV. https://arxiv.org/abs/2304.02643 — The paper itself: a promptable segmentation model and the SA-1B dataset.
- Ravi, N., et al. (2024). *SAM 2: Segment Anything in Images and Videos*. arXiv. https://arxiv.org/abs/2408.00714 — The successor that extends promptable segmentation to video with a memory.
- He, K., Chen, X., Xie, S., Li, Y., Dollár, P. & Girshick, R. (2022). *Masked Autoencoders Are Scalable Vision Learners*. CVPR. https://arxiv.org/abs/2111.06377 — The masked-image pre-training that the SAM image encoder uses.
- Lin, T.-Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV. https://arxiv.org/abs/1405.0312 — The COCO benchmark on which the reported detection and segmentation results are measured.
- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR. https://arxiv.org/abs/2010.11929 — The Vision Transformer on which the SAM image encoder is built.

### Surveys and textbooks

- Minaee, S., Boykov, Y., Porikli, F., Plaza, A., Kehtarnavaz, N. & Terzopoulos, D. (2021). *Image Segmentation Using Deep Learning: A Survey*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3059968 — Places promptable and interactive segmentation alongside the earlier deep segmentation families.
