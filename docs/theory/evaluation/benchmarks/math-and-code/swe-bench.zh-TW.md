---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
---

# SWE-bench

SWE-bench 以軟體工程來評估語言模型。它包含 2,294 題，取自 12 個熱門 Python 儲存庫中真實的 GitHub 議題與其拉取請求。模型必須修改程式碼庫，使議題獲得解決（Jimenez et al., 2024）。

## 任務與資料

每個任務提供模型一個程式碼庫與一段議題描述。解決議題通常需要跨越數個函式、類別或檔案的修改，模型可能還需要執行程式並閱讀測試輸出（Jimenez et al., 2024）。

## 協定與指標

候選修補會套用到儲存庫上，並由儲存庫的測試評判。修復前失敗、修復後通過的測試決定是否成功。分數是被解決的任務比例。因為結果取決於代理的框架，例如模型能如何讀取檔案與執行指令，所以分數必須連同框架一起報告。Yang et al.（2024）顯示，專門設計的代理與電腦介面會大幅改變結果。

## 它能說明什麼

這個基準把程式模型的評估，從以單元測試檢驗的函式層級生成（Chen et al., 2021），推向整個儲存庫的任務。它衡量的是系統能否在真實的程式碼庫中工作，而不只是完成單一函式。

## 限制

- **語言涵蓋。** 所有任務都是 Python。
- **污染。** 儲存庫與議題都是公開的，因此可能出現在訓練資料中。
- **測試品質。** 測試可能不完整或有缺陷，因此修補可能通過測試卻是錯的，也可能未通過測試卻是正確的。
- **對框架的依賴。** 分數同時反映模型與工具，除非框架相同，否則模型之間的比較不可靠。

## 相關

- [GSM8K](gsm8k.md) 與 [MATH](math.md) 涵蓋數學推理。
- [數學與程式家族概述](index.md) 比較此領域的基準。

## 參考文獻

### 開創性論文

- Jimenez, C. E. et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv. https://arxiv.org/abs/2310.06770 — 介紹 2,294 個議題、儲存庫測試與解決率指標。
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — 介紹以單元測試進行函式層級程式評估與 pass@k 指標。

### 文章與文件

- Yang, J. et al. (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. arXiv. https://arxiv.org/abs/2405.15793 — 顯示代理所使用的介面如何改變它解決的議題數。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 常與程式代理一起使用的推理提示。

### 補充來源

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 說明為何基準設計必須考慮模型如何被提示與搭配框架。
