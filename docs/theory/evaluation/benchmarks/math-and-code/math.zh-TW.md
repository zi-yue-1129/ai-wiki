---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# MATH

MATH 是 12,500 題的競賽數學資料集，每題都附有完整的逐步解答。這些解答可用來教模型寫出推導過程，論文也提供了一份輔助的預訓練資料集（Hendrycks et al., 2021）。

## 任務與資料

每題要求一個簡短的最終答案，例如一個數字或一個運算式。題目來自數學競賽，涵蓋數個科目與數個難度等級。逐步解答使監督中間推理成為可能（Hendrycks et al., 2021）。

## 協定與指標

指標是**最終答案的準確率**。最終答案在正規化後與參考答案比對，因此檢查器無法辨識的等價形式會被算作錯誤。協定應說明正規化規則，以及解答是取樣還是貪婪解碼。

## 它能說明什麼

即使是大型 Transformer 也只能達到中等準確率。作者主張，若觀察到的趨勢持續，單靠增加模型規模與訓練預算對於強的數學推理並不實際（Hendrycks et al., 2021）。Lightman et al.（2023）之後以逐步標籤訓練獎勵模型，並在 MATH 的一個子集上評估。

## 限制

- **答案檢查。** 以不同形式表達的等價答案可能被判錯，而形式特殊的正確答案很難自動驗證。
- **污染。** 競賽題目與其解答廣泛公開。
- **與研究數學的距離。** 競賽題有簡短且已知的解答，而開放的研究問題沒有參考答案。

## 相關

- [GSM8K](gsm8k.md) 是較簡單的小學應用題基準。
- [數學與程式家族概述](index.md) 比較此領域的基準。

## 參考文獻

### 開創性論文

- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — 介紹 12,500 題、其解答與輔助預訓練資料。
- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv. https://arxiv.org/abs/2110.14168 — 較簡單的基準，促成了數學推理的驗證器方法。

### 文章與文件

- Lightman, H. et al. (2023). *Let's Verify Step by Step*. arXiv. https://arxiv.org/abs/2305.20050 — 訓練過程監督的獎勵模型，並在 MATH 的一個子集上評估。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 中間推理步驟能提升數學基準的表現。

### 補充來源

- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — 介紹程式生成的 pass@k 指標，是評分生成解答的相關方式。
