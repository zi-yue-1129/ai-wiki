---
translation_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - multimodal
aliases:
  - Multimodal benchmarks
  - 多模態基準
---

# 多模態基準

多模態基準測試模型能否把它所看到的與它所知道的結合起來。此家族中的基準各自強調的重點不同：VQA v2 檢查模型是否真的使用了影像，MMMU 則檢查模型對影像的專家級推理。

## 概述

視覺問答（VQA）要求系統針對一張影像，回答自由形式、開放式的自然語言問題。作者希望問題能針對影像的不同區域，並且需要超越一般影像描述的理解。他們建立了一個約有 25 萬張影像、76 萬個問題與 1,000 萬個答案的資料集（Agrawal et al., 2015）。由於多數答案很短，這項任務仍可以自動評分。

第一版資料集有一個嚴重缺陷：模型常常只靠問題文字就能作答。VQA v2 的解法是讓每個問題配上兩張相似但答案不同的影像，使影像必須發揮作用（Goyal et al., 2016）。論文描述平衡後的資料集，其影像-問題配對約為原版的兩倍。GQA 也關注同樣的問題，它以場景圖產生 2,200 萬個推理問題，並附上可控制答案分布的功能程式，以減少問題偏誤（Hudson & Manning, 2019）。

MMMU 則轉向專家知識。它包含取自大學考試、測驗與教科書的 11.5K 題，涵蓋六大學科、30 個科目與 183 個子領域，並使用 30 種影像類型，例如圖表、示意圖、地圖與化學結構。作者報告，GPT-4V 達到 56%，Gemini Ultra 達到 59%，仍有相當大的進步空間（Yue et al., 2023）。

## 比較的基準

| 基準 | 任務 | 主要指標 |
|---|---|---|
| [VQA v2](vqa-v2.md) | 針對影像的簡短開放式答案 | 與人類答案的一致程度 |
| [MMMU](mmmu.md) | 附影像的大學程度問題 | 準確率，整體與各學科分別計算 |

兩個基準測的能力不同。VQA v2 主要考驗簡單問題中的感知與視覺定位。MMMU 則同時考驗感知、學科知識與多步驟推理，因此低分可能來自其中任何一項。

## 關鍵概念

- **語言先驗**：模型從問題文字中學到的系統性答案傾向，無需看影像即可作答。
- **平衡配對**：兩張外觀相似、但對同一問題給出不同答案的影像，用來檢驗模型是否真的讀取影像。
- **場景圖**：對影像中物件、屬性與關係的結構化描述，GQA 用它來產生問題。

## 運作方式

模型接收一張影像與一個問題，通常以文字提示的形式，並產生答案與參考答案比對。像 MMMU 這樣的選擇題可以與正確選項做完全符合的比對。開放式答案則需要標準化步驟，以及與數個人類答案的一致程度量測。

## 常見問題

- **語言先驗。** 模型可能只靠問題作答，這會使分數膨脹。平衡資料可以對抗這個問題（Goyal et al., 2016）。
- **訊號混雜。** 專家題的分數同時結合了感知、知識與推理，因此很難把錯誤歸因於單一原因（Yue et al., 2023）。
- **飽和。** 近期系統在較舊的資料集上已得高分，因此新基準必須轉向更難的問題。
- **影像多樣性。** 若基準主要使用同一種影像，例如自然照片，就難以說明模型在圖表或示意圖上的表現。

## 相關連結

- [視覺](../vision/index.md) 涵蓋這些任務所延伸的純影像基準。
- [語言](../language/index.md) 涵蓋純文字的對應基準。
- [視覺感知](../../../../brain-mind/visual-perception/index.md) 說明大腦如何把所見與先備知識結合，這正是 VQA 對模型所提出的問題。

## 開放問題

- 多模態基準衡量的是視覺理解，還是主要反映讀取影像的語言模型的語言能力。
- 如何設計讓純文字模型無法得高分的基準，並在報告分數時一併報告此項檢查。

## 相關

- [基準概述](../index.md) 列出所有家族。
- [推理與代理](../reasoning-agents/index.md) 涵蓋某些多模態系統也會接受測試的多步驟任務。

## 參考文獻

### 開創性論文

- Agrawal, A. et al. (2015). *VQA: Visual Question Answering*. arXiv. https://arxiv.org/abs/1505.00468 — 定義開放式視覺問答，並介紹第一個大型 VQA 資料集。
- Goyal, Y. et al. (2016). *Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. arXiv. https://arxiv.org/abs/1612.00837 — 顯示語言先驗會使分數膨脹，並介紹平衡的 VQA v2 資料集。
- Hudson, D. A. & Manning, C. D. (2019). *GQA: A New Dataset for Real-World Visual Reasoning and Compositional Question Answering*. arXiv. https://arxiv.org/abs/1902.09506 — 從場景圖產生 2,200 萬個組合式問題，並控制答案分布的偏誤。

### 文章與文件

- Yue, X. et al. (2023). *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI*. arXiv. https://arxiv.org/abs/2311.16502 — 介紹涵蓋六大學科的 11.5K 題大學程度問題，並報告 GPT-4V 與 Gemini Ultra 的結果。
- Radford, A. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision*. arXiv. https://arxiv.org/abs/2103.00020 — 從自然語言監督中學習視覺模型，是多模態系統廣泛使用的起點。
