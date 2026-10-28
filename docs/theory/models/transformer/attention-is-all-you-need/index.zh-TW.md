---
translation_reviewed: 2026-10-28
---

# Attention Is All You Need（Vaswani 等人，2017）

以多頭縮放點積注意力取代遞迴與卷積，使每個位置都能並行地關注所有其他位置。

## 問題

循環式序列模型一次處理一個 token，限制了平行訓練，也讓長距離依賴難以學習。

## 核心想法

完全移除循環與卷積。每個位置透過多頭縮放點積注意力關注所有其他位置，並把位置資訊加到嵌入上。

## 方程式或演算法

編碼器與解碼器各自堆疊多頭注意力與前饋網路的層。解碼器遮蔽未來的位置，因此每個輸出只依賴先前的輸出。

## 結果

在 WMT 2014 英譯德任務上達到 28.4 BLEU，比先前最佳結果（包括集成模型）高出超過 2 BLEU。單一模型在英譯法上達到 41.8 BLEU。訓練花了 3.5 天，使用八個 GPU。

## 限制

注意力的成本隨序列長度的平方增長（見上方的效率一節）。原始模型是用於翻譯的編碼器–解碼器，而非今日多數語言模型使用的純解碼器形式。

## 連結

- 母頁：[Transformer 與注意力機制](../index.md)
- 同一主題的另一方法：[加性注意力（Bahdanau）](../bahdanau-attention/index.md)

## 參考文獻

### 開創性論文

- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力取代遞迴。
- Bahdanau, D., Cho, K. & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR. https://arxiv.org/abs/1409.0473 — 在序列到序列的翻譯中加入可學習的注意力，此想法後來被 Transformer 推廣。
- Elhage, N., et al. (2021). *A Mathematical Framework for Transformer Circuits*. Anthropic. https://transformer-circuits.pub/2021/framework/index.html — 把 Transformer 視為殘差流的讀寫之間的一組線性路徑，是機械式可解釋性研究的基礎。

### 綜述與教科書

- Tay, Y., et al. (2020). *Efficient Transformers: A Survey*. arXiv. https://arxiv.org/abs/2009.06732 — 綜述許多降低注意力二次方成本的嘗試，並提供方法分類。

### 講座與影片

- Radford, A., Wu, J., Child, R., Luan, D., Amodei, D. & Sutskever, I. (2019). *Language Models are Unsupervised Multitask Learners*. OpenAI technical report. https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf — GPT-2 技術報告，描述影片中實作的僅解碼器 Transformer 語言模型。

### 文章與文件

- Rush, A. M. (2018). *The Annotated Transformer*. Proceedings of Workshop for NLP Open Source Software (NLP-OSS). https://doi.org/10.18653/v1/w18-2509 — 逐篇對照原文的 PyTorch 實作，並附帶註解。

## 延伸學習

- Karpathy, A. (2023). *Let's build GPT: from scratch, in code, spelled out*. YouTube. https://www.youtube.com/watch?v=kCc8FmEb1nY — 從空白檔案現場撰寫一個小型 GPT，寫的同時解說 Transformer 的每個部分。
