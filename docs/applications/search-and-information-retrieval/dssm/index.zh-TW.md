---
translation_reviewed: 2026-10-28
---

# DSSM（Huang 等人，2013）

深層結構化語意模型（Deep Structured Semantic Model, DSSM）把查詢與網路文件映射到同一個低維向量空間，使相關性變成兩個向量之間的距離。Huang 等人以網路搜尋引擎的點擊資料訓練它。它是網頁搜尋中[檢索](../index.md)的早期神經方法之一，父頁面為[搜尋引擎與資訊檢索](../index.md)。

## 概述

關鍵字檢索依文件與查詢共享的字詞來評分。兩段講同一主題的文字可能只共享很少的字詞；例如一段症狀描述的查詢，可能會匹配到使用不同醫學詞彙的文件。潛在語意模型，例如潛在語意分析（LSA），以把文字投影到低維空間來處理這個問題，但它們的訓練沒有使用點擊資料，而點擊正是搜尋引擎得知人們真正想要什麼的依據。

## 關鍵概念

- **雙塔**：查詢用一個網路，文件用另一個網路。兩者各自把文字映射為一個向量，且兩個網路不共享參數。
- **餘弦相關性**：文件與查詢的相關性，就是兩者向量的餘弦相似度。
- **詞雜湊**：每個字詞被切分為帶有邊界標記的字母三元組，因此「go」會變成「#go」與「go#」。詞彙量因此維持在較小的規模，拼字錯誤與罕見字詞也能與已知的字詞共享特徵。
- **點擊資料訓練**：某查詢下被點擊的文件是正例，而曝光但未被點擊的文件，或從語料中抽樣的文件，則作為負例。

## 運作方式

對於查詢 $Q$ 與文件 $D$，令 $y_Q$ 與 $y_D$ 為兩個塔所產生的向量。相關性與給定查詢時文件的機率為

$$
R(Q,D) = \cos(y_Q, y_D), \qquad P(D \mid Q) = \frac{\exp(\gamma R(Q,D))}{\sum_{D' \in \mathcal{D}} \exp(\gamma R(Q,D'))}
$$

其中 $\gamma$ 是平滑因子，$\mathcal{D}$ 是該查詢的候選集合，其中包含被點擊的文件 $D^{+}$。訓練會最大化被點擊文件的似然，等同於在所有訓練配對上最小化 $-\sum \log P(D^{+} \mid Q)$。

程序如下：

1. 把每個查詢與文件轉換為字母三元組的袋（詞雜湊）。
2. 讓每種表示在各自的塔中通過數層非線性層，產生低維向量。
3. 對於一個查詢，計算其被點擊的文件與抽樣負例的每一對之餘弦相似度。
4. 套用上述的 Softmax，並以梯度下降更新兩個塔，使被點擊文件的負對數似然最小。
5. 推論時，先離線編碼所有文件並儲存其向量。對每個查詢，編碼查詢後依餘弦相似度對儲存的文件排序。

第 5 步使模型具有實用性。文件向量是離線計算的，因此線上成本只有一次查詢編碼與一次最近鄰搜尋。

## 結果

論文在由真實搜尋資料建立的網頁文件排序任務上評估這些模型。作者報告，他們最好的模型明顯優於其他潛在語意模型，後者是本研究之前的最先進方法。摘要沒有給出數字，因此本頁不引用任何數值。

## 限制

- **沒有字詞層級的互動。**查詢與文件只透過一個餘弦分數相遇，因此模型無法看出查詢中的哪個字詞與段落中的哪個字詞相符。之後的模型，例如 Mitra 等人（2016）的 Duet 模型，正是為此結合了精確的字詞匹配與分散式表示。
- **三元組的袋。**詞雜湊移除了字詞順序，使表示變得粗略，因此意義不同但字母相同的片語可能發生碰撞。
- **每份文件只有一個向量。**一個向量必須概括整份文件。具有多個主題的長文件會失去細節，這促成了 [ColBERT](../../../engineering/vector-databases/colbert.md) 等多向量方法。

## 開放問題

- 雙編碼器如今在第一階段檢索中已相當普遍，但最好的訓練方式，以及它們能否達到交叉編碼器的精確度，仍有爭議。

## 相關連結

- 這種雙塔設計與[密集段落檢索](../../../engineering/vector-databases/dense-passage-retrieval.md)是同一個想法，後者為開放領域問答而提出。
- 訓練目標是在候選之上做 Softmax，與[對比學習](../../../theory/paradigms/self-supervised/contrastive-learning/index.md)所用的目標相似。
- 以這種方式檢索到的候選，會再由排序器排序，例如 [RankNet](../ranknet/index.md) 或 [Wide & Deep](../wide-and-deep/index.md) 之類的模型。

## 應用

DSSM 風格的雙塔模型用於檢索候選文件、廣告與項目，應用於搜尋與推薦，其中項目向量可以事先建立索引。

## 參考文獻

### 開創性論文

- Huang, P.-S. et al. (2013). Learning deep structured semantic models for web search using clickthrough data. CIKM. https://doi.org/10.1145/2505515.2505665 — 以點擊資料訓練查詢與文件網路，使被點擊的文件在共享的語意空間中得分較高，並以詞雜湊達成規模化。
- Mitra, B., Diaz, F. & Craswell, N. (2016). Learning to match using local and distributed representations of text for web search. https://arxiv.org/abs/1610.08136 — 為網頁文件排序結合精確的字詞匹配與學習到的分散式表示，回應雙編碼器缺乏字詞層級互動的問題。
- Karpukhin, V. et al. (2020). Dense passage retrieval for open-domain question answering. https://arxiv.org/abs/2004.04906 — 顯示以點積評分、經訓練的雙編碼器可以在段落檢索上取代 BM25，且只需少量問題與段落配對。
- Formal, T. et al. (2021). SPLADE: Sparse lexical and expansion model for first stage ranking. https://arxiv.org/abs/2107.05720 — 學習稀疏的查詢與文件表示，保留倒排索引的效率，是密集第一階段檢索的另一種選擇。

### 綜述與教科書

- Lin, J., Nogueira, R. & Yates, A. (2020). Pretrained transformers for text ranking: BERT and beyond. https://arxiv.org/abs/2010.06467 — 神經文字排序綜述，並列說明雙編碼器與重新排序器，比較兩者的取捨。
