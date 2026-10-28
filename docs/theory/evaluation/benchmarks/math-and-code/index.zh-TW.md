---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# 數學與程式基準

這些基準測試模型能否解決有可檢查答案的問題：應用題中的數字、競賽數學中的正式答案，或真實儲存庫中通過的測試套件。

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [GSM8K](gsm8k.md) | 小學應用題 | 最終數字的準確率 |
| [MATH](math.md) | 競賽數學 | 最終答案的準確率 |
| [SWE-bench](swe-bench.md) | 解決 Python 儲存庫中的 GitHub 議題 | 測試判定已解決的議題比例 |

## 常見問題

- **答案檢查。** 不同形式的等價答案可能被判錯，因此正規化器很重要。
- **對框架的依賴。** 對於程式代理，工具與提示也是結果的一部分。
- **污染。** 公開的題目與儲存庫可能出現在訓練資料中。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [準確率](../../metrics/classification/accuracy.md) 是前兩個基準背後的指標。

## 參考文獻

### 開創性論文

- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv. https://arxiv.org/abs/2110.14168 — 介紹 GSM8K 應用題與驗證器方法。
- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — 介紹 MATH 競賽題目與其解答。
- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv. https://arxiv.org/abs/2310.06770 — 介紹以測試判定的儲存庫層級軟體工程任務。

### 文章與文件

- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — 介紹以單元測試進行函式層級程式評估與 pass@k。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示中間推理步驟如何改變這些基準的分數。
