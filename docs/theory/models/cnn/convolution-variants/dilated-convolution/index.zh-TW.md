---
related:
- theory/models/cnn/convolution-variants
- theory/models/cnn
aliases:
  - Dilated Convolution
  - Atrous Convolution
  - 空洞卷積
tags:
  - convolution
  - receptive field
  - dense prediction
translation_reviewed: 2026-10-28
---

# 空洞卷積

空洞卷積把核的取樣點拉開間隔，使一層能涵蓋輸入中更大的區域，而且不增加參數。Yu 與 Koltun（2015）在論文 "Multi-Scale Context Aggregation by Dilated Convolutions" 中，以堆疊的空洞層做密集預測，讓感受野隨深度呈指數成長，同時特徵圖維持全解析度。

## 問題

密集預測（例如替影像的每個像素標上類別）需要每個輸出都看見很大的脈絡。一疊普通的 3×3 層，每層只把感受野增加兩個像素。池化或步幅層可以擴大感受野，但會降低輸出的空間解析度。

## 核心想法

空洞（或稱 atrous）卷積在核的取樣點之間插入間隔。空洞率為 \(l\) 時，位置 \(\mathbf{p}\) 的輸出會對所有滿足 \(\mathbf{s} + l\mathbf{t} = \mathbf{p}\) 的輸入 \(\mathbf{s}\) 求和；\(l = 1\) 即為一般卷積。若空洞率逐層加倍（1、2、4、8……），感受野就隨層數指數成長，而每層的權重數量與特徵圖大小都不變。

## 方程式或演算法

對於離散特徵圖 \(F\) 與核 \(k\)，論文把 \(l\) 空洞卷積定義為

\[
(F *_{l} k)(\mathbf{p}) = \sum_{\mathbf{s} + l\mathbf{t} = \mathbf{p}} F(\mathbf{s})\, k(\mathbf{t})，
\]

並指出一般的離散卷積就是 1 空洞卷積。論文的脈絡模組堆疊 3×3 的層，空洞率依序為 1、1、2、4、8、16、1，最後接一個 1×1 層。論文給出 \(F_{i+1}\) 中每個元素的感受野為 \((2^{i+2}-1) \times (2^{i+2}-1)\)，因此 \(F_1\)、\(F_2\)、\(F_3\) 的感受野分別為 3×3、7×7 與 15×15。論文的表 1 列出八層的感受野邊長為 3、5、9、17、33、65、67、67。論文在第 6 層之後停止指數成長，因為其前端輸出為 64×64 的特徵圖。

## 結果

在 PASCAL VOC 2012 驗證集上，論文報告僅有前端時 mIoU 為 69.8，加入基本脈絡模組為 71.3，加入大型脈絡模組為 72.1。加入 CRF-RNN 後，驗證集最佳結果為 73.9。測試集上，大型脈絡模組為 73.5，加上 CRF-RNN 為 75.3。在 CamVid 上，論文的 Dilation8 模型為 65.3，附錄中的 DeepLab-LFOV 為 61.6。

## 限制

論文自己指出：最初訓練脈絡模組的嘗試，未能提升準確率；將脈絡模組與前端聯合訓練，也沒有帶來顯著改善。基本模組的特徵圖沒有正規化，模組內部也沒有定義損失函數。作者還表示，目前最先進的語意分割系統仍有很大的進步空間。上文提到的網格偽影問題，不在論文列出的這些限制之中。

## 相關連結

[卷積變體](../index.md)頁面把空洞與其他形式並列比較，[CNN 家族](../../index.md)頁面說明它在 CNN 組件中的位置。以全解析度擴大脈絡的想法，也出現在[注意力變體](../../../transformer/attention-variants/index.md)中，局部窗口與全域注意力都能擴大每個輸出所見的範圍。涵蓋分割等密集任務的背景見[電腦視覺](../../../computer-vision/index.md)。改用學習取樣位置、而非固定間隔的做法，見[可變形卷積](../deformable-convolution/index.md)。

## 未解問題與更多變體

- **網格效應。** 堆疊的空洞可能使某些輸入像素從未被取樣。卷積變體頁面指出，後來的設計以混合的空洞率來處理；如何選擇這些空洞率，仍無定論。
- **脈絡模組的訓練。** 論文報告最初的訓練嘗試沒有提升準確率，聯合訓練也沒有顯著改善，因此訓練方式的影響仍未充分探討。
- **長程脈絡。** 空洞堆疊擴展了脈絡，但每一層仍是局部的。它能否在需要長程關係的任務上匹敵全域注意力，仍未確定。

## 參考文獻

### 開創性論文

- Yu, F. & Koltun, V. (2015). "Multi-Scale Context Aggregation by Dilated Convolutions". [arXiv:1511.07122](https://arxiv.org/abs/1511.07122) — 用於密集預測的空洞卷積，感受野隨深度指數成長。
- Dai, J., et al. (2017). "Deformable Convolutional Networks". [arXiv:1703.06211](https://arxiv.org/abs/1703.06211) — 學習取樣偏移量，使卷積能適應物件形狀。
- Chollet, F. (2016). "Xception: Deep Learning with Depthwise Separable Convolutions". [arXiv:1610.02357](https://arxiv.org/abs/1610.02357) — 顯示把空間與通道混合分解後，能以較低成本超越 Inception 式設計。
- Chen, L.-C., et al. (2016). "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs". [arXiv:1606.00915](https://arxiv.org/abs/1606.00915) — 空洞卷積搭配全連接條件隨機場，用於密集分割。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 9 章介紹卷積網路與卷積運算的標準說明。

### 講座與影片

（本頁尚未核對）

### 文章與文件

（本頁尚未核對）
