---
translation_reviewed: 2026-10-28
related:
  - theory/evaluation/metrics/segmentation/iou.md
---

# 物件偵測（Object Detection）

物件偵測在影像中找出某一組物件類別的每一個實例，並為每個實例回傳一個邊界框與一個類別標籤。它比影像分類困難，因為分類只為整張影像給出一個標籤；它也是大多數實用視覺系統的前提，從駕駛輔助到工廠檢測都需要它。

## 概述

偵測器必須同時回答兩個問題：影像中有*什麼*，以及它*在哪裡*。輸出是一個長度不固定的清單，每一筆包含一個類別與一個信心分數。物件數量事先未知，而且相鄰的預測可能對同一個物件提出多次。這兩個事實塑造了下面大部分的設計。

偵測以每個類別的平均精確率（AP）評估，並對各類別取平均得到 mAP。當預測框與標準框的重疊程度，以[交集除以聯集（IoU）](../../../evaluation/metrics/segmentation/iou.md)衡量，超過某個門檻時，該預測框才算正確。COCO 基準對數個 IoU 門檻取 AP 的平均，因此同時獎勵類別正確與定位精準（Lin 等人，2014）。

## 關鍵概念

- **邊界框**：一個矩形，通常以中心點、寬與高表示，或以兩個角點表示。
- **錨框或預設框**：在每個特徵圖位置放置的一組固定形狀參考框。網路預測相對於它們的偏移量。
- **非極大值抑制（NMS）**：一個後處理步驟，在同一類別互相重疊的偵測結果中，只保留分數最高的框。
- **特徵金字塔**：取自多種解析度的特徵，使小物件與大物件都能被處理。
- **指派（assignment）**：決定哪些預測要被訓練去匹配哪些真實物件的規則。

## 運作方式

大多數偵測器共用同一條管線。卷積或 Transformer 骨幹網路擷取特徵；頭部在每個候選位置預測一個類別分數與一個框的修正量。訓練時把預測匹配到真實物件，推論時移除重複的偵測。各家族的差異在於候選如何產生，以及重複如何被移除。

**兩階段偵測器。** R-CNN（Girshick 等人，2013）對來自獨立提案方法的區域提案執行 CNN，並報告相較於先前最佳結果，在 PASCAL VOC 2012 上的 mAP 相對提升超過 30%。Fast R-CNN（Girshick，2015）每張影像只計算一次卷積特徵，再為每個提案池化。論文指出，它訓練 VGG16 網路的速度是 R-CNN 的九倍。Faster R-CNN（Ren 等人，2015）以區域提案網路取代外部提案方法，此網路與偵測器共享卷積特徵，因此整個系統可以端到端訓練。

**單階段偵測器。** YOLO（Redmon 等人，2015）把偵測視為從影像到框與類別的單次迴歸。論文指出其基礎模型每秒可處理 45 張影像。SSD（Liu 等人，2015）在數個特徵圖上，一次預測一組固定預設框的分數與偏移量，並報告其準確率可與基於提案的方法相比，速度則快得多。RetinaNet（Lin 等人，2017）處理密集偵測器中前景與背景樣本極度不平衡的問題，並提出焦點損失（focal loss），降低已被正確分類樣本的權重，使訓練不被大量容易的背景位置主導。

**集合預測。** DETR（Carion 等人，2020）以 Transformer 編碼器與解碼器直接輸出一組固定數量的物件預測。訓練時，預測與真實物件之間的二分匹配提供一對一的指派。論文報告這使錨框與非極大值抑制都不再必要。

## 關鍵方法

簡要比較。每個被提到的偵測器都可以有自己的方法頁面；這些頁面尚未撰寫，因此目前在本節提供細節。

- **R-CNN 家族（兩階段）**：先提出區域，再做逐區域的分類與修正。準確，但推論歷來較慢。
- **YOLO 與 SSD（單階段）**：在密集位置上一次完成預測。較快，早期準確率落後，後來的設計（包括焦點損失）縮小了這個差距。
- **RetinaNet（帶焦點損失的單階段）**：密集偵測器，其損失針對類別不平衡重新加權。
- **DETR（集合預測）**：Transformer 解碼器加上二分匹配，沒有錨框，也沒有非極大值抑制。

