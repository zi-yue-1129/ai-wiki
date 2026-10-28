---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/normalisation
  - theory/models/cnn
tags:
  - regularisation
  - dropout
  - generalisation
aliases:
  - 隨機正則化
  - 丟棄法
  - Dropout
  - Stochastic regularisation
---

# 丟棄法與隨機正則化

丟棄法（dropout）及相關方法透過在訓練時注入隨機性來正則化網路。單元、路徑或整個訓練樣本會被隨機移除或混合，使模型無法依賴任何單一特徵。這些方法能減少過擬合，也常被解讀為模型平均與貝氏推論的近似。

## 概觀

當模型在訓練集上擬合得很好，但泛化得很差時，就會發生過擬合。傳統的正則化器會懲罰較大的權重。隨機方法則以不同的方式正則化：它們在訓練信號中隨機加入變化，使學到的函數必須在網路或資料的許多擾動版本上都能運作。

## 關鍵概念

- **丟棄法（dropout）**：訓練時隨機把一部分激活值設為零，並縮放其餘的值，使期望輸出不變。
- **隨機深度（stochastic depth）**：訓練時隨機跳過整個殘差區塊。
- **混合增強（mixup）**：在成對樣本及其標籤的凸組合上訓練。
- **標籤平滑（label smoothing）**：以軟化的分布取代獨熱（one-hot）目標，抑制過度自信的預測。
- **貝氏解釋（Bayesian interpretation）**：把丟棄法視為對模型權重的近似推論。

## 運作方式

在原始的丟棄法中，每個訓練步驟中每個單元以機率 $p$ 被保留，測試時則使用所有單元，並把權重縮放至相符。Srivastava 等人顯示，這能在多種架構與任務上減少過擬合 [(Srivastava et al., 2014)](https://jmlr.org/papers/v15/srivastava14a.html)。隨機深度把同樣的想法套用到層：殘差區塊被隨機跳過，使訓練時的網路變短，也因此加速訓練 [(Huang et al., 2016)](https://arxiv.org/abs/1603.09382)。

混合增強改變的是資料，而不是網路。兩個樣本及其標籤以隨機權重混合，鼓勵訓練點之間呈現線性行為 [(Zhang et al., 2017)](https://arxiv.org/abs/1710.09412)。標籤平滑改變的是目標。Szegedy 等人在 Inception v3 的研究中使用它來降低過度自信 [(Szegedy et al., 2016)](https://arxiv.org/abs/1512.00567)。

## 關鍵方法

- [丟棄法](dropout-method.zh-TW.md)：隨機移除單元，即原始方法及其縮放規則。
- [混合增強](mixup.zh-TW.md)：訓練成對樣本的凸組合。
- [隨機深度](stochastic-depth.zh-TW.md)：隨機跳過殘差區塊。

## 解釋

丟棄法可以被理解為訓練一組共享權重的稀疏網路所構成的集成。Gal 與 Ghahramani 指出，在測試時套用的丟棄法可以解釋為近似的貝氏推論，因此能透過重複的隨機預測估計模型的不確定性 [(Gal and Ghahramani, 2016)](https://arxiv.org/abs/1506.02142)。這些解釋很有用，但都只是近似，確切的關聯取決於模型與丟棄率的選擇。

## 關聯

[正規化層](../normalisation/index.zh-TW.md)在訓練期間也具有正則化的效果。卷積網路在分類器頭部使用丟棄法，並在深層殘差堆疊中使用隨機深度；見[卷積神經網路](../../models/cnn/index.zh-TW.md)。不確定性背後的統計概念見[機率與統計](../../math/index.zh-TW.md)。

## 應用

丟棄法與混合增強在影像分類中很常見。隨機深度用於深層視覺骨幹網路。標籤平滑出現在翻譯與語言建模中，用來抑制過度自信的詞元預測。

## 開放問題

- 當大型模型在足夠的資料上訓練、本來就不會過擬合時，隨機正則化器還有幫助嗎？
- 丟棄法應如何與正規化搭配，因為兩者會互相影響？
- 貝氏解釋在實務上能給出校準良好的不確定性嗎？

## 參考文獻

### 奠基性論文

- Srivastava、Hinton、Krizhevsky、Sutskever 與 Salakhutdinov，*Dropout: A Simple Way to Prevent Neural Networks from Overfitting*，Journal of Machine Learning Research（2014）。https://jmlr.org/papers/v15/srivastava14a.html — 原始的丟棄法及其實驗。
- Huang、Sun、Liu、Sedra 與 Weinberger，*Deep Networks with Stochastic Depth*（2016）。https://arxiv.org/abs/1603.09382 — 訓練時隨機跳過殘差區塊。
- Zhang、Cisse、Dauphin 與 Lopez-Paz，*mixup: Beyond Empirical Risk Minimization*（2017）。https://arxiv.org/abs/1710.09412 — 提出混合增強，即對樣本的凸組合進行訓練。
- Gal 與 Ghahramani，*Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning*（2016）。https://arxiv.org/abs/1506.02142 — 把丟棄法與近似貝氏推論連結起來。
- Szegedy 等人，*Rethinking the Inception Architecture for Computer Vision*，IEEE Conference on Computer Vision and Pattern Recognition（2016）。https://arxiv.org/abs/1512.00567 — 以標籤平滑作為正則化器而廣為人知。
