---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
aliases:
  - Language benchmarks
  - 語言基準
---

# 語言基準

語言基準涵蓋三種不同的能力：句子層級的理解（GLUE 與 SuperGLUE）、以選擇題形式考驗的廣泛知識（MMLU），以及難以靠搜尋回答的專家級問題（GPQA 與 Humanity's Last Exam）。不同團隊的分數不能直接互換，因為它們測的技能與答題格式都不同。

## 概述

第一代語言基準詢問模型是否理解句子：兩個句子是否互相蘊含、代名詞是否指向某個名詞，以及類似的任務。GLUE 把多個這類任務合併成一個分數，並加入用於語言學分析的診斷測試集。作者發現，多任務與遷移的基線並未立即超越為每項任務分別訓練模型的做法（Wang et al., 2018）。

GLUE 的表現很快就提升，因此 SuperGLUE 以更難的任務、工具包與公開排行榜推出，因為舊基準已超過非專家人類的水準（Wang et al., 2019）。之後的世代轉向知識與推理。MMLU 涵蓋 57 個科目，從國小數學到法律，設計上要求模型必須具備廣泛的世界知識才能得高分（Hendrycks et al., 2021）。作者發表時，多數模型接近隨機猜測，而最大的 GPT-3 模型平均僅比隨機猜測高出約 20 個百分點。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [GLUE](glue.md) | 句子與句對的理解任務，合併計分 | 各任務分數，合併成一個數字 |
| [SuperGLUE](superglue.md) | 更難的理解任務，附人類基線 | 各任務分數，合併成一個數字 |
| [MMLU](mmlu.md) | 涵蓋 57 個科目的選擇題知識測驗 | 準確率 |
| [GPQA](gpqa.md) | 由專家撰寫的研究所程度選擇題 | 準確率 |
| [Humanity's Last Exam](hle.md) | 2,700 題專家題目，含選擇題與簡答題 | 以自動評分計算的準確率 |

GPQA 的設計目標是讓搜尋難以幫上忙。其 448 道選擇題由專家撰寫，具博士程度的專家達到 65% 準確率，而有網路存取權的熟練非專家只達到 34%。論文中最強的以 GPT-4 為基礎的基線達到 39%（Rein et al., 2023）。Humanity's Last Exam 將此想法延伸到多個科目的 2,700 題，答案明確，但無法在網路上很快找到（Phan et al., 2025）。

## 關鍵概念

- **飽和**：當多數系統都接近基準的上限，該基準便無法區分它們，即稱為飽和。HLE 論文指出，模型在 MMLU 上已超過 90%。
- **人類基線**：以人類的分數來顯示還有多少空間。SuperGLUE 的動機正是 GLUE 的分數已超過非專家人類。
- **選擇題與開放作答**：選擇題可以自動評分，但允許猜測；簡答題則需要評分者。

## 運作方式

典型的評估會把問題與選項，或任務的範例，交給模型提示，接著擷取答案並與標準答案比對。準確率是答對的比例。理解任務會先逐項計分再取平均，因此除非彙整方式另有規定，單一大型任務不會主導結果。

## 常見問題

- **飽和。** 多數基準在發布後幾年內就達到很高分數，之後便無法區分系統。
- **資料污染。** 公開的題目可能出現在預訓練資料中，因此分數可能部分反映記憶，而非推理。
- **提示與答案擷取的敏感性。** 少樣本範例、答案擷取方式與評分器都會改變結果，因此必須連同分數一起報告協定。

## 相關連結

- [語言模型](../../../models/llm/index.md) 是這些基準用來評估的系統。
- [準確率](../../metrics/classification/accuracy.md) 是多數分數背後的指標。
- [大腦中的語言](../../../../brain-mind/language-in-brain/index.md) 說明如何研究人類的語言理解，這與基準準確率是不同的問題。

## 開放問題

- 單一的知識分數究竟衡量的是理解，還是主要反映模型看過多少文字。
- 當前沿系統接近專家基線時，如何讓專家基準維持其用途。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [評估與基準](../../../../engineering/evaluation/index.md) 提供語言模型的實務指引。
- [數學與程式](../math-and-code/index.md) 涵蓋與這些基準有許多共同問題的重推理基準。

## 參考文獻

### 開創性論文

- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — 介紹多任務理解基準、其診斷測試集，以及多任務基線尚未超越各任務專用模型的發現。
- Wang, A. et al. (2019). *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*. arXiv. https://arxiv.org/abs/1905.00537 — 說明 GLUE 超過非專家人類後為何失去空間，並介紹更難的任務。
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. arXiv (2020). https://arxiv.org/abs/2009.03300 — 介紹 57 項任務的知識測驗，並報告發表時多數模型接近隨機猜測。

### 文章與文件

- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — 介紹 448 題專家撰寫的科學題，並報告專家與非專家的準確率。
- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — 介紹 2,700 題專家題目，設計目標是讓前沿模型仍感困難。
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — GPT-3 論文，其提示方式是在大型模型上執行這些基準的常見做法。
