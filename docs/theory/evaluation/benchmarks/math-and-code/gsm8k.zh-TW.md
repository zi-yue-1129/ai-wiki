---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# GSM8K

GSM8K 是 8,500 題的小學程度數學應用題資料集，需要數個步驟的算術推理。提出它的論文也提議訓練用來為候選解答評分的驗證器，作為提升準確率的方法（Cobbe et al., 2021）。

## 任務與資料

每題以自然語言撰寫，只有一個數值答案。題目的語言變化多，每一步的推理都簡單，因此困難來自於正確地組合各步驟（Cobbe et al., 2021）。

## 協定與指標

指標是**最終數值答案的準確率**，中間步驟不直接評分。思維鏈提示（Wei et al., 2022），以及取多條推理路徑多數答案的自洽性（Wang et al., 2022），都提升了此基準的分數。因此結果高度取決於提示與解碼設定，必須一併報告。

## 它能說明什麼

原始論文發現，即使是大型 Transformer 也無法達到高測試準確率，而且驗證器隨資料增加的擴展性比單純微調更好（Cobbe et al., 2021）。它可用來診斷語言模型的多步推理。

## 限制

- **飽和。** 近期模型的分數非常高，若沒有區間，很難解讀它們之間的差異。
- **污染。** 題目是公開的，類似的題目可能出現在訓練資料中。
- **只看最終答案。** 以無效路徑得到的正確最終答案也會被算作正確。

## 相關

- [MATH](math.md) 是較困難的競賽數學基準。
- [SWE-bench](swe-bench.md) 涵蓋軟體工程，以測試作為評判。
- [數學與程式家族概述](index.md) 比較此領域的基準。

## 參考文獻

### 開創性論文

- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv. https://arxiv.org/abs/2110.14168 — 介紹 8,500 題的資料集與驗證器方法。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示中間推理步驟如何提升算術應用題的準確率。

### 文章與文件

- Wang, X. et al. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. arXiv. https://arxiv.org/abs/2203.11171 — 取樣多條推理路徑並採多數答案，在 GSM8K 上有所提升。
- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — 承接 GSM8K 的較困難數學基準。

### 補充來源

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 介紹上下文提示，多數 GSM8K 結果都是以此方式取得。
