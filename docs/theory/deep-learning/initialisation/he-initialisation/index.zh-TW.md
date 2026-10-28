---
translation_reviewed: 2026-10-28
---

# He 初始化

He 初始化，或稱 Kaiming 初始化，為整流線性單元所構成的網路，將每個權重的變異數設為 \(2/n_{\text{in}}\)。He 等人於 2015 年推導此方法，修正了 [Xavier（Glorot）規則](../glorot-xavier/index.md)，因為整流單元會移除輸入的負值部分。在論文的實驗中，它訓練了一個 30 層的普通網路，而 Xavier 方案在此停滯。它是上層[權重初始化](../index.md)頁面中所比較的方法之一。

## 概述

Glorot 與 Bengio 的規則是針對對稱且在零點斜率為一的激活函數推導的，例如 tanh。整流線性單元 \(\max(0, x)\) 既非對稱，也非線性，卻成為深層卷積網路的標準激活函數。He 等人（2015）問：對於整流網路，應採用什麼尺度？他們發現，答案與 Xavier 規則在變異數上相差兩倍。

論文也推導了參數化整流單元（PReLU）的規則，其負斜率可以學習，並涵蓋普通整流單元與線性情況。

## 關鍵概念

- **整流單元。** 輸入為正時輸出其輸入，否則輸出零的單元。若輸入的分布對稱，它大約會保留輸入二階矩的一半。
- **負斜率 \(a\)。** 在 PReLU 中，負輸入會乘上 \(a\)。\(a = 0\) 對應普通整流單元，\(a = 1\) 則對應線性單元。
- **反向條件。** 一層的梯度是其所餵入各單元之和，因此反向條件使用的是輸出數。當各層寬度相近時，兩種選擇給出的尺度幾乎相同。

## 運作方式

設第 \(l\) 層有 \(n_l\) 個輸入，這些輸入是前一層整流器的輸出。預激活值的變異數為 \(\mathrm{Var}[y_l] = n_l \mathrm{Var}[w_l]\,\mathrm{E}[x_l^2]\)，而對於整流器，\(\mathrm{E}[x_l^2] = \tfrac{1}{2}\mathrm{Var}[y_{l-1}]\)。經過 \(L\) 層後得到

\[
\mathrm{Var}[y_L] = \mathrm{Var}[y_1] \prod_{l=2}^{L} \tfrac{1}{2} n_l \mathrm{Var}[w_l].
\]

每個因子都必須等於一，因此 \(\tfrac{1}{2} n_l \mathrm{Var}[w_l] = 1\)，得到

\[
w_l \sim \mathcal{N}\left(0, \frac{2}{n_l}\right)，
\]

即標準差為 \(\sqrt{2/n_l}\) 的零均值高斯分布。偏置設為零。對於負斜率為 \(a\) 的 PReLU，條件變為 \(\tfrac{1}{2}(1 + a^2)\,n_l \mathrm{Var}[w_l] = 1\)，在 \(a = 0\) 時回到整流單元，在 \(a = 1\) 時為線性情況。

對於反向傳播，同樣的推導給出 \(\tfrac{1}{2}\hat{n}_l\mathrm{Var}[w_l] = 1\)，其中 \(\hat{n}_l\) 為輸出數乘以卷積核大小的平方。論文指出，在其網路中，任一條件單獨成立即足以使訓練收斂。程序如下：對每一層計算 \(n_l\)（輸入數乘以卷積核面積），從 \(\mathcal{N}(0, 2/n_l)\) 抽取權重，並將偏置設為零。

## 結果

He 等人在 ImageNet 2012 分類基準上，以整流網路比較了此方案與 Xavier。

- **中等深度的模型。** 在一個 22 層模型上，兩種方案都能收斂，新方案較早開始降低誤差。對於 14 層模型，論文報告新方案的 top-1 與 top-5 誤差分別為 33.82% 與 13.34%，Xavier 則為 33.90% 與 13.44%，兩者在準確率上沒有明顯差異。
- **極深的模型。** 在論文針對最深 30 層（27 個卷積層與 3 個全連接層）模型所做的比較中，新方案使 30 層模型得以收斂，而 Xavier 方案停滯，梯度也持續縮小。
- **最終系統。** 一個 PReLU 網路在 ImageNet 2012 上達到 4.94% 的 top-5 誤差；作者報告，這相對於 GoogLeNet 的 6.66% 有 26% 的相對改進。

論文也報告，其 ImageNet 的 30 層模型 top-1 與 top-5 誤差分別為 38.56% 與 16.59%，明顯比 14 層模型差。在這些實驗中，單靠加深網路並未改善準確率。

## 限制

- **控制的是尺度，而非準確率。** 此方案在起點讓訊號維持合理的大小；它並未證明訓練後的網路泛化得更好。
- **加深的效益遞減。** ImageNet 上較深的模型表現較差，論文也引用其他研究，指出較深的網路會出現飽和。初始化可以讓深層網路能夠訓練，但不保證加深一定有幫助。
- **推導針對整流單元。** GELU、SiLU 等其他激活函數不適用於二分之一的因子，需要另外推導其增益。
- **寬度改變。** 此規則固定的是某一寬度下的尺度；[muP](../mup/index.md) 處理的是網路變寬時學習率應如何改變。

## 開放問題

- 現代 Transformer 中常見的門控前饋區塊，應採用什麼增益。
- 在使用殘差連接與正規化的情況下，此方案在極深網路中的優勢是否仍然存在。論文中的普通網路並未測試這一點。

## 參考文獻

### 開創性論文

- He, K., Zhang, X., Ren, S. & Sun, J. (2015). *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*. arXiv. https://arxiv.org/abs/1502.01852 — 推導整流單元與 PReLU 的 \(2/n_l\) 初始化，並顯示 30 層網路可用此方案收斂。
- Glorot, X. & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS. https://proceedings.mlr.press/v9/glorot10a.html — Xavier 或標準化初始化，He 等人將其改寫以適用於整流單元。

### 文章與文件

- Schoenholz, S. S., Gilmer, J., Ganguli, S. & Sohl-Dickstein, J. (2017). *Deep Information Propagation*. arXiv. https://arxiv.org/abs/1611.01232 — 以平均場理論說明深度如何限制隨機網路的可訓練性。
- Pennington, J., Schoenholz, S. S. & Ganguli, S. (2017). *Resurrecting the sigmoid in deep learning through dynamical isometry: theory and practice*. arXiv. https://arxiv.org/abs/1711.04735 — 顯示 ReLU 網路無法達到動力等距，而正交權重的 sigmoid 網路可以。
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Identity Mappings in Deep Residual Networks*. arXiv. https://arxiv.org/abs/1603.05027 — 說明恆等跳接如何與整流殘差區塊互動。
