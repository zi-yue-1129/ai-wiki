---
translation_reviewed: 2026-10-28
tags:
  - self-supervised learning
  - vision transformer
  - visual representation
aliases:
  - DINOv2
  - 自監督視覺特徵
---

# DINOv2

DINOv2 是一種自監督視覺 Transformer，其凍結的特徵無需微調主幹網路，即可用於許多影像任務。Oquab 等人（2023）結合了來自 DINO 的影像層級自我蒸餾目標，以及來自 iBOT 的圖像塊層級遮罩目標，並在約 1.42 億張經過策展的影像上訓練。

## 概述

凍結的 DINOv2 主幹網路會為整張影像，以及為每個圖像塊各產生一個特徵。下游系統可以用一個輕量的頭來使用這些特徵，無須為每項任務各自訓練一個主幹網路。論文的主要主張是：在經策展資料上大規模訓練的自監督模型，其特徵可與公開可得的最佳弱監督模型相匹敵；論文也報告，在多數基準上這些特徵超過 OpenCLIP。本頁的上層子主題是[非對比方法](index.md)。

## 問題

監督式預訓練需要昂貴的標籤，並使特徵偏向所選的類別。早期的自監督方法通常以較小的資料訓練，其特徵在不同任務間的可靠度較低。論文探討自監督學習能否在弱監督模型的規模上，產生通用的視覺特徵。

## 關鍵概念

- **影像層級目標**：學生與教師的類別 token 特徵之間的交叉熵，計算於同一影像的不同裁切區域。這是 DINO 的目標。
- **圖像塊層級目標**：學生看到部分被遮罩的圖像塊，被遮罩 token 上的損失使其特徵與教師的圖像塊特徵相符。這是 iBOT 的目標。
- **中心化**：教師的輸出經過中心化處理，這項技術論文取自 SwAV。
- **KoLeo 正則化**：促使批次中的特徵盡量均勻分散。
- **經策展的資料**：從未經策展的資料池中檢索影像，使其近似一組經策展的參考資料集。

## 運作方式

1. **策展資料。**從約 12 億張未經策展的影像資料池開始，移除近似重複的影像，並檢索與經策展參考資料集（如 ImageNet-22k、ImageNet-1k 與 Google Landmarks）相近的影像。檢索使用在 ImageNet-22k 上以自監督方式訓練的 ViT-H/16 所產生的嵌入、餘弦相似度與 k-means 分群。結果為含 1.42 億張影像的 LVD-142M。
2. **訓練主幹網路。**以影像層級與圖像塊層級目標，加上 KoLeo 正則化，訓練一個視覺 Transformer。
3. **凍結。**預訓練後，主幹網路保持固定。
4. **使用特徵。**把影像與圖像塊特徵輸入下游的頭，用於分類、分割、深度估計或檢索。

## 關鍵方法

### DINOv2: Learning Robust Visual Features without Supervision（Oquab 等人，2023）

- **問題：**自監督特徵在不同任務間的可靠度一直低於弱監督特徵，而規模本身是否足以縮小差距並不清楚。
- **核心想法：**結合 DINO 的影像層級自我蒸餾與 iBOT 的遮罩圖像塊目標，並在以檢索方式挑選的大型經策展資料集上訓練。
- **方程式或演算法：**兩個損失與 KoLeo 正則化在論文的方法章節中描述。本頁以文字說明，而不是單一方程式。
- **結果：**對最大的模型（凍結的 ViT-g/14），論文報告在 ImageNet-1k 上的線性探測 top-1 為 86.5%；在 ADE20k 上以線性頭得到 49.0 mIoU（多尺度測試為 53.0）；在 NYUd 深度估計上以 DPT 頭得到 0.279 的 RMSE（越低越好）。論文也報告 Oxford-Hard 檢索的 mAP 為 52.3。
- **限制：**最大的模型是一個十億參數的 ViT，在嵌入式硬體上執行成本高。策展步驟取決於所選的參考資料集，因此若沒有相同的檢索流程，很難重現確切的資料組成。凍結的特徵不會適應新領域，因此其對變化的穩健性必須針對各應用另行測量。

## 相關連結

- [遮罩預測](../masked-prediction/index.md)：圖像塊層級目標是把遮罩預測的概念應用於影像圖像塊。
- [視覺 Transformer](../../../models/transformer/index.md)：主幹網路的架構。
- [機器人學](../../../../applications/robotics/index.md)：凍結的視覺特徵被用作具身任務的編碼器。

## 應用

- **影像分類、分割與深度估計**：使用凍結特徵，即論文的評估所涵蓋者。
- **影像檢索**：論文在實例層級的基準上報告結果。

## 開放問題

- 當新領域的資料很少時，能否以有原則的選擇規則取代人工挑選的參考資料集。
- 凍結特徵在光照與視角大幅改變下的表現如何，而這在戶外機器人中很重要。

## 參考文獻

### 開創性論文

- Oquab, M. et al. (2023). DINOv2: Learning Robust Visual Features without Supervision. *Transactions on Machine Learning Research*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — 本論文，包含兩種目標、經策展的資料與凍結特徵的結果。
- Caron, M. et al. (2021). Emerging Properties in Self-Supervised Vision Transformers. arXiv:2104.14294. https://arxiv.org/abs/2104.14294 — DINO，DINOv2 所保留的影像層級自我蒸餾目標。
- Zhou, J. et al. (2022). iBOT: Image BERT Pre-training with Online Tokenizer. arXiv:2111.07832. https://arxiv.org/abs/2111.07832 — DINOv2 與 DINO 結合使用的遮罩圖像塊目標。
- Dosovitskiy, A. et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. arXiv:2010.11929. https://arxiv.org/abs/2010.11929 — 用作主幹網路的視覺 Transformer 架構。
- Chen, T. et al. (2020). A Simple Framework for Contrastive Learning of Visual Representations. arXiv:2002.05709. https://arxiv.org/abs/2002.05709 — SimCLR，與自我蒸餾相對的對比式替代方法。
