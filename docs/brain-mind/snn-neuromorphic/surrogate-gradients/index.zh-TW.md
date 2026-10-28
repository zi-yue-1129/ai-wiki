---
translation_reviewed: 2026-10-28
---

# 替代梯度（Neftci、Mostafa 與 Zenke，2019）

脈衝網路以反向傳播訓練，方法是把閾值的導數換成平滑的替代函數。

## 問題

脈衝是階躍函數，其導數幾乎處處為零，因此反向傳播無法直接訓練脈衝網路。

## 核心想法

前向傳遞時保留硬閾值；反向傳遞時，以平滑的替代函數取代閾值的導數，再進行時間反向傳播。

## 方程式或演算法

前向時，神經元在膜電位超過閾值時發放脈衝；反向時，其導數被以以閾值為中心的平滑替代函數 \(\sigma'\) 取代。

## 結果

論文將替代梯度呈現為訓練脈衝網路的一種靈活且有效的方法，而非單一基準的結果。

## 限制

替代函數的選擇是經驗性的。時間反向傳播需要儲存網路的歷史，記憶體成本隨序列長度增加。

## 連結

- 母頁：[脈衝神經網路與神經形態運算](../index.md)
- 同一主題的另一方法：[具局部更新的線上學習（e-prop）](../eprop/index.md)

## 參考文獻

### 開創性論文

- Neftci, E. O., Mostafa, H. & Zenke, F.（2019）。Surrogate Gradient Learning in Spiking Neural Networks. *IEEE Signal Processing Magazine*. https://doi.org/10.1109/MSP.2019.2931595 — 提出替代梯度，讓脈衝網路能以時間反向傳播訓練。
- Bellec, G., 等人（2020）。A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*. https://doi.org/10.1038/s41467-020-17236-y — e-prop 學習規則，是脈衝網路時間反向傳播的線上近似。

### 綜述與教科書

- Eshraghian, J. K., 等人（2023）。Training Spiking Neural Networks Using Lessons From Deep Learning. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2023.3308088 — 以深度學習工具訓練脈衝網路的教學，含 snnTorch 範例。
- Roy, K., Jaiswal, A. & Panda, P.（2019）。Towards spike-based machine intelligence with neuromorphic computing. *Nature*. https://doi.org/10.1038/s41586-019-1677-2 — 脈衝式運算與神經形態硬體的綜述。
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L.（2014）。*Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — 關於脈衝神經元模型與網路的免費線上教科書。
