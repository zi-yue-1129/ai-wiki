---
translation_reviewed: 2026-10-28
---

# 學習率排程與預熱

學習率是梯度下降的步長，大多數訓練過程都會隨時間改變它。排程則指定它如何改變。這個選擇同時影響網路訓練的速度與最終結果；而對 Transformer 與極大批次的訓練，開頭通常還需要一段短暫的預熱。

## 概述

梯度下降的更新為 \(\theta_t = \theta_{t-1} - \eta_t\, g_t\)，其中 \(g_t\) 為梯度，\(\eta_t\) 為學習率。固定的 \(\eta\) 必然是一種折衷。開頭安全的學習率，在接近極小值時可能太大：那裡的損失曲面很窄，迭代點會來回震盪。足夠小、適合訓練末段的學習率，在開頭又會太慢。排程讓學習率在前期較大、後期較小，兼顧兩者。

預熱處理的是另一個問題。在初始化時，梯度並不可靠，若學習率太大，權重可能在網路穩定之前就被推入不佳的區域。從小的學習率開始再逐步升高，可以避免這個問題；批次越大，這一點越重要。

## 核心概念

- **排程**：從步數（或 epoch）索引映射到學習率的函數。
- **衰減**：學習率在訓練過程中逐步下降，方式可以是階梯式、線性或餘弦曲線。
- **預熱**：開頭的一段時間，學習率從小值上升到目標值。
- **重啟**：在固定時點把學習率重新拉高，開始新一輪的衰減。
- **週期**：排程中一段重複的上升與下降。

## 運作方式

大多數實務可由三種形狀涵蓋：

| 形狀 | 公式 | 常見用途 |
|---|---|---|
| 階梯式衰減 | \(\eta_t = \eta_0\,\gamma^{\lfloor t/s \rfloor}\)，每 \(s\) 步乘以 \(\gamma\) | 經典的影像分類設定 |
| 線性衰減 | \(\eta_t = \eta_0\,(1 - t/T)\)，在第 \(T\) 步降到零 | 微調與語言模型 |
| 預熱後衰減 | 線性上升，之後接任何一種衰減 | Transformer 與大批次訓練 |

預熱與衰減通常一起使用。上升段很短，常為數個 epoch 或數千步；衰減則佔據訓練的其餘部分。

## 關鍵方法

以下為三個里程碑式方法，各有獨立頁面。它們的差別在於排程的形狀，以及它們所解決的問題。

| 方法 | 形狀 | 區別所在 |
|---|---|---|
| [漸進式預熱與線性縮放](gradual-warm-up.md)（Goyal 等人，2017） | 在前幾個 epoch 線性升到 \(k\eta\) | 依批次大小縮放學習率，並以漸進上升避免初期不穩定。同一頁也討論 Vaswani 等人（2017）的 Transformer 排程 |
| [餘弦退火與暖重啟](cosine-annealing-warm-restarts.md)（Loshchilov 與 Hutter，2017） | 餘弦衰減，在固定時點重啟，每一輪比上一輪更長 | 依排程重啟衰減，並可在每輪結束時保存快照 |
| [循環學習率](cyclical-learning-rates.md)（Smith，2017） | 學習率在兩個界限之間來回振盪 | 沒有固定的衰減。界限由短暫的線性上升決定，因此不需手動調整 |

## 關聯

- [自適應方法](adaptive/index.md)（如 Adam）仍使用全域學習率，排程會乘上每個參數的步長。因此 Adam 系列的 Transformer 訓練常會加上預熱。
- [SGD 與動量](sgd-and-momentum/index.md)是學習率穩定性上界 \(\eta \le 1/L\) 最容易說明的設定，排程對最終點的影響在這裡也最清楚。
- [正則化與權重衰減](regularisation-and-weight-decay.md)與排程互相影響，因為有效的衰減取決於當前的學習率。
- [大批次與分散式訓練](large-batch-and-distributed.md)是預熱與線性縮放規則最重要的場景。

## 應用

- 在 ImageNet 上以階梯式或餘弦排程訓練 ResNet。
- 以預熱加衰減的方式預訓練 Transformer 語言模型。
- 以短而小學習率的排程微調預訓練網路。

## 開放問題

- 預熱為何有幫助？它是在解決訓練初期的最佳化問題，還是主要在穩定正規化層的統計量？
- 在固定的訓練預算下，應如何選擇預熱長度與重啟週期？
- 在某一架構上調好的排程，能否轉移到另一個架構？

## 參考文獻

### 開創性論文

- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — 提出線性縮放規則與漸進式預熱，並用於批次大小達 8192 的訓練。
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR. https://arxiv.org/abs/1608.03983 — 提出附暖重啟的餘弦退火，並說明它所支持的快照集成。
- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV. https://arxiv.org/abs/1506.01186 — 讓學習率在界限之間循環變化，免去手動設計的排程。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 以線性預熱加上反平方根衰減來訓練 Transformer。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機梯度方法的綜述，包含步長排程及其收斂理論。
