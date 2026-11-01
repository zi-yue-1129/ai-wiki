---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
  - generalisation
last_reviewed: 2026-11-01
translation_reviewed: 2026-11-01
aliases:
  - ImageNetV2
  - ImageNet V2
  - Do ImageNet Classifiers Generalize to ImageNet?
  - ImageNet 第二版測試集
  - ImageNet 再收集測試集
---

# ImageNetV2

ImageNetV2 是 ImageNet 的新測試集，依照原始的資料蒐集流程重新蒐集而成。Recht et al.（2019）建構它的目的，是檢驗影像分類器在標準 ImageNet 驗證集上達到的準確率，能否延續到以同樣方式蒐集的影像上。他們的答案是：大致可以，但每個模型在新測試集上的分數都較低（Recht et al., 2019）。

## 任務與資料

任務與 [ImageNet](imagenet.md) 相同：為一張照片指派 1,000 個標籤之一。新測試集有 10,000 張影像，每類十張。作者也為 CIFAR-10 建構了 2,000 張影像的新測試集（Recht et al., 2019）。

Recht et al. 遵循原始的資料建立流程。他們每類從一個龐大的候選影像池中抽取十張，而影像的選取取決於每張候選影像在原始流程中被選中的頻率。三種抽樣策略產生三個測試集，它們的差異在於與原始選取頻率的貼近程度（Recht et al., 2019）。

## 協定與指標

指標仍是 top-1 準確率，與原始基準相同。改變的是測試集。作者估計每張候選影像在原始流程中被選中的頻率，並以此決定保留哪些影像。三個測試集如下：

- **MatchedFrequency。** 抽樣使每個類別的選取頻率與原始分布相符。平均選取頻率為 0.73，平均 top-1 變化為 −11.8%。
- **Threshold 0.7。** 只保留選取頻率至少為 0.7 的影像。平均頻率為 0.85，平均 top-1 變化為 −3.2%。
- **TopImages。** 每類保留選取頻率最高的十張影像。平均頻率為 0.93，平均 top-1 變化為 +2.1%。

主要比較使用 MatchedFrequency 測試集，因為它最接近原始驗證集（Recht et al., 2019）。

## 它能說明什麼

研究中的模型在新測試集上的分數都比原始測試集低。表現最好的 PNASNet 從 82.9% 降到 72.2%，排名由第一降到第三。其他代表性模型的降幅相近：ResNet-152 從 78.3% 降到 67.0%，AlexNet 從 56.5% 降到 44.0%（Recht et al., 2019）。

比降幅大小更重要的有兩點。第一，作者發現降幅並非來自適應性，也就是反覆使用舊測試集來挑選模型。第二，在原始測試集上的準確率提升，會延續到新測試集上。作者認為，剩餘的降幅反映的是模型對稍微困難一些的影像泛化能力有限（Recht et al., 2019）。

TopImages 的結果也有參考價值。保留選取頻率最高的影像會讓測試集變得較容易，準確率因此略為上升。因此，測試集的難度取決於抽取哪些影像，而不只取決於類別本身。

## 相關連結

- [ImageNet](imagenet.md) 是 ImageNetV2 所複製的基準。兩者應在相同的指標與相同的訓練資料下比較。
- [基準總覽](../index.md) 列出其他視覺與語言基準，測試集擬合的問題也在那裡討論。
- 對合成損壞的穩健性是另一種測試。Hendrycks and Dietterich（2019）為此提出 ImageNet-C，並報告從 AlexNet 到 ResNet，相對損壞穩健性變化不大。
- Taori et al.（2020）在 204 個 ImageNet 模型上研究自然分布偏移，發現對合成偏移的穩健性很難轉移到自然偏移上。
- [準確率](../../metrics/classification/accuracy.md) 是這些測試集共同使用的指標。

## 應用

ImageNetV2 可以作為對分類器 ImageNet 分數的第二道檢驗。若模型在原始驗證集上分數很好，但在新測試集上表現不佳，它可能是擬合了蒐集流程，而非視覺概念本身。

## 未解問題

- 原始與新測試集之間的差距，有多少反映影像難度，又有多少反映其他選取方式的差異。作者對較困難影像的解釋只是一個假設，並未直接測量。
- 分布內準確率與分布外準確率之間的相關性，是否在所有新測試集上都成立。Miller et al.（2021）在許多偏移上發現強相關，但也報告了相關較弱的情況。
- 如何建構新測試集，使其在許多模型比較後仍然具有代表性。

## 參考文獻

### 開創性論文

- Recht, B., Roelofs, R., Schmidt, L. & Shankar, V. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — 為 CIFAR-10 與 ImageNet 重新蒐集測試集，並測量許多模型造成的準確率下降。
- Deng, J. et al. (2009). *ImageNet: A large-scale hierarchical image database*. CVPR, pp. 248–255. https://doi.org/10.1109/CVPR.2009.5206848 — ImageNetV2 所複製的原始資料庫。
- Russakovsky, O. et al. (2014). *ImageNet Large Scale Visual Recognition Challenge*. arXiv. https://arxiv.org/abs/1409.0575 — 描述建立在此資料庫上的競賽，以及前幾年的經驗。

### 綜述與基準

- Hendrycks, D. & Dietterich, T. (2019). *Benchmarking Neural Network Robustness to Common Corruptions and Perturbations*. arXiv. https://arxiv.org/abs/1903.12261 — ImageNet-C，一個以合成損壞測量穩健性的基準。
- Taori, R. et al. (2020). *Measuring Robustness to Natural Distribution Shifts in Image Classification*. arXiv. https://arxiv.org/abs/2007.00644 — 在 213 種自然測試條件下評估 204 個 ImageNet 模型，發現合成穩健性很少能轉移。
- Miller, J. et al. (2021). *Accuracy on the Line: On the Strong Correlation Between Out-of-Distribution and In-Distribution Generalization*. arXiv. https://arxiv.org/abs/2107.04649 — 在許多模型與偏移上，顯示分布內與分布外準確率之間的強相關，包括 ImageNet 的變體。
