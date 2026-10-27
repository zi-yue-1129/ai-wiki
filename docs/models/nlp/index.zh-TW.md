# 自然語言處理

## 發展脈絡

| 時期 | 方法 | 代表 |
|---|---|---|
| 1950–1980s | 規則與語法 | 喬姆斯基語法、ELIZA、SHRDLU |
| 1990–2000s | 統計 NLP | n-gram、HMM、CRF、統計機器翻譯 |
| 2013–2017 | 詞向量＋神經網路 | word2vec、GloVe、LSTM、Seq2Seq＋注意力 |
| 2018–2020 | 預訓練＋微調 | ELMo、BERT、GPT-2、T5 |
| 2020– | 大型語言模型＋提示 | GPT-3 之後的 LLM，見 [LLM](../llm/index.md) |

## 詞向量的直覺

「看一個字的鄰居就知道它的意思」（分布假說，Firth 1957）。word2vec 學出的向量有著名的類比性質：

\[
\vec{\text{國王}} - \vec{\text{男人}} + \vec{\text{女人}} \approx \vec{\text{皇后}}
\]

靜態詞向量的問題：一個詞只有一個向量，無法處理一詞多義。BERT 等上下文模型解決了這點。

## 經典任務

| 任務 | 說明 | 現況 |
|---|---|---|
| 斷詞（中文）、詞性標註 | 基礎處理 | CKIP Tagger、Jieba；LLM 時代重要性下降 |
| 命名實體辨識 NER | 找出人名、地名、組織 | 微調 BERT 或 LLM 抽取 |
| 情感分析 | 正負面、情緒 | 微調小模型仍很實用 |
| 文本分類 | 主題、意圖 | 嵌入＋分類器或 LLM |
| 機器翻譯 | 跨語言 | NMT → LLM |
| 摘要 | 抽取式／生成式 | LLM 為主 |
| 問答 | 閱讀理解、開放域 | RAG＋LLM |
| 資訊抽取 | 關係、事件 | LLM＋結構化輸出 |
| 語意相似與檢索 | 句向量 | Sentence-BERT、嵌入模型、重排序器 |
| 對話系統 | 任務型、閒聊 | LLM |

## 中文與繁體中文 NLP

- 無空格斷詞、簡繁轉換（[OpenCC](https://github.com/BYVoid/OpenCC)）、兩岸用詞差異（軟體／软件、網路／网络）
- 中研院 CKIP：[CKIP Transformers](https://github.com/ckiplab/ckip-transformers)
- 繁中評測：TMMLU+、TMLU 等
- 在地 LLM：TAIDE、Breeze 等（見 [LLM](../llm/index.md)）

## 語言學與心理語言學的連結

- **喬姆斯基 vs 統計學習**：語言能力是先天的普遍語法，還是可從資料學出？LLM 的成功重新點燃這場辯論（Piantadosi 2023 認為 LLM 反駁了喬姆斯基的論點；喬姆斯基等人則持反對意見）
- **驚訝度（surprisal）理論**：人類閱讀時間與字的負對數機率成正比（Hale 2001；Levy 2008）；LLM 提供的驚訝度是很好的閱讀時間預測指標
- **N400 腦波**：對語意意外詞的反應，與語言模型的驚訝度相關
- **探測（probing）研究**：LLM 內部是否表徵句法樹、語意角色（Hewitt & Manning, 2019 的結構探測）
- 詳見 [認知科學](../../brain-mind/cognitive-science/index.md)

## 學習資源

- Jurafsky & Martin《Speech and Language Processing》第三版草稿（免費線上）
- Stanford CS224n
- Hugging Face NLP Course
- [d2l-zh 自然語言處理章節](https://zh.d2l.ai/chapter_natural-language-processing-pretraining/index.html)
