---
translation_reviewed: 2026-11-18
---

# Sentence-BERT

Sentence-BERT（SBERT）把預訓練 BERT 或 RoBERTa 改成共享權重的孿生編碼器，每個句子產生一個固定維度向量。兩句可直接比較餘弦相似度，不必逐對通過模型。父頁[嵌入與表徵學習](index.md)介紹其與其他表示方法的關係。

## 問題

BERT 被微調為句對交叉編碼器時，會同時讀取兩句並輸出分數；每個候選句對都要執行一次網路。Reimers 與 Gurevych（2019）估計，從 10,000 句中找出最相似的一對，需要約 5,000 萬次推論，在 V100 GPU 上約花 65 小時。直接平均 BERT 詞元輸出或取 `[CLS]`，在其 STS Benchmark 測試中分別只有 46.35、16.50 的 Spearman 相關（乘以 100）。

## 核心概念

兩句分別通過共享權重的編碼器，再把詞元輸出池化為句向量。論文比較 `[CLS]`、平均池化 MEAN（預設）與最大池化 MAX，並以句對資料微調表示。

每句能獨立編碼，因此整個資料庫可預先建立向量並儲存；相似度計算不再需要逐對執行 transformer，只需向量運算。

## 方程與演算法

論文依標註資料使用三種目標：

- **分類**：採欄向量慣例，令 \(u,v\in\mathbb R^n\)，串接 \(h=[u;v;|u-v|]\in\mathbb R^{3n}\)。若有 \(k\) 個標籤，使用 \(W\in\mathbb R^{k\times3n}\) 得到 \(o=\operatorname{softmax}(Wh)\)，再計算交叉熵。若改用列向量，權重矩陣也須轉置；逐元素差值提供兩句差異資訊。
- **迴歸**：以均方誤差讓 \(u,v\) 的餘弦相似度接近人工相似度分數。
- **三元組**：錨點 \(s_a\)、正例 \(s_p\)、負例 \(s_n\) 的損失為 \(\max(\lVert s_a-s_p\rVert_2-\lVert s_a-s_n\rVert_2+\varepsilon,0)\)。論文實驗使用歐氏距離與 \(\varepsilon=1\)。

可先用自然語言推論（NLI）資料訓練分類目標，再用 STS Benchmark 的迴歸目標微調。

## 結果

[原論文表 1、2](https://aclanthology.org/D19-1410/)報告 STS Benchmark（STSb）測試集的 Spearman 相關（乘以 100）：

| 模型 | Spearman |
|---|---|
| BERT 詞元平均表示 | 46.35 |
| SBERT-NLI-base（未用 STSb 訓練） | 77.03 |
| SBERT-NLI-large（未用 STSb 訓練） | 79.23 |
| SBERT-NLI-STSb-base | 85.35 ± 0.17 |
| SBERT-NLI-STSb-large | 86.10 ± 0.13 |
| BERT 交叉編碼器，NLI 與 STSb，base（比較基準） | 88.33 ± 0.19 |

在上述 NLI 加 STSb 設定中，交叉編碼器分數較高，但這不是所有任務與模型的固定排序。對 10,000 句的搜尋，論文報告建立向量約 5 秒，餘弦比較約 0.01 秒；這是作者當時的實驗條件，不是任意硬體的速度保證。

## 限制

- **跨主題泛化**：Argument Facet Similarity 實驗以兩個主題訓練、另一主題測試，SBERT 約落後 BERT 七個 Spearman 點。這是特定資料設定的限制，不是普遍適用的最低訓練主題數。
- **獨立編碼**：句子不會直接對另一句的詞元做交叉注意力。
- **原始遷移測試的範圍**：第 5 節用 SentEval 分類器評估凍結句向量；作者強調相似度搜尋用途，不把它視為所有新任務微調 BERT 的替代品。這不表示後續句向量模型不能做遷移學習。
- **比較有得有失**：部分任務如 SICK-R、TREC 落後 Universal Sentence Encoder；原論文實驗也未發現 RoBERTa 帶來顯著改善。

## 參考資料

### 奠基論文

- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. arXiv. https://arxiv.org/abs/1908.10084 — 說明孿生架構、池化、訓練目標、STSb 與計算時間。
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv. https://arxiv.org/abs/1810.04805 — SBERT 所改造的預訓練編碼器與交叉編碼器基準。

### 綜述與教科書

- Cer, D., Diab, M., Agirre, E., Lopez-Gazpio, I. & Specia, L. (2017). *SemEval-2017 Task 1: Semantic Textual Similarity – Multilingual and Cross-lingual Focused Evaluation*. arXiv. https://arxiv.org/abs/1708.00055 — 介紹本頁使用的 STS Benchmark。
- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — 學習表示與遷移的背景。

### 文章與文件

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — 詞層級表示與向量比較的代表方法。
