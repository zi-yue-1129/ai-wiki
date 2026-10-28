---
translation_reviewed: 2026-10-28
---

# 機率圖模型

機率圖模型（PGM）以圖形描述許多變數的聯合分布。每條邊或每個缺少的邊，都代表一項關於哪些變數彼此相依的陳述。圖形讓高維聯合分布得以緊湊表示，也讓推論能以圖上的局部計算來組織。本頁是[機率與貝氏方法](../index.md)的一部分。

## 概述

對 \(n\) 個二元變數的聯合分布，有 \(2^n-1\) 個自由參數，變數一多就難以處理。條件獨立假設可以把參數數量縮小。PGM 以圖形陳述這些假設，並把聯合分布分解成小的局部項。主要有兩大類：

- **有向**模型（貝氏網路）把聯合分布分解為 \(p(x)=\prod_i p(x_i\mid \mathrm{pa}(x_i))\)，其中 \(\mathrm{pa}(x_i)\) 是 \(x_i\) 的父節點。
- **無向**模型（馬可夫隨機場）把聯合分布分解為團勢函數，\(p(x)=\frac{1}{Z}\prod_c \psi_c(x_c)\)。

兩者表達相依的方式不同。有向圖適合描述因果或生成式的故事，無向圖則適合描述對稱的交互作用，例如影像中相鄰像素的平滑性。

## 關鍵概念

- **因式分解**：聯合分布是許多局部項的乘積，因此只需儲存局部的表或勢函數。
- **條件獨立**：在圖中，若給定某些變數，兩組變數互不相依，圖會把它們分隔開。分隔規則可直接從圖讀出這些陳述。
- **分割函數**：\(Z=\sum_x\prod_c\psi_c(x_c)\) 用來正規化無向模型。它通常難以計算，使學習與推論更困難。
- **因子圖**：一種二部圖，包含變數節點與因子節點。它為許多 PGM 方法共用的訊息傳遞演算法提供統一的語言（Kschischang 等人，2001）。
- **精確與近似推論**：圖小或呈樹狀時，精確方法可計算邊際分布或最可能的組態；其餘情況需要近似方法。

## 運作方式

有兩項核心任務。**推論**是在給定證據 \(e\) 的條件下，求邊際分布 \(p(x_i\mid e)\) 或最可能的指派。**學習**則是從資料估計各因子。對參數為 \(\theta\) 的模型，最大概似學習沿著對數概似的梯度前進，而梯度等於資料統計量與模型期望值之差。模型期望值需要推論，因此學習與推論密不可分。

以變數消去法做精確推論，其成本由圖的**樹寬**決定。在樹上，和積演算法（或[信念傳播](belief-propagation.md)）只需兩次掃描就能給出精確的邊際分布。圖中有迴路時，精確推論可能變得難以處理，此時需要近似。兩大近似族分別是抽樣（見[馬可夫鏈蒙地卡羅](../mcmc/index.md)）與以較簡單分布逼近後驗（見[變分推論](../variational-inference/index.md)）。

## 主要方法

- [信念傳播](belief-propagation.md)：在因子圖上的訊息傳遞。在樹上是精確的，在有迴路的圖上則是近似的。
- [隱馬可夫模型](hidden-markov-models.md)：用於序列的鏈狀有向模型。前向–後向演算法與 Viterbi 演算法是標準的推論工具（Rabiner，1989）。

此族中其他具名模型整理於下表。本節只有上述方法另有專頁。

| 類型 | 圖形 | 例子 |
|---|---|---|
| 貝氏網路 | 有向、無環 | 診斷、因果模型 |
| 馬可夫隨機場 | 無向 | 影像平滑、伊辛模型 |
| 隱馬可夫模型 | 帶隱藏狀態的有向鏈 | 語音辨識、基因定位 |
| 條件隨機場 | 無向，以輸入為條件 | 序列標註 |
| 線性高斯狀態空間模型 | 連續狀態的有向鏈 | 追蹤，以卡爾曼濾波器為代表（Kalman，1960） |

## 與其他頁面的連結

- [機率與統計](../../../math/probability-statistics/index.md)提供 PGM 所用的因式分解、條件獨立與最大概似的概念。
- [變分推論](../variational-inference/index.md)與[馬可夫鏈蒙地卡羅](../mcmc/index.md)是當精確推論成本過高時，兩種主要的近似推論方法。
- 上述有向鏈模型是此族中的序列成員。其判別式對應方法見[監督式學習](../../supervised/index.md)。

## 應用

- **醫療與專家系統**：貝氏網路編碼不確定的知識，並由觀察到的症狀計算診斷。Lauritzen 與 Spiegelhalter（1988）提出的局部計算方法，使大型網路的推論得以實用。
- **語音辨識**：隱馬可夫模型曾長期是標準的聲學模型（Rabiner，1989）。
- **追蹤與導航**：線性高斯狀態空間模型是卡爾曼濾波器的基礎（Kalman，1960）。
- **錯誤更正碼**：迭代解碼是因子圖上訊息傳遞的一個實例（Kschischang 等人，2001）。

## 開放問題

- 迴路圖上的近似推論沒有一般性的收斂或精確度保證。理論只涵蓋部分特殊情形，實務上仍多依賴實驗。
- 從資料學習圖的結構很困難，結構搜尋的成本也高。
- 精確推論的成本隨樹寬成長，因此圖的設計常需在表達力與可處理性之間取捨。

## 參考文獻

### 奠基性論文

- Lauritzen, S. L. & Spiegelhalter, D. J. (1988). Local computations with probabilities on graphical structures and their application to expert systems. *Journal of the Royal Statistical Society, Series B* 50(2), 157–194. https://doi.org/10.1111/j.2517-6161.1988.tb01721.x — 提出在圖模型上做精確推論的局部計算方法，並應用於專家系統。
- Kschischang, F. R., Frey, B. J. & Loeliger, H.-A. (2001). Factor graphs and the sum-product algorithm. *IEEE Transactions on Information Theory* 47(2), 498–519. https://doi.org/10.1109/18.910572 — 以因子圖統一描述訊息傳遞，包括和積規則。
- Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. *Proceedings of the IEEE* 77(2), 257–286. https://doi.org/10.1109/5.18626 — 隱馬可夫模型三大基本問題（評估、解碼與學習）的教學綜述，並含語音應用。
- Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering* 82(1), 35–45. https://doi.org/10.1115/1.3662552 — 線性高斯狀態空間模型的遞迴估計器。

### 綜述與教科書

- Yedidia, J. S., Freeman, W. T. & Weiss, Y. (2005). Constructing free-energy approximations and generalized belief propagation algorithms. *IEEE Transactions on Information Theory* 51(7), 2282–2312. https://doi.org/10.1109/tit.2005.850085 — 把信念傳播與 Bethe 自由能連結，並提出廣義信念傳播。
- Wainwright, M. J. & Jordan, M. I. (2008). Graphical models, exponential families, and variational inference. *Foundations and Trends in Machine Learning*. https://nowpublishers.com/article/Details/MAL-001 — 把圖模型、指數族與變分方法連結起來的專書。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；有圖模型與推論的章節。
