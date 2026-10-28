---
translation_reviewed: 2026-10-28
tags:
  - robotics
  - visual localisation
  - place recognition
  - visual representation
aliases:
  - Visual localisation
  - Visual place recognition
  - 視覺定位
---

# 視覺定位

視覺定位是藉由比較機器人目前的相機畫面與先前見過的影像，來判斷它位於何處。最常見的形式是地點辨識：給定一張查詢影像，從資料庫中檢索出相符的影像。機器人需要這個能力，以便從漂移中恢復、閉合迴路，並在地圖中重新定位。本子主題涵蓋特徵如何學習、方法如何在視角與外觀改變下被評估，以及凍結的預訓練編碼器如何改變這個領域。

## 概述

地點辨識系統有三個部分：把影像轉成描述子的編碼器、把局部特徵合併成單一向量的聚合步驟，以及在資料庫上的最近鄰搜尋。各種方法的差異在於如何訓練編碼器，以及是否使用凍結的基礎模型，或為地點辨識專門訓練的網路。

有兩種改變很重要。一是視角改變，例如不同的航向或位置；二是外觀改變，例如光照、天氣或季節的變化。一個方法可能對其中一種很穩健，對另一種卻很脆弱，因此評估必須兩者都考慮。

## 關鍵方法

每個方法都有自己的頁面。此處的概述與比較只是簡短的整理。

| 方法 | 編碼器 | 訓練 | 改變的部分 |
|---|---|---|---|
| [AnyLoc](anyloc.md)（Keetha 等人，2023） | 凍結的 DINOv2 特徵，不經訓練即聚合 | 編碼器不需訓練 | 顯示通用基礎模型可以與為任務訓練的地點辨識編碼器相當或更好 |
| [EigenPlaces](eigenplaces.md)（Berton 等人，2023） | 卷積網路 | 在每個地點的多個視角上訓練 | 把視角穩健性變成訓練目標，而不是資料中偶然具備的性質 |

## 在改變下的評估

Zaffar 等人（2021）建立了一個基準，把視角改變與外觀改變以受控的幅度分開。結果顯示，航向與三維偏移比橫向偏移更傷害匹配，而方向性的光照比均勻的亮度變化更傷害匹配。這個基準之所以有用，是因為混合資料集上的單一分數會隱藏是哪一種改變造成失敗。

## 機器人中的預訓練表示

同樣的問題也出現在機器人操作與導航中。Burns 等人（2023）發現，預訓練的視覺表示對光照與紋理改變的穩健性各不相同，而預訓練時所用的增強方式，比監督方式的選擇更重要。Silwal 等人（2024）報告，預訓練編碼器在真實機器人上能維持效能，而從頭訓練的編碼器則不行。這些結果支持以凍結的基礎模型特徵作為機器人地點辨識的起點，前提是其穩健性要在目標平台上測量。

## 相關主題

- [機器人](../index.md) 把視覺定位放在本站其他機器人任務之中。
- [以視覺目標導航](../navigation/index.md) 使用相同的檢索想法，在影像圖中找出下一個路標。
- [DINOv2](../../../theory/paradigms/self-supervised/non-contrastive-methods/dinov2.md) 說明 AnyLoc 所用的凍結骨幹。

## 開放問題

- 在一個季節訓練的描述子，能否在長時間後對差異很大的條件良好地轉移。
- 多視角訓練所得的視角穩健性，能否在只錄製一次行走的機器人上低成本取得。

## 參考文獻

- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision, 129(7), 2136–2174. arXiv:2005.08135. https://arxiv.org/abs/2005.08135 — 把視角改變與外觀改變分開的基準。
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — 用於地點辨識的凍結基礎模型特徵。
- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. arXiv:2308.10832. https://arxiv.org/abs/2308.10832 — 在每個地點的多個視角上訓練地點辨識，以達到視角穩健性。
- Burns, K., Witzel, Z., Hamid, J. I., et al. (2023). *What makes pre-trained visual representations successful for robust manipulation?* arXiv:2312.12444. https://arxiv.org/abs/2312.12444 — 視覺偏移下預訓練表示的穩健性。
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* ICRA 2024. arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — 預訓練編碼器在機器人上的模擬到真實轉移。
