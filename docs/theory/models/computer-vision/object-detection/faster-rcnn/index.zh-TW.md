---
translation_reviewed: 2026-10-28
---

# Faster R-CNN

Faster R-CNN 是一種雙階段物件偵測器。一個小型的區域提議網路（RPN）觀察整張影像的卷積特徵，並提出物件可能所在的位置。第二個網路，即 Fast R-CNN 頭部，對每個提議進行分類並修正其邊界框。由於兩個階段共享卷積層，提議幾乎不需要額外的計算成本。它是 [物件偵測](../index.md) 頁所列的方法之一。

## 概述

論文指出，區域提議的計算是當時最快偵測器的瓶頸：SPPnet 與 Fast R-CNN 已讓偵測網路變快，但標準的提議方法選擇性搜尋，以論文的計時，在 CPU 上每張影像約需 1.5 秒。[^1] 該論文的核心做法，是以一個重用偵測器已計算之特徵的網路來產生提議。

這條脈絡可追溯至 R-CNN 與 Fast R-CNN。R-CNN 對每個提議分別套用一次 CNN；Fast R-CNN 則對整張影像只計算一次卷積特徵，再為每個提議進行池化。Faster R-CNN 保留 Fast R-CNN 作為第二階段。

## 關鍵概念

- **錨框（anchors）。** 在最後一張特徵圖的每個位置，RPN 考慮九個參考框：三種尺度（框面積為 128²、256² 與 512² 像素）與三種長寬比。每個錨框會得到一個物件性分數與四個框偏移量。
- **區域提議網路。** 一個全卷積網路：一個 3×3 卷積，後接兩個並列的層，分別負責物件性與框回歸。它在每個位置執行，因此只需對影像做一次前向計算，就能得到所有提議。
- **RoI 池化。** 每個提議被池化為固定大小的特徵圖，使偵測器的全連接層能夠處理它。
- **共享。** RPN 與偵測頭部使用相同的卷積層，其學習方式即論文所述的訓練方案。

## 運作方式

對每個錨框，RPN 預測一個物件性分數與四個偏移量，採用慣用的中心與大小參數化方式；例如中心的偏移量為 \(t_x = (x - x_a)/w_a\)。損失結合分類項與回歸項，與 Fast R-CNN 相同：

$$
L(\{p_i\}, \{t_i\}) = \frac{1}{N_{\text{cls}}} \sum_i L_{\text{cls}}(p_i, p_i^*) + \lambda \frac{1}{N_{\text{reg}}} \sum_i p_i^* L_{\text{reg}}(t_i, t_i^*)
$$

其中 \(p_i\) 是錨框 \(i\) 為物件的預測機率，\(p_i^*\) 是其標籤，\(L_{\text{reg}}\) 是平滑 L1 損失，\(\lambda\) 用來平衡兩項；預設值為 \(\lambda = 10\)。只有正樣本錨框會參與回歸。每個小批次從單一影像中抽取 256 個錨框，正負樣本比例最多為 1:1。

提議會經過非極大值抑制，測試時頭部對前 300 個提議進行分類。論文的四步驟交替訓練方案為：先訓練 RPN，再以其提議訓練一個獨立的偵測器，接著用該偵測器初始化 RPN，最後在共享層固定的情況下微調偵測器。論文也描述了一種近似的聯合訓練變體，它忽略提議座標上的梯度。

## 結果

在 PASCAL VOC 2007 測試集上，使用 VGG-16 與每張影像 300 個提議時，Faster R-CNN 在 VOC 2007 與 2012 的 trainval 上訓練，達到 73.2% 的 mAP；若再加入 COCO 作為訓練資料，則達到 78.8%。在 VOC 2012 測試集上，它達到 70.4% 的 mAP。[^1] 論文報告，Faster R-CNN 與 RPN 是 ILSVRC 與 COCO 2015 競賽中多個賽道第一名作品的基礎。

