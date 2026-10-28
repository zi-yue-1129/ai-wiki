---
translation_reviewed: 2026-10-28
---

# 分詞（Tokenisation）

分詞是把原始文字切成離散單位（稱為詞元，即 token）的步驟，語言模型就是讀取並預測這些詞元。單位的選擇決定了多少文字能放進上下文視窗、各語言受到的服務是否公平，以及某些任務（例如數字母或做長串加法）對模型來說是否容易。

## 概述

神經語言模型並不直接讀取字元或單字。它讀取的是從固定詞彙表中取出的整數 id 序列，每個 id 再查表得到一個學習得來的向量。分詞定義了這個詞彙表，以及把任意字串轉成 id、再轉回來的規則。兩者都在預訓練開始前就已決定，因此模型之後的每個階段都繼承了分詞器的選擇。

兩種簡單的選擇可以說明其中的取捨。以單字為單位的詞彙表讓每個單字都是一個單位，但需要非常大的詞彙表，而且訓練時沒見過的字都會變成未知符號。以字元或位元組為單位的做法詞彙表很小，也沒有未知符號，但會產生很長的序列，耗費更多運算，並把模型的注意力分散到多得多的位置上。子詞分詞是大型語言模型中的主流做法，它介於兩者之間：常見的字成為單一詞元，罕見的字則被切成模型見過的較小片段。[^1]

## 關鍵概念

- **詞元（Token）**：詞彙表中的一個條目。詞元可以是一個完整的字、字的片段、標點符號或單一位元組。詞元與字並不相同，一個字可能需要好幾個詞元。
- **詞彙表（Vocabulary）**：詞元及其 id 組成的有限清單。詞彙表通常有數萬到數十萬個條目，大小是設計上的選擇。
- **預分詞（Pre-tokenisation）**：在學習得來的切分之前，先做的一次粗略切分，通常以空白與標點為界。有些系統會跳過這一步。
- **切分（Segmentation）**：給定詞彙表後，把字串切成詞元的規則。兩個切分器可以共用同一個詞彙表，卻把同一段文字切得不一樣。
- **位元組後備（Byte fallback）**：把詞彙表中沒有的字元，以其 UTF-8 原始位元組來編碼的規則，因此任何輸入都不會是未知的。
- **特殊詞元（Special tokens）**：保留給文字結束、填充以及對話輪次邊界等標記使用的 id。

## 運作方式

```mermaid
flowchart LR
  A[原始文字] --> B[正規化<br/>Unicode 形式、空白]
  B --> C[預分詞<br/>粗略的字級切分]
  C --> D[子詞切分<br/>學習得來的詞彙表]
  D --> E[詞元 id]
  E --> F[嵌入查表<br/>再交給 Transformer]
```

訓練分詞器，就是在語料中統計數據，並決定哪些片段有資格進入詞彙表。影響較大的幾種做法，其決定方式各不相同。[位元組對編碼（BPE）](bpe/index.md)從單一符號出發，反覆合併最常相鄰的一對。[SentencePiece](sentencepiece/index.md)的 unigram 模型則從大量候選片段開始，移除那些對語料似然度影響最小的片段。WordPiece 常見於許多 BERT 類編碼器，並在 GNMT 系統中被用於機器翻譯，它與 BPE 相似，但評分合併候選時看的是合併後能提高多少訓練資料的似然度，而非單純的頻率。[^2]

編碼新文字時，就是套用學習到的規則。BPE 分詞器會依學習順序重播合併規則；unigram 分詞器則用動態規劃找出機率最高的切分。解碼時把 id 對回片段再接起來。好的分詞器是無損的：解碼 id 會還原原始字串，包括空白。許多做法會用特殊符號標記字首的空白，以便還原原本的間隔。

預分詞會改變學習得來的切分器所看到的東西。若先依空白切開，就無法跨越字的邊界合併，這樣做效率高，但不適合不以空白分隔字詞的語言。直接處理原始字元串的做法（如 SentencePiece）則把空白當成一般符號，不需要特定語言的規則。

