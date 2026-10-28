---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/dropout
tags:
  - dropout
  - regularisation
  - overfitting
aliases:
  - 丟棄法
  - Dropout
---

# 丟棄法

丟棄法在每個訓練步驟中隨機移除網路中的單元。剩下的單元必須學會在沒有特定夥伴的情況下也能運作的特徵，這能減少過擬合。測試時使用完整網路，並把激活值縮放，使其期望值與訓練時一致。

## 概觀

[本章](index.zh-TW.md)涵蓋隨機正則化。本頁說明原始的丟棄法、其縮放規則與變體。

## 問題

具有大量參數的大型網路可能會記住訓練集。對權重加上懲罰有幫助，但同一層中的單元可能彼此共適應，每個單元都依賴特定的其他單元。此方法直接針對共適應問題。

## 核心想法

每個訓練步驟中，某一層的每個單元都以機率 $p$ 被保留，否則獨立地設為零。梯度只流經被保留的單元。由於每一步都在訓練一個與其他步驟共享權重的不同稀疏網路，訓練的行為就像許多網路的集成。

## 方程式

對於激活向量 $\mathbf{h}$，訓練時的輸出為 $\tilde{\mathbf{h}} = \mathbf{m} \odot \mathbf{h}$，其中遮罩 $m_i \sim \mathrm{Bernoulli}(p)$。測試時則直接使用 $\mathbf{h}$，這在期望意義上等同於對訓練時的輸出做縮放。

## 結果

摘要指出，丟棄法能顯著減少過擬合，並在其他正則化方法之上有大幅改進。論文的實驗給出數字，此處不重述。

## 限制

- 訓練需要更長的時間，因為帶有雜訊的單元使網路需要更多步驟才能收斂。
- 當模型本來就沒有過擬合時，效益會縮小；而在卷積層中，相鄰激活值高度相關，丟棄法可能反而損害效能。
- 丟棄法與正規化層會互相影響，若直接並用，可能改變測試時所見的變異數。

## 關聯

丟棄法的貝氏解釋見[本章](index.zh-TW.md)，其中 Gal 與 Ghahramani 把測試時的丟棄法與近似推論相連 [(Gal and Ghahramani, 2016)](https://arxiv.org/abs/1506.02142)。此方法常與[混合增強](mixup.zh-TW.md)與[隨機深度](stochastic-depth.zh-TW.md)並用。

## 應用

分類器頭部與許多網路中的全連接層，以及小型資料集的正則化。

## 開放問題

- 對於在極大資料上訓練的大型模型，是否仍需要丟棄法？
- 不同層與不同架構應如何設定丟棄率？

## 參考文獻

### 奠基性論文

- Srivastava、Hinton、Krizhevsky、Sutskever 與 Salakhutdinov，*Dropout: A Simple Way to Prevent Neural Networks from Overfitting*，Journal of Machine Learning Research（2014）。https://jmlr.org/papers/v15/srivastava14a.html — 原始的丟棄法及其實驗。
- Gal 與 Ghahramani，*Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning*（2016）。https://arxiv.org/abs/1506.02142 — 丟棄法的貝氏解釋。
- Huang、Sun、Liu、Sedra 與 Weinberger，*Deep Networks with Stochastic Depth*（2016）。https://arxiv.org/abs/1603.09382 — 一個相關方法，會整個丟棄殘差區塊。
- Ioffe 與 Szegedy，*Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*（2015）。https://arxiv.org/abs/1502.03167 — 說明為何丟棄法與正規化併用時需要謹慎。
- Zhang、Cisse、Dauphin 與 Lopez-Paz，*mixup: Beyond Empirical Risk Minimization*（2017）。https://arxiv.org/abs/1710.09412 — 與丟棄法並用的資料層級正則化器。
