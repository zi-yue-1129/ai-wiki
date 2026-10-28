---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning
  - theory/models/transformer
  - start/history/expert-systems-and-winters
tags:
  - history
  - deep learning
  - large language models
aliases:
  - 深度學習革命
  - 深度學習發展
  - Deep learning revolution
---

# 歷史：深度學習革命（2006 至今）

從 2000 年代中期開始，多層神經網路從小眾研究主題成為 AI 的核心方法。它們的成功依賴於訓練深層模型的方法、大型標記與未標記資料集，以及讓大規模實驗負擔得起的硬體。本頁依序介紹主要步驟：從深度信念網路、AlexNet，到序列模型、AlphaGo、Transformer，以及大型語言模型的時代。同時說明每個步驟如何改變這個領域的制度，而不只是方法。

## 概述

這波復甦始於一種逐層訓練深層網路的方法。Hinton、Osindero 與 Teh 展示，深度信念網路可以用貪婪的逐層程序訓練，之後再進行微調 [(Hinton, Osindero and Teh, 2006)](https://doi.org/10.1162/neco.2006.18.7.1527)。這個方法顯示深度可以重新變得可以訓練。幾年之內，重心從預訓練轉向在大量資料上，以改進的最佳化器與激活函數訓練的大型監督式網路。

## 關鍵步驟

- **深度信念網路（2006）**：逐層預訓練讓深層模型在實務上可以訓練 [(Hinton et al., 2006)](https://doi.org/10.1162/neco.2006.18.7.1527)。
- **ImageNet 與 AlexNet（2012）**：在 ImageNet 上訓練的深度卷積網路，使影像分類有了大幅躍進。論文展示了資料與運算規模的價值 [(Krizhevsky, Sutskever and Hinton, 2012)](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)。
- **序列到序列學習（2014）**：編碼器—解碼器網路學會把一個序列對映到另一個序列，例如把英文句子翻譯成法文 [(Sutskever, Vinyals and Le, 2014)](https://arxiv.org/abs/1409.3215)。
- **注意力機制（2014）**：在翻譯中學習對齊來源與目標的詞，移除了單一固定長度向量的瓶頸 [(Bahdanau, Cho and Bengio, 2014)](https://arxiv.org/abs/1409.0473)。
- **AlphaGo（2016）**：深度網路與樹搜尋的結合，讓電腦在圍棋上達到過去難以企及的水準 [(Silver et al., 2016)](https://doi.org/10.1038/nature16961)。
- **Transformer（2017）**：純注意力的架構成為序列建模的預設選擇，之後也用於許多其他任務 [(Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)。
- **大型語言模型（2020 起）**：以大量資料與參數擴展 Transformer 語言模型，帶來從提示中進行少樣本學習的能力。例如 GPT-3 的報告描述了一個具 1,750 億參數的模型 [(Brown et al., 2020)](https://arxiv.org/abs/2005.14165)。

## 領域如何改變

這場革命改變的是這個領域的組織方式，而不只是它做了什麼。像 ImageNet 這樣的基準讓進展可見並可共享，也樹立了「共同資料集定義一個研究社群」的模式。開源框架降低了實驗的成本。例如 PyTorch 被介紹為兼顧易用性與速度的函式庫 [(Paszke et al., 2019)](https://arxiv.org/abs/1912.01703)。大型產業實驗室以大學難以匹敵的規模投入研究，訓練成本也開始決定誰能在前沿工作。

深度學習也帶來新的角色與新的問題。研究越來越仰賴大型工程團隊與運算資源的取得，這種依賴是[算力治理](../../../society/governance/compute-governance.zh-TW.md)等後續頁面的主題。

## 與其他頁面的關聯

較早的步驟見[專家系統與寒冬章節](../expert-systems-and-winters/index.zh-TW.md)。方法見[深度學習](../../../theory/deep-learning/index.zh-TW.md)與 [Transformer](../../../theory/models/transformer/index.zh-TW.md)。[AI 發展史](../index.zh-TW.md)總覽中的時間軸，把日期集中列在一處。

## 應用

深度學習如今支撐語音辨識、翻譯、影像分析、藥物發現，以及推薦與搜尋系統。許多應用來自於方法在不同任務間的遷移，而非各自獨立的研究計畫。

## 開放問題

- 規模化帶來的收益，哪些會持續，哪些會趨於飽和？
- 轉向大型實驗室，在多大程度上改變了所提出的研究問題？
- 哪些制度性改變，例如共享基準或開放釋出，有助於領域判斷進展？

## 參考文獻

### 重要論文

- Hinton、Osindero 與 Teh，*A Fast Learning Algorithm for Deep Belief Nets*，Neural Computation（2006）。https://doi.org/10.1162/neco.2006.18.7.1527 — 提出訓練深度信念網路的逐層程序。
- Krizhevsky、Sutskever 與 Hinton，*ImageNet Classification with Deep Convolutional Neural Networks*，NeurIPS（2012）。https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 論文。
- Sutskever、Vinyals 與 Le，*Sequence to Sequence Learning with Neural Networks*（2014）。https://arxiv.org/abs/1409.3215 — 用於序列轉換的編碼器—解碼器模型。
- Bahdanau、Cho 與 Bengio，*Neural Machine Translation by Jointly Learning to Align and Translate*（2014）。https://arxiv.org/abs/1409.0473 — 為神經機器翻譯引入注意力機制。
- Silver 等人，*Mastering the game of Go with deep neural networks and tree search*，Nature（2016）。https://doi.org/10.1038/nature16961 — AlphaGo 論文。
- Vaswani 等人，*Attention Is All You Need*（2017）。https://arxiv.org/abs/1706.03762 — 提出 Transformer。
- Brown 等人，*Language Models are Few-Shot Learners*（2020）。https://arxiv.org/abs/2005.14165 — GPT-3 的報告。

### 綜述與教科書

- LeCun、Bengio 與 Hinton，*Deep learning*，Nature（2015）。https://doi.org/10.1038/nature14539 — 由該領域三位核心人物撰寫的核心理念綜述。

### 文章與文件

- Paszke 等人，*PyTorch: An Imperative Style, High-Performance Deep Learning Library*（2019）。https://arxiv.org/abs/1912.01703 — 描述一個廣泛使用的框架及其設計目標。
