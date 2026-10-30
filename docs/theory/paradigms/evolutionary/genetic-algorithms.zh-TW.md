---
status: draft
last_reviewed: 2026-10-30
translation_reviewed: 2026-10-30
related:
  - theory/paradigms/evolutionary
  - theory/optimization/zeroth-order-and-evolutionary
tags:
  - evolutionary
  - population-based
aliases:
  - Genetic algorithm
  - GA
  - 遺傳演算法
---

# 遺傳演算法

遺傳演算法透過維持一個族群、為每個成員評分，並以選擇、交叉與突變產生下一代，來搜尋候選解的空間。Holland（1975）發展了此方法與其模式（schema）理論。Goldberg（1989）使它作為實用的工程搜尋方法而廣為人知。上層概述見[演化與群體智慧](index.zh-TW.md)。

## 概述

遺傳演算法不需要梯度，也不需要平滑的目標函數。它只需要一種編碼候選解的方式、為每個候選解評分的方法，以及能重組與擾動編碼的運算子。經典形式使用固定長度的位元串，但同樣的迴圈也適用於向量、排列與樹狀結構。

## 問題

許多設計、排程與組合問題的目標是離散、有雜訊的，或只能透過模擬取得。從單一點出發的局部搜尋會停在局部最佳解，而隨機取樣又浪費評估次數。遺傳演算法要問的是：從族群中重組良好的部分解，能否比單獨使用任一方法更快找到更好的解？

## 核心想法

好的解往往共享有用的組成區塊。交叉把兩個親代的部分組合起來，使在兩者中都有效的區塊能出現在某個子代中。選擇偏好較優的候選解，使能提升適應度的區塊愈來愈常見。突變則加入新的變異，使族群不會塌縮到單一模式。

## 演算法

1. 初始化一個由隨機編碼組成的族群。
2. 評估每個成員的適應度。
3. 選出親代，例如以錦標賽選擇，讓較優的候選解更常勝出。
4. 以機率 \(p_c\) 對親代配對進行交叉。對位元串而言，即單點或均勻交叉。
5. 對每個子代進行突變，以機率 \(p_m\) 翻轉每個位元。
6. 以子代取代族群（若使用菁英策略，則保留最佳成員），然後重複。

在 Holland 的模式分析中，模式 \(H\) 是位元串上的一個模板，部分位置固定、其餘為萬用字元。它在下一代的期望複製數有以下下界：

\[
\mathbb{E}[m(H,t+1)] \ge m(H,t)\,\frac{f(H)}{\bar f}\left[1 - p_c\frac{\delta(H)}{l-1} - p_m\, o(H)\right],
\]

其中 \(m(H,t)\) 為第 \(t\) 代中符合 \(H\) 的成員數，\(f(H)\) 為它們的平均適應度，\(\bar f\) 為族群平均適應度，\(\delta(H)\) 為最外側固定位置之間的距離，\(o(H)\) 為固定位置的數目，\(l\) 為字串長度。短、低階且高於平均適應度的模式會在族群中增加。這就是模式定理，也是此方法為何有效的標準解釋。

## 關鍵方法

兩個重要的變體保留了選擇與變異的迴圈，但改變了族群的內容：

- [遺傳規劃](genetic-programming.zh-TW.md)（Koza，1992）演化的是程式樹，而非固定長度的字串。
- [NEAT](neat.zh-TW.md)（Stanley 與 Miikkulainen，2002）同時演化網路的權重與拓撲，並以物種分化保護新結構。

## 主要結果

Holland（1975）給出模式定理，並分析選擇、交叉與突變如何影響模式。Goldberg（1989）介紹各運算子並將其應用於工程問題。本頁不引用數值基準結果，因為結論取決於問題與編碼。在架構搜尋的情境中，Real 等人（2019）報告，以老化演化（aging evolution）找到的 AmoebaNet-A 在 CIFAR-10 上的測試誤差為 3.34 ± 0.06%，參數量為 3.2 M（F = 36），而 NASNet-A 基準為 3.41%。論文指出，演化比強化學習更早達到較高準確率，但此比較只以圖表呈現。

## 限制

- 模式定理解釋的是期望行為，但不保證收斂到全域最佳解。
- 效能高度依賴編碼。不良的表徵會使有用的組成區塊難以形成。
- 早熟收斂很常見。族群失去多樣性，除非突變或小生境（niching）機制維持其多樣性，否則就不再探索。
- 每個候選解都必須評估，因此在評估成本高時方法很昂貴。

## 關聯

- [演化與群體智慧](index.zh-TW.md)是上層概述，遺傳演算法與其他群體方法並列於其中。
- [遺傳規劃](genetic-programming.zh-TW.md)把同樣的迴圈應用於程式樹，而非固定長度的字串。
- [NEAT](neat.zh-TW.md)把交叉與物種分化應用於神經網路拓撲。
- [零階與演化最佳化](../../optimization/zeroth-order-and-evolutionary.zh-TW.md)涵蓋連續參數方法，例如演化策略，它們使用相似的選擇概念。

## 應用

- 排程與路徑規劃，候選解為排列，成本由模擬器計算。
- 架構搜尋，近期的研究如 Real 等人（2019）使用類似錦標賽的演化迴圈來選擇網路設計。

## 未解問題

- 對特定問題而言，哪些組成區塊重要？編碼能否被學習，而非由人手動設計？
- 模式理論中有多少能推廣到具有雜訊、高維適應度的真實問題？

## 參考文獻

### 開創性論文

- Holland, J. H.（1975）。*Adaptation in Natural and Artificial Systems*。University of Michigan Press。https://openlibrary.org/isbn/9780262581110 — 提出模式與模式定理。連結的紀錄為 1992 年的 MIT Press 版本。
- Goldberg, D. E.（1989）。*Genetic Algorithms in Search, Optimization, and Machine Learning*。Addison-Wesley。https://openlibrary.org/isbn/0201157675 — 運算子、模式分析與工程應用的標準教科書式介紹。
- Koza, J. R.（1992）。*Genetic Programming: On the Programming of Computers by Means of Natural Selection*。MIT Press。https://openlibrary.org/isbn/0262111705 — 提出遺傳規劃，以演化的程式樹解決指定任務。
- Stanley, K. O. & Miikkulainen, R.（2002）。Evolving Neural Networks through Augmenting Topologies。*Evolutionary Computation*, 10(2), 99–127。https://doi.org/10.1162/106365602320169811 — 提出 NEAT，同時演化權重與拓撲，並以物種分化保護新結構。
- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V.（2019）。Regularized Evolution for Image Classifier Architecture Search。收錄於 *Proceedings of the AAAI Conference on Artificial Intelligence*。arXiv:1802.01548。https://arxiv.org/abs/1802.01548 — 以錦標賽選擇搜尋網路架構的現代遺傳式迴圈範例。

### 綜述與教科書

- Eiben, A. E. & Smith, J. E.（2015）。*Introduction to Evolutionary Computing*。Springer。https://doi.org/10.1007/978-3-662-44874-8 — 教科書，涵蓋表徵、運算子與遺傳演算法的收斂行為。
- Bäck, T.（1996）。*Evolutionary Algorithms in Theory and Practice*。Oxford University Press。https://doi.org/10.1093/oso/9780195099713.001.0001 — 教科書，分析群體搜尋中的選擇壓力與其他設計選擇。

## 延伸學習

供想進一步探索的讀者參考，這些不是參考文獻。

- [DEAP](https://github.com/DEAP/deap) 是開源的 Python 框架，可用來建構遺傳演算法及相關方法。
