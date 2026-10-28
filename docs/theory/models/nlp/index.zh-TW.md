# 自然語言處理

## 發展脈絡

| 時期 | 方法 | 代表 |
|---|---|---|
| 1950 年代–1980 年代 | 規則與文法 | 喬姆斯基式文法、ELIZA、SHRDLU |
| 1990 年代–2000 年代 | 統計式 NLP | n-gram、HMM、CRF、統計機器翻譯 |
| 2013–2017 | 詞向量加神經網路 | word2vec、GloVe、LSTM、帶注意力的 seq2seq |
| 2018–2020 | 預訓練加微調 | ELMo、BERT、GPT-2、T5 |
| 2020 起 | LLM 加提示 | 見[大型語言模型](../llm/index.md) |

## 詞向量

「你會透過一個詞的伴隨詞來認識它」（分布假說，Firth 1957）。word2vec 的向量以能支持類比而聞名：

\[
\vec{\text{king}} - \vec{\text{man}} + \vec{\text{woman}} \approx \vec{\text{queen}}
\]

靜態嵌入不論詞義為何，每個詞只有一個向量；BERT 這類的上下文模型解決了這個問題。

## 經典任務

| 任務 | 說明 | 現今 |
|---|---|---|
| 斷詞、詞性標註、句法分析 | 基礎分析 | 在 LLM 時代較不核心；仍用於管線與語言學研究 |
| 命名實體辨識 | 找出人名、地名、組織 | 微調的編碼器或 LLM 擷取 |
| 情感分析 | 極性、情緒 | 小型的微調模型仍然實用 |
| 文本分類 | 主題、意圖 | 嵌入加分類器，或 LLM |
| 機器翻譯 | 跨語言翻譯 | 神經機器翻譯 → LLM |
| 摘要 | 抽取式／生成式 | 主要由 LLM 完成 |
| 問答 | 閱讀理解、開放領域 | RAG 加 LLM |
| 資訊擷取 | 關係、事件 | 搭配結構化輸出的 LLM |
| 語意相似度與檢索 | 句子嵌入 | Sentence-BERT、嵌入模型、重新排序器 |
| 對話 | 任務導向、開放領域 | LLM |

## 多語言與低資源 NLP

- 全球約 7,000 種語言中，大多數語言的數位文本很少；在這些語言上，效能會急劇下降
- 分詞器可能使某些文字系統每個詞的成本高出數倍
- 因應方法：多語言預訓練、跨語言遷移、社群資料計畫（非洲語言的 Masakhane、Aya），以及針對無文字語言的語音優先方法
- 與中文相關的特殊問題：斷詞、繁體與簡體字的轉換（[OpenCC](https://github.com/BYVoid/OpenCC)）、地區性的詞彙差異

## 語言學與心理語言學

- **喬姆斯基 vs 統計學習**：語言是與生俱來的普遍文法，還是可以從資料中學習？LLM 重新點燃了這場辯論（Piantadosi, 2023 主張 LLM 削弱了喬姆斯基的論證；喬姆斯基等人則不同意）
- **驚訝度理論（surprisal theory）**：人類的閱讀時間與一個詞的負對數機率成正比（Hale, 2001；Levy, 2008）；LLM 的驚訝度是閱讀時間的優良預測指標
- **N400** 這個事件相關電位成分，對語意上出乎意料的詞會有反應，並與語言模型的驚訝度相關
- **探測（probing）**：LLM 是否編碼了句法樹與語意角色？（Hewitt & Manning, 2019，結構探測）
- 見[認知科學](../../../brain-mind/cognitive-science/index.md)

## 學習資源

- Jurafsky & Martin，*Speech and Language Processing*，第三版草稿（可免費線上閱讀）
- Stanford CS224n
- Hugging Face LLM 課程
- [d2l：NLP 章節](https://d2l.ai/chapter_natural-language-processing-pretraining/index.html)

## 參考文獻

### 開創性論文

- Mikolov, T., et al. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — word2vec，學習稠密的詞向量，其幾何結構能捕捉意義與類比。
- Sutskever, I., Vinyals, O. & Le, Q. V. (2014). *Sequence to Sequence Learning with Neural Networks*. NeurIPS. https://arxiv.org/abs/1409.3215 — 以 LSTM 實作的編碼器—解碼器，端到端地翻譯整個句子，是神經機器翻譯的基礎。
- Devlin, J., et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv. https://arxiv.org/abs/1810.04805 — 遮罩語言模型預訓練，成為微調 NLP 系統的標準起點。

### 綜述與教科書

- Jurafsky, D. & Martin, J. H. *Speech and Language Processing*，第三版（草稿）。https://web.stanford.edu/~jurafsky/slp3/ — 標準的 NLP 教科書，從文本處理一直講到大型語言模型；作者提供免費的線上草稿。

### 講座與影片

- Yang, D. & Choi, Y. *CS224N: Natural Language Processing with Deep Learning*. Stanford University. https://web.stanford.edu/class/cs224n/ — 史丹佛的神經網路 NLP 課程，從詞向量講到大型語言模型，附有 PyTorch 作業。

### 文章與文件

- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). *Distributed Representations of Words and Phrases and their Compositionality*. NeurIPS. arXiv:1310.4546. https://arxiv.org/abs/1310.4546 — 提出 skip-gram 搭配負採樣的訓練方法，能有效學習詞嵌入。
