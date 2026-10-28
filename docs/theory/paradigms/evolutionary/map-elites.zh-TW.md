---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/evolutionary
  - theory/paradigms/reinforcement-learning
tags:
  - evolutionary
  - quality-diversity
aliases:
  - MAP-Elites
  - 品質多樣性
---

# MAP-Elites

大多數演化搜尋只保留一個最佳解，或收斂到一個族群。MAP-Elites 則在網格的每個格子中保留找到的最佳解。格子由行為描述子定義，因此檔案庫保存的是一組行為不同的解。

## 概觀

本頁是[演化計算與群體智慧](index.zh-TW.md)的子頁面。上層概述會把它與遺傳演算法、演化策略並列比較。它的目標與最佳化不同：要用許多好而且不同的解來填滿檔案庫。

## 問題

單一最優解可能掩蓋有用的替代方案。一台有一種快速步態的機器人，若其中一條腿損壞就可能失效。設計任務也可能需要多個在不同特徵間取捨的解。標準演化會丟棄任何不是唯一最佳的解，因此這些替代方案會遺失。

## 核心想法

Mouret 與 Clune 在行為描述子的空間上定義一個網格。每個候選同時評估其效能與描述子。候選會放入描述子所指定的格子，只有在效能優於該格原有解時才會取代它。下一代的親代從檔案庫中隨機抽取，因此每個已填滿的格子都能產生後代。

## 演算法

1. 隨機產生一組候選，為每個候選評估適應度 \(f\) 與描述子 \(b\)。
2. 將每個候選放入格子 \(c(b)\)。若格子為空，或 \(f\) 優於該格現有的適應度，就保留它。
3. 重複：從檔案庫中均勻隨機抽取一個菁英，對它做突變（也可選擇與另一個菁英重組），評估後代，並依步驟 2 插入。

輸出是檔案庫本身，而非族群。會回報其覆蓋率（有多少格子被填滿）以及每格的最佳值。

## 關鍵結果

Mouret 與 Clune（2015）報告，此方法能產生大量高效能但質性不同的解，並在三個問題領域中示範，包括模擬與實體的軟體機器人。腿部受損時能恢復的六足機器人結果，來自 Cully 等人（2015），他們以類似的檔案庫建立步態庫。腿部故障時，機器人會從檔案庫中找到可用的步態，而不必從頭搜尋。兩篇摘要都未給出數字，因此本頁不引用任何數字。

## 限制

- 格子數會隨描述子維度數呈指數成長，因此此方法只適用於描述子數量少的情況。Vassiliades et al.（2016）以中心 Voronoi 鑲嵌把檔案庫擴展到較大的描述子空間。
- 描述子的選擇是一項設計決定，會影響結果。描述子不佳時，檔案庫雖然覆蓋了整個網格，卻沒有涵蓋有用的行為。
- 每個格子內的插入是貪婪的，因此格子可能保留一個局部良好、但遠離該行為下可達最佳值的解。

## 關聯

- [演化計算與群體智慧](index.zh-TW.md)是把 MAP-Elites 與遺傳演算法、演化策略並列的概述。
- 演化策略與 CMA-ES（[零階與演化](../../optimization/zeroth-order-and-evolutionary.zh-TW.md)）最佳化單一搜尋分布，而 MAP-Elites 維護的是多樣的檔案庫。
- 品質多樣性方法的綜述見 Pugh et al.（2016）。新穎性搜尋（Lehman & Stanley, 2011）是更早的多樣性途徑，它完全捨棄目標函數。

## 應用

- 具備可從損壞中恢復之動作庫的機器人控制。
- 創意與程序式生成，其中重視多樣的輸出。

## 未解問題

- 如何自動選擇描述子空間，使網格涵蓋有用的行為，而不需人工設計？
- 在高維描述子空間中，如何有效率地使用檔案庫？

## 參考文獻

### 開創性論文

- Mouret, J.-B. & Clune, J. (2015). *Illuminating search spaces by mapping elites*. arXiv:1504.04909. https://arxiv.org/abs/1504.04909 — 提出 MAP-Elites，在行為網格的每個格子中保留最佳解，並應用於三個問題領域，包括軟體機器人。
- Cully, A., Clune, J., Tarapore, D. & Mouret, J.-B. (2015). *Robots that can adapt like animals*. *Nature*, 521, 503–507. https://doi.org/10.1038/nature14422 — 以類似 MAP-Elites 的檔案庫建立步態庫，讓受損的六足機器人能從檔案庫中嘗試替代方案而恢復。
- Vassiliades, V., Chatzilygeroudis, K. & Mouret, J.-B. (2016). *Using centroidal Voronoi tessellations to scale up the multi-dimensional archive of phenotypic elites algorithm*. arXiv:1610.05729. https://arxiv.org/abs/1610.05729 — 以中心 Voronoi 鑲嵌把檔案庫擴展到較大的描述子空間。
- Pugh, J. K., Soros, L. B. & Stanley, K. O. (2016). *Quality diversity: a new frontier for evolutionary computation*. Frontiers in Robotics and AI, 3, 40. https://doi.org/10.3389/frobt.2016.00040 — 綜述品質多樣性方法，MAP-Elites 屬於此類。
- Lehman, J. & Stanley, K. O. (2011). *Abandoning objectives: evolution through the search for novelty alone*. Evolutionary Computation, 19, 189–223. https://doi.org/10.1162/EVCO_a_00025 — 主張以搜尋新穎性取代目標函數，是較早的多樣性途徑。

## 延伸學習

- [pyribs](https://pyribs.org/) 是實作 MAP-Elites 與相關品質多樣性演算法的開源函式庫。
