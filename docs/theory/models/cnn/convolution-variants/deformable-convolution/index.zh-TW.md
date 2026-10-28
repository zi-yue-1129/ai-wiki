---
related:
- theory/models/cnn/convolution-variants
- theory/models/cnn
aliases:
  - Deformable Convolution
  - DCN
  - 可變形卷積
tags:
  - convolution
  - object detection
  - spatial adaptation
translation_reviewed: 2026-10-28
---

# 可變形卷積

可變形卷積讓卷積的取樣位置可以移動。Dai 等人（2017）在 "Deformable Convolutional Networks" 中為每個取樣點學習一個偏移量，使核能貼合物件的形狀。論文報告了物件偵測與語意分割上的增益。

## 問題

一般卷積在每個輸出位置周圍取固定的網格，因此它的感受野在各處都是同一形狀。物件的形狀、尺度與姿態各不相同，一個固定網格無法同時符合所有物件。Dai 等人讓取樣網格本身可以學習，使每個輸出都能從適應物件的區域取樣。

## 核心想法

規則網格上的每個取樣點，都會得到一個額外的學習偏移量，由一個獨立的偏移層預測，該層讀取同一張輸入特徵圖。偏移層以零權重開始，因此運算一開始就是一般卷積。由於偏移量通常是小數，輸入會以雙線性內插取樣，使運算保持可微。同樣的偏移想法也套用在 RoI 池化上，讓池化的分箱能隨物件移動。

## 方程式或演算法

對於規則網格 \(\mathcal{R}\) 上的一般卷積，論文寫為

\[
\mathbf{y}(\mathbf{p}_0) = \sum_{\mathbf{p}_n \in \mathcal{R}} \mathbf{w}(\mathbf{p}_n)\, \mathbf{x}(\mathbf{p}_0 + \mathbf{p}_n)。
\]

可變形卷積為 \(N = |\mathcal{R}|\) 個取樣點各加上一個學習的偏移量 \(\Delta\mathbf{p}_n\)：

\[
\mathbf{y}(\mathbf{p}_0) = \sum_{\mathbf{p}_n \in \mathcal{R}} \mathbf{w}(\mathbf{p}_n)\, \mathbf{x}(\mathbf{p}_0 + \mathbf{p}_n + \Delta\mathbf{p}_n)。
\]

小數位置以雙線性內插取樣，每個軸的權重為 \(g(a,b) = \max(0, 1 - |a - b|)\)。對於可變形 RoI 池化，論文給出 \(\mathbf{y}(i,j) = \sum_{\mathbf{p} \in \text{bin}(i,j)} \mathbf{x}(\mathbf{p}_0 + \mathbf{p} + \Delta\mathbf{p}_{ij}) / n_{ij}\)，其中 \(n_{ij}\) 為分箱內的像素數，偏移量乘上 \(\gamma = 0.1\) 的縮放。

## 結果

論文的結果除非另有註明，皆使用 ResNet-101。在 COCO test-dev 上，Faster R-CNN 的 mAP@[0.5:0.95] 從 29.4 升至 33.1，R-FCN 從 30.8 升至 34.5；採多尺度測試與迭代框平均的 R-FCN 則從 35.5 升至 37.5。論文把三組主要比較的相對提升描述為「11%、13% 與 12%」。在分割方面，以 DeepLab 為基礎，PASCAL VOC 的 mIoU 從 69.7 升至 75.3，Cityscapes 從 70.4 升至 75.2。在 PASCAL VOC 2007 上，R-FCN 的 mAP@0.5 從 80.0 升至 82.6。額外成本很小：Faster R-CNN 的參數量從 58.3M 增至 59.9M，前向時間從 0.147 秒增至 0.192 秒，量測環境為 Intel E5-2650 v2 CPU 與 Nvidia K40 GPU。

## 限制

論文沒有獨立的限制章節，但正文提到幾項注意事項。可變形卷積只套用在最後幾個卷積層，論文選定三層為「良好的折衷」。增益隨深度飽和：DeepLab 在 3 個可變形層時飽和，其他模型在 6 個時飽和。可變形 RoI 池化目前使用大小相同的分箱，並且忽略部件之間的空間關係，論文認為這比可變形部件模型（DPM）更簡單。消融實驗使用固定、預先計算的 RPN 提案，且不共享特徵。額外成本的數字是在一組 CPU 與 GPU 環境下的實際時間，因此並未量測上文中某些硬體上的主要成本，也就是不規則記憶體存取。

## 相關連結

[卷積變體](../index.md)頁面把可變形卷積列為學習取樣位置的形式，[CNN 家族](../../index.md)頁面說明它是 CNN 的組件之一。[空洞卷積](../dilated-convolution/index.md)頁面以間隔固定取樣模式，而非學習它；[深度可分離卷積](../depthwise-separable-convolution/index.md)頁面則改變通道的混合方式，而非取樣位置。論文報告增益的偵測與分割任務，見[電腦視覺](../../../computer-vision/index.md)頁面。[注意力變體](../../../transformer/attention-variants/index.md)頁面涵蓋與「層該看哪裡」相關的想法。

## 未解問題與更多變體

- **不規則存取的成本。** 論文量測的額外成本在其自身硬體上很小，但上文指出，在某些加速器上不規則記憶體存取才是主要成本。對硬體友善的學習式取樣仍是待解問題。
- **深度飽和。** 論文報告增益在 DeepLab 為 3 層、其他模型為 6 層後飽和。改變偏移層的設計能否延後這種飽和，仍是開放問題。
- **部件之間的關係。** 可變形 RoI 池化忽略部件之間的空間關係，論文把它視為相對 DPM 的簡化。加入這些關係是否有幫助，論文並未測試。

## 參考文獻

### 開創性論文

- Dai, J., et al. (2017). "Deformable Convolutional Networks". arXiv:1703.06211 — 學習取樣偏移量，使卷積能適應物件形狀。
- Yu, F. & Koltun, V. (2015). "Multi-Scale Context Aggregation by Dilated Convolutions". arXiv:1511.07122 — 用於密集預測的空洞卷積，感受野隨深度指數成長。
- Chen, L.-C., et al. (2016). "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs". arXiv:1606.00915 — 空洞卷積搭配全連接條件隨機場，用於密集分割。
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — 殘差連接，使極深的 CNN 能夠訓練。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 9 章介紹卷積網路與卷積運算的標準說明。

### 講座與影片

（本頁尚未核對）

### 文章與文件

（本頁尚未核對）
