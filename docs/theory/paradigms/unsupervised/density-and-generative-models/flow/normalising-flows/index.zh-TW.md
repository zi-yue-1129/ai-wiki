---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
tags:
  - 正規化流
  - 生成模型
  - 密度估計
aliases:
  - 正規化流
  - 標準化流
  - Normalizing flows
  - Real NVP
  - Glow
---

# 正規化流（Normalising Flows）

正規化流是由一連串可逆、可微的映射建構的生成模型。由於每個映射都可逆，且其雅可比行列式容易計算，任何資料點的精確對數似然與精確抽樣都可取得。本頁涵蓋離散流的家族，並分別為 Real NVP 與 Glow 撰寫方法頁。連續的替代方法見[流匹配](../flow-matching/index.md)，家族總覽與兩個分支的比較見[流模型](../index.md)頁。

## 概覽

Dinh 等人（2014）以 NICE 提出此方法，使用加性耦合層，使行列式恰為一。Dinh 等人（2017）把耦合層推廣為仿射耦合，既保有容易計算的行列式，又能做尺度變換，並將其應用於影像。Kingma 與 Dhariwal（2018）隨後加入可逆 1×1 卷積與啟動正規化（actnorm），使架構更深、更有表達力。Rezende 與 Mohamed（2015）更早就為此一般框架命名，並把流用於變分後驗。

## 關鍵概念

- **基底分布** \(p_z\)：通常是標準高斯，抽樣由此開始。
- **可逆映射** \(f\)：由多層堆疊而成，其反函數的計算成本與前向傳遞相同。
- **耦合層**：把輸入分成兩部分，保留其中一部分不變，另一部分則以前者計算出的尺度與平移來轉換。
- **對數行列式**：修正 \(f\) 造成體積變化的項，在每一層都加入似然中。
- **多尺度架構**：在多個解析度上擠壓並分出部分表徵，使深層看到較小的輸入。

## 運作方式

對於 \(x = f(z)\)，\(z\sim p_z\)，變數變換給出

\[
\log p_x(x) = \log p_z\big(f^{-1}(x)\big) + \log\left|\det \frac{\partial f^{-1}(x)}{\partial x}\right|
\]

訓練時最大化資料上平均的此對數似然。抽樣時抽取 \(z\sim p_z\)，並以一次前向傳遞計算 \(f(z)\)。

## 關鍵方法

- [Real NVP（Dinh 等人，2017）](realnvp.md)：仿射耦合層，並以多尺度架構處理影像。其尺度與平移網路不受限制，反函數與前向傳遞的成本相同。
- [Glow（Kingma 與 Dhariwal，2018）](glow.md)：每一步都包含 actnorm 與可逆 1×1 卷積，並可在潛在空間中操控影像。

兩者使用相同的變數變換似然，差異在於層的設計，而非訓練目標。

## 關聯

- 流的公式是[生成模型](../../generative-models/index.md)頁三大生成演算法之一，與 [VAE](../../vae/index.md) 和 [GAN](../../gan/index.md) 並列。
- 流被用作變分推論中有彈性的後驗，見[機率方法](../../../../probabilistic/index.md)。
- 耦合層使用一般的卷積或全連接子網路，見[卷積網路](../../../../../models/cnn/index.md)。

## 應用

密度估計與異常偵測、以學到的先驗做無失真與有失真壓縮，以及貝氏模型中的後驗近似。

## 開放問題

- 在保有精確似然的同時，達到擴散與 GAN 模型的樣本品質。
- 可逆性是否真的限制了模型能學到的東西，或只是成本。
- 以合理的運算量擴展到非常高的解析度。

## 參考文獻

### 開創性論文

- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. ICML. https://arxiv.org/abs/1505.05770 — 把正規化流定義為用於有彈性後驗的可逆變換。
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — 提出加性耦合層，其雅可比行列式為一。
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2017). *Density Estimation Using Real NVP*. ICLR. https://arxiv.org/abs/1605.08803 — 提出用於影像的仿射耦合層與多尺度架構。
- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS（arXiv）. https://arxiv.org/abs/1807.03039 — 加入可逆 1×1 卷積與 actnorm，並展示潛在空間的影像操控。

### 綜述與教科書

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 流架構及其在密度估計與推論中的應用綜述。

## 延伸學習

- Eric Jang, *Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows*。連結：https://blog.evjang.com/2018/01/nf2.html — 以淺顯方式介紹現代流架構與其雅可比行列式。
