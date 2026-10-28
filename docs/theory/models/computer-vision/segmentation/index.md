---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/evaluation/metrics/segmentation/index.md
tags:
  - computer vision
  - image segmentation
aliases:
  - Image segmentation
  - 影像分割
  - 語意分割
  - U-Net
  - Segment Anything
---

# Image Segmentation

Image segmentation assigns a label to every pixel of an image, or to every region that a model separates from its surroundings. Where [object detection](../object-detection/index.md) returns a box around each object, segmentation returns the object's exact shape, so it is used when the outline matters: a tumour boundary, a road surface, or the edge of a part on a production line.

## Overview

The three standard variants differ in what counts as one output. **Semantic segmentation** gives each pixel a class, and two objects of the same class are not separated. **Instance segmentation** gives each object its own mask, so that two cars are two masks even though they share a label. **Panoptic segmentation** combines the two: every pixel receives a class, and "stuff" regions such as sky or road are covered together with countable "thing" objects. Kirillov et al. (2018) introduced the panoptic task and define it as unifying the semantic and instance tasks.

Quality is measured by overlap between predicted and reference masks, usually with [intersection over union (IoU)](../../../evaluation/metrics/segmentation/iou.md) and the [Dice coefficient](../../../evaluation/metrics/segmentation/dice.md).

## Key concepts

- **Mask**: a binary or per-class map over pixels that marks the region of one object or class.
- **Encoder–decoder**: a network that first reduces the resolution to capture context, then restores it to produce a full-size map.
- **Skip connection**: a link that passes high-resolution features from the encoder to the decoder, so that fine boundaries can be recovered.
- **Promptable segmentation**: a model that produces a mask for the object indicated by a point, box or text prompt.

## How it works

**Fully convolutional networks.** Long, Shelhamer and Darrell (2014) showed that a classification network can be converted into a network that outputs a dense map and can be trained end to end from pixels to pixels. Their abstract reports that such networks exceed the state of the art in semantic segmentation at the time.

**U-Net.** Ronneberger, Fischer and Brox (2015) built a symmetric encoder–decoder with skip connections. The contracting path captures context, and the expanding path recovers localisation. The paper reports that the architecture can be trained end to end from very few images, relying on strong data augmentation. It was designed for biomedical images, and the same design is also used as the denoising network in many diffusion models.

**Instance segmentation.** Mask R-CNN (He et al., 2017) adds a branch that predicts an object mask in parallel with the box branch of Faster R-CNN. Masks are predicted for each region of interest, which gives instance masks from one network.

**Promptable segmentation.** Segment Anything (Kirillov et al., 2023) trains a model to return a mask for any object indicated by a prompt, so that it can transfer zero-shot to new image distributions. Its authors released the SA-1B dataset, which the abstract describes as 1 billion masks on 11 million images.

## Key methods

Brief comparison. Each method named above is a candidate for its own method page; those pages are not yet written, so the detail is given here for now.

- **FCN (semantic)**: dense prediction by converting a classifier. Simple and general, with coarse boundaries.
- **U-Net (semantic, encoder–decoder)**: skip connections for precise boundaries, trained from few annotated images.
- **Mask R-CNN (instance)**: a mask head on top of a two-stage detector, giving one mask per object.
- **Segment Anything (promptable)**: prompt-driven masks with broad zero-shot transfer.

## Connections

The U-Net design is covered in more detail on the [U-Net](../cnn/unet/index.md) page. Its use as the denoising network of diffusion models links this topic to [Generative Models](../../../paradigms/unsupervised/density-and-generative-models/generative-models/index.md). The metrics are on the [Segmentation metrics](../../../evaluation/metrics/segmentation/index.md) page.

Segmentation also connects to vision science. Separating a figure from its background is a central problem in perception, and models that segment images are sometimes compared with neural data. A good mask on a benchmark does not by itself show that a model perceives regions as people do.

## Applications

- **Medical imaging.** Outlining organs, lesions and tumours in scans, the setting in which U-Net was first developed. See [Healthcare](../../../../applications/healthcare/index.md).
- **Autonomous driving.** Labelling road surfaces, lanes and free space for planning. See [Autonomous Driving](../../../../applications/autonomous-driving/index.md).
- **Remote sensing and agriculture.** Mapping land cover and field boundaries from aerial images.

## Open questions

- Annotation is expensive, and the masks in benchmarks may not match the boundaries that users need.
- Panoptic and instance quality are hard to compare across datasets with different class definitions.
- Promptable models depend on the prompt, and it is not clear how reliably they handle ambiguous prompts.
- Extending segmentation from still images to video, with consistent identities over time, is an active area.

## References

### Seminal papers

- Long, J., Shelhamer, E. & Darrell, T. (2014). *Fully Convolutional Networks for Semantic Segmentation*. arXiv. https://arxiv.org/abs/1411.4038 — Converts classification networks into fully convolutional networks trained end to end for dense prediction.
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. arXiv. https://arxiv.org/abs/1505.04597 — Introduces the U-Net encoder–decoder with skip connections, trained from few images with heavy data augmentation.
- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN*. arXiv. https://arxiv.org/abs/1703.06870 — Adds a mask branch to Faster R-CNN, predicting an object mask in parallel with the box.
- Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., Dollár, P. & Girshick, R. (2023). *Segment Anything*. arXiv. https://arxiv.org/abs/2304.02643 — A promptable segmentation model trained on the SA-1B dataset, with zero-shot transfer to new image distributions.
- Kirillov, A., He, K., Girshick, R., Rother, C. & Dollár, P. (2018). *Panoptic Segmentation*. arXiv. https://arxiv.org/abs/1801.00868 — Defines panoptic segmentation as a unification of semantic and instance segmentation.

### Surveys and benchmarks

- Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick, R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L. & Dollár, P. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — A large benchmark with instance masks and the average precision protocol used for instance segmentation results.
