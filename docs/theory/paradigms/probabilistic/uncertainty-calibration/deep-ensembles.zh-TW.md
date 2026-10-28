---
translation_reviewed: 2026-10-28
---

# 深度集成

深度集成獨立訓練數個神經網路，每個網路使用不同的隨機初始化與資料順序，然後平均它們的預測分布。成員之間預測的分散程度可以估計不確定性。本頁是[不確定性量化與校準](index.md)的一部分。

## 概述

平均多個模型通常能提升準確率，這是早期神經網路集成研究的既有結論（Hansen 與 Salamon，1990）。Lakshminarayanan 等人（2017）指出，以適當評分規則訓練的網路集成，也能給出校準良好的不確定性，包括對遠離訓練資料的輸入。此方法不需改變架構，實作也簡單。

## 關鍵概念

- **集成成員**：一個擁有自己隨機初始化與訓練順序的網路。
- **混合預測**：各成員預測分布的平均，即 \(p(y\mid x)=\frac{1}{M}\sum_m p_m(y\mid x)\)。
- **分歧**：成員之間的差異，在不熟悉的資料上通常較大。
- **適當評分規則**：負對數概似，它使每個成員學會回報校準後的機率。

## 運作方式

在相同資料上訓練 \(M\) 個網路，各自使用不同的隨機種子。對新輸入，平均它們預測的分布。這個平均就是集成的預測，其熵或成員之間的分歧可作為不確定性的度量。Lakshminarayanan 等人（2017）還加入對抗訓練以鼓勵平滑性，並在迴歸中讓每個成員同時輸出平均值與變異數。

Fort、Hu 與 Lakshminarayanan（2019）認為，集成成員的多樣性來自它們位於損失地形的不同盆地中，這也解釋了為何獨立訓練的網路比同一次訓練的網路更容易分歧。

## 變體

- **快照集成**從同一次訓練的不同時點收集模型，成本較低，但多樣性較少。
- **隨機化集成**在各成員之間改變資料順序、資料增強或架構。
- **貝氏風格的集成**把平均與先驗或近似後驗樣本結合，使此方法與貝氏推論相連（Gal 與 Ghahramani，2016）。

## 結果與限制

- 集成通常同時改善準確率與校準，並且在各種任務中都穩健，因此是強勁的基準。
- 無論訓練或推論，成本都隨成員數線性增加。
- 成員可能過於相似，因此用來估計不確定性的多樣性可能比預期小。
- 集成並不是參數上的真正後驗。其不確定性是經驗性的估計，沒有一般性的保證。

## 應用

- **影像分類與迴歸**：在準確率與校準信心上的強勁基準（Lakshminarayanan 等人，2017）。
- **分布外偵測**：標記成員之間意見分歧的輸入。
- **安全關鍵的預測**：以分歧決定何時交由人工判斷。

## 開放問題

- 在固定的計算預算下，需要多少成員、多大的多樣性，才能得到好的不確定性。
- 對於訓練每個成員都很昂貴的超大型模型，集成能否提供可靠的不確定性。

## 參考文獻

### 奠基性論文

- Lakshminarayanan, B., Pritzel, A. & Blundell, C. (2017). Simple and scalable predictive uncertainty estimation using deep ensembles. In *Advances in Neural Information Processing Systems* 30. https://proceedings.neurips.cc/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html — 提出以深度集成估計預測不確定性。
- Hansen, L. K. & Salamon, P. (1990). Neural network ensembles. *IEEE Transactions on Pattern Analysis and Machine Intelligence* 12(10), 993–1001. https://doi.org/10.1109/34.58871 — 早期分析，顯示平均神經網路能改善泛化。
- Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/gal16.html — 把以 dropout 訓練的網路集成與近似貝氏推論連結起來。

### 綜述與教科書

- Fort, S., Hu, H. & Lakshminarayanan, B. (2019). Deep ensembles: a loss landscape perspective. arXiv:1912.02757. https://arxiv.org/abs/1912.02757 — 解釋獨立訓練的成員為何分歧，以及這如何影響不確定性。
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70. https://proceedings.mlr.press/v70/guo17a.html — 比較集成與事後校準。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋集成與貝氏模型平均。
