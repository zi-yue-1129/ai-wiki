---
translation_reviewed: 2026-10-28
---

# 稀疏編碼（Olshausen & Field, 1996）

自然影像小塊可以用少數學得的基底函數的稀疏組合來描述。

## 問題

初級視覺皮質（V1）的神經元為何對特定位置的定向邊緣有反應？

## 核心想法

將自然影像小塊表示為少數基底函數的加權和，且係數稀疏。基底函數由無標籤的影像學得。

## 方程式或演算法

對每個影像小塊，求係數 \(a_i\) 與基底函數 \(\phi_i\)，使下式最小化：

\[
E = \Big\| I - \sum_i a_i \phi_i \Big\|^2 + \lambda \sum_i S(a_i)
\]

其中 \(S\) 是稀疏性懲罰項，偏好只有少數係數為非零。

## 結果

學到的基底函數具有局部性、方向性與帶通特性，類似 V1 簡單細胞的感受野。

## 限制

這是線性生成模型，未涵蓋複雜細胞、時間動態與高層回饋。稀疏編碼是多種規範性解釋之一，並非 V1 的完整模型。

## 連結

- 母頁：[計算神經科學](../index.md)
- 同一主題的另一方法：[Hodgkin–Huxley 模型](../hodgkin-huxley/index.md)

## 參考文獻

### 開創性論文

- Hodgkin, A. L. & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1952.sp004764 — 推導動作電位的四變數電導模型，是多數生物物理神經元模型的基礎。
- Izhikevich, E. M. (2003). Simple model of spiking neurons. *IEEE Transactions on Neural Networks*. https://doi.org/10.1109/TNN.2003.820440 — 雙變數模型，以低計算成本重現多種皮質發放型態。
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*. https://doi.org/10.1038/381607a0 — 顯示自然影像的稀疏編碼會產生類似 V1 簡單細胞的定向局部濾波器。
- Richards, B. A. et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — 主張以目標函數、學習規則與架構來研究大腦。

### 綜述與教科書

- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — 免費線上教科書，從單一神經元模型到網路與學習規則。
