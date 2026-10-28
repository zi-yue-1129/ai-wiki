---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/interpretability
  - theory/models/transformer
  - brain-mind/neuroai
tags:
  - interpretability
  - probing
  - representations
aliases:
  - 探測分類器
  - 表徵分析
  - Probing classifiers
  - Representation analysis
  - Linear probes
---

# 探測分類器與表徵分析

探測分類器（probing classifier）是一個簡單模型，經訓練後從較大網路的內部啟動值中讀取某種性質。若一個小型分類器能從某一層的啟動值中恢復該性質，就稱該層編碼了此性質。探測是用來詢問網路表徵了什麼的最古老、也最廣泛使用的工具之一，而它與神經科學有密切的平行關係，後者以相同的邏輯分析大腦的記錄。

## 概述

訓練後的網路不透明，但其啟動值是可以讀取的。探測會提出一個具體的問題：這一層是否含有詞性、物件身分、棋盤上棋子位置，或某陳述是否為真的資訊？探測是在凍結的啟動值上訓練，因此網路本身不會被改變。探測的準確率高，表示資訊以探測器能使用的形式存在。困難之處在於，足夠強大的探測器可以找到網路從未使用的資訊，因此單靠探測無法說明模型依賴的是什麼。

## 核心概念

- **探測器（probe）**：在某一層的啟動值 \(h\) 上訓練、用以預測外部標籤 \(y\) 的分類器或迴歸器。
- **線性探測器（linear probe）**：形式為 \(\hat{y} = \mathrm{softmax}(Wh + b)\) 的探測器。其簡單是刻意的，因為線性映射能讀出的資訊，較容易說明模型確實在使用它。
- **控制任務（control task）**：在相同輸入上指派隨機標籤後訓練的探測器，用來量測探測器能記住多少。
- **選擇性（selectivity）**：探測器在真實任務上的準確率減去其在控制任務上的準確率。
- **表徵相似度（representational similarity）**：透過兩個系統對相同刺激的回應之間的相似度結構來比較它們，而非逐一比對單一單元。

## 運作方式

常見的程序有四個步驟：

1. 選定一個訓練好的模型與一層。
2. 對標籤 \(y\) 已知的輸入蒐集啟動值 \(h\)，並將資料分為訓練集與測試集。
3. 在訓練啟動值上訓練探測器，並在測試集上量測準確率。
4. 與基準比較，例如在原始輸入上的探測器、在隨機初始化網路上的探測器，或控制任務。

比較各層可以顯示資訊在何處出現、又在何處消失。Alain 與 Bengio（2016）在一個深度影像網路的每個深度上使用線性探測器，發現類別標籤的線性可分性通常隨深度增加。他們的工作使探測成為標準的診斷工具。

## 主要方法

- **[線性探測器](linear-probes.md)（Alain & Bengio, 2016）。** 每一層訓練一個線性分類器，以顯示類別資訊如何隨深度發展。此方法簡單快速；其弱點在於它報告的是可解碼性，而非使用情形。
- **結構探測器（Hewitt & Manning, 2019）。** 學習一個對詞表徵的線性轉換，使轉換後的平方距離近似句法樹上的距離。此探測器能從上下文嵌入中恢復樹結構，這是單純的標籤分類探測所無法顯示的。
- **[控制任務](control-tasks.md)（Hewitt & Liang, 2019）。** 報告選擇性，即真實任務與隨機標籤準確率之間的差距，使高分代表表徵確實編碼了該性質，而非探測器在記憶。
- **[表徵相似度分析](representational-similarity-analysis.md)（Kriegeskorte et al., 2008）。** 透過兩系統回應之間的成對相異度矩陣來比較它們，使網路某一層與大腦區域能在相同刺激上進行比較。
- **結合因果介入的探測（Li et al., 2023）。** 在僅以落子序列訓練的序列模型中，以探測器辨識黑白棋（Othello）的棋盤狀態，並對該表徵進行介入，檢查模型的輸出是否改變。此類介入測試的是使用，而不只是存在。

