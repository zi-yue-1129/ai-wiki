---
translation_reviewed: 2026-10-28
related:
  - applications/robotics/visual-localisation
tags:
  - robotics
  - place recognition
  - viewpoint robustness
aliases:
  - EigenPlaces
  - 視角穩健的地點辨識
---

# EigenPlaces

EigenPlaces 由 Berton、Trivigno、Caputo 與 Masone（2023）提出，它在每個地點的多個視角上訓練地點辨識網路，使相機視角改變時描述子仍然穩定。論文的論點是：視角穩健性必須在訓練中被監督，因為只在每個地點的單一視角上學習的模型，無法可靠地學到它。上層子主題是[視覺定位](index.md)。

## 概述

EigenPlaces 是一個以地點為類別做分類訓練的卷積網路。每個地點由從不同視角拍攝的影像來表示，群組是根據場景的幾何形成的，因此同一地點會以不同的航向與位置出現。學得的描述子之後像其他地點辨識系統一樣用於檢索。

## 問題

在每個地點只有單一視角的資料上訓練的地點辨識模型，學到的特徵會依賴視角。當機器人以不同航向或稍微不同的位置回到某地時，描述子可能改變得足以錯過匹配。論文探討：以明確的多視角群組訓練，能否在不付出高訓練記憶體成本的情況下，讓描述子對視角穩健。

## 核心想法

組織訓練資料，使每個地點都以數個視角出現，並訓練網路把這些視角全部歸為同一類。分組使用幾何資訊，因此同一組內的視角確實顯示同一地點。這使視角穩健性從資料可能具備也可能不具備的性質，變成一個訓練目標。

## 運作方式

1. **切分地圖。** 以 UTM 座標表示的訓練地圖被切成 15 公尺乘 15 公尺的格子。格子被分成數個子集，使相鄰的格子不屬於同一子集，且每個訓練週期後網格會位移。
2. **為每個格子找出焦點。** 在格子內，方法對中心化的座標執行主成分分析。第一主成分近似道路方向，第二主成分近似道路的一側，也就是假設建築立面所在的方向。焦點為

$$
c_i = \mathbb{E}[X_i] + D\, v_1,
$$

   其中 $\mathbb{E}[X_i]$ 是格子中心，$v_1$ 是第一主成分，$D$ 是焦距，主要實驗中設為 10 公尺。
3. **形成類別。** 朝向焦點的方位角最接近的影像被歸為同一類。每個格子產生一個橫向類別（焦點沿第二主成分），對於正面拍攝的資料集，還會產生一個正面類別（焦點沿第一主成分）。因此每個類別包含同一地點從不同位置與航向拍攝的影像。
4. **訓練與檢索。** 卷積骨幹在這些類別上訓練，學得的描述子存入資料庫。對於查詢影像，最近的已儲存描述子即為匹配結果。

作者以 San Francisco eXtra Large（SF-XL）資料集進行訓練。

## 結果

論文以 ResNet-50 骨幹，將其與基於分類的地點辨識模型 CosPlace 比較。下表為 2048 維描述子的前一名召回率（R@1）：

| 基準 | CosPlace | EigenPlaces |
|---|---|---|
| Pitts30k | 90.9 | 92.5 |
| Tokyo 24/7 | 87.3 | 93.0 |
| SF-XL test v1 | 76.4 | 84.1 |
| MSLS Val | 87.4 | 89.1 |
| Nordland | 71.9 | 71.2 |
| SVOX Night | 50.7 | 58.9 |

EigenPlaces 在大多數基準上領先，而在 Nordland 上 CosPlace 略高。論文中關於記憶體與描述子大小的主張，是與 MixVPR 而非 CosPlace 比較：作者報告訓練時的 GPU 記憶體低於 7 GB，而 MixVPR 超過 18 GB；描述子為 2048 維，MixVPR 則為 4096 維。評估涵蓋多視角基準（例如 AmsterTime、Eynsham 與 Tokyo 24/7），以及正面視角基準（MSLS、Nordland、St Lucia 與 SVOX）。

## 限制

- 評估集都是戶外的街道與景觀影像，論文並未展示其在室內機器人情境中的轉移。
- 此方法依賴幾何資訊（例如以 GPS 為基礎的座標）來形成訓練群組，訓練集中必須有這些資訊或能估計出來。
- 夜間表現仍然偏低：以 2048 維描述子，EigenPlaces 在 SVOX Night 上達到 58.9，因此視角訓練並未解決外觀改變的問題。VPR-Bench 的研究把外觀當作另一個獨立的因素。

## 相關主題

- [視覺定位](index.md) 把 EigenPlaces 與凍結特徵的方法 AnyLoc 放在一起比較。
- [AnyLoc](anyloc.md) 代表避免訓練編碼器的替代方案。
- [以視覺目標導航](../navigation/index.md) 以另一種方式使用地點層級的檢索，來找出下一個路標。

## 開放問題

- 對於只錄製一次地點行走的機器人，能否取得多視角訓練所需的資料。
- 同一類網路在室內執行時，視角穩健性有多少能夠保留。

## 參考文獻

- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. https://openaccess.thecvf.com/content/ICCV2023/papers/Berton_EigenPlaces_Training_Viewpoint_Robust_Models_for_Visual_Place_Recognition_ICCV_2023_paper.pdf — 幾何多視角分組、SF-XL 訓練與上文基準表格的來源。arXiv 版本為 [arXiv:2308.10832](https://arxiv.org/abs/2308.10832)。
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — 地點辨識中的凍結特徵替代方案，於概覽頁中比較。
- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision (2021). https://doi.org/10.1007/s11263-021-01469-5 — 把視角與外觀改變分開的基準。
- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — 凍結替代方案所使用的自監督特徵。
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — 預訓練視覺表示在模擬到真實機器人上的證據。
