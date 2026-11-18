---
translation_reviewed: 2026-11-18
---

# GloVe

GloVe（Global Vectors for Word Representation）透過擬合全語料詞對共現次數的對數，為每個詞學習一個向量。它結合全域計數統計與 [word2vec](word2vec.md) 等預測型方法所捕捉的線性關係。父頁[嵌入與表徵學習](index.md)說明這類訓練訊號的位置。

## 問題

Pennington、Socher 與 Manning（2014）指出，潛在語義分析等計數方法能利用全域共現統計，但詞類比表現較弱；局部視窗預測方法則能捕捉類比關係，卻不直接擬合全域計數。GloVe 試圖結合兩者。

## 核心概念

令 \(X_{ij}\) 為詞 \(j\) 出現在詞 \(i\) 上下文的次數。模型為詞與上下文分別學習 \(w_i\)、\(\widetilde w_j\) 及偏置，使內積加偏置近似 \(\log X_{ij}\)。加權則降低稀少詞對的影響，並避免極高頻詞對持續取得更大權重。

模型由共現矩陣出發，卻使用可最佳化的迴歸目標。作者指出，計數與預測兩類方法都利用同一種共現資訊，並非完全對立。

## 方程與演算法

對觀察過的詞與上下文配對，最小化加權平方誤差：

\[
J=\sum_{i,j:X_{ij}>0}f(X_{ij})\left(w_i^\top\widetilde w_j+b_i+\widetilde b_j-\log X_{ij}\right)^2.
\]

僅對正計數求和，避免計算 \(\log 0\)。權重為

\[
f(x)=\begin{cases}(x/x_{\max})^\alpha,&0<x<x_{\max},\\1,&x\ge x_{\max}.\end{cases}
\]

論文設定 \(x_{\max}=100\)、\(\alpha=3/4\)。權重隨計數增加，直到封頂為 1；不是高頻越高、權重越低。作者發現截止值影響較小，\(\alpha=3/4\) 相較線性權重 \(\alpha=1\) 有適度改善。

先掃描語料建立共現矩陣，再對非零項迭代最佳化；因此每輪成本依賴實際觀察到的詞對數，而非必須遍歷完整矩陣。

## 結果

[原論文表 2](https://aclanthology.org/D14-1162/)使用與 word2vec 相同的語義／語法詞類比測試：

| 模型 | 向量維度 | 語料詞數 | 語義 | 語法 | 總體 |
|---|---|---|---|---|---|
| GloVe | 300 | 420 億 | 81.9% | 69.3% | 75.0% |
| GloVe | 300 | 60 億 | 77.4% | 67.0% | 71.7% |
| Skip-gram（作者實作設定） | 300 | 60 億 | 73.0% | 66.0% | 69.1% |
| CBOW（作者實作設定） | 300 | 60 億 | 63.6% | 67.4% | 65.7% |

75% 的結果來自 420 億詞模型。作者也報告，在匹配語料、詞彙、視窗與訓練時間的比較中，GloVe 表現較好。語料包括 Wikipedia、Gigaword 5 與 Common Crawl；除 Common Crawl 模型外，詞彙表取最常見的 40 萬詞。這些是論文實驗結果，不是本頁重現的量測。

## 限制

- **經驗性權重**：\(\alpha=3/4\) 的選擇主要由實驗支持。
- **比較依賴設定**：兩類模型有多種超參數；作者承認需要更完整的分析。
- **語料組成影響**：語義準確率未隨語料量單調上升；作者認為 Gigaword 的固定新聞來源與過時事實可能是原因之一。
- **最壞成本**：非零詞對數最壞可與詞彙量平方同階；更緊的估計依賴共現計數的冪律假設。
- **靜態向量**：不同詞義仍共用同一向量。

## 參考資料

### 奠基論文

- Pennington, J., Socher, R. & Manning, C. (2014). GloVe: Global Vectors for Word Representation. In *Proceedings of EMNLP 2014*, pp. 1532–1543. https://aclanthology.org/D14-1162/ — 定義加權平方誤差、權重函數與本頁類比結果。
- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — 介紹用於比較的 word2vec 預測模型。

### 綜述與教科書

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — 分布式表示與泛化的背景。

### 文章與文件

- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). *Distributed Representations of Words and Phrases and their Compositionality*. arXiv. https://arxiv.org/abs/1310.4546 — 說明常用於比較的負採樣詞向量方法。
- Goldberg, Y. & Levy, O. (2014). *word2vec Explained: deriving Mikolov et al.'s negative-sampling word-embedding method*. arXiv. https://arxiv.org/abs/1402.3722 — 解釋 word2vec 負採樣目標。
