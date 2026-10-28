---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - math-and-code
aliases:
  - Math and code benchmarks
  - 數學與程式基準
---

# 數學與程式基準

這些基準測試模型能否推理出一個可以檢查結果的問題：應用題結尾的數字、競賽數學中的正式答案、通過單元測試的函式，或是能解決真實儲存庫問題的修補程式。由於結果可以自動檢查，這類任務已成為衡量語言模型推理能力的標準方式。

## 概述

此家族的第一個基準 GSM8K 包含 8.5K 道國小應用題。作者發現，即使是當時最大的 Transformer 模型也無法達到高測試準確率，因此他們提出訓練驗證器（verifier），由它對許多候選解答排序並選出最佳者。他們報告，驗證器提升了表現，而且相對於微調基線，隨資料量增加的擴展性更好（Cobbe et al., 2021）。

競賽數學更難。MATH 資料集有 12,500 道題，每題都附有逐步解答。作者報告，即使使用非常大的 Transformer 模型，準確率仍然相對偏低，單靠擴展規模並未解決這個基準（Hendrycks et al., 2021）。

程式基準則從單一函式擴展到整個儲存庫。HumanEval 衡量模型生成的 Python 函式能否通過針對文件字串撰寫的單元測試。Codex 論文報告，其模型解出 28.8% 的題目，GPT-3 為 0%，GPT-J 為 11.4%；若對每題取 100 個樣本進行重複抽樣，解出比例提升到 70.2%（Chen et al., 2021）。SWE-bench 則更進一步：它使用來自 12 個熱門 Python 儲存庫的 2,294 個真實 GitHub issue，模型必須編修程式碼以處理該 issue（Jimenez et al., 2024）。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [GSM8K](gsm8k.md) | 國小應用題 | 最終數字的準確率 |
| [MATH](math.md) | 競賽數學 | 最終答案的準確率 |
| [HumanEval](humaneval.md) | 依文件字串撰寫 Python 函式 | 通過題目的比例，重複抽樣時以 pass@k 報告 |
| [SWE-bench](swe-bench.md) | 解決 Python 儲存庫中的 GitHub issue | 已解決的 issue 比例 |

前兩者檢查最終答案，因此答案的標準化方式決定分數。後兩者檢查行為：程式會在沙箱中以保留的測試執行來評判，issue 則看修補後的儲存庫能否通過測試。

## 關鍵概念

- **驗證器**：為候選解答評分的模型或程序，用來在多個樣本中挑選。
- **重複抽樣**：對同一題抽取多個解答，只要有一個樣本通過即算解出。抽樣數量必須與分數一起報告。
- **鷹架（scaffold）**：模型周圍的工具、提示與迴圈。對程式代理而言，鷹架本身就是結果的一部分。

## 運作方式

對數學基準，模型寫出解答，擷取答案後經標準化再與標準答案比對。對程式基準，生成的程式或修補會在沙箱中以保留的測試執行。要求模型寫出中間步驟的思維鏈提示，改善了 GSM8K 上的結果；論文報告，一個具有 540B 參數、以八個範例提示的模型，超越了搭配驗證器的微調 GPT-3（Wei et al., 2022）。

## 常見問題

- **答案檢查。** 以不同形式寫出的等價答案可能被判為錯誤，因此標準化程序與模型同樣重要。
- **鷹架依賴。** 提示、工具存取與搜尋都會改變結果，因此兩個系統的差異可能主要來自鷹架。
- **資料污染。** 公開的題目、解答與儲存庫可能出現在訓練資料中。

## 相關連結

- [思維鏈](../../../models/reasoning/chain-of-thought.md) 是這些任務最常使用的提示方法，[推理模型](../../../models/reasoning/index.md) 則涵蓋更廣的家族。
- [推理與代理基準](../reasoning-agents/index.md) 將同一個問題延伸到需要工具的多步驟任務。
- [準確率](../../metrics/classification/accuracy.md) 是前兩個基準背後的指標。

## 開放問題

- 競賽數學的高分究竟反映一般的數學推理，還是對熟悉技巧的檢索。
- 當每個程式代理各自帶有不同的鷹架、搜尋預算與測試環境時，如何公平比較。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [語言](../language/index.md) 涵蓋理解與知識類的基準。

## 參考文獻

### 開創性論文

- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems*. arXiv. https://arxiv.org/abs/2110.14168 — 介紹 8.5K 題的 GSM8K 應用題，以及為抽樣解答排序的驗證器。
- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — 介紹 12,500 道附逐步解答的競賽題，並報告在大規模下準確率仍然偏低。
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — 介紹 HumanEval、函式層級的測試，以及重複抽樣的效果。
- Jimenez, C. E. et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv (2023). https://arxiv.org/abs/2310.06770 — 介紹 2,294 個來自真實 GitHub issue 的問題，橫跨 12 個熱門 Python 儲存庫。

### 文章與文件

- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示寫出中間推理步驟能改善 GSM8K 與其他推理任務的結果。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — 描述許多這些基準在大型模型上執行時所用的提示設定。
