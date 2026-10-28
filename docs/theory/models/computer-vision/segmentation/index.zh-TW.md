---
translation_reviewed: 2026-10-28
related:
  - theory/evaluation/metrics/segmentation/index.md
---

# 影像分割（Image Segmentation）

影像分割為影像中的每個像素指定一個標籤，或為模型從周圍區分出來的每個區域指定標籤。[物件偵測](../object-detection/index.md)為每個物件回傳一個框，分割則回傳物件的精確形狀，因此當輪廓很重要時會使用它，例如腫瘤邊界、道路表面，或生產線上零件的邊緣。

## 概述

三種標準變體的差別在於輸出的單位。**語意分割**為每個像素指定一個類別，同類別的物件不會被分開。**實例分割**為每個物件給出自己的遮罩，因此兩輛汽車即使共享同一標籤，也是兩個遮罩。**全景分割**結合兩者：每個像素都獲得一個類別，「物質」區域（如天空或道路）與可計數的「物件」一起被涵蓋。Kirillov 等人（2018）提出了全景任務，並將其定義為統一語意分割與實例分割。

品質以預測遮罩與參考遮罩之間的重疊衡量，通常使用[交集除以聯集（IoU）](../../../evaluation/metrics/segmentation/iou.md)與 [Dice 係數](../../../evaluation/metrics/segmentation/dice.md)。

## 關鍵概念

- **遮罩**：以像素為單位的二元或逐類別地圖，標示一個物件或類別的區域。
- **編碼器—解碼器**：先降低解析度以擷取上下文，再將其還原為全尺寸地圖的網路。
- **跳躍連接**：把高解析度特徵從編碼器傳到解碼器的連結，使細緻的邊界能夠被恢復。
- **可提示的分割**：根據點、框或文字提示，為指定物件產生遮罩的模型。

## 運作方式

**全卷積網路。** Long、Shelhamer 與 Darrell（2014）展示了，分類網路可以轉換為輸出密集地圖的網路，並從像素到像素端到端訓練。他們的摘要報告，這類網路在當時的語意分割上超越了最先進的結果。

**U-Net。** Ronneberger、Fischer 與 Brox（2015）建立了對稱的編碼器—解碼器，並加上跳躍連接。收縮路徑擷取上下文，擴張路徑恢復定位資訊。論文報告，此架構可以從極少的影像端到端訓練，並依賴強烈的資料擴增。它是為生物醫學影像設計的，而同樣的設計現在也被用作許多擴散模型中的去噪網路。

**實例分割。** Mask R-CNN（He 等人，2017）在 Faster R-CNN 的框分支旁，加入一個與之平行預測物件遮罩的分支。遮罩是針對每個感興趣區域預測的，因此一個網路即可得到實例遮罩。

**可提示的分割。** Segment Anything（Kirillov 等人，2023）訓練一個模型，為提示所指定的任何物件回傳遮罩，使其能零樣本遷移到新的影像分布。作者釋出了 SA-1B 資料集，摘要將其描述為 10 億個遮罩、1,100 萬張影像。

## 關鍵方法

簡要比較。上面提到的每個方法都可以有自己的方法頁面；這些頁面尚未撰寫，因此目前在此提供細節。

- **FCN（語意）**：把分類器轉換為做密集預測。簡單而通用，但邊界較粗糙。
- **U-Net（語意，編碼器—解碼器）**：以跳躍連接取得精確邊界，可從少量標註影像訓練。
- **Mask R-CNN（實例）**：在兩階段偵測器上加一個遮罩頭，每個物件得到一個遮罩。
- **Segment Anything（可提示）**：由提示驅動的遮罩，具有廣泛的零樣本遷移能力。

## 關聯

U-Net 的設計在 [U-Net](../cnn/unet/index.md) 頁面有更詳細的說明。它作為擴散模型去噪網路的用途，使本主題與[生成模型](../../../paradigms/unsupervised/density-and-generative-models/generative-models/index.md)相連。指標見[分割指標](../../../evaluation/metrics/segmentation/index.md)頁面。

分割也與視覺科學相關。把圖形與背景分開，是知覺中的核心問題，而分割影像的模型有時會與神經資料比較。基準上的好遮罩本身並不能說明模型是否像人一樣知覺區域。

## 應用

- **醫學影像。** 在掃描中勾勒器官、病灶與腫瘤，U-Net 最初便是在此情境下發展的。見[醫療保健](../../../../applications/healthcare/index.md)。
- **自動駕駛。** 標示道路表面、車道與可行駛空間，供規劃使用。見[自動駕駛](../../../../applications/autonomous-driving/index.md)。
- **遙測與農業。** 從航拍影像繪製土地覆蓋與田地邊界。

## 開放問題

- 標註成本高昂，而基準中的遮罩未必符合使用者所需的邊界。
- 全景與實例品質在類別定義不同的資料集之間難以比較。
- 可提示模型依賴提示，目前尚不清楚它們如何可靠地處理含糊的提示。
- 把分割從靜態影像延伸到影片、並在時間上保持一致的身分，是一個活躍的領域。

## 參考文獻

### 開創性論文

- Long, J., Shelhamer, E. & Darrell, T. (2014). *Fully Convolutional Networks for Semantic Segmentation*. arXiv. https://arxiv.org/abs/1411.4038 — 將分類網路轉換為全卷積網路，並端到端訓練以做密集預測。
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. arXiv. https://arxiv.org/abs/1505.04597 — 提出帶跳躍連接的 U-Net 編碼器—解碼器，以少量影像與大量資料擴增訓練。
- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN*. arXiv. https://arxiv.org/abs/1703.06870 — 在 Faster R-CNN 上加入遮罩分支，與框平行預測物件遮罩。
- Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., Dollár, P. & Girshick, R. (2023). *Segment Anything*. arXiv. https://arxiv.org/abs/2304.02643 — 在 SA-1B 資料集上訓練的可提示分割模型，可零樣本遷移到新的影像分布。
- Kirillov, A., He, K., Girshick, R., Rother, C. & Dollár, P. (2018). *Panoptic Segmentation*. arXiv. https://arxiv.org/abs/1801.00868 — 將全景分割定義為語意分割與實例分割的統一。

### 綜述與基準

- Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick, R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L. & Dollár, P. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — 含實例遮罩的大型基準，以及實例分割結果所用的平均精確率協定。
