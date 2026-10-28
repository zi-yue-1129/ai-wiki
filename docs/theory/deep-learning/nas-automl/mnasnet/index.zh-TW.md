---
translation_reviewed: 2026-10-28
---

# MnasNet：平台感知神經架構搜尋（Tan et al., 2018）

MnasNet 由 Tan et al.（2018）提出，它以一個包含真實手機實測延遲的獎勵來搜尋行動卷積網路，而不是採用乘加運算次數這類代理指標。它是[硬體感知神經架構搜尋](../index.md)最清楚的例子之一，其搜尋空間也被重複使用於 [EfficientNet](../../../models/cnn/backbones-and-scaling/efficientnet/index.md) 的基準網路。

## 概述

行動視覺模型必須小、快，同時又要準確，而以手動方式權衡這些取捨十分困難。早期的搜尋方法經常以代理指標衡量速度，通常是 FLOPS，但它與手機上的真實推論時間只有微弱的關聯。Tan et al. 直接在手機上測量延遲，並把這個測量納入搜尋目標。

結果是 MnasNet-A1：在 ImageNet 上達到 75.2% 的 top-1 準確率，在 Pixel 1 手機上每張影像 78 ms，參數為 3.9M，乘加運算為 312M（論文表 1）。

## 關鍵概念

- **分解式階層搜尋空間。** 網路被分成多個區塊，每個區塊有固定的輸入解析度與濾波器大小。在每個區塊內，搜尋選擇單一層的運算與連接，以及該層重複的次數，因此早期與後期區塊可以不同。
- **實測延遲。** 每個取樣的模型都在 Pixel 1 手機的大型 CPU 核心上執行，批次大小為一，以測量其延遲。
- **加權乘積目標。** 準確率與延遲被合併成單一分數。作者選擇它而非硬性限制，是因為它易於客製化，並能給出一系列的權衡。
- **帕雷托前緣。** 一次搜尋會沿著準確率與延遲的前緣產生多個模型。MnasNet-A2 與 MnasNet-A3 來自同一次搜尋，但延遲不同。

## 運作方式

搜尋使用循環控制器，並以近端策略最佳化（PPO）訓練，共分四個階段。

1. **取樣。** 控制器預測一串 token，在分解式空間中指定一個模型。
2. **訓練與測量。** 模型在目標任務上以縮短的訓練排程訓練，得到準確率 \(\mathrm{ACC}(m)\)。其延遲 \(\mathrm{LAT}(m)\) 則在手機上測得。
3. **獎勵。** 獎勵為

\[
\text{最大化} \quad \mathrm{ACC}(m) \times \left(\frac{\mathrm{LAT}(m)}{T}\right)^{w}, \qquad w = \begin{cases} \alpha, & \mathrm{LAT}(m) \le T \\ \beta, & \mathrm{LAT}(m) > T \end{cases}
\]

其中 \(T\) 為目標延遲。論文使用 \(T = 75\) ms 與 \(\alpha = \beta = -0.07\)。兩個指數相等時，超出目標的懲罰是平滑的，而非硬性截斷，因此控制器把目標視為軟性限制。

4. **更新。** 以 PPO 更新控制器，以最大化期望獎勵，然後重複迴圈。

搜尋取樣了約 8,000 個模型，在 64 台 TPUv2 上花了 4.5 天。之後取前 15 名，在完整的 ImageNet 上訓練。

## 結果

論文表 1 中，各模型在 ImageNet 上的比較如下。

| 模型 | 搜尋 | 參數 | 乘加運算 | Top-1 | 延遲（Pixel 1） |
|---|---|---|---|---|---|
| MobileNetV2 (1.4×) | 手動 | 6.9M | 585M | 74.7% | 143 ms |
| AmoebaNet-A | 自動 | 5.1M | 555M | 74.5% | 190 ms |
| MnasNet-A1 | 自動 | 3.9M | 312M | 75.2% | 78 ms |
| MnasNet-A3 | 自動 | 5.2M | 403M | 76.7% | 103 ms |

MnasNet-A1 的速度是表中經搜尋得到的 AmoebaNet-A 的兩倍以上，準確率則高於人工設計的 MobileNetV2，延遲約為其一半。MnasNet-A3 來自同一次搜尋，是表中最準確的模型，延遲為 103 ms。論文也比較了硬性延遲限制與此處使用的軟性限制：硬性限制會把搜尋集中在比目標更快的模型上，軟性限制則會取樣多種延遲，使一次搜尋得到數個帕雷托模型。論文另外討論了層的多樣性，認為它是所找到的架構表現良好的原因之一。

## 限制

- **單一裝置。** 延遲只在一款手機上測量。搜尋針對該裝置調校，在某一裝置上快的模型，在另一裝置上不一定快。
- **搜尋成本。** 在手機上測量每個取樣模型很慢，而且搜尋仍需要 64 個加速器運作 4.5 天。
- **人工設定的取捨。** 指數 \(\alpha\) 與 \(\beta\) 由作者選定，因此準確率與速度之間的偏好並非由搜尋學得。

## 開放問題

- **代理延遲。** 延遲測量在不同手機與加速器之間的轉移效果如何？EfficientNet 的搜尋重用了這個空間，但最佳化的是 FLOPS，因此兩篇論文回答的是關於速度的不同問題。
- **較便宜的搜尋。** 能否從模型的結構預測延遲，使手機不必執行每個候選者？這能降低成本，但也會增加誤差來源。
- **獎勵設計。** 以單一加權乘積合併準確率與速度，是否是正確的做法？論文認為它實用。

## 參考文獻

### 開創性論文

- Tan, M., et al. (2018). *MnasNet: Platform-Aware Neural Architecture Search for Mobile*. arXiv:1807.11626. https://arxiv.org/abs/1807.11626 — 論文本身：納入手機延遲的獎勵，產生在準確率與速度之間權衡的行動 CNN。
- Tan, M. & Le, Q. V. (2019). *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks*. arXiv:1905.11946. https://arxiv.org/abs/1905.11946 — 重用 MnasNet 的搜尋空間設計基準網路，再以複合規則縮放。
- Zoph, B. & Le, Q. V. (2016). *Neural Architecture Search with Reinforcement Learning*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — 以強化學習訓練的 RNN 控制器，是 MnasNet 控制器的前身。

### 綜述與教科書

- Elsken, T., Metzen, J. H. & Hutter, F. (2018). *Neural Architecture Search: A Survey*. arXiv:1808.05377. https://arxiv.org/abs/1808.05377 — 依搜尋空間、搜尋策略與效能估計組織 NAS。

### 文章與文件

- Yang, A., Esperança, P. M. & Carlucci, F. M. (2019). *NAS evaluation is frustratingly hard*. arXiv:1912.12522. https://arxiv.org/abs/1912.12522 — 主張 NAS 結果在不同協定下難以比較，這點也適用於考慮延遲的比較。
