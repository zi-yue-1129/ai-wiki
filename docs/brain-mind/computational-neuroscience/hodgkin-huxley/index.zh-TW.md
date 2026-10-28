---
translation_reviewed: 2026-10-28
---

# Hodgkin–Huxley 模型（Hodgkin & Huxley, 1952）

以離子通道與門控變數建立的神經元膜電位電導模型。

## 問題

動作電位如何由跨越烏賊巨大軸突細胞膜的離子流動產生？

## 核心想法

細胞膜被視為一個電容，與電壓門控的鈉、鉀電導以及漏電流並聯。三個閘控變數（m、h、n）各自朝向依電壓而定的數值鬆弛，並控制電導。

## 方程式或演算法

（採用現代的符號慣例）

\[
C\frac{dV}{dt} = I - g_{Na}\,m^3 h\,(V - E_{Na}) - g_K\,n^4\,(V - E_K) - g_L\,(V - E_L)
\]

\[
\frac{dx}{dt} = \alpha_x(V)\,(1 - x) - \beta_x(V)\,x, \qquad x \in \{m, h, n\}
\]

## 結果

模擬出的動作電位形狀與烏賊軸突的記錄相符，並重現了動作電位沿軸突傳播的情形。

## 限制

只根據單一標本、單一溫度擬合，沒有樹突結構。每個區室四個耦合方程，對大型網路計算成本高，因此上表中較簡單的 LIF 與 Izhikevich 模型才這麼常見。

## 連結

- 母頁：[計算神經科學](../index.md)
- 同一主題的另一方法：[稀疏編碼](../sparse-coding/index.md)

## 參考文獻

### 開創性論文

- Hodgkin, A. L. & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1952.sp004764 — 推導動作電位的四變數電導模型，是多數生物物理神經元模型的基礎。
- Izhikevich, E. M. (2003). Simple model of spiking neurons. *IEEE Transactions on Neural Networks*. https://doi.org/10.1109/TNN.2003.820440 — 雙變數模型，以低計算成本重現多種皮質發放型態。
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*. https://doi.org/10.1038/381607a0 — 顯示自然影像的稀疏編碼會產生類似 V1 簡單細胞的定向局部濾波器。
- Richards, B. A. et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — 主張以目標函數、學習規則與架構來研究大腦。

### 綜述與教科書

- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — 免費線上教科書，從單一神經元模型到網路與學習規則。
