---
tags:
  - supervised learning
  - kernels
  - optimization
---

# 支援向量機與核方法

核方法藉由用相似度函數比較範例、而不是使用座標，讓線性演算法獲得非線性的能力。支援向量機（SVM）是其中最著名的例子。

## 最大間隔分類

對於可分的資料，SVM 會選出能使兩類最近點之間間隔 $2/\lVert w\rVert$ 最大的超平面 $w^\top x + b = 0$。若允許違反（軟間隔），則引入鬆弛變數 $\xi_i$：

$$
\min_{w,b,\xi}\ \tfrac12\lVert w\rVert^2 + C\sum_i \xi_i \quad \text{s.t. } y_i(w^\top x_i + b) \ge 1-\xi_i,\ \xi_i\ge 0.
$$

這等價於最小化帶有 $\ell_2$ 懲罰的 **hinge 損失** $\max(0, 1-y f(x))$。只有**支援向量**——位於間隔上或間隔內的點——會決定解。

## 核技巧

對偶問題只透過內積 $x_i^\top x_j$ 依賴資料。把內積換成核 $k(x_i,x_j)=\langle\phi(x_i),\phi(x_j)\rangle$，就等於隱式地在高維特徵空間中運算。

| 核函數 | 公式 | 用途 |
|---|---|---|
| 線性 | $x^\top x'$ | 高維稀疏的文本 |
| 多項式 | $(x^\top x' + c)^p$ | 特徵交互作用 |
| RBF／高斯 | $\exp(-\gamma\lVert x-x'\rVert^2)$ | 通用 |
| 字串、圖、樹核 | 針對結構設計 | 生物學、化學 |

有效的核必須是對稱且半正定的（Mercer 條件）。表示定理保證解是訓練點上核函數的加權和，$f(x)=\sum_i \alpha_i k(x_i,x)$。

## 相關的核方法

核嶺迴歸、核主成分分析、[高斯過程](../instance-based-and-probabilistic/index.md)（核加貝氏推論），以及用於[領域適應](../../transfer/index.md)的最大均值差異（MMD）。

## 限制與復興

訓練的成本隨範例數介於 $O(n^2)$ 與 $O(n^3)$ 之間成長，這是深度學習在大資料上取代 SVM 的原因。隨機傅立葉特徵與 Nyström 近似可以把核方法擴展到更大的規模。**神經正切核**（Jacot et al., 2018）顯示，以梯度下降訓練的無限寬網路，其行為就像一台核機器，從而連結了兩個領域。

## 參考文獻

### 開創性論文

- Boser, B. E., Guyon, I. M. & Vapnik, V. N. (1992). A training algorithm for optimal margin classifiers. *COLT*. https://doi.org/10.1145/130385.130401 — 第一篇核 SVM 論文，結合最大間隔與核技巧。
- Cortes & Vapnik (1995), "Support-vector networks", *Machine Learning* 20. https://link.springer.com/doi/10.1007/BF00994018 — 提出軟間隔 SVM，允許部分訓練錯誤。
- Jacot, Gabriel & Hongler (2018), "Neural tangent kernel", NeurIPS, arXiv:1806.07572 — 顯示以梯度下降訓練的無限寬網路，行為就像一台核機器。
- Niculescu-Mizil & Caruana (2005), "Predicting good probabilities with supervised learning", ICML. https://mlanthology.org/icml/2005/niculescumizil2005icml-predicting — 比較包括 SVM 在內的各種分類器，產生校準機率的能力。

### 綜述與教科書

（本頁未查核任何綜述或教科書。）

### 講座與影片

- Yaser Abu-Mostafa，*Learning From Data*，Caltech 線上課程（2012），關於支援向量機與核的講座。https://work.caltech.edu/telecourse — 免費的大學課程，從學習理論出發建構 SVM 與核方法。

### 文章與文件

- Belkin, Hsu, Ma & Mandal (2019), "Reconciling modern machine-learning practice and the bias–variance trade-off", *PNAS*, arXiv:1812.11118 — 說明核模型與神經模型如何內插訓練資料，同時仍能泛化。

## 延伸閱讀

- Schölkopf & Smola，*Learning with Kernels*，MIT Press（2002）。未查核免費連結。
- Platt (1999), "Probabilistic outputs for support vector machines", in *Advances in Large Margin Classifiers*。未查核免費連結。
