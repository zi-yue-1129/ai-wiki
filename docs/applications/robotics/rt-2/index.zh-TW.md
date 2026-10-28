---
translation_reviewed: 2026-10-28
related:
  - theory/models/multimodal
  - theory/models/llm
aliases:
  - RT-2
  - Vision-language-action model
  - 視覺語言動作模型
---

# RT-2：視覺語言動作模型（Brohan 等人，2023）

Brohan 等人想知道：在網路資料上預訓練的視覺語言模型，能否直接控制機器人。他們的答案是 RT-2，它把機器人動作寫成文字 token，因此同一個模型同時處理語言與控制。本頁說明這篇論文；上層主題是[機器人](../index.md)。

## 問題

只用機器人資料訓練的機器人，對日常任務所需的物件、概念與推理所知有限。大型視覺語言模型知識豐富，但輸出的是文字，而不是馬達指令。

## 核心想法

RT-2 把網路預訓練的視覺語言模型，與機器人軌跡以及一般的視覺語言任務（例如視覺問答）一起微調。機器人動作寫成文字 token，因此與語言共用同一種格式。作者把這類模型稱為視覺語言動作（VLA）模型。

## 程序

1. 從大量網路資料上預訓練的視覺語言模型開始。
2. 以機器人軌跡微調，動作寫成文字 token，並與一般視覺語言資料一起訓練。
3. 執行時，依相機影像與指令生成動作 token，再解碼成機器人指令。

## 結果

論文報告約 6,000 次評估試驗，未將其拆分為真實機器人與模擬執行；模擬只用於 Language-Table 基準。與只用機器人資料訓練相比，RT-2 能更好地泛化到新物件，能執行機器人資料中沒有出現的指令，也能處理基本推理。加入思維鏈步驟後，它能為多步驟問題產生計畫；論文只以定性範例呈現這部分。

## 限制

- 論文的評估只在作者自己的機器人設定與任務類型上進行。
- 訓練與執行這種規模的模型需要大量運算資源。
- 把動作寫成文字，使控制與語言模型的輸出格式綁在一起；論文結果未說明這對控制速度有何影響。

## 連結

- 視覺語言模型見[多模態模型](../../../theory/models/multimodal/index.md)。
- 語言模型的部分見[大型語言模型](../../../theory/models/llm/index.md)。
- 同一系列後來的開放模型：[OpenVLA](../openvla/index.md)。

## 參考文獻

### 開創性論文

- Brohan, A. et al. (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv. https://arxiv.org/abs/2307.15818 — 以機器人資料微調網路預訓練的視覺語言模型，並把動作寫成文字 token。
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — RT-2 所依據的 transformer 機器人策略，以大量真實機器人資料訓練。
- Padalkar, A. et al. (2023). Open X-Embodiment: Robotic Learning Datasets and RT-X Models. arXiv. https://arxiv.org/abs/2310.08864 — 來自 22 種機器人的共享資料集，以及在其上訓練的 RT-X 模型。
- Black, K. et al. (2024). π0: A Vision-Language-Action Flow Model for General Robot Control. arXiv. https://arxiv.org/abs/2410.24164 — 較晚的機器人基礎模型，以視覺語言骨幹搭配流匹配。

### 教科書與綜述

- Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv. https://arxiv.org/abs/2108.07258 — 基礎模型的報告，包含機器人作為應用領域。
