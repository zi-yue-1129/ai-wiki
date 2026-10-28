---
translation_reviewed: 2026-10-28
tags:
  - optimization
  - weight decay
  - scaling
aliases:
  - AdamW weight decay scaling
  - AdamW 權重衰減縮放
---

# AdamW 的權重衰減縮放

Wang 與 Aitchison（2024）探討當模型或資料集變大時，AdamW 的權重衰減應如何改變。他們的答案是：衰減應設定為讓權重的平均時間尺度以 epoch 計保持大致固定，這表示模型越大，衰減越要提高；資料集越大，衰減越要降低。上層子主題是[權重範數動態](index.md)，最佳化器是 [AdamW](../adaptive/adamw.md)。

## 概述

在 AdamW 下，權重的行為近似於過去更新的指數移動平均，其時間尺度為 \(\tau = 1/(\eta\lambda)\) 次迭代，其中 \(\eta\) 是學習率，\(\lambda\) 是衰減。\(\tau\) 大時，舊的更新會保留在權重中；\(\tau\) 小時，舊的更新很快被遺忘。一個 \(\tau\) 好不好，取決於一個 epoch 有多少次迭代，因此以 epoch 作為時間尺度的單位比較自然。

## 問題

實務上，衰減值常從一種模型或資料集大小搬到另一種，而在某個規模有效的數值，換到另一個規模可能表現很差。學習率的遷移方法（例如讓學習率能在寬度之間轉移的參數化）在衰減沒有隨學習率調整時也會失效。論文問的是：最佳衰減如何縮放，才能用一條規則跨越不同規模。

## 核心想法

論文的主要發現是：以 epoch 計的最佳時間尺度，在模型與資料集改變時大致保持不變。若此成立，衰減就可以直接由學習率與每個 epoch 的迭代數推出。模型變大時衰減要提高，因為每個 epoch 的步數會隨批次大小與資料集改變；資料集變大時衰減要降低。

## 運作方式

1. 依小規模的掃描，固定一個以 epoch 計的目標時間尺度 \(\tau\)。
2. 以目標設定的每個 epoch 步數，把它換算成迭代數。
3. 設定 \(\lambda = 1/(\eta \tau_{\text{iters}})\)，使衰減與實際使用的學習率相配。
4. 學習率或模型寬度改變時，讓 \(\lambda\) 隨 \(\eta\) 重新縮放，而不是固定不動。

## 結果

論文在圖像分類的殘差網路與視覺 Transformer，以及小型語言模型上掃描衰減。它報告，在這些設定下，以 epoch 時間尺度表示的最佳衰減大致相似。任何數值在重用前，都應先在論文中核對掃描結果與圖表。

## 限制

- 規則是在固定訓練配方下的掃描推導出來的。它並未確立每種排程的最佳時間尺度，預熱與隨時間改變 \(\eta\) 的排程都會改變 \(\tau\)。
- 「時間尺度在 epoch 上為常數」是在所研究設定上的經驗發現，並非對所有架構都成立的定理。
- 衰減只是眾多旋鈕之一。它對注意力穩定性的影響另見 [QK 正規化](../../models/transformer/qk-norm.md) 頁面。

## 相關主題

- [權重範數動態](index.md) 把此結果放在平衡分析旁邊。
- [旋轉平衡](rotational-equilibrium.md) 提供以步數計的時間尺度 \(1/(\eta\lambda)\)，這條規則即以此為基礎。
- [AdamW](../adaptive/adamw.md) 定義了此規則所設定的解耦衰減。
- [學習率排程](../learning-rate-schedules.md) 很重要，因為衰減與實際使用的學習率相連。

## 開放問題

- 時間尺度為常數的規則，是否適用於以固定 token 數而非 epoch 訓練的超大模型。
- 排程不是常數時（例如餘弦衰減或長預熱），規則應如何修改。

## 參考文獻

- Wang, X., & Aitchison, L. (2024). *How to Set AdamW's Weight Decay as You Scale Model and Dataset Size*. arXiv:2405.13698. https://arxiv.org/abs/2405.13698 — 以 epoch 時間尺度為基礎的規則與縮放掃描的來源。
- Loshchilov, I., & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. arXiv:1711.05101. https://arxiv.org/abs/1711.05101 — 定義此規則所調整的解耦權重衰減。
- Kosson, A., Messmer, B., & Jaggi, M. (2023). *Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks*. arXiv:2305.17212. https://arxiv.org/abs/2305.17212 — 以 \(1/(\eta\lambda)\) 給出以步數計的時間尺度。
- Li, Z., & Arora, S. (2019). *An Exponential Learning Rate Schedule for Deep Learning*. arXiv:1910.07454. https://arxiv.org/abs/1910.07454 — 說明衰減與正規化如何與學習率互動。
- Wortsman, M., Liu, P. J., Xiao, L., et al. (2023). *Small-scale proxies for large-scale Transformer training instabilities*. arXiv:2309.14322. https://arxiv.org/abs/2309.14322 — 測試穩定學習率範圍如何隨權重衰減與預熱改變。
