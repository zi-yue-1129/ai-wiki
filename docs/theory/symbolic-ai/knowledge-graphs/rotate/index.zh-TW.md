---
translation_reviewed: 2026-10-28
---

# RotatE

RotatE 是一種知識圖譜嵌入模型。它把每個實體表示為一個複數向量，把每個關係表示為逐元素的旋轉，因此一個真實的三元組 $(h, r, t)$，是指頭實體經該關係旋轉後，會落在尾實體上。Sun 等人於 ICLR 2019 提出此模型。它是[知識圖譜概述](../index.md)中的代表性方法之一。

## 概述

知識圖譜並不完整，因此核心任務是鏈結預測：對於給定的頭實體與關係，哪些尾實體是合理的？嵌入方法為每個實體與關係指派一個向量，並為每個三元組評分。分數必須尊重關係的行為方式。論文列出三種模式：**對稱**（若 A 與 B 結婚，則 B 與 A 結婚）、**反轉**（若 A 是 B 的父母，則 B 是 A 的子女），以及**組合**（兩個關係的鏈結蘊含第三個關係）。

早先的模型只捕捉到其中一部分。TransE 能處理反轉與組合，但會迫使對稱關係的平移向量為零。ComplEx 能處理非對稱性，卻無法推論組合。RotatE 的設計目標是同時處理這三種模式。[^1] 符號系統會把這些模式寫成規則；RotatE 則以幾何方式編碼它們。

## 核心概念

- **複數嵌入**：每個實體是由 $k$ 個複數組成的向量。
- **單位模關係**：關係向量的每個元素絕對值為 1，因此它是純粹的相位 $e^{i\theta}$。乘上它會使複數旋轉而不被拉伸。
- **自對抗取樣**：依據目前模型認為的合理程度為負樣本（虛假三元組）加權，使訓練的心力集中於困難的案例。

## 運作方式

設 $h, r, t \in \mathbb{C}^k$，RotatE 要求

$$
t_i = h_i\, r_i, \qquad |r_i| = 1.
$$

每個 $r_i = e^{i\theta_{r,i}}$ 是逆時針旋轉 $\theta_{r,i}$ 弧度。評分所用的距離為（$\circ$ 為逐元素的 Hadamard 乘積）

$$
d_r(h, t) = \lVert h \circ r - t \rVert.
$$

模長限制產生了上述模式。當關係向量的每個元素為 $\pm 1$ 時，該關係為對稱。兩個關係互為反向，是指其中一個向量是另一個的複共軛。一個關係是另外兩個關係的組合，是指其相位等於兩者相位之和。論文在附錄中證明了這些性質。[^1]

訓練採用邊界損失，作用於取樣得到的負樣本 $(h'_i, r, t'_i)$：

$$
L = -\log \sigma\big(\gamma - d_r(h, t)\big) - \sum_{i=1}^{n} p(h'_i, r, t'_i)\,\log \sigma\big(d_r(h'_i, t'_i) - \gamma\big),
$$

其中 $\gamma$ 為固定的邊界，$\sigma$ 為 sigmoid 函數。每個負樣本的權重，是以目前模型的分數 $f_r = -d_r$ 計算的 softmax，溫度為 $\alpha$：

$$
p(h'_j, r, t'_j) = \frac{\exp\big(\alpha\, f_r(h'_j, t'_j)\big)}{\sum_i \exp\big(\alpha\, f_r(h'_i, t'_i)\big)}.
$$

愈接近真實三元組、愈合理的負樣本會獲得較大的權重。論文指出，此模型的成本在時間與記憶體上都保持線性。[^1]

## 結果

論文在四個基準上評估：FB15k、WN18、FB15k-237 與 WN18RR。指標為平均倒數排名（MRR）與 Hits@N，採用過濾式設定。[^2]

在 FB15k 上，RotatE 回報的 MRR 為 0.797，Hits@10 為 0.884，ComplEx 則為 0.692 與 0.840。在 WN18 上，RotatE 回報的 MRR 為 0.949，Hits@10 為 0.959。[^2]

在 FB15k-237 與 WN18RR 上，優勢更為明顯。RotatE 在 FB15k-237 回報的 MRR 為 0.338，Hits@10 為 0.533，ConvE 則為 0.325 與 0.501；在 WN18RR 上，RotatE 回報的 MRR 為 0.476，Hits@10 為 0.571，ConvE 則為 0.43 與 0.52。[^2] RotatE 與其相位變體之間的差距（該變體同時限制實體的模長）在這兩個資料集上最大。論文據此認為，模長對組合模式十分重要。[^2]

## 限制

- **僅使用三元組。** 模型不使用實體類型、文本或本體公理，因此無法直接套用綱要限制。
- **不確定性。** 作者將建模圖譜中的不確定性列為未來工作，因此模型並未表示一個事實的可信程度。[^1]
- **比較。** 部分基準數字來自其他論文，因此比較混合了不同的訓練執行。[^2]
- **調參。** 邊界與取樣溫度是從格點中選取的，結果取決於這項搜尋。[^1]

## 開放問題

- 以旋轉為基礎的模型能否表示涉及兩個以上實體的事實，或隨時間變化的事實？Ji 等人綜述了時序圖譜。[^3]
- 在學習得到的關係中所發現的模式結構，能否延伸到雜訊較多、自動建構的圖譜？

## 參考文獻

### 開創性論文

- Sun, Z. et al. (2019). RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space. *ICLR*. https://arxiv.org/abs/1902.10197 — 將每個關係建模為複數空間中的旋轉，並在四個鏈結預測基準上報告結果。
- Yang, B. et al. (2014). Embedding Entities and Relations for Learning and Inference in Knowledge Bases. arXiv. https://arxiv.org/abs/1412.6575 — 一種用於鏈結預測的簡單雙線性模型，也是 RotatE 比較的基準之一。
- Trouillon, T. et al. (2016). Complex Embeddings for Simple Link Prediction. arXiv. https://arxiv.org/abs/1606.06357 — 以複值嵌入處理對稱與非對稱關係。

### 綜述與教科書

- Nickel, M. et al. (2015). A Review of Relational Machine Learning for Knowledge Graphs. arXiv. https://arxiv.org/abs/1503.00759 — 回顧用於預測知識圖譜事實的潛在特徵模型。
- Ji, S. et al. (2020). A Survey on Knowledge Graphs: Representation, Acquisition and Applications. arXiv. https://arxiv.org/abs/2002.00388 — 綜述知識圖譜的表示學習、補全、時序圖譜與應用。

[^1]: Sun et al. (2019)，見上方參考文獻。
[^2]: Sun et al. (2019)，見上方參考文獻，表 4 與表 5。數字直接取自表格，其中的基準列來自其他論文。
[^3]: Ji et al. (2020)，見上方參考文獻。
