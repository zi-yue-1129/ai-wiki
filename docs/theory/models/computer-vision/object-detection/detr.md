---
status: draft
last_reviewed: 2026-11-03
tags:
  - computer vision
  - object detection
  - transformer
aliases:
  - DETR
  - Detection Transformer
  - Deformable DETR
  - 檢測 Transformer
  - 偵測 Transformer
---

# DETR (Detection Transformer)

DETR treats object detection as direct set prediction. A transformer outputs a fixed set of object predictions in one pass, and a bipartite matching during training assigns each prediction to at most one ground-truth object. The design removes the anchors and the non-maximum suppression that most detectors use (Carion et al., 2020).

This page is part of [Object Detection](index.md).

## Overview

Most detectors before DETR were built from hand-designed parts: anchors that define candidate boxes, a proposal or assignment rule that matches candidates to objects, and non-maximum suppression (NMS) that removes duplicates afterwards. Each part encodes assumptions about object sizes and overlaps. DETR asks whether detection can instead be trained as one prediction problem, with the network learning the assignment itself.

## Key concepts

- **Object queries**: a fixed set of learned embeddings. Each query is decoded into one prediction for a box and a class, or for "no object".
- **Bipartite matching**: a one-to-one assignment between the predicted set and the ground-truth set, found with the Hungarian algorithm.
- **Set loss**: the training loss computed on the matched pairs, which makes duplicates costly and so removes the need for NMS.
- **Parallel decoding**: all queries are decoded together at each layer, rather than one object after another as in autoregressive decoding.

## How it works

A convolutional backbone extracts image features. A transformer encoder refines them, and a transformer decoder takes the **N = 100** object queries and attends to the image features. Each query produces one class and one box. Unlike the autoregressive decoder in the original Transformer, the paper decodes all N objects in parallel at each decoder layer.

During training, the Hungarian algorithm matches the N predictions to the ground-truth objects, and the loss is applied to each matched pair. Unmatched predictions are trained toward "no object". The paper adds prediction feed-forward networks and the Hungarian loss after every decoder layer. The layer-wise results show that accuracy improves at each depth. The ablation model uses six encoder and six decoder layers with width 256.

## Key methods

This page is the detail for one of the landmark methods in the [Object Detection](index.md) overview. Its closest relatives are:

- **Faster R-CNN**: the two-stage design with an explicit proposal stage and NMS-style post-processing ([Faster R-CNN](faster-r-cnn.md)).
- **YOLO**: a one-stage grid design ([YOLO](yolo.md)).
- **RetinaNet**: a one-stage detector with an anchor scheme and the focal loss ([RetinaNet](retinanet.md)).

## Results

On COCO validation, the paper reports **42.0 AP** and **62.4 AP50** for DETR with a ResNet-50 backbone, using a 500-epoch schedule. Its Faster R-CNN-FPN baseline, trained with the Detectron2 3× schedule, reaches 40.2 AP. A stronger Faster R-CNN-FPN baseline trained for 9× (109 epochs) reaches 42.0 AP. The authors conclude that DETR is competitive with Faster R-CNN at the same number of parameters.

Small objects are the weak point. The paper reports APS of 20.5 for DETR, against 24.2 for the 3× Faster R-CNN baseline and 26.6 for the 9× one. The text describes the gap as 5.5 points, but Table 1 gives 3.7 points against the first baseline and 6.1 against the second.

## Limitations

- **Small objects.** The paper itself reports lower performance on small objects.
- **Training length.** The paper states that the new model "requires extra-long training schedule", at 500 epochs against about 109 for the stronger Faster R-CNN baseline.

Deformable DETR (Zhu et al., 2020) targets both points. Its abstract reports better performance than DETR with **10 times fewer training epochs**, and better results on small objects. It attends only to a small set of key sampling points around each reference point, rather than to every position.

## Connections

The encoder and decoder of DETR are transformers, described on the [Transformer](../../transformer/index.md) page. Its backbone is a convolutional network, as on the [Convolutional Networks](../../cnn/index.md) page.

## References

### Seminal papers

- Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A. & Zagoruyko, S. (2020). *End-to-End Object Detection with Transformers*. arXiv. https://arxiv.org/abs/2005.12872 — Introduces DETR, with the object queries, bipartite matching and the COCO results used above.
- Zhu, X., Su, W., Lu, L., Li, B., Wang, X. & Dai, J. (2020). *Deformable DETR: Deformable Transformers for End-to-End Object Detection*. arXiv. https://arxiv.org/abs/2010.04159 — Replaces full attention with deformable attention over a few sampling points, reporting 10 times fewer training epochs than DETR.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage baseline that DETR's COCO results are compared with.
- Girshick, R. (2015). *Fast R-CNN*. arXiv. https://arxiv.org/abs/1504.08083 — The detector head used inside the Faster R-CNN baseline.

### Surveys and benchmarks

- Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick, R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L. & Dollár, P. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — The COCO benchmark and the AP metric in which the DETR results are reported.
