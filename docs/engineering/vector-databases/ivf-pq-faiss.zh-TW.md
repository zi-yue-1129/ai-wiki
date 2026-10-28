---
related:
- engineering/vector-databases
- engineering/hardware
tags:
- engineering
- retrieval
- vector search
- quantisation
aliases:
- IVF-PQ
- FAISS 中的 IVF-PQ
---

# FAISS 中的 IVF-PQ

IVF-PQ 結合了倒排檔案索引與乘積量化。它保存壓縮後的向量，使超大型資料集能放進 GPU 或伺服器的記憶體，並且每次查詢只掃描少數幾個區格。這個方法實作於 FAISS 函式庫，由 Johnson、Douze 與 Jégou（2017）說明。

## 概述

全精度向量佔用大量記憶體，掃描它們的時間又與資料量成正比。IVF-PQ 同時降低這兩者。倒排檔案把資料集切成多個區格，因此查詢只需看最近的幾個。乘積量化則把每個儲存的向量壓縮成短碼，並用查找表從短碼估計距離。

## 關鍵概念

- **粗量化器**：一組質心，通常以 k-means 學習，用來把每個向量指派到一個區格。
- **倒排檔案（IVF）**：每個區格對應一份向量清單。查詢會探查固定數量的區格，這是主要的速度設定。
- **乘積量化（PQ）**：把向量切成子向量，每個子向量以其在小型碼本中最近質心的索引取代。
- **殘差編碼**：向量相對於所屬區格質心進行編碼，因此編碼描述的是局部偏移，而不是整個向量。

## 運作方式

```mermaid
flowchart LR
  X[查詢向量] --> C[粗量化器挑出最近的區格]
  C --> P[只掃描被探查的區格]
  P --> L[用 PQ 查找表估計距離]
  L --> R[以精確距離重新排序前幾名候選]
```

## 關鍵想法

- **問題**：為數十億筆項目儲存並掃描全精度向量，超過單一 GPU 或伺服器的記憶體與時間。
- **核心想法**：用粗量化器把資料集分成 $n_{\text{list}}$ 個區格（倒排檔案，IVF），使查詢只掃描最近的少數區格。在每個區格內，用乘積量化（PQ）壓縮每個向量：把它切成 $m$ 個子向量，並為每個子向量儲存最近質心的索引，每個子向量只佔一個位元組。
- **方程式或演算法**：與壓縮向量的距離近似為 $\lVert q - x \rVert^2 \approx \sum_{j=1}^{m} \lVert q_j - c_{j}(x_j) \rVert^2$，其中 $c_j(x_j)$ 是第 $j$ 個子向量所儲存的質心。預先計算的查找表使每一項都只是一次表格讀取。
- **結果**：論文指出在 GPU 上完成十億規模的相似度搜尋，記憶體、速度與召回率之間的取捨由 $m$ 與探查的區格數控制。
- **限制**：PQ 的誤差會限制召回率，因此系統常以精確距離重新排序前幾名候選。訓練量化器需要有代表性的資料。

## 取捨

- **記憶體與召回率**：每個向量的位元組越少、探查的區格越少，越能節省記憶體與時間，但每一項都會降低召回率。
- **訓練成本**：粗量化器與碼本必須以代表資料集的資料訓練，當資料分布改變時需要重新訓練。
- **更新**：新向量可以加入既有區格，但內容大幅變動時需要重新訓練。

## 開放問題

- 當資料分布漂移時，量化器應多久重新訓練一次？又該如何偵測？
- 落在區格之間的罕見查詢，會損失多少召回率？

## 參考文獻

- Johnson, J., Douze, M. & Jégou, H. (2017). *Billion-scale similarity search with GPUs*. arXiv:1702.08734. https://arxiv.org/abs/1702.08734 — 說明 FAISS，以及使用倒排檔案與乘積量化的十億規模 GPU 搜尋。
- Malkov, Y. A. & Yashunin, D. A. (2016). *Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs*. arXiv:1603.09320. https://arxiv.org/abs/1603.09320 — 提出倒排檔案索引的圖式替代方案。
- Guo, R. et al. (2019). *Accelerating Large-Scale Inference with Anisotropic Vector Quantization*. arXiv:1908.10396. https://arxiv.org/abs/1908.10396 — 提出一種量化損失，用來改進 IVF 式索引所使用的乘積量化碼。
- Aumüller, M., Bernhardsson, E. & Faithfull, A. (2018). *ANN-Benchmarks: A Benchmarking Tool for Approximate Nearest Neighbor Algorithms*. arXiv:1807.05614. https://arxiv.org/abs/1807.05614 — 在常見資料集上比較量化式與圖式索引的召回率與速度。
- Thakur, N. et al. (2021). *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models*. NeurIPS 2021 Datasets and Benchmarks. https://arxiv.org/abs/2104.08663 — 在 18 個資料集上評估檢索器，索引的召回率直接影響最終品質。
