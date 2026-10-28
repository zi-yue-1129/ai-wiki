---
translation_reviewed: 2026-10-28
---

# 神經網路中稀疏性的現況

神經網路中稀疏性的現況是一個 2019 年的基準研究，在同一套協定下，於大規模任務上評估數種剪枝與稀疏化方法。它的主要發現是：簡單的量值剪枝與更複雜的方法相當或更好，這也是[量值剪枝](../index.zh-TW.md)仍是新方法必須超越的基準的原因。

## 問題

許多稀疏化方法各自使用不同的設定被提出，因此結果無法直接比較。不清楚哪些進步是真的，哪些來自訓練上的差異。

## 核心想法

在共同的協定下，於大規模的影像與語言任務上執行數種稀疏化方法。各方法共用「遮罩後重新訓練」的模式，差別只在遮罩如何選擇與更新，因此比較能分離出這個選擇的效果。

## 公式或演算法

基準本身沒有新的演算法。每個方法在目標稀疏度下選擇遮罩，對遮罩後的網路重新訓練，並在相同稀疏度下比較最終準確度。論文報告各方法的準確度與稀疏度之間的取捨。

## 結果

摘要表示，在大規模任務上，簡單的量值剪枝與更複雜的稀疏化技術相當或更好。

## 限制

基準涵蓋的是當時的影像與語言模型。論文也指出，經剪枝學得的稀疏架構，無法從頭訓練到與聯合稀疏化與最佳化模型相同的測試準確度，這對稀疏訓練方法是一個限制。

## 開放問題與相關變體

- **新模型。** 同樣的排序在大型 Transformer 上是否成立，原始基準沒有涵蓋；大型 Transformer 的剪枝常是單次進行，見[大型語言模型單次剪枝](../../one-shot-llm-pruning/index.zh-TW.md)。
- **相關**：[漸進剪枝](../gradual-pruning/index.zh-TW.md)是基準中量值基準所使用的排程。

## 相關連結

這個基準使量值作為整個[剪枝](../../index.zh-TW.md)家族預設分數的選擇有了依據。它的稀疏度與速度之間的取捨，取決於執行結果的硬體，見 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 在同一協定下比較稀疏化方法，發現簡單的量值剪枝是強基準。
- Zhu, M., Gupta, S. (2017). *To prune, or not to prune: exploring the efficacy of pruning for model compression*. arXiv:1710.01878. https://arxiv.org/abs/1710.01878 — 基準評估的漸進量值剪枝。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 定義基準基線的剪枝加重新訓練方法。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 將基準中的方法放在更廣的脈絡中的綜述。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — 與基準中可訓練性發現相關的稀疏訓練結果。
