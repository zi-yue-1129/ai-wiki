---
translation_reviewed: 2026-11-18
---

# word2vec

word2vec 是一組高效率的詞向量學習方法，從大量文字為每個詞學習一個稠密向量。CBOW 與 Skip-gram 透過預測鄰近詞來學習表示；它們也是採用共現統計的 [GloVe](glove.md) 的重要比較對象。父頁[嵌入與表徵學習](index.md)比較不同的訓練訊號。

## 問題

較早的神經語言模型能學到有用詞向量，但詞彙量與隱藏層大小會提高訓練成本，使超大語料訓練昂貴。Mikolov 等人（2013）研究如何有效率地利用數十億詞的語料，以及如何檢驗表示是否捕捉詞義關係。

## 核心概念

兩種架構都省去較早模型中的非線性隱藏層，保留把詞投影到向量空間的步驟。

- **CBOW（連續詞袋）**：由周圍詞預測中央詞。論文的一組設定使用前四詞與後四詞作為輸入，以正確分類目前詞為目標。
- **Skip-gram**：方向相反，由目前詞預測前後視窗中的詞。

出現在相似上下文的詞受到相關的訓練訊號，因此可能學到相近的分布式表示，但不保證向量相同。論文發現，首都與國家、動詞時態等部分關係在向量空間中近似線性。

## 方程與演算法

以 \(E\) 輪訓練、\(T\) 個訓練詞、向量維度 \(D\)、詞彙量 \(V\)，以及論文的上下文／視窗參數 \(N\)（CBOW）或 \(C\)（Skip-gram）表示，論文的近似訓練成本記帳為 \(O=E\times T\times Q\)：

- CBOW：\(Q=ND+D\log_2V\)。
- Skip-gram：\(Q=C(D+D\log_2V)\)。

\(\log_2V\) 來自採用詞樹的階層式 softmax。Mikolov 等人（2013b）後來提出負採樣，作為階層式 softmax 的替代目標；[Goldberg 與 Levy（2014）](https://arxiv.org/abs/1402.3722)提供推導。

訓練以文字滑動視窗產生預測目標，再用隨機梯度更新相關的輸入與輸出向量。CBOW 的輸入是上下文詞；Skip-gram 的輸入則是中央詞。

## 結果

[原論文表 5、6](https://arxiv.org/abs/1301.3781)以語義與語法類比問題評估詞向量。60 億詞的模型使用分散式 DistBelief 訓練，與 16 億詞列並非完全相同的設定。

| 模型 | 向量維度 | 訓練詞數 | 語義 | 語法 | 總體 |
|---|---|---|---|---|---|
| CBOW | 300 | 16 億（1 輪） | 16.1% | 52.6% | 36.1% |
| Skip-gram | 300 | 16 億（1 輪） | 52.2% | 55.1% | 53.8% |
| CBOW | 1000 | 60 億 | 57.3% | 68.9% | 63.7% |
| Skip-gram | 1000 | 60 億 | 66.1% | 65.1% | 65.6% |

這些成對結果中，Skip-gram 的語義準確率較高。論文也研究語料量與維度的影響，但不能由此斷言增加兩者一定改善所有指標。數字取自作者實驗，本頁未重新訓練模型。

## 限制

- **不使用詞形結構**：模型不直接知道詞內部組成；作者因此認為此測試很難達到 100%，並建議納入詞形資訊。
- **完全匹配評分**：與標準答案不同的同義詞仍算錯誤。
- **每詞只有一個向量**：同一詞在不同語境與詞義下共用表示；後續上下文模型處理了這項限制。
- **大規模成本**：更大語料與向量會增加成本，也是分散式訓練的動機。

## 參考資料

### 奠基論文

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — 提出 CBOW、Skip-gram、成本分析與詞類比評估。
- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). *Distributed Representations of Words and Phrases and their Compositionality*. arXiv. https://arxiv.org/abs/1310.4546 — 提出負採樣與高頻詞次採樣。

### 綜述與教科書

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — 說明學習分布式表示的背景。

### 文章與文件

- Goldberg, Y. & Levy, O. (2014). *word2vec Explained: deriving Mikolov et al.'s negative-sampling word-embedding method*. arXiv. https://arxiv.org/abs/1402.3722 — 逐步推導負採樣目標。

### 比較方法

- Pennington, J., Socher, R. & Manning, C. (2014). GloVe: Global Vectors for Word Representation. In *Proceedings of EMNLP 2014*, pp. 1532–1543. https://aclanthology.org/D14-1162/ — 以共現計數建立詞向量，並與 word2vec 比較。
