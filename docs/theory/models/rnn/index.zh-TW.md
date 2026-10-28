---
related:
- brain-mind/memory-learning
- theory/models/ssm
aliases:
  - Recurrent Neural Networks
  - RNN
  - LSTM
  - 循環神經網路
  - 遞迴神經網路
tags:
  - recurrent networks
  - sequence modelling
  - architecture
translation_reviewed: 2026-10-28
---

# 循環神經網路

循環神經網路（RNN）逐步處理序列，並把隱藏狀態從每一步傳到下一步。這個狀態是對已見內容的學習摘要，因此同一個網路能以固定的參數數量讀取任意長度的序列。在注意力模型取代它們之前，RNN 主導了語言與語音建模，之後多數任務已改用注意力模型。不過在輸入以串流形式到達、記憶體必須極為便宜，或模型需要線上更新狀態的場合，RNN 仍然有用。

## 核心想法

每一步，網路把當前輸入與前一個隱藏狀態結合，產生新的隱藏狀態，並可選擇性地產生輸出。最簡單的循環單元用一次非線性變換完成這件事。它的弱點在訓練：跨越許多步的梯度容易消失或爆炸，使網路難以學到跨越長間隔的依賴。門控單元就是為了解決這點而設計的，也是下面第一個組件。

## 組件與變體

- [門控單元](gated-cells/index.md)：原始單元、LSTM 與 GRU，以及它們的閘門如何控制記憶。
- [序列模式](sequence-modes/index.md)：雙向處理、編碼器–解碼器配對、堆疊，以及訓練如何處理長序列。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| 長短期記憶（LSTM） | 1997 | 以加法更新的記憶單元，配合閘門控制寫入與讀取 | [LSTM](gated-cells/lstm/index.md) |
| 序列到序列學習 | 2014 | 以編碼器 LSTM 與解碼器 LSTM 端到端地翻譯 | [序列到序列](sequence-modes/sequence-to-sequence/index.md) |

LSTM 以門控記憶讓長程依賴變得可以學習。序列到序列模型則顯示，單一循環編碼器–解碼器可以端到端地翻譯。

## 取捨

- **記憶體與串流。** 循環狀態的大小固定，因此 RNN 處理串流成本低，也不需要鍵值快取。
- **平行化。** 每一步都依賴前一步，因此訓練無法像 Transformer 那樣沿時間平行化。這是它們失去優勢的主要原因。
- **長程依賴。** 門控有幫助，但非常長程的資訊仍然難以保留，這也是注意力與狀態空間模型被發展出來的原因。

## 應用範圍

語音辨識的前端、時間序列預測、線上控制與感測器處理，以及一些記憶體與延遲都很緊張的裝置端語言任務。

## 相關連結

[狀態空間](../ssm/index.md)家族以更好的長程行為回到循環的觀點，而 [Transformer](../transformer/index.md) 則以注意力取代了循環。在神經科學中，循環迴路是皮層動態的預設模型，門控的想法也被拿來與工作記憶機制比較，見[記憶與學習](../../../brain-mind/memory-learning/index.md)。

## 未解問題與更多變體

- **循環與注意力。** 線性循環模型能否在規模上追上注意力，以及何時各自較佳，仍在測試中。
- **訓練穩定性。** 實務上使用梯度裁剪與小心的初始化，但何時循環訓練會成功，尚無完整理論。
- **生物合理性。** 通過時間的反向傳播很難與已知的神經機制相容，替代方案正被積極研究。

## 參考文獻

### 開創性論文

- Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory". *Neural Computation* 9(8). https://doi.org/10.1162/neco.1997.9.8.1735 — LSTM，以加法更新的記憶單元解決梯度消失問題。
- Bengio, Y., Simard, P. & Frasconi, P. (1994). "Learning long-term dependencies with gradient descent is difficult". *IEEE Transactions on Neural Networks* 5(2). https://doi.org/10.1109/72.279181 — 說明為何以梯度下降學習循環網路中的長程依賴很困難。
- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". arXiv:1406.1078 — 提出 GRU，以及用於序列到序列任務的編碼器–解碼器架構。
- Sutskever, I., Vinyals, O. & Le, Q. V. (2014). "Sequence to Sequence Learning with Neural Networks". NeurIPS. arXiv:1409.3215 — 以端到端的編碼器–解碼器 LSTM 進行機器翻譯。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 10 章涵蓋循環與遞迴網路，以及通過時間的反向傳播。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). "On the difficulty of training Recurrent Neural Networks". arXiv:1211.5063 — 分析梯度爆炸與消失，並提出梯度範數裁剪。
