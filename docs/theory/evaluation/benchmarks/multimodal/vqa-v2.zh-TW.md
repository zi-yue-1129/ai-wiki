---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - multimodal
---

# VQA v2

VQA v2 是視覺問答基準的平衡版本。視覺問答針對一張影像提出開放式問題，並期待簡短的答案（Antol et al., 2015）。VQA v2 是在發現模型只靠問題文字就能取得高分之後建立的（Goyal et al., 2016）。

## 任務與資料

給定一張影像與一個問題，例如「公車是什麼顏色？」，系統要回傳答案。在 VQA v2 中，每個問題都與兩張答案不同的影像配對，這去除了「直接回答該問題最常見的答案」這種捷徑（Goyal et al., 2016）。

## 協定與指標

每個問題有十個人類答案。預測答案的準確率為相符的人類答案數除以三，再以一為上限，因此當標註者意見分歧時會給予部分分數（Antol et al., 2015）。比對前會先做正規化，因此必須說明正規化規則。

## 它能說明什麼

平衡資料降低了依賴語言先驗的模型分數，也使影像理解成為取得好表現的必要條件（Goyal et al., 2016）。它是檢驗模型是否真的使用影像的標準測試。

## 限制

- **短答案。** 回答只有一個或幾個詞，因此基準不測試解釋或多步驟推理。
- **標註者一致性。** 人類答案分歧時，分數反映的是共識規則與模型同樣多。
- **飽和。** 近期的多模態系統分數已很高，因此差異需要區間。

## 相關

- [MMMU](mmmu.md) 測試影像上的大學程度推理，而非簡短的事實答案。
- [ImageNet](../vision/imagenet.md) 是通常最先用來評估視覺編碼器的分類基準。
- [多模態家族概述](index.md) 比較此領域的基準。

## 參考文獻

### 開創性論文

- Goyal, Y. et al. (2016). *Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. arXiv. https://arxiv.org/abs/1612.00837 — 介紹平衡資料集，以及語言先驗使分數膨脹的證據。
- Antol, S. et al. (2015). *VQA: Visual Question Answering*. arXiv. https://arxiv.org/abs/1505.00468 — 定義開放式任務、資料集與以共識為基礎的準確率。

### 文章與文件

- Yue, X. et al. (2023). *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI*. arXiv. https://arxiv.org/abs/2311.16502 — 承接 VQA 測試推理能力的較困難多模態基準。
- He, K. et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — 殘差網路，是視覺問答中常見的影像編碼器。

### 補充來源

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露對原始蒐集方式的適配程度。
