---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
---

# ImageNet

ImageNet 是依 WordNet 名詞組織的大型影像資料庫。它最知名的基準是 ImageNet 大規模視覺辨識挑戰賽（ILSVRC），自 2010 年起每年舉辦（Russakovsky et al., 2015）。它是影像分類的參考基準，也用於物件偵測，並作為預訓練資料的來源。

## 任務與資料

給定一張影像，模型要從一組固定的類別中預測其中之一。挑戰賽涵蓋數百個類別、數百萬張影像的分類與物件偵測（Russakovsky et al., 2015）。分類子集使用 1,000 個類別。

## 協定與指標

挑戰賽的主要指標是 **top-5 錯誤率**：只要正確類別在分數最高的五個預測之中，即算正確。同時也報告 top-1 準確率。測試標籤不公開，因此分數來自提交的預測，而非本地評估。

這些數字所依據的指標，見[準確率](../../metrics/classification/accuracy.md)。top-k 準確率的概念相同，只是決策規則較寬鬆。

## 它能說明什麼

這個基準讓深度卷積網路成為影像辨識的標準做法。之後的架構仍常在此比較，包括殘差網路（He et al., 2015）與視覺 Transformer（Dosovitskiy et al., 2020）。2015 年的論文也把最好的系統與人類準確率做比較，顯示此任務仍困難之處。

## 限制

- **對新資料的泛化。** Recht et al.（2019）依照原始程序蒐集新的測試集，許多模型的準確率因此下降，這顯示基準的一部分衡量的是對其蒐集程序的適配程度。
- **標籤模糊。** 多數影像含有數個物件，但只有一個標籤。top-5 計分能減輕這個問題，但無法消除。
- **飽和。** 頂尖系統的分數已遠高於最初定義進步的水準，因此小的差距需要區間與明確的測試集大小，才能解讀。

## 變體

ImageNetV2 是 Recht et al.（2019）重新蒐集的測試集，是最知名的替代測試集。當原始測試集上的分數不足以說明問題時，會使用穩健性或分布外的變體。

## 相關

- [COCO](coco.md) 以逐實例遮罩涵蓋偵測與分割。
- [少樣本基準](../few-shot/index.md) 使用了 ImageNet 的影像。
- [視覺家族概述](index.md) 比較各視覺基準。

## 參考文獻

### 開創性論文

- Deng, J. et al. (2009). *ImageNet: A large-scale hierarchical image database*. CVPR. https://doi.org/10.1109/cvpr.2009.5206848 — 介紹 ILSVRC 基準所取樣的影像資料庫。
- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — 說明挑戰賽、其指標，以及與人類準確率的比較。

### 文章與文件

- He, K. et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — 殘差網路，是在 ImageNet 分類上評估的標準架構。
- Dosovitskiy, A. et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv. https://arxiv.org/abs/2010.11929 — 在 ImageNet 上訓練與評估的視覺 Transformer。

### 補充來源

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 依原始程序重新蒐集測試集，並衡量其造成的準確率下降。
