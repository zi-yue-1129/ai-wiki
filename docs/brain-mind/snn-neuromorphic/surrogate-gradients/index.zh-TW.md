---
translation_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- brain-mind/neuroscience
tags:
- neuroscience
- neuromorphic
- learning
aliases:
  - 替代梯度學習
  - Neftci 2019
  - 替代梯度
---

# 替代梯度（Neftci、Mostafa 與 Zenke，2019）

脈衝神經網路以離散的脈衝溝通，而產生脈衝的閾值，其導數幾乎處處為零。替代梯度在前向傳播中保留硬閾值，在反向傳播中則以平滑函數取代其導數。這使脈衝神經網路可以用時間反向傳播來訓練，與一般遞迴網路所用的方法屬於同一類。

本頁是[脈衝神經網路與神經形態運算](../index.md)的子頁。上層頁面提供概述，本頁說明方法與證據。

## 問題

脈衝神經元在膜電位越過閾值時發出脈衝。若寫成函數，脈衝是一個階躍：輸出在閾值處從零跳到一，其餘之處皆為平的。以梯度為基礎的學習需要導數，而階躍的導數幾乎處處為零，因此誤差訊號無法傳到權重。

## 方法

這個方法把前向與反向傳播分開。前向傳播使用真正的脈衝非線性，因此網路以脈衝進行計算。反向傳播則使用替代導數，也就是以閾值為中心的平滑函數，使誤差訊號能沿著時間往回傳。

步驟如下：

1. 沿時間向前模擬脈衝網路，每個神經元在膜電位越過閾值時發出脈衝。
2. 在反向傳播時，以替代導數 \(\sigma'\) 取代脈衝的導數；這是一個在閾值附近較大、遠離閾值時較小的平滑函數。
3. 應用時間反向傳播，用替代導數計算權重更新。

以方程式表示，設膜電位為 \(v_t\)、閾值為 \(\vartheta\)、脈衝輸出為 \(s_t\)，前向傳播為 \(s_t = H(v_t - \vartheta)\)，其中 \(H\) 為階躍函數。反向傳播則以 \(\partial s_t / \partial v_t \approx \sigma'(v_t - \vartheta)\) 取代階躍的導數。論文把 \(\sigma'\) 的選擇視為一項設計決定，實務上會使用多種形狀。

第 2 步是替代導數發揮作用的地方。只有反向傳播改變，因此網路仍以它被訓練產生的同一種離散脈衝進行計算。

## 結果

論文把替代梯度呈現為訓練脈衝網路的一種靈活且有效的途徑，證據是它能應用於多種架構與任務，而非單一基準結果。本頁所用的摘要中，這些結果是定性的。引用具體準確率前，請查閱論文與後續的基準測試。

## 限制

- 替代函數的選擇是一種經驗法則。不同的形狀可能導致不同的訓練行為，沒有單一有原則的選擇。
- 時間反向傳播會儲存網路的歷史，因此記憶體成本隨序列長度增加。
- 替代導數只是真實梯度的近似，因此這個方法並未最佳化脈衝網路的精確目標。

## 與其他主題的關聯

- **線上學習**：不需要儲存完整歷史的局部、線上替代方案，見[以局部更新進行線上學習（e-prop）](../eprop/index.md)。
- **上層頁面**：包括硬體在內的更廣泛脈衝與神經形態運算領域，見[脈衝神經網路與神經形態運算](../index.md)。
- **NeuroAI**：脈衝網路的梯度式訓練如何與受大腦啟發的學習相關，見 [NeuroAI](../../neuroai/index.md)。

## 開放問題

- **哪一種替代函數最好，原因為何？** 領域使用多種形狀，但何時各自有效，仍缺乏有原則的說明。
- **替代梯度訓練能否擴展到大腦的學習規則？** 時間反向傳播並非明顯具有生物合理性，局部近似能否彌補這個差距仍是開放問題。

## 參考文獻

### 開創性論文

- Neftci, E. O., Mostafa, H. & Zenke, F.（2019）。Surrogate gradient learning in spiking neural networks. *arXiv*。https://arxiv.org/abs/1901.09948 — 提出替代梯度，使脈衝神經網路能以時間反向傳播來訓練。
- Bellec, G., et al.（2020）。A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*。https://pmc.ncbi.nlm.nih.gov/articles/PMC7367848 — e-prop 學習規則，是脈衝網路上時間反向傳播的線上近似。

### 綜述與教科書

- Eshraghian, J. K., et al.（2023）。Training spiking neural networks using lessons from deep learning. *Proceedings of the IEEE*。https://arxiv.org/abs/2109.12894 — 以深度學習工具訓練脈衝網路的教學，附 snnTorch 範例。
- Roy, K., Jaiswal, A. & Panda, P.（2019）。Towards spike-based machine intelligence with neuromorphic computing. *Nature*。https://doi.org/10.1038/s41586-019-1677-2 — 關於脈衝式計算與神經形態硬體的綜述。
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L.（2014）。*Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*。Cambridge University Press。https://neuronaldynamics.epfl.ch/book.html — 關於脈衝神經元模型與網路的免費線上教科書。
