---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/vision-transformer
  - theory/models/cnn/backbones-and-scaling
tags:
  - transformers
  - computer vision
  - knowledge distillation
  - data efficiency
aliases:
  - DeiT
  - Data-efficient image Transformer
  - 資料高效影像 Transformer
translation_reviewed: 2026-10-28
---

# DeiT：以資料高效方式訓練影像 Transformer

DeiT（Data-efficient image Transformer，資料高效影像 Transformer）只用 ImageNet-1K 訓練一個[視覺 Transformer](../index.md)。它加入一個蒸餾 token，讓 Transformer 透過注意力從卷積網路教師學習。Touvron 等人（2021）顯示，具競爭力的 ViT 可以在單機上於三天內訓練完成，且不需要外部預訓練資料。

## 概述

[原始 ViT](../index.md) 只有在使用數億張影像預訓練後才達到最佳結果，而那需要多數團隊沒有的基礎設施。DeiT 問的是：若訓練配方與教師能彌補資料的不足，同樣的架構能否只靠 ImageNet 訓練。論文保留 ViT 架構，只改動兩件事：一套強力的資料增強與正則化配方，以及一個蒸餾 token。

## 關鍵概念

- **蒸餾（distillation）**：訓練學生網路去匹配較強教師的輸出，這裡的教師是有標籤的影像分類器。
- **蒸餾 token**：與類別 token 並列的第二個可學習 token，其輸出被訓練來預測教師的標籤。
- **硬標籤蒸餾（hard-label distillation）**：以教師預測的類別作為硬目標，而非完整的機率向量。
- **模型變體**：DeiT-Ti（5M 參數）、DeiT-S（22M）與 DeiT-B（86M），除非另有說明，皆為 224 解析度。

## 運作方式

編碼器的輸入是區塊嵌入，外加兩個額外 token：類別 token 與蒸餾 token。兩者各有自己的輸出頭。類別頭以真實標籤 \(y\) 訓練，蒸餾頭以教師的硬標籤 \(y_t\) 訓練，訓練損失是兩個交叉熵項的等權重和：

\[
\mathcal{L} = \tfrac{1}{2}\,\mathrm{CE}\big(\psi(z^{\text{cls}}_L),\, y\big) + \tfrac{1}{2}\,\mathrm{CE}\big(\psi(z^{\text{dist}}_L),\, y_t\big)
\]

其中 \(\psi\) 是線性分類器，\(y_t = \arg\max_c Z_t(c)\) 是教師預測的類別。測試時，論文的主要方法是把兩個頭的 softmax 輸出相加來融合。蒸餾 token 與類別 token 注意相同的區塊，因此教師的訊號會透過注意力層傳給學生。

## 關鍵方法

### Training data-efficient image transformers & distillation through attention（Touvron 等人，2021）

- **問題：** ViT 需要數億張預訓練影像與昂貴的基礎設施，限制了它的採用。問題是：不使用卷積、只用 ImageNet-1K，Transformer 能否具競爭力。
- **核心想法：** 保留 ViT 架構，加入以卷積網路教師標籤訓練的蒸餾 token，並以強力的資料增強與正則化配方彌補資料量較少的問題。
- **方程式或演算法：** 上述的雙頭交叉熵損失，搭配教師的硬標籤。訓練配方（論文表 9）使用 AdamW，學習率為 \(5\times10^{-4}\) 並依批次大小按 512 縮放，權重衰減 0.05，餘弦衰減，批次大小 1024，訓練 300 個 epoch。
- **結果：** 摘要指出，參考模型（86M 參數）在不使用外部資料下，於 ImageNet 上達到 83.1% top-1 準確率（單一裁切），而論文的教師-學生設定可達 85.2%。論文表 3 顯示，未使用蒸餾時，DeiT-Ti、DeiT-S 與 DeiT-B 在 224 解析度下分別為 72.2%、79.8% 與 81.8%；使用蒸餾後，同樣的模型分別為 74.5%、81.2% 與 83.4%。
- **限制：** 如摘要所述，蒸餾的增益在教師為卷積網路時最大。蒸餾模型依賴一個強教師，此處是 84M 參數的 RegNetY-16GF。配方很繁重（RandAugment、Mixup、CutMix、隨機抹除、隨機深度與重複增強），因此「資料高效」的主張依賴於這套配方。

## 組件與變體

- **資料增強與正則化。** 論文表 9 列出 RandAugment（9, 0.5）、機率 0.8 的 Mixup、機率 1.0 的 CutMix、機率 0.25 的隨機抹除、0.1 的隨機深度與 0.1 的標籤平滑。作者也使用重複增強，並排除了 dropout。
- **教師的選擇。** 論文比較了不同教師，其中卷積網路教師的增益最大；Transformer 教師的增益較小。
- **較高解析度。** 在 384 解析度下微調，可讓 DeiT-B 在未使用蒸餾時達到 83.1%。使用蒸餾並延長訓練後，最佳報告結果為 85.2%。

## 連結

- [視覺 Transformer（ViT）](../index.md)是 DeiT 保留的架構。DeiT 改變的是訓練配方，並加入蒸餾 token。
- [Transformer 與注意力機制](../../index.md)提供兩個模型都使用的注意力區塊。
- [ConvNeXt](../../../cnn/backbones-and-scaling/convnext/index.md)是能匹配 Transformer 基線的卷積網路，也是最能幫助 DeiT 的那類教師。
- [電腦視覺](../../../computer-vision/index.md)涵蓋 DeiT 作為骨幹使用的影像分類模型。

## 未解問題

- **對教師的依賴。** 蒸餾會增加第二個網路與教師的訓練成本。在沒有教師的情況下，對未標註 ImageNet 做自監督預訓練能否獲得同樣好處，是一個實際問題。
- **配方與架構的區分。** 大部分增益來自資料增強與正則化，因此很難把蒸餾 token 本身的貢獻與配方分開。
- **超越 ImageNet 的擴展。** 論文的主張針對 ImageNet-1K，遷移到其他任務的結果只簡短展示。

## 參考文獻

### 開創性論文

- Touvron, H., et al. (2021). *Training data-efficient image transformers & distillation through attention*. ICML 2021, PMLR 139, pp. 10347–10357. [arXiv:2012.12877](https://arxiv.org/abs/2012.12877) — 提出 DeiT，以蒸餾 token 只用 ImageNet 訓練 ViT。
- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929) — DeiT 所保留的 ViT 架構。
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. [arXiv:1503.02531](https://arxiv.org/abs/1503.02531) — 提出知識蒸餾，蒸餾 token 即建立於此。

### 綜述與教科書

（本頁尚未查核）

### 講座

（本頁尚未查核）

### 文章與文件

- Facebook Research, *DeiT*, GitHub. [facebookresearch/deit](https://github.com/facebookresearch/deit) — 官方 DeiT 儲存庫，包含評估與訓練程式碼及預訓練模型。該儲存庫已封存，也涵蓋相關論文。

## 延伸學習

（尚未新增）
