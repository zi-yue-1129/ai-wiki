---
translation_reviewed: 2026-10-28
---

# SentencePiece 與 Unigram 模型（Kudo and Richardson, 2018）

SentencePiece 是一個分詞器函式庫，它直接從原始文字學習子詞片段，並把空白當成一般符號看待。它的 unigram 模型透過詢問「語料最能承受失去哪些片段」來選出詞彙表。這是上層主題頁[分詞](../index.md)中三種主要做法之一。

## 概述

早期的流程會先依空白把文字切成字，套用特定語言的規則，再對結果執行 BPE 等子詞方法。這種流程對不以空白分隔字詞的語言（如中文與日文）很不方便，而且會使反向還原失去無損性，因為原本的空白已經遺失。Kudo 與 Richardson（2018）設計 SentencePiece 來同時避免這兩個問題。輸入是一串 Unicode 字元，空白被替換成一個可見的標記符號。因此訓練與編碼不需要特定語言的前處理，解碼則能精確還原原始文字。

本頁聚焦於 unigram 模型。

## 關鍵概念

- **Unigram 語言模型（Unigram language model）**：每個片段都有一個機率，而切分的機率是其各片段機率的乘積。片段被視為彼此獨立。
- **候選詞彙表（Candidate vocabulary）**：一個起始的大型片段集合，例如語料中所有頻繁的子字串，最終詞彙表是從中剪枝而來。
- **維特比切分（Viterbi segmentation）**：在模型之下，字串最可能的切分方式，透過對所有切法做動態規劃來求得。
- **子詞正則化（Subword regularisation）**：訓練時從模型取樣一種切分，而非總是使用機率最高的那一種，使網路看到同一個字的多種切法（Kudo, 2018）。

## 運作方式

對於字串 $x$，令 $S(x)$ 為把它切成詞彙表中片段的所有方式的集合，並令一種切分為 $\mathbf{s} = (s_1, \dots, s_n)$。在 unigram 模型下，它的機率為

$$P(\mathbf{s}) = \prod_{i=1}^{n} p(s_i), \qquad \sum_{v \in V} p(v) = 1,$$

而編碼時會選出機率最高的切分 $\mathbf{s}^* = \arg\max_{\mathbf{s} \in S(x)} P(\mathbf{s})$。

訓練會擬合片段機率，然後剪枝詞彙表：

1. 從語料中建立一個包含頻繁子字串的大型候選詞彙表。
2. 使用期望最大化（expectation-maximisation），估計能使語料對數似然度 $\sum_{x \in D} \log \sum_{\mathbf{s} \in S(x)} P(\mathbf{s})$ 最大的片段機率。
3. 對每個片段，估計若移除它，語料似然度會下降多少。單一字元的片段會被保留，以確保每個字串都能被編碼。
4. 移除損失最小的固定比例片段，並重複步驟 2 與 3，直到詞彙表達到目標大小。
5. 以維特比切分編碼新文字，或為了正則化而取樣切分。

由於切分是定義在原始字元串上的，解碼就只是串接片段，再把空白標記換回空格。這正是此方法無損的關鍵。

## 結果

2018 年的 SentencePiece 論文主要是對已釋出函式庫的系統描述，其主要貢獻是設計與工具本身。切分方式對翻譯品質的影響，證據主要來自 Kudo（2018），該文報告在其實驗中，取樣切分能改善神經機器翻譯。分數見該論文，此處不重複。

## 限制

- **獨立性假設。** 片段被獨立評分，因此模型無法捕捉哪些片段傾向於接在哪些片段之後。
- **不保證形態。** 似然度偏好頻繁的片段，而這些片段可能跨越形態邊界。
- **訓練成本。** 對大型候選集做期望最大化，比一次 BPE 合併的計算量更大。
- **詞彙表固定。** 和 BPE 一樣，此方法產生一組固定的片段，因此來自新文字系統或新領域的文字仍可能被切成許多小片段。

## 開放問題

- 在詞彙表大小與資料完全相同的情況下，unigram 模型是否比 BPE 產生更好的下游模型？文獻中的比較設定各不相同。
- 從原始文字建立的多語言詞彙表，是否能公平地分配各語言的詞元？Rust et al.（2021）顯示分詞器的契合度會影響各語言的表現。

## 相關連結

- 上層主題：[分詞](../index.md)。
- 相關方法：[位元組對編碼](../bpe/index.md)與 [ByT5](../byt5/index.md)。

## 參考文獻

### 開創性論文

- Kudo, T. & Richardson, J. (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing*. EMNLP (System Demonstrations). https://arxiv.org/abs/1808.06226 — 介紹 SentencePiece 函式庫，它直接在原始文字上訓練子詞模型，不需要特定語言的預分詞。
- Kudo, T. (2018). *Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates*. ACL. https://arxiv.org/abs/1804.10959 — 提出在訓練時，從 unigram 語言模型取樣多種切分結果。
- Sennrich, R., Haddow, B. & Birch, A. (2016). *Neural Machine Translation of Rare Words with Subword Units*. ACL. https://arxiv.org/abs/1508.07909 — 為神經機器翻譯引入位元組對編碼，是 unigram 方法的主要替代做法。

### 綜述與教科書

- Mielke, S. J. et al. (2021). *Between words and characters: A Brief History of Open-Vocabulary Modeling and Tokenization in NLP*. arXiv. https://arxiv.org/abs/2112.10508 — 回顧 NLP 如何從字走向字元與子詞，並整理每種單位的取捨。

### 文章與文件

- Rust, P. et al. (2021). *How Good is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models*. ACL. https://arxiv.org/abs/2012.15613 — 發現多語言模型在單一語言上的表現，取決於共用的分詞器與該語言的契合程度。
- Petrov, A. et al. (2023). *Language Model Tokenizers Introduce Unfairness Between Languages*. arXiv. https://arxiv.org/abs/2305.15425 — 顯示分詞器可能讓同樣的內容在某些語言中所需的詞元數遠多於英文。
- Wu, Y. et al. (2016). *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation*. arXiv. https://arxiv.org/abs/1609.08144 — 描述 GNMT 系統及其所用的 wordpiece 切分，供與 unigram 方法比較。
