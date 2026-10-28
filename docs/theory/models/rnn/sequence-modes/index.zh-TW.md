---
related:
- theory/models/transformer
aliases:
  - Sequence Modes
  - Bidirectional RNN
  - Encoder–Decoder
  - 序列模式
  - 雙向循環網路
tags:
  - recurrent networks
  - sequence modelling
  - training
translation_reviewed: 2026-10-28
---

# 序列模式

同一個循環單元可以用幾種方式連接，以適應不同任務。選擇包括：序列被讀取的方向、輸入序列如何映射到輸出序列、單元如何堆疊，以及長序列的訓練如何組織。每種選擇都會改變網路在每一步能使用的資訊，以及訓練的成本。

## 概觀

| 模式 | 第 \(t\) 步可用的資訊 | 典型用途 |
|---|---|---|
| 單向 | 直到 \(t\) 的輸入 | 串流、生成 |
| 雙向 | 所有輸入 | 為完整序列加標籤 |
| 編碼器–解碼器 | 整個輸入，之後是已生成的輸出 | 翻譯、摘要 |
| 堆疊 | 每一步都有更深的特徵 | 更高的容量 |

## 做法

### 雙向循環

雙向 RNN 分別向前與向後做一次循環，並在每個位置把兩個隱藏狀態串接起來。因此每個輸出都能使用完整脈絡，適合整段錄音都可用的標記與辨識任務。它不能用於串流，因為需要未來的輸入。

### 編碼器–解碼器

編碼器讀取輸入序列，並把它壓縮成一個狀態。解碼器再從該狀態開始，一次生成一個 token，並把自己的預測餵回去。Sutskever 等人（2014）展示了這種架構能以端到端的神經網路進行翻譯。單一固定大小的狀態限制了兩部分之間傳遞的資訊量，這正是注意力被引入來緩解的問題。

### 堆疊與深度

多層循環可以堆疊，每層的輸出作為下一層的輸入。較深的堆疊能表示更抽象的特徵，但會使梯度路徑變長，因此常在層與層之間使用殘差或門控連接。

### 長序列訓練

通過時間的反向傳播會把網路沿整個序列展開，記憶體成本與序列長度成正比。截斷式的時間反向傳播則把長序列切成固定長度的片段處理，跨片段保留狀態，但把梯度流限制在每個片段內。教師強制（teacher forcing）在訓練時餵入真實的前一個輸出，能加速學習，但生成時模型使用自己的輸出，兩者會產生不匹配。

## 關鍵方法

| 方法 | 年份 | 核心想法 | 頁面 |
|---|---|---|---|
| 序列到序列學習 | 2014 | 以編碼器 LSTM 與解碼器 LSTM 端到端地翻譯 | [序列到序列](sequence-to-sequence/index.md) |

## 取捨

- **脈絡與延遲。** 雙向模式能看到更多脈絡，但無法串流。單向模式可串流，但無法使用未來的脈絡。
- **記憶體與準確率。** 截斷式訓練節省記憶體，但可能遺漏比片段更長的依賴。
- **教師強制。** 它能穩定並加速訓練，但推論時生成的誤差會累積，這個問題在「曝光偏差」（exposure bias）之名下被研究。

## 相關連結

編碼器–解碼器的架構正是注意力首次被加入序列模型的場景，見[注意力變體](../../transformer/attention-variants/index.md)。堆疊與殘差連接也與 [Transformer](../../transformer/index.md) 家族共用，而串流的問題在[狀態空間](../../ssm/index.md)家族中再次出現。

## 未解問題與更多變體

- **曝光偏差。** 在模型自己的輸出上訓練（例如排程取樣）能減少不匹配，但會使訓練更複雜，效果也因任務而異。
- **長序列訓練。** 分段訓練以記憶體換取可能遺漏的長程結構，如何選擇片段邊界的更好方法尚無定論。
- **雙向生成。** 用雙向性來生成（而不只是標記）很困難，因為模型正在生成的正是未來。

## 參考文獻

### 開創性論文

- Sutskever, I., Vinyals, O. & Le, Q. V. (2014). "Sequence to Sequence Learning with Neural Networks". NeurIPS. arXiv:1409.3215 — 以端到端的編碼器–解碼器循環網路進行機器翻譯。
- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". arXiv:1406.1078 — 用於翻譯的 RNN 編碼器–解碼器與門控單元。
- Bahdanau, D., Cho, K. & Bengio, Y. (2014). "Neural Machine Translation by Jointly Learning to Align and Translate". arXiv:1409.0473 — 加入注意力，使解碼器能回看整個輸入。

### 綜述與教科書

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — 第 10 章涵蓋雙向與編碼器–解碼器循環網路，以及截斷式的通過時間反向傳播。

### 講座與影片

（本頁尚未核對）

### 文章與文件

- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). "On the difficulty of training Recurrent Neural Networks". arXiv:1211.5063 — 分析使長序列訓練困難的梯度問題。
