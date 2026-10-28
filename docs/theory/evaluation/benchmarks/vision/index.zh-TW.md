---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
aliases:
  - Vision benchmarks
  - 視覺基準
---

# 視覺基準

視覺基準在兩個層級衡量辨識能力：整張影像的分類，以及個別物件的偵測與分割。這兩種任務使用不同的指標與不同的標註，因此兩者的分數不能直接比較。

## 概述

此領域的參照點是 ImageNet，一個大型階層式影像資料庫，由 Deng et al.（2009）描述。每年舉辦的 ImageNet 大規模視覺辨識挑戰賽，以數百個物件類別與數百萬張影像建立了分類與偵測基準，並將最佳系統與人類的準確率作比較。主辦者也描述了五年舉辦挑戰賽的經驗教訓（Russakovsky et al., 2015）。

偵測與分割則需要另一種資料。Microsoft COCO 收集日常場景，並以逐個體的分割遮罩標註物件。它包含 91 種物件類型、328k 張影像中的 250 萬個標註實例，設計目的是把辨識放在場景理解的脈絡中（Lin et al., 2014）。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [ImageNet](imagenet.md) | 影像分類 | Top-1 與 top-5 準確率 |
| [COCO](coco.md) | 偵測與實例分割 | 數個重疊門檻上的平均精確率 |

影像分類問的是圖中有什麼，因此每張影像一個標籤就夠了。偵測與分割則要問每個物件在哪裡、形狀如何，因此指標必須同時考量定位品質與標籤。這也是同一個模型在兩種基準上排名可能不同的原因。

## 比較分數

請在相同的測試集、相同的指標與相同的訓練資料下比較模型。在更大的影像集合上預訓練，會改變微調分數的意義，因此訓練資料必須與分數一併註明。不同的輸入解析度或裁切策略也會造成差異，比較時應固定這些條件。

## 關鍵概念

- **Top-1 與 top-5 準確率**：正確標籤是最高預測，或位於前五高預測之中的影像比例。
- **實例分割**：分別標註每個物件，而不只是依類別標註每個像素。
- **重疊門檻**：預測區域與真實區域之間必須達到的最小重疊，偵測才算正確。

## 常見問題

- **測試集擬合。** 反覆使用同一測試集可能造成擬合。Recht et al.（2019）依原始流程收集新的測試集後，發現 CIFAR-10 上準確率下降 3% 至 15%，ImageNet 上下降 11% 至 14%，並將此下降歸因於模型在稍微更難的影像上失敗，而非適應性。
- **穩健性。** 在乾淨資料上的高分可能掩蓋對模糊、雜訊與天氣的脆弱性。ImageNet-C 以常見的損壞來測試這一點（Hendrycks & Dietterich, 2019）。
- **標籤模糊。** 影像中可能有多個有效的標籤或物件，這限制了任何分數能說明的內容。
- **飽和。** 頂尖系統在較舊的資料集上已留下很小的空間，因此差異需要信賴區間。

## 相關連結

- [視覺感知](../../../../brain-mind/visual-perception/index.md) 說明大腦如何辨識物件，這正是 Brain-Score 為模型所具體化的比較。
- [少樣本](../few-shot/index.md) 測試從少數範例進行辨識的能力。
- [準確率](../../metrics/classification/accuracy.md) 與 [IoU](../../metrics/segmentation/iou.md) 是這些基準背後的指標。

## 開放問題

- ImageNet 上的進展有多少能轉移到新的影像集合，以及如何建立能長期保持新鮮的測試集。
- 有許多小物件的偵測基準，是否與只有一個主要物件的分類基準衡量相同的能力。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [神經科學](../neuroscience/index.md) 將模型的表徵與同類影像上的神經反應作比較。
- [多模態](../multimodal/index.md) 將影像與語言結合。

## 參考文獻

### 開創性論文

- Deng, J. et al. (2009). *ImageNet: A large-scale hierarchical image database*. CVPR 2009. https://doi.org/10.1109/CVPR.2009.5206848 — 介紹分類基準背後的影像資料庫。
- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision, 115, 211–252. https://doi.org/10.1007/s11263-015-0816-y — 描述挑戰賽、其資料，以及最佳系統與人類準確率的比較。
- Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — 介紹 328k 張影像中 250 萬個逐實例標註，即偵測與分割基準。

### 文章與文件

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 為 CIFAR-10 與 ImageNet 重新收集測試集，並測量準確率的下降。
- Hendrycks, D. & Dietterich, T. (2019). *Benchmarking Neural Network Robustness to Common Corruptions and Perturbations*. arXiv. https://arxiv.org/abs/1903.12261 — 介紹 ImageNet-C 與 ImageNet-P，測量對常見損壞的穩健性，而非最壞情況的擾動。
