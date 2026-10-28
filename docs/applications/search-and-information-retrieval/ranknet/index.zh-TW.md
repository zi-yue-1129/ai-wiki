---
translation_reviewed: 2026-10-28
---

# RankNet（Burges 等人，2005）

RankNet 是一種神經網路，它從文件配對中學習如何排列搜尋結果；配對中的其中一份文件應排在較前面。Burges 等人於 2005 年在 ICML 發表此方法，它開啟了[學習排序](../index.md)方法中的成對式系列。本方法是父頁面[搜尋引擎與資訊檢索](../index.md)列出的代表性方法之一。

## 概述

在 RankNet 之前，搜尋的排序函數通常靠人工調整，或以簡單的線性模型擬合。Burges 等人想知道：以梯度下降訓練的神經網路，能否直接從人類對「哪份文件較好」的判斷中學出排序函數？他們的關鍵選擇是從配對而非絕對分數中學習。對標註者來說，問「文件 A 對這個查詢是否比文件 B 好」通常比為每份文件給出精確的等級容易，而且這也符合人們評判排序清單的方式。

## 關鍵概念

- **評分函數**：一個網路 $f$，把單一文件的特徵映射為一個實數分數。某查詢的排序，就是依分數由高到低排列文件。
- **成對偏好**：對同一查詢中的兩份文件 $i$ 與 $j$，$i$ 應排在 $j$ 之前的目標機率。若 $i$ 較相關，目標為 1；若 $j$ 較相關，目標為 0；若兩者相同，目標為 0.5。
- **機率式成本**：模型把分數差轉換為機率，而成本則是該機率與目標之間的交叉熵。

## 運作方式

對於特徵向量分別為 $x_i$ 與 $x_j$ 的文件 $i$ 與 $j$，分數差與模型化的機率為

$$
o_{ij} = f(x_i) - f(x_j), \qquad P_{ij} = \frac{e^{o_{ij}}}{1 + e^{o_{ij}}}
$$

該配對的成本是目標 $\bar{P}_{ij}$ 與 $P_{ij}$ 之間的交叉熵：

$$
C_{ij} = -\bar{P}_{ij}\log P_{ij} - (1-\bar{P}_{ij})\log(1-P_{ij})
$$

由於成本只取決於兩個分數的差，把所有分數加上同一常數不會改變任何結果，因此網路學到的是相對順序，而非絕對等級。訓練程序如下：

1. 對每個查詢，收集候選文件與其相關性標籤。
2. 形成配對 $(i, j)$，其中標籤指出 $i$ 應排在 $j$ 之前；平手的配對目標設為 0.5。
3. 以同一個網路為兩份文件評分。
4. 計算該配對的機率與交叉熵成本。
5. 反向傳播成本，並以梯度下降更新權重。
6. 推論時，為每個候選評分並依分數排序。

## 結果

論文在玩具資料與某商業網路搜尋引擎的資料上呈現測試結果。摘要沒有給出數字，因此本頁不引用任何數值。

## 限制

- **每個配對權重相同。**排序清單頂端的錯誤與底部的錯誤成本相同，但排序品質指標主要關注頂端位置。Burges（2010）描述的 LambdaRank 會依交換兩份文件所造成的 nDCG 變化來縮放每個配對的梯度；LambdaMART 則把同樣的想法應用到提升樹上。
- **有標籤的配對成本高。**配對數量隨候選清單的長度呈平方成長，而且配對所需的偏好標籤收集成本高昂。
- **特徵固定。**網路處理的是工程師提供的特徵，它並不學習文字表示。之後的神經網路排序器，例如 [DSSM](../dssm/index.md) 與 BERT 重新排序器，則能學習文字表示。
- **點擊有偏差。**使用者較常點擊前面的位置，因此從記錄點擊所導出的配對會承襲這種偏差，即使如 Joachims（2002）所建議，把點擊讀為偏好也無法避免。

## 開放問題

- 成對成本並不直接最佳化排序指標。究竟逐列或加權指標的變體能縮小多少差距，仍在研究中。
- 成對訓練是否仍適用於大型神經網路重新排序器，後者在文字上使用交叉編碼器，而非人工設計的特徵。

## 相關連結

- 此成本是[損失函數與最佳化](../../../theory/paradigms/supervised/loss-functions-and-optimization/index.md)中所說明的一類成對損失。
- 其基於樹的後繼者 LambdaMART 是提升樹模型，參見[決策樹與集成方法](../../../theory/paradigms/supervised/trees-and-ensembles/index.md)。
- 取代人工特徵的神經文字匹配，是 [DSSM](../dssm/index.md) 的主題。

## 應用

RankNet 及其後繼方法用來為搜尋引擎排序結果清單，此時候選已經被檢索出來，只需依相關性排序。

## 參考文獻

### 開創性論文

- Burges, C. et al. (2005). Learning to rank using gradient descent. ICML. https://doi.org/10.1145/1102351.1102363 — 提出 RankNet，一種以文件配對的機率式成本訓練的神經網路排序器，並在某商業搜尋引擎的資料上測試。
- Joachims, T. (2002). Optimizing search engines using clickthrough data. KDD. https://doi.org/10.1145/775047.775067 — 說明如何把使用者點擊轉換為成對偏好資料，以訓練排序函數。
- Dehghani, M. et al. (2017). Neural ranking models with weak supervision. https://arxiv.org/abs/1704.08803 — 以自動產生而非人工判斷的標籤訓練神經排序器，減少了標註的需求。

### 綜述與教科書

- Liu, T.-Y. (2009). Learning to rank for information retrieval. Foundations and Trends in Information Retrieval. https://doi.org/10.1561/1500000016 — 綜述，把學習排序方法組織為逐點、成對與逐列三類。
- Burges, C. J. C. (2010). From RankNet to LambdaRank to LambdaMART: An overview. Microsoft Research Technical Report MSR-TR-2010-82. https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/ — 完整說明成對的 RankNet 成本如何發展為逐列的 LambdaRank 與基於樹的 LambdaMART。
- Lin, J., Nogueira, R. & Yates, A. (2020). Pretrained transformers for text ranking: BERT and beyond. https://arxiv.org/abs/2010.06467 — 神經文字排序綜述，把成對與逐點損失放在 Transformer 重新排序器的脈絡中說明。
