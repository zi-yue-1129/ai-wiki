---
translation_reviewed: 2026-10-28
---

# 殘差網路（He 等人，2015）

每個區塊學習輸入的殘差函數，並透過捷徑把輸入加回來，因此讓訊號原樣通過變得容易。

## 問題

非常深的網路難以最佳化，因此增加層數反而不再有幫助。

## 核心想法

每個區塊學習輸入的殘差函數，並透過捷徑把輸入加回去。讓訊號原樣通過因此容易學習。

## 方程式或演算法

對輸入 \(x\) 的區塊，

\[
y = \mathcal{F}(x, \{W_i\}) + x
\]

## 結果

網路深度最多 152 層，約為 VGG 網路的八倍，且複雜度較低。這些網路組成的集成模型在 ImageNet 測試集上達到 3.57% 錯誤率，並在 ILSVRC 2015 分類任務中獲得第一名。

## 限制

3.57% 來自集成模型，而非單一網路。恆等捷徑是論文所主張的設計選擇，並未證明它是最佳的。

## 連結

- 母頁：[深度學習](../index.md)
- 同一主題的另一方法：[AlexNet](../alexnet/index.md)

## 參考文獻

### 開創性論文

- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文，其在 ImageNet 上的成果開啟了現代深度學習時代。
- He, K., et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — 殘差連接，使極深的網路得以訓練。
- Kingma, D. P. & Ba, J. (2014). *Adam: A Method for Stochastic Optimization*. arXiv. https://arxiv.org/abs/1412.6980 — Adam 最佳化器，至今仍是訓練許多神經網路的預設選擇。
- Zhang, C., et al. (2017). *Understanding deep learning requires rethinking generalization*. ICLR. https://arxiv.org/abs/1611.03530 — 顯示網路可以擬合隨機標籤，挑戰了深度模型如何泛化的古典解釋。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 深度學習數學與實務的標準教科書，可免費線上閱讀。
- Zhang, A., Lipton, Z. C., Li, M. & Smola, A. J. *Dive into Deep Learning*. https://d2l.ai/ — 附有可執行程式碼的互動式線上教科書，適合實作練習。
