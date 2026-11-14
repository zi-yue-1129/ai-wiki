---
translation_reviewed: 2026-11-04
---

# ComplEx（複數嵌入）

ComplEx 是一種知識圖譜嵌入模型，把實體與關係表示為複數值向量，並以埃爾米特積（Hermitian product）為三元組打分。它的主要目的是建模非對稱關係，而這是以平移為基礎的 [TransE](transe.md) 較難處理的。本頁是[知識圖譜與知識表示](index.md)的一部分。

## 概述

連結預測會為三元組缺少的一端排序候選實體，TransE 的設定即是如此（Bordes 等人，2013）。許多早期嵌入模型以實數值的雙線性乘積打分。對這類模型而言，(h, r, t) 與 (t, r, h) 的分數常常相同，因此若不加額外機制，就無法表示「是…的父母」這類非對稱關係。Trouillon 等人（2016）指出，複數能以很小的額外成本解決這個問題：當關係的嵌入具有非零虛部時，兩個方向的分數就會不同。

## 關鍵概念

- **複數嵌入**：每個實體與關係都是一組複數向量，其實部與虛部由資料學得。
- **埃爾米特積**：主體的一個分量、關係的一個分量與客體分量共軛的乘積之和，其實部即為分數。
- **非對稱性**：當 (h, r, t) 成立而 (t, r, h) 不成立時，關係即為非對稱。模型需要非實數的關係向量才能表示這一點。
- **帶正則化的邏輯損失**：訓練時讓真實三元組的分數高於損壞的三元組，並對嵌入施加 L2 懲罰。

## 運作方式

對三元組 (h, r, t)，其中向量都在 $\mathbb{C}^k$ 中，ComplEx 使用的分數為

\[
\phi(h,r,t)=\operatorname{Re}\Big(\sum_{i=1}^{k} h_i\, r_i\, \overline{t_i}\Big),
\]

其中 $\overline{t_i}$ 是 $t_i$ 的共軛複數。令 $r = r_R + i\,r_I$，分數可拆成若干實數項，其中 $r_I$ 與主體和客體的交叉項相乘。當 $r$ 為實數時，分數對 $h$ 與 $t$ 對稱；當 $r$ 具有非零虛部時，交換主體與客體會改變分數，因此模型能表示非對稱性。

訓練遵循嵌入模型的常見做法。真實三元組與以替換主體或客體得到的損壞三元組配對，模型以邏輯損失與 L2 正則項擬合，並採用基於梯度的最佳化（Trouillon 等人，2016）。由於分數對嵌入是雙線性的，其梯度也很容易計算。

## 主要方法

- [TransE](transe.md)：簡單且快速的平移模型，但對對稱關係而言，其關係向量會被迫趨近於零。ComplEx 保留相同的目標，並把分數改為複數乘積。
- 其他具有不同評分函數的嵌入模型，在 Wang 等人（2017）與 Nickel 等人（2016）的綜述中有所整理。

## 結果與限制

- 論文在標準連結預測基準上，相較當時可用的模型報告了強勁的結果（Trouillon 等人，2016）。確切數字請以論文的表格為準，不應採信本頁的摘要。
- 表示非對稱性使每個維度的實數參數數量加倍，因此增加記憶體與訓練時間。
- 雙線性分數並不直接表示關係的組合，因此多跳推理需要其他工具。
- 結果取決於基準與評估協定。某些基準含有反向關係，使任務比表面上容易（Dettmers 等人，2018）。

## 應用

- **補全大型知識圖譜**：為搜尋與問答預測缺少的事實。
- **具有有向關係的圖**：推薦或生物醫學圖中，「治療」或「導致」等關係依方向而定。

## 與其他頁面的連結

- [TransE](transe.md) 與 ComplEx 有相同的連結預測目標，並在對稱關係上形成有用的對照。
- [神經符號 AI](../neuro-symbolic/index.md) 探討把嵌入式補全與邏輯約束結合的可能。
- [知識圖譜概覽](index.md) 把 ComplEx 置於各種嵌入方法之中。

## 開放問題

- 嵌入維度如何與其能捕捉的關係類型取捨，目前尚未完全理解。
- 嵌入模型是轉導式的：若不重新訓練，就無法為訓練時未見過的實體安置向量。
- 基準的設計仍會影響哪個模型看起來最好（Dettmers 等人，2018）。

## 參考文獻

### 奠基性論文

- Trouillon, T., Welbl, J., Riedel, S., Gaussier, É. & Bouchard, G. (2016). Complex embeddings for simple link prediction. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/trouillon16.html — 提出 ComplEx 與用於非對稱關係的複數埃爾米特分數。
- Bordes, A., Usunier, N., Garcia-Duran, A., Weston, J. & Yakhnenko, O. (2013). Translating embeddings for modeling multi-relational data. In *Advances in Neural Information Processing Systems* 26. https://proceedings.neurips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html — ComplEx 所延續的 TransE 基準設定。
- Dettmers, T., Minervini, P., Stenetorp, P. & Riedel, S. (2018). Convolutional 2D knowledge graph embeddings. In *Proceedings of the AAAI Conference on Artificial Intelligence* 32. https://arxiv.org/abs/1707.01476 — 指出廣泛使用的基準含有反向關係的洩漏。

### 綜述與教科書

- Nickel, M., Murphy, K., Tresp, V. & Gabrilovich, E. (2016). A review of relational machine learning for knowledge graphs. *Proceedings of the IEEE* 104(1), 11–33. https://doi.org/10.1109/JPROC.2015.2483592 — 回顧關係嵌入模型，包括雙線性模型一族。
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). Knowledge graph embedding: a survey of approaches and applications. *IEEE Transactions on Knowledge and Data Engineering* 29(12), 2724–2743. https://doi.org/10.1109/TKDE.2017.2754499 — 綜述嵌入方法及其評分函數。
- Hogan, A. et al. (2021). Knowledge graphs. *ACM Computing Surveys* 54(4), 1–37. https://doi.org/10.1145/3447772 — 把嵌入模型置於知識圖譜研究的脈絡中。
