---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - dictionary learning
aliases:
  - k-sparse autoencoders
  - Top-k sparse autoencoder
  - k-稀疏自編碼器
  - Top-k 稀疏自編碼器
---

# k-稀疏自編碼器

k-稀疏自編碼器（k-sparse autoencoder）的做法是：對每個輸入只保留隱藏激活中最大的 $k$ 個，其餘設為零，以此強制稀疏性。Makhzani 與 Frey（2014）把它提出來，作為大多數稀疏自編碼器所用 L1 懲罰的替代方案。由於稀疏程度是由計數決定，而不是由懲罰權重決定，此方法避免了 L1 懲罰所造成的激活收縮。top-k 規則後來被用於語言模型的稀疏自編碼器，詳見[稀疏自編碼器](sparse-autoencoders.md)。

## 問題

標準的稀疏自編碼器在重建誤差與隱藏碼上的 L1 懲罰之間取捨。懲罰權重必須調整，懲罰會把活躍的單元推向零，而最後的稀疏程度並非直接設定。Makhzani 與 Frey 問：能否以一種簡單訓練、並能得到有用特徵的方式，精確地強制稀疏性？

## 核心想法

以硬性限制取代懲罰。編碼器算出隱藏激活後，保留最大的 $k$ 個，其餘全部設為零。解碼器使用這些少數單元重建輸入。由於規則本身就產生稀疏性，不需要調整懲罰權重，而且每個輸入的活躍單元數恰好為 $k$。

## 演算法

1. 對輸入 $x$ 計算隱藏的前激活 $h = W_{\text{enc}} x + b$。
2. 選出 $h$ 中最大的 $k$ 個值的索引。
3. 把 $h$ 中其餘的項設為零，得到稀疏碼 $z$。
4. 以 $\hat{x} = W_{\text{dec}} z + c$ 重建輸入。
5. 以梯度下降最小化重建誤差 $\lVert x - \hat{x} \rVert^2$。對每個輸入，梯度只流過被選中的 $k$ 個單元。

因此，此方法的稀疏程度由 $k$ 決定，而不是由懲罰權重決定。論文也描述了把學到的特徵作為分類器的輸入。

## 結果

Makhzani 與 Frey（2014）在 MNIST 與 NORB 上評估此方法。摘要報告，其分類結果優於去噪自編碼器，以及以 dropout 與受限玻爾茲曼機訓練的網路。論文的表格顯示，這個優勢主要出現在無監督特徵搭配邏輯斯回歸時。經過微調後結果參差：在 MNIST 上，深層 dropout 自編碼器的錯誤率為 0.85%，優於深層 k-稀疏模型的 0.97%；在 NORB 上，深層 dropout（7.0%）與三階 RBM（6.5%）都優於深層 k-稀疏模型（7.4%）。摘要也說此方法易於訓練、編碼非常快；論文只做了定性說明，未提供計時測量。

## 限制

- **固定的 $k$。** 每個輸入都恰好有 $k$ 個活躍單元，即使是比平均更簡單或更複雜的輸入也一樣。依輸入而變的稀疏性可能更貼合資料。
- **死單元。** 某些單元可能很少甚至從不進入前 $k$ 名，因此學不到有用的東西。top-k 規則並未直接促使每個單元都被使用。
- **資料規模。** 論文的實驗使用規模適中的影像資料集，其結果並未顯示在大型語言模型激活上的表現。
- **特徵分裂。** 和其他字典學習方法一樣，當字典變大時，k-稀疏自編碼器可能把一個概念分裂為數個特徵。

## 相關連結

top-k 規則是後來語言模型稀疏自編碼器所採用的方法，詳見[稀疏自編碼器](sparse-autoencoders.md)。它是對經典稀疏編碼的工程性修改，而稀疏編碼在神經科學中的動機是效率編碼的想法，相關連結見[稀疏編碼](../../brain-mind/computational-neuroscience/sparse-coding/index.md)。關於這些方法所分析的激活來源，即 Transformer 架構，見[Transformer](../../theory/models/transformer/index.md)。

## 應用

- 以固定的稀疏程度從影像資料中學習稀疏特徵。
- 預訓練編碼器，再把其特徵用於分類。
- 以 top-k 字典分析語言模型激活，如後來的稀疏自編碼器研究所做。

## 開放問題

- 固定的 $k$ 對自然資料而言是好的歸納偏置，還是加上了不自然的結構？
- 如何在不改變 top-k 規則的情況下避免死單元？
- 在同一個模型上，top-k 特徵與依輸入而變的稀疏特徵相比如何？

## 參考文獻

### 開創性論文

- Makhzani, A. & Frey, B. (2014). *k-Sparse Autoencoders*. ICLR 2014. https://arxiv.org/abs/1312.5663 — Introduces the k-sparse autoencoder, which enforces sparsity by keeping only the k largest hidden activations.
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*, 381, 607–609. https://doi.org/10.1038/381607a0 — Shows that a sparse coding objective trained on natural images produces receptive-field-like filters.

### 綜述與教科書

- Cunningham, H. et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv:2309.08600. https://arxiv.org/abs/2309.08600 — Applies sparse autoencoders to language model activations, the setting where top-k variants are later used.
- Gao, L. et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv:2406.04093. https://arxiv.org/abs/2406.04093 — Studies how sparse autoencoders scale with dictionary size, and proposes a top-k architecture and evaluation metrics.
- Lieberum, T. et al. (2024). *Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2*. arXiv:2408.05147. https://arxiv.org/abs/2408.05147 — Releases a suite of sparse autoencoders for an open model family.
