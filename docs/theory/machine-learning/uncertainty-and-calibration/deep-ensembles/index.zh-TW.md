---
translation_reviewed: 2026-10-28
---

# 深度集成

深度集成是從不同的隨機起點訓練同一神經網路的數個副本，然後平均它們的預測。副本之間的分散程度，是認知不確定性的一種實用估計。Lakshminarayanan、Pritzel 與 Blundell（2017）把此方法提出，作為[貝氏神經網路](../index.md)的簡單替代方案。

## 概述

深度網路是強大的預測器，但單一網路無法可靠地告訴我們應該信任某個輸出到什麼程度。貝氏神經網路提供了有原則的答案，但需要改動訓練程序，而且成本高昂。Lakshminarayanan 等人（2017）提出了另一條路。他們的摘要描述一種容易實作、可平行化、幾乎不需要超參數調校，並能產生高品質預測不確定性的方法。其想法是集成，這是降低變異的經典方法，應用於同時回報自身雜訊的網路上。

## 關鍵概念

- **集成成員。** 一個網路，具有自己的隨機初始化，通常也有自己的訓練資料順序。
- **適當評分規則。** 每個成員都以某種損失訓練，例如負對數概似，此損失會獎勵誠實的機率。
- **多樣性。** 只有當成員在它們不確定的輸入上意見不一時，集成才有幫助。犯同樣錯誤的成員，貢獻很小。

## 運作方式

對分類而言，每個成員 \(m\) 輸出一個機率 \(p_m(y \mid x)\)。集成的預測為平均：

\[
p(y \mid x) = \frac{1}{M}\sum_{m=1}^{M} p_m(y \mid x).
\]

對迴歸而言，每個成員輸出平均 \(\mu_m(x)\) 與變異數 \(\sigma^2_m(x)\)。把各成員視為等權重的高斯混合，集成的平均與變異數為

\[
\mu_*(x) = \frac{1}{M}\sum_{m=1}^{M}\mu_m(x), \qquad
\sigma^2_*(x) = \frac{1}{M}\sum_{m=1}^{M}\big(\sigma^2_m(x) + \mu_m(x)^2\big) - \mu_*(x)^2.
\]

每個成員最小化負對數概似。對高斯輸出而言，在忽略常數項後為 \(\frac{(y-\mu)^2}{2\sigma^2} + \tfrac{1}{2}\log \sigma^2\)。

流程如下。

1. 選定一種架構，以及輸出的適當評分規則。
2. 獨立訓練 \(M\) 個副本，各自使用不同的隨機初始化與資料順序。
3. 對新輸入，執行全部 \(M\) 個成員，並以上述公式合併其輸出。
4. 以分散程度（而不只是平均值）作為不確定性。

## 結果

摘要指出，此方法在分類與迴歸基準上能產生校準良好的不確定性估計，且其品質等於或優於近似貝氏神經網路。對來自未見分布的測試範例，此方法表現出較高的不確定性，這正是模型超出其能力範圍時應有的行為。作者也回報，此方法可擴展至 ImageNet。確切數字見原論文，本頁未重新執行。

## 限制

- **成本。** 訓練與執行 \(M\) 個網路會使所需的運算與記憶體成倍增加，不過各副本可以平行執行。
- **多樣性有限。** 只因隨機種子不同的成員，可能收斂到相似的解，從而降低平均的效益。
- **不是精確的後驗。** 集成是貝氏平均的近似。Wilson 與 Izmailov（2020）主張它有效，但它並不等同於對後驗積分。
- **偏移問題未解。** Ovadia 等人（2019）發現，在資料集偏移下，以模型邊緣化的方法表現出出奇強的結果；但當輸入遠離訓練資料時，準確率與校準仍會惡化。

## 未解問題

- 如何以低成本增加多樣性，例如透過不同的架構、資料子集或訓練目標？
- 集成能否壓縮成單一網路而不損失其校準，例如透過[知識蒸餾](../../../model-compression/knowledge-distillation/index.md)？
- 當集成很大，但其成員系統性地對同一錯誤答案意見一致時，應該相信哪些成員？

## 相關連結

此方法延伸了古典學習中熟悉的想法。[樹與集成](../../../paradigms/supervised/trees-and-ensembles/index.md)結合許多弱模型以降低變異，而深度集成把同樣的平均套用到輸出同時帶有不確定性的網路上。[機率方法](../../../probabilistic/index.md)頁面描述了集成所近似的貝氏觀點，而 [MC 丟棄法](../mc-dropout/index.md)則是只使用單一網路的較便宜近似。大腦與心智的連結只是類比：人們依可靠度權衡多個有雜訊的線索（Ernst 與 Banks，2002），但這並不能證明大腦運行的是集成。

## 參考文獻

### 開創性論文

- Lakshminarayanan, B., Pritzel, A. & Blundell, C. (2017). Simple and scalable predictive uncertainty estimation using deep ensembles. NeurIPS. https://arxiv.org/abs/1612.01474 — 提出以適當評分規則訓練一組網路的集成，作為貝氏神經網路之外簡單且可擴展的替代方案。
- Ernst, M. O. & Banks, M. S. (2002). Humans integrate visual and haptic information in a statistically optimal fashion. *Nature*. https://doi.org/10.1038/415429a — 顯示人們依感官線索的可靠度來加權，即相關連結一節所用的類比。

### 綜述與教科書

- Wilson, A. G. & Izmailov, P. (2020). Bayesian deep learning and a probabilistic perspective of generalization. NeurIPS. https://arxiv.org/abs/2002.08791 — 主張深度集成提供貝氏邊緣化的有效近似。
- Gawlikowski, J. et al. (2021). A survey of uncertainty in deep neural networks. arXiv. https://arxiv.org/abs/2107.03342 — 綜述深度網路的不確定性來源與估計方法。
- Hüllermeier, E. & Waegeman, W. (2021). Aleatoric and epistemic uncertainty in machine learning: an introduction to concepts and methods. *Machine Learning*. https://arxiv.org/abs/1910.09457 — 介紹集成分散程度所要衡量的偶然與認知不確定性之區分。

### 文章與文件

- Ovadia, Y. et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. NeurIPS. https://arxiv.org/abs/1906.02530 — 基準測試，顯示以模型邊緣化的方法在資料集偏移下有出奇強的結果。
