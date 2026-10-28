---
translation_reviewed: 2026-10-28
---

# AlexNet（Krizhevsky、Sutskever 與 Hinton，2012）

一個在 GPU 上訓練的大型深度卷積網路，使用非飽和神經元與一種新的正則化方法。

## 問題

將 130 萬張高解析度的 ImageNet 影像分為 1,000 類，當時既有系統的表現遠遠不足。

## 核心想法

在 GPU 上訓練的大型深度卷積網路。使用非飽和神經元加速訓練，並為全連接層加入新的正則化方法以減少過擬合。

## 架構

五個卷積層（部分後接最大池化）與兩個全連接層，最後是 1,000 類的 softmax，約有 6,000 萬個參數。

## 結果

在 LSVRC-2010 測試資料上，top-1 與 top-5 錯誤率分別為 39.7% 與 18.9%，作者認為明顯優於先前的最佳結果。

## 限制

證據來自單一網路與 2010 年的基準資料集。訓練依賴大量的標註資料與 GPU 算力，這在當時並不普遍。

## 連結

- 母頁：[深度學習](../index.md)
- 同一主題的另一方法：[CNN 章節中的 ResNet](../../models/cnn/backbones-and-scaling/resnet/index.md)

## 參考文獻

### 開創性論文

- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文，其在 ImageNet 上的成果開啟了現代深度學習時代。
- He, K., et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — 殘差連接，使極深的網路得以訓練。
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization*. arXiv. https://arxiv.org/abs/1412.6980 — Adam 最佳化器，至今仍是訓練許多神經網路的預設選擇。
- Zhang, C., et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — 顯示網路可以擬合隨機標籤，挑戰了深度模型如何泛化的古典解釋。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 深度學習數學與實務的標準教科書，可免費線上閱讀。
- Zhang, A., Lipton, Z. C., Li, M. & Smola, A. J. *Dive into Deep Learning*. https://d2l.ai/ — 附有可執行程式碼的互動式線上教科書，適合實作練習。
