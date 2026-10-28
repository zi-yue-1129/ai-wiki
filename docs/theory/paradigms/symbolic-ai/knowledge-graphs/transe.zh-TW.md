---
translation_reviewed: 2026-10-28
---

# TransE

TransE 是一種知識圖譜嵌入模型，把每個關係表示為一個平移向量。當主體嵌入加上關係嵌入後接近客體嵌入時，三元組 (h, r, t) 就被視為合理。本頁是[知識圖譜與知識表示](index.md)的一部分。

## 概述

知識圖譜是不完整的，缺少的事實要從圖的其餘部分來預測。TransE 把這件事視為學習向量。每個實體與關係在向量空間中都有一個點，一個三元組的分數取決於關係能否把主體平移到客體附近。這個模型簡單、參數少，且能擴展到大型圖（Bordes 等人，2013）。

## 關鍵概念

- **嵌入**：每個實體與每個關係學得的向量。
- **平移**：關係把主體向量移到客體向量的想法，即 \(\mathbf{h}+\mathbf{r}\approx\mathbf{t}\)。
- **損壞的三元組**：把真實三元組的主體或客體替換為隨機實體所產生的負例。
- **連結預測**：給定主體與關係，為候選客體排序（反向亦然），並衡量真實實體的排名。

## 運作方式

對三元組 \((h,r,t)\)，分數為距離 \(d(\mathbf{h}+\mathbf{r},\mathbf{t})\)，通常使用 L1 或 L2 範數。訓練時最小化基於間隔的排序損失，

\[
\mathcal{L}=\sum_{(h,r,t)\in S}\sum_{(h',r,t')\in S'}\big[\gamma+d(\mathbf{h}+\mathbf{r},\mathbf{t})-d(\mathbf{h}'+\mathbf{r},\mathbf{t}')\big]_+,
\]

其中 \(S\) 為真實三元組，\(S'\) 為損壞的三元組，\(\gamma\) 為間隔，\([x]_+=\max(0,x)\)。訓練過程中會正規化實體嵌入，損失則促使真實三元組的分數比損壞的三元組至少近 \(\gamma\)。

## 變體

- **關係專屬投影**：讓每個關係擁有自己的空間，使同一實體在不同關係下可以有不同的表示。
- **複數值與旋轉關係**：針對 TransE 在非對稱關係上的弱點而設計（Trouillon 等人，2016）。

## 結果與限制

- TransE 在標準連結預測基準上具競爭力，且訓練快速（Bordes 等人，2013）。
- 它不能很好地表示對稱關係，因為 \(\mathbf{h}+\mathbf{r}\approx\mathbf{t}\) 與 \(\mathbf{t}+\mathbf{r}\approx\mathbf{h}\) 同時成立，會迫使 \(\mathbf{r}\approx\mathbf{0}\)。
- 對一對多與多對多的關係，同一主體與關係的不同客體會被拉向同一點，這不利於排序。2013 年的論文分析了這些關係類型。
- 模型只有單一平移，若不加以擴充，就無法捕捉組合或層級結構。

## 應用

- **補全知識圖譜**：為大型公開與企業圖譜預測缺少的事實。
- **問答**：以向量運算檢索符合查詢的實體。
- **推薦**：在包含關係類型的圖中為使用者與項目的連結打分。

## 開放問題

- 平移是否為多數關係類型的正確歸納偏置，目前尚無定論；更豐富的模型也未必一致地勝過它。
- 評估依賴的基準切分可能洩漏反向關係，因此報告的進展需要仔細檢驗。

## 參考文獻

### 奠基性論文

- Bordes, A., Usunier, N., Garcia-Duran, A., Weston, J. & Yakhnenko, O. (2013). Translating embeddings for modeling multi-relational data. In *Advances in Neural Information Processing Systems* 26. https://proceedings.neurips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html — 提出 TransE、基於間隔的訓練以及關係類型分析。
- Trouillon, T., Welbl, J., Riedel, S., Gaussier, É. & Bouchard, G. (2016). Complex embeddings for simple link prediction. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/trouillon16.html — 建模非對稱關係，這是 TransE 處理得不好的地方。

### 綜述與教科書

- Nickel, M., Murphy, K., Tresp, V. & Gabrilovich, E. (2016). A review of relational machine learning for knowledge graphs. *Proceedings of the IEEE* 104(1), 11–33. https://doi.org/10.1109/JPROC.2015.2483592 — 回顧平移與其他關係嵌入模型。
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). Knowledge graph embedding: a survey of approaches and applications. *IEEE Transactions on Knowledge and Data Engineering* 29(12), 2724–2743. https://doi.org/10.1109/TKDE.2017.2754499 — 綜述 TransE 及其延伸。
- Hogan, A. et al. (2021). Knowledge graphs. *ACM Computing Surveys* 54(4), 1–37. https://doi.org/10.1145/3447772 — 把嵌入模型置於知識圖譜研究的脈絡中。
