---
translation_reviewed: 2026-10-28
---

# 最大概似估計

最大概似估計（MLE）選出使觀測資料機率最大的參數值。它是擬合參數模型的預設方法，以交叉熵或均方誤差訓練神經網路，就是其實例。本頁是[機率與統計](index.md)的一部分。

## 概述

假設資料 \(D = \{x_1, \dots, x_N\}\) 是從模型 \(p(x\mid\theta)\) 獨立抽出的，其中參數 \(\theta\) 未知。概似 \(L(\theta) = \prod_i p(x_i\mid\theta)\) 衡量在每個 \(\theta\) 之下資料出現的機率。MLE 選出使其最大的 \(\theta\)。由於對數函數遞增，最大化對數概似可得到相同答案，而且能把乘積變成和。

## 關鍵概念

- **概似**：固定資料時，\(L(\theta)\) 是 \(\theta\) 的函數。它不是關於 \(\theta\) 的機率分布。
- **負對數概似（NLL）**：\(-\log L(\theta)\)。最小化 NLL 是常見的訓練目標。
- **一致性**：在標準正則條件下，隨著樣本增加，MLE 收斂到真實參數。
- **漸近常態性**：樣本夠大時，MLE 近似服從以真值為中心的高斯分布，由此可得標準誤。

## 運作方式

MLE 求解

\[
\hat\theta_{\text{MLE}} = \arg\max_\theta \sum_{i=1}^{N} \log p(x_i\mid\theta) = \arg\min_\theta \; \text{NLL}(\theta).
\]

兩個例子說明此概念。對於均值與變異數皆未知的高斯分布，均值的 MLE 是樣本平均，而變異數的 MLE 除以 \(N\) 而非 \(N-1\)，因此在小樣本下有偏差。對於類別分類器，最大化正確標籤的概似，即等同於最小化交叉熵損失。

Fisher（1922）給出此方法的現代形式，並提出估計量的一致性、效率與充分性等性質。Bishop（2006）與 Murphy（2022）則以機器學習的角度說明同一內容。

## 主要方法

- [最大後驗估計](maximum-a-posteriori.md)：在對數概似上加上對數先驗。先驗為平坦時即退化為 MLE。

## 與其他頁面的連結

- [機率與統計](index.md)提供本領域的概述與其他估計量。
- [機率與貝氏方法](../../paradigms/probabilistic/index.md)保留完整後驗，而非只取一個點估計。
- [資訊理論](../../information-theory/index.md)說明資料分布與模型之間的交叉熵，等於負對數概似的期望值。

## 應用

- **分類器訓練**：交叉熵損失，即類別分布的 NLL（Bishop, 2006）。
- **語言模型**：下一個詞元的訓練，即最大化觀測文本的對數概似。
- **迴歸**：在常數變異數的高斯雜訊下，最小平方擬合就是 MLE。

## 開放問題

- 資料稀少或模型很靈活時，MLE 可能過擬合，而單靠概似無法說明應如何信任擬合結果。
- 在高維模型中，概似可能有多個同樣好的極大值或平坦區域，此時 MLE 並不唯一。

## 參考文獻

### 奠基性論文

- Fisher, R. A. (1922). On the mathematical foundations of theoretical statistics. *Philosophical Transactions of the Royal Society A*. https://digital.library.adelaide.edu.au/handle/2440/15172 — 以現代形式提出最大概似估計，並定義一致性與效率。
- 對 Fisher（1922）的評論：*From evidence to understanding*，PubMed Central。https://pmc.ncbi.nlm.nih.gov/articles/PMC4360088/ — 說明該論文的內容與影響，包括其對概似的處理。

### 綜述與教科書

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 說明在高斯雜訊下 MLE 如何得到最小平方法，在分類中得到交叉熵。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；把最大概似視為擬合大多數模型的基礎。
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — 比較最大概似與貝氏估計，並討論其漸近行為。
