---
translation_reviewed: 2026-10-28
---

# 循環學習率

循環學習率讓學習率在一個下界與一個上界之間反覆變化，而不是單調地衰減。Smith（2017）提出此方法，其界限由一段短暫、學習率線性上升的測試找出。它免去了手動設計全域排程的需要。上層概述見[學習率排程與預熱](learning-rate-schedules.md)。

## 概述

大多數排程假設學習率應隨時間下降。Smith 的觀察是，較高的學習率有助於最佳化器跨越鞍點與平坦區域，而較低的學習率則幫助它落入極小值。在兩者之間振盪，網路就能同時受益，而不需要外部決定何時降低學習率。

## 問題

找出最佳的固定學習率，以及最佳的衰減排程，若用網格搜尋成本很高。Smith 想知道，是否有簡單的規則，能自動找出一個有用的學習率範圍，並讓學習率在範圍內循環。

## 核心想法

以學習率範圍測試估計一對合理的界限 \(\eta_{\min}\) 與 \(\eta_{\max}\)：在數個 epoch 中線性提高學習率，觀察損失下降最快的區間，以及開始上升的位置。接著在其餘的訓練中，讓學習率在這兩個界限之間循環。

## 演算法

1. 執行一段短測試，在數個 epoch 內線性提高學習率。
2. 從損失下降的範圍取得 \(\eta_{\min}\) 與 \(\eta_{\max}\)。
3. 讓學習率在兩個界限之間循環。最簡單的形式是每個週期內先從 \(\eta_{\min}\) 線性升到 \(\eta_{\max}\)，再線性降回。

摘要並未指出循環的具體政策，也未說明如何選擇週期長度。

## 結果

- 摘要指出，讓學習率在界限之間循環，能在不需手動調校的情況下改善分類準確率，而且常能在較少的迭代中達成。
- 摘要稱此方法「實際上消除了為全域學習率實驗尋找最佳值與排程的需要」。
- 基準為 CIFAR-10、CIFAR-100 與 ImageNet，架構包括 ResNet、Stochastic Depth 網路、DenseNet、AlexNet 與 GoogLeNet。摘要未給出定量結果。

## 限制

- 摘要沒有數字，因此增益的大小需要由論文中的實驗確認。
- 週期長度決定學習率多久回到最大值，而摘要並未解決這個選擇。
- 界限來自單一架構與資料集上的範圍測試。摘要未說明它們能否轉移到其他架構。

## 關聯

- [附暖重啟的餘弦退火](cosine-annealing-warm-restarts.md)同樣會重啟學習率，但每輪內部是平滑的衰減。
- [漸進式預熱](gradual-warm-up.md)在開頭使用線性上升，這也正是範圍測試所做的事。
- [學習率排程與預熱](learning-rate-schedules.md)是把本方法放在其他方法之中的上層概述。
- [損失地形](theory-and-landscapes.md)解釋了為何較大的學習率有助於逃離平坦區域與鞍點。

## 開放問題

- 循環排程何時優於調校良好的衰減，何時不如？
- 對於給定的預算，應如何選擇週期長度？

## 參考文獻

### 開創性論文

- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV. https://arxiv.org/abs/1506.01186 — 提出在界限之間循環學習率，界限由線性範圍測試找出。
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR. https://arxiv.org/abs/1608.03983 — 每輪內為餘弦衰減的週期排程，供比較之用。
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — 預熱排程，說明起始學習率為何重要。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 預熱之後的單調衰減，是實務上循環排程常比較的基準。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機方法的步長選擇綜述，範圍測試正是其中一種實務做法。
