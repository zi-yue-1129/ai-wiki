---
translation_reviewed: 2026-10-28
---

# 分詞（Tokenisation）

語言模型讀取的是稱為詞元（token）的離散單位序列。分詞器把原始文字映射為詞元序列，也能再映射回文字。詞元的選擇決定了詞彙表的大小、一段文字會變成多長，以及模型究竟能表示哪些字串。本頁是[大語言模型](../index.md)的一部分。

## 概述

神經網路需要固定的詞彙表。整個單字作為單位時，詞彙表會太大，而罕見或未見過的單字就沒有對應的條目。以單一字元為單位可以避免這個問題，但序列會變長，成本也較高。Sennrich、Haddow 與 Birch（2016）把子詞單位引入神經機器翻譯，使常見的字保持完整，罕見的字則拆成模型已見過的片段。多數現代語言模型都使用這類學習得到的子詞分詞器。

## 關鍵概念

- **詞彙表**：模型可以輸出的固定詞元集合，通常由數萬到數十萬個條目組成。
- **子詞單位**：字的一部分，例如 `token` 與 `isation`，比單字短，通常比字元長。
- **切分**：把字串切成詞元的規則。學習得到的分詞器也會決定未見過文字的切分方式。
- **位元組級分詞器**：以 256 個位元組值為基礎字母表的分詞器，因此任何腳本的任何字串都能編碼，不會出現未知符號。
- **詞元繁衍率（fertility）**：每個字平均所需的詞元數，用來衡量分詞器表示某種語言的效率。

## 問題

應如何把文字切成單位，使詞彙表大小可控、罕見的字仍可表示，且序列短到模型能夠處理？

## 運作方式

多數分詞器會在語料上訓練一次，之後就固定不變。訓練決定詞彙表，以及把文字映射到詞彙表的規則。對新字串進行編碼時，會依固定順序套用這些規則；解碼則把詞元接回文字。

常用的三類學習式分詞器如下：

- **位元組對編碼（BPE）** 從字元開始，反覆合併最常相鄰的一對符號。詳見[位元組對編碼](byte-pair-encoding.md)。
- **WordPiece** 與 BPE 相近，但每次合併的選擇是為了讓訓練資料的似然最大，而不是單純依據配對次數。Schuster 與 Nakajima（2012）為日語與韓語語音搜尋引入此方法，BERT（Devlin 等人，2019）也採用它。
- **unigram 語言模型** 從一個很大的候選詞彙表開始，移除對語料似然貢獻最少的片段。SentencePiece 實作了這個方法，也實作了 BPE，並直接處理原始文字，不需要先切成單字。詳見 [SentencePiece 與 unigram 模型](sentencepiece.md)。

## 主要方法

- [位元組對編碼](byte-pair-encoding.md)：反覆合併最頻繁的符號對，是許多 GPT 類分詞器的基礎。
- [SentencePiece 與 unigram 模型](sentencepiece.md)：在原始文字上與語言無關地訓練，並以取樣的切分做正則化。

## 變體

- **詞級**：每個字一個詞元。簡單，但詞彙表無法涵蓋罕見的字。
- **字元級**：每個字元一個詞元。能涵蓋任何字串，但序列很長。
- **位元組級子詞**：以位元組為基礎的 BPE，由 Wang 等人（2019）研究。任何腳本的字串都可以表示。
- **無詞元模型**：直接讀取位元組或字元的模型。ByT5（Xue 等人，2022）以輕量編碼器處理位元組，CANINE（Clark 等人，2022）則直接處理字元並在 Transformer 層前做降取樣。

## 結果與限制

- 子詞單位讓神經翻譯模型能處理罕見與未見過的字，不需要未知字元符號（Sennrich 等人，2016）。
- 位元組級模型避免了未知符號，對拼寫雜訊也較穩健，但作者在 ByT5 中指出，較長的位元組序列會讓訓練與推論的成本更高（Xue 等人，2022）。
- 分詞器的選擇會改變同一段文字在不同語言中所需的詞元數。分詞器訓練時未涵蓋的語言，常需要每個字好幾個詞元，因此使用該語言的成本較高。
- 分詞可能讓某些任務比表面上更困難。數字字串上的字母計數或算術，都取決於文字如何被切分。

## 應用

- **多語言語言模型**：選擇能涵蓋多種書寫系統的詞彙表，同時不在任何一種語言上浪費詞元。
- **成本估算**：計算詞元數，以決定 API 請求的價格，或判斷內容是否放得進上下文視窗。
- **程式碼模型**：在原始碼上訓練的分詞器，使識別字與縮排的表示更有效率。

## 開放問題

- 能否在不損失太多計算效率的前提下，改以位元組或字元學習，而不使用分詞器？
- 詞彙表應在訓練前固定，還是能與模型共同學習切分方式？
- 對於不以空白分隔字詞的書寫系統，應如何設計分詞器？

## 與其他頁面的連結

- 上層主題：[大語言模型](../index.md)
- 相關：[自然語言處理](../../nlp/index.md)
- 本主題的另一方法：[運算最佳化訓練](../compute-optimal-training/index.md)，它計算的是訓練詞元數，而非模型參數。

## 參考文獻

### 奠基性論文

- Sennrich, R., Haddow, B. & Birch, A. (2016). Neural Machine Translation of Rare Words with Subword Units. In *Proceedings of the 54th Annual Meeting of the ACL (Volume 1: Long Papers)*, 1715–1725. https://doi.org/10.18653/v1/P16-1162 — 把位元組對編碼改寫為神經機器翻譯的子詞詞彙表建構方法。
- Schuster, M. & Nakajima, K. (2012). Japanese and Korean voice search. In *ICASSP 2012*, 5149–5152. https://doi.org/10.1109/ICASSP.2012.6289079 — 提出 WordPiece，一種資料驅動的子詞切分方法。
- Kudo, T. & Richardson, J. (2018). SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing. arXiv:1808.06226. https://arxiv.org/abs/1808.06226 — 直接在原始文字上訓練子詞模型，並能可逆地還原文字。
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In *NAACL-HLT 2019*. arXiv:1810.04805. https://arxiv.org/abs/1810.04805 — 在廣泛使用的預訓練編碼器中採用 WordPiece 分詞器。

### 綜述與教科書

- Xue, L. et al. (2022). ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models. *Transactions of the ACL* 10, 291–306. https://doi.org/10.1162/tacl_a_00461 — 把位元組級模型當作無詞元的替代方案進行研究，並討論其成本。
- Clark, J. H. et al. (2022). CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation. *Transactions of the ACL* 10, 73–91. https://doi.org/10.1162/tacl_a_00448 — 直接讀取字元的編碼器，在 Transformer 層前先做降取樣。
- Wang, C., Cho, K. & Gu, J. (2020). Neural Machine Translation with Byte-Level Subwords. In *AAAI 2020*. arXiv:1909.03341. https://arxiv.org/abs/1909.03341 — 為翻譯而設計的位元組級子詞切分，沒有未知符號的問題。

## 延伸學習

- Hugging Face, *Summary of the tokenizers*. https://huggingface.co/docs/transformers/tokenizer_summary — 主要分詞器的概覽，附可執行的範例。
