---
translation_reviewed: 2026-10-28
---

# ByT5：無分詞的位元組級建模（Xue et al., 2022）

ByT5 是一個預訓練的 Transformer，它直接讀取文字的 UTF-8 位元組，因此完全不需要學習得來的分詞器。它移除了上層主題[分詞](../index.md)所圍繞的詞彙表問題，代價是輸入序列大幅變長。

## 概述

子詞分詞器把文字壓縮成片段，而它們的詞彙表在分詞器訓練完成時就已固定。Xue et al.（2022）問的是：模型能否改為處理文字最底層的表示？任何字串都可以寫成位元組序列，而位元組值構成一個涵蓋所有語言、共 256 個符號的固定字母表。因此位元組級模型不會遇到未知符號，並能直接看到拼寫與字元層級的結構。

ByT5 是 mT5 的位元組級版本。mT5 是一個多語言子詞模型，採用相同的編碼器—解碼器設計。作者為了配合較長的序列，調整了編碼器與解碼器大小的比例，並以適用於位元組的 span corruption 目標進行預訓練。

## 關鍵概念

- **UTF-8 位元組（UTF-8 bytes）**：把每個 Unicode 字元表示為一到四個位元組的編碼。ASCII 字母佔一個位元組，多數帶重音的歐洲字母佔兩個，多數中日韓（CJK）字元佔三個。
- **位元組詞彙表（Byte vocabulary）**：256 個位元組值加上少量特殊 id，因此嵌入表與子詞詞彙表相比非常小。
- **序列膨脹（Sequence inflation）**：同樣的文字以位元組計算，會成為比詞元更長的序列，從而增加注意力與生成的成本。
- **Span corruption**：一種預訓練任務，把輸入中隨機的片段替換成哨兵標記，並讓模型預測被遮蓋的片段。

## 運作方式

模型依下列少數步驟處理文字：

1. 把輸入字串編碼為 UTF-8 位元組。
2. 把每個位元組值對映到一個 id，並以特殊詞元的數量作為位移。
3. 以 span corruption 預訓練編碼器—解碼器 Transformer：遮蓋隨機的位元組片段，並訓練解碼器重建它們。
4. 在下游任務上以相同的位元組格式微調。
5. 生成時，把預測出的位元組解碼回文字。若多位元組字元被拆散在不同的生成步驟中，必須明確處理，因為在整個序列完成之前，單獨的位元組並不構成有效字元。

成本很容易說明。對於固定的一段文字，位置的數目就是 UTF-8 位元組的總數。因此一句中文在 ByT5 中的長度，會是具備中文感知子詞詞彙表的模型的好幾倍；而在完整注意力中，運算量隨長度的平方增長。

## 結果

Xue et al. 報告，在相當的模型大小下，ByT5 在標準多語言基準上與其子詞對應模型 mT5 相當。他們也報告了在依賴拼寫與發音的任務上的優勢，以及在輸入文字含有雜訊（如拼寫錯誤）時更強的穩健性。由於輸出序列較長，生成速度較慢。確切分數見原論文，此處不重複。

## 限制

- **序列更長。** 同樣的文字，訓練與推論的成本都更高，而長文件能放進固定上下文視窗的內容也更少。
- **容量分配。** 位元組級模型必須把容量用於學習字元如何組成字，而子詞詞彙表是事先完成這項工作的。
- **效益取決於任務。** 在拼寫與雜訊敏感任務上的收益，不會自動延伸到依賴大量知識或長上下文的任務。
- **生態系統。** 多數已部署的模型及其工具都假設使用子詞分詞器，使位元組級模型較難被採用。

## 開放問題

- 位元組級模型能否在保持穩健性的同時，恢復子詞模型的效率？Byte Latent Transformer（Pagnoni et al., 2024）以動態大小的位元組區塊來達成，其擴展行為是一個值得持續檢驗的案例。
- 應如何在相同的訓練成本（而非相同的參數量）下，公平地比較位元組級模型與子詞模型？
- 移除分詞器，是否會改變模型對形態與拼寫的學習？這個問題與上層主題中關於人類比較的爭論相關。

## 相關連結

- 上層主題：[分詞](../index.md)。
- 相關方法：[位元組對編碼](../bpe/index.md)（位元組級的想法透過位元組級 BPE 延伸而來）與 [SentencePiece](../sentencepiece/index.md)。
- 模型家族：[大型語言模型](../../index.md)。

## 參考文獻

### 開創性論文

- Xue, L. et al. (2022). *ByT5: Towards a token-free future with pre-trained byte-to-byte models*. TACL. https://arxiv.org/abs/2105.13626 — 一種以位元組為單位的預訓練 Transformer，完全移除分詞器，並與子詞模型進行比較。
- Wang, C., Cho, K. & Gu, J. (2019). *Neural Machine Translation with Byte-Level Subwords*. arXiv. https://arxiv.org/abs/1909.03341 — 把位元組級 BPE 應用於翻譯，使任何文字都能以 256 個位元組值組成的基礎詞彙表來編碼。
- Pagnoni, A. et al. (2024). *Byte Latent Transformer: Patches Scale Better Than Tokens*. arXiv. https://arxiv.org/abs/2412.09871 — 提出一種位元組級模型，把位元組分成大小動態變化的區塊，並與以分詞器為基礎的模型比較其擴展特性。

### 綜述與教科書

- Mielke, S. J. et al. (2021). *Between words and characters: A Brief History of Open-Vocabulary Modeling and Tokenization in NLP*. arXiv. https://arxiv.org/abs/2112.10508 — 回顧 NLP 如何從字走向字元與子詞，並整理每種單位的取捨。

### 文章與文件

- Petrov, A. et al. (2023). *Language Model Tokenizers Introduce Unfairness Between Languages*. arXiv. https://arxiv.org/abs/2305.15425 — 顯示分詞器可能讓同樣的內容在某些語言中所需的詞元數遠多於英文。
- Schmidt, C. W. et al. (2024). *Tokenization Is More Than Compression*. arXiv. https://arxiv.org/abs/2402.18376 — 主張單靠壓縮率無法預測分詞器在下游語言建模中的表現，並以其他標準比較各種分詞器。
