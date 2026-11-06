---
translation_reviewed: 2026-11-06
related:
  - theory/models/transformer/index.md
---

# Informer

Informer 把 [Transformer](../transformer/index.md) 改造用於長序列時間序列預測。它以稀疏近似取代完整的自注意力，縮短編碼器層之間的序列，並一次產生整段預測。它是[時間序列預測](index.md)頁面比較的三個代表性方法之一。

## 問題

長期預測需要模型讀入很長的歷史，並向前預測許多步。標準的自注意力會將每個位置與其他所有位置比較，因此其時間與記憶體隨輸入長度的平方成長。原始的編碼器–解碼器 Transformer 也是一步一步產生輸出，這會造成誤差累積並拖慢推論。論文主張長序列預測需要很高的預測能力，但現有的 Transformer 對此來說成本過高。

## 核心想法

Informer 改動了 Transformer 的三個部分：

- **ProbSparse 自注意力。** 每個查詢依其注意力分布偏離均勻分布的程度來評分。只有分數最高的查詢會注意所有的鍵，其餘查詢則以值的平均作為輸出。論文報告，這使注意力的時間與記憶體成本降為 $O(L \log L)$，其中 $L$ 是輸入長度。
- **自注意力蒸餾。** 在編碼器層之間，序列長度約減半，使很長的輸入能以較少的記憶體與計算處理。
- **生成式解碼器。** 解碼器接收一段起始片段與一組佔位位置，並在一次前向傳播中預測整段輸出序列，而不是逐步產生。

## 方程式與演算法

標準注意力為

$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d}}\right) V.$$

ProbSparse 注意力保留這個形式，但會估計哪些查詢較重要。對查詢 $q_i$，稀疏度分數是它與各鍵內積中最大值與平均值之差：

$$M(q_i, K) = \max_j \frac{q_i k_j^\top}{\sqrt{d}} - \frac{1}{L_K}\sum_{j} \frac{q_i k_j^\top}{\sqrt{d}}.$$

論文依此衡量選出分數最高的查詢，為它們計算完整注意力，並以值的平均填補其餘列的輸出。由於只有少數查詢需要完整計算，成本低於標準注意力。

## 結果

摘要報告，Informer 在四個大型資料集上顯著優於既有方法。論文的比較是在作者所選的資料集與預測期上進行的，各設定的數字應查閱原文表格，而不應只依此摘要。

## 限制

- **評估範圍。** 基準由作者選定。後來的研究發現，在其他基準上更簡單的模型可以勝過它（見下文）。
- **注意力未必是瓶頸。** 自注意力具有排列不變性，因此輸入的順序必須透過位置編碼提供。Zeng 等人（2022）認為這會損失時間順序，並報告在九個真實資料集上，簡單的單層線性模型勝過以 Transformer 為基礎的預測器。
- **稀疏近似。** 稀疏度分數只決定哪些查詢要完整計算，因此其效益取決於資料中注意力是否集中在少數鍵上。
- **設計依賴長輸入。** 蒸餾與生成式解碼器是為長輸入與長輸出設計的。若預測期很短，較簡單的模型可能更合適。

## 關聯

Informer 沿用 [Transformer](../transformer/index.md) 頁面所述的注意力機制，以及其[注意力變體](../transformer/attention-variants/index.md)。序列預測的循環替代方法是 [DeepAR](deepar.md)，見[循環神經網路](../rnn/index.md)頁面；非注意力的替代方法是 [N-BEATS](n-beats.md)。

## 參考文獻

### 開創性論文

- Zhou, H., Zhang, S., Peng, J., Zhang, S., Li, J., Xiong, H. & Zhang, W. (2020). *Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting*. arXiv. https://arxiv.org/abs/2012.07436 — 原始論文：用於長期預測的 ProbSparse 注意力、自注意力蒸餾與生成式解碼器。
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — 提出 Transformer 與 Informer 所近似的縮放點積注意力。
- Zeng, A., Chen, M., Zhang, L. & Xu, Q. (2022). *Are Transformers Effective for Time Series Forecasting?* arXiv. https://arxiv.org/abs/2205.13504 — 批判性研究，在九個真實資料集上比較 Transformer 預測器與簡單線性模型。

### 綜述與教科書

- Lim, B. & Zohren, S. (2020). *Time Series Forecasting With Deep Learning: A Survey*. arXiv. https://arxiv.org/abs/2004.13408 — 綜述多步預測的編碼器與解碼器設計，包括以注意力為基礎的設計。
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — 可免費閱讀的教科書，介紹以注意力為基礎的模型所比較的古典預測方法。
