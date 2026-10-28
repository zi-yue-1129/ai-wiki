---
translation_reviewed: 2026-10-28
---

# 範數裁剪

範數裁剪在梯度範數超過固定門檻時重新縮放梯度，使步長上限受到限制，同時保留方向。Pascanu、Mikolov 與 Bengio（2013）提出此方法，用來防止循環神經網路的梯度爆炸。上層概述見[梯度裁剪與正規化更新](gradient-clipping-and-normalisation.md)。

## 概述

循環網路在每個時間步使用相同的權重，因此其梯度是許多雅可比矩陣的乘積。當這些矩陣的範數大於一時，乘積可能無限制地成長，單次更新就可能把參數推得很遠。解決方法必須便宜且只在少數情況下觸發，因為大多數梯度都是正常的。Pascanu 等人因此提出限制梯度範數，作為處理爆炸的簡單做法。

## 問題

以時間反向傳播訓練循環網路常常不穩定。梯度爆炸會造成損失突然飆升，梯度消失則使網路無法從長程依賴中學習。摘要點出這兩個問題，並歸因於先前的分析。論文想知道，一個簡單的方法能否處理爆炸的問題，並為消失的情況提出一個軟性約束。

## 核心想法

照常計算梯度。若其範數大於門檻，就重新縮放，使其範數等於門檻；否則保持不變。重新縮放只乘上一個正數，方向因此不變，只有長度受到限制。論文認為，裁剪後的更新對目前的小批次仍是下降方向。

## 演算法

令 \(g\) 為梯度，\(\tau\) 為門檻。

1. 計算 \(\|g\|\)。
2. 若 \(\|g\| > \tau\)，令 \(g \leftarrow \tau\, g / \|g\|\)。
3. 以裁剪後的梯度套用最佳化器更新。

門檻是超參數。論文建議依許多次更新中梯度範數的平均統計量來設定。

## 結果

摘要指出，作者提出了一種梯度範數裁剪策略來處理梯度爆炸，並在實驗部分以實證驗證了假說與所提出的解法。摘要未給出具體數字，因此本頁不引用任何數值。

## 限制

- 必須選擇門檻。太小會減慢學習，太大則幾乎沒有作用。
- 裁剪無法處理梯度消失，論文以另一個軟性約束來處理該問題。
- 以範數裁剪是對所有參數的整體操作，因此把尺度差異很大的各層視為同一個整體。

## 關聯

- [梯度裁剪與正規化更新](gradient-clipping-and-normalisation.md)是上層概述，範數裁剪與 LARS、LAMB 並列於其中。
- [循環神經網路](../models/rnn/index.md)是此方法最初設計所針對的設定。
- [LARS](lars.md)提供逐層的替代做法，縮放的是每一層，而非整個梯度。
- [學習率排程](learning-rate-schedules.md)與裁剪互相影響，因為門檻與步長共同決定了最大可能的更新量。

## 開放問題

- 裁剪門檻應否在訓練過程中自適應調整？
- 對於各層尺度差異很大的模型（如 Transformer），以範數為單位進行裁剪是否合適？

## 參考文獻

### 開創性論文

- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). *On the Difficulty of Training Recurrent Neural Networks*. ICML. https://arxiv.org/abs/1211.5063 — 提出以梯度範數裁剪處理梯度爆炸，並分析循環網路中的梯度消失。
- You, Y., Gitman, I. & Ginsburg, B. (2017). *Large Batch Training of Convolutional Networks*. arXiv. https://arxiv.org/abs/1708.03888 — 對整體步長的逐層替代做法。
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — 以預熱處理訓練初期不穩定的另一種做法。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機方法中的步長控制與梯度大小綜述。
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*，第 10 章序列建模。MIT Press。https://www.deeplearningbook.org/ — 教科書對循環網路中梯度爆炸與消失的說明，包括梯度裁剪，可線上免費閱讀。
