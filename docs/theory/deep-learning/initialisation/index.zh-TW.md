---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/normalisation
  - theory/models/transformer
tags:
  - initialisation
  - signal propagation
  - hyperparameters
aliases:
  - 權重初始化
  - 訊號傳播
  - 參數初始化
  - Weight initialisation
---

# 權重初始化與訊號傳播

網路權重的起始值決定了訊號與梯度能否順利通過許多層。如果激活值隨深度呈指數成長或衰減，訓練會在開始之前就停滯或發散。初始化方案會選擇權重的變異數，使訊號維持穩定的尺度；而訊號傳播的分析則解釋了為何某些架構比其他架構更容易開始訓練。

## 概觀

網路透過反覆的線性映射與非線性函數計算輸出。在初始化時，權重是隨機的，因此每一層之後激活值的大小是許多隨機因子的乘積。妥善選擇變異數，可使這個乘積維持在接近一的水準。殘差連接與正規化層會改變這個情況，使許多原本會失敗的初始化方式得以運作。

## 關鍵概念

- **變異數保持（variance preservation）**：一個設計目標，使激活值與梯度的變異數在各層之間大致保持不變。
- **扇入與扇出（fan-in and fan-out）**：一層的輸入與輸出數量，決定了尺度良好的權重矩陣的變異數。
- **混沌邊緣（edge of chaos）**：有序與混沌訊號傳播之間的邊界區域，深層網路在此最容易訓練。
- **超參數轉移（hyperparameter transfer）**：把在小模型上調好的超參數，重用於大模型。

## 運作方式

對於權重變異數為 $\sigma^2$ 的隨機線性層，輸出的變異數按 $n\sigma^2$ 成長，其中 $n$ 是扇入。Glorot 與 Bengio 選擇了一個能平衡前向訊號與反向梯度的變異數，使用扇入與扇出的平均值 [(Glorot and Bengio, 2010)](https://proceedings.mlr.press/v9/glorot10a.html)。對於整流線性單元，有一半的輸入會被設為零，因此變異數必須加倍。He 等人為此情況推導出一種初始化方式，使非常深的整流網路得以訓練 [(He et al., 2015)](https://arxiv.org/abs/1502.01852)。

Saxe 等人研究了深度線性網路的學習動態，並在某些初始條件下找到學習過程隨時間變化的精確解 [(Saxe, McClelland and Ganguli, 2013)](https://arxiv.org/abs/1312.6120)。Schoenholz 等人以平均場理論研究隨機網路中的訊號如何傳播，並找出輸入之間相關性消失所經過的深度尺度，這是混沌邊緣觀點的基礎 [(Schoenholz et al., 2016)](https://arxiv.org/abs/1611.01232)。

## 關鍵方法

- [Glorot（Xavier）初始化](glorot-initialisation.zh-TW.md)：選擇能平衡前向與反向訊號的變異數。
- [He 初始化](he-initialisation.zh-TW.md)：為整流激活調整的變異數。
- [最大更新參數化（muP）](mup.zh-TW.md)：一種參數化方式，使最佳超參數在寬度增加時保持穩定。

## 殘差連接與正規化

殘差連接會把區塊的輸入加到其輸出上，使恆等路徑能把訊號帶過許多層。正規化則使每個區塊內激活值的尺度保持穩定。兩者結合後，初始化的選擇變得較不關鍵，這也是非常深的網路得以訓練的部分原因。這種互動關係見[正規化](../normalisation/index.zh-TW.md)。

## 縮放與超參數轉移

隨著模型變寬，最佳學習率常常會改變，使大規模調參變得昂貴。muP 是一種參數化方式，據報導在此參數化下，小模型上的最佳超參數對寬模型仍接近最佳。這使得可以在小模型上調參，再轉移到大模型 [(Yang et al., 2022)](https://arxiv.org/abs/2203.03466)。

## 關聯

初始化必須保持穩定的梯度，其計算方式如[自動微分](../../math/automatic-differentiation/index.zh-TW.md)所述。Transformer 特有的正規化位置見[Transformer](../../models/transformer/index.zh-TW.md)，神經網路基礎見[深度學習](../index.zh-TW.md)。

## 應用

在開始訓練任何深度網路時，包括非常深的卷積與殘差網路；以及透過轉移方法為大型語言模型選擇學習率。

## 開放問題

- 混沌邊緣是否為具有注意力與閘控機制的架構，應該追求的初始化目標？
- muP 等縮放規則能推廣到多遠的新架構與最佳化器？

## 參考文獻

### 奠基性論文

- Glorot 與 Bengio，*Understanding the difficulty of training deep feedforward neural networks*，Proceedings of the 13th International Conference on Artificial Intelligence and Statistics（2010）。https://proceedings.mlr.press/v9/glorot10a.html — 平衡前向與反向訊號的變異數規則。
- He、Zhang、Ren 與 Sun，*Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*（2015）。https://arxiv.org/abs/1502.01852 — 為整流網路推導出初始化方式。
- Saxe、McClelland 與 Ganguli，*Exact solutions to the nonlinear dynamics of learning in deep linear neural networks*（2013）。https://arxiv.org/abs/1312.6120 — 深度線性網路的精確學習動態。
- Schoenholz、Gilmer、Ganguli 與 Sohl-Dickstein，*Deep Information Propagation*（2016）。https://arxiv.org/abs/1611.01232 — 深層隨機網路中訊號傳播的平均場分析。
- Yang 等人，*Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*（2022）。https://arxiv.org/abs/2203.03466 — muP 參數化與零樣本超參數轉移。
