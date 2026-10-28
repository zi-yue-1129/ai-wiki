---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# HumanEval

HumanEval 是一組 164 道人工撰寫的 Python 程式設計題，每題附有單元測試，用來衡量程式碼模型能否依照 docstring 寫出正確的函式（Chen et al., 2021）。它提出了 pass@k 指標，現在已是報告程式碼生成結果的標準方式。

## 任務與資料

每題給出函式簽章與 docstring，模型需要補完函式本體。題目涵蓋基本演算法、字串處理與簡單數學。每題都附有隱藏的單元測試，只有全部通過，程式才算正確（Chen et al., 2021）。

## 協定與指標

指標是 pass@k：k 個抽樣解答中，至少一個通過所有測試的機率。Chen et al.（2021）給出不偏估計式：每題抽取 n 個樣本（n 至少為 k），並計算正確的數量 c。分數取決於抽樣溫度、樣本數與執行沙箱，因此三者都必須報告。

## 它能說明什麼

它顯示模型能否把精確的規格轉成行為正確的程式。由於測試檢查的是行為而非文字，解答是依其實際表現來判定，而非依外觀。

## 限制

- **題目數少。** 只有 164 題，少數題目就會明顯改變分數，因此需要區間。
- **污染。** 公開題目可能出現在訓練資料中，而論文中的題目也被大量轉載。
- **題目偏簡單。** 許多題目是短函式，因此這個基準對大型程式碼庫的說明有限；後者由 SWE-bench 涵蓋。

## 相關

- [數學與程式概述](index.md) 比較數學與程式基準。
- [SWE-bench](swe-bench.md) 測試儲存庫規模的軟體工程。

## 參考文獻

### 開創性論文

- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — 介紹 HumanEval 與附不偏估計式的 pass@k 指標。

### 文章與文件

- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，揭露其取捨。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。

### 補充來源

- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 主張在固定任務上的技能是衡量智能的弱指標。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。
