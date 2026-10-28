---
translation_reviewed: 2026-10-28
---

# DCGAN：深度卷積生成對抗網路

DCGAN 由 Radford、Metz 與 Chintala（2015）提出，是一組架構規則，使卷積 GAN 能在自然影像上穩定訓練。它保留[原始 GAN](../original-gan/index.md)的對抗目標，只改變網路結構，因此是[生成對抗網路](../index.md)主題中的代表性方法之一。

## 概述

在這項工作之前，以卷積網路建構的 GAN 很難擴展。訓練常常失敗，產生的影像雜訊多且難以辨認。作者搜尋了許多架構，找出一個能在多個資料集上穩定訓練的家族，並且能支援更高的解析度與更深的模型。論文的貢獻有三點：架構指引、把訓練後的判別器當作特徵擷取器使用，以及對潛在空間的分析，包括對輸入雜訊做簡單的向量運算。

## 核心概念

- **步幅卷積**：判別器以可學習的步幅卷積取代池化來降低取樣。生成器則以分數步幅卷積來升取樣。
- **批次正規化**：論文發現，它對深層生成器開始學習至關重要，因為它能防止所有樣本都塌縮到同一點。
- **激活函數**：生成器除輸出層使用 Tanh 外，其餘各層使用 ReLU；判別器各層都使用 LeakyReLU。
- **潛在輸入**：一個 100 維的雜訊向量，投影成一個小的空間張量，作為卷積堆疊的起點。
- **潛在空間運算**：論文指出，對輸入做簡單的向量運算，能方便地操控生成樣本的語意特質。

## 運作方式

論文把架構概括為四條指引：

1. 判別器以步幅卷積取代池化層，生成器則以分數步幅卷積取代。
2. 兩個網路都使用批次正規化。若套用到每一層會造成振盪與不穩定，因此生成器輸出層與判別器輸入層不使用。
3. 在較深的架構中移除全連接隱藏層。只有生成器的第一層，也就是把雜訊重塑的那一層，扮演稠密投影的角色。
4. 使用「關鍵概念」中列出的激活函數。

訓練細節與架構同樣重要。影像縮放到 \([-1, 1]\)。權重從零中心的常態分布初始化，標準差為 0.02。最佳化器是 Adam（Kingma 與 Ba，2014），學習率為 0.0002：作者發現建議的 0.001 太高，因此改用 0.0002。動量項 \(\beta_1\) 設為 0.5，因為預設的 0.9 會造成振盪。小批次大小為 128，LeakyReLU 的洩漏斜率為 0.2。

## 結果

論文以三種方式評估學到的表徵與生成影像。

- **CIFAR-10 分類。**以在 ImageNet-1k 上訓練的判別器特徵，匯集成 28,672 維的向量，再以線性 L2-SVM 分類。論文報告準確率為 82.8%。它勝過單層 K-means 基準的 80.6%，但不及 Exemplar CNN 的 84.3%（論文的表 1）。
- **SVHN 分類。**在只有 1,000 個標記樣本的情況下，同一套流程達到 22.48% 的測試錯誤率。論文指出，在當時的標記數量下，這是最先進的結果。
- **影像生成。**論文展示了 LSUN 臥室樣本，分別是資料經過一次完整訓練後與五個週期後的結果。作者以此說明，模型並非單純記住了訓練影像。

## 限制

- **主要依靠目視評估。**生成影像以肉眼判斷。量化結果衡量的是特徵，而不是樣本。
- **經驗性的指引。**這些規則是經由搜尋找到的，論文沒有提供它們為何能穩定訓練的理論。
- **敏感性。**為了避免振盪，需要若干設定，包括動量項與批次正規化的位置。
- **並非完整解決方案。**單靠架構無法保證穩定。Arjovsky 等人（2017）顯示，在標準 GAN 目標下，沒有批次正規化且濾波器數量固定的類 DCGAN 生成器表現很差。

## 開放問題

- 批次正規化與這些卷積限制為何有助於對抗博弈，理論上的原因是什麼？
- 在更大規模下，GAN 判別器的特徵與自監督方法的特徵相比如何？

## 參考文獻

### 開創性論文

- Radford, A., Metz, L. & Chintala, S. (2015). *Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks*. ICLR. https://arxiv.org/abs/1511.06434 — 論文本身：架構指引、訓練細節，以及本頁所述的 CIFAR-10 與 SVHN 特徵實驗。
- Goodfellow, I. et al. (2014). *Generative Adversarial Nets*. NeurIPS. https://arxiv.org/abs/1406.2661 — 原始框架，DCGAN 保留其目標，只改變網路結構。
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — 提出 Adam 最佳化器，DCGAN 的訓練依賴其動量設定。
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. ICML. https://arxiv.org/abs/1502.03167 — 提出批次正規化，這是 DCGAN 採用的三項架構要素之一。
- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. ICML. https://arxiv.org/abs/1701.07875 — 測試有與沒有批次正規化的類 DCGAN 生成器，並顯示沒有它時 GAN 訓練可能失敗。

### 綜述與教科書

- Creswell, A. et al. (2018). *Generative Adversarial Networks: An Overview*. IEEE Signal Processing Magazine. https://doi.org/10.1109/MSP.2017.2765202 — GAN 架構與應用的綜述，包括 DCGAN 之後出現的卷積設計。

### 講座與影片

- Goodfellow, I. (2016). *NIPS 2016 Tutorial: Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.00160 — 作者關於 GAN 訓練實務與架構選擇的教學報告，包括卷積生成器與判別器，並附有習題。