在 K40 GPU 上，選擇性搜尋加 Fast R-CNN 每張影像需要 1,830 毫秒。使用 VGG-16 的 RPN 版本需要 198 毫秒，約每秒 5 幀。提議步驟本身則從 1,510 毫秒降至 10 毫秒。[^1]

## 限制

- **錨框預先固定。** 尺度與長寬比必須人工選定。論文的消融實驗顯示，每個位置只用一個錨框會使 mAP 下降三到四個百分點；學習而來的框回歸與錨框同樣重要。[^1]
- **兩個階段耗費時間。** 頭部仍需對每個提議執行。
- **訓練是多步驟的。** 交替訓練方案有四個步驟，而聯合變體則以精確性換取速度。
- **固定的提議預算。** 測試時 300 個提議的上限，限制了擁擠場景能產生的物件數量。論文的基準很少達到這個上限。

## 開放問題

- **是否仍需要錨框？** [RetinaNet](../retinanet/index.md) 與 [DETR](../detr/index.md) 顯示，其他預測候選框的方式也能運作良好。
- **雙階段設計是否仍是最佳的取捨？** RetinaNet 在論文的 COCO 比較中超越了帶有 FPN 骨幹網路的 Faster R-CNN；DETR 則在不使用 NMS 的情況下達到相近的準確率。結果取決於骨幹網路、訓練排程與資料集。
- **提議階段在哪裡限制了準確率？** 論文的基準只能部分回答，提議階段在小物件或不尋常的物件上，於多大程度上限制了準確率。

## 關聯

- [CNN](../../../cnn/index.md) 骨幹網路，例如主要實驗所用的 VGG-16 網路，提供共享的特徵。同一家族中較強的骨幹網路，例如[殘差網路](../../../cnn/backbones-and-scaling/resnet/index.md)，能把其進步帶到偵測器上。
- RPN 是一種注意力的形式：摘要說它「告訴統一網路該往哪裡看」。這與[注意力模型](../../../transformer/attention-variants/index.md)中的選擇是一種鬆散的類比，也與[基於顯著性的注意力](../../../../../brain-mind/attention-brain-machine/saliency-map/index.md)中由下而上的階段相似，後者依特徵對比來選擇要看的位置。

## 應用

Faster R-CNN 及其變體已用於駕駛系統中的行人與車輛偵測、醫學影像分析以及工業檢測。

## 參考文獻

### 開創性論文

- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — 提出區域提議網路，它與 Fast R-CNN 偵測器共享卷積特徵。
- Girshick, R., Donahue, J., Darrell, T. & Malik, J. (2013). *Rich feature hierarchies for accurate object detection and semantic segmentation*. arXiv. https://arxiv.org/abs/1311.2524 — R-CNN，第一批區域式偵測器之一，會對每個區域提議執行 CNN。
- Girshick, R. (2015). *Fast R-CNN*. arXiv. https://arxiv.org/abs/1504.08083 — 每張影像只計算一次卷積特徵，再逐提議池化，並使用多任務損失。
- Lin, T.-Y., Dollár, P., Girshick, R., He, K., Hariharan, B. & Belongie, S. (2016). *Feature Pyramid Networks for Object Detection*. arXiv. https://arxiv.org/abs/1612.03144 — 從 CNN 骨幹網路建立自上而下的特徵金字塔，後續偵測器用它進行多尺度偵測。
- Lin, T.-Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — Faster R-CNN 2015 年的結果所報告的 COCO 資料集，後續偵測器也以它進行比較。
- Zou, Z., et al. (2019). *Object Detection in 20 Years: A Survey*. arXiv. https://arxiv.org/abs/1905.05055 — 涵蓋偵測方法的廣泛綜述，並將區域式方法放在其歷史脈絡中。

[^1]: Ren et al. (2015)，表 3、4、5 與 8。VOC 的 mAP 數值取決於訓練資料；計時是在 K40 GPU 上測得，選擇性搜尋的時間則是在 CPU 上測得。
