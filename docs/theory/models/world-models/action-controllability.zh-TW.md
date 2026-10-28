---
translation_reviewed: 2026-10-28
tags:
  - world models
  - controllability
aliases:
  - 動作可控性
  - action controllability
---

# 世界模型中的動作可控性

世界模型只有在動作改變時預測也跟著改變，才對規劃有用。許多學到的模型無法通過這項檢驗：它們能預測合理的下一幀，但幾乎沒有使用動作輸入。本頁說明這種失效、造成它的捷徑，以及文獻中提出的補救方法。

## 概述

以動作為條件的世界模型，輸入目前的狀態與一個動作，預測下一個狀態。在記錄資料上訓練時，模型因為預測下一幀正確而得到獎勵。在影片與機器人資料中，下一幀通常與目前的幀很接近，因此模型可以複製目前的狀態、忽略動作，同樣得到很低的預測誤差。結果是模型的預測幾乎不隨代理人的行動改變，在動作上做搜尋的規劃器也就得不到有用的訊號。

## 關鍵概念

- **忽略動作的模型（action-ignoring model）**：當動作改變時，預測的未來變化很小的模型。
- **逆動力學（inverse dynamics）**：從兩個觀測之間的轉變，預測造成該轉變的動作。常被當作輔助任務加入，讓潛在表徵保留動作資訊。
- **捷徑（shortcut）**：一條能降低訓練損失、但繞過了原本訊號的路徑，例如把答案直接複製進潛在編碼。
- **可控性（controllability）**：預測的未來對所選動作的依賴程度。

## 運作方式

文獻中描述了三種讓模型忽略動作的機制。

1. **透過逆動力學頭複製。** 如果逆模型同時看到目前與下一個觀測，它可以把下一個觀測本身編碼進「潛在動作」。Schmidt 與 Jiang（2024）指出，若沒有瓶頸，逆模型「很可能會學到直接複製」下一個觀測。他們的補救是對潛在動作做向量量化，限制傳到前向模型的資訊量。見 [LAPO](lapo.md)。
2. **透過串接洩漏。** 如果預測動作的解碼器讀取目前與下一個潛在狀態的串接，下一個狀態可能帶有與動作相關的線索，而這些線索前向預測器已經用過了。Zhang 等人（2026，預印本）報告，從兩個狀態的潛在差值解碼動作，比從串接解碼更有效。他們的消融實驗指出，「位移式動作解碼始終比端點串接更有效」。
3. **單步近視的可控性。** Rudolph 等人（2024）觀察到，單步逆動力學只在有限的時間範圍內捕捉到可控性。他們提出動作雙模擬（action bisimulation），以遞迴不變性約束來捕捉更長時程的控制相關性。

另一類補救方法是加入訓練目標，而不是改動架構。Shi 等人（2026，預印本）主張，只把動作當作輸入並不足夠。他們規範模型，使其在假設性地改變動作與場景時仍保持一致，讓模型無法依賴那些在沒有動作效果時也成立的統計規律。

## 關鍵方法

- [LAPO（Schmidt & Jiang, 2024）](lapo.md)：以量化瓶頸限制潛在動作，使它編碼幀與幀之間的變化，而不是下一幀本身。
- [DINO-WM（Zhou 等人, 2025）](dino-wm.md)：把動作的嵌入加到凍結視覺特徵的每個 patch 上，讓預測器以動作為條件。它沒有加入可控性目標。
- Delta-JEPA（Zhang 等人, 2026）與 CoCo（Shi 等人, 2026）是近期的預印本。前者改變動作解碼器讀取的訊號，後者加入反事實一致性項。它們的主張尚未經過同儕審查。

## 與其他主題的連結

以學到的模型做規劃，在[以模型為基礎的強化學習](../../paradigms/reinforcement-learning/model-based-rl/index.md)中有詳細說明。在那裡，可控性失效表現為規劃器無法分辨後果不同的動作。

能預測自身動作感覺後果的前向模型，與忽略這些動作的模型之間的區別，是運動控制中的熟悉概念。神經科學背景見[世界模型與具身智慧](index.md)。

## 應用

只要代理人要在學到的模擬器中做規劃，就需要可控的世界模型，例如從影片或記錄軌跡學習的機器人操作與導航。

## 開放問題

- 以交換動作進行的可控性測試，是否真的衡量了規劃所需的能力？
- 像從差值解碼這類洩漏修正，是否會改變預測畫面的品質？
- 多步一致性訓練的成本，與它在規劃成功率上的增益相比如何？

## 參考文獻

### 奠基性論文

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024（spotlight）. https://arxiv.org/abs/2312.10812 — 提出 LAPO，從無動作標籤的影片中學習潛在動作，並以向量量化瓶頸阻止逆模型複製下一幀。
- Rudolph, M. 等人 (2024). *Learning Action-based Representations Using Invariance*. Reinforcement Learning Conference 2024. https://arxiv.org/abs/2403.16369 — 分析單步逆動力學如何捕捉可控性，並提出適用於較長時程的動作雙模擬。
- Zhou, G.、Pan, H.、LeCun, Y. 與 Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025. https://proceedings.mlr.press/v267/zhou25t.html — 在凍結 DINOv2 patch 特徵上的動作條件預測器，用於規劃。

### 文章與預印本

- Zhang, Z. 等人 (2026). *Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding*. arXiv 預印本. https://arxiv.org/abs/2606.31232 — 從潛在差值解碼動作，而非端點串接。預印本，尚未經同儕審查。
- Shi, Y. 等人 (2026). *Overcoming Statistical Bias in Action-Controllable World Models*. arXiv 預印本. https://arxiv.org/abs/2608.04653 — 為動作可控的世界模型提出反事實一致性規範。預印本，尚未經同儕審查。