## 關聯

物件偵測建立在[卷積網路](../../cnn/index.md)與 [U-Net](../../cnn/unet/index.md) 頁面所述的卷積特徵之上。DETR 家族與 [Transformer](../../transformer/index.md) 架構相連。任務總覽見[電腦視覺](../index.md)頁面。

與大腦的連結是間接的。偵測基準衡量的是框與標籤，而非神經反應，因此它們無法說明偵測器是否與大腦定位物件的方式相符。物件辨識網路與神經資料的比較，在[NeuroAI](../../../../brain-mind/neuroai/index.md)中討論。

## 應用

- **自動駕駛。** 偵測車輛、行人與交通標誌，是主要的感知任務之一。見[自動駕駛](../../../../applications/autonomous-driving/index.md)。
- **醫學影像。** 在掃描影像中定位病灶或器官。見[醫療保健](../../../../applications/healthcare/index.md)。
- **工業檢測。** 在生產線上找出瑕疵或零件。見[製造業](../../../../applications/manufacturing/index.md)。

## 開放問題

- 小物件與擁擠場景的準確率，仍低於大型且孤立的物件。
- 長尾的類別分布使稀有類別難以學習，這正是焦點損失所要解決的問題。
- 開放詞彙偵測（以文字描述而非固定標籤集來尋找物件）是一個活躍的領域，其取捨不同於封閉集合的偵測器。
- 速度與準確率必須在模型部署的硬體上取得平衡，而基準結果未必能轉移。

## 參考文獻

### 開創性論文

- Girshick, R., Donahue, J., Darrell, T. & Malik, J. (2013). *Rich feature hierarchies for accurate object detection and semantic segmentation*. arXiv. https://arxiv.org/abs/1311.2524 — 提出 R-CNN：區域提案加上 CNN 特徵，摘要中報告了 PASCAL VOC 2012 上的 mAP 相對提升。
- Girshick, R. (2015). *Fast R-CNN*. arXiv. https://arxiv.org/abs/1504.08083 — 以 RoI 池化在提案之間共享卷積運算，並報告 VGG16 的訓練速度是 R-CNN 的九倍。
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — 加入與偵測器共享特徵的區域提案網路，使提案生成成為可訓練網路的一部分。
- Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2015). *You Only Look Once: Unified, Real-Time Object Detection*. arXiv. https://arxiv.org/abs/1506.02640 — 把偵測表述為單一迴歸問題，並報告基礎模型每秒 45 張影像。
- Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y. & Berg, A. C. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — 在數個特徵圖上以單次前向傳遞，預測預設框的分數與偏移量。
- Lin, T.-Y., Goyal, P., Girshick, R., He, K. & Dollár, P. (2017). *Focal Loss for Dense Object Detection*. arXiv. https://arxiv.org/abs/1708.02002 — 為密集單階段偵測器的類別不平衡問題提出焦點損失。
- Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A. & Zagoruyko, S. (2020). *End-to-End Object Detection with Transformers*. arXiv. https://arxiv.org/abs/2005.12872 — 提出 DETR，以二分匹配預測一組物件，且不需要錨框或非極大值抑制。

### 綜述與基準

- Everingham, M., Van Gool, L., Williams, C. K. I., Winn, J. & Zisserman, A. (2010). The Pascal Visual Object Classes (VOC) challenge. *International Journal of Computer Vision*, 88(2), 303–338. https://ora.ox.ac.uk/objects/uuid:8e9c1a89-e97d-4ca5-8581-a97a8cbb9f0a — VOC 基準與其評估協定，早期偵測器皆以此評估。牛津大學儲存庫的紀錄確認了標題、作者、期刊與卷號；其年份欄位為 2009，即線上發表日期。
- Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick, R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L. & Dollár, P. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — COCO 資料集，以及在多個 IoU 門檻上取平均的 AP 指標。
