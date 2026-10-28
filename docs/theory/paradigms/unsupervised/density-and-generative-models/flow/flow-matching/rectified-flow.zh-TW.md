---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/flow
  - theory/models/transformer
---

# 修正流（Rectified Flow）

修正流學習一個 ODE，其軌跡盡可能地直，因此即使只用很少的解算器步數，抽樣仍然準確。Liu、Gong 與 Liu（2022）提出了它，並加入能進一步拉直軌跡的修正（reflow）程序。家族比較見[流匹配](index.md)與[流模型](../index.md)頁。

## 概述

以 ODE 解算器抽樣，每一步都需要一次網路評估，因此彎曲的軌跡很難精確積分。修正流以成對雜訊與資料點之間的直線段來訓練漂移項。當學到的軌跡接近直線時，單一步的 Euler 法就能給出可用的樣本。訓練目標與[條件流匹配](conditional-flow-matching.md)使用的直線方向相同，新的部分是改變成對方式的修正程序。

## 關鍵概念

- **線性內插**：\(X_t = t\,X_1 + (1-t)\,X_0\)，其中 \(X_0\) 取自雜訊分布 \(\pi_0\)，\(X_1\) 取自資料分布 \(\pi_1\)。
- **漂移項**：時間相依的向量場 \(v(z,t)\)，定義 ODE \(\mathrm{d}Z_t = v(Z_t,t)\,\mathrm{d}t\)，把樣本從 \(\pi_0\) 帶到 \(\pi_1\)。
- **修正**：以先前修正流模擬出的配對 \((Z^k_0, Z^k_1)\) 進行新一輪訓練。

## 運作方式

獨立抽取 \(X_0\sim\pi_0\) 與 \(X_1\sim\pi_1\)，依上式形成 \(X_t\)，並以最小平方法沿時間擬合漂移項：

\[
\min_v \int_0^1 \mathbb E\big[\lVert (X_1 - X_0) - v(X_t, t)\rVert^2\big]\,\mathrm{d}t
\]

修正時，取第 \(k\) 輪訓練好的流，從 \(\pi_0\) 模擬得到端點配對 \((Z^k_0, Z^k_1)\)，再於這些配對上訓練新的修正流，即 \(Z^{k+1} = \mathrm{RectFlow}\big((Z^k_0, Z^k_1)\big)\)。每一輪都讓路徑更直。論文提醒，修正輪數太多會累積估計誤差。

## 關鍵方法

### Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow（Liu、Gong 與 Liu，2022）

- **問題：** 以 ODE 為基礎的生成模型需要很多解算器步數，因為粗糙的積分器無法精確逼近彎曲的軌跡。
- **核心想法：** 沿線性內插把漂移項擬合到直線方向 \(X_1 - X_0\)，再以修正程序讓雜訊與資料沿更直的路徑配對。
- **公式或演算法：** 上述最小平方目標與修正更新。每一輪修正都在前一個流的端點配對上訓練。
- **結果：** 摘要指出，接近直線的流即使只用單一 Euler 步，也能給出高品質的樣本。在 CIFAR-10（無條件生成，DDPM++ 架構）上，論文表 1(a) 列出單步結果。文字引用經蒸餾的兩輪修正流 FID 為 4.85，而表中同一列的單步數值為 12.21，4.85 則以括號附於其旁。單輪流以自適應 RK45 模擬時，約 127 次函數評估即達到 FID 2.58。論文未提供 ImageNet 的 FID，其高解析度結果僅以定性方式呈現。
- **限制：** 修正每一輪都需要模擬前一個模型，計算成本高。輪數太多會累積誤差。第一輪使用獨立配對，因此沒有處理配對方式的選擇，這也是[小批次最優傳輸流匹配](minibatch-ot-flow-matching.md)的動機之一。

## 關聯

- [條件流匹配](conditional-flow-matching.md)使用相同的直線目標，但沒有修正程序。
- [隨機插值](stochastic-interpolants.md)提供一個框架，其中這個線性內插只是其中一個選擇。
- Esser 等人（2024）把修正流以 Transformer 擴展到高解析度的文字到影像生成，見下方參考文獻。

## 開放問題

- 修正輪數要多少才值得其成本，以及如何在誤差累積前停止。
- 直線軌跡對大型條件模型是否仍是最佳目標。

## 參考文獻

### 開創性論文

- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv；ICLR 2023. https://arxiv.org/abs/2209.03003 — 提出修正流與本頁描述的修正程序。
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — 修正流所比較的條件流匹配目標。
- Tong, A., Fatras, K., Malkin, N., Huguet, G., Zhang, Y., Rector-Brooks, J., Wolf, G. & Bengio, Y. (2024). *Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport*. TMLR. https://arxiv.org/abs/2302.00482 — 處理第一輪修正留下的雜訊與資料配對問題。

### 規模化與應用

- Esser, P., et al. (2024). *Scaling Rectified Flow Transformers for High-Resolution Image Synthesis*. arXiv. https://arxiv.org/abs/2403.03206 — 以 Transformer 將修正流應用於高解析度文字到影像生成，並報告此方法優於既有的擴散模型公式化方式。

### 背景

- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. arXiv. https://arxiv.org/abs/1806.07366 — 定義流並以 ODE 解算器抽樣的連續深度框架。
