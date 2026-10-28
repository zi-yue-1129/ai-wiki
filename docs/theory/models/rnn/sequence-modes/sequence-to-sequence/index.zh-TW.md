---
related:
- theory/models/rnn/sequence-modes
- theory/models/rnn
aliases:
  - Sequence to Sequence Learning
  - Seq2Seq
  - 序列到序列學習
tags:
  - recurrent networks
  - sequence modelling
  - machine translation
translation_reviewed: 2026-10-28
---

# 序列到序列學習

序列到序列學習是一種編碼器–解碼器方法，其中多層 LSTM 把輸入序列映射為長度可能不同的輸出序列。它由 Sutskever、Vinyals 與 Le 在 2014 年 NeurIPS 的論文 "Sequence to Sequence Learning with Neural Networks" 中提出，並展示了神經網路可以端到端地學會翻譯。

## 問題

深度網路需要固定維度的輸入與目標，但翻譯所處理的序列長度事先並不知道。因此，適用於機器翻譯的方法必須能接受任意長度的來源句，並產生任意長度的目標句。

## 核心想法

一個多層 LSTM 讀取來源句，並把它編碼為一個固定大小的向量。第二個 LSTM 再從這個向量出發，每次生成目標句的一個詞。來源詞以相反的順序輸入。

## 方程式或演算法

模型把目標句的機率分解為

\[
p(y_1,\dots,y_{T'} \mid x_1,\dots,x_T) = \prod_{t} p(y_t \mid v,\, y_1,\dots,y_{t-1}),
\]

其中 \(v\) 是編碼器產生的固定向量，每個因子都是對詞彙表的 softmax。

## 結果

在 WMT'14 英文到法文任務（ntst14 測試集）上，由五個反向 LSTM 組成的集成、束寬為 12，達到 BLEU 34.81，而短語式統計機器翻譯基線為 33.30。把來源句反轉，使單一模型的 BLEU 從 25.9 提升到 30.6。

## 限制

論文指出，對於少於 35 個詞的句子沒有效能下降，只有最長的句子有輕微下降。作者表示他們"do not have a complete explanation"，即無法完整解釋為何反轉來源句會有幫助。訓練在 8 GPU 的設定下耗時約十天。

## 相關連結

[序列模式](../index.md)頁面把編碼器–解碼器模式與雙向及堆疊的循環結構並列描述，而[循環神經網路](../../index.md)頁面則把它放在其他循環模型之中。[LSTM](../../gated-cells/lstm/index.md)頁面說明編碼器與解碼器共同使用的單元。固定大小的向量正是注意力被提出來紓解的瓶頸，見[注意力變體](../../../transformer/attention-variants/index.md)。

## 未解問題與更多變體

- **固定大小的瓶頸。** 單一向量限制了長輸入中有多少資訊能傳給解碼器，這正是注意力機制設計來彌補的缺口。
- **反轉來源。** 反轉來源句的好處已被觀察到，但作者並未解釋其原因，因此仍是開放問題。
- **長輸入。** 論文中最長句子的準確率只有輕微下降，但在更長輸入上的表現是另一個問題。

## 參考文獻

### 開創性論文

- Sutskever, I., Vinyals, O. & Le, Q. V. (2014). "Sequence to Sequence Learning with Neural Networks". NeurIPS. arXiv:1409.3215 — Encoder–decoder LSTMs for machine translation, trained end to end.
- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". arXiv:1406.1078 — 提出 GRU，以及用於序列到序列任務的編碼器–解碼器架構。
- Bahdanau, D., Cho, K. & Bengio, Y. (2014). "Neural Machine Translation by Jointly Learning to Align and Translate". arXiv:1409.0473 — 加入注意力，使解碼器能回看整個輸入。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 10 章涵蓋雙向與編碼器–解碼器循環網路，以及截斷式的通過時間反向傳播。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Chung, J., et al. (2014). "Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling". arXiv:1412.3555 — 在多個序列任務上比較 LSTM、GRU 與原始循環單元。
