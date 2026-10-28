---
related:
- theory/models/rnn
aliases:
  - Structured State Spaces
  - HiPPO
  - S4
  - 結構化狀態空間
tags:
  - state-space models
  - long-range memory
  - initialisation
translation_reviewed: 2026-10-28
---

# 結構化狀態空間

線性狀態空間模型只有在狀態矩陣選得仔細時，才能記住很長的歷史。隨機矩陣會以指數速度遺忘，因此這個家族的大部分設計工作都放在狀態矩陣 \(A\) 的結構與初始化上。結構化變體使用特殊的初始形式（例如 HiPPO 矩陣），再把矩陣限制為能快速計算的簡單形式。結果是一個能透過固定大小狀態記住長歷史、又能平行訓練的模型。

## 概觀

| 變體 | 狀態矩陣 | 主要想法 | 例子 |
|---|---|---|---|
| 隨機或無約束 | 自由學習 | 簡單，但遺忘很快 | 早期的線性循環 |
| HiPPO | 人工設計 | 把歷史投影到正交多項式上 | HiPPO-LegS |
| 正規加低秩 | 結構化 | 對角加低秩，可用柯西核計算 | S4 |
| 對角 | 複數對角 | 更簡單，效果接近 | S4D、S5 |

## 做法

### HiPPO 初始化

HiPPO 定義了一個狀態矩陣，使其在任何時刻都儲存輸入歷史在某個選定測度下的最佳多項式近似。Gu 等人（2020）指出，這種投影給出一個以原則方式壓縮過去的狀態，由它建構的遞迴能表示長程依賴。這個矩陣是固定的設計，作為學習的起點。

### S4 與結構化參數化

S4 把狀態矩陣表示為對角加低秩矩陣，可以轉成卷積核並用快速演算法計算。這使訓練速度與卷積相當，而 HiPPO 結構提供了長記憶。Gu 等人（2021）在長程基準上回報了強勁結果，那些任務上 Transformer 表現不佳，這也是該家族引起廣泛注意的原因。

### 對角與線性循環變體

後續工作顯示，帶有複數項的對角狀態矩陣，能以較簡單的實作獲得大部分好處。S5 使用對角形式加上平行掃描，線性循環單元則對對角循環做仔細的初始化。這些變體讓這個家族更容易實作與延伸。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| S4 | 2021 | 結構化的狀態矩陣，其卷積核可以快速計算 | [S4](s4/index.md) |
| HiPPO | 2020 | 把輸入歷史投影到多項式上，用來初始化狀態矩陣 | [HiPPO](hippo/index.md) |
| S4D | 2022 | 帶有仔細初始化的複數對角狀態矩陣 | [S4D](s4d/index.md) |
| S5 | 2022 | 帶有平行掃描的對角狀態空間層 | [S5](s5/index.md) |
| 線性循環單元 | 2023 | 對對角線性循環做仔細的初始化 | [線性循環單元](linear-recurrent-units/index.md) |

## 取捨

- **固定動力學。** 因為矩陣不依輸入而變，模型無法決定保留什麼，這限制了依內容的回憶。選擇性變體就是為了解決這點。
- **對初始化敏感。** 效能取決於初始化與時間尺度參數，因此設定很重要。
- **表達力。** 線性時不變系統只能計算輸入歷史的線性函數，與注意力相比這是實際的限制。

## 相關連結

結構化家族是 [狀態空間模型](../index.md) 家族中靜態、不依輸入而變的一側，其依輸入而變的延伸見[選擇性狀態空間](../selective-state-spaces/index.md)。它與較早循環觀點的連結，是 [RNN](../../rnn/index.md) 家族也研究的長記憶問題。

## 未解問題與更多變體

- **測度的選擇。** HiPPO 對歷史使用特定的測度。其他測度是否適合其他資料類型，研究尚少。
- **簡單與記憶。** 對角形式較簡單，在基準上效果接近，但它為何如此有效，尚未完全理解。
- **多維輸入。** 把結構推廣到影像與其他網格，是有多種相互競爭設計的活躍領域。

## 參考文獻

### 開創性論文

- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". [arXiv:2008.07669](https://arxiv.org/abs/2008.07669) — 推導 HiPPO 狀態矩陣，透過多項式投影使循環能記住歷史。
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". [arXiv:2111.00396](https://arxiv.org/abs/2111.00396) — S4，具正規加低秩結構與快速卷積核。
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". [arXiv:2206.11893](https://arxiv.org/abs/2206.11893) — 仔細初始化的複數對角狀態矩陣，能以較簡單的實作匹敵 S4。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". [arXiv:2208.04933](https://arxiv.org/abs/2208.04933) — S5，帶有平行掃描的對角狀態空間層。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". [arXiv:2303.06349](https://arxiv.org/abs/2303.06349) — 對對角線性循環做仔細初始化，在長程基準上與 S4 相當。
