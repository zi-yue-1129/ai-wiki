---
related:
- theory/models/mlp
- theory/models/transformer
aliases:
  - Gaussian Error Linear Units
  - GELU
  - 高斯誤差線性單元
tags:
  - activation functions
  - feedforward networks
  - transformers
translation_reviewed: 2026-10-28
---

# 高斯誤差線性單元

高斯誤差線性單元（GELU）是一種平滑的激活函數，由 Hendrycks 與 Gimpel 在 2016 年的論文「Gaussian Error Linear Units (GELUs)」中提出。它以標準常態累積分布函數在該輸入處的值為權重來加權每個輸入，而不是在零處把輸入截斷。現在它常見於 Transformer 的前饋區塊。

## 問題

激活函數通常被視為固定的架構決定，與 dropout 等隨機正則化方法分開考量，但兩者都影響神經元的輸入有多少能傳到輸出。

## 核心想法

ReLU 依輸入的正負號決定是否放行該輸入。GELU 則以輸入的數值本身作為權重。它可以理解為一個隨機遮罩的期望輸出：遮罩要麼保留輸入不變，要麼把它設為零，而保留輸入的機率是標準常態的 CDF。較大的輸入被保留的機率較高，而且函數在各處都是平滑的。

## 方程式或演算法

精確形式為

\[
\mathrm{GELU}(x) = x\,\Phi(x) = x \cdot \tfrac{1}{2}\left[1 + \mathrm{erf}\!\left(\tfrac{x}{\sqrt{2}}\right)\right],
\]

其中 \(\Phi\) 是標準常態 CDF。論文的 tanh 近似式為

\[
0.5\,x\left(1 + \tanh\!\left[\sqrt{2/\pi}\,\left(x + 0.044715\,x^3\right)\right]\right),
\]

論文的所有實驗都使用這個近似式。

## 結果

在 CIFAR-10 上，採用 9 層 CNN 且不做資料擴增時，GELU 的測試誤差中位數為 7.89%，ReLU 為 8.16%，ELU 為 8.41%。在 CIFAR-100 上，採用 40 層寬殘差網路時，GELU 為 20.74%，ReLU 為 21.77%。

## 限制

tanh 形式是近似，這些近似以精確度換取速度。作者建議搭配帶動量的最佳化器。他們的 MNIST 結果只出現在圖中，因此這裡不引用其數值。

## 相關連結

GELU 常見於 [Transformer](../../transformer/index.md) 的前饋區塊，也是 [MLP](../index.md) 家族頁面討論的激活選擇之一。同一頁面一併討論的正規化方法，見 [層正規化](../layer-normalisation/index.md)。

## 未解問題與更多變體

- **激活函數的選擇。** 新激活函數帶來的經驗增益，在不同任務間往往小且不一致，原因尚未完全理解。
- **精確形式與近似形式。** tanh 近似以精確度換取速度，因此在兩者之間如何選擇，是每個實作的實務決定。
- **隨機遮罩的解讀。** 遮罩的解釋能否說明 GELU 在本論文實驗之外的表現，仍是開放問題。

## 參考文獻

### 開創性論文

- Hendrycks, D. & Gimpel, K. (2016). "Gaussian Error Linear Units (GELUs)". arXiv:1606.08415 — GELU 激活函數，被許多 Transformer 模型採用。
- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). "Learning representations by back-propagating errors". *Nature* 323: 533–536. https://doi.org/10.1038/323533a0 — 推廣了以反向傳播訓練具隱藏層的多層網路。
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — 殘差連接，使深層網路能夠訓練。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 6 章涵蓋前饋網路、激活函數與通用逼近結果。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). "Layer Normalization". arXiv:1607.06450 — 在特徵上而非批次上做正規化。
