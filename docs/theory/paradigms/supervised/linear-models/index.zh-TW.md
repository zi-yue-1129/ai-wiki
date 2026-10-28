---
tags:
  - supervised learning
  - regression
  - classification
---

# 線性模型與廣義線性模型

線性模型以輸入特徵的加權和進行預測。它們是最古老的監督式學習器，至今仍是預設的基準模型，也是每一層神經網路的基本組成。

## 概觀

給定特徵 $x \in \mathbb{R}^d$，線性模型計算 $z = w^\top x + b$，再把 $z$ 通過連結函數。由於預測對每個權重都是單調的，擬合後的係數可以直接解讀，這使得這類模型在醫學、經濟學與心理學中很受歡迎。

## 主要模型

| 模型 | 輸出 | 損失／概似 |
|---|---|---|
| 普通最小平方法 | 實數 $z$ | 平方誤差（高斯雜訊） |
| Ridge（$\ell_2$） | 實數 | 平方誤差 $+ \lambda\lVert w\rVert_2^2$ |
| Lasso（$\ell_1$） | 實數，$w$ 稀疏 | 平方誤差 $+ \lambda\lVert w\rVert_1$ |
| Elastic net | 實數 | $\ell_1$ 與 $\ell_2$ 懲罰的混合 |
| 邏輯迴歸 | $p = \sigma(z)$ | 伯努利對數概似（交叉熵） |
| Softmax 迴歸 | 對 $K$ 個類別的分布 | 類別交叉熵 |
| Poisson 迴歸 | 非負計數，$\lambda = e^{z}$ | Poisson 對數概似 |
| 感知器 | 類別 sign$(z)$ | 由錯誤驅動的更新 |

這些都是**廣義線性模型（GLM）**的實例：目標變數服從指數族分布，其平均值與 $z$ 透過連結函數相連。

## 擬合方式

- 最小平方法有封閉解 $\hat w = (X^\top X + \lambda I)^{-1} X^\top y$。
- 邏輯迴歸與其他 GLM 是凸問題；可用迭代加權最小平方法、L-BFGS 或隨機梯度下降求解。
- $\ell_1$ 懲罰會把係數精確地壓成零，提供自動的特徵選擇；$\ell_2$ 懲罰則會把彼此相關的係數一起收縮。
- 貝氏觀點：ridge 是在 $w$ 上取高斯先驗時的 MAP 估計，lasso 則對應拉普拉斯先驗。

## 優點與限制

優點：訓練是凸的、理論完整、（邏輯迴歸）機率校準良好、速度快、容易稽核。限制：在給定的特徵空間中，只能畫出線性的決策邊界。常見的解法是特徵工程（多項式、樣條）、[核方法](../kernel-methods-svm/index.md)，或堆疊帶有非線性的層——也就是一個[神經網路](../../../deep-learning/index.md)。

## 與其他概念的連結

用來訓練單一線性單元的 delta 規則，與制約學習中的 Rescorla–Wagner 模型是同一個方程式（見[監督式學習](../index.md)）。線性探針（在凍結特徵上訓練的邏輯迴歸）是測試[自監督](../../self-supervised/index.md)表徵學到了什麼的標準方法。

## 參考文獻

### 開創性論文

- Tibshirani (1996), "Regression shrinkage and selection via the lasso", *JRSS B*. https://www.math.cuhk.edu.hk/~btjin/math6221/p7.pdf — 提出 lasso，即讓部分係數精確為零的 L1 懲罰。
- Kingma & Ba (2015), "Adam: a method for stochastic optimization", ICLR, arXiv:1412.6980 — Adam 最佳化器，是以梯度下降訓練邏輯模型與神經模型的預設選擇。
- Guo et al. (2017), "On calibration of modern neural networks", ICML, arXiv:1706.04599 — 顯示預測的機率可能校準不良，並提出以溫度縮放作為修正方法。

### 綜述與教科書

- Hastie、Tibshirani 與 Friedman，*The Elements of Statistical Learning*，Springer（2009），第 3–4 章。https://doi.org/10.1007/978-0-387-84858-7 — 對最小平方法、收縮與線性分類器的標準教科書式處理；作者提供免費 PDF。

### 講座與影片

- Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. *Journal of the Royal Statistical Society: Series B*, 58(1), 267–288. https://doi.org/10.1111/j.2517-6161.1996.tb02080.x — 提出 lasso，以 L1 懲罰的迴歸同時完成正則化與變數選取。

### 文章與文件

- Andrew Ng，Stanford CS229 講義。https://cs229.stanford.edu/main_notes.pdf — 線性迴歸、邏輯迴歸的推導，以及廣義線性模型的框架。

## 延伸學習

- StatQuest with Josh Starmer，關於邏輯迴歸與正規化的單元，YouTube。https://www.youtube.com/@statquest — 為初學者提供邏輯迴歸、ridge 與 lasso 的簡短視覺化解說。

## 延伸閱讀

- McCullagh & Nelder，*Generalized Linear Models*，第二版（1989）。https://doi.org/10.1201/9780203753736 — 廣義線性模型的標準教科書。此 DOI 為 Routledge 重印版（2019）。
