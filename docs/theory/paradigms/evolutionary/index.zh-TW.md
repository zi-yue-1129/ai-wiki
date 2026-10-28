---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/meta-learning
  - theory/optimization/zeroth-order-and-evolutionary
  - applications/science
tags:
  - evolutionary
  - swarm
  - population-based
aliases:
  - 演化計算
  - 群體智慧
  - 族群搜尋
---

# 演化計算與群體智慧

有些搜尋問題沒有梯度可以跟隨：目標是離散、多峰的，或只能透過執行模擬器取得。演化與群體方法的處理方式，是維護一個**族群**的候選解、為每個候選打分，再從最好的候選建立下一代。搜尋是靠整個族群進行，而不是靠單一點。

## 概觀

本頁是[範式](../index.zh-TW.md)章節的一部分。每個方法各有獨立頁面，本頁負責比較。以梯度估計方式從函數值估計搜尋方向的零階方法（演化策略與 CMA-ES），見[零階與演化最佳化](../../optimization/zeroth-order-and-evolutionary.zh-TW.md)，本頁僅作摘要。

## 關鍵方法

| 方法 | 族群更新方式 | 典型應用 | 頁面 |
|---|---|---|---|
| 遺傳演算法 | 在位元串或向量上做選擇、交叉與突變 | 排程、設計 | [遺傳演算法](genetic-algorithms.zh-TW.md) |
| 遺傳規劃 | 在程式樹上做交叉與突變 | 符號迴歸 | [遺傳規劃](genetic-programming.zh-TW.md) |
| 演化策略與 CMA-ES | 抽取高斯樣本，並把其均值與共變異數移向好的樣本 | 連續黑箱最佳化 | [零階與演化](../../optimization/zeroth-order-and-evolutionary.zh-TW.md) |
| NEAT | 同時演化權重與拓撲，並使用創新編號 | 神經演化、控制 | [NEAT](neat.zh-TW.md) |
| MAP-Elites | 在行為網格的每個格子中保留最佳解 | 多樣的解、機器人動作庫 | [MAP-Elites](map-elites.zh-TW.md) |
| 粒子群最佳化 | 每個粒子依自身與鄰居的最佳位置移動 | 連續最佳化 | [粒子群最佳化](particle-swarm.zh-TW.md) |
| 螞蟻演算法 | 螞蟻在好的路徑上留下費洛蒙，依比例抽樣路徑 | 組合式路徑問題 | [螞蟻演算法](ant-colony.zh-TW.md) |

## 關鍵概念

- **適應度**：每個候選解的分數，透過執行目標函數取得，不需要微分。
- **變異**：新候選由既有候選重組或擾動而來。交叉混合兩個親代，突變加入雜訊。
- **選擇壓力**：最好的候選被偏好的程度。壓力太大會失去多樣性，太小則搜尋會漫無方向。
- **多樣性**：族群收斂到一點後就無法再探索。小生境、物種分化與品質多樣性方法讓多個解同時存活。

## 與深度學習的結合

- **神經架構搜尋**：演化一群網路設計，並以訓練每個設計來打分。成本很高，因此後續研究會讓候選之間共享權重。
- **演化策略作為強化學習的替代**：Salimans et al.（2017）顯示，簡單的演化策略估計器能在許多平行工作節點上大規模訓練策略，不必透過環境反向傳播。
- **以 LLM 驅動的搜尋**：語言模型提出新候選，自動評估器為其打分。FunSearch（Romera-Paredes et al., 2023）以此搜尋可構造新數學物件的程式。AlphaEvolve（Novikov et al., 2025）把相同模式用於演算法發現。

## 群體智慧

群體方法使用簡單的代理，彼此在局部互動，產生有用的集體結果。本章中有獨立頁面的是粒子群最佳化與螞蟻演算法。Boids 是電腦圖學中的群飛模型，也是同一原則的早期例子，這裡不再深入。

## 與大腦的關係

演化塑造先天結構，學習則加以調整。Zador（2019）主張，許多動物行為來自基因指定的接線，而不是從零開始學習。這個觀點推動了元學習與學習者起始時歸納偏置的研究。見[元學習](../meta-learning/index.zh-TW.md)。

## 限制

- 評估成本高。每個候選通常需要完整執行一次目標，因此在平滑問題上，族群方法所需的評估次數遠多於梯度方法。
- 結果取決於編碼與運算子。同一個問題，依表示方式不同可能很容易，也可能很難。
- 大多數這類方法的收斂保證很弱，其成效通常以實驗展示。

## 未解問題

- **以學習得到的變異運算子擴展。** LLM 驅動的運算子讓突變步驟豐富許多，但評估器必須便宜且可靠。
- **開放式演化。** 搜尋能否在沒有固定目標的情況下，持續產生新穎且日益複雜的解，仍未解決。

## 參考文獻

### 開創性論文

- Salimans, T., Ho, J., Chen, X., Sidor, S. & Sutskever, I. (2017). *Evolution Strategies as a Scalable Alternative to Reinforcement Learning*. arXiv:1703.03864. https://arxiv.org/abs/1703.03864 — 顯示演化策略估計器能在許多平行工作節點上大規模訓練策略。
- Romera-Paredes, B., et al. (2023). *Mathematical discoveries from program search with large language models*. Nature. https://doi.org/10.1038/s41586-023-06924-6 — 以語言模型搭配自動評估器，搜尋可構造新數學物件的程式。
- Mouret, J.-B. & Clune, J. (2015). *Illuminating search spaces by mapping elites*. arXiv:1504.04909. https://arxiv.org/abs/1504.04909 — 提出 MAP-Elites，在行為網格的每個格子中保留最佳解。

### 綜述與教科書

（本頁尚未查核任何項目）

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Novikov, A., et al. (2025). *AlphaEvolve: A coding agent for scientific and algorithmic discovery*. arXiv:2506.13131. https://arxiv.org/abs/2506.13131 — 以語言模型的程式碼代理，搭配自動評估器演化程式，用於科學與演算法問題。
- Zador, A. M. (2019). *A critique of pure learning and what artificial neural networks can learn from animal brains*. Nature Communications. https://pmc.ncbi.nlm.nih.gov/articles/PMC6704116 — 主張許多動物行為來自基因編碼的結構，而非從零開始學習。

## 延伸學習

- [DEAP](https://github.com/DEAP/deap)、[EvoTorch](https://github.com/nnaisense/evotorch) 與 [pyribs](https://pyribs.org/) 是演化與品質多樣性搜尋的開源函式庫。
