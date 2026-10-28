---
related:
- theory/models/transformer
aliases:
  - Selective State Spaces
  - Mamba
  - Selective Scan
  - 選擇性狀態空間
tags:
  - state-space models
  - selection
  - efficient sequence modelling
translation_reviewed: 2026-10-28
---

# 選擇性狀態空間

選擇性狀態空間模型讓參數依當前輸入而變，使狀態能依內容保留部分資訊、丟棄其餘。較早的線性狀態空間模型對每個 token 套用相同的動力學，因此無法選擇要記住什麼。Mamba 展示了讓步長與讀寫狀態的投影依輸入而變，可以得到能依內容選擇相關資訊的模型；而硬體感知的掃描則讓訓練仍保有效率，即使已失去卷積的形式。

## 核心想法

在選擇性模型中，離散化步長與讀寫狀態的投影，都由每個位置的輸入計算。較大的步長會把狀態重設為當前 token，較小的步長則保留舊狀態。因此模型能學會忽略填充內容，保留重要的 token。注意力透過比較鍵與查詢達成同樣的行為。

## 做法

### Mamba

Gu 與 Dao（2023）提出了選擇性掃描。因為參數隨時間變化，早期 SSM 的卷積捷徑不再成立，因此 Mamba 以平行掃描在快速的晶片上記憶體中計算遞迴，避免為每個 token 實體化完整狀態。該模型在語言建模上的品質，據報導與相近規模的 Transformer 相當，且成本與序列長度呈線性，每個生成 token 的記憶體固定。

### Mamba-2 與結構化對偶

Dao 與 Gu（2024）證明，一種限制形式的選擇性 SSM（每個頭使用純量狀態轉移）等價於一種結構化遮罩注意力。這種對偶讓同一計算可以寫成矩陣乘法，在現代加速器上執行效率高，也釐清了 SSM 與注意力的關係。

### 混合模型

數個語言模型把選擇性 SSM 區塊與注意力區塊交錯使用，大部分深度用 SSM 層，同時保留少數注意力層以精確回憶。層類型的比例是經驗選擇的，最佳比例取決於任務。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| Mamba | 2023 | 依輸入而變的參數，搭配硬體感知的平行掃描 | [Mamba](mamba/index.md) |
| Mamba-2 | 2024 | 結構化狀態空間對偶，把選擇性 SSM 與注意力連起來 | [Mamba-2](mamba-2/index.md) |

## 取捨

- **選擇與簡單性。** 依輸入而變的動力學表達力更強，但需要較複雜的平行掃描，也不能使用簡單的卷積。
- **回憶。** 選擇有幫助，但固定大小的狀態仍會壓縮歷史，因此精確檢索許多早先項目仍比注意力弱。
- **硬體。** 速度取決於仔細的核心設計，這限制了新變體被採用的速度。

## 相關連結

選擇性 SSM 是[狀態空間模型](../index.md)家族中依輸入而變的一側，它回應了 [門控單元](../../rnn/gated-cells/index.md) 在 RNN 家族中提出的門控問題。它與注意力的對偶，則把它們與[注意力變體](../../transformer/attention-variants/index.md)頁面連結起來。

## 未解問題與更多變體

- **回憶的限制。** 選擇性 SSM 能否在不靠混合模型的情況下，於需要精確回憶許多項目的任務上追上注意力，仍在測試中。
- **被選擇的是什麼。** 學到的選擇在經驗上有效，但它學到的準則很難檢查。
- **擴展律。** 選擇性 SSM 隨資料與運算量擴展的方式，與 Transformer 相比如何，是活躍的量測領域。

## 參考文獻

### 開創性論文

- Gu, A. & Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces". arXiv:2312.00752 — 依輸入而變的狀態空間參數，以硬體感知的平行掃描計算。
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — 多項式投影框架，提供 S4 一脈所用的狀態矩陣。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Dao, T. & Gu, A. (2024). "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality". arXiv:2405.21060 — Mamba-2，以及選擇性 SSM 與結構化注意力的對偶。
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4，選擇性 SSM 所延伸的靜態結構化模型。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — 仔細設計對角線性循環的初始化，在長程基準上可與 S4 相當。
