---
translation_reviewed: 2026-10-28
---

# 彩票假說

彩票假說指出，隨機初始化的稠密網路中包含一個小型稀疏子網路；若單獨從其原始初始權重訓練，它能達到與完整網路相近的準確度。這樣的子網路稱為**獲勝彩票**。這個想法改變了研究者對[剪枝](../index.zh-TW.md)的看法：大型網路中有價值的部分，可能和訓練後的權重一樣，取決於幸運的初始化。

## 概述

原始實驗很簡單：訓練稠密網路，剪除量值最小的權重，把剩下的權重重設為訓練開始時的值，再重新訓練。如果重設後的子網路能訓練到原本的準確度，它就是獲勝彩票。若改為重設成隨機權重，效果會消失，這說明了初始化的重要性。

## 關鍵概念

- **獲勝彩票**：稀疏子網路加上它被重設到的初始權重，能訓練到稠密網路的準確度。
- **迭代量值剪枝（IMP）**：訓練、剪除一部分權重、倒回並重複的程序。比單次剪枝能找到更稀疏的彩票。
- **倒回**：把剩餘權重重設為訓練早期的某個迭代，而不是第一步。倒回到早期訓練，使彩票能在較深的網路上運作。
- **達到的稀疏度**：獲勝彩票在小型網路上常能達到很高的稀疏度，但同樣的程序在較深的網路上沒有倒回便很難成功。

## 各重要方法比較

| 方法 | 對程序的改變 | 頁面 |
| --- | --- | --- |
| 彩票假說 | 把剩餘權重重設為原始初始化 | [彩票假說](lottery-ticket-hypothesis/index.zh-TW.md) |
| 穩定彩票 | 倒回到訓練的早期點，適用於較深的網路 | [穩定彩票](stabilised-lottery-ticket/index.zh-TW.md) |

第二個方法保留第一個方法的程序，只改變權重倒回的位置。正是這個改變，使彩票能在較深的網路中被找到。

## 取捨

- **洞見與效率**：這個假說解釋了剪枝後的網路為何能被訓練，但找彩票需要多次訓練，對大型模型很昂貴。
- **初始化與訓練**：獲勝彩票取決於初始權重，因此對隨機種子與最佳化器很敏感。
- **初始化時剪枝**：在訓練前剪枝能節省計算量，但在大規模下，比起基於訓練後網路的方法，它一直較不可靠。

## 更多變體與開放問題

- **開放問題**：大型 Transformer 是否存在獲勝彩票，以及倒回應如何運作。
- **開放問題**：找到的子網路能否在不同資料集與任務之間轉移。
- **變體**：[量值剪枝](../magnitude-pruning/gradual-pruning/index.zh-TW.md)加上漸進排程，能避免重複訓練。

## 相關連結

彩票的觀點連結到更廣泛的問題：為什麼過參數化的網路能良好訓練，這在[深度學習理論](../../../../theory/deep-learning/index.zh-TW.md)中討論。大腦一開始形成的連接比最後保留的多，其中部分在發育選擇中存活，這與[神經科學](../../../../brain-mind/neuroscience/index.zh-TW.md)相關。

## 參考文獻

### 開創性論文

- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — 從原始初始化訓練的稀疏子網路，能達到稠密網路的準確度。
- Frankle, J., Dziugaite, G. K., Roy, D. M., Carbin, M. (2019). *Stabilizing the Lottery Ticket Hypothesis*. arXiv:1903.01611. https://arxiv.org/abs/1903.01611 — 倒回到訓練的早期點，在較深的網路中找到彩票。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 彩票程序所依據的剪枝加重新訓練流程。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 涵蓋稀疏訓練與推論，包括彩票。
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 比較各方法，並顯示訓練後的稀疏網路很難從頭訓練。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

（本頁尚未查核任何項目）
