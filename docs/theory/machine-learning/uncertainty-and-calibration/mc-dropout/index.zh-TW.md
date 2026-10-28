---
translation_reviewed: 2026-10-28
---

# MC 丟棄法

MC 丟棄法在已訓練網路做預測時仍保持丟棄法啟用。它執行數次隨機前向傳播，並以其分散程度估計模型的不確定性。Gal 與 Ghahramani（2016）指出，此程序具有貝氏的詮釋。它是[不確定性與校準](../index.md)頁面中比較的方法之一。

## 概述

丟棄法在訓練時隨機把一部分網路單元設為零，有助於減少過度擬合。測試時通常會關閉它，使網路只給出一個確定的答案。Gal 與 Ghahramani 的摘要描述了對同一網路的另一種用法。他們把深度網路中的丟棄法訓練，視為深度高斯過程中的近似貝氏推論，而這個結果提供了以丟棄法網路建模不確定性的工具。它適用於既有的丟棄法網路，作者也主張它不會犧牲計算複雜度或測試準確率。

## 關鍵概念

- **丟棄遮罩。** 每次前向傳播時抽取的一個由 0 與 1 組成的隨機向量，決定哪些單元啟用。
- **隨機前向傳播。** 以一個抽樣遮罩所做的預測。以不同遮罩重複進行，就會得到同一輸入的預測分布。
- **近似後驗。** 論文把每一組抽樣遮罩，詮釋為網路權重上近似後驗的一個樣本，因此分散程度可被讀為模型的不確定性。
- **認知不確定性。** 此方法所針對的不確定性部分。資料中的雜訊，即偶然部分，除非另行建模，否則不會被捕捉。

## 運作方式

令 \(f(x; \hat{W}_t)\) 為抽樣丟棄遮罩時，網路對輸入 \(x\) 的輸出，並令 \(T\) 為執行次數。預測平均與樣本變異數為

\[
\hat{\mu}(x) = \frac{1}{T}\sum_{t=1}^{T} f(x; \hat{W}_t), \qquad
\widehat{\operatorname{Var}}(x) = \frac{1}{T}\sum_{t=1}^{T}\big(f(x; \hat{W}_t) - \hat{\mu}(x)\big)^2.
\]

對迴歸而言，論文在變異數中加入觀測雜訊項。對分類而言，對抽樣得到的機率取平均，而平均後分布的熵是常用的不確定性分數。

1. 以在所用各層加上丟棄法的一般網路進行訓練。
2. 對新輸入，保持丟棄法啟用，並抽取 \(T\) 個遮罩。
3. 對每個遮罩執行一次前向傳播，得到 \(T\) 個預測。
4. 以平均作為預測，以分散程度作為不確定性。

## 結果

摘要回報，在迴歸與分類任務上，相對於現有最先進的方法，預測對數概似與 RMSE 有相當大的改進，並以 MNIST 作為例子。摘要也提到，丟棄法的不確定性被用於深度強化學習。此處為定性摘要。確切數字見原論文，本頁未重新執行。

## 限制

- **粗糙的近似。** 近似後驗的形式受限，因此分散程度只是一種近似，其品質取決於架構，以及丟棄法的套用方式。
- **丟棄率。** 丟棄率是超參數，它同時改變準確率與不確定性估計。理論對於如何選擇它的指引有限。
- **推論時的成本。** 每次預測都需要 \(T\) 次前向傳播，對小型網路來說便宜，對大型網路來說昂貴。
- **只有部分的圖像。** 此方法捕捉認知不確定性。Kendall 與 Gal（2017）另外加上一個單獨學習的偶然項，以同時取得兩者。

## 未解問題

- 應如何選擇丟棄率與其位置，才能使不確定性（而不只是準確率）良好？
- 基於丟棄法的不確定性，在遠離訓練資料的輸入上是否仍然可靠？Ovadia 等人（2019）等資料集偏移下的基準測試，是常用的檢驗方式。
- MC 丟棄法與真正的後驗相比如何？又與 Wilson 與 Izmailov（2020）的集成觀點相比如何？

## 相關連結

MC 丟棄法是[機率方法](../../../paradigms/probabilistic/index.md)頁面所描述之變分途徑的一個實際例子，也是[深度集成](../deep-ensembles/index.md)的單一網路對應方法。Knill 與 Pouget（2004）主張，大腦可以被描述為執行近似的貝氏推論。以抽樣為基礎的推論觀點，是該想法的一種建模方式，但 MC 丟棄法是工程上的近似，並非神經雜訊的模型。

## 參考文獻

### 開創性論文

- Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. ICML. https://arxiv.org/abs/1506.02142 — 顯示丟棄法訓練可被讀為近似的貝氏推論，並給出從已訓練丟棄法網路估計不確定性的方法。
- Kendall, A. & Gal, Y. (2017). What uncertainties do we need in Bayesian deep learning for computer vision? NeurIPS. https://arxiv.org/abs/1703.04977 — 在視覺任務中，結合用於認知不確定性的貝氏丟棄法，以及一個學到的偶然項。
- Blundell, C., Cornebise, J., Kavukcuoglu, K. & Wierstra, D. (2015). Weight uncertainty in neural networks. ICML. https://arxiv.org/abs/1505.05424 — Bayes by Backprop，是直接學習權重分布的變分替代方案。
- Knill, D. C. & Pouget, A. (2004). The Bayesian brain: the role of uncertainty in neural coding and computation. *Trends in Neurosciences*. https://doi.org/10.1016/j.tins.2004.10.007 — 回顧文章，主張大腦表徵不確定性，並進行近似的貝氏計算。

### 綜述與教科書

- Wilson, A. G. & Izmailov, P. (2020). Bayesian deep learning and a probabilistic perspective of generalization. NeurIPS. https://arxiv.org/abs/2002.08791 — 討論深度網路中的貝氏邊緣化，以及它為何能改善校準。
- Gawlikowski, J. et al. (2021). A survey of uncertainty in deep neural networks. arXiv. https://arxiv.org/abs/2107.03342 — 綜述深度網路的不確定性估計方法。

### 文章與文件

- Ovadia, Y. et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. NeurIPS. https://arxiv.org/abs/1906.02530 — 大規模基準測試，在資料集偏移下檢驗預測不確定性方法，包括近似的貝氏方法。
