---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - High-order Polynomial Projection Operators
  - HiPPO
  - 高階多項式投影運算子
tags:
  - state-space models
  - long-range memory
  - online function approximation
translation_reviewed: 2026-10-28
---

# HiPPO：高階多項式投影

HiPPO 是 High-order Polynomial Projection Operators（高階多項式投影運算子）的縮寫，是一個建構循環記憶的框架，能把輸入的歷史以一組多項式係數的向量儲存起來。Gu 等人在 2020 年的論文 "HiPPO: Recurrent Memory with Optimal Polynomial Projections" 中提出了它。它的狀態矩陣是結構化狀態空間模型長程記憶的基礎。

## 問題

序列模型必須用有限的儲存空間，摘要輸入的完整歷史，並且隨時線上更新這份摘要。循環網路有梯度消失的問題。LSTM 與 GRU 等門控設計，以及 LMU 等較早的記憶單元，往往需要對序列長度或時間尺度的先驗知識，而且許多設計缺乏對長程依賴的保證。

## 核心想法

論文把記憶視為線上的函數逼近。輸入 \(f\) 的歷史會依一個隨時間變化的測度 \(\mu^{(t)}\)（它為過去的時刻加權）投影到多項式基底上。係數 \(c(t) \in \mathbb{R}^N\) 依一個線性常微分方程演化，此方程可離散化為遞迴。論文研究三種測度：

- **LegT**（平移勒讓德）在長度為 \(\theta\) 的滑動窗口上給予均勻權重，因此 \(\theta\) 是一個超參數。
- **LagT**（平移拉蓋爾）對過去給予指數遞減的權重。
- **LegS**（尺度化勒讓德）對整段歷史 \([0, t]\) 給予均勻權重。它是論文的主要測度，不需要窗口長度。

## 方程式或演算法

對於 LegS 測度，係數滿足

\[
\frac{dc}{dt} = -\frac{1}{t}\,A\,c(t) + \frac{1}{t}\,B\,f(t),
\]

其中 \(A_{nk} = \sqrt{2n+1}\sqrt{2k+1}\)（當 \(n > k\)）、\(A_{nk} = n+1\)（當 \(n = k\)）、\(A_{nk} = 0\)（當 \(n < k\)），且 \(B_n = \sqrt{2n+1}\)。以前向歐拉法離散化，得到遞迴

\[
c_{k+1} = \left(I - \tfrac{1}{k}A\right) c_k + \tfrac{1}{k}\,B\,f_k .
\]

論文也給出 LegT 與 LagT 的矩陣，實驗中則使用雙線性離散化。

## 結果

在排列後的 MNIST 上，論文報告 HiPPO-LegS 達到 98.3%，高於所列的基線，包括 Transformer 的 97.9% 與 LMU 的 97.15%。論文註明，其 HiPPO 數字是三個隨機種子的驗證準確率平均，而它所比較的文獻數字是測試準確率。在時間尺度偏移或資料缺失的 Character Trajectories 任務上，HiPPO-LegS 在兩種時間尺度偏移下分別得到 88.8% 與 90.1%，在兩種資料缺失設定下分別得到 94.5% 與 94.9%。摘要指出，它在準確率上優於 RNN 與神經 ODE 基線「25-40%」。在長度 200 的複製任務上，LegS 幾乎完美解決此任務，而 LegT 對其窗口長度非常敏感。論文的 C++ 實作在單一 CPU 核心上每秒可處理 470,000 個時間步。

## 限制

平移測度需要先驗知識。LegT 需要正確的窗口長度 \(\theta\)，LagT 與 LegT 都需要步長 \(\Delta t\)。LegS 移除了窗口，但論文的效率結果只對 LegS 證明，作者推測它可推廣到其他測度。LegT 的更新會引入逼近誤差，因為它假設目前的係數足夠精確，能還原窗口起點的輸入。在此設定下，前向歐拉法不如雙線性法精確。作者把大規模任務（如語音、影片與強化學習）以及整合到其他模型，列為未來工作。論文沒有專門的限制一節，因此這些觀點取自其討論。

## 相關連結

HiPPO-LegS 是[結構化狀態空間](../index.md)家族的起始矩陣。[S4](../s4/index.md) 以正規加低秩的形式使用它，[S4D](../s4d/index.md) 取其對角部分，[S5](../s5/index.md) 則使用對角化的 HiPPO-N 矩陣。[線性循環單元](../linear-recurrent-units/index.md) 使用另一種環狀初始化。更廣的[狀態空間模型](../../index.md)家族涵蓋整個設計。HiPPO 所處理的記憶問題，也是 [RNN](../../../rnn/index.md) 家族所研究的問題，而依輸入而變的後繼設計則見[選擇性狀態空間](../../selective-state-spaces/index.md)。

## 未解問題與更多變體

- **測度的選擇。** LegS 移除了窗口超參數，但其效率結果並未對其他測度證明，作者把這點留作推測。
- **離散化。** 此處前向歐拉法不如雙線性法精確，離散化對其他任務的影響尚未刻劃。
- **規模。** 論文的實驗規模很小，語音、影片與強化學習被列為未來工作。

## 參考文獻

### 開創性論文

- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — 為狀態矩陣提供長程記憶的 HiPPO 框架。
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4，具結構化狀態空間，能高效處理很長的序列。
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". arXiv:2206.11893 — 仔細初始化的複數對角狀態矩陣，能以較簡單的實作匹敵 S4。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". arXiv:2208.04933 — S5，帶有平行掃描的對角狀態空間層。
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — 仔細設計的線性循環單元，在長序列基準上能與 SSM 匹敵。
