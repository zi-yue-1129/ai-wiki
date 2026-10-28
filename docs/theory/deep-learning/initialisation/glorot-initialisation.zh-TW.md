---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/initialisation
tags:
  - Glorot initialisation
  - Xavier initialisation
  - initialisation
aliases:
  - Glorot 初始化
  - Xavier 初始化
  - Glorot initialization
---

# Glorot（Xavier）初始化

Glorot 初始化依據線性層的扇入與扇出來選擇權重的變異數，使前向傳播的訊號與反向傳播的梯度維持相近的尺度。它是為使用飽和激活函數（如 sigmoid 與雙曲正切）的網路而提出的，後來成為許多層的預設值。

## 概觀

[本章](index.zh-TW.md)涵蓋一般的初始化。本頁說明 Glorot 規則。論文分析了為何深層網路在標準的隨機初始化下訓練效果不佳，並提出一個能使激活值與梯度保持在有用範圍內的尺度。

## 問題

若權重從固定分布中抽取，在使用飽和非線性函數的深層網路中，激活值會逐漸漂移到激活函數的平坦區域，那裡的梯度會消失。論文探討權重的變異數應如何依層的大小而變，以避免此問題。

## 核心想法

選擇權重變異數，使前向變異數保持不變（這需要包含扇入 $n_{\text{in}}$ 的變異數），並使反向變異數保持不變（這需要包含扇出 $n_{\text{out}}$ 的變異數）。Glorot 與 Bengio 取兩者的平均。權重依此變異數以均勻分布或常態分布抽取。

## 方程式

對於一個具有 $n_{\text{in}}$ 個輸入與 $n_{\text{out}}$ 個輸出的層，均勻形式的抽取方式為

$$W \sim \mathcal{U}\left[-\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}},\; \sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}\right]$$

其變異數為 $2 / (n_{\text{in}} + n_{\text{out}})$。常態形式使用相同的變異數。

## 結果

論文顯示，在使用 sigmoid 與 tanh 激活的深層網路上，所提方案比當時常用的固定尺度初始化更可靠地完成訓練。具體數字見其實驗。

## 限制

- 推導假設的是線性層，且激活函數在零附近近似線性，因此對於整流激活的準確度較低。[He 初始化](he-initialisation.zh-TW.md)處理了這種情況。
- 它沒有考慮殘差連接或正規化，而這些都會改變訊號的尺度。

## 關聯

此規則是 [He 初始化](he-initialisation.zh-TW.md)的起點。訊號傳播的整體圖像見[本章](index.zh-TW.md)。變異數論證背後的梯度計算見[自動微分](../../math/automatic-differentiation/index.zh-TW.md)。

## 應用

許多框架層的預設初始化，尤其是使用 tanh 或 sigmoid 激活的全連接與循環層。

## 開放問題

- 如何把 Glorot 式的尺度推廣到注意力與閘控層？
- 對於使用現代最佳化器訓練的超寬模型，它仍是正確的預設值嗎？

## 參考文獻

### 奠基性論文

- Glorot 與 Bengio，*Understanding the difficulty of training deep feedforward neural networks*，Proceedings of the 13th International Conference on Artificial Intelligence and Statistics（2010）。https://proceedings.mlr.press/v9/glorot10a.html — 原始分析與扇入、扇出的變異數規則。
- He、Zhang、Ren 與 Sun，*Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*（2015）。https://arxiv.org/abs/1502.01852 — 針對 ReLU 修正 Glorot 尺度的整流變體。
- Schoenholz、Gilmer、Ganguli 與 Sohl-Dickstein，*Deep Information Propagation*（2016）。https://arxiv.org/abs/1611.01232 — 隨機深層網路中變異數傳播的平均場分析。
- Saxe、McClelland 與 Ganguli，*Exact solutions to the nonlinear dynamics of learning in deep linear neural networks*（2013）。https://arxiv.org/abs/1312.6120 — 深度線性網路的學習動態，與尺度選擇相關。
- Ioffe 與 Szegedy，*Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*（2015）。https://arxiv.org/abs/1502.03167 — 降低對初始尺度依賴的正規化方法。
