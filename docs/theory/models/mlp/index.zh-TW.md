---
related:
- theory/deep-learning
aliases:
  - Multilayer Perceptron
  - MLP
  - Feedforward Network
  - 多層感知器
  - 前饋網路
tags:
  - feedforward networks
  - architecture
  - deep learning
translation_reviewed: 2026-10-28
---

# 多層感知器

多層感知器（MLP），又稱前饋網路，是把仿射映射與非線性激活函數一層層堆疊，從輸入到輸出沒有迴路。它是最簡單的深度架構；在緊緻集上，只要寬度足夠，它就能以任意精度逼近連續函數。其他家族也由 MLP 的零件組成：Transformer 內的前饋區塊、CNN 與 RNN 的讀出頭，以及許多新模型中的混合層。因此理解 MLP 是理解其他所有家族的基礎。

## 核心想法

一層計算 \(h = \sigma(Wx + b)\)，其中 \(\sigma\) 是非線性激活。堆疊這樣的層，就是簡單函數的組合，並以反向傳播端到端訓練。一般的訓練理論，例如最佳化與泛化，見[深度學習](../../deep-learning/index.md)。本頁介紹定義架構本身的設計選擇。

## 組件與變體

- **激活函數。** sigmoid 與 tanh 會飽和，因此多數現代網路使用整流或平滑的變體。例如 GELU 把輸入乘以高斯累積分布函數，常見於 Transformer（Hendrycks & Gimpel, 2016）。
- **正規化。** 批次正規化在批次上做正規化，適合 CNN；層正規化在特徵上做正規化，不依賴批次統計，適合序列模型（Ba 等人，2016）。
- **殘差連接。** 把輸入加回區塊的輸出，使深層堆疊能夠訓練。這個設計是為 CNN 提出的，現在已用於各個家族（He 等人，2015）。
- **寬度與深度。** 寬而淺的 MLP 與窄而深的 MLP 可以表示相近的函數，但較深的網路通常以少得多的參數做到這點。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| 高斯誤差線性單元（GELU） | 2016 | 以高斯累積分布函數加權輸入的平滑激活函數 | [GELU](gelu/index.md) |
| 層正規化 | 2016 | 對每個樣本的特徵做正規化，不依賴批次統計 | [層正規化](layer-normalisation/index.md) |

GELU 是 ReLU 的平滑替代方案。層正規化不依賴批次統計，因此適合序列模型。

## 取捨

- **通用性與結構。** MLP 不對輸入的結構做假設，因此對於有結構的輸入，需要比 CNN 或圖網路更多的資料。
- **參數成本。** 稠密層的參數量隨寬度呈二次增長，這也是大型模型的前饋區塊常被稀疏或專家式設計取代的原因。
- **可解釋性。** 稠密網路難以直接檢視，這促成了 [Transformer](../transformer/index.md) 家族中相關的可解釋性研究。

## 應用範圍

表格資料預測、Transformer 的前饋區塊、嵌入編碼器，以及多數其他架構的輸出頭。

## 相關連結

MLP 區塊出現在 [CNN](../cnn/index.md)、[RNN](../rnn/index.md) 與 [Transformer](../transformer/index.md) 家族中。為 MLP 所做的殘差與正規化選擇，與 [骨幹與縮放](../cnn/backbones-and-scaling/index.md) 頁面共用。與大腦的早期連結來自 McCulloch–Pitts 神經元與感知器，它們是這個家族的歷史前身。

## 未解問題與更多變體

- **大型模型中的前饋區塊。** 在規模上，稠密前饋層是否是參數的最佳用途，或混合專家與結構化層是否更好，仍在測試中。
- **激活函數的選擇。** 新激活函數帶來的經驗增益，在不同任務間往往小且不一致，原因尚未完全理解。
- **表達力與可學習性。** 通用逼近說明的是能表示什麼，而不是能從資料學到什麼。這個差距是該家族的核心開放問題。

## 參考文獻

### 開創性論文

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). "Learning representations by back-propagating errors". *Nature* 323: 533–536. https://doi.org/10.1038/323533a0 — 推廣了以反向傳播訓練具隱藏層的多層網路。
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — 殘差連接，使深層網路能夠訓練。
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). "Layer Normalization". arXiv:1607.06450 — 在特徵上而非批次上做正規化。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 6 章涵蓋前饋網路、激活函數與通用逼近結果。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Hendrycks, D. & Gimpel, K. (2016). "Gaussian Error Linear Units (GELUs)". arXiv:1606.08415 — GELU 激活函數，被許多 Transformer 模型採用。
