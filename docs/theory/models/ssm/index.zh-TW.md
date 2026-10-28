---
related:
- theory/models/rnn
- theory/models/transformer
aliases:
  - State-Space Models
  - SSM
  - Mamba
  - 狀態空間模型
tags:
  - state-space models
  - sequence modelling
  - architecture
translation_reviewed: 2026-10-28
---

# 狀態空間模型

狀態空間模型（SSM）用一個隱藏狀態來描述序列，該狀態依線性遞迴演化，輸出則從狀態讀出。這個遞迴可以像 RNN 一樣逐步執行，使每個生成 token 的成本固定；也可以展開成對整個序列的卷積，允許平行訓練。近期的 SSM 架構，從 S4 與 Mamba 開始，顯示這種設計能以遠少於注意力的記憶體建模很長的序列，同時在語言上接近 Transformer。它們是繼注意力之後的第二大序列家族，而且越來越多模型把兩者混合使用。

## 核心想法

連續的線性系統 \(x'(t)=Ax(t)+Bu(t)\)、\(y(t)=Cx(t)\) 會被離散化為逐步的遞迴。矩陣 \(A\) 控制狀態如何記住過去的輸入，這是關鍵的設計問題。狀態空間家族探討如何選擇 \(A\)，使狀態能摘要很長的歷史；而在較新的模型中，還探討如何讓參數依輸入而變。這兩個問題定義了下面的組件。

## 組件與變體

- [結構化狀態空間](structured-state-spaces/index.md)：如何初始化與結構化 \(A\)（HiPPO、對角形式），使長程記憶成為可能，如 S4、S5 與線性循環單元。
- [選擇性狀態空間](selective-state-spaces/index.md)：依輸入而變的參數，讓模型決定保留什麼，如 Mamba 與 Mamba-2。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| S4 | 2021 | 結構化的狀態矩陣，其卷積核可以快速計算 | [S4](structured-state-spaces/s4/index.md) |
| Mamba | 2023 | 依輸入而變的參數，搭配硬體感知的平行掃描 | [Mamba](selective-state-spaces/mamba/index.md) |

S4 提供可以像卷積一樣快速訓練的長記憶狀態。Mamba 讓參數依輸入而變，使模型能決定保留什麼。

## 取捨

- **成本。** 循環式推論每個 token 只需固定記憶體，且沒有鍵值快取；注意力則隨上下文長度增長。
- **回憶能力。** 固定大小的狀態必須壓縮歷史，因此精確檢索較早的細節比注意力弱。這是混合模型保留少數注意力層的主要原因。
- **訓練。** 線性時不變的 SSM 可用卷積平行訓練，選擇性模型則需要硬體感知的平行掃描。

## 應用範圍

音訊、基因組學與時間序列等長序列建模，以及需要低成本長上下文的語言模型。混合模型會交錯使用 SSM 與注意力層。

## 相關連結

SSM 是 [RNN](../rnn/index.md) 家族所探討之循環記憶取捨的現代答案，也是 [Transformer](../transformer/index.md) 家族中注意力的主要替代方案。Transformer 頁面把它們列為替代架構，而 [注意力變體](../transformer/attention-variants/index.md) 頁面則介紹另一條高效長上下文的路線。

## 未解問題與更多變體

- **回憶與效率的取捨。** 純 SSM 能否在需要精確回憶許多項目的任務上追上注意力，尚無定論，混合模型是常見的折衷。
- **選擇的理論。** 依輸入而變的狀態轉移威力強，但較難分析，其表達力與注意力相比仍在摸索中。
- **硬體。** 每一種新變體都需要高效的掃描與核心實作，這會減慢新設計的採用。

## 參考文獻

### 開創性論文

- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". [arXiv:2111.00396](https://arxiv.org/abs/2111.00396) — S4，具結構化狀態空間，能高效處理很長的序列。
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". [arXiv:2008.07669](https://arxiv.org/abs/2008.07669) — 為狀態矩陣提供長程記憶的 HiPPO 框架。
- Gu, A. & Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces". [arXiv:2312.00752](https://arxiv.org/abs/2312.00752) — 依輸入而變的狀態空間參數，並以硬體感知的平行掃描實作。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Dao, T. & Gu, A. (2024). "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality". [arXiv:2405.21060](https://arxiv.org/abs/2405.21060) — Mamba-2，以及選擇性 SSM 與結構化注意力之間的對偶關係。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". [arXiv:2303.06349](https://arxiv.org/abs/2303.06349) — 仔細設計的線性循環單元，在長序列基準上能與 SSM 匹敵。
