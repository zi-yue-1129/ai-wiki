---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/flow
---

# 小批次最優傳輸流匹配（Minibatch OT Flow Matching）

小批次最優傳輸流匹配（OT-CFM）來自 Tong 等人（2024）。它保留條件流匹配的目標，但改變雜訊樣本與資料點的配對方式。在每個訓練小批次中，它解一個雜訊集與資料集之間的最優傳輸問題，並以傳輸計畫給出的配對進行訓練。結果是更直、訓練更穩定的流，而且只需以便宜的方式逼近最優傳輸。

## 概述

條件流匹配把每個資料點與一個獨立的雜訊樣本配對。獨立配對會使條件路徑可能交叉，因此回歸目標的變異數較高。作者報告 OT-CFM 能產生較簡單的流，使推論更快、訓練更穩定。以最優傳輸在小批次內配對，使配對步驟的成本侷限在每個批次之內，這讓它能用於大型資料集。

## 關鍵概念

- **小批次傳輸計畫**：一批雜訊樣本 \(x_0\) 與一批資料樣本 \(x_1\) 之間的最優傳輸計畫，通常以平方歐氏距離為成本計算。
- **條件路徑**：圍繞線性內插 \(\mu_t = t\,x_1 + (1-t)\,x_0\)、標準差為 \(\sigma\) 的高斯。
- **回歸目標**：配對點之間的方向 \(x_1 - x_0\)。

## 運作方式

對每個訓練批次，此方法：

1. 抽取雜訊點 \(x_0\) 與目標點 \(x_1\)。
2. 在兩批之間解一個最優傳輸問題，得到配對上的傳輸計畫。
3. 依該計畫重新抽樣配對 \((x_0, x_1)\)，而非獨立配對。
4. 抽取 \(t\sim\mathcal U[0,1]\)，並從以 \(\mu_t\) 為中心、標準差為 \(\sigma\) 的高斯中抽取點 \(x\)。
5. 以平方誤差損失把 \(v_\theta(t, x)\) 回歸到 \(x_1 - x_0\)。

最優傳輸的批次大小不必與最佳化的批次大小相同。當傳輸批次涵蓋完整的支撐集時，此方法可恢復兩分布之間的精確最優傳輸。批次大小為一時，此方法退化為標準的條件流匹配。

## 關鍵方法

### Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport（Tong 等人，2024）

- **問題：** 條件流匹配中的獨立配對會產生高變異數的回歸目標與彎曲的流，因此抽樣需要更多步，訓練也較慢。
- **核心想法：** 依每個小批次上計算的最優傳輸計畫重新抽樣雜訊與資料的配對。目標保留流匹配的條件形式。
- **公式或演算法：** 把 \(v_\theta(t, x)\) 回歸到 \(x_1 - x_0\)，其中 \(x\) 取自圍繞 \(\mu_t\) 的高斯，而 \((x_0, x_1)\) 來自小批次傳輸計畫。損失為此回歸的平方誤差。
- **結果：** 摘要指出，OT-CFM 能產生較簡單、訓練較穩定的流，並帶來更快的推論。論文報告，在 CIFAR-10 上，以少量函數評估時表現明顯較好。在相同的訓練步數下，它的驗證表現優於條件流匹配，作者把這歸因於較低的目標變異數。
- **限制：** 小批次傳輸計畫只是近似，精確的最優傳輸需要涵蓋完整支撐集的批次。解指派問題會增加每個批次的成本。報告的進步來自影像基準，論文並未宣稱在所有資料類型上都成立。

## 關聯

- [條件流匹配](conditional-flow-matching.md)是此方法保留的目標，只是配對規則不同。
- [修正流](rectified-flow.md)以修正程序拉直路徑，是改變配對方式的另一條途徑。
- [隨機插值](stochastic-interpolants.md)提供通用框架，可在其中比較耦合與插值的選擇。
- 最優傳輸的背景見下方參考文獻中的 Peyré 與 Cuturi（2019）。

## 開放問題

- 小批次要多大，才能使對最優傳輸的近似不再改善。
- 變異數的降低能否延伸到極高解析度或非影像資料。

## 參考文獻

### 開創性論文

- Tong, A., Fatras, K., Malkin, N., Huguet, G., Zhang, Y., Rector-Brooks, J., Wolf, G. & Bengio, Y. (2024). *Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport*. TMLR. https://arxiv.org/abs/2302.00482 — 提出小批次最優傳輸配對與本頁描述的 OT-CFM 目標。
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — 本方法所修改的條件流匹配目標。
- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv. https://arxiv.org/abs/2209.03003 — 透過修正程序取得直線路徑的另一條途徑。
- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — 可在其中分析耦合選擇的插值框架。

### 最優傳輸背景

- Peyré, G. & Cuturi, M. (2019). *Computational Optimal Transport*. arXiv. https://arxiv.org/abs/1803.00567 — 介紹本頁傳輸計畫所用的計算方法。
