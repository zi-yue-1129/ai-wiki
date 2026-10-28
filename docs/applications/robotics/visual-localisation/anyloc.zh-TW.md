---
translation_reviewed: 2026-10-28
tags:
  - robotics
  - place recognition
  - foundation model
aliases:
  - AnyLoc
  - 通用視覺地點辨識
---

# AnyLoc

AnyLoc 由 Keetha、Mishra、Karhade、Jatavallabhula、Scherer、Krishna 與 Garg（2023）提出，是一個以凍結的基礎模型建構的地點辨識方法。它取用 DINOv2 的中間層特徵，不經訓練就把它們聚合成單一描述子，並從資料庫中檢索相符的地點。論文的主張是：一個通用描述子能在論文評估中的不同領域上運作。上層子主題是[視覺定位](index.md)。

## 概述

AnyLoc 沒有編碼器訓練步驟。凍結的 DINOv2 骨幹產生密集的局部特徵，再以基於分群的聚合（一種不需標註即可學得詞彙的局部聚合描述子向量，VLAD 的形式），把它們合併成每張影像一個向量。檢索則是最近鄰搜尋。此方法的核心是特徵與聚合方式的選擇，而不是新的網路。

## 問題

地點辨識方法通常在單一領域上訓練，例如城市街道，換到其他地方準確率就會下降。為每個環境訓練新的編碼器成本高，而機器人也不一定有足夠的資料。論文探討：通用基礎模型能否作為跨領域的單一編碼器，以及哪一層與哪種聚合能得到最佳結果。

## 核心想法

使用凍結的自監督模型特徵，取自作者發現效果最好的中間層，並以不需標註的方式聚合。聚合步驟把豐富的特徵圖轉成適合檢索的緊湊描述子。

## 運作方式

1. 讓影像通過凍結的 DINOv2 骨幹，保留所選中間層的特徵。
2. 以不需標註學得的詞彙對局部特徵分群，並聚合成影像的向量。
3. 將描述子正規化，並與其所屬地點一起存入資料庫。
4. 對查詢影像，計算其描述子並檢索最近的已儲存描述子。

## 結果

作者報告，在室內資料集上，AnyLoc 的 R@1 高於為任務訓練的編碼器。例如，在一個室內資料集上，他們報告 AnyLoc 為 75.2，而 MixVPR 為 64.4。作者也報告，在較大的骨幹尺寸下增益趨於平緩。這些數字取決於評估協定，重用前應先在論文表格中核對。

## 限制

- 檢索本身不估計幾何，因此機器人在依賴匹配之前仍需驗證。
- 最大的骨幹在嵌入式硬體上成本高，而論文沒有報告機器人尺寸版本的延遲。
- 此方法在檢索基準上評估，閉迴路的機器人結果不在論文範圍之內。

## 相關主題

- [視覺定位](index.md) 把 AnyLoc 與另一種訓練式的方法 EigenPlaces 放在一起比較。
- [DINOv2](../../../theory/paradigms/self-supervised/non-contrastive-methods/dinov2.md) 說明 AnyLoc 所用的凍結骨幹。
- [EigenPlaces](eigenplaces.md) 代表為視角穩健性而訓練的做法。

## 開放問題

- 聚合步驟能否在不損失準確率的情況下，為小型平台上的即時使用變得更便宜。
- 凍結特徵如何處理 Zaffar 等人（2021）基準所隔離的視角改變。

## 參考文獻

- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — 凍結特徵方法與室內結果的來源。
- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — AnyLoc 所用的凍結骨幹。
- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. arXiv:2308.10832. https://arxiv.org/abs/2308.10832 — 為視角穩健性而訓練的替代方案。
- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision, 129(7), 2136–2174. arXiv:2005.08135. https://arxiv.org/abs/2005.08135 — 具有受控視角與外觀改變的基準。
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* ICRA 2024. arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — 預訓練編碼器比從頭訓練的編碼器更能轉移到真實機器人的證據。
