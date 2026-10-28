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

正規化流是由一連串可逆、可微的映射建構的生成模型。由於每個映射都可逆，且其雅可比行列式容易計算，任何資料點的精確對數似然與精確抽樣都可取得。本頁涵蓋離散流的家族，並分別詳述 Real NVP 與 Glow。連續的替代方法見[流匹配](../flow-matching/index.md)，家族總覽與兩個分支的比較見[流模型](../index.md)頁。

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

### 以 Real NVP 做密度估計（Dinh、Sohl-Dickstein 與 Bengio，2017）

- **問題：** 影像的精確似然生成模型受限於小型或簡單的架構，而早期的 NICE 耦合無法擴展到自然影像。
- **核心想法：** 仿射耦合層。把輸入分成 \(x_A\) 與 \(x_B\)，輸出為 \(y_A = x_A\) 與 \(y_B = x_B \odot \exp(s(x_A)) + t(x_A)\)，其中 \(s\) 與 \(t\) 為神經網路。反函數同樣容易計算，對數行列式即為 \(s\) 的總和。
- **公式或演算法：** 堆疊耦合層，交替轉換的兩半，並加入批次正規化與多尺度的表徵分解。以最大似然訓練。
- **結果：** 論文在多個自然影像資料集上報告對數似然結果與生成影像。摘要未給出數字，引用時請以論文的數據為準。
- **限制：** 每個維度的轉換受到限制，且當時的樣本不如 GAN 樣本清晰。精確似然並不保證好的樣本，下方的開放問題會再談到這點。

### Glow（Kingma 與 Dhariwal，2018）

- **問題：** 當時的流難以加深，也難以用於高解析度影像的控制。
- **核心想法：** 以可逆 1×1 卷積混合通道，它取代了 Real NVP 固定的置換，改為學習混合方式；並以 actnorm 層做穩定的初始化。每一步為 actnorm、可逆 1×1 卷積與仿射耦合。
- **公式或演算法：** 權重矩陣為 \(W\) 的 1×1 卷積，作用於 \(h\times w\) 的特徵圖時，其對數行列式為 \(h\,w\,\log\lvert\det W\rvert\)。Glow 以多尺度架構堆疊多個此類步驟，並以最大似然訓練。
- **結果：** 摘要報告在標準基準上對數似然有顯著提升，並能真實且有效率地合成與操控大型影像。摘要強調潛在空間操控，例如沿學到的方向改變屬性。摘要未給出具體數字。
- **限制：** 在高解析度下模型仍然昂貴，而精確似然不一定與人眼所見的品質一致。後續架構為了表達力而犧牲了部分精確性。

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
