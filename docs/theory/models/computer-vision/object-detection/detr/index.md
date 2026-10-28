---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
  - brain-mind/attention-brain-machine
tags:
  - computer vision
  - transformers
  - attention
aliases:
  - DETR
  - DEtection TRansformer
  - 偵測 Transformer
  - 端到端物件偵測
---

# DETR

DETR (DEtection TRansformer) treats object detection as direct set prediction. A CNN extracts image features, and a Transformer encoder and decoder turn them into a fixed set of predictions, one per learned object query, in a single pass. During training, the predictions are matched one-to-one with the ground-truth objects by bipartite matching, so no anchors and no non-maximum suppression (NMS) are needed. It is one of the methods named on the [Object Detection](../index.md) page.

## Overview

Most detectors encode prior knowledge in hand-designed components: anchors, proposal rules, and an NMS threshold that removes duplicates. The DETR paper argues that a set-based loss makes many of these unnecessary. Its two ingredients are a global loss that forces unique predictions through bipartite matching, and a Transformer encoder–decoder that reasons about relations between objects and the whole image.[^1]

The paper reports that DETR matches the accuracy and speed of a well-tuned Faster R-CNN on COCO, and that the framework extends to panoptic segmentation.[^1] The main cost it reports is training time, since the schedules are long.

## Key concepts

- **Set prediction.** The model outputs an unordered set of N predictions, with N chosen well above the typical number of objects in an image. Slots without an object carry a "no object" class.
- **Object queries.** A fixed set of N learned embeddings. The decoder turns each query into one prediction, so each output slot is tied to its own query. The main model uses 100.
- **Bipartite matching.** The one-to-one assignment between predictions and ground-truth objects with the lowest total cost, computed with the Hungarian algorithm.
- **Box loss.** A generalised IoU loss plus an L1 loss on the box coordinates, with weights 2 and 5.[^2]

## How it works

A CNN backbone produces a feature map. A 1×1 convolution reduces its channels to a width of 256, and the map is flattened into a sequence with positional encodings. The encoder applies self-attention, so every position sees the whole image. The decoder runs the N object queries through self-attention and through cross-attention over the encoder output. A small feed-forward network turns each query embedding into a class probability vector, including "no object", and a normalised box.

Training first finds the optimal assignment by minimising the total matching cost:

$$
\hat{\sigma} = \arg\min_{\sigma} \sum_{i=1}^{N} \mathcal{L}_{\text{match}}\big(y_i, \hat{y}_{\sigma(i)}\big)
$$

Here \(y_i = (c_i, b_i)\) is a ground-truth object, and \(\hat{y}_{\sigma(i)}\) is the prediction assigned to it. The cost rewards a high probability for the true class and a close box. The loss is then computed on the matched pairs:

$$
\mathcal{L}_{\text{Hungarian}}(y, \hat{y}) = \sum_{i=1}^{N} \Big[-\log \hat{p}_{\hat{\sigma}(i)}(c_i) + \mathbb{1}_{\{c_i \neq \varnothing\}}\, \mathcal{L}_{\text{box}}\big(b_i, \hat{b}_{\hat{\sigma}(i)}\big)\Big]
$$

Here \(\mathcal{L}_{\text{box}}\) is the weighted sum of the generalised IoU and L1 terms. Predictions matched to "no object" contribute only to the classification term. Because each object has exactly one prediction, the loss discourages duplicates. The paper notes that decoder self-attention lets queries communicate, which removes double predictions.[^3]

The baseline trains for 300 epochs, about three days on 16 V100 GPUs. Like other Transformers, DETR uses Adam and dropout, unlike the SGD used for Faster R-CNN.[^4]

## Results

On COCO validation, the ResNet-50 DETR reaches 42.0 AP at 28 frames per second, with 41M parameters. Faster R-CNN with an FPN backbone reaches 40.2 AP at 26 frames per second with the standard schedule, and 42.0 AP with the enhanced training used for the comparison. The ResNet-101 DETR reaches 43.5 AP.[^5]

Results vary with object size. DETR's APS is 20.5, against 24.2 for Faster R-CNN with FPN, while its APL is 61.1 against 52.0.[^5] Removing the encoder drops overall AP by 3.9 points, with the largest drop on large objects. AP improves by 8.2 points across the decoder's layers.[^6]

