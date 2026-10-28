---
related:
  - engineering/evaluation
  - theory/evaluation/protocols/index.md
tags:
  - evaluation
  - protocols
  - statistics
---

# 配對自助法

配對自助法估計兩個方法之間差異的不確定性，方式是對兩個方法共同測試過的範例進行重抽樣。由於兩個方法共享每個範例，重抽樣能保留這種配對，因此得到的差異區間比比較兩個獨立平均值更窄（Efron, 1992）。

## 程序

若測試集有 n 個範例，就記錄每個方法在每個範例上的分數。以放回方式抽出 n 個範例，計算重抽樣上的平均分數差，重複很多次，通常至少 1,000 次。中間 95% 的差異即為區間。若區間不包含零，這個差異就不太可能只是由測試集中恰好出現哪些範例所造成。

## 適用時機

重抽樣的單位必須與資料的相依方式一致。同一對話中的多輪，或同一份文件的多個問題，並非獨立範例，應一起重抽樣。SciPy 的自助法實作提供了一般的重抽樣機制（SciPy contributors）。

## 報告

說明重抽樣次數、重抽樣單位、信賴水準與區間的計算方法，例如百分位法或偏誤校正法。差異應與區間一併報告，而不只是兩個分數。

## 限制

- **只涵蓋測試集的變異。** 自助法捕捉的是測試了哪些範例造成的變異，不包括訓練過程的變異。當主張依賴於此時，應以多個種子重複訓練。
- **樣本小。** 範例很少時，區間本身也不可靠。
- **相依性。** 忽略資料中的分群會使區間過窄。

## 相關

- [評估協定概述](../index.md) 說明為何必須報告不確定性。
- [交叉驗證](cross-validation.md) 從不同切分取得重複估計。

## 參考文獻

### 開創性論文

- Efron, B. (1992). *Bootstrap Methods: Another Look at the Jackknife*. In *Breakthroughs in Statistics*, Vol. 1. Springer. https://doi.org/10.1007/978-1-4612-4380-9_41 — 將自助法介紹為估計不確定性的一般方法，為 1979 年論文的重印。

### 文章與文件

- SciPy contributors. *scipy.stats.bootstrap*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html — 描述自助法信賴區間與配對觀測的重抽樣選項。
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 顯示重新蒐集的測試集能揭露模型對原始蒐集方式的適配程度。

### 補充來源

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 跨情境與指標評估模型，因此差異需要區間。
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及由基準推出廣泛結論的限制。
