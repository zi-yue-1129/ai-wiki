---
translation_reviewed: 2026-10-28
---

# Swin Transformer：移位視窗（Liu et al., 2021）

Swin Transformer 是一種階層式視覺 Transformer，它在小型局部視窗內計算自注意力，並在各層之間移動視窗，使成本隨影像大小線性成長。它是[視覺 Transformer](../index.md)主題中的第二個里程碑式變體，設計目的是作為偵測、分割與分類的通用骨幹網路。

## 概觀

原始的 [ViT](../vit/index.md) 只保有單一的特徵解析度，並對所有區塊計算注意力，因此成本隨影像面積的平方成長。偵測與分割等密集任務需要高解析度、多尺度的特徵，而 ViT 並未提供。Swin 像 CNN 一樣建構特徵金字塔，並把注意力限制在視窗內，使成本保持可控。作者把它與偵測任務中使用的 [ResNet](../../../cnn/backbones-and-scaling/resnet/index.md) 骨幹網路比較，並指出它在這些任務上是更好的骨幹，而不僅限於分類。

## 關鍵概念

- **區塊合併（patch merging）**：每個階段把每一組 2 × 2 的相鄰 token 串接起來並做投影，使解析度減半、寬度加倍。
- **視窗注意力（window attention）**：自注意力在互不重疊的 M × M 視窗內計算。預設的視窗大小為 M = 7。
- **移位視窗（shifted windows）**：在交替的層中，視窗格線會平移半個視窗，使相鄰視窗中的 token 能交換資訊。
- **相對位置偏置（relative position bias）**：一種學得的偏置，取決於視窗內兩個 token 之間的位置偏移，用來取代絕對位置嵌入。

## 運作方式

一個 4 × 4 的區塊嵌入把影像轉換為寬度為 C 的 token。接著有四個階段，解析度分別為 H/4、H/8、H/16 與 H/32。每個階段包含數個 Swin 區塊，且第一個階段之後的每個階段都以區塊合併層開始。兩個相續的區塊計算為

$$
\hat z^l = \text{W-MSA}(\text{LN}(z^{l-1})) + z^{l-1}, \quad z^l = \text{MLP}(\text{LN}(\hat z^l)) + \hat z^l
$$

$$
\hat z^{l+1} = \text{SW-MSA}(\text{LN}(z^l)) + z^l, \quad z^{l+1} = \text{MLP}(\text{LN}(\hat z^{l+1})) + \hat z^{l+1}
$$

其中 W-MSA 使用一般視窗，SW-MSA 使用移位視窗。注意力包含相對位置偏置 B：

$$
\text{Attention}(Q,K,V) = \text{SoftMax}\!\left(\frac{QK^\top}{\sqrt{d}} + B\right)V
$$

成本為 \(\Omega(\text{W-MSA}) = 4hwC^2 + 2M^2hwC\)，在視窗大小固定時，它與區塊數 \(hw\) 呈線性關係；全域注意力則與 \(hw\) 呈平方關係。為了有效率地移位視窗，特徵圖會被循環式地平移，並以遮罩阻止 token 跨越環繞的邊界進行注意力計算，因此視窗數量維持不變。Swin-T 與 Swin-S 使用 C = 96，深度分別為 {2, 2, 6, 2} 與 {2, 2, 18, 2}；Swin-B 與 Swin-L 分別使用 C = 128 與 192，深度模式與 Swin-S 相同。

## 結果

論文的表 1 報告 224 × 224 下 ImageNet-1K 的 top-1 準確率。Swin-T 以 29M 參數達到 81.3%，而 DeiT-S 為 79.8%。Swin-B 達到 83.5%，而 DeiT-B 為 81.8%。使用 ImageNet-22K 預訓練時，Swin-B 在 384 解析度下達到 86.4%，Swin-L 達到 87.3%。在 COCO 上，使用多尺度測試的 Swin-L 搭配 HTC++ 在 test-dev 上達到 58.7 的 box AP；搭配 UperNet 的 Swin-L 在 ADE20K 驗證集上達到 53.5 mIoU。

消融實驗使用 Swin-T。相較於單一的一般分區，移位視窗在 ImageNet-1K 上增加 1.1% 的 top-1。相對位置偏置相較於沒有位置編碼增加 1.2% 的 top-1，相較於絕對嵌入增加 0.8%。論文也比較了移位視窗與滑動視窗。兩者的準確率相近（81.3% 對 81.4%），但移位版本依實作方式快約 1.5 至 4 倍。

## 限制

- **視窗大小固定。** 每一層只看到 M × M 個 token 的視窗，因此全域脈絡只能透過深度與移位逐步建立。論文的所有實驗都使用固定的預設值 M = 7。
- **實作。** 作者指出，他們的版本使用內建的 PyTorch 函式，而核心層級的最佳化超出了論文的範圍。
- **來自 CNN 的競爭。** [ConvNeXt](../../../cnn/backbones-and-scaling/convnext/index.md) 後來顯示，純卷積網路可以在相近成本下與 Swin 相當，這使得「視窗式注意力是關鍵要素」的主張減弱。

## 開放問題

- 設計中究竟是階層結構還是視窗化更重要？論文的消融實驗著重於移位與位置偏置，因此對階層結構的直接檢驗較少。
- 視窗式注意力如何擴展到非常大的影像或影片，其中視窗格線與相對偏置必須改變。
- 單一骨幹能否同時服務視覺與語言，這是作者在論文末尾提出的目標。

## 參考文獻

### 開創性論文

- Liu, Z., et al. (2021). *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*. arXiv；ICCV 2021. https://arxiv.org/abs/2103.14030 — 原始論文，介紹移位視窗注意力與階層式 Swin 骨幹網路。
- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv；ICLR 2021. https://arxiv.org/abs/2010.11929 — 單一解析度的 ViT，Swin 設計來改善其在密集任務上的表現。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Swin 所修改的自注意力與 Transformer 區塊。
- He, K., et al. (2016). *Deep Residual Learning for Image Recognition*. arXiv；CVPR 2016. https://arxiv.org/abs/1512.03385 — 殘差 CNN 骨幹網路，Swin 在偵測實驗中與之比較。
- Lin, T.-Y., et al. (2017). *Feature Pyramid Networks for Object Detection*. arXiv；CVPR 2017. https://arxiv.org/abs/1612.03144 — 建構多尺度特徵金字塔，是 Swin 階層結構所設計要餵入的結構。
- Liu, Z., et al. (2022). *A ConvNet for the 2020s*. arXiv；CVPR 2022. https://arxiv.org/abs/2201.03545 — ConvNeXt，一種純 CNN，在相近成本下與 Swin 相當或更好。
