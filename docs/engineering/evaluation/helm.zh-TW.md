---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
tags:
  - evaluation
  - benchmarks
  - transparency
aliases:
  - HELM
  - Holistic Evaluation of Language Models
  - 語言模型整體評估
---

# HELM（Liang 等人，2022）

HELM（Holistic Evaluation of Language Models，語言模型整體評估）是一個框架，能同時跨越許多情境與許多指標來評估語言模型。它的提出是為了提高模型能力、限制與風險的透明度，並顯示單一準確率數字所隱藏的指標之間的取捨。Liang 等人（2022）描述了此框架及其第一次大規模評估。

本頁是[基準套件](benchmark-suites.zh-TW.md)的一部分，該頁也涵蓋 MMLU 及其後繼者。

## 概述

多數排行榜每個模型只報告一個數字。一個模型可能準確率很高，卻校準不佳、對某些群體不公平，或運行成本高昂。HELM 的做法是對感興趣的情境與指標進行分類，選擇一組廣泛的指標，並在可能時為每個情境報告所有指標。作者也記錄了缺漏之處，例如被忽略之英語方言的問答，以及可信度的指標。

## 關鍵概念

- **情境：**由任務、資料集與設定界定的使用場景。HELM 把情境組織成模型用途的分類。
- **指標：**對某項期望性質的衡量。框架使用七項：準確率、校準、穩健性、公平性、偏見、毒性與效率。
- **核心情境：**十六個核心情境之一，在可能時所有指標都會在其上報告。
- **取捨視圖：**讓讀者看到同一模型在兩項指標之間關係的呈現方式。

## 運作方式

HELM 分三步進行。作者先對情境與指標進行分類。接著，依涵蓋範圍與可行性選出一個子集，並報告仍存在的缺漏。最後，他們讓每個模型在每個核心情境上運行，並衡量全部七項指標。論文報告，大部分的情境—模型組合（約 87.5% 的時候）都能測得所有指標，因此結果是一張網格，而非單一排名。

## 結果

摘要指出，框架在可能的情況下為 16 個核心情境各衡量七項指標，約佔 87.5% 的時間，這使準確率以外的指標不會被忽略。框架的設計目的，是讓取捨清楚可見，因此主要成果是比較本身，而非單一的贏家。

## 限制

- **選擇的判斷。**情境分類與選出的子集反映作者的判斷，其他選擇會得到不同的網格。
- **成本。**讓每個模型在每個情境與每項指標上運行，成本很高，這限制了套件更新的頻率。
- **指標是代理變數。**公平性、毒性與穩健性是由特定測試衡量的，只捕捉到各自性質的一部分。
- **版本問題。**結果取決於提示、模型與運行的日期，因此很快就會過時。

## 關聯

- 包括 MMLU 在內的套件全貌，見[基準套件](benchmark-suites.zh-TW.md)。
- 模型與應用的評估實務，見[評估與基準](index.zh-TW.md)。
- 指標定義與統計處理，在理論章節的[評估](../../theory/evaluation/index.zh-TW.md)。
- HELM 所衡量的公平與偏見，見[社會](../../society/index.zh-TW.md)。

## 應用

- 比較模型在準確率與校準或公平性之間的取捨。
- 為透明度報告記錄模型的行為。

## 開放問題

- 隨著使用情境的變化，整體性套件應納入哪些情境？
- 當部署需要其中某項指標優先時，各指標應如何加權？

## 參考文獻

### 開創性論文

- Liang, P. 等人（2022）。*Holistic Evaluation of Language Models*。arXiv。https://arxiv.org/abs/2211.09110 — 提出 HELM，包括情境與指標的分類，以及 16 個核心情境上的七項指標網格。
- Hendrycks, D. 等人（2021）。*Measuring Massive Multitask Language Understanding*。ICLR。https://arxiv.org/abs/2009.03300 — 以準確率為基礎的套件，HELM 的準確率指標即與之比較。
- Srivastava, A. 等人（2022）。*Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*。arXiv。https://arxiv.org/abs/2206.04615 — 一套廣泛、由多方共同建立的任務，用來衡量模型規模增長時的能力。

### 調查與教科書

- Wang, Y. 等人（2024）。*MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark*。arXiv。https://arxiv.org/abs/2406.01574 — MMLU 的後繼者，可與 HELM 的衡量方法對照。
