---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - multimodal
---

# MMMU

MMMU（Massive Multi-discipline Multimodal Understanding and Reasoning）在大學程度的題目上評估多模態模型，這些題目把影像與文字結合。它包含 11.5K 題，取自大學考試、小考與教科書，涵蓋六大領域、30 個科目與 183 個子領域（Yue et al., 2023）。

## 任務與資料

每題包含一或多張影像，例如圖表、示意圖、地圖、表格、樂譜或化學結構，並提出一個同時需要視覺感知與學科知識的問題。論文描述了 30 種異質的影像類型，這也是它與早期影像描述與問答資料集的不同之處（Yue et al., 2023）。

## 協定與指標

指標是題目的**準確率**，整體與各領域分別報告。分數同時混合了兩種能力：讀懂影像與掌握學科知識，因此低分可能來自任一方面。提示詞與答案擷取也是協定的一部分，必須報告。

## 它能說明什麼

這個基準的設計目標，是同時測試進階的感知與審慎的推理，而不只是辨認（Yue et al., 2023）。由於內容是大學程度，分數反映的是系統把所見與領域知識結合的能力。

## 限制

- **訊號混合。** 只看分數，無法把錯誤歸因於感知或知識。
- **答案格式。** 選擇題與開放題的計分方式不同，單一數字會掩蓋兩者的組成。
- **語言先驗。** 模型有時不看影像，只靠文字就能作答，這會使分數膨脹。

## 相關

- [VQA v2](vqa-v2.md) 是較早的視覺問答基準，設計目的是抵消語言先驗。
- [MMLU](../language/mmlu.md) 是純文字的知識基準，MMMU 與它相呼應。
- [多模態家族概述](index.md) 比較此領域的基準。

## 參考文獻

### 開創性論文

- Yue, X. et al. (2023). *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI*. arXiv. https://arxiv.org/abs/2311.16502 — 介紹 11.5K 題的大學程度多模態題目與其學科分類。
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — MMMU 所仿效的純文字多科目基準。

### 文章與文件

- Goyal, Y. et al. (2016). *Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. arXiv. https://arxiv.org/abs/1612.00837 — 顯示語言先驗會使視覺問答分數膨脹。
- Antol, S. et al. (2015). *VQA: Visual Question Answering*. arXiv. https://arxiv.org/abs/1505.00468 — 定義開放式視覺問答及其自動評估。

### 補充來源

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 描述包含多模態任務的廣泛基準設計。
