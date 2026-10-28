---
translation_reviewed: 2026-10-28
tags:
  - transformer
  - attention
  - reparameterisation
  - training stability
aliases:
  - σReparam
  - Spectral reparameterisation
  - σ 重參數化
---

# σReparam

σReparam 以譜範數乘上一個可學習純量，對 Transformer 的每個線性層做重參數化。Zhai 等人（2023）用它來防止注意力熵崩潰，並把這個崩潰連結到注意力 logit 的譜範數。論文報告，在沒有預熱、權重衰減、層正規化或自適應最佳化器的情況下，仍有具競爭力的表現。上層概述是[Transformer 與注意力](index.md)，它所依賴的範數分析見[權重範數動態](../../optimization/weight-norm-dynamics/index.md)頁面。

## 概述

以權重 \(W\) 的線性層被取代為 \(\hat W = \dfrac{\gamma}{\sigma(W)}\,W\)，其中 \(\sigma(W)\) 是 \(W\) 的最大奇異值，\(\gamma\) 是可學習純量。於是 \(\hat W\) 的譜範數由 \(\gamma\) 決定，而不是由 \(W\) 的尺度決定。控制譜範數的參數因此與實際做運算的矩陣分開。

## 問題

Zhai 等人指出，注意力分布的熵有一個下界，該下界隨注意力 logit 的譜範數增長而指數式下降。範數增長時，注意力分布可能崩向單一位置，訓練變得不穩定。論文的補救方法直接控制各層的譜範數。

## 核心想法

重參數化每個線性層，使其譜範數由單一可學習純量決定，而不是讓權重矩陣的尺度自由增長。使用 \(\hat W = (\gamma/\sigma(W))\,W\) 後，每層的譜範數由一個可學習純量控制。查詢、鍵、值、輸出與前饋層都套用同樣的參數化。

## 運作方式

1. 對每個線性層，以幾步冪迭代估計最大奇異值 \(\sigma(W)\)，與譜正規化相同。
2. 計算重參數化後的權重 \(\hat W = (\gamma/\sigma(W))\,W\)，每層有一個可學習的 \(\gamma\)。
3. 在前向傳播中使用 \(\hat W\)，讓最佳化器更新 \(W\) 與 \(\gamma\)。
4. 訓練中監測注意力熵，因為此方法的動機正是來自它。

## 結果

論文報告，σReparam 在沒有預熱、權重衰減、層正規化或自適應最佳化器的情況下，仍有具競爭力的表現。實驗、任務與圖表都在論文中，使用任何數字前應先核對。

## 限制

- 此方法改變每個線性層的參數化，因此不是可以直接套用到既有檢查點的改動。
- 冪迭代估計譜範數每一步都有額外成本，而論文的比較只限於特定架構與任務。
- 限制譜範數能抑制定理所預測的熵崩潰，但並不能證明注意力因此保持可分辨。Noci 等人（2022）分析的秩崩潰是另一種失敗模式。

## 相關主題

- [QK 正規化](qk-norm.md) 是另一種方案，直接正規化查詢與鍵向量，而不是權重。
- [權重範數動態](../../optimization/weight-norm-dynamics/index.md) 解釋訓練中層的範數為何持續改變。
- [Transformer 與注意力](index.md) 描述此方法所保護的注意力區塊。

## 開放問題

- 對於非常大的模型，每層一個可學習純量是否足夠，還是必須逐層調整。
- 此參數化與大規模訓練所用的權重衰減如何互動，因為譜範數不再由權重範數決定。

## 參考文獻

- Zhai, S., Likhomanenko, T., Littwin, E., et al. (2023). *Stabilizing Transformer Training by Preventing Attention Entropy Collapse*. ICML 2023, PMLR 202:40770–40803. https://proceedings.mlr.press/v202/zhai23a.html — 提出 σReparam 與注意力熵的下界。
- Dehghani, M., Djolonga, J., Mustafa, B., et al. (2023). *Scaling Vision Transformers to 22 Billion Parameters*. ICML 2023, PMLR 202:7480–7512. https://proceedings.mlr.press/v202/dehghani23a.html — 針對同一問題的另一種穩定化修改，即查詢鍵正規化。
- Wortsman, M., Liu, P. J., Xiao, L., et al. (2023). *Small-scale proxies for large-scale Transformer training instabilities*. arXiv:2309.14322. https://arxiv.org/abs/2309.14322 — 在小規模上重現注意力 logit 與輸出 logit 的不穩定。
- Noci, L., Anagnostidis, S., Biggio, L., et al. (2022). *Signal Propagation in Transformers: Theoretical Perspectives and the Role of Rank Collapse*. arXiv:2206.03126. https://arxiv.org/abs/2206.03126 — 分析秩崩潰，這是限制範數無法移除的失敗。
- Xiong, R., Yang, Y., He, D., et al. (2020). *On Layer Normalization in the Transformer Architecture*. ICML 2020. https://arxiv.org/abs/2002.04745 — 研究正規化的位置，σReparam 部分地取代了它。