第三類做法則完全捨棄學習得來的詞彙表。[ByT5](byt5/index.md) 直接讀取文字的 UTF-8 位元組，因此它的詞彙表就是位元組值的集合。代價是序列變長：一個中文字在 UTF-8 中佔三個位元組，一個英文字母只佔一個，因此同一段文字用位元組計算，長度可能是學習得來的詞彙表所產生詞元數的好幾倍。

## 主要方法

| 方法 | 基本單位 | 詞彙表如何選出 | 頁面 |
|---|---|---|---|
| 位元組對編碼（BPE） | 符號，從字元或位元組開始 | 反覆合併最常相鄰的一對 | [BPE](bpe/index.md) |
| SentencePiece（unigram 模型） | 從原始文字切出的子詞，包含空白 | 移除對語料似然度影響最小的候選片段 | [SentencePiece](sentencepiece/index.md) |
| ByT5（無分詞） | 原始 UTF-8 位元組 | 沒有學習得來的詞彙表；位元組值即是詞彙表 | [ByT5](byt5/index.md) |

每種方法都有自己的頁面，內容包括演算法、報告的結果與限制。

## 相關連結

- 上層主題：[大型語言模型](../index.md)。分詞是該頁所述模型生命週期的第一個階段。
- [自然語言處理](../../nlp/index.md)把分詞當成獨立的分析步驟，通常使用規則與特定語言的工具。在 LLM 時代，分詞通常從資料中學習，並與模型綁在一起。
- [Transformer](../../transformer/index.md) 讀取的是詞元序列，因此詞彙表的大小決定了嵌入層與輸出層的規模。
- [多模態模型](../../multimodal/index.md)把同樣的概念應用於影像、語音與影片，這些資料在共用模型讀取之前，會先轉換成各自的單位。
- 大腦與心智的角度放在「開放問題」中討論：人類的讀者與聽者，並不明顯地把語言切成分詞器所學到的那種單位。參見[大腦中的語言](../../../../brain-mind/language-in-brain/index.md)。

## 應用

- **每一個已部署的 LLM** 都依賴分詞器。服務供應商以詞元計價並設定上下文上限，因此分詞器的選擇同時影響成本，以及模型一次請求能容納的文字量。
- **開源工具。** Hugging Face tokenizers 函式庫與 SentencePiece 等工具，用來在研究與正式環境中訓練並執行分詞器；參見[框架](../../../../engineering/frameworks/index.md)。
- **多語言系統。** 詞彙表涵蓋哪些書寫系統，決定了模型處理各文字的效率。團隊會以平衡的語料建立詞彙表、加入特定語言的片段，或改用位元組級模型。各語言之間的成本差距，Petrov et al. (2023) 有記錄。[^3]

## 開放問題

- **語言公平性。** 以不平衡語料訓練的分詞器，可能讓同一段內容在某些語言中的成本遠高於英文。詞彙表應以成本平衡、依語言分別建立，還是改用位元組級模型，目前仍未有定論。
- **算術與計數。** 模型常常難以數字母或做長串數字的加法。分詞是可能的原因之一，因為數字與字母可能被切成任意片段。Singh and Strouse (2024) 顯示數字的分組方式很重要，但模型容量與訓練也有影響。
- **詞彙表大小。** 詞彙表越大，序列越短，但嵌入層與輸出層也越大，而且罕見詞元的訓練資料很少。目前還沒有一套被普遍接受的選擇大小原則。
- **無分詞模型。** 位元組級模型避開了詞彙表的問題，但會拉長序列。像 Byte Latent Transformer（Pagnoni et al., 2024）那樣對位元組做動態分塊，是一種恢復效率的嘗試；它能否在規模上追上以分詞器為基礎的模型，還需要更廣泛的測試。
- **與人類的比較。** 人類的語言處理是否使用更接近詞素、字或音節的單位，仍有爭議，而子詞詞元是另一種單位。這個問題關係到我們如何解讀模型從文字中學到了什麼。

