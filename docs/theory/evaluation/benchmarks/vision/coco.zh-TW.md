---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
---

# COCO

COCO（Common Objects in Context）是日常場景中物件偵測與實例分割的基準。它的目的是把物件辨識放在更廣的場景理解之中（Lin et al., 2014）。

## 任務與資料

資料集包含 91 種物件類型的照片，共 328,000 張影像中的 250 萬個標註實例。每個物件都有逐實例的分割遮罩，因此模型必須同時定位每個實例並描出其輪廓（Lin et al., 2014）。

## 協定與指標

偵測與分割以**平均精確率（AP）**評分，並在數個交集除以聯集的門檻上取平均，門檻從 0.5 到 0.95，每次增加 0.05。重疊的度量是 [IoU](../../metrics/segmentation/iou.md)。PASCAL VOC 只用單一門檻 0.5（Everingham et al., 2010），因此 COCO 的平均分數對定位品質的要求較嚴格。COCO 也分別報告小、中、大物件的分數。

## 它能說明什麼

因為 AP 是跨門檻平均，模型不能靠大致找到物件而取得高分。COCO 上的偵測結果成為偵測器設計的常見參考，例如 Faster R-CNN（Ren et al., 2015）。

## 限制

- **邊界品質。** 在高門檻下，遮罩差幾個像素就可能拉低 AP，因此分數同時取決於標註協定與模型。
- **小物件。** 多數系統對小實例的 AP 都很低，使整體平均對測試集中小物件的數量很敏感。
- **測試標籤不公開。** 測試結果來自評估伺服器，這限制了團隊能多頻繁、多細緻地探測測試集。

## 變體

COCO 的全景分割與長尾延伸版本會改變標籤集合或任務。只有在相同的標註版本、切分與 AP 定義下，分數才可比較。

## 相關

- [IoU](../../metrics/segmentation/iou.md) 是 AP 背後的重疊度量。
- [ImageNet](imagenet.md) 是多數視覺骨幹網路最先評估的分類基準。
- [視覺家族概述](index.md) 比較各視覺基準。

## 參考文獻

### 開創性論文

- Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV. https://doi.org/10.1007/978-3-319-10602-1_48 — 介紹資料集、逐實例遮罩與基準分析。
- Everingham, M. et al. (2010). *The PASCAL Visual Object Classes (VOC) Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-009-0275-4 — 定義 VOC 評估，包括偵測的單一 0.5 重疊門檻。

### 文章與文件

- Ren, S. et al. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — 其在 COCO 上的結果成為常見的參考點的偵測器。
- Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — 預印本，含資料集的完整統計分析。

### 補充來源

- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — 說明 COCO 常被拿來比較的早期大規模基準。
