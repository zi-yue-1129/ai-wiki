---
translation_reviewed: 2026-10-28
related:
  - applications/robotics/visual-localisation
tags:
  - robotics
  - place recognition
  - foundation model
aliases:
  - AnyLoc
  - 通用視覺地點辨識
---

# AnyLoc

AnyLoc 由 Keetha、Mishra、Karhade、Jatavallabhula、Scherer、Krishna 與 Garg（2023）提出，是一個以凍結的自監督基礎模型建構的地點辨識方法。它取用 DINOv2 的中間層特徵，不訓練編碼器，就把每張影像聚合成一個描述子，並從資料庫中檢索相符的地點。論文的主張是：一個通用描述子能在差異很大的環境中運作。上層子主題是[視覺定位](index.md)。

## 概述

AnyLoc 沒有編碼器訓練步驟。凍結的 DINOv2 骨幹產生密集的局部特徵，再以無監督、基於分群的聚合，把它們合併成每張影像一個向量。檢索則是最近鄰搜尋。這個方法的貢獻在於特徵的選擇、特徵取自哪一層，以及如何聚合，而不是一個新的網路。

## 問題

地點辨識方法通常在單一類型的場景上訓練，例如城市街道，換到其他環境時準確率就會下降。為每個環境訓練新的編碼器成本高，而機器人也不一定有足夠的標註資料。論文探討：通用基礎模型能否作為跨領域的單一編碼器，以及哪一層與哪種聚合能得到最佳結果。

## 核心想法

使用凍結的自監督模型特徵，取自較深的中間層，並以不需標註的方式聚合。聚合步驟把豐富的局部特徵轉成適合檢索的緊湊描述子。作者也依環境類型把資料庫分組，讓每一組擁有自己的聚合詞彙。

## 運作方式

1. 讓影像通過凍結的 DINOv2 骨幹，保留所選一層與一個分面（facet）的特徵。論文使用最大的 ViT-G/14 模型的 value 分面，取第 31 層。
2. 把每個局部特徵指派給一個含 $K$ 個中心的詞彙中最近的聚類中心 $c_k$。這些中心來自資料庫特徵上的 k-means，因此不使用任何標註。
3. 以 VLAD 聚合，把指派到各中心的特徵殘差加總：

$$
v_k = \sum_{x_i \in \text{第 } k \text{ 群}} \left(x_i - c_k\right), \qquad d = \left[v_1, \dots, v_K\right]
$$

   串接後的向量 $d$ 經過正規化，並與其所屬地點一起存入資料庫。
4. 對查詢影像，計算其描述子，並檢索距離最小的已儲存描述子。

詞彙是依領域分別建立的。作者以主成分分析（PCA）投影全域的 DINOv2 描述子，把資料庫分成城市、室內、航空、地下、退化影像與水下等領域。論文中 AnyLoc-VLAD-DINOv2 的設定使用 32 個聚類中心。

## 結果

論文在多個基準上評估前一名召回率（R@1）。與主張相關的數字如下：

| 資料集 | AnyLoc-VLAD-DINOv2 | MixVPR | CosPlace | NetVLAD |
|---|---|---|---|---|
| Baidu Mall（室內） | 75.2 | 64.4 | 41.6 | 53.1 |
| Gardens Point | 95.5 | 91.5 | 74.0 | 58.5 |
| Hawkins（非結構化） | 65.2 | 25.4 | 31.4 | 34.8 |

論文也報告，中間到較深的層效果最好，而較大骨幹帶來的增益並不均勻：在 Urban 資料上，ViT-G 相較 ViT-B 把召回率從 82.6 提高到 92.3，但在 Underwater 上則略低。摘要把優勢概括為在某些設定下效能高出現有方法最多四倍。這些數字取決於基準，應在閱讀論文完整結果後再引用。

## 限制

- 檢索本身不估計幾何，因此機器人在依賴匹配之前仍需驗證。
- 依領域分別的詞彙假設能辨識資料所屬的領域，論文以資料庫上的 PCA 流程來完成這件事。
- 最佳結果使用最大的骨幹，而擴大規模的增益在各領域之間並不一致。
- 評估是檢索召回率，閉迴路的機器人表現不在論文範圍之內。

## 相關主題

- [視覺定位](index.md) 把 AnyLoc 與另一種訓練式的方法 EigenPlaces 放在一起比較。
- [DINOv2](../../../theory/paradigms/self-supervised/non-contrastive-methods/dinov2.md) 說明 AnyLoc 所用的凍結骨幹。
- [EigenPlaces](eigenplaces.md) 代表為視角穩健性而訓練的做法。

## 開放問題

- 聚合步驟能否在不損失準確率的情況下，為小型平台上的即時使用變得夠便宜。
- 當新環境的領域不在詞彙所建立的分組之中時，增益還能保留多少。

## 參考文獻

- Keetha, N., Mishra, A., Karhade, J., Jatavallabhula, K. M., Scherer, S., Krishna, M. & Garg, S. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — 凍結特徵方法、依領域的詞彙與上文引用之基準表格的來源。
- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — AnyLoc 不經微調直接使用其特徵的自監督骨幹。
- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. https://openaccess.thecvf.com/content/ICCV2023/papers/Berton_EigenPlaces_Training_Viewpoint_Robust_Models_for_Visual_Place_Recognition_ICCV_2023_paper.pdf — 為視角穩健性而訓練的替代方案，用於比較。
- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision (2021). https://doi.org/10.1007/s11263-021-01469-5 — 具有受控視角與外觀改變的基準，與 AnyLoc 的穩健性有關。
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — 預訓練視覺編碼器從模擬轉移到真實機器人的證據。
