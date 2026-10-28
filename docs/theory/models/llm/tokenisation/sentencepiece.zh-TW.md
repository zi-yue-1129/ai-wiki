---
translation_reviewed: 2026-10-28
---

# SentencePiece 與 unigram 模型（Kudo，2018）

SentencePiece 是直接在原始文字上訓練的分詞器，不需要先把文字切成單字，並可選擇以位元組對編碼或 unigram 語言模型來挑選片段。unigram 版本以整體切分的似然來評分，並能在訓練時取樣不同的切分。本頁是[分詞](index.md)的一部分。

## 概述

早期的子詞工具假設輸入已經先切成單字，對於日語、中文等不以空白分隔字詞的語言而言，這很難做到。Kudo 與 Richardson（2018）建立 SentencePiece，把輸入當作原始字元串流處理，空白則以可見的符號編碼。這使切分可以逆轉，解碼即能完整還原原始文字。Kudo（2018）加入了 unigram 模型，以及對同一句子取樣不同切分的方法。

## 關鍵概念

- **片段（piece）**：詞彙表中的單位，可以是字元、子詞或整個字。
- **unigram 語言模型**：為每個片段指定機率，並把一種切分視為各片段機率之乘積的模型。
- **切分格（lattice）**：以詞彙表中片段切分一個句子的所有方式。
- **子詞正則化**：訓練時使用取樣的切分，而非唯一的最可能切分，使模型看到同一個字的多種切分。
- **空白標記**：代表片段前空白的符號，使空白成為詞元序列的一部分，因此可以還原。

## 問題

應如何從任何語言的原始文字學習子詞詞彙表，並如何切分句子，才能使結果可逆，同時讓模型受益於切分上的不確定性？

## 運作方式

unigram 方法把句子 \(X\) 視為片段序列 \(\mathbf{x}=(x_1,\dots,x_M)\)，其機率為

\[
p(\mathbf{x}) = \prod_{i=1}^{M} p(x_i), \qquad \sum_{x\in V} p(x) = 1.
\]

給定詞彙表與片段機率，切分由 Viterbi 演算法選出，即 \(\mathbf{x}^\ast = \arg\max_{\mathbf{x}\in S(X)} p(\mathbf{x})\)，其中 \(S(X)\) 為 \(X\) 在詞彙表中所有可能的切分。

訓練從一個很大的候選詞彙表開始。它以期望最大化在語料上估計片段機率，然後移除一部分片段，這些片段被移除後對語料似然的降低最少。重複這些步驟，詞彙表就會縮小到目標大小。

在子詞正則化中，則是取樣切分，而不是取最大值。Kudo（2018）從 \(P(\mathbf{x}\mid X) \propto p(\mathbf{x})^{\alpha}\) 中取樣，其中 \(\alpha\) 控制取樣偏向可能切分的程度。

## 主要方法

- **BPE 模式**：SentencePiece 也在原始文字上實作位元組對編碼，因此同一工具可產生兩種詞彙表。見[位元組對編碼](byte-pair-encoding.md)。
- **unigram 模式**：上述以似然為基礎的方法，可選擇是否取樣。

## 變體

- **確定性 unigram**：總是使用 Viterbi 切分，結果可重現，服務時也較簡單。
- **取樣 unigram**：在訓練時抽取切分，如子詞正則化所做的。這相當於對輸入文字做資料擴增。
- **位元組備援**：後來的實作提供的選項，把詞彙表外的字元以位元組編碼，因此沒有任何輸入是未知的。

## 結果與限制

- Kudo 與 Richardson（2018）報告了英日翻譯的驗證實驗，發現直接在原始句子上訓練子詞模型，所得準確度與在預先切詞的輸入上訓練相當。
- Kudo（2018）報告，在多個資料集上，子詞正則化相較於單一固定切分能提升翻譯品質。
- unigram 詞彙表取決於擬合時所用的語料，因此在一個領域學到的詞彙表，可能對另一個領域的文字切分效果不佳。
- 在訓練時使用取樣切分，而推論時使用最可能的切分，會造成訓練與推論之間的不一致，這是此方法在設計上接受的代價。

## 應用

- **多語言翻譯與語音模型**：多種語言共用一個詞彙表，包括不以空白分隔字詞的語言。
- **預訓練語言模型**：許多多語言模型採用 SentencePiece 詞彙表，可逆的空白標記使模型能輸出完整精確的文字。
- **資料擴增**：取樣的切分使模型接觸到罕見字的其他切分方式。

## 開放問題

- 當訓練資料龐大且多樣時，應如何設定取樣溫度 \(\alpha\)？
- 取樣對大規模預訓練是否有幫助，還是其效益僅限於小型翻譯資料集？

## 與其他頁面的連結

- 上層主題：[分詞](index.md)
- 本主題的另一方法：[位元組對編碼](byte-pair-encoding.md)
- 使用於：[大語言模型](../index.md)

## 參考文獻

### 奠基性論文

- Kudo, T. & Richardson, J. (2018). SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing. arXiv:1808.06226. https://arxiv.org/abs/1808.06226 — 描述 SentencePiece 函式庫，它能在原始文字上訓練 BPE 或 unigram 詞彙表，並可逆地還原文字。
- Kudo, T. (2018). Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates. In *Proceedings of the 56th Annual Meeting of the ACL (Volume 1: Long Papers)*, 66–75. https://doi.org/10.18653/v1/P18-1007 — 提出 unigram 切分模型，以及為正則化而取樣子詞候選的方法。
- Sennrich, R., Haddow, B. & Birch, A. (2016). Neural Machine Translation of Rare Words with Subword Units. In *Proceedings of the 54th Annual Meeting of the ACL (Volume 1: Long Papers)*, 1715–1725. https://doi.org/10.18653/v1/P16-1162 — SentencePiece 同時實作的位元組對編碼基準。

### 綜述與教科書

- Schuster, M. & Nakajima, K. (2012). Japanese and Korean voice search. In *ICASSP 2012*, 5149–5152. https://doi.org/10.1109/ICASSP.2012.6289079 — 針對沒有字詞邊界的語言所做的資料驅動子詞切分，是原始文字設計的動機之一。
- Xue, L. et al. (2022). ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models. *Transactions of the ACL* 10, 291–306. https://doi.org/10.1162/tacl_a_00461 — 比較子詞詞彙表與位元組級輸入，後者不需要學習詞彙表。
- Wang, C., Cho, K. & Gu, J. (2020). Neural Machine Translation with Byte-Level Subwords. In *AAAI 2020*. arXiv:1909.03341. https://arxiv.org/abs/1909.03341 — 當字元集很大時，可作為替代方案的位元組級切分。
