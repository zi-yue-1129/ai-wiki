---
related:
- brain-mind/neuroai
- theory/models/computer-vision
aliases:
  - Convolutional Neural Networks
  - CNN
  - 卷積神經網路
tags:
  - convolutional networks
  - architecture
  - computer vision
translation_reviewed: 2026-10-28
---

# 卷積神經網路

卷積神經網路（CNN）在網格的每個位置套用同一個小型濾波器來計算特徵。因為濾波器在各位置共用，它的參數遠少於同一輸入上的全連接層，並且內建了「有用的圖樣可以出現在任何位置」的假設。在 Transformer 興起之前，CNN 是多數影像模型的架構家族，至今仍常用於影像、音訊頻譜圖與時間序列。它的歸納偏置（局部性與平移等變性）最直接受到視覺皮層的啟發。這些任務的介紹見[電腦視覺](../computer-vision/index.md)。

## 核心想法

卷積層把學到的核在輸入上滑動，每個位置、每個濾波器產生一個輸出值。疊加多層會擴大感受野，因此較深的單元能看到輸入中更大的區域。池化或步幅卷積會降低空間解析度，最後一層把特徵轉成預測。最重要的設計選擇是卷積的形式，以及各層如何堆疊與縮放。這兩者即下面的兩個組件。

## 組件與變體

- [卷積變體](convolution-variants/index.md)：標準、空洞、深度可分離、轉置與可變形卷積，以及各自的取捨。
- [骨幹與縮放](backbones-and-scaling/index.md)：殘差連接、從 AlexNet 到 ConvNeXt 的演進，以及複合縮放。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| AlexNet | 2012 | 在 GPU 上訓練的大型深度卷積網路 | [AlexNet](backbones-and-scaling/alexnet/index.md) |
| 深度殘差學習（ResNet） | 2015 | 捷徑連接使極深的網路能夠訓練 | [ResNet](backbones-and-scaling/resnet/index.md) |
| 複合縮放（EfficientNet） | 2019 | 以單一係數同時縮放深度、寬度與解析度 | [EfficientNet](backbones-and-scaling/efficientnet/index.md) |
| U-Net | 2015 | 用於密集預測的帶跳接連線編碼器–解碼器 | [U-Net](unet/index.md) |

ResNet 讓極深的骨幹可以訓練，EfficientNet 則同時選擇深度、寬度與解析度，而不是逐一調整。

## 取捨

- **歸納偏置。** 局部性與權重共用使 CNN 在影像上資料效率高，但除非擴大感受野，否則會限制長程依賴的建模。
- **效率。** 深度可分離設計大幅減少運算，對行動與嵌入式裝置很重要。
- **與 Transformer 相比。** 視覺 Transformer 直接建模全域關係，但通常需要更多資料或預訓練。CNN 與 Transformer 的想法現在可以自由混合，例如 ConvNeXt 就在卷積網路中採用了 Transformer 的設計選擇。

## 應用範圍

影像分類、物件偵測與分割的骨幹、醫學影像、遙測，以及語音的前端，還有許多多模態系統的視覺編碼器。

## 相關連結

CNN 的感受野隨深度增長，這是[循環](../rnn/index.md)與[注意力](../transformer/attention-variants/index.md)家族以其他方式處理的性質。卷積在共享空間佈局中做局部濾波，也常與皮層的感受野相比較，見 [NeuroAI](../../../brain-mind/neuroai/index.md)：深度 CNN 的特徵已被拿來與視覺皮層的活動比較，但吻合是部分的。

## 未解問題與更多變體

- **長程脈絡。** 大核、空洞與注意力層都試圖擴展感受野。純 CNN 在密集預測上需要多少長程建模，尚無定論。
- **穩健性。** CNN 對小幅變換與紋理線索敏感，如何讓它們不變或更穩健，仍是開放問題。
- **設計架構。** 多數設計仍來自人工搜尋。自動搜尋方法存在，但相對於調校良好的人工設計，增益通常不大。

## 參考文獻

### 開創性論文

- LeCun, Y., Bottou, L., Bengio, Y. & Haffner, P. (1998). "Gradient-based learning applied to document recognition". *Proceedings of the IEEE* 86(11). https://doi.org/10.1109/5.726791 — 介紹以梯度下降訓練的 LeNet 系列卷積網路。
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — 殘差連接，使極深的 CNN 能夠訓練。
- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". arXiv:1905.11946 — 同時縮放深度、寬度與輸入解析度。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 9 章介紹卷積網路與卷積運算的標準說明。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". arXiv:2201.03545 — ConvNeXt，一個現代化的純 CNN，與 Transformer 基線相當。
