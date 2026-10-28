---
related:
- theory/models/transformer
aliases:
  - Backbones and Scaling
  - Residual Networks
  - ResNet
  - EfficientNet
  - 骨幹網路與縮放
  - 殘差網路
tags:
  - residual connections
  - model scaling
  - computer vision
translation_reviewed: 2026-10-28
---

# 骨幹網路與縮放

CNN 骨幹是把原始像素轉成特徵的疊層，任務頭再用這些特徵做分類、偵測或分割。骨幹的發展大致是在解決兩個問題：如何讓網路夠深而有用，又不至於無法訓練；以及有更多運算時，應如何擴大網路。前者靠殘差連接解決，後者靠縮放規則解決。

## 概觀

| 想法 | 代表模型 | 解決的問題 |
|---|---|---|
| 深層卷積堆疊 | AlexNet、VGG | 大規模端到端學習特徵 |
| 殘差連接 | ResNet | 訓練極深的網路 |
| 複合縮放 | EfficientNet | 同時選擇深度、寬度與解析度 |
| 現代化卷積 | ConvNeXt | 以純 CNN 達到 Transformer 基線水準 |

## 做法

### 殘差連接

殘差區塊學習一個修正量 \(F(x)\)，並加回輸入，因此輸出為 \(x + F(x)\)。He 等人（2015）指出，沒有這個捷徑時，較深的普通網路反而有更高的訓練誤差，這說明問題在最佳化而非過擬合。有了捷徑，梯度能直接穿過網路，數百層的網路因此可以訓練。殘差連接現在幾乎用於所有深度架構，包括 Transformer。

### 複合縮放

要做更大的網路，可以增加深度、寬度或輸入解析度。EfficientNet 主張只增加其中一項很快會飽和，因此提出以固定比例同時縮放三者，比例由小型搜尋決定。這個系列在每單位運算的準確率上，優於只縮放單一維度。

### 現代化的純 CNN

Liu 等人（2022）從 ResNet 出發，逐步修改其設計，借用 Transformer 的選擇，例如較大的核、較少的激活函數、層正規化與反向瓶頸。得到的 ConvNeXt 在影像分類與偵測上與 Transformer 基線相當。這個結果顯示，CNN 與 Transformer 之間的差距，有相當部分來自訓練配方與設計細節，而非核心運算本身。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| 深度殘差學習（ResNet） | 2015 | 捷徑連接使極深的網路能夠訓練 | [ResNet](resnet/index.md) |
| 複合縮放（EfficientNet） | 2019 | 以單一係數同時縮放深度、寬度與解析度 | [EfficientNet](efficientnet/index.md) |
| VGG | 2015 | 以小型 3×3 卷積堆疊的普通深層設計 | [VGG](vgg/index.md) |
| ConvNeXt | 2022 | 逐步現代化的 ResNet，與 Transformer 基線相當 | [ConvNeXt](convnext/index.md) |

## 取捨

- **深度與寬度。** 較深的網路能表示更複雜的函數，但訓練時記憶體成本較高；寬度通常有較好的硬體效率。
- **每單位運算的準確率。** 這個家族的縮放規律很有用，但最佳比例取決於目標硬體與資料。
- **預訓練。** 在大型資料集上預訓練的大型 CNN 骨幹遷移性好，因此同一架構常以其預訓練結果來評斷。

## 相關連結

殘差連接與 [Transformer](../../transformer/index.md) 中的跳接連接是同一個想法，也出現在 [MLP](../../mlp/index.md) 中。縮放問題在 [Transformer](../../transformer/index.md) 家族中再次出現，那裡的模型大小與資料大小是一起設定的。與大腦的連結較間接：深度 CNN 的層已被拿來與視覺區域的階層比較，見 [NeuroAI](../../../../brain-mind/neuroai/index.md)。

## 未解問題與更多變體

- **跨家族的縮放規則。** 複合縮放規則是針對一個家族推導的。它能否遷移到其他家族，以及如何縮放這些家族，尚無定論。
- **殘差為何有效。** 從梯度流到類似集成的行為，有數種解釋都獲得實驗支持，它們的相對重要性仍有爭議。
- **架構搜尋。** 自動搜尋能找到有競爭力的骨幹，但搜尋成本高，結果也取決於搜尋空間。

## 參考文獻

### 開創性論文

- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — 殘差連接使極深的 CNN 能夠訓練，是後續骨幹的基礎。
- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". arXiv:1905.11946 — 同時縮放深度、寬度與輸入解析度的複合縮放。
- Simonyan, K. & Zisserman, A. (2015). "Very Deep Convolutional Networks for Large-Scale Image Recognition". arXiv:1409.1556 — 堆疊小型 3×3 卷積的普通深層設計，即 VGG 的基礎。
- Huang, G., et al. (2017). "Densely Connected Convolutional Networks". arXiv:1608.06993 — 每一層都與其後所有層相連，重用特徵並改善梯度流。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". arXiv:2201.03545 — 逐步現代化的 ResNet，與 Transformer 基線相當。
