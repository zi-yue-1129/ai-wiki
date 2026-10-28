---
translation_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - 正規化流
  - 生成模型
  - 密度估計
aliases:
  - Glow
  - Glow 生成流
  - Generative flow with invertible 1x1 convolutions
---

# Glow

Glow 是一種正規化流，以學到的可逆 1×1 卷積取代 [Real NVP](realnvp.md) 固定的通道置換。它加入 actnorm 以達到穩定的初始化，並證明流模型能生成與操控大型人臉影像。它屬於[正規化流](index.md)家族。

## 概覽

Kingma 與 Dhariwal（2018）以 Real NVP 的耦合層建構了更深的流。他們的兩項新增是可學習的通道混合步驟，以及依資料初始化的正規化層。他們在數個自然影像資料集上報告比 Real NVP 更好的似然，並展示學到的潛在空間支援平滑內插與屬性編輯。

## 關鍵概念

- **Actnorm**：每通道的尺度與偏置，由第一個小批次初始化，使每個通道的平均為零、變異數為一。初始化後，與其他參數一樣被訓練。
- **可逆 1×1 卷積**：可學習的通道混合矩陣 \(W\)。它取代 Real NVP 固定的置換，並以隨機旋轉矩陣初始化，因此其對數行列式一開始為零。
- **LU 分解**：把 \(W\) 寫成 LU 形式，可把其對數行列式的成本從通道數的三次方降為線性。
- **零初始化的耦合層**：每個耦合網路的最後一層卷積以零初始化，使每個耦合層一開始都是恆等映射。

## 運作方式

一個流步驟依序為 actnorm、可逆 1×1 卷積，然後是仿射耦合層。對於 \(h \times w\) 的特徵圖，1×1 卷積對對數行列式的貢獻為 \(h\,w\,\log\lvert\det W\rvert\)。各步驟以與 Real NVP 相同的多尺度設計堆疊，每個尺度做擠壓與分出。訓練時最大化精確的對數似然。

## 關鍵方法

### Glow（Kingma 與 Dhariwal，2018）

- **問題：** 當時的流很難加深，也難以控制高解析度影像。
- **核心想法：** 以可逆 1×1 卷積學習通道混合，並以 actnorm 正規化激活，使深層堆疊能可靠地訓練。每一步仍保有耦合流容易計算的對數行列式。
- **公式或演算法：** 上述步驟結構與 1×1 卷積的對數行列式，搭配 Real NVP 的多尺度架構。每一步為 actnorm、可逆 1×1 卷積與仿射耦合。
- **結果：** 論文表 2 中，每維位元數在所列的每個資料集上都低於 Real NVP。例如 CIFAR-10 為 3.35（Real NVP 為 3.49），LSUN bedroom 為 2.38（2.72），ImageNet 32×32 為 4.09（4.28）。附錄表 3 報告 5 位元的結果，其中 CelebA-HQ 256×256 為 1.03 位元，但其位元深度與 8 位元的表不同，不宜直接比較。論文也展示潛在空間中的內插與屬性編輯，屬性方向是在訓練後由有標籤的影像計算得出。
- **限制：** 在高解析度下模型成本高。似然並不保證知覺品質。5 位元的結果若要與 8 位元的結果比較，需要小心。

## 關聯

- [Real NVP](realnvp.md) 是 Glow 所延伸的耦合層設計。
- 似然與正規化流框架見[正規化流](index.md)總覽。
- 連續時間的流是另一種方法，見[流匹配](../flow-matching/index.md)。
- 耦合網路在影像上為卷積式，見[卷積網路](../../../../../models/cnn/index.md)。

## 應用

具精確似然的高解析度影像合成，以及透過學到的屬性方向對人臉潛在空間做編輯。

## 開放問題

- 學到的通道混合，在較大尺度上是否真的優於固定置換。
- 如何降低高解析度下深層流的成本。
- 以流做潛在空間編輯，是否與 GAN 或擴散模型的編輯一樣可靠。

## 參考文獻

### 開創性論文

- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS（arXiv）. https://arxiv.org/abs/1807.03039 — 在多尺度流中提出 actnorm 與可逆 1×1 卷積，即本頁的方法。
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2017). *Density Estimation Using Real NVP*. ICLR（arXiv）. https://arxiv.org/abs/1605.08803 — 提出仿射耦合層與 Glow 所建立於其上的多尺度架構。
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — 提出加性耦合層，是此家族的起源。
- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. ICML. https://arxiv.org/abs/1505.05770 — 把正規化流定義為一般的可逆變換類別。

### 綜述與教科書

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — 流架構（包括 Glow 的設計）及其在密度估計中的應用綜述。

## 延伸學習

- Eric Jang, *Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows*。連結：https://blog.evjang.com/2018/01/nf2.html — 以淺顯方式介紹現代流架構。
