---
translation_reviewed: 2026-11-26
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

CBOW 與 Skip-gram 決定預測方向。輸出的訓練目標則是另一項選擇，包括階層式 softmax 或負採樣。[^objectives]

### 使用階層式 softmax 的成本

以 $E$ 輪訓練、$T$ 個訓練詞、向量維度 $D$、詞彙量 $V$，以及論文的上下文／視窗參數 $N$（CBOW）或 $C$（Skip-gram）表示，論文的近似訓練成本記帳為 $O=E\times T\times Q$：

- CBOW：$Q=ND+D\log_2V$。
- Skip-gram：$Q=C(D+D\log_2V)$。

$\log_2V$ 來自採用詞樹的階層式 softmax。Mikolov 等人（2013b）後來提出負採樣，作為階層式 softmax 的替代目標；[Goldberg 與 Levy（2014）](https://arxiv.org/abs/1402.3722)提供推導。

訓練以文字滑動視窗產生預測目標，再用隨機梯度更新相關的輸入與輸出向量。CBOW 的輸入是上下文詞；Skip-gram 的輸入則是中央詞。

### 使用負採樣的 Skip-gram

令 $v_w\in\mathbb R^D$ 為中央詞 $w$ 的輸入向量，$u_c\in\mathbb R^D$ 為上下文 $c$ 的輸出向量。即使詞與上下文詞彙表包含相同詞元，兩者仍是不同的參數表。寫成 $s_{wc}=u_c^\top v_w$，對上下文詞彙集合 $\mathcal V$，完整 softmax 會定義正規化的條件分布[^objectives]

$$
p_\theta(c\mid w)=\frac{\exp(s_{wc})}{\sum_{c'\in\mathcal V}\exp(s_{wc'})}.
$$

使用負採樣的 Skip-gram（SGNS）改為訓練二元分類器，區分觀察到的詞與上下文配對，以及雜訊配對。對一組觀察配對 $(w,c)$，再由雜訊分布 $q$ 抽取 $k\ge1$ 個上下文 $n_r$，最小化[^objectives]

$$
\begin{aligned}
\ell(w,c)&=-\log\sigma(s_{wc})-\sum_{r=1}^{k}\log\sigma(-s_{w n_r}),\\
\sigma(s)&=\frac{1}{1+\exp(-s)},\qquad n_r\sim q.
\end{aligned}
$$

此採樣損失計算一個正例及 $k$ 個負例的內積，因此每組觀察配對的這些分數與更新成本為 $O((k+1)D)$。前述階層式 softmax 成本公式並不描述這種輸出目標。SGNS 所最佳化的損失也與完整 softmax 的對數概似不同。[^objectives]

Mikolov 等人（2013b）使用將單詞頻率 $f(c)$ 提升至 $3/4$ 次方的雜訊分布，[^noise]

$$
q(c)=\frac{f(c)^{3/4}}{\sum_{c'\in\mathcal V}f(c')^{3/4}}.
$$

它控制哪些上下文會被抽為負例。高頻詞次採樣則在建立訓練樣本時，丟棄部分語料詞元。雜訊樣本是訓練標籤，並不能證明被抽到的詞與中央詞在語義上不相容。[^noise]

## 如何解讀 sigmoid

SGNS 的 sigmoid 分數對應到觀察配對與雜訊配對的分類任務，並未對上下文詞彙表正規化。為了看出差異，固定中央詞與上下文，令經驗條件機率 $p=p_{\mathrm{data}}(c\mid w)>0$，且 $q(c)>0$。將期望的正、負項彙整後，得到此配對的損失[^interpretation]

$$
j(s)=-p\log\sigma(s)-kq(c)\log\sigma(-s).
$$

若每組配對分數都能獨立最佳化，令 $j'(s)=(p+kq(c))\sigma(s)-p$ 為零，可得

$$
s^*=\log\frac{p}{kq(c)},\qquad
\sigma(s^*)=\frac{p}{p+kq(c)}.
$$

此理想最佳解假設配對分數可獨立調整。有限維度的詞與上下文向量會讓不同配對的分數相互受限，因此訓練後的嵌入不一定能同時達到每個最佳值。[^interpretation]

取一個包含兩種上下文的建構例子，令 $k=5$，兩者的 $q(c)$ 都為 $0.5$。使用自然對數，四捨五入至小數點後四位，可得下表。

| 上下文 | $p_{\mathrm{data}}(c\mid w)$ | 理想分數 $s^*$ | 二元 sigmoid 值 $\sigma(s^*)$ |
|---|---|---|---|
| A | 0.8 | -1.1394 | 0.2424 |
| B | 0.2 | -2.5257 | 0.0741 |

經驗條件機率加總為一，理想二元 sigmoid 值卻只加總為約 $0.3165$。即使經驗條件分布固定，改變 $k$ 或 $q$ 也會改變這些 sigmoid 值。此表展示目標函數的性質，不是 word2vec 的實測輸出。

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

[^objectives]: Mikolov 等人（2013b）第 2.2 節式（4），以及 Goldberg 與 Levy（2014）第 1–2 節，區分 softmax 條件分布、負採樣目標與各自的詞／上下文向量。每組配對的成本由 $k+1$ 組向量配對的計算數量得出。
[^noise]: Mikolov 等人（2013b）第 2.2–2.3 節，說明 $3/4$ 雜訊分布與獨立的高頻詞元次採樣流程。Goldberg 與 Levy（2014）第 2 節說明採樣配對的二元標籤。
[^interpretation]: Levy 與 Goldberg（2014）第 3.1–3.2 節及註腳 1，分析可獨立最佳化的分數、單詞雜訊分布、其平滑變體與維度限制。此處的一般 $q$ 公式與表格由對上述期望損失微分而得。

## 參考資料

### 奠基論文

- Mikolov, T., Chen, K., Corrado, G. & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv. https://arxiv.org/abs/1301.3781 — 提出 CBOW、Skip-gram、成本分析與詞類比評估。
- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. (2013). *Distributed Representations of Words and Phrases and their Compositionality*. arXiv. https://arxiv.org/abs/1310.4546 — 提出負採樣與高頻詞次採樣。
- Levy, O. & Goldberg, Y. (2014). *Neural Word Embedding as Implicit Matrix Factorization*. NIPS 27. https://proceedings.neurips.cc/paper/2014/hash/b78666971ceae55a8e87efb7cbfd9ad4-Abstract.html — 推導使用單詞雜訊分布的 SGNS 與平移 PMI 的關係，並說明有限嵌入維度如何限制理想配對分數。

### 綜述與教科書

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — 說明學習分布式表示的背景。

### 文章與文件

- Goldberg, Y. & Levy, O. (2014). *word2vec Explained: deriving Mikolov et al.'s negative-sampling word-embedding method*. arXiv. https://arxiv.org/abs/1402.3722 — 逐步推導負採樣目標。

### 比較方法

- Pennington, J., Socher, R. & Manning, C. (2014). GloVe: Global Vectors for Word Representation. In *Proceedings of EMNLP 2014*, pp. 1532–1543. https://aclanthology.org/D14-1162/ — 以共現計數建立詞向量，並與 word2vec 比較。
