---
translation_reviewed: 2026-10-28
related:
- theory/models/rnn
tags:
- neuromorphic
- spiking neural networks
- learning rules
aliases:
  - e-prop
  - eligibility propagation
---

# 以局部更新進行線上學習：e-prop（Bellec et al., 2020）

學習使用局部的資格跡（eligibility trace）與學習訊號，而不是沿時間反向傳播（backpropagation through time）。這讓循環式脈衝神經網路可以線上訓練：權重隨著輸入到達而更新，只使用每個突觸在當下可得的資訊。

本頁屬於[脈衝神經網路與神經形態運算](../index.md)。它詳細說明一種學習規則。

## 概述

以沿時間反向傳播（BPTT）訓練循環網路，必須儲存整段活動歷史，再把誤差沿著歷史倒推。這在電腦上是可行的，但與突觸局部能知道的資訊不相符，也很難在節能的神經形態硬體上執行。e-prop 是一種學習規則：每個突觸只保留一段短的跡，每個神經元則接收一個學習訊號，並邊跑邊更新。

## 核心概念

- **資格跡（eligibility trace）**：每個突觸一個的量，以前向時間方式記錄該突觸近期的活動，對神經元輸出可能有多少貢獻。
- **學習訊號（learning signal）**：每個神經元一個的誤差訊號，從局部迴路之外傳入該神經元，例如目標或獎勵。
- **線上學習（online learning）**：在輸入仍在進行時就更新權重，而不是等整段序列結束後才更新。
- **脈衝神經元（spiking neuron）**：以離散脈衝溝通的神經元，其狀態通常是膜電位。

## 問題

沿時間反向傳播需要整段歷史，也很難與生物學相容。循環脈衝網路能否只用局部可得的資訊進行線上學習？這個問題既關乎神經形態硬體的實用性，也關乎大腦可能如何學習的模型。

## 核心想法

為每個突觸計算一段以前向時間方式更新的資格跡，用它來近似梯度。再把它與從局部迴路之外傳到每個神經元的學習訊號結合。如此一來，每個時間步都可以更新。作者展示，這樣的組合近似於 BPTT 會計算的梯度，只是省略了某些項。

## 方程式或演算法

權重更新是把學習訊號與資格跡的乘積沿時間加總：

\[
\Delta W_{ji} = \sum_t L_j(t)\, e_{ji}(t)
\]

其中 \(L_j(t)\) 為神經元 j 的學習訊號，\(e_{ji}(t)\) 為從神經元 i 到神經元 j 之突觸的資格跡。資格跡在每個時間步由局部量更新，因此此規則不需要儲存歷史。

## 結果

作者報告，在他們測試的任務上，線上規則的表現接近沿時間反向傳播，這些任務包括論文中描述的脈衝網路任務。比較的對象是同一網路上的 BPTT，因此衡量的是近似所付出的準確度代價。

## 限制

- **只是近似。**此規則省略了某些梯度項，因此不是精確的梯度；在被省略的項很重要的任務上，表現可能低於 BPTT。
- **所選的任務。**所報告的結果只涵蓋作者選定的任務，推廣到其他任務與架構需要另外測試。
- **學習訊號的來源。**此規則假設每個神經元都能收到學習訊號；在生物或硬體系統中如何提供這種訊號，則是另一個問題。

## 與其他主題的關聯

- **代理梯度（surrogate gradients）**：訓練脈衝網路的另一條路，用平滑的替代函數取代脈衝函數，再以反向傳播訓練。見[代理梯度](../surrogate-gradients/index.md)。
- **循環網路**：此規則是 BPTT 在循環模型上的線上替代方案。標準的循環架構見[循環神經網路](../../../theory/models/rnn/index.md)。
- **母主題**：[脈衝神經網路與神經形態運算](../index.md)。

## 應用

- **神經形態硬體**：局部更新適合把權重與跡存放在神經元旁邊的晶片，不需要儲存完整歷史。
- **大腦學習的模型**：局部規則是皮質迴路如何學習的候選機制，有待與資料比對檢驗。

## 開放問題

- **在較難的任務上，近似有多精確？**與 BPTT 的差距只在所報告的任務上呈現，較大的問題可能會擴大這個差距。
- **學習訊號從哪裡來？**此規則需要每個神經元的訊號，而這種訊號在生物或硬體中的來源，仍是開放的設計問題。
- **生物突觸是否遵循此規則？**以突觸記錄來檢驗資格跡學習，是尚待解決的實驗問題。

## 參考文獻

### 開創性論文

- Bellec, G., et al.（2020）。A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*。https://doi.org/10.1038/s41467-020-17236-y — e-prop 學習規則，是脈衝網路上沿時間反向傳播的線上近似。
- Neftci, E. O., Mostafa, H. & Zenke, F.（2019）。Surrogate Gradient Learning in Spiking Neural Networks. *IEEE Signal Processing Magazine*。https://doi.org/10.1109/MSP.2019.2931595 — 提出代理梯度，使脈衝網路能以沿時間反向傳播訓練。

### 綜述與教科書

- Eshraghian, J. K., et al.（2023）。Training Spiking Neural Networks Using Lessons From Deep Learning. *Proceedings of the IEEE*。https://doi.org/10.1109/JPROC.2023.3308088 — 以深度學習工具訓練脈衝網路的教學，附 snnTorch 範例。
- Roy, K., Jaiswal, A. & Panda, P.（2019）。Towards spike-based machine intelligence with neuromorphic computing. *Nature*。https://doi.org/10.1038/s41586-019-1677-2 — 關於脈衝式計算與神經形態硬體的綜述。
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L.（2014）。*Neuronal Dynamics*。Cambridge University Press。https://neuronaldynamics.epfl.ch/ — 關於脈衝神經元模型與網路的免費線上教科書。
