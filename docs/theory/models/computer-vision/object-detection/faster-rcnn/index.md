---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn/backbones-and-scaling
  - brain-mind/attention-brain-machine
tags:
  - computer vision
  - benchmarks
  - convolutional networks
aliases:
  - Faster R-CNN
  - 區域提議網路
  - Region Proposal Network
  - RPN
---

# Faster R-CNN

Faster R-CNN is a two-stage object detector. A small region proposal network (RPN) looks at the convolutional features of the whole image and proposes where objects might be. A second network, the Fast R-CNN head, classifies each proposal and refines its box. Because the two stages share convolutional layers, the proposals cost almost nothing to compute. It is one of the methods named on the [Object Detection](../index.md) page.

## Overview

The paper identifies region proposal computation as the bottleneck of the fastest detectors of its time: SPPnet and Fast R-CNN had made the detection network quick, but the standard proposal method, Selective Search, took about 1.5 seconds per image on a CPU in the paper's timing.[^1] The paper's central move was to generate the proposals with a network that reuses the features the detector already computes.

The lineage runs through R-CNN, which applied a CNN to each proposal separately, and Fast R-CNN, which computed convolutional features once per image and pooled them for each proposal. Faster R-CNN keeps Fast R-CNN as its second stage.

## Key concepts

- **Anchors.** At each position of the final feature map, the RPN considers nine reference boxes: three scales (box areas of 128², 256² and 512² pixels) and three aspect ratios. Each anchor gets an objectness score and four box offsets.
- **Region proposal network.** A fully convolutional network: a 3×3 convolution followed by two sibling layers, for objectness and for box regression. It runs at every position, so one pass over the image yields all the proposals.
- **RoI pooling.** Each proposal is pooled into a fixed-size feature map, so the detector's fully connected layers can process it.
- **Sharing.** The RPN and the detection head use the same convolutional layers, learned with the training schemes the paper describes.

## How it works

For each anchor, the RPN predicts an objectness score and four offsets, using the usual centre-and-size parametrisation; for example, the centre offset is \(t_x = (x - x_a)/w_a\). The loss combines a classification term and a regression term, as in Fast R-CNN:

$$
L(\{p_i\}, \{t_i\}) = \frac{1}{N_{\text{cls}}} \sum_i L_{\text{cls}}(p_i, p_i^*) + \lambda \frac{1}{N_{\text{reg}}} \sum_i p_i^* L_{\text{reg}}(t_i, t_i^*)
$$

Here \(p_i\) is the predicted probability that anchor \(i\) is an object, \(p_i^*\) is its label, \(L_{\text{reg}}\) is the smooth L1 loss, and \(\lambda\) balances the terms; the default is \(\lambda = 10\). Only positive anchors contribute to regression. Each mini-batch samples 256 anchors from one image, with positives and negatives in a ratio of up to 1:1.

Proposals are filtered by non-maximum suppression, and the head classifies the top 300 at test time. The paper's four-step alternating scheme trains the RPN, trains a detector on its proposals, uses that detector to initialise the RPN, and then fine-tunes the detector with the shared layers fixed. It also describes an approximate joint variant that ignores the gradient with respect to the proposal coordinates.

## Results

On PASCAL VOC 2007 test, with VGG-16 and 300 proposals per image, Faster R-CNN reaches 73.2% mAP when trained on VOC 2007 and 2012 trainval, and 78.8% with COCO added to the training data. On VOC 2012 test it reaches 70.4% mAP.[^1] The paper reports that Faster R-CNN and RPN underpin first-place entries in several tracks of the ILSVRC and COCO 2015 competitions.

On a K40 GPU, Selective Search with Fast R-CNN takes 1,830 ms per image. The RPN version takes 198 ms with VGG-16, about 5 frames per second. The proposal step alone falls from 1,510 ms to 10 ms.[^1]

## Limitations

- **Anchors are fixed in advance.** Scales and aspect ratios are chosen by hand. The paper's ablation shows that a single anchor per location costs three to four points of mAP, and the learned box regression matters as much as the anchors.[^1]
- **Two stages cost time.** The head still runs on every proposal.
- **Training is multi-step.** The alternating scheme has four steps, and the joint variants trade exactness for speed.
- **A fixed proposal budget.** The cap of 300 proposals at test time bounds how many objects a crowded scene can yield. The paper's benchmarks rarely reach that limit.

## Open questions

- **Are anchors needed?** [RetinaNet](../retinanet/index.md) and [DETR](../detr/index.md) show that other ways of predicting candidate boxes can work well.
- **Is the two-stage design still the best trade-off?** RetinaNet surpasses Faster R-CNN with an FPN backbone in its COCO comparison, and DETR reaches comparable accuracy without NMS. Results depend on the backbone, the schedule and the dataset.
- **Where does the proposal stage limit accuracy?** The paper's benchmarks only partly answer how far the proposal stage limits accuracy on small or unusual objects.

## Connections

- The [CNN](../../../cnn/index.md) backbone, such as the VGG-16 network of the main experiments, provides the shared features. Stronger backbones from the same family, such as [residual networks](../../../cnn/backbones-and-scaling/resnet/index.md), carry their gains over to the detector.
- The RPN is a form of attention: the abstract says it "tells the unified network where to look". This is a loose analogy to [attention-based models](../../../transformer/attention-variants/index.md), and it resembles the bottom-up stage of [saliency-based attention](../../../../../brain-mind/attention-brain-machine/saliency-map/index.md), which chooses where to look from feature contrast.

## Applications

Faster R-CNN and its variants have been used for pedestrian and vehicle detection in driving systems, for medical image analysis and for industrial inspection.

[^1]: Ren et al. (2015), Tables 3, 4, 5 and 8. The VOC mAP values depend on the training data; the timing is measured on a K40 GPU, and the Selective Search time is measured on a CPU.

## References

### Seminal papers

- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — Introduces the region proposal network, which shares convolutional features with the Fast R-CNN detector.
- Girshick, R., Donahue, J., Darrell, T. & Malik, J. (2013). *Rich feature hierarchies for accurate object detection and semantic segmentation*. arXiv. https://arxiv.org/abs/1311.2524 — R-CNN, the first of the region-based detectors, which runs a CNN on each region proposal.
- Girshick, R. (2015). *Fast R-CNN*. arXiv. https://arxiv.org/abs/1504.08083 — Computes convolutional features once per image and pools them per proposal, with a multi-task loss.
- Lin, T.-Y., Dollár, P., Girshick, R., He, K., Hariharan, B. & Belongie, S. (2016). *Feature Pyramid Networks for Object Detection*. arXiv. https://arxiv.org/abs/1612.03144 — Builds a top-down pyramid of features from a CNN backbone, which later detectors use for multi-scale detection.
- Lin, T.-Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — The COCO dataset on which Faster R-CNN's 2015 results were reported and against which later detectors are compared.
- Zou, Z., et al. (2019). *Object Detection in 20 Years: A Survey*. arXiv. https://arxiv.org/abs/1905.05055 — A broad survey of detection methods, with the region-based family placed in its historical context.
