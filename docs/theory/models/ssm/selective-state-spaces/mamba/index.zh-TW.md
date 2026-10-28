---
related:
- theory/models/ssm/selective-state-spaces
- theory/models/ssm
aliases:
  - Linear-Time Sequence Modeling with Selective State Spaces
  - Mamba
  - 線性時間序列建模
tags:
  - state-space models
  - selection
  - hardware-aware scan
translation_reviewed: 2026-10-28
---

# Mamba

Mamba 是 Gu 與 Dao 在 2023 年的論文 "Mamba: Linear-Time Sequence Modeling with Selective State Spaces" 中提出的選擇性狀態空間模型。它讓狀態空間的參數依輸入而變，使模型能依每個 token 決定保留什麼；同時，硬體感知的平行掃描讓訓練仍保有效率。

## 問題

注意力的計算量隨視窗長度呈二次成長，而次二次方的模型在離散、資訊密集的資料（例如文字）上效果較差。作者把此歸因於基於內容的推理能力較弱。

## 核心想法

核心是選擇。參數 Δ、B 與 C 都是輸入的函數，因此模型可以依當前 token 保留或丟棄資訊。依輸入而變的設計去除了卷積形式，因此遞迴以硬體感知的平行掃描執行，避免把展開的狀態寫入緩慢的 GPU 記憶體。

## 方程式或演算法

在零階保持（zero-order hold）下，離散轉移為 \(\bar A = \exp(\Delta A)\)，其中 Δ 在每一步由輸入計算。遞迴則為

\[
h_t = \bar A_t\, h_{t-1} + \bar B_t\, x_t,
\]

並以掃描的方式求值。

## 結果

摘要報告其吞吐量比 Transformer 高 5 倍。論文指出，Mamba-3B 在預訓練與下游評估中，勝過同規模的 Transformer，並與兩倍規模的 Transformer 相當。掃描在 A100 GPU 上最多比先前方法快 3 倍。

## 限制

效率取決於硬體感知的掃描。去除了早期 SSM 為求速度所用的卷積形式，因此模型需要這種專用的核心才能快速執行。

## 相關連結

Mamba 是[選擇性狀態空間](../index.md)家族中依輸入而變的成員，該家族位於更大的[狀態空間模型](../../index.md)家族之中。它延伸了靜態的結構化模型 [S4](../../structured-state-spaces/s4/index.md)，並放棄了 S4 的卷積形式。選擇機制回應了 RNN 家族中 [門控單元](../../../rnn/gated-cells/index.md) 提出的門控問題；它與注意力的對偶，則把它與[注意力變體](../../../transformer/attention-variants/index.md)頁面連結起來。

## 未解問題與更多變體

- **回憶的限制。** 選擇性 SSM 能否在不靠混合模型的情況下，於需要精確回憶許多項目的任務上追上注意力，仍在測試中。
- **被選擇的是什麼。** 選擇在經驗上有效，但模型學到的準則很難檢查。
- **擴展律。** 選擇性 SSM 隨資料與運算量擴展的方式，與 Transformer 相比如何，是活躍的量測領域。

## 參考文獻

### 開創性論文

- Gu, A. & Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces". arXiv:2312.00752 — 依輸入而變的狀態空間參數，以硬體感知的平行掃描計算。
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4，具結構化狀態空間，能高效處理很長的序列。
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — 為狀態矩陣提供長程記憶的 HiPPO 框架。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Dao, T. & Gu, A. (2024). "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality". arXiv:2405.21060 — Mamba-2，以及選擇性 SSM 與結構化注意力之間的對偶關係。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — 仔細設計的線性循環單元，在長序列基準上能與 SSM 匹敵。
