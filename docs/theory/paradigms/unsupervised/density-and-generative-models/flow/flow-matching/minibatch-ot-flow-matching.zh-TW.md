---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/flow
---

# 小批次最優傳輸流匹配（Minibatch OT Flow Matching）

小批次最優傳輸流匹配（OT-CFM）來自 Tong 等人（2024）。它保留條件流匹配的目標，但改變雜訊樣本與資料點的配對方式。在每個訓練小批次中，它解一個雜訊集與資料集之間的最優傳輸問題，並以傳輸計畫給出的配對進行訓練。結果是更直、訓練更穩定的流，而且只需以便宜的方式逼近最優傳輸。

## 概述

條件流匹配會把每個資料點與一個獨立的雜訊樣本配對。作者認為，這種獨立配對使回歸目標的變異數偏高。其附錄指出，小批次最優傳輸「大幅降低回歸目標的變異數」，實驗也顯示流更直，且更容易積分。摘要指出，OT-CFM「產生更簡單、訓練更穩定的流」，並帶來更快的推論。在小批次內以最優傳輸進行配對，使配對步驟的成本侷限於該批次，這也是它能用於大型資料集的原因。

## 關鍵概念

- **小批次傳輸計畫**：在一批雜訊樣本 \(x_0\) 與一批資料樣本 \(x_1\) 之間的最優傳輸計畫，在訓練批次內計算。
- **條件路徑**：以線性插值 \(\mu_t = t\,x_1 + (1-t)\,x_0\) 為中心、標準差為小量 \(\sigma\) 的高斯分布。
- **回歸目標**：配對點之間的方向 \(x_1 - x_0\)。

## 運作方式

對於每個訓練批次，此方法會：

1. 抽取來源點 \(x_0\) 與目標點 \(x_1\)。
2. 在兩批資料之間解一個最優傳輸問題，得到成對點上的傳輸計畫。
3. 依該計畫重新抽取配對 \((x_0, x_1)\)，而不是獨立配對。
4. 抽取 \(t\sim\mathcal U[0,1]\)，以及來自以 \(\mu_t\) 為中心、標準差為 \(\sigma\) 的高斯分布的點 \(x\)。
5. 以平方誤差損失，把 \(v_\theta(t, x)\) 回歸到 \(x_1 - x_0\)。

最優傳輸批次的大小不必與最佳化批次相同。當傳輸批次涵蓋完整支撐集時，此方法恢復兩個分布之間的精確最優傳輸。批次大小為一時，此方法退化為標準條件流匹配。

## 關鍵方法

### Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport（Tong 等人，2024）

- **問題：** 條件流匹配中的獨立配對，使回歸目標的變異數偏高，訓練較困難，產生的流也較不直，因此取樣需要更多步。
- **核心想法：** 依每個小批次上計算的最優傳輸計畫重新抽取雜訊與資料的配對。目標仍保持流匹配的條件形式。
- **公式或演算法：** 把 \(v_\theta(t, x)\) 回歸到 \(x_1 - x_0\)，其中 \(x\) 取自以 \(\mu_t\) 為中心的高斯分布，\((x_0, x_1)\) 來自小批次傳輸計畫。損失為此回歸的平方誤差。
- **結果：** 摘要指出，OT-CFM「產生更簡單、訓練更穩定的流」，並帶來更快的推論。論文文字說，在 CIFAR-10 上，OT-CFM 在函數評估次數少時「表現顯著更好」，但表中的差距很小：採用自適應積分時 FID 為 3.58，I-CFM 為 3.66；以 100 步 Euler 積分時分別為 4.44 與 4.46。在低維測試中，N→8gaussians 的正規化路徑能量，OT-CFM 為 0.018，I-CFM 為 0.222。附錄指出，OT-CFM 的目標變異數明顯低於 CFM，作者將其與較容易訓練連結。
- **限制：** 小批次傳輸計畫只是近似，精確的最優傳輸需要涵蓋完整支撐集的批次。每個批次解配對問題會增加成本。CIFAR-10 上的差距在報告的表中很小，因此所宣稱的優勢主要依賴低維與單細胞實驗。

## 關聯

- [條件流匹配](conditional-flow-matching.md)是此方法保留的目標，只是配對規則不同。
- [修正流](rectified-flow.md)透過修正程序使路徑變直，是改變配對方式以外的另一條路。
- [隨機插值](stochastic-interpolants.md)提供一般框架，可在其中比較耦合與插值的選擇。
- 關於最優傳輸背景，見下方參考文獻中的 Peyré 與 Cuturi（2018）。

## 開放問題

- 小批次要多大，才能使對最優傳輸的逼近不再改善。
- 變異數縮減是否能延伸到極高解析度或非影像資料。

## 參考文獻

### 開創性論文

- Tong, A., Fatras, K., Malkin, N., Huguet, G., Zhang, Y., Rector-Brooks, J., Wolf, G. & Bengio, Y. (2024). *Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport*. TMLR. https://arxiv.org/abs/2302.00482 — 提出小批次最優傳輸配對與本頁描述的 OT-CFM 目標。
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — OT-CFM 所修改的條件流匹配目標。
- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv；ICLR 2023. https://arxiv.org/abs/2209.03003 — 透過修正程序得到直路徑的另一條路線。
- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — 可在其中分析耦合選擇的插值框架。

### 最優傳輸背景

- Peyré, G. & Cuturi, M. (2018). *Computational Optimal Transport*. arXiv. https://arxiv.org/abs/1803.00567 — 介紹本頁傳輸計畫所用的計算方法。
