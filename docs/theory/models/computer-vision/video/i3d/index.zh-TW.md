---
translation_reviewed: 2026-10-28
---

# 膨脹三維卷積網路（I3D）

I3D 是一種影片分類器，做法是把深層的二維影像網路 Inception-v1 擴展為三維。由於擴展後的濾波器可以從 ImageNet 權重開始，網路因此能先在大型影片資料集上預訓練。Carreira 與 Zisserman 於 2017 年與 Kinetics 資料集一同提出它。它是[影片理解與生成](../index.md)頁所列的方法之一。

## 概述

在 I3D 之前，動作辨識主要有兩種設計。雙流網路在影格與預先算好的光流上分別執行二維卷積網路，因此運動只能經由光流輸入進入網路。[^1] 完整的三維卷積網路，例如 C3D，直接從像素學習運動，但參數遠多於二維網路，也無法沿用影像權重。[^2]

I3D 保留三維卷積，並把經過驗證的影像架構加以膨脹，以提供起始權重。標準基準資料集太小，難以區分不同架構，這促成了 Kinetics：400 個動作類別，每類至少 400 個片段，約 24 萬個訓練片段。[^3]

雙流設計與神經科學中的雙流假說有鬆散的關聯。該假說主張腹側通路負責物體，背側通路負責運動。[^4] 這種相似只是組織方式上的。參見[知覺與視覺系統](../../../../../brain-mind/visual-perception/index.md)。

## 關鍵概念

- **時空卷積。** 同時跨越空間與時間的核，例如 $3\times3\times3$，能對跨影格移動的圖樣產生反應。
- **膨脹。** 每個 $N\times N$ 的濾波器變成 $N\times N\times N$，池化核也增加時間維度。
- **無聊影片。** 把靜態影像沿時間重複而成的影片，網路對它的輸出應與對原影像相同。當二維權重複製 $N$ 次並除以 $N$ 時即可達成。[^2]
- **光流。** 兩張影格之間表觀運動的場，為第二條串流離線計算。

## 運作方式

每個 I3D 網路輸入一段由影格組成的短片段，並輸出類別分數。膨脹規則為

$$
W^{\text{3D}}_{t} = \frac{1}{N}\,W, \qquad t = 1,\dots,N,
$$

其中 $W$ 是二維權重。對無聊影片而言，對 $t$ 求和會還原 $W$，因此回應與影像網路一致。[^2]

主要模型執行兩個 I3D 網路，一個處理 RGB 影格，一個處理光流，兩者分別訓練後取平均。它是一種多了一個時間軸的[卷積神經網路](../../../cnn/index.md)。

## 結果

- **Kinetics-400，從零開始。** 雙流 I3D 以 RGB 與光流合併，達到 71.6% 的 top-1 準確率。類似 C3D 的網路則為 56.1%。
- **Kinetics-400，以 ImageNet 初始化。** 雙流 I3D 達到 74.2% 的 top-1 與 91.3% 的 top-5。較早的雙流基準為 65.6%。
- **Kinetics 預訓練後的 UCF-101 與 HMDB-51。** 論文回報 98.0% 與 80.9%。[^2] 比較表中較強的先前結果是一個結合手工軌跡特徵的殘差雙流網路，分別為 94.6% 與 70.3%。

## 限制

- **高度依賴預訓練。** 最強的結果需要大規模預訓練，而比較的每一種架構都能從 Kinetics 獲益。[^2]
- **光流是另一個昂貴的步驟。** 光流需離線計算。作者認為迭代式的光流最佳化，正是前饋 RGB 網路仍需要光流串流的原因。[^2]
- **時間範圍短。** 片段只涵蓋短暫的時段，因此緩慢展開的動作難以建模。[^5]

## 開放問題

- 膨脹是否同樣適用於 Inception-v1 以外的架構？
- 當網路夠大、訓練影片夠多時，是否仍需要獨立的光流串流？SlowFast 與 TimeSformer 只處理 RGB 影格。[^5][^6]

## 參考文獻

### 開創性論文

- Szegedy, C., et al. (2014). *Going Deeper with Convolutions*. arXiv. https://arxiv.org/abs/1409.4842 — Inception 架構，I3D 所膨脹的是其中的 Inception-v1 版本。
- Russakovsky, O., et al. (2014). *ImageNet Large Scale Visual Recognition Challenge*. arXiv. https://arxiv.org/abs/1409.0575 — ImageNet 基準，其預訓練權重用來初始化 I3D。
- Soomro, K., Zamir, A. R. & Shah, M. (2012). *UCF101: A Dataset of 101 Human Actions Classes From Videos in The Wild*. arXiv. https://arxiv.org/abs/1212.0402 — 用於微調的 101 類動作資料集。
- Kuehne, H., Jhuang, H., Garrote, E., Poggio, T. & Serre, T. (2011). *HMDB: A large video database for human motion recognition*. ICCV. https://doi.org/10.1109/ICCV.2011.6126543 — 用於微調的 51 類動作資料集。
- Carreira, J. & Zisserman, A. (2017). *Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset*. arXiv. https://arxiv.org/abs/1705.07750 — 透過膨脹 Inception-v1 提出 I3D，並在三個資料集上測試。
- Simonyan, K. & Zisserman, A. (2014). *Two-Stream Convolutional Networks for Action Recognition in Videos*. arXiv. https://arxiv.org/abs/1406.2199 — 分別處理 RGB 影格與光流的兩個卷積網路，其預測結果加以融合。
- Tran, D., et al. (2014). *Learning Spatiotemporal Features with 3D Convolutional Networks*. arXiv. https://arxiv.org/abs/1412.0767 — C3D 網路，在影片上從零開始訓練。
- Kay, W., et al. (2017). *The Kinetics Human Action Video Dataset*. arXiv. https://arxiv.org/abs/1705.06950 — 用於預訓練 I3D 的 400 類 YouTube 片段資料集。
- Feichtenhofer, C., Fan, H., Malik, J. & He, K. (2018). *SlowFast Networks for Video Recognition*. arXiv. https://arxiv.org/abs/1812.03982 — 以慢速與快速兩條路徑，同時建模語意與運動。
- Bertasius, G., Wang, H. & Torresani, L. (2021). *Is Space-Time Attention All You Need for Video Understanding?* arXiv. https://arxiv.org/abs/2102.05095 — TimeSformer，一種不使用卷積的影片 Transformer。
- Goodale, M. A. & Milner, A. D. (1992). *Separate visual pathways for perception and action*. Trends in Neurosciences. https://doi.org/10.1016/0166-2236%2892%2990344-8 — 提出腹側與背側視覺通路的架構，雙流設計與之相互比較。

[^1]: Simonyan 與 Zisserman（2014），摘要：空間與時間串流及其融合。
[^2]: Carreira 與 Zisserman（2017）：第 2 節（膨脹）、引言（參數數量），以及表 3、表 4 與表 5 的結果。準確率在 Kinetics-400 為 top-1，在 UCF-101 與 HMDB-51 則為三個切分的平均。
[^3]: Kay 等人（2017）：400 類，每類至少 400 個片段，每段約十秒，來自不同的 YouTube 影片。24 萬個訓練片段的數字見 Carreira 與 Zisserman（2017）第 3 節。
[^4]: Goodale 與 Milner（1992）。雙流設計與此理論有關，Simonyan 與 Zisserman 的論文曾提及此關聯但未加以檢驗。
[^5]: Feichtenhofer 等人（2018）：慢速路徑為低影格率，快速路徑為高影格率。
[^6]: Bertasius 等人（2021），摘要：僅由時空自注意力構成的影片 Transformer。
