---
tags:
  - supervised learning
  - ensembles
  - tabular data
---

# 決策樹與集成方法

樹狀方法以簡單的規則把輸入空間切分成若干區域，而集成方法則把許多棵樹組合起來。在表格資料上，梯度提升樹通常仍是最強的實務選擇。

## 決策樹

樹會遞迴地選出最能分開標籤的特徵與門檻，依據的是不純度量：分類時使用 Gini 不純度 $1-\sum_k p_k^2$ 或熵 $-\sum_k p_k\log p_k$，迴歸時使用變異數（CART，Breiman et al. 1984；ID3／C4.5，Quinlan）。單棵的深樹偏差低、變異高；剪枝或限制深度可以加以控制。樹不需要特徵縮放，能處理混合型態的資料與缺失值，並且能給出易讀的規則。

## 裝袋法與隨機森林

**裝袋法（bagging）**在自助重抽樣（bootstrap）的資料上訓練許多棵樹並加以平均，可以降低變異。**隨機森林**（Breiman, 2001）還會在每次分裂時隨機選取一部分特徵，使各棵樹之間的相關性降低。袋外（out-of-bag）樣本可以免費提供驗證估計。森林穩健、幾乎不需調參，也很少嚴重過擬合。

## 提升法

提升法依序建立樹，每一棵都在修正目前集成的錯誤。

- **AdaBoost** 會對被誤分類的樣本重新加權。
- **梯度提升**（Friedman, 2001）讓每棵新樹擬合損失函數的負梯度，因此 $F_m = F_{m-1} + \eta\, h_m$。
- **XGBoost、LightGBM、CatBoost** 加入二階資訊、正規化、基於直方圖的分裂，以及對類別特徵更好的處理。

| 方法 | 降低的對象 | 樹的特性 | 調參成本 |
|---|---|---|---|
| 裝袋／森林 | 變異 | 深、彼此獨立 | 低 |
| 提升 | 偏差（與部分變異） | 淺、依序建立 | 中 |

## 堆疊與其他集成

堆疊法在多個異質的基礎模型之預測上訓練一個元模型。平均多個神經網路（深度集成）也是估計不確定性的強大基準。

## 與其他概念的連結

為什麼在許多表格任務上，樹模型能勝過深度網路？Grinsztajn et al.（2022）指出，原因在於目標函數不規則、特徵資訊量低的情況下，樹模型較為穩健。樹的集成在金融、醫療風險評分與推薦排序中被廣泛使用；見[應用領域](../../../../applications/index.md)。

## 參考文獻

### 開創性論文

- Quinlan, J. R. (1986). Induction of decision trees. *Machine Learning*, 1(1), 81–106. https://doi.org/10.1007/BF00116251 — ID3 演算法，依資訊增益建立決策樹。
- Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. https://mlanthology.org/mlj/2001/breiman2001mlj-random — 結合隨機特徵選取的裝袋樹，以及袋外誤差估計。
- Friedman (2001), "Greedy function approximation: a gradient boosting machine", *Annals of Statistics* 29(5). https://doi.org/10.1214/AOS/1013203451 — 把梯度提升推導為函數空間中的梯度下降。
- Ke et al. (2017), "LightGBM: a highly efficient gradient boosting decision tree", NeurIPS. https://neurips.cc/virtual/2017/poster/9099 — 基於直方圖的分裂與逐葉生長，使大資料上的提升更快。
- Prokhorenkova et al. (2018), "CatBoost: unbiased boosting with categorical features", NeurIPS. https://proceedings.neurips.cc/paper/2018/hash/14491b756b3a51daac41c24863285549-Abstract.html — 有序提升與目標統計量，在不洩漏的前提下處理類別特徵。

### 綜述與教科書

- Hastie、Tibshirani 與 Friedman，*The Elements of Statistical Learning*，Springer（2009），第 9、10、15 章。https://doi.org/10.1007/978-0-387-84858-7 — 深入介紹樹、提升與隨機森林；作者提供免費 PDF。

### 講座與影片

- Friedman, J. H. (2001). Greedy function approximation: a gradient boosting machine. *Annals of Statistics*, 29(5), 1189–1232. https://doi.org/10.1214/aos/1013203451 — 提出梯度提升機，以函數空間中的梯度下降逐步加入弱學習器。

### 文章與文件

- Grinsztajn, Oyallon & Varoquaux (2022), "Why do tree-based models still outperform deep learning on tabular data?", NeurIPS, arXiv:2207.08815 — 基準測試與分析，說明為什麼在表格資料上樹的集成常勝過神經網路。

## 延伸學習

- StatQuest with Josh Starmer，關於隨機森林與梯度提升的單元，YouTube。https://www.youtube.com/@statquest — 以動畫逐步說明樹如何建立與組合。

## 延伸閱讀

- Chen & Guestrin (2016), "XGBoost: a scalable tree boosting system", KDD。未查核連結。
