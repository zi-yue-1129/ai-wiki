---
translation_reviewed: 2026-10-28
---

# 餘弦退火與暖重啟

附暖重啟的餘弦退火（SGDR）沿著半個餘弦曲線衰減學習率，然後在固定時點把它拉回最大值並重新開始，每一輪都比前一輪更長。此方法由 Loshchilov 與 Hutter（2017）提出。上層概述見[學習率排程與預熱](learning-rate-schedules.md)。

## 概述

單純的餘弦衰減會從高的學習率平滑地降到低的學習率，是常見的選擇。它的缺點是搜尋可能停留在某個區域，學習率在訓練結束前一直很小。定期重啟學習率，能讓最佳化器有機會離開原區域，並收斂到新的區域；而每次重啟的結束點，都可以保存為一個快照。

## 問題

訓練預算是有限的，而通常的衰減在訓練開始前就已決定。Loshchilov 與 Hutter 想知道，重啟式的排程能否更快達到好的解，衡量標準是訓練過程中任一時點的表現，而不只是結束時的表現。

## 核心想法

在第 \(i\) 輪中，依餘弦曲線把學習率從 \(\eta^i_{\max}\) 衰減到 \(\eta^i_{\min}\)。該輪結束時，將學習率重設為 \(\eta^i_{\max}\) 以重啟。每一輪的長度以 \(T_{\mathrm{mult}}\) 倍成長，使訓練末段有更長的階段。

## 演算法

對於長度為 \(T_i\) 個 epoch 的第 \(i\) 輪，令 \(T_{\mathrm{cur}}\) 為自上次重啟以來經過的 epoch 數，每個批次後更新。學習率為

\[
\eta_t = \eta^i_{\min} + \frac{1}{2}\left(\eta^i_{\max} - \eta^i_{\min}\right)\left(1 + \cos\!\left(\frac{T_{\mathrm{cur}}}{T_i}\,\pi\right)\right)
\]

每次重啟令 \(T_{i+1} = T_{\mathrm{mult}}\, T_i\)。論文建議以此方式增加每輪的長度，以改善訓練中任一時點的表現。每輪結束時的模型快照，可以平均成一個集成。

## 結果

- 摘要指出，此方法能改善深層網路訓練中隨機梯度下降在任意時點的表現，並在 CIFAR-10 與 CIFAR-100 上給出新的最先進結果。摘要報告的錯誤率為 3.14%（CIFAR-10）與 16.21%（CIFAR-100），論文將其歸因於快照集成。
- 摘要也提到在腦電圖（EEG）記錄與縮小版 ImageNet 上的實驗，但未給出數字。

## 限制

- 重啟點與各輪的長度 \(T_0\)、\(T_{\mathrm{mult}}\) 都是手動選擇的，因此仍需要對預算做決定。
- 若一輪在學習率夠小、模型能穩定下來之前就結束，重啟可能浪費運算。
- 主要的錯誤率來自快照集成，因此它並不是以相同排程訓練的單一模型的錯誤率。

## 關聯

- [學習率排程與預熱](learning-rate-schedules.md)比較這種衰減與階梯式衰減、循環學習率。
- [漸進式預熱](gradual-warm-up.md)常與餘弦衰減合用，以預熱作為第一階段。
- [循環學習率](cyclical-learning-rates.md)同樣會重啟學習率，但界限固定，且沒有餘弦衰減。
- [正則化與權重衰減](regularisation-and-weight-decay.md)與學習率互相影響，因為有效的衰減取決於學習率。

## 開放問題

- 重啟排程在大型資料集與長時間訓練上，是否比短時間訓練更有幫助？
- 對於給定的運算預算，是否有選擇 \(T_{\mathrm{mult}}\) 的原則性規則？

## 參考文獻

### 開創性論文

- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR. https://arxiv.org/abs/1608.03983 — 提出附暖重啟的餘弦退火，並報告 CIFAR-10 與 CIFAR-100 的錯誤率。
- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV. https://arxiv.org/abs/1506.01186 — 另一種週期排程，其界限由學習率範圍測試決定。
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — 訓練開頭的預熱，餘弦排程常接在其後。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 線性預熱之後接另一種衰減，供與餘弦衰減比較。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機梯度方法步長排程的綜述，並包含其收斂理論。
