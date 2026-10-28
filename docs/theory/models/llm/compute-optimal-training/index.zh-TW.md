---
translation_reviewed: 2026-10-28
---

# 運算最佳化訓練（Hoffmann 等人，2022）

在固定的運算預算下，透過跨多次訓練的擬合，找出最佳的模型大小與訓練 token 數。

## 問題

在固定的運算預算下，模型大小與訓練 token 數量應如何平衡？

## 核心想法

訓練超過 400 個語言模型，參數從 7,000 萬到 160 億以上，資料量從 50 億到 5,000 億 token 不等，再找出每個運算預算下的最佳大小。模型大小與資料量應一起成長。

## 規則

模型大小每加倍，訓練 token 數也加倍。

## 結果

Chinchilla 有 700 億參數與四倍的資料，使用的運算量與 Gopher（2,800 億參數）相同，在廣泛的下游任務上勝過 Gopher、GPT-3 等模型。它在 MMLU 上達到 67.5% 的平均準確率。

## 限制

這個規則是根據作者所訓練的範圍擬合出來的。許多後來的模型刻意訓練到遠超過此比例，因為較小的模型提供服務的成本較低。

## 連結

- 母頁：[大型語言模型](../index.md)
- 同一主題的另一方法：[GPT-3 少樣本學習](../gpt-3-few-shot/index.md)
- 同一主題的另一方法：[InstructGPT 與 RLHF](../instructgpt-rlhf/index.md)

## 參考文獻

### 開創性論文

- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — GPT-3 論文，顯示非常大的模型能從提示中給出的少量範例學會新任務。
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — 顯示隨著模型大小、資料與運算量增加，損失如何可預測地下降。
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — Chinchilla 研究，主張在固定運算預算下，模型大小與訓練 token 數應該同步成長。
- Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT，結合監督式微調與來自人類偏好的強化學習。
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示要求模型寫出中間推理步驟，可改善多步驟問題的解題能力。

### 綜述與教科書

- Zhao, W. X., et al. (2023). *A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — 對 LLM 的預訓練、適應與評估進行廣泛綜述，並附有模型時間線。

### 講座與影片

- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — 一小時、非技術性的概述，介紹 LLM 如何訓練、能做什麼、在哪裡失敗。

### 文章與文件

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — 使用 Hugging Face 函式庫來使用、微調與建構 LLM 的實作課程。
