---
translation_reviewed: 2026-10-28
---

# 濾波器剪枝

濾波器剪枝移除整個卷積濾波器，連同下一層對應的輸入通道一起移除，使網路變成較小的稠密網路。Li 等人提出依濾波器權重量值排序，並剪除最小的濾波器。它是卷積網路[結構化剪枝](../index.zh-TW.md)的參考方法。

## 問題

剪除個別權重會得到稀疏層，標準卷積函式庫無法加速。需要一種能得到較小稠密層的剪枝方案。

## 核心想法

依各卷積層濾波器權重的量值排序，移除最小的濾波器，再重新訓練。論文也分析哪些層對剪枝較敏感，並對它們少剪。

## 公式或演算法

濾波器 \(j\) 的重要性是其權重的 \(\ell_1\) 範數。移除濾波器 \(j\) 也會移除後續層的輸入通道 \(j\)。網路在每輪移除後重新訓練，各層依其敏感度剪除不同比例。

## 結果

摘要報告，在 CIFAR-10 上，VGG-16 的推論成本最多降低 34%，ResNet-110 最多降低 38%。

## 限制

減少的是計算量，記憶體的節省較少。重要性量度忽略了移除某個濾波器對後續層的影響，只靠重新訓練來補償。

## 開放問題與相關變體

- **較好的分數。** 衡量移除效果損失的分數比範數更準確，但計算成本較高。
- **相關**：[網路瘦身](../network-slimming/index.zh-TW.md)改用批次正規化的縮放因子作為分數。

## 相關連結

濾波器剪枝產生 [AI 加速器](../../../../../engineering/hardware/index.zh-TW.md)擅長處理的稠密矩陣，因此在部署中很常見。與非結構化剪枝的對比，見[同時學習權重與連接](../../learning-weights-and-connections/index.zh-TW.md)。

## 參考文獻

### 開創性論文

- Li, H., Kadav, A., Durdanovic, I., Samet, H., Graf, H. P. (2016). *Pruning Filters for Efficient ConvNets*. arXiv:1608.08710. https://arxiv.org/abs/1608.08710 — 濾波器剪枝，在 CIFAR-10 上使 VGG-16 的推論成本最多降低 34%。
- Liu, Z., 等人 (2017). *Learning Efficient Convolutional Networks through Network Slimming*. arXiv:1708.06519. https://arxiv.org/abs/1708.06519 — 以 \(\ell_1\) 懲罰作用在批次正規化尺度上來選擇通道。
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — 非結構化剪枝，是結構化方法的對照基準。

### 綜述與教科書

- Hoefler, T., 等人 (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — 比較訓練與推論中的結構化與非結構化稀疏。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — 比較稀疏化方法，包括結構化方法。
