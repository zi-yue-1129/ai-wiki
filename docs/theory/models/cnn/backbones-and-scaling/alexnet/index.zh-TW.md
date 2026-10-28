---
translation_reviewed: 2026-10-28
---

# AlexNet（Krizhevsky、Sutskever 與 Hinton，2012）

一個在 GPU 上訓練的大型深度卷積網路，使用非飽和（ReLU）神經元與 dropout 正則化。它在 ImageNet 分類上創下新的最佳結果，常被視為電腦視覺現代深度學習時代的起點。

## 概述

論文報告，其網路在 LSVRC-2010 基準上明顯優於先前的最佳結果。它顯示，在大量標註資料上以 GPU 訓練的深度卷積網路，能比作者所比較的系統更準確地分類 ImageNet。論文篇幅不長，但其選擇（ReLU 單元、dropout、GPU 訓練與資料擴增）被後來的多數視覺模型沿用。

## 關鍵概念

- **卷積層**：以學到的濾波器掃過影像的層，在各位置共享權重。
- **非飽和神經元（ReLU）**：激活函數 max(0, x)，對大的正輸入其梯度不會消失，因此比 tanh 等飽和單元訓練得更快。
- **Dropout**：訓練時，每個隱藏單元以機率 0.5 被設為零，以抑制單元之間的共同適應。
- **top-1 與 top-5 錯誤率**：測試影像中，正確標籤不是最高預測（top-1），或不在前五名預測中（top-5）的比例。

## 問題

將 130 萬張高解析度的 ImageNet 訓練影像分為 1,000 類，當時既有系統的表現遠遠不足。

## 核心想法

使用在 GPU 上訓練的大型深度卷積網路。非飽和神經元加速訓練，全連接層中的 dropout 則減少過擬合。

## 架構

網路有八個可學習的層：五個卷積層與三個全連接層。最後一層全連接層是 1,000 類的 softmax。根據摘要，網路約有 6,000 萬個參數與 50 萬個神經元。

## 核心方法

AlexNet 有兩個各自命名的組成部分。以下把它們與論文所取代的替代做法相比。

- **ReLU 非線性**：取代 tanh 或 sigmoid 單元。論文指出，使用 ReLU 的深度卷積網路，訓練速度比使用 tanh 的同類網路快數倍。
- **全連接層中的 dropout**：套用於前兩個全連接層，機率為 0.5。當時的替代做法是僅使用權重衰減，而論文並未以後者取代 dropout。

## 結果

在 LSVRC-2010 測試資料上，網路的 top-1 與 top-5 錯誤率分別為 39.7% 與 18.9%。摘要將此描述為明顯優於先前的最佳結果。

## 限制

- 證據來自單一網路與一個 2010 年的基準。其相對其他系統的優勢，只在該設定下有報告。
- 訓練依賴大量的標註資料與 GPU 算力，這在當時並不普遍。
- 此架構以當時的標準而言相當龐大。論文的設計選擇（例如各層的大小）後來被更深的網路簡化並改進，包括 [ResNet](../resnet/index.md)。

## 變體與更多變體

- **更深的後繼者**：VGG 與 ResNet 保留卷積的想法，並增加深度。[ResNet](../resnet/index.md)頁說明殘差連接的版本。
- **正則化的替代方案**：後來的模型常在網路的部分位置以批次正規化或權重衰減取代 dropout。

## 連結

- 母頁：[骨幹網路與縮放](../index.md)
- 同一主題的另一方法：[ResNet](../resnet/index.md)
- 訓練此類網路最常用的最佳化器是 [Adam](https://arxiv.org/abs/1412.6980)，見下方參考。

## 應用

- 影像分類，這正是 AlexNet 的設計目標，也是視覺中遷移學習的基礎。
- 特徵萃取：在 ImageNet 上預訓練的卷積層，常被重用為其他影像任務的特徵。

## 開放問題

- AlexNet 設計中哪些部分是必要的，哪些只是 2012 年硬體條件下的產物？
- 當目標任務的影像分布差異很大時，ImageNet 預訓練能帶來多少幫助？

## 參考文獻

### 開創性論文

- Krizhevsky, A., Sutskever, I. & Hinton, G. E.（2012）。*ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文，包含 39.7% 與 18.9% 的測試錯誤率，以及 6,000 萬參數的網路。
- He, K., Zhang, X., Ren, S. & Sun, J.（2015）。*Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — 殘差連接；摘要指出，它使極深的網路更容易最佳化，並能隨深度增加獲得更高準確率。
- Kingma, D. P. & Ba, J.（2015）。*Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — Adam 最佳化器，首次發表於 ICLR 2015，被廣泛用於訓練神經網路。
- Zhang, C., et al.（2017）。*Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — 顯示網路很容易擬合隨機標籤，挑戰了深度模型如何泛化的古典解釋。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A.（2016）。*Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 深度學習數學與實務的標準教科書，可免費線上閱讀。
- Zhang, A., Lipton, Z. C., Li, M. & Smola, A. J. *Dive into Deep Learning*. https://d2l.ai/ — 互動式線上教科書，每一節都是可執行的 notebook，適合實作練習。
