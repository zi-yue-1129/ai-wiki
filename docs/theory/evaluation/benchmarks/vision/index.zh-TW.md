---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
---

# 視覺基準

視覺基準在兩個層級上衡量辨識能力：整張影像的分類，以及實例層級的偵測與分割。兩類任務使用不同的指標，因此分數不能互相比較。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [ImageNet](imagenet.md) | 影像分類 | top-5 錯誤率與 top-1 準確率 |
| [COCO](coco.md) | 偵測與實例分割 | 在 0.5 到 0.95 的 IoU 門檻上的平均精確率 |

## 比較分數

比較模型時，應使用相同的測試集、相同的指標與相同的訓練資料。在更大的影像集合上預訓練，會改變微調後分數的意義，因此分數必須連同訓練資料一起報告。

## 常見問題

- **測試集擬合。** 測試集可能因反覆使用而被擬合，重新蒐集的測試集則可能顯示較低的準確率（Recht et al., 2019）。
- **標籤模糊。** 影像可能含有多個有效標籤或物件，這限制了任何分數所能說明的事。
- **飽和。** 頂尖系統留下的空間很小，因此差異需要區間。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [少樣本](../few-shot/index.md) 測試從少數範例中辨識的能力。
- [準確率](../../metrics/classification/accuracy.md) 與 [IoU](../../metrics/segmentation/iou.md) 是這些基準背後的指標。

## 參考文獻

### 開創性論文

- Deng, J. et al. (2009). *ImageNet: A large-scale hierarchical image database*. CVPR. https://doi.org/10.1109/cvpr.2009.5206848 — 介紹分類基準背後的影像資料庫。
- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — 說明挑戰賽、其指標與人類比較。
- Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV. https://doi.org/10.1007/978-3-319-10602-1_48 — 介紹含逐實例遮罩的偵測與分割基準。

### 文章與文件

- Everingham, M. et al. (2010). *The PASCAL Visual Object Classes (VOC) Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-009-0275-4 — 定義較早期的 VOC 評估，採單一重疊門檻。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 重新蒐集 ImageNet 測試集，並衡量準確率的下降。
