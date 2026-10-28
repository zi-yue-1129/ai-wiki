---
translation_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/models/world-models
tags:
  - robotics
  - navigation
  - foundation model
aliases:
  - GNM
  - General Navigation Model
  - 通用導航模型
---

# GNM：通用導航模型

GNM 由 Shah、Sridhar、Bhorkar、Hirose 與 Levine（2022）提出，是一個以目標為條件的單一導航模型，訓練資料來自六種不同的機器人。它以目前的觀測與目標影像為輸入，預測一段短的、經正規化的路點序列。其主要結論關於動作的表示：依各機器人的最高速度縮放的路點，比原始速度更能跨平台轉移。所屬的子主題是 [以視覺目標導航](index.md)。

## 概述

導航策略通常只用一台機器人的資料訓練，當平台改變時表現就會下降。GNM 探討的是，來自許多相異但結構相似的機器人的資料能否匯集成一個模型。作者指出兩個讓匯集成為可能的設計選擇：使用時間上下文，以及標準化的動作空間。他們報告，在異質資料上訓練的全能策略（omnipolicy）優於只在任一單一資料集上訓練的策略，並且可以部署到訓練集中沒有的機器人上（Shah et al., 2022）。

## 問題

以視覺為基礎的導航策略需要資料，而在單一機器人上蒐集資料很慢。不同機器人的資料有不同的相機、速度與動力學，因此直接匯集可能使模型混淆。問題在於：哪一種動作表示能讓不同機器人的軌跡可以互相比較，以及模型還需要看到什麼，才能善加利用這些資料。

## 核心想法

標準化動作空間。每個路點都依機器人的最高速度縮放，因此不論機器人大小，一單位的移動都代表其能力的相同比例。模型也看到一段過去影像的短歷史，提供單一影像無法區分的動作所需的上下文。單一網路同時在所有機器人的資料上訓練。

## 方程式或演算法

策略有兩個頭，以監督式學習聯合訓練：

1. **視覺編碼器。** 分別以 MobileNetV2 編碼器處理目前的觀測（含其上下文影像）與目標影像。兩個嵌入向量串接後，通過三個全連接層。
2. **時間距離。** 一個頭預測到目標的正規化時間距離，以正例與負例配對訓練。
3. **正規化路點。** 第二個頭預測五個未來路點，每個路點包含相對位置與偏航角變化，並依機器人的最高速度縮放。它只以正例配對訓練，使用迴歸損失。

論文使用五個過去觀測作為上下文。兩個頭之間損失的權重，在本頁所讀的正文中未說明。

## 結果

在動作空間的比較中，作者以 LoCoBot 在十個環境中評估。報告的是簡單與中等環境的成功率（Shah et al., 2022, Table V）：

| 輸出空間 | 簡單 | 中等 |
|---|---|---|
| 速度 | 0.73 | 0.54 |
| 原始路點 | 0.42 | 0.26 |
| 正規化路點 | 1.00 | 0.95 |

表 II 比較 GNM 與兩個單一機器人基線 GS 與 RECON，涵蓋四台機器人：LoCoBot、DJI Tello、Vizbot 與 Clearpath Jackal（Shah et al., 2022, Table II）。數值為平均成功率。

| 方法 | LoCoBot | DJI Tello | Vizbot | Jackal |
|---|---|---|---|---|
| GS | 0.26 | 0.21 | 0.51 | 0.31 |
| RECON | 0.62 | 0.79 | 0.26 | 0.68 |
| GNM | 0.96 | 0.99 | 0.93 | 0.94 |

論文的圖說指出，共享策略在每台機器人上都優於該機器人上最佳的單一機器人策略。論文沒有與 ViNG 的直接比較。

## 限制

- 模型以模仿學習訓練，因此繼承行為複製的限制，包括對示範資料分布的敏感性。
- 正規化需要每台機器人的最高速度，每個新平台都必須事先知道。
- 正文與表 I 給出的資料集數量與資料時數不一致，因此需要精確數字時，應以論文的表格為準。

## 相關連結

- [ViNG](ving.md) 是同一研究脈絡中較早的方法，使用觀測圖，並在單一機器人上預測相對位姿。
- [ViNT](vint.md) 是較大的 Transformer 後繼模型，訓練於更多資料集。
- [NoMaD](nomad.md) 以擴散模型取代迴歸頭，並加入與目標無關的探索。
- [視覺教導與重播](visual-teach-and-repeat.md) 是不需學習策略的經典方法。

## 開放問題

- 正規化表示能否適用於控制介面不是平面速度的機器人。
- 要讓共享模型可靠地適應新平台，需要多少機器人專屬資料。

## 參考文獻

- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N. & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — 共享模型、標準化動作空間與輸出空間比較的來源。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N. & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — 將相同想法擴展到更多資料，並加入時間距離與路點輸出的 Transformer 後繼模型。
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N. & Levine, S. (2021). *ViNG: Learning Open-World Navigation with Visual Goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — 較早的單一機器人方法，結合學習的策略與拓撲圖。
- Sridhar, A., Shah, D., Glossop, C. & Levine, S. (2023). *NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration*. arXiv. https://arxiv.org/abs/2310.07896 — 基於擴散的後繼模型，用於以目標為條件的導航與探索。
