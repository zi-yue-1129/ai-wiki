---
translation_reviewed: 2026-10-28
tags:
  - world models
  - self-supervised
  - planning
aliases:
  - DINO-WM
  - DINO 世界模型
---

# DINO-WM

DINO-WM 是一種潛在世界模型，預測的是未來的視覺特徵，而不是像素。特徵來自凍結、預先訓練好的 DINOv2 編碼器，並由一個以動作為條件的 transformer 預測這些特徵如何改變。作者用這個預測器做規劃，不需要任務專用的訓練，他們稱之為零樣本規劃（zero-shot planning）。

## 問題

以像素為單位的世界模型，會把容量花在與控制無關的細節上，例如紋理與光照。若從零開始，只用機器人自己的資料訓練預測器，成本也很高。DINO-WM 探討：一個不使用動作、通用的視覺表徵，能否作為規劃用世界模型的狀態空間。

## 核心想法

觀測模型保持凍結。作者指出，「觀測模型在訓練與測試期間都保持凍結」。預測器是基於 ViT 設計的 transformer。每個動作經過一個小型 MLP，得到的向量串接到每一幀的每個 patch 向量上。訓練使用離線軌跡：給定過去幀的 patch 特徵與所採取的動作，預測器預測未來幀的 patch 特徵。規劃時，在預測的特徵空間中搜尋動作序列，並以其最終預測特徵與目標影像的吻合程度評分。

## 運作方式

1. 用凍結的編碼器把每一幀編碼成 DINOv2 patch 特徵。
2. 用 MLP 嵌入每個動作，並把嵌入串接到每個 patch token 上。
3. 在離線軌跡上訓練因果 transformer 預測器，預測未來的 patch 特徵。
4. 測試時，在預測的特徵空間中以最佳化方式選擇動作序列，並以目標觀測為評分標準。

## 關鍵方法

DINO-WM 是為動作條件式預測器建立方法的一種方式。與其他方法相比：

- 相對於 [LAPO](lapo.md)，後者從影片學習動作本身；DINO-WM 假設動作已知，專注於預測器的狀態空間。
- 相對於 [V-JEPA 2](v-jepa-2.md)，後者先在大量影片上訓練，再用機器人影片做後訓練；DINO-WM 則保持視覺編碼器凍結，只在目標環境的軌跡上訓練預測器。

## 結果

摘要指出，該方法在數個環境中以離線資料學到的預測器進行規劃。具體數字見論文，應直接從論文抄錄，而非從二手摘要取得。

## 限制

- 預測器只能預測凍結編碼器保留下來的內容。DINOv2 特徵捨棄的細節無法被預測。
- 把動作串接到每個 token 是一種簡單的條件化方式。它能否讓預測器對動作保持敏感，正是 [動作可控性](action-controllability.md) 所討論的問題。

## 與其他主題的連結

DINO-WM 位於[自監督](../../paradigms/self-supervised/index.md)視覺表徵學習與以模型為基礎的規劃之間。它以潛在預測為目標，與預測表徵而非像素的聯合嵌入預測家族相關。同一世界模型家族在[總覽頁](index.md)中有說明。

## 應用

從影像進行機器人規劃，以及在能用記錄軌跡訓練預測器的模擬環境中做目標導向的導航或操作。

## 開放問題

- 為外觀而訓練的凍結編碼器，是否適合接觸密集的任務。
- 規劃成本如何隨時程長度與動作空間大小增加。

## 參考文獻

### 奠基性論文

- Zhou, G.、Pan, H.、LeCun, Y. 與 Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025. https://proceedings.mlr.press/v267/zhou25t.html — 提出此方法：在凍結 DINOv2 patch 特徵上的動作條件預測器，用於零樣本規劃。arXiv 版本見 https://arxiv.org/abs/2411.04983。

### 文章與預印本

- Oquab, M. 等人 (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv 預印本. https://arxiv.org/abs/2304.07193 — 自監督視覺特徵，DINO-WM 把其 patch token 用作凍結的狀態空間。
- Assran, M. 等人 (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning*. arXiv 預印本. https://arxiv.org/abs/2506.09985 — 以影片訓練的替代方案，透過機器人影片後訓練加入動作條件。
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv 預印本. https://arxiv.org/abs/1803.10122 — 早期的潛在世界模型，策略在模型自身模擬的環境中訓練。
- Moerland, T. M. 等人 (2020). *Model-based Reinforcement Learning: A Survey*. arXiv 預印本. https://arxiv.org/abs/2006.16712 — 學習得來的動力學模型及其在規劃中用法的綜述。
