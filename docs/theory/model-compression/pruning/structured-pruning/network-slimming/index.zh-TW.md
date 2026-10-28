---
translation_reviewed: 2026-10-28
---

# 網路瘦身

網路瘦身以批次正規化的縮放因子作為重要性分數，來選擇要移除的通道。訓練時加入稀疏化懲罰，使許多縮放因子趨近於零；縮放因子小的通道隨後被移除，再微調網路。它是[結構化剪枝](../index.zh-TW.md)方法，不需要另外的評分過程。

## 問題

選擇要移除哪些通道，需要一個計算成本低、又能反映訓練後各通道重要性的分數。

## 核心想法

在訓練時對批次正規化的縮放因子加上 \(\ell_1\) 懲罰。許多因子會變小，表示它們的通道不重要。移除這些通道，再微調其餘部分。

## 公式或演算法

訓練損失包含對批次正規化縮放參數 \(\gamma\) 的懲罰 \(\lambda \sum_\gamma |\gamma|\)。訓練後，縮放因子 \(\gamma\) 小的通道被移除，剩餘網路再微調以恢復準確度。

## 結果

對 VGGNet，摘要報告多次通過版本的方法能使模型大小減少 20 倍，計算操作減少 5 倍。

## 限制

懲罰係數需要人工設定。方法依賴架構中存在批次正規化，因此對不使用批次正規化的模型有限制。

## 開放問題與相關變體

- **沒有批次正規化的架構。** 沒有批次正規化時，縮放因子是否仍有意義，是開放問題。
- **相關**：[濾波器剪枝](../filter-pruning/index.zh-TW.md)改用濾波器範數作為分數。

## 相關連結

網路瘦身移除整個通道，因此結果能在 [AI 硬體](../../../../../engineering/hardware/index.zh-TW.md)討論的稠密硬體上執行。它與生物界發育期間消除整條路徑的現象之間的連結，見[神經科學](../../../../../brain-mind/neuroscience/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Liu, Z., 等人 (2017). *Learning Efficient Convolutional Networks through Network Slimming*. arXiv:1708.06519. https://arxiv.org/abs/1708.06519 — 以 \(\ell_1\) 懲罰作用在批次正規化尺度上來選擇通道，使 VGGNet 縮小為 20 倍。
- Li, H., Kadav, A., Durdanovic, I., Samet, H., Graf, H. P. (2016). *Pruning Filters for Efficient ConvNets*. arXiv:1608.08710. https://arxiv.org/abs/1608.08710 — 以濾波器範數作為分數的替代方法。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 通道移除所比較的非結構化基準。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 比較通道層級與權重層級的稀疏度。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 在同一協定下比較結構化與非結構化稀疏。
