---
translation_reviewed: 2026-10-28
---

# 耦合振盪循環神經網路（coRNN）

coRNN 是一種循環神經網路，其隱藏單元是耦合、阻尼與受迫振子方程式的離散化形式。Rusch 與 Mishra（2021）提出它，用於學習長序列。它是一種工程架構，而非大腦模型，但它是本 wiki 中[神經振盪與同步](../index.md)這些想法最直接的人工對應。

## 概述

在長序列中，沿著許多循環步驟反向傳播的梯度往往會消失或爆炸。常見的解法是門控，如 LSTM（Hochreiter 與 Schmidhuber，1997）。Rusch 與 Mishra 採取不同的路線。耦合、受迫且有阻尼的振子，可以讓其狀態變數保持有界，同時仍能產生豐富的輸出。因此他們以這類振子建構 RNN，並在所列假設下證明其隱藏狀態與梯度的界限。

## 關鍵概念

- **阻尼**：從振子中逐漸移除能量的摩擦。在 coRNN 中由參數 $\epsilon$ 設定。
- **振盪頻率**：由參數 $\gamma$ 與循環權重矩陣 $W$ 的對角線設定。
- **速度變數**：隱藏狀態的時間導數，在離散網路中作為第二個狀態攜帶。
- **梯度穩定性**：長序列中梯度既不爆炸也不消失的性質。這些界限是論文的主要理論主張。
- **IMEX 離散化**：一種時間步進方案，對某些項採隱式處理、對其他項採顯式處理。在 coRNN 中它決定阻尼如何套用。

## 運作方式

起點是每個隱藏單元 $y$ 的二階方程式，活化函數為 $\sigma = \tanh$：

$$\ddot{y} = \sigma\big(W y + \tilde{W}\dot{y} + V u + b\big) - \gamma y - \epsilon \dot{y}.$$

其中 $u(t)$ 為輸入，$W$、$\tilde W$ 與 $V$ 為權重矩陣，$b$ 為偏置。參數 $\gamma$ 設定振盪頻率，$\epsilon$ 設定阻尼。論文將 $W$ 的對角線與頻率相連，將 $\tilde W$ 的對角線與阻尼相連，而非對角元素則耦合各單元。令速度 $z = \dot y$，便得到一階系統。論文以時間步長 $\Delta t$ 將其離散化：

$$z_n = z_{n-1} + \Delta t\,\sigma\big(W y_{n-1} + \tilde{W} z_{n-1} + V u_n + b\big) - \Delta t\,\gamma\, y_{n-1} - \Delta t\,\epsilon\, z_{\bar n}, \qquad y_n = y_{n-1} + \Delta t\, z_n,$$

其中 $\bar n$ 為 $n$（隱式阻尼）或 $n-1$（顯式阻尼）。兩個版本的差別只在於阻尼項的處理方式。

運作流程如下。

1. 選擇時間步長 $0 < \Delta t < 1$ 與初始狀態。
2. 對每個輸入 $u_n$，先更新速度 $z_n$，再以新速度更新狀態 $y_n$。論文的主要描述省略了讀出用的仿射層。

## 結果

論文的實驗使用了為測試長程依賴而選擇的基準。以下數字取自其表格與文字。

- **加法問題。** 網路要在長度為 $T$ 的序列中，把兩個被標記的數字相加。論文報告，在 $T = 2000$ 時只有 coRNN 與 expRNN 的誤差低於基準；在 $T = 5000$ 時，coRNN 仍能快速收斂，而 expRNN 無法穩定地超越基準。
- **序列 MNIST 與排列序列 MNIST。** 論文報告，使用 128 個隱藏單元時，sMNIST 與 psMNIST 的測試準確率分別為 99.3% 與 96.6%；使用 256 個單元時分別為 99.4% 與 97.3%。在 sMNIST 上它領先所列的循環基準，在 psMNIST 上則接近最佳。
- **噪聲填充 CIFAR-10。** 使用 128 個隱藏單元時，coRNN 達到 59.0%，是論文表格中所列模型的最高值。所列的最佳門控反對稱 RNN 為 54.7%。

論文還報告了 IMDB 情感分析、人類活動辨識與 Lorenz 96 預測的競爭性結果。

## 限制

- **可比，但不是全面較優。** 論文主張的是具競爭力的表現，而非在所有任務上勝出。在加法問題上，expRNN 在 $T = 2000$ 時也超越基準；在 psMNIST 上，一個基準在 128 個單元時略高。
- **生物連結較鬆散。** 論文從生物學動機出發設計，但明確略去了許多神經細節。兩者的相似是數學結構上的，而非解剖上的。
- **參數很重要。** 穩定性界限在論文所列假設下成立。實際上，$\gamma$、$\epsilon$ 與 $\Delta t$ 會影響行為，作者以隨機搜尋來調整它們。
- **任務組合較窄。** 基準多為分類與預測任務。論文未評估大規模語言模型，因此其結果不能直接推及 Transformer 占主導的場景。

## 開放問題

- **振盪是否為關鍵要素？** 反對稱 RNN 也是一種基於穩定常微分方程的設計（Chang 等人，2019）。消融研究可以檢驗，振盪形式在穩定性之外是否真的重要。
- **學到的頻率是否有意義？** 訓練後的網路是否學到與[主題頁](../index.md)所討論頻帶相似的頻率結構，仍是開放問題。
- **它與狀態空間模型的關係為何？** 兩者都把連續時間動力學離散化，用於序列建模。比較見[狀態空間模型](../../../theory/models/ssm/index.md)。

## 參考文獻

### 開創性論文

- Rusch, T. K. & Mishra, S. (2021). Coupled Oscillatory Recurrent Neural Network (coRNN): An accurate and (gradient) stable architecture for learning long time dependencies. *ICLR*. https://arxiv.org/abs/2010.00951 — 提出 coRNN，並推導其隱藏狀態梯度的界限。
- Hochreiter, S. & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — 提出 LSTM，即長程序列模型常用的門控基準。

### 綜述與教科書

- Strogatz, S. H. (2000). From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators. *Physica D*. https://doi.org/10.1016/S0167-2789(00)00094-4 — 綜述 Kuramoto 耦合振子模型與同步的出現。
- Buzsáki, G. & Draguhn, A. (2004). Neuronal oscillations in cortical networks. *Science*. https://doi.org/10.1126/science.1099745 — 綜述皮質網路振盪，是振子模型的生物學背景。

### 文章與文件

- Chang, B., Chen, M., Haber, E. & Chi, E. H. (2019). AntisymmetricRNN: A Dynamical System View on Recurrent Neural Networks. arXiv. https://arxiv.org/abs/1902.09689 — 提出一種反對稱循環網路，其基於穩定的常微分方程。
- Erichson, N. B., Azencot, O., Queiruga, A., Hodgkinson, L. & Mahoney, M. W. (2020). Lipschitz Recurrent Neural Networks. arXiv. https://arxiv.org/abs/2006.12070 — 提出一種具穩定性條件的循環單元，立基於動力系統理論。
