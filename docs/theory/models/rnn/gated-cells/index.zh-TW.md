---
related:
- brain-mind/memory-learning
aliases:
  - Gated Recurrent Units
  - LSTM Variants
  - GRU
  - 門控循環單元
  - 長短期記憶網路
tags:
  - recurrent networks
  - gating
  - long-term dependencies
translation_reviewed: 2026-10-28
---

# 門控單元

門控循環單元在每一步決定保留多少舊記憶，以及寫入多少新資訊。閘門是輸入與前一狀態的可學習 sigmoid 函數，使單元能跨越許多步攜帶資訊，而梯度消失的速度比原始循環網路慢。三種單元最常見：原始單元、長短期記憶（LSTM）單元與門控循環單元（GRU）。它們的差別在於使用幾個閘門，以及記憶是否與輸出分開保存。

## 概觀

| 單元 | 閘門 | 是否有獨立的記憶狀態 | 每單元參數量 |
|---|---|---|---|
| 原始（Elman） | 無 | 否 | 最少 |
| LSTM | 輸入、遺忘、輸出 | 是 | 約為原始單元的四倍 |
| GRU | 更新、重置 | 否 | 約為原始單元的三倍 |

## 做法

### 原始循環單元

原始單元把新狀態計算為輸入與舊狀態的非線性函數。它簡單且便宜，但跨時間的梯度是許多 Jacobian 的乘積，容易消失或爆炸。這正是 Bengio 等人（1994）分析的失敗，也是門控設計的動機。

### 長短期記憶

LSTM 保留一個獨立的記憶狀態，並以加法方式更新。遺忘閘門縮放舊的記憶狀態，輸入閘門縮放候選更新，輸出閘門決定哪一部分記憶暴露為隱藏狀態。因為記憶狀態以加法更新，梯度可以跨許多步傳遞而不會快速縮小。Hochreiter 與 Schmidhuber（1997）提出了這個設計，多年來它一直是標準的循環單元。

### 門控循環單元

GRU 把記憶狀態與隱藏狀態合併，只使用兩個閘門：更新閘門在舊狀態與新狀態之間內插，重置閘門控制舊狀態有多少進入候選值。它的參數比 LSTM 少。Cho 等人（2014）提出了它，Chung 等人（2014）則在多個序列任務上比較了 LSTM 與 GRU，發現兩種門控單元都明顯優於原始單元，而且兩者沒有一致的優劣。

## 取捨

- **容量與成本。** LSTM 參數較多，能把更多資訊分開保存；GRU 較便宜，在較小的資料上通常訓練較快。
- **遺忘閘偏置。** 把遺忘閘初始化為保留資訊是常見做法，能加速早期訓練，但對最終準確率的影響取決於任務。
- **可解釋性。** 閘門的激活可以檢查，有助於分析，但本身並不能解釋學到的計算。

## 相關連結

門控是其他家族所用的學習式乘法控制的循環前身，包括[狀態空間模型](../../ssm/selective-state-spaces/index.md)中的選擇性更新。在神經科學中，門控記憶曾被拿來與前額葉迴路對工作記憶的控制比較，見[記憶與學習](../../../../brain-mind/memory-learning/index.md)。

## 未解問題與更多變體

- **門控為何有效。** 閘門解決了梯度問題，但學到的閘門在真實任務上計算什麼，完整說明仍不足。
- **與注意力混合。** 門控單元與注意力或卷積的組合很常見，最佳組合尚無定論。
- **長脈絡限制。** 即使是門控單元，在非常長的序列上也會退化，這促成了較新的線性循環模型。

## 參考文獻

### 開創性論文

- Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory". *Neural Computation* 9(8). https://doi.org/10.1162/neco.1997.9.8.1735 — 具有加法記憶更新與乘法閘門的 LSTM 單元。
- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". arXiv:1406.1078 — 提出 GRU。

### 綜述與教科書

（本頁尚未核對）

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Chung, J., et al. (2014). "Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling". arXiv:1412.3555 — 在多個序列任務上比較 LSTM、GRU 與原始循環單元。
- Bengio, Y., Simard, P. & Frasconi, P. (1994). "Learning long-term dependencies with gradient descent is difficult". *IEEE Transactions on Neural Networks* 5(2). https://doi.org/10.1109/72.279181 — 分析原始循環網路為何在長跨度上梯度失效。
