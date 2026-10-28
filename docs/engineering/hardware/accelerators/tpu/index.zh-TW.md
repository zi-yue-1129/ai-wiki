---
translation_reviewed: 2026-10-28
---

# 張量處理單元

張量處理單元（TPU）是 Google 為神經網路推論設計的特殊應用晶片，核心是一個由乘加單元組成的大型脈動陣列。Jouppi 等人描述第一代 TPU，並報告它執行正式工作負載時，速度約為當時 CPU 與 GPU 的 15 至 30 倍，每瓦效能約高出 30 至 80 倍。它是 [AI 加速器](../index.zh-TW.md)的一種，設計原則是為稠密矩陣乘法固定資料流。

## 問題

資料中心規模的神經網路推論，主要是少數運算元類型的矩陣乘法。通用處理器把大部分能量花在指令擷取、控制與記憶體搬移上，而非算術運算，每次推論的成本因而受到這些額外開銷所主導。

## 核心想法

以一個大型矩陣單元為核心設計晶片，讓資料流過由乘加單元組成的網格。每個權重只載入一次，並在許多輸入之間重複使用；每個激活值則從一個單元傳到下一個單元，因此大多數數值只從記憶體讀取一次。控制邏輯很小，晶片在每個週期執行相同的運算。

## 公式或演算法

核心運算是矩陣乘積 \(Y = XW\)。在大小為 \(n \times n\) 的脈動陣列中，每個單元把其儲存的權重乘上進入的激活值，並把結果加到傳給鄰居的部分和上。因此，大小為 \(m \times k\) 乘以 \(k \times n\) 的層能讓陣列保持忙碌，而記憶體流量很少。第一代 TPU 使用 8 位元整數運算，以精度換取吞吐量。

## 結果

摘要報告，TPU 的速度約為當時 GPU 與 CPU 的 15 至 30 倍，每瓦效能約為 30 至 80 倍。論文也估計，若給 TPU 與 GPU 相同的記憶體頻寬，它的實際吞吐量大約會提高為三倍。這個比較涵蓋當時的工作負載，數字只適用於那些工作負載。

## 限制

固定的資料流適合稠密矩陣工作，但對不規則或稀疏的運算處理得不好。第一代晶片是推論加速器，之後的世代加入了訓練與晶片間互連的功能。這類比較取決於所用的工作負載與軟體堆疊。

## 開放問題與相關變體

- **稀疏工作負載。** 脈動設計能否在不損失效率的情況下利用稀疏性，是開放的設計問題；[Eyeriss v2](../eyeriss-v2/index.zh-TW.md)以不同的方式處理它。
- **記憶體頻寬。** 論文自己的估計顯示，限制晶片的是記憶體，而非矩陣單元。Gholami 等人在下方引用的記憶體牆分析中也提出相同的觀點。
- **相關：** GPU 內的矩陣單元，也就是張量核心，扮演類似的角色，但控制結構較有彈性。

## 相關連結

TPU 的運算叢集透過晶片間網路連接，而擴展的討論依賴於它。它的稠密矩陣設計，也是[Transformer](../../../../theory/models/transformer/index.zh-TW.md)層特別適合它的原因。

## 參考文獻

### 開創性論文

- Jouppi, N. P., 等人 (2017). *In-Datacenter Performance Analysis of a Tensor Processing Unit*. arXiv:1704.04760. https://arxiv.org/abs/1704.04760 — 描述第一代 TPU，並報告其速度與每瓦效能分別為當時 CPU 與 GPU 的 15 至 30 倍與 30 至 80 倍。
- Chen, Y.-H., 等人 (2018). *Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices*. arXiv:1807.07928. https://arxiv.org/abs/1807.07928 — 以可重新配置的晶片內網路利用稀疏性的對照設計。

### 綜述與教科書

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — 綜述使稠密矩陣工作變得高效的架構。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gholami, A., 等人 (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — 說明為什麼記憶體頻寬限制 TPU 等加速器。
- Dao, T., 等人 (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — 展示減少記憶體流量如何加速加速器上的注意力。