## Limitations

- **Small objects.** The paper states that DETR is less accurate on small objects than Faster R-CNN, and expects future work to address this.[^5]
- **Training cost.** The comparison schedule runs for 500 epochs, which adds 1.5 AP over the shorter one.[^4]
- **Fixed capacity.** N is set in advance, so an image can contain at most N objects.
- **Attention cost.** Full attention over image features grows quickly with resolution. Deformable DETR attributes DETR's limited spatial resolution to this cost.[^7]

## Open questions

- **Convergence.** Deformable DETR replaces dense attention with attention over a few sampling points. It reports better accuracy than DETR, especially on small objects, with ten times fewer training epochs.[^7]
- **Small objects.** Whether a set-prediction detector can match convolutional detectors on small objects without a multi-scale design is still open.
- **Matching and duplicates.** Bipartite matching removes the need for NMS, but its effect on training stability and on crowded scenes needs more study than the paper provides.

## Connections

- **Transformers.** DETR applies the [Transformer](../../../transformer/index.md) to detection, with the same attention mechanism as [Attention Is All You Need](../../../transformer/attention-is-all-you-need/index.md).
- **Attention and competition.** Interaction between object queries, which lets one query suppress another's duplicate, is a learned competition between candidate objects. This loosely resembles the biased competition account of visual attention in [Attention in Brains and Machines](../../../../../brain-mind/attention-brain-machine/index.md). The analogy is one of organisation, not evidence of a shared mechanism.
- **Two-stage contrast.** [Faster R-CNN](../faster-rcnn/index.md) uses a learned proposal stage and NMS, both of which DETR removes.

## Applications

The paper evaluates DETR on COCO object detection and shows that the framework extends to panoptic segmentation.[^1]

## References

### Seminal papers

- Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A. & Zagoruyko, S. (2020). *End-to-End Object Detection with Transformers*. arXiv. https://arxiv.org/abs/2005.12872 — Introduces DETR, which replaces anchors and NMS with bipartite matching over a fixed set of Transformer predictions.
- Zhu, X., et al. (2020). *Deformable DETR: Deformable Transformers for End-to-End Object Detection*. arXiv. https://arxiv.org/abs/2010.04159 — Replaces dense attention with attention over a few sampling points, which speeds up convergence and helps small objects.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — The Transformer architecture, whose encoder and decoder DETR uses for detection.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage detector that DETR's accuracy and speed are compared with, and whose anchors and NMS DETR removes.
- Lin, T.-Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — The COCO dataset and the AP metric on which DETR's results are reported.

### Surveys and textbooks

- Zou, Z., et al. (2019). *Object Detection in 20 Years: A Survey*. arXiv. https://arxiv.org/abs/1905.05055 — A survey of detection methods, including the hand-designed components that DETR replaces.

[^1]: Carion et al. (2020), abstract and introduction: the set-based loss with bipartite matching and the Transformer encoder–decoder; accuracy and run-time on par with Faster R-CNN on COCO; and the extension to panoptic segmentation.
[^2]: Carion et al. (2020), Section 3 and the training details in the appendix: the box loss combines a generalised IoU term and an L1 term, with weights λ_iou = 2 and λ_L1 = 5.
[^3]: Carion et al. (2020), Section 4.2: the decoder self-attention reduces double predictions, and the ablation shows the effect of removing it.
[^4]: Carion et al. (2020), Section 4: the 300-epoch baseline trained for three days on 16 V100 GPUs, the 500-epoch comparison schedule, and the optimiser comparison with Faster R-CNN in Section 4.1.
[^5]: Carion et al. (2020), Table 1: COCO validation AP, APS and APL, GFLOPS and FPS for Faster R-CNN and DETR with ResNet-50 and ResNet-101 backbones.
[^6]: Carion et al. (2020), Table 2 and Section 4.2: AP by number of encoder layers (36.7 with none, 41.6 with 12), and the AP gain across the decoder layers.
[^7]: Zhu et al. (2020), abstract: Deformable DETR performs better than DETR, especially on small objects, with 10 times fewer training epochs.