## 參考文獻

### 開創性論文

- Sennrich, R., Haddow, B. & Birch, A. (2016). *Neural Machine Translation of Rare Words with Subword Units*. ACL. https://arxiv.org/abs/1508.07909 — 為神經機器翻譯引入位元組對編碼，使罕見字與未見過的字能由已知的子詞單位組成。
- Kudo, T. & Richardson, J. (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing*. EMNLP (System Demonstrations). https://arxiv.org/abs/1808.06226 — 介紹 SentencePiece 函式庫，它直接在原始文字上訓練子詞模型，不需要特定語言的預分詞。
- Kudo, T. (2018). *Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates*. ACL. https://arxiv.org/abs/1804.10959 — 提出在訓練時，從 unigram 語言模型取樣多種切分結果。
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation*. arXiv. https://arxiv.org/abs/1609.08144 — 描述 GNMT 系統及其所用的 wordpiece 切分，這是一種類似 BPE、用於實際翻譯服務的子詞方法。
- Xue, L. et al. (2022). *ByT5: Towards a token-free future with pre-trained byte-to-byte models*. TACL. https://arxiv.org/abs/2105.13626 — 一種以位元組為單位的預訓練 Transformer，完全移除分詞器，並與子詞模型進行比較。

### 綜述與教科書

- Mielke, S. J. et al. (2021). *Between words and characters: A Brief History of Open-Vocabulary Modeling and Tokenization in NLP*. arXiv. https://arxiv.org/abs/2112.10508 — 回顧 NLP 如何從字走向字元與子詞，並整理每種單位的取捨。

### 文章與文件

- Petrov, A. et al. (2023). *Language Model Tokenizers Introduce Unfairness Between Languages*. arXiv. https://arxiv.org/abs/2305.15425 — 顯示分詞器可能讓同樣的內容在某些語言中所需的詞元數遠多於英文。
- Singh, A. K. & Strouse, D. J. (2024). *Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs*. arXiv. https://arxiv.org/abs/2402.14903 — 探討分詞器中數字的分組方式如何影響前沿語言模型的算術準確度。
- Nogueira, R., Jiang, Z. & Lin, J. (2021). *Investigating the Limitations of Transformers with Simple Arithmetic Tasks*. arXiv. https://arxiv.org/abs/2102.13019 — 顯示以簡單算術訓練的 Transformer 難以推廣到與訓練時不同的數字上，是關於數字表示的早期警示。
- Rust, P. et al. (2021). *How Good is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models*. ACL. https://arxiv.org/abs/2012.15613 — 發現多語言模型在單一語言上的表現，取決於共用的分詞器與該語言的契合程度。
- Schmidt, C. W. et al. (2024). *Tokenization Is More Than Compression*. arXiv. https://arxiv.org/abs/2402.18376 — 主張單靠壓縮率無法預測分詞器在下游語言建模中的表現，並以其他標準比較各種分詞器。
- Pagnoni, A. et al. (2024). *Byte Latent Transformer: Patches Scale Better Than Tokens*. arXiv. https://arxiv.org/abs/2412.09871 — 提出一種位元組級模型，把位元組分成大小動態變化的區塊，並與以分詞器為基礎的模型比較其擴展特性。
- Wang, C., Cho, K. & Gu, J. (2019). *Neural Machine Translation with Byte-Level Subwords*. arXiv. https://arxiv.org/abs/1909.03341 — 把位元組級 BPE 應用於翻譯，使任何文字都能以 256 個位元組值組成的基礎詞彙表來編碼。

[^1]: 開放詞彙建模的歷史，從字到字元再到子詞，已由 Mielke et al. (2021) 作過回顧；參見參考文獻。
[^2]: WordPiece 在 GNMT 論文（Wu et al., 2016）中有描述。以似然度為基礎的評分規則，是引用前應對照該論文再次確認的細節。
[^3]: 各語言之間不平等的詞元成本，已由 Petrov et al. (2023) 測量；參見參考文獻。
