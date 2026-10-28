---
translation_reviewed: 2026-10-28
---

# InstructGPT：從人類回饋中進行強化學習（Ouyang 等人，2022）

分三個階段微調 GPT-3：示範資料的監督學習、獎勵模型，以及以該獎勵模型為標的的強化學習。

## 問題

模型變大並不會自動更能遵循使用者的意圖，它仍可能不誠實、有毒性或沒有幫助。

## 核心想法

將 GPT-3 分三個階段微調：以人類示範做監督式學習、以模型輸出的排序訓練獎勵模型，再以該獎勵進行強化學習。

## 方程式或演算法


  1. 收集標註者的示範，並以監督式學習微調。
  2. 收集模型輸出的排序，並據此訓練獎勵模型。
  3. 以強化學習（PPO）針對獎勵模型最佳化策略。

## 結果

人類評分者偏好 13 億參數的 InstructGPT 所產生的輸出，勝過 1,750 億參數的 GPT-3。這些模型更誠實、產生的有毒內容較少，在公開的 NLP 資料集上只有極小的退步。

## 限制

作者指出，InstructGPT 仍會犯簡單的錯誤。獎勵反映的是一小群標註者的偏好，並非普世標準。

## 連結

- 母頁：[大型語言模型](../index.md)
- 同一主題的另一方法：[GPT-3 少樣本學習](../gpt-3-few-shot/index.md)
- 同一主題的另一方法：[運算最佳化訓練](../compute-optimal-training/index.md)

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


## 延伸學習

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — 使用 Hugging Face 函式庫來使用、微調與建構 LLM 的實作課程。
- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — 一小時、非技術性的概述，介紹 LLM 如何訓練、能做什麼、在哪裡失敗。
