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

DINOv2 由 Oquab 等人（2023）提出，是一個自監督的視覺 Transformer，其凍結的特徵不需微調就能用於許多任務。它以 patch 層級的目標擴充 DINO 系列的自蒸餾方法，並在經過整理的影像集合上訓練。上層子主題是[非對比方法](index.md)，它所建立於其上的前一個方法是 [DINO](index.md)。

## 概述

凍結的 DINOv2 骨幹為每張影像與每個 patch 產生一個特徵。下游系統可以直接使用這些特徵，搭配輕量的頭或檢索步驟，而不必為每個任務重新訓練骨幹。論文的主要主張是：在經過整理的資料上大規模自監督訓練的模型，其特徵在多個基準上能與弱監督預訓練的特徵相當或更好。

## 問題

監督式預訓練需要昂貴的標註，而且標註會使特徵偏向所選的類別。較早的自監督方法雖能得到有用的特徵，但通常使用較小的資料，而且特徵在不同任務間的可靠度較低。論文探討：自監督學習能否在規模上達到與弱監督模型相當的一般性視覺特徵。

## 核心想法

結合兩個自監督目標。影像層級的目標在同一張影像的不同視角之間做教師與學生的自蒸餾。patch 層級的目標則從影像其餘部分預測被遮蔽的 patch，使局部特徵也能被訓練。資料經過整理，以減少重複並平衡概念，作者認為這對特徵品質很重要。

## 運作方式

1. 建立大型且經過整理的影像集合，以檢索步驟找出與一組種子資料集相似的影像。
2. 以全域裁剪上的影像層級自蒸餾損失訓練視覺 Transformer。
3. 加入遮蔽 patch 上的 patch 層級損失，使密集特徵與全域特徵一起學習。
4. 凍結訓練好的骨幹，把其影像與 patch 特徵用於下游任務，例如分類、分割與檢索。

## 結果

論文報告，凍結的 DINOv2 特徵在影像分類、分割與深度估計上表現強勁，通常不需為骨幹做任務專用的訓練。機器人與地點辨識的研究把凍結的特徵當作可直接替換的編碼器使用。例如，AnyLoc 的工作報告，凍結的 DINOv2 特徵在室內資料集上優於為該任務訓練的地點辨識編碼器。基準數字應以論文表格為準。

## 限制

- 最大的骨幹在嵌入式硬體上執行成本高，因此機器人上常使用較小的版本或蒸餾版本。
- 凍結的特徵不會適應特定領域，其對光照與視角的穩健性必須針對每個應用測量。
- 帶來最佳特徵的整理步驟取決於所選的參考資料集，因此確切的資料組合難以重現。

## 相關主題

- [非對比方法](index.md) 把 DINOv2 放在自蒸餾方法之中。
- [視覺定位](../../../../applications/robotics/visual-localisation/index.md) 展示 DINOv2 特徵在機器人情境中的用法。
- [遮蔽預測](../../self-supervised/masked-prediction/index.md) 描述 patch 層級目標所屬的方法家族。

## 開放問題

- 整理後的資料能否由適用於新領域（資料很少時）的原則性選擇規則取代。
- 凍結的特徵在戶外機器人中重要的強烈光度變化下表現如何。

## 參考文獻

- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — 自監督目標、整理後的資料與凍結特徵結果的來源。
- Caron, M., Touvron, H., Misra, I., et al. (2021). *Emerging Properties in Self-Supervised Vision Transformers*. ICCV 2021. arXiv:2104.14294. https://arxiv.org/abs/2104.14294 — DINOv2 所延伸的 DINO 自蒸餾方法。
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — 在地點辨識中使用凍結的 DINOv2 特徵。
- Burns, K., Witzel, Z., Hamid, J. I., et al. (2023). *What makes pre-trained visual representations successful for robust manipulation?* arXiv:2312.12444. https://arxiv.org/abs/2312.12444 — 比較視覺偏移下的預訓練視覺表示，包括 DINO 類模型。
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* ICRA 2024. arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — 針對導航的預訓練編碼器之模擬到真實研究。
