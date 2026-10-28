---
translation_reviewed: 2026-10-28
---

# 網路瘦身

網路瘦身以批次正規化的縮放係數作為重要性分數，來選擇要移除的通道。訓練時加入稀疏懲罰，使許多縮放係數向零收縮。接著移除縮放係數小的通道，再微調網路。它是一種[結構化剪枝](../index.zh-TW.md)方法，不需要另外的評分步驟。

## 問題

要選擇移除哪些通道，需要一個計算成本低、又能反映訓練後各通道重要程度的分數。濾波器範數並不總能反映這一點。

## 核心想法

在訓練時對批次正規化的縮放係數加上 \(\ell_1\) 懲罰。許多係數會變小，代表其通道不重要。移除這些通道，並微調其餘網路。

## 公式或演算法

訓練目標在批次正規化層的縮放參數 \(\gamma\) 上加入稀疏懲罰：

\[
\mathcal{L} = \sum_{(x,y)} \ell\big(f(x, W), y\big) + \lambda \sum_{\gamma \in \Gamma} |\gamma|
\]

其中 \(\lambda\) 用來平衡兩項。論文以驗證集上對 \(10^{-3}\)、\(10^{-4}\) 與 \(10^{-5}\) 的網格搜尋來選擇它；VGGNet 使用 \(10^{-4}\)，ResNet 與 DenseNet 使用 \(10^{-5}\)。\(\ell_1\) 項不平滑，因此論文以次梯度下降訓練。訓練後，以全域門檻剪枝，門檻為所有縮放係數的某個百分位數。在 CIFAR 上的多輪 VGGNet 實驗中，每一層最多只能剪掉一半的通道，以免整層被移除。之後再微調網路。

## 結果

摘要報告，多輪版本的網路瘦身使 VGGNet 的模型大小縮小為 20 倍、計算運算量減少為 5 倍。

## 限制

懲罰係數 \(\lambda\) 必須靠搜尋選擇；若沒有加上每層上限，全域門檻可能會把整層移除。此方法依賴架構中存在批次正規化，因此對不使用批次正規化的模型適用性有限。

## 未解問題與相關變體

- **沒有批次正規化的架構。** 當架構中沒有批次正規化時，縮放係數是否仍有意義，是未解的問題。
- **相關。** [濾波器剪枝](../filter-pruning/index.zh-TW.md)改以濾波器範數作為分數。

## 與其他主題的連結

網路瘦身移除的是整個通道，因此結果能在 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)所討論的稠密硬體上執行。它與生物學中整條通路在發育過程被消除的情況之間的關聯，見[神經科學](../../../../../brain-mind/neuroscience/index.zh-TW.md)。

## 參考文獻

### 奠基性論文

- Liu, Z., Li, J., Shen, Z., Huang, G., Yan, S., Zhang, C. (2017). *Learning Efficient Convolutional Networks through Network Slimming*. arXiv:1708.06519. https://arxiv.org/abs/1708.06519 — 以批次正規化縮放係數的 \(\ell_1\) 懲罰來選擇通道；多輪版本可使 VGGNet 縮小為 20 倍。
- Li, H., Kadav, A., Durdanovic, I., Samet, H., Graf, H. P. (2016). *Pruning Filters for Efficient ConvNets*. arXiv:1608.08710. https://arxiv.org/abs/1608.08710 — 以濾波器範數作為分數的替代方法，對照批次正規化分數。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 通道移除所比較的非結構化基準。

### 綜述與教科書

- Hoefler, T., Alistarh, D., Ben-Nun, T., Dryden, N., Peste, A. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 比較訓練與推論中通道層級與權重層級的稀疏。

### 講座與影片

（本頁未檢核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 在同一套流程下比較結構化與非結構化稀疏。
