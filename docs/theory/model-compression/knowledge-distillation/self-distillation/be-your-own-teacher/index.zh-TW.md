---
translation_reviewed: 2026-10-28
---

# 自己當老師

Be Your Own Teacher 是一種自我蒸餾方法，在單次訓練中改善同一個網路。網路被切分成若干區段，每段接一個分類器，最深分類器的知識再向較淺的分類器傳遞。Zhang 等人報告平均準確率比基線高 2.65%。它是一種[自我蒸餾](../index.zh-TW.md)方法，不需要另外訓練教師。

## 問題

以獨立的教師與學生網路進行知識蒸餾成本很高，因為必須先訓練大型教師。單一網路應該能在一次訓練中自我改善，同時維持相同的推論成本。

## 核心想法

把卷積網路切成數段，每段都有一個瓶頸層與一個分類器。每個淺層分類器同時以真實標籤、最深分類器的輸出，以及最深區段的特徵圖訓練。最深分類器充當其下所有層的教師，它本身只以標籤訓練。因此訓練時，知識會在網路內向下流動。

## 公式或演算法

總損失是所有 \(C\) 個分類器的損失總和：

\[
\mathcal{L} = \sum_{i=1}^{C} \Big( (1-\alpha)\,\mathrm{CE}(q^i, y) + \alpha\,\mathrm{KL}(q^i \,\Vert\, q^C) + \lambda\,\Vert F_i - F_C \Vert_2^2 \Big)
\]

其中 \(q^i\) 是第 \(i\) 個分類器的 softmax 輸出，\(q^C\) 是最深分類器的輸出，\(y\) 是標籤，\(F_i\) 與 \(F_C\) 分別是第 \(i\) 段與最深段的特徵圖。第一項是標籤損失，第二項是蒸餾項，第三項是特徵提示項，使淺層特徵圖與最深層對齊。論文將最深分類器的 \(\alpha\) 與 \(\lambda\) 設為零。softmax 溫度通常設為 1。淺層分類器可用於深度可調的推論，作者提議用於資源受限的裝置。

## 結果

論文的主要表格在 CIFAR-100 上比較基線與自我蒸餾，數字為最深分類器的準確率：

| 網路 | 基線 (%) | 自我蒸餾 (%) |
|---|---|---|
| VGG19 (BN) | 64.47 | 67.73 |
| ResNet18 | 77.09 | 78.64 |
| ResNet50 | 77.68 | 80.56 |
| ResNet101 | 77.98 | 81.23 |
| ResNet152 | 79.21 | 81.61 |
| ResNeXt29-8 | 81.29 | 81.51 |

摘要報告平均準確率提升 2.65%，從 ResNeXt 的 0.61% 到 VGG19 的 4.07%。表格也列出較淺分類器與分類器集成的結果，本頁不重複。

## 限制

此方法增加了分類器與訓練項，因此訓練成本高於基線，雖然推論成本不變。論文評估的是卷積網路的影像分類。同樣的向下流動是否對層間功能差異較大的 transformer 有效，論文未測試。損失權重 \(\alpha\) 與 \(\lambda\) 論文未固定，必須自行調校。

## 未解問題與相關變體

- **架構。** 同樣的向下流動是否對 transformer 有效，仍是未解問題。
- **完整重訓的替代方案。** [Born-again networks](../born-again-networks/index.zh-TW.md) 透過訓練同架構的完整新一代網路達到類似效果，但訓練成本高得多。
- **特徵目標。** 特徵提示項沿用 [FitNets](../../feature-based/fitnets/index.zh-TW.md) 的想法。

## 與其他主題的連結

此方法是一種深度監督，中間層會接收自己的訓練訊號。從深層分類器向淺層的向下流動，也是[深度學習理論](../../../../../theory/deep-learning/index.zh-TW.md)的問題。

## 參考文獻

### 奠基性論文

- Zhang, L., Song, J., Gao, A., Chen, J., Bao, C., Ma, K. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — 以輔助分類器進行深層自我蒸餾；平均準確率提升 2.65%，從 0.61%（ResNeXt）到 4.07%（VGG19）。
- Furlanello, T., Lipton, Z. C., Tschannen, M., Itti, L., Anandkumar, A. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — 與教師架構相同、經蒸餾訓練的學生，可以超越那些教師。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 淺層分類器所用的蒸餾目標。

### 綜述與教科書

- Gou, J., Yu, B., Maybank, S. J., Tao, D. (2021). *Knowledge Distillation: A Survey*. arXiv:2006.05525. https://arxiv.org/abs/2006.05525 — 蒸餾方法綜述，包括自我蒸餾；arXiv 頁面列出已發表版本為 https://doi.org/10.1007/s11263-021-01453-z。

### 講座與影片

（本頁未檢核任何項目）

### 文章與文件

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 中間層提示，是深層自我教學在特徵層級的對應方法。
