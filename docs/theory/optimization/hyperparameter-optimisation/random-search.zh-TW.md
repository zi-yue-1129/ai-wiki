---
translation_reviewed: 2026-10-28
---

# 隨機搜尋（Bergstra 與 Bengio，2012）

隨機搜尋從搜尋空間上的分布中，獨立取樣每一組超參數設定，訓練後保留最好的一組。它是超參數最佳化的標準基準。本頁是[超參數最佳化](index.md)的一部分。

## 概述

在這篇論文之前，格點搜尋是調校模型的常用方法。Bergstra 與 Bengio（2012）指出，當只有少數超參數重要時，隨機取樣設定能以相同的執行次數，比格點更好地覆蓋重要的維度。隨機搜尋不需要目標函數的模型，容易平行化，也不會把執行次數浪費在只在不重要維度上不同的組合。

## 關鍵概念

- **取樣分布**：每個超參數抽取所用的分布，例如學習率在對數尺度上的均勻分布。
- **有效維度**：真正改變目標函數的超參數數目，通常遠小於調校的超參數數目。
- **試驗**：一組取樣出的設定，經訓練並在驗證集上評分。

## 問題

在 \(n\) 次訓練執行的固定預算與給定的搜尋空間下，應訓練哪些設定，才能以高機率找到最好的一組？

## 運作方式

每次試驗從取樣分布中抽出設定 \(x\)，並記錄驗證分數 \(f(x)\)。最好的試驗即為回傳結果。試驗彼此獨立，因此可以在任意多個工作者上執行。

對於佔取樣質量比例為 \(p\) 的搜尋空間區域，\(n\) 次獨立試驗都不落在其中的機率為 \((1-p)^n\)，因此至少落在其中一次的機率為 \(1-(1-p)^n\)。例如 \(n = 60\)、\(p = 0.05\) 時，此機率約為 \(1 - 0.95^{60} \approx 0.95\)。

## 主要方法

本頁只涵蓋一種方法：從搜尋空間上的分布獨立取樣，保留最好的試驗。

1. 為每個超參數選擇取樣分布，若效果是乘性的，則使用對數尺度。
2. 獨立抽取 \(n\) 組設定。
3. 以完整預算訓練每組設定，並記錄其驗證分數。
4. 回傳最好的設定。

## 變體

- **準隨機取樣**以低差異序列取代獨立抽樣，使試驗分布得更均勻。
- **搭配提早停止的隨機搜尋**提早停止表現差的試驗，這正是 [Hyperband](hyperband.md) 的想法。
- **帶先驗的隨機搜尋**從依據先前結果而改變的分布中取樣，逐漸接近以模型為基礎的方法。

## 結果與限制

- 在 Bergstra 與 Bengio（2012）的實驗中，當某些超參數影響很小時，隨機搜尋以較少的試驗找到至少與格點一樣好的設定。
- 隨機搜尋不會從先前的試驗中學習，因此會把執行次數花在先前結果已顯示表現不佳的區域。[貝氏最佳化](bayesian-optimisation.md)等以模型為基礎的方法會利用這些資訊。
- 其效果取決於取樣分布，若尺度選擇不當（例如學習率採用線性尺度），可能浪費大部分預算。

## 應用

- **深度網路的基準調校**，在可負擔數十到數百次執行的情況下。
- **大規模平行掃描**，試驗之間的獨立性使協調變得不必要。
- **參考基準**，當新的搜尋方法聲稱比它更有效率時。

## 開放問題

- 當有效維度事先未知時，需要多少次試驗才足夠？
- 能否在沒有目標函數模型的情況下，自動選出取樣分布？

## 與其他頁面的連結

- 上層主題：[超參數最佳化](index.md)
- 窮舉的替代方案：[格點搜尋](grid-search.md)
- 以模型為基礎的替代方案：[貝氏最佳化](bayesian-optimisation.md)

## 參考文獻

### 奠基性論文

- Bergstra, J. & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13, 281–305. https://jmlr.org/papers/v13/bergstra12a.html — 顯示當只有少數超參數重要時，隨機取樣設定優於格點搜尋。
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). Practical Bayesian Optimization of Machine Learning Algorithms. In *NeurIPS 2012*. arXiv:1206.2944. https://arxiv.org/abs/1206.2944 — 利用試驗歷史的以模型為基礎調校，這是隨機搜尋所沒有的。
- Li, L. et al. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. *Journal of Machine Learning Research* 18(185). arXiv:1603.06560. https://arxiv.org/abs/1603.06560 — 以隨機取樣作為候選來源，並在其間分配預算。

### 綜述與教科書

- Feurer, M. & Hutter, F. (2019). Hyperparameter Optimization. In *Automated Machine Learning*, Springer, 3–33. https://doi.org/10.1007/978-3-030-05318-5_1 — 比較隨機搜尋與其他調校方法的章節。
- Shahriari, B. et al. (2016). Taking the Human Out of the Loop: A Review of Bayesian Optimization. *Proceedings of the IEEE* 104(1), 148–175. https://doi.org/10.1109/JPROC.2015.2494218 — 把隨機搜尋定位為以模型為基礎方法之基準的綜述。
- Hutter, F., Kotthoff, L. & Vanschoren, J. (eds.) (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer. https://doi.org/10.1007/978-3-030-05318-5 — 含超參數搜尋（包括隨機搜尋）的書籍章節。
