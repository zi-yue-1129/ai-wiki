---
translation_reviewed: 2026-10-28
tags:
  - robotics
  - place recognition
  - viewpoint robustness
aliases:
  - EigenPlaces
  - 視角穩健的地點辨識
---

# EigenPlaces

EigenPlaces 由 Berton、Trivigno、Caputo 與 Masone（2023）提出，它在每個地點的多個視角上訓練地點辨識網路，使相機視角改變時描述子仍然穩定。論文的論點是：視角穩健性必須在訓練中被監督，因為只看過每個地點單一視角的模型，不會可靠地學到它。上層子主題是[視覺定位](index.md)。

## 概述

EigenPlaces 是一個以地點為類別做分類訓練的卷積網路。每個地點由從不同視角拍攝的影像群組來表示，群組是根據場景的幾何形成的，因此同一地點會以不同的航向與位置出現。學得的描述子之後像其他地點辨識系統一樣用於檢索。

## 問題

在每個地點只有單一視角的資料上訓練的地點辨識模型，學到的特徵會依賴視角。當機器人以不同航向或稍微不同的位置回到某地時，描述子可能改變得足以錯過匹配。論文探討：以明確的多視角群組訓練，能否在不付出高記憶體成本的情況下，讓描述子對視角穩健。

## 核心想法

組織訓練資料，使每個地點都以數個視角出現，並訓練網路把這些視角全部歸為同一地點。分組使用幾何資訊，因此同一組內的視角確實屬於同一地點。這使視角穩健性從資料可能具備也可能不具備的性質，變成一個訓練目標。

## 運作方式

1. 利用場景的幾何資訊，為每個地點從不同視角的影像建立訓練群組。
2. 以地點為類別，用分類式的目標訓練卷積骨幹，每個地點以其多視角群組表示。
3. 把學得的描述子用於檢索：為資料庫儲存描述子，並為每個查詢找出最近的已儲存描述子。

## 結果

作者報告，在他們測試的大多數地點辨識基準上達到最先進的結果；他們也報告，相較於早期以分類為基礎的 CosPlace，此方法使用較少的訓練記憶體，並產生較小的描述子。實驗在戶外、街道層級的大型資料集上進行。確切數字取決於所用的基準，應在論文表格中核對。

## 限制

- 結果來自戶外的街道層級資料，論文並未展示其在室內機器人情境中的轉移。
- 此方法依賴幾何資訊來形成多視角群組，訓練集中必須有這些資訊或能估計出來。
- 視角訓練本身並不處理外觀改變，Zaffar 等人（2021）的基準把外觀改變當作另一個獨立的因素。

## 相關主題

- [視覺定位](index.md) 把 EigenPlaces 與凍結特徵的方法 AnyLoc 放在一起比較。
- [AnyLoc](anyloc.md) 代表避免訓練編碼器的替代方案。
- [以視覺目標導航](../navigation/index.md) 以另一種方式使用地點層級的檢索，來找出下一個路標。

## 開放問題

- 對於只錄製一次地點行走的機器人，能否取得多視角訓練所需的資料。
- 同一網路在室內執行時，視角穩健性有多少能夠保留。

## 參考文獻

- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. arXiv:2308.10832. https://arxiv.org/abs/2308.10832 — 多視角訓練與戶外結果的來源。
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — 地點辨識中的凍結特徵替代方案。
- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision, 129(7), 2136–2174. arXiv:2005.08135. https://arxiv.org/abs/2005.08135 — 把視角與外觀改變分開的基準。
- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — 凍結替代方案所依賴的自監督特徵。
- Burns, K., Witzel, Z., Hamid, J. I., et al. (2023). *What makes pre-trained visual representations successful for robust manipulation?* arXiv:2312.12444. https://arxiv.org/abs/2312.12444 — 預訓練增強方式在視覺穩健性中的角色。
