---
translation_reviewed: 2026-10-28
---

# Mask R-CNN

Mask R-CNN 是一種實例分割方法。它在 [Faster R-CNN](../../object-detection/faster-rcnn/index.md) 偵測器上加入一個分支，與方框與類別的預測平行地，為每個偵測到的物件預測二值遮罩。一項新的運算 RoIAlign 使特徵與它們所描述的像素保持對齊。它是[圖像分割](../index.md)頁所列的四種代表性方法之一。

## 概述

實例分割要求的是每個物件的類別、其方框，以及其確切的像素。早期的實例方法通常從逐像素分類開始，再把同一類別的像素切分為不同的實例。Mask R-CNN 採取相反的路線：先偵測每個物件，再於每個偵測結果之中預測遮罩。論文將其描述為一個簡單而靈活的框架，對 Faster R-CNN 只增加少量負擔，並以每秒 5 幀的速度運行。[^1]

Faster R-CNN 並非為像素級的對齊而設計：它的 RoIPool 運算會量化區域的座標。RoIAlign 移除了這種量化。

## 關鍵概念

- **實例優先策略**：先偵測物件，再在其方框內進行分割。
- **RoIAlign**：以精確的、小數座標的取樣點進行雙線性插值來池化每個區域，不對區域的座標做四捨五入。
- **解耦的遮罩**：遮罩頭對每個類別以逐像素的 sigmoid 預測一個二值遮罩。類別由分類分支決定，因此各個遮罩之間不相互競爭。
- **多任務訓練**：方框、類別與遮罩的損失，在抽樣得到的感興趣區域（RoI）上共同最佳化。

## 運作方式

第一階段是 Faster R-CNN 的區域提議網路，它從共享的卷積特徵中提出候選方框。對每個提議，RoIAlign 擷取一張固定大小的特徵圖。接著兩個頭平行運行：一個全連接頭預測類別並修正方框，一個小型全卷積遮罩頭則為 \(K\) 個類別中的每一個預測一張 \(28\times28\) 的遮罩。

訓練時，每個抽樣得到的 RoI 貢獻的損失為

$$
\mathcal{L} = \mathcal{L}_{cls} + \mathcal{L}_{box} + \mathcal{L}_{mask}
$$

其中分類與方框損失與 Fast R-CNN 的相同。遮罩損失是逐像素 sigmoid 的平均二元交叉熵，且僅在真實類別 \(k\) 的遮罩上計算。推論時，預測類別的遮罩會被縮放到方框大小，並以 0.5 的閾值二值化。

## 結果

在 COCO 基準上，論文以 101 層的殘差骨幹加上特徵金字塔，於 test-dev 分割上報告遮罩平均精確度（AP）為 35.7；使用同一家族中更強的骨幹則為 37.1。這些單一模型的結果超越了 COCO 2015 與 2016 分割挑戰賽的冠軍。[^2]

驗證分割上的消融實驗顯示了各項設計選擇的效果：

- **RoIAlign** 取代 RoIPool，遮罩 AP 提高 7.3 點，IoU 0.75 下的遮罩 AP 提高 10.5 點，此為使用步幅 32 骨幹、50 層殘差網路的設定。
- **逐像素獨立 sigmoid** 取代 FCN 所用的逐像素 softmax，遮罩 AP 提高 5.5 點，論文將此差距歸因於遮罩與類別預測的解耦。
- **類別無關的遮罩**，即所有類別共用一張遮罩，其遮罩 AP 為 29.7，而類別特定的遮罩為 30.3，這符合分工的設計：方框分支負責分類。

## 限制

- **兩個階段。** 遮罩分支運行在偵測器之上，因此該方法比單階段設計慢，且依賴偵測品質。遺漏或錯置的方框無法由遮罩挽回。
- **粗糙的遮罩。** 一張 28×28 的遮罩被拉伸到方框上，限制了邊界的銳利度，對大型物件尤其明顯。
- **標註成本。** 訓練需要為訓練集中的每個物件提供標籤，以及多邊形或遮罩。

## 開放問題

- 單階段或以查詢為基礎的設計，能否以較低成本達到兩階段管線的準確度？[圖像分割](../index.md)頁所介紹的 Mask2Former，是在更廣泛的全景分割設定中的一種答案。
- 在不損失速度的前提下，遮罩解析度能提高到多少？

[^1]: He 等人（2017）摘要：Mask R-CNN 在 Faster R-CNN 上加入遮罩分支，並以 5 fps 運行。
[^2]: He 等人（2017）表 1：遮罩 AP 報告於 COCO test-dev；表 2 的消融實驗則在驗證集的 minival 分割上進行。

## 參考文獻

### 開創性論文

- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN*. ICCV. https://arxiv.org/abs/1703.06870 — 論文本身：在 Faster R-CNN 上加入遮罩分支與 RoIAlign，用於實例分割。
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — Mask R-CNN 所擴充的偵測器，其區域提議網路與偵測器共享特徵。
- Lin, T.-Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV. https://arxiv.org/abs/1405.0312 — COCO 資料集與基準，實例分割結果即在其上報告。
- Kirillov, A., He, K., Girshick, R., Rother, C. & Dollár, P. (2019). *Panoptic Segmentation*. CVPR. https://arxiv.org/abs/1801.00868 — 將實例遮罩與事物背景類別結合於單一的全景任務中。
- Girshick, R. (2015). *Fast R-CNN*. arXiv. https://arxiv.org/abs/1504.08083 — 在區域提議之間共享卷積計算，並定義此處使用的方框與類別損失。
- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR. https://arxiv.org/abs/1411.4038 — 本比較中逐像素 softmax 所出自的全卷積分割器。
- Cheng, B., Misra, I., Schwing, A. G., Kirillov, A. & Girdhar, R. (2022). *Masked-attention Mask Transformer for Universal Image Segmentation*. CVPR. https://arxiv.org/abs/2112.01527 — 之後以查詢為基礎的架構，可處理實例、全景與語意分割。

### 綜述與教科書

- Minaee, S., Boykov, Y., Porikli, F., Plaza, A., Kehtarnavaz, N. & Terzopoulos, D. (2021). *Image Segmentation Using Deep Learning: A Survey*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3059968 — 在更廣泛的回顧中涵蓋 Mask R-CNN 家族的實例分割方法。
