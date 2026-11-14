---
related:
  - theory/paradigms/meta-learning
  - theory/paradigms/supervised/instance-based-and-probabilistic
  - theory/evaluation/benchmarks/few-shot
tags:
  - meta-learning
  - few-shot learning
  - metric learning
  - attention
aliases:
  - Matching networks
  - 匹配網路
  - One-shot matching
translation_reviewed: 2026-11-01
---

# 匹配網路

匹配網路（Vinyals 等人，2016）透過對一組小型標註支持集做注意力，來分類新樣本。模型在模擬測試情境的訓練回合（episode）上訓練，因此學會把新樣本與已標註的樣本配對，而不需要在新類別上微調。類似方法的家族見[基於度量的少樣本學習](index.md)頁面。

## 問題

單樣本學習是指只用一個標註樣本來學習一個新類別。以梯度下降訓練的深度網路通常需要多得多的每類標註，而且若不重新訓練，就無法快速吸收新類別。非參數方法（如最近鄰）可以立即加入新樣本，但它們依賴固定的距離，在原始影像上效果不佳。論文探討如何結合兩者：學習得到的嵌入，加上一個能在測試時使用新標註樣本的規則。

## 核心想法

模型把標籤預測為支持集 \(S = \{(x_i, y_i)\}_{i=1}^{k}\) 標籤的加權投票。每個支持樣本的權重是它與查詢相似度的 softmax，因此預測是注意力加權的 one-hot 標籤平均。這也是論文將此規則與核密度估計及最近鄰相連的原因。

訓練採用回合制。每個回合從任務分布中抽出一個標籤集 \(L\)，再從 \(L\) 中的類別抽出支持集 \(S\) 與批次 \(B\)。網路被訓練為在給定 \(S\) 的情況下預測 \(B\) 中的標籤。論文所宣稱的原則是「測試與訓練條件必須一致」：在每類樣本數少的回合上訓練的模型，會在相同形式的回合上評估。

## 演算法

設 \(c\) 為餘弦相似度，\(f\) 為查詢的嵌入，\(g\) 為支持樣本的嵌入（兩者可以相同），預測為

\[
\hat y = \sum_{i=1}^{k} a(\hat x, x_i)\, y_i, \qquad a(\hat x, x_i) = \frac{\exp\big(c(f(\hat x), g(x_i))\big)}{\sum_{j=1}^{k} \exp\big(c(f(\hat x), g(x_j))\big)}
\]

論文也引入了**完整上下文嵌入**。在基本模型中，每個支持樣本是單獨嵌入的；完整上下文版本則讓嵌入依賴整個支持集。雙向 LSTM 在支持集上計算 \(g(x_i, S)\)，而對 \(g(S)\) 做讀取注意力的 LSTM 則在固定的處理步數中計算 \(f(\hat x, S)\)。

## 結果

論文在 Omniglot 與 mini-ImageNet 上評估。以下的表格使用論文中餘弦匹配的列。完整上下文變體在 1-shot 的 mini-ImageNet 上提升 3.0 個百分點，在 5-shot 上提升 0.8 個百分點；論文指出在 Omniglot 上沒有差異。

**Omniglot**（表 1，準確率，未微調）：

| 設定 | 5-way 1-shot | 5-way 5-shot | 20-way 1-shot | 20-way 5-shot |
|---|---|---|---|---|
| 餘弦匹配 | 98.1% | 98.9% | 93.8% | 98.5% |

**mini-ImageNet，5-way**（表 2，準確率）：

| 設定 | 1-shot | 5-shot |
|---|---|---|
| 餘弦匹配，未微調 | 41.2% | 56.2% |
| 餘弦匹配，加入完整上下文嵌入 | 44.2% | 57.0% |
| 餘弦匹配，完整上下文，並微調 | 46.6% | 60.0% |

這些結果是在 [Omniglot](../../../evaluation/benchmarks/few-shot/omniglot.md) 與 [mini-ImageNet](../../../evaluation/benchmarks/few-shot/mini-imagenet.md) 所描述的基準上取得的。

## 限制

- **成本隨支持集增長。** 論文稱此為模型「明顯的缺點」，因為計算量隨支持集大小增加。作者提到稀疏與基於抽樣的變體可能是解決方法。
- **標籤分布偏差。** 在 ImageNet 犬種的細粒度子任務上，表現下降約 1%。作者將其歸因於以隨機抽樣的標籤集訓練，而非細粒度的標籤集，並表示當標籤分布有明顯偏差時，模型會「受損」。
- **分布偏移。** 當測試任務與訓練任務分布相差很遠時，表現預期會下降，論文在第 2.2 節指出這一點。
- **微調會過擬合。** 在支持集上微調會導致「嚴重的過擬合」，不過作者觀察到仍有增益，因為模型的正則化程度很高。

## 關聯

- 此方法是度量式家族的注意力形式，與以類別均值取代注意力的[原型網路](https://arxiv.org/abs/1703.05175)並列。
- 它所引入的回合式訓練，被其他用於少樣本任務的[元學習](../index.md)方法廣泛採用。
- 它所推廣的最近鄰規則，見監督式學習中的[基於實例與機率的方法](../../supervised/instance-based-and-probabilistic/index.md)。

## 未解問題

- 能否在不損失準確率的前提下，降低完整支持集計算的成本？
- 應如何抽樣回合，使模型不依賴訓練任務的標籤分布？
- 完整上下文嵌入為何在較困難的資料上幫助更大，如論文結果所示？

## 參考文獻

### 奠基論文

- Vinyals, O., Blundell, C., Lillicrap, T., Kavukcuoglu, K. & Wierstra, D. (2016). Matching Networks for One Shot Learning. NeurIPS. [arXiv:1606.04080](https://arxiv.org/abs/1606.04080) — 引入對標註支持集的注意力，並在模擬測試條件的回合上訓練。
- Lake, B. M., Salakhutdinov, R. & Tenenbaum, J. B. (2015). Human-level concept learning through probabilistic program induction. Science, 350, 1332–1338. [DOI 10.1126/science.aab3050](https://doi.org/10.1126/science.aab3050) — 引用來源為匹配網路論文所用的 Omniglot 基準。
- Snell, J., Swersky, K. & Zemel, R. (2017). Prototypical Networks for Few-shot Learning. [arXiv:1703.05175](https://arxiv.org/abs/1703.05175) — 以到類別原型的距離取代注意力規則，是密切相關的度量式方法。
- Santoro, A. 等人（2016）。One-shot Learning with Memory-Augmented Neural Networks. [arXiv:1605.06065](https://arxiv.org/abs/1605.06065) — 以外部記憶進行單樣本預測，是處理同一問題的同期方法。
- Hochreiter, S. & Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9, 1735–1780. [DOI 10.1162/neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735) — 完整上下文嵌入所用的 LSTM 架構。

### 綜述與教科書

- Hospedales, T., Antoniou, A., Micaelli, P. & Storkey, A. (2021). Meta-learning in Neural Networks: A Survey. IEEE TPAMI. [arXiv:2004.05439](https://arxiv.org/abs/2004.05439) — 將匹配網路置於其他元學習家族之中。

### 講座與影片

（本頁未核對）

### 文章與文件

（本頁未核對）
