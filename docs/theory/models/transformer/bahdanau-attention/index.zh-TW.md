---
translation_reviewed: 2026-10-28
---

# 以學習對齊進行神經機器翻譯（Bahdanau 等人，2015）

解碼器以學得的軟對齊權重搜尋來源句，而不是只依賴一個固定長度的向量。

## 問題

編碼器–解碼器的翻譯會把整個來源句壓縮成一個固定長度的向量，長句中的資訊因此遺失。

## 核心想法

在每個輸出步驟，解碼器以軟對齊搜尋來源句，即對編碼器狀態做加權平均。權重由各來源位置與目前解碼器狀態的匹配程度學得。

## 結果

論文報告，注意力模型在長句上的翻譯品質，比固定向量的基線模型更好。

## 限制

編碼器與解碼器仍是循環式的，因此訓練仍需依序進行。每個輸出詞的對齊成本與來源長度成正比。

## 連結

- 母頁：[Transformer 與注意力機制](../index.md)
- 同一主題的另一方法：[Attention Is All You Need 原始論文](../attention-is-all-you-need/index.md)

## 參考文獻

### 開創性論文

- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力取代遞迴。
- Bahdanau, D., Cho, K. & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR. https://arxiv.org/abs/1409.0473 — 在序列到序列的翻譯中加入可學習的注意力，此想法後來被 Transformer 推廣。
- Elhage, N., et al. (2021). *A Mathematical Framework for Transformer Circuits*. Anthropic. https://transformer-circuits.pub/2021/framework/index.html — 把 Transformer 視為殘差流的讀寫之間的一組線性路徑，是機械式可解釋性研究的基礎。

### 綜述與教科書

- Tay, Y., et al. (2020). *Efficient Transformers: A Survey*. arXiv. https://arxiv.org/abs/2009.06732 — 綜述許多降低注意力二次方成本的嘗試，並提供方法分類。

### 講座與影片

- Luong, M.-T., Pham, H. & Manning, C. D. (2015). *Effective Approaches to Attention-based Neural Machine Translation*. EMNLP. arXiv:1508.04025. https://arxiv.org/abs/1508.04025 — 比較神經機器翻譯中的全域與局部注意力機制，並比較多種計分函數。

### 文章與文件

- Harvard NLP. *The Annotated Transformer*. https://nlp.seas.harvard.edu/annotated-transformer/ — 逐篇對照原文的 PyTorch 實作，並附帶註解。

## 延伸學習

- Karpathy, A. (2023). *Let's build GPT: from scratch, in code, spelled out*. YouTube. https://www.youtube.com/watch?v=kCc8FmEb1nY — 從空白檔案現場撰寫一個小型 GPT，寫的同時解說 Transformer 的每個部分。
