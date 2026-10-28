---
translation_reviewed: 2026-10-28
---

# 具局部更新的線上學習：e-prop（Bellec 等人，2020）

學習使用局部的資格跡與學習訊號，而不是沿時間反向傳播。

## 問題

時間反向傳播需要完整的歷史，也很難與生物學調和。遞迴脈衝網路能否只用局部可取得的資訊進行線上學習？

## 核心想法

以每個突觸的資格跡（可隨時間向前計算）近似梯度，並與從外部傳到神經元的學習訊號結合。如此，更新可以在每個時間步進行。

## 方程式或演算法

權重更新是把學習訊號與資格跡相乘後，對時間加總：

\[
\Delta W_{ji} = \sum_t L_j(t)\, e_{ji}(t)
\]

## 結果

作者指出，在其測試的任務上，此線上規則的表現接近時間反向傳播。

## 限制

此規則省略了部分梯度項，因此只是近似。報告的結果僅涵蓋作者選擇的任務。

## 連結

- 母頁：[脈衝神經網路與神經形態運算](../index.md)
- 同一主題的另一方法：[替代梯度](../surrogate-gradients/index.md)

## 參考文獻

### 開創性論文

- Neftci, E. O., Mostafa, H. & Zenke, F.（2019）。Surrogate Gradient Learning in Spiking Neural Networks. *IEEE Signal Processing Magazine*. https://doi.org/10.1109/MSP.2019.2931595 — 提出替代梯度，讓脈衝網路能以時間反向傳播訓練。
- Bellec, G., 等人（2020）。A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*. https://doi.org/10.1038/s41467-020-17236-y — e-prop 學習規則，是脈衝網路時間反向傳播的線上近似。

### 綜述與教科書

- Eshraghian, J. K., 等人（2023）。Training Spiking Neural Networks Using Lessons From Deep Learning. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2023.3308088 — 以深度學習工具訓練脈衝網路的教學，含 snnTorch 範例。
- Roy, K., Jaiswal, A. & Panda, P.（2019）。Towards spike-based machine intelligence with neuromorphic computing. *Nature*. https://doi.org/10.1038/s41586-019-1677-2 — 脈衝式運算與神經形態硬體的綜述。
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L.（2014）。*Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — 關於脈衝神經元模型與網路的免費線上教科書。
