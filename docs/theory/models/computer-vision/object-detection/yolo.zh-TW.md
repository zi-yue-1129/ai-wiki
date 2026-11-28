---
status: draft
last_reviewed: 2026-11-28
tags:
  - computer vision
  - object detection
aliases:
  - YOLO
  - You Only Look Once
  - 你只看一次
---

# YOLO（You Only Look Once）

YOLO 是一種單階段物件偵測器，它用一個網路在單次前向傳播中，為整張影像預測邊界框與類別機率。它把偵測視為一個迴歸問題，而不是對許多候選區域逐一做分類（Redmon et al., 2016）。[^yolo] 它的速度使即時偵測變得實用，此後這個系列持續發展出多個版本。

本頁是 [物件偵測](index.md) 的一部分。

## 概觀

早期的偵測器會對每個候選區域各執行一次分類器，再把結果合併。這些流程雖然準確，但速度慢，而且各階段是分開訓練的。YOLO 去掉了候選區域的階段：一個卷積網路只看一次影像，就同時輸出所有邊界框與類別。

代價是對影像的觀察較為粗略。每個物件依其中心點被指派給一個網格格子，但預測的邊界框可以延伸到該格子之外。每個格子的預測數量有限，因此很難偵測密集排列的小物件。[^yolo]

## 關鍵概念

- **網格格子（grid cell）**：影像被切分成 S × S 的網格。包含物件中心點的格子，負責預測該物件。
- **邊界框預測器（box predictor）**：每個格子預測 B 個邊界框。每個框有五個數值：中心的 x 與 y、寬與高，以及一個信心分數。
- **類別機率（class probabilities）**：每個格子也預測 C 個類別機率，由它的 B 個框共用。
- **負責的預測器（responsible predictor）**：在一個格子內，與真實物件重疊最多的那個框。

## 運作方式

在 PASCAL VOC 上，論文使用 S = 7、B = 2、C = 20，因此網路輸出一個 7 × 7 × 30 的張量（7 × 7 × (B × 5 + C)）。訓練使用由多個部分組成的平方和誤差。框中心的誤差，以及框寬高平方根的誤差，以 λcoord = 5 加權，以強調定位的重要性。對於不負責任何物件的框預測器，其信心誤差以 λnoobj = 0.5 降權，因為大多數格子都沒有物件。類別誤差只計入確實含有物件的格子。[^yolo]

論文對寬與高取平方根，使同樣大小的誤差在小框上的代價大於大框。[^yolo]

## 關鍵方法

本頁是 [物件偵測](index.md) 概觀中一種代表性方法的詳細說明。它最接近的相關方法包括：

- **Faster R-CNN**：先產生候選區域的兩階段替代方案（[Faster R-CNN](faster-r-cnn.md)）。
- **DETR**：以 Transformer 直接預測一組固定物件的單階段設計（[DETR](detr.md)）。
- **RetinaNet**：以新的損失函數處理類別不平衡的單階段偵測器（[RetinaNet](retinanet.md)）。

## 結果

在 PASCAL VOC 2007 測試集上，以 VOC 2007+2012 trainval 訓練，論文報告 YOLO 的 mAP 為 **63.4%**，速度為每秒 **45 幀**；較小的版本 Fast YOLO 則為 **52.7%** mAP、**155 fps**。同一張表中，Fast R-CNN 的 mAP 為 70.0%，但速度僅約 0.5 fps。YOLO 的速度是在 Titan X GPU 上、未使用批次處理所量測的。該表比較的是已發表的系統，並非在相同硬體上控制條件的基準測試。[^yolo]

錯誤分析會檢查每個類別前 N 個偵測結果，其中 N 為該類別的真實物件數，然後對 20 個類別取平均。在這些偵測中，YOLO 的定位錯誤佔 19.0%，Fast R-CNN 為 8.6%；背景誤報則是 YOLO 4.75%，Fast R-CNN 13.6%。這些百分比的分母包含所有前 N 個偵測結果，包括正確的偵測，而不只是錯誤的偵測。[^yolo]

後來的 YOLOv3 報告（Redmon and Farhadi, 2018）在其 320 像素的模型上，COCO AP（對 IoU 門檻 0.50–0.95 取平均）為 **28.2**，並稱其執行時間為 22 毫秒。這與上面 VOC 的分數屬於不同的基準與指標。其圖 1 將這個結果與 SSD321（28.0 AP、61 毫秒）比較；作者表示速度約快三倍，所用的計時來自 M40 或 Titan X GPU，並非單一且匹配的硬體環境。[^yolov3]

## 限制

原始 YOLO 論文列出了它自己的弱點；這些限制適用於本頁所描述的原始模型，不會自動適用於後續版本：[^yolo]

- 每個格子只預測兩個框、且只能屬於一個類別，因此能找到的相鄰物件數量有限。論文以成群的小物件（例如一群鳥）作為例子。
- 模型對形狀或長寬比不尋常的物件泛化能力較差。
- 多層的下採樣使用於框預測的特徵變得粗糙。
- 誤差的主要來源是定位錯誤。

YOLOv3 報告描述了該系列一連串較小的設計改動，在維持速度的同時提升了準確度。YOLO9000（Redmon and Farhadi, 2017）則以聯合訓練偵測與分類資料的方式，擴展了這一脈絡。[^yolo9000]

## 關聯

YOLO 是 [物件偵測](index.md) 概觀中兩階段路線的單階段對應方法。它的骨幹是卷積網路，詳見 [卷積神經網路](../../cnn/index.md) 頁面。與大腦的關聯較為間接：和其他偵測文獻一樣，YOLO 是以邊界框與標籤來評估，而不是以神經反應來評估。

## 參考文獻

### 奠基性論文

[^yolo]: Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2016). *You Only Look Once: Unified, Real-Time Object Detection*. CVPR, pp. 779–788. doi:[10.1109/CVPR.2016.91](https://doi.org/10.1109/CVPR.2016.91)（預印本：https://arxiv.org/abs/1506.02640）— 原始 YOLO 論文，包含網格設計、損失函數，以及上文使用的 PASCAL VOC 速度與準確度結果。

[^yolo9000]: Redmon, J. & Farhadi, A. (2017). *YOLO9000: Better, Faster, Stronger*. CVPR, pp. 6517–6525. doi:[10.1109/CVPR.2017.690](https://doi.org/10.1109/CVPR.2017.690)（預印本：https://arxiv.org/abs/1612.08242）— 第二版，包含批次正規化、錨框，以及偵測與分類資料的聯合訓練。

[^yolov3]: Redmon, J. & Farhadi, A. (2018). *YOLOv3: An Incremental Improvement*. arXiv. https://arxiv.org/abs/1804.02767 — 第三版，包含 COCO AP、AP50，以及與 SSD 和 RetinaNet 的速度比較。

- Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y. & Berg, A. C. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — 另一種單階段偵測器，在多個特徵圖上預測框，是 YOLOv3 的比較對象。
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — YOLO 速度所比較的兩階段系統。

### 綜述與基準

- Everingham, M., Van Gool, L., Williams, C. K. I., Winn, J. & Zisserman, A. (2010). The Pascal Visual Object Classes (VOC) challenge. *International Journal of Computer Vision*, 88, 303–338. doi:[10.1007/s11263-009-0275-4](https://doi.org/10.1007/s11263-009-0275-4) — YOLO 結果所依據的 VOC 基準與評估協定。
