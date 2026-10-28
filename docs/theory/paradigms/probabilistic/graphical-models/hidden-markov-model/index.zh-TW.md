---
translation_reviewed: 2026-10-28
---

# 隱馬可夫模型

隱馬可夫模型（hidden Markov model, HMM）是一種處理序列的潛變數模型。隱藏狀態隨時間依馬可夫鏈變化，每個狀態再發出一個觀測。它是處理序列最簡單的有向圖模型，也是[機率圖模型](../index.md)總覽中的方法之一。

## 概述

許多訊號是由不可直接觀察的過程產生的序列，例如語音由變化中的聲道產生。HMM 以兩條規則描述這類過程：一條是隱藏狀態如何變化的轉移規則，另一條是每個狀態產生什麼觀測的發射規則。隱藏狀態從不被直接觀察，因此模型只能透過觀測來擬合與使用。

Baum 等人（1970）給出後來稱為 Baum–Welch 的估計程序，Rabiner 的教學文章（1989）則讓這個模型廣為人知。HMM 成為語音辨識的主流方法，Gales 與 Young（2008）描述了這個基本模型如何被改良成大詞彙系統。由於 HMM 就是鏈上的貝氏網路，它的演算法是[主題頁](../index.md)中一般方法的特例。

## 核心概念

- **隱藏狀態** \(z_t\)：時間 \(t\) 時不可觀察的狀態，取 \(K\) 個離散值之一。
- **觀測** \(x_t\)：在時間 \(t\) 所看到的東西。發射可以是離散符號，也可以是連續密度。
- **轉移矩陣** \(A\)，其中 \(a_{ij} = p(z_t = j \mid z_{t-1} = i)\)，以及**初始分布** \(\pi\)。
- **發射分布** \(b_j(x) = p(x \mid z = j)\)。
- **三個問題**（Rabiner, 1989）：評估，即計算一段序列的概似；解碼，即找出最可能的隱藏路徑；學習，即估計參數。

## 運作方式

對於長度為 \(T\) 的序列，狀態與觀測的聯合分布是一個鏈狀的乘積：

\[
p(z_{1:T}, x_{1:T}) = \pi(z_1)\,b_{z_1}(x_1)\prod_{t=2}^{T} a_{z_{t-1} z_t}\, b_{z_t}(x_t).
\]

**評估**使用前向演算法，其中 \(\alpha_t(j) = p(x_{1:t}, z_t = j)\)：

1. 設定 \(\alpha_1(j) = \pi_j\, b_j(x_1)\)。
2. 對之後的每一步，計算 \(\alpha_t(j) = b_j(x_t)\sum_i \alpha_{t-1}(i)\, a_{ij}\)。
3. 概似為 \(\sum_j \alpha_T(j)\)。這兩步的成本都是 \(O(K^2 T)\)。

**解碼**使用 Viterbi 演算法。它把對前一狀態的求和換成求最大值，記錄回溯指標，並從最佳的最終狀態回溯。

**學習**使用 Baum–Welch 演算法，它是期望最大化（EM）的一個實例。E 步執行前向與後向遍歷，得到狀態與轉移的後驗分布。M 步再用這些期望值重新估計 \(\pi\)、\(A\) 與發射參數。這個程序會收斂到局部最優解，結果取決於起始值。

## 實驗結果

Rabiner 的教學文章本身沒有基準測試。Gales 與 Young（2008）指出，在他們回顧的時期，以 HMM 為基礎的大詞彙連續語音辨識系統幾乎是所有此類系統的基礎。他們的案例研究把這些系統應用於廣播新聞與對話語音的轉寫，並說明要達到最先進的準確率，需要大量工程努力，例如判別式參數估計與適應。

## 限制

- **記憶很短。**下一個狀態只依賴目前狀態。較長距離的結構必須編碼在更大的狀態空間中，而這個空間會迅速變大。
- **觀測的條件獨立。**每個觀測只依賴其目前狀態，因此相鄰觀測之間的相關性需要額外建模。
- **生成式訓練。**最大概似擬合的是聯合分布，即使任務只是預測標籤也是如此。判別式替代方法因此被發展出來，例如 Collins（2002）的感知器式訓練，它在詞性標註與分塊上，相較最大熵標註器有所進步。
- **局部最優。**EM 訓練取決於起始值。

## 開放問題

- 狀態數與轉移結構能否從資料中學習，而不是靠人工固定？
- HMM 系統的成功，有多少來自馬可夫結構，又有多少來自周圍的工程？神經序列模型如今已取代了這套結構的大部分，而兩者的比較尚無定論。
- 因子 HMM（Ghahramani & Jordan, 1997）描述多條彼此交互的隱藏鏈。這類結構能在多大程度上自動學習？

## 參考文獻

### 開創性論文

- Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. *Proceedings of the IEEE*. https://doi.org/10.1109/5.18626 — 定義 HMM 的評估、解碼與學習問題，並給出前向、Viterbi 與 Baum–Welch 演算法的教學文章。
- Baum, L. E., Petrie, T., Soules, G. & Weiss, N. (1970). A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains. *The Annals of Mathematical Statistics*. https://doi.org/10.1214/aoms/1177697196 — 提出馬可夫鏈機率函數的估計程序，即今日所稱的 Baum–Welch。
- Viterbi, A. (1967). Error bounds for convolutional codes and an asymptotically optimum decoding algorithm. *IEEE Transactions on Information Theory*. https://doi.org/10.1109/TIT.1967.1054010 — 提出卷積碼的解碼演算法，今日用於在 HMM 中找出最佳隱藏路徑。

### 綜述與教科書

- Gales, M. & Young, S. (2008). *The Application of Hidden Markov Models in Speech Recognition*. Foundations and Trends in Signal Processing. https://doi.org/10.1561/2000000004 — 回顧以 HMM 為基礎的大詞彙語音辨識，以及達到最先進準確率所需的改進。

### 文章與文件

- Ghahramani, Z. & Jordan, M. I. (1997). Factorial Hidden Markov Models. *Machine Learning*. https://doi.org/10.1023/A:1007425814087 — 把 HMM 擴展為多條並行演化的隱藏鏈，這些鏈透過觀測彼此交互。
- Collins, M. (2002). Discriminative Training Methods for Hidden Markov Models: Theory and Experiments with Perceptron Algorithms. *EMNLP 2002*. https://aclanthology.org/W02-1001/ — 以經 Viterbi 解碼的感知器式更新訓練標註模型，並與最大熵標註器比較。