## 結果

Hewitt 與 Liang（2019）主張，探測器能夠記住與詞彙相關的標籤，因此單看準確率會高估表徵所含的內容；選擇性衡量的正是這個差距。Hewitt 與 Manning（2019）報告，對 ELMo 與 BERT 的嵌入做線性轉換後，平方距離對應句法樹上的距離，平方範數對應深度，而基線模型沒有這種結構。Li 等人（2023）顯示，僅在落子序列上訓練的模型會形成非線性的棋盤狀態內部表徵，對此表徵的介入能控制模型的輸出。Park 等人（2023）報告 LLaMA-2 中概念的線性表徵，並顯示這些表徵與線性探測及引導向量（steering vectors）相關。

## 限制

- **存在不等於使用。** 探測只顯示資訊可被解碼，並未顯示模型是否依賴它。Belinkov（2022）批判性地回顧了探測分類器的方法學限制。
- **探測器容量。** 探測器架構的選擇會改變結論。線性探測器可用來限制此問題，但非線性結構仍可能被漏掉。
- **標籤品質。** 探測器會承襲標籤中的錯誤，而像真實性這類抽象性質的標籤很難定義。
- **混淆因子。** 探測器可能抓到與目標相關的其他性質。平衡的資料集與控制可降低此風險。

## 關聯

探測是神經網路可解釋性與神經科學之間最直接共用的工具。表徵相似度分析原本源自神經科學，用來將網路與大腦記錄進行比較；更廣泛的研究計畫見 [NeuroAI](../../brain-mind/neuroai/index.md)。探測通常應用於的架構，即 Transformer 及其殘差流，見 [Transformer](../../theory/models/transformer/index.md)。探測是[可解釋性](index.md)概述中列出的方法之一，與[特徵歸因](feature-attribution.md)並列。

## 應用

- 在決定介入位置之前，檢查語言模型是否編碼了句法、語意或世界狀態。
- 診斷哪些層攜帶了對下游任務有用的資訊。
- 在共同刺激上比較模型與大腦區域。
- 稽核敏感屬性：即使從輸入中移除，檢查表徵是否仍編碼它們。

## 未解問題

- **因果使用。** 如何將探測方向連結到模型所執行的計算，而不只是它所含的內容。
- **非線性與分散式編碼。** 線性探測器可能遺漏以複雜方式承載的資訊；更好的探測器能否在不過度擬合的情況下揭露這些資訊，仍未解決。
- **概念幾何。** 線性表徵假說是否廣泛適用於不同模型與概念，是活躍的研究領域。

## 參考文獻

### 開創性論文

- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. *arXiv preprint*. https://arxiv.org/abs/1610.01644 — 在深度網路的每一層引入線性探測器，以量測類別資訊如何隨深度發展。
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — 顯示上下文嵌入的線性轉換能恢復句法樹距離。
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — 引入控制任務與選擇性，以區分探測器的記憶與被編碼的資訊。
- Kriegeskorte, N., Mur, M. & Bandettini, P. (2008). Representational similarity analysis – connecting the branches of systems neuroscience. *Frontiers in Systems Neuroscience*. https://doi.org/10.3389/neuro.06.004.2008 — 定義表徵相似度分析，透過回應幾何來比較系統。
- Li, K., Hopkins, A. K., Bau, D., Viégas, F., Pfister, H. & Wattenberg, M. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — 在以黑白棋落子序列訓練的模型中發現非線性的棋盤狀態表徵，並以介入測試它。
- Park, K., Choe, Y. J. & Veitch, V. (2023). The Linear Representation Hypothesis and the Geometry of Large Language Models. *arXiv preprint*. https://arxiv.org/abs/2311.03658 — 將語言模型中概念的線性表徵形式化並加以檢驗。

### 綜述與教科書

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — 批判性地回顧探測分類器框架，包括其優點、缺點與進展。

## 延伸學習

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — 將探測延伸到因果分析的機制可解釋性研究。
