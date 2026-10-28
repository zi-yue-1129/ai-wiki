---
related:
- theory/models/rnn/gated-cells
- theory/models/rnn
aliases:
  - Long Short-Term Memory
  - LSTM
  - 長短期記憶
tags:
  - recurrent networks
  - gating
  - long-term dependencies
translation_reviewed: 2026-10-28
---

# 長短期記憶

長短期記憶（LSTM）是一種具有門控記憶的循環單元，能學習跨越長時間間隔的依賴。它由 Hochreiter 與 Schmidhuber 在 1997 年的論文 "Long Short-Term Memory" 中提出，此後多年成為標準的循環單元。

## 問題

誤差沿著許多時間步反向傳回時，往往不是爆炸就是縮成零。因此以梯度下降訓練的原始循環網路，很難把某個事件與許多步之前的起因連結起來，學習這種連結可能耗時到不切實際，或者根本失敗。

## 核心想法

LSTM 以一個記憶單元取代原始的循環單元，這個記憶單元圍繞一個自我連接的線性單元建立，論文稱之為 "constant error carousel"（恆定誤差輸送帶）。因為單元狀態以加法更新，誤差可以穿過它反向傳遞，而不會被反覆相乘。兩個乘法閘門，一個在輸入端、一個在輸出端，分別決定何時把資訊寫入單元，以及何時讀出。

## 方程式或演算法

對於時間 \(t\) 的記憶單元 \(c\)，其輸入閘門為 \(y_{\text{in}}\)，輸出閘門為 \(y_{\text{out}}\)，壓縮函數為 \(g\) 與 \(h\)，論文給出

\[
s_c(t) = s_c(t-1) + y_{\text{in}}(t)\, g\big(\text{net}_c(t)\big), \qquad y_c(t) = y_{\text{out}}(t)\, h\big(s_c(t)\big),
\]

其中兩個閘門都是 logistic sigmoid。學習使用截斷的梯度，論文給出的更新成本為每步 O(W)，其中 W 是權重的數量。

## 結果

在嵌入式 Reber 文法上，LSTM 在所有試驗中都學會了任務，150 次試驗中有兩次失敗，最佳配置需要 8,440 次序列呈現。在具有 100 步延遲的任務上，LSTM 在 5,040 個序列後於所有試驗中成功，而 RTRL 與 BPTT 在 500 萬次序列呈現內都未能成功。

## 限制

論文指出，截斷式演算法 "will not easily solve" 強延遲的 XOR 問題。論文也提到，隨機猜測權重就能解決的任務，例如 500 步的奇偶性問題，對於初始權重很小的截斷式 LSTM 而言仍然困難。

## 相關連結

[門控單元](../index.md)頁面比較了 LSTM 與原始單元及 GRU，而[循環神經網路](../../index.md)頁面則把它放在其他循環模型之中。[序列到序列學習](../../sequence-modes/sequence-to-sequence/index.md)頁面以 LSTM 作為翻譯的編碼器與解碼器。[Transformer](../../../transformer/index.md) 以注意力取代循環，而[記憶與學習](../../../../../brain-mind/memory-learning/index.md)則涵蓋與工作記憶的比較。

## 未解問題與更多變體

- **單元設計。** Greff 等人（2017）對多種 LSTM 變體做了基準測試，發現原始設計難以超越，因此額外閘門或連接的價值仍未定論。
- **長序列。** 即使是門控單元，在非常長的序列上也會退化，這也是較新的線性循環模型被提出的原因之一。
- **截斷式訓練。** 論文自己的失敗案例，例如強延遲 XOR 與 500 步奇偶性問題，顯示截斷的梯度在某些任務上仍是弱點。

## 參考文獻

### 開創性論文

- Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory". *Neural Computation* 9(8). https://doi.org/10.1162/neco.1997.9.8.1735 — LSTM，以加法更新的記憶單元解決梯度消失問題。
- Bengio, Y., Simard, P. & Frasconi, P. (1994). "Learning long-term dependencies with gradient descent is difficult". *IEEE Transactions on Neural Networks* 5(2). https://doi.org/10.1109/72.279181 — 說明為何以梯度下降學習循環網路中的長程依賴很困難。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 10 章涵蓋循環與遞迴網路，以及通過時間的反向傳播。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). "On the difficulty of training Recurrent Neural Networks". [arXiv:1211.5063](https://arxiv.org/abs/1211.5063) — 分析梯度爆炸與消失，並提出梯度範數裁剪。
- Greff, K., et al. (2017). "LSTM: A Search Space Odyssey". [arXiv:1503.04069](https://arxiv.org/abs/1503.04069) — 比較多種 LSTM 變體，發現原始設計難以超越。
