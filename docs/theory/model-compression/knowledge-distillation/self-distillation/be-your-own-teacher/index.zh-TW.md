---
translation_reviewed: 2026-10-28
---

# 做你自己的老師

做你自己的老師（Be Your Own Teacher）是一種自我蒸餾方法，在一次訓練中改進單一網路。輔助分類器被加在淺層，每一個都被訓練去匹配最深的分類器，使知識在網路內部向下流動。Zhang 等人報告，平均準確度比基準高出 2.65%。它是一種[自我蒸餾](../index.zh-TW.md)方法，不需要另外執行教師的訓練。

## 問題

以分開的教師與學生訓練來做自我蒸餾很昂貴。單一網路應該能在一次訓練中自我改進。

## 核心想法

在網路的淺層加上輔助分類器，並訓練每個分類器同時匹配標籤與最深分類器的輸出。最深的分類器對它下方的各層而言，就是教師。

## 公式或演算法

損失加總所有分類器與標籤的交叉熵，再加上一個蒸餾項，把每個淺層分類器拉向最深的分類器。推論時會移除輔助分類器，因此推論成本不變。

## 結果

摘要報告平均準確度提升 2.65%，從 ResNeXt 的 0.61% 到 VGG19 的 4.07%。

## 限制

此方法在訓練時增加分類器與訓練項。改善是針對卷積網路的影像分類；論文未測試語言模型。

## 開放問題與相關變體

- **架構。** 同樣的向下流動是否對 Transformer 有效（其各層差異較大），尚待確認。
- **相關：** [重生網路](../born-again-networks/index.zh-TW.md)以一次完整的額外訓練達成相似的效果。

## 相關連結

此方法是深層監督的一種，中間層各自接收自己的訓練訊號。深層分類器向淺層分類器的向下流動，本身也是[深度學習理論](../../../../../theory/deep-learning/index.zh-TW.md)的問題。

## 參考文獻

### 開創性論文

- Zhang, L., et al. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — 以輔助分類器進行深層自我蒸餾，平均準確度提升 2.65%。
- Furlanello, T., et al. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — 完整世代的替代方案，是在單一訓練中自我教學的對照。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 淺層分類器所使用的蒸餾損失。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述自我蒸餾的變體。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — 中間層提示，是深層自我教學在特徵層級的對應。
