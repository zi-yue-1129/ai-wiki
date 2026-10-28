---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/trees-and-ensembles
  - theory/paradigms/supervised/kernel-methods-svm
  - theory/paradigms/supervised/generalization-theory
  - theory/paradigms/supervised/evaluation-and-validation
---

# 隨機森林

隨機森林把許多棵決策樹的預測加以平均。每棵樹都在訓練資料的自助重抽樣（bootstrap）樣本上生成，而且每次分裂時只考慮隨機選取的一部分特徵。Breiman（2001）指出，這份額外的隨機性使樹之間的相關性降低，而森林的誤差取決於單棵樹的強度，以及樹與樹之間的相關程度。家族層級的全貌見[決策樹與集成方法](index.md)頁。

## 概述

裝袋法已經能透過平均在重抽樣資料上訓練的樹來降低不穩定學習器的變異。然而在裝袋樹中，最強的特徵幾乎會在每棵樹的上層被選中，因此各棵樹犯的錯誤相似，平均時能消除的誤差也就有限。Breiman 的隨機森林透過限制每次分裂只能使用隨機的特徵子集，打破了這種相似性。

此方法幾乎不需調參，能處理混合型態的特徵而不必縮放，並且能透過袋外（out-of-bag）樣本，只用訓練資料就給出誤差估計。因此它常被當作表格問題的第一個模型。

## 核心概念

- **自助樣本**：從訓練集中以放回抽樣所得、與訓練集等大的樣本。每棵樹各自使用一份。
- **特徵子集大小 F**：每次分裂時考慮的特徵數。Breiman 嘗試了 F = 1，以及第二種預設值，即小於 \(\log_2 M + 1\) 的最大整數，其中 \(M\) 為輸入數。
- **袋外（OOB）估計**：每個訓練點大約會被約三分之一的自助樣本排除在外，因此沒有見過該點的樹可以對它進行預測。這些預測的誤差提供了泛化誤差的估計，不需要另外的測試集。
- **強度與相關性**：強度衡量每棵樹的準確度，相關性衡量兩棵樹的錯誤彼此相似的程度。Breiman 的分析以這兩個量來表示森林的泛化誤差。

## 運作方式

對於 \(t = 1, \dots, T\)：

1. 從訓練集抽出大小為 \(n\) 的自助樣本。
2. 在該樣本上生成一棵樹。每個節點從隨機選出的 \(F\) 個特徵中，挑選最佳的分裂。

接著組合所有樹。分類時取多數決，迴歸時取平均：

\[
\hat f(x) = \frac{1}{T}\sum_{t=1}^{T} h_t(x)
\]

Breiman 的論文主張，增加樹的數量不會使森林過擬合。由於增加樹不會造成傷害，樹的數量可以設得較大，而不必像提升法那樣為了提前停止而調校。

## 關鍵方法

### Random Forests（Breiman, 2001）

- **問題：** 單棵樹的變異很高，而裝袋樹常因為同一個強特徵主導許多分裂而彼此相關。集成需要的樹既準確又彼此不同。
- **核心想法：** 每個節點只使用隨機的特徵子集進行分裂。子集越小，樹之間的相關性越低，代價是每棵樹的強度會下降。論文直接指出目標：隨機性應該追求低相關性，同時維持合理的強度。
- **公式或演算法：** 上述的自助抽樣加投票程序，以及平均規則。訓練點 \(i\) 的袋外誤差，是僅由那些自助樣本未包含 \(i\) 的樹所組成的平均預測之誤差。
- **結果：** 在第 9 節的合成資料上（1,000 個二元輸入，貝氏誤差為 1.0%），F = 25 的森林測試誤差為 2.8%。F = 1 時為 10.7%。在表 2 的乳癌資料上，隨機特徵森林的測試誤差為 2.7%，AdaBoost 為 3.2%。以上為論文實驗所報告的數值。
- **限制：** 森林比單棵樹更難解釋。分段常數的樹平均後，無法外推到訓練目標範圍之外。記憶體與預測時間隨樹的數量增加。相關的輸入特徵會把重要性分散到許多變數上，削弱變數重要性的衡量。

## 關聯

- 本方法是[梯度提升](gradient-boosting.md)的降變異對應方法；梯度提升則依序擬合樹以降低偏差。
- 表格資料上的其他方法，以及與間隔方法的更廣泛比較，見[支援向量機](../kernel-methods-svm/svm.md)頁。
- 袋外樣本的誤差估計與[評估與驗證](../evaluation-and-validation/index.md)中的方法相連。
- 森林為何能泛化的理論，見[泛化理論](../generalization-theory/index.md)。

## 開放問題

- 為什麼個別的深樹幾乎完全擬合訓練資料，森林卻仍能有如此好的泛化能力？
- 特徵子集大小的預設值在各種任務上是否通用？何時調校它才會有影響？

## 參考文獻

### 開創性論文

- Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324 — 提出每次分裂時的隨機特徵選取、袋外誤差估計，以及強度與相關性的分析。
- Breiman, L. (1996). Bagging predictors. *Machine Learning*, 24, 123–140. https://doi.org/10.1007/BF00058655 — 提出自助聚合（bagging）的平均想法，隨機森林即建立於其上。論文指出，預測方法的不穩定性是關鍵要素。
- Ho, T. K. (1995). Random decision forests. *Proceedings of the Third International Conference on Document Analysis and Recognition (ICDAR 1995)*. https://doi.org/10.1109/ICDAR.1995.598994 — 在隨機特徵子集上生成樹的集成之早期提案。
- Amit, Y. & Geman, D. (1997). Shape quantization and recognition with randomized trees. *Neural Computation*. https://mlanthology.org/neco/1997/amit1997neco-shape — 把隨機化的樹用於形狀辨識，是隨機特徵想法的早期來源。

### 綜述與教科書

- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning*（第 2 版）。Springer。https://doi.org/10.1007/978-0-387-84858-7 — 涵蓋樹、提升與隨機森林的章節；作者提供免費 PDF。
- Scornet, E., Biau, G. & Vert, J.-P. (2015). Consistency of random forests. *Annals of Statistics*。https://doi.org/10.1214/15-AOS1321 — 證明 Breiman 原始森林演算法在加法迴歸模型中的一致性。
