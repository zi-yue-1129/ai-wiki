---
translation_reviewed: 2026-10-28
---

# GPT-3：從提示中進行少樣本學習（Brown 等人，2020）

一個 1,750 億參數的自回歸 Transformer，以提示中的零、一或少數範例進行測試。

## 問題

語言模型能否只靠提示中的少量範例學會新任務，而不需要任何梯度更新？

## 核心想法

將自迴歸 Transformer 擴大到 1,750 億參數，並在提示中提供零個、一個或少數幾個範例來測試。模型並未針對該任務微調。

## 方程式或演算法


  1. 在提示中寫入任務描述與幾組輸入–輸出範例。
  2. 接上新的輸入。
  3. 讓模型逐個 token 生成輸出。權重不變。

## 結果

在翻譯、問答與填空任務上表現強勁，也能做 3 位數的算術，摘要將後者列為即時推理任務之一。

## 限制

論文指出，在部分任務上，少樣本表現仍落後於針對該任務微調的模型。

## 連結

- 母頁：[大型語言模型](../index.md)
- 同一主題的另一方法：[運算最佳化訓練](../compute-optimal-training/index.md)
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


### 文章與文件

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — 使用 Hugging Face 函式庫來使用、微調與建構 LLM 的實作課程。
