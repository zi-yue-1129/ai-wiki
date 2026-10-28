---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - overview
---

# 基準測試

基準測試是一組固定的任務、資料與指標，由社群約定用於比較。本區為每個具名基準各撰寫一頁，並依任務家族分組，讓每個基準回答的問題清楚，其分數也能與協定一起解讀。

## 家族

| 家族 | 基準 | 任務 |
|---|---|---|
| [視覺](vision/index.md) | [ImageNet](vision/imagenet.md)、[COCO](vision/coco.md) | 分類、偵測與實例分割 |
| [語言](language/index.md) | [GLUE](language/glue.md)、[SuperGLUE](language/superglue.md)、[MMLU](language/mmlu.md)、[GPQA](language/gpqa.md)、[人類的最後考試](language/hle.md) | 理解、知識與專家推理 |
| [數學與程式](math-and-code/index.md) | [GSM8K](math-and-code/gsm8k.md)、[MATH](math-and-code/math.md)、[SWE-bench](math-and-code/swe-bench.md) | 數學與軟體推理 |
| [多模態](multimodal/index.md) | [VQA v2](multimodal/vqa-v2.md)、[MMMU](multimodal/mmmu.md) | 結合影像、知識與推理 |
| [推理與代理](reasoning-agents/index.md) | [ARC-AGI](reasoning-agents/arc-agi.md)、[GAIA](reasoning-agents/gaia.md)、[WebArena](reasoning-agents/webarena.md) | 規則獲得、真實世界問題與網頁任務 |
| [少樣本](few-shot/index.md) | [miniImageNet](few-shot/mini-imagenet.md) | 從少數有標籤的範例辨識新類別 |

## 如何解讀分數

基準分數只有在附上三項資訊時才能解讀：指標、協定與測試集的歷史。指標見[指標](../metrics/index.md)。協定，包括切分、污染與不確定性的報告，見[評估協定](../protocols/index.md)。對於以網路文字訓練的模型，測試集相對於訓練資料的時間也很重要。

## 基準能說明什麼、不能說明什麼

基準在固定條件下提供可比較的數字。分數高只表示系統能通過那個測試，不代表它在每種情境都有用（Raji et al., 2021）。整體評估主張報告多種情境與指標，讓取捨可見（Liang et al., 2022）。分數也會飽和，而測試集可能偏離它原本要取樣的母體（Recht et al., 2019）。

## 開放問題

基準很快就會飽和，而同一個測試常同時用來挑選模型與報告結果。開放式與多步驟的任務，需要經典家族沒有提供的評估方法。

## 相關

- [評估概述](../index.md) 把基準放在指標與協定之中。
- [評估與基準](../../../engineering/evaluation/index.md) 提供語言模型的實務指引。
- [資料集](../../../reference/datasets/index.md) 列出具名資料集，供查詢。

## 參考文獻

### 開創性論文

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及根據基準表現做出廣泛主張的限制。
- Liang, P. & Bommasani, R. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨多種情境與指標評估語言模型，揭露取捨。
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — 主張固定任務上的技能是衡量智力的弱指標。

### 文章與文件

- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — 廣泛使用的基準，其飽和顯示分數的意義可以多快改變。
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 描述大型基準集合及其任務的選擇方式。
