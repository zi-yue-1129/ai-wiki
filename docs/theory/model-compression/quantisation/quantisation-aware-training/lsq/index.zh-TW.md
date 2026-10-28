---
translation_reviewed: 2026-10-28
---

# 可學習步長量化（LSQ）

可學習步長量化（LSQ）是一種量化感知訓練方法，把量化器的步長當作可訓練參數，與網路權重一起以梯度下降學習。它是[量化感知訓練](../index.zh-TW.md)中的一種變體，在影像分類的低位元下能達到全精度準確度。

## 問題

與損失無關的固定步長規則，例如依張量統計量設定步長，沒有針對損失調整。在 2 到 4 位元時，步長的選擇對準確度影響很大，因此在 8 位元有效的規則，在 3 位元時可能會嚴重失效。

## 核心想法

把每個量化器的步長當作參數，並像權重一樣依損失更新。對步長的梯度透過捨入函數、以直通近似取得，因此步長會移動到該位元寬度下損失最低的位置。

## 公式或演算法

量化值為 \(\hat{x} = s \cdot \operatorname{round}(\operatorname{clip}(x/s, -Q_n, Q_p))\)，其中 \(s\) 是學習得到的步長，\(Q_n\)、\(Q_p\) 依位元寬度設定整數範圍。對 \(s\) 的梯度以直通估計器穿過捨入運算取得。論文以 \(g = 1/\sqrt{N Q_p}\) 縮放此梯度，其中 \(N\) 為該層權重（或特徵）的數量，使步長相對於權重以合理的速度學習。

## 結果

摘要表示，此方法在 ImageNet 上對量化到 2、3、4 位元的模型達到迄今最高準確度，並且 3 位元模型能達到全精度基準的準確度。

## 限制

訓練成本即完整或較長時間的微調成本，而 PTQ 方法可以避開這個成本。結果針對影像分類，且需要有標籤的訓練資料；大型語言模型的規模下尚未被證實。

## 開放問題與相關變體

- **分布偏移下的穩定性**：可學習步長是依訓練資料擬合的；當部署後的輸入分布改變時，它們是否仍然適用，目前量測不足。
- **相關**：[純整數推論](../integer-only-inference/index.zh-TW.md)在訓練時使用固定的仿射映射；[混合精度](../../mixed-precision/index.zh-TW.md)則為不同層指定不同位元，而不是為每層學習步長。

## 相關連結

LSQ 依賴執行量化模型的[硬體](../../../../../engineering/hardware/index.zh-TW.md)所支援的數字格式。對大型模型而言，訓練成本是主要障礙，因此較常見的是[訓練後量化](../../post-training/index.zh-TW.md)路線。

## 參考文獻

### 開創性論文

- Esser, S. K., 等人 (2019). *Learned Step Size Quantization*. arXiv:1902.08153. https://arxiv.org/abs/1902.08153 — 以梯度下降學習量化步長，3 位元達到全精度準確度。
- Jacob, B., 等人 (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — LSQ 所推廣的固定尺度量化感知訓練。
- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — LSQ 所依據的離散權重直通式訓練。

### 綜述與教科書

- Gholami, A., 等人 (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — 把可學習步長放在訓練期量化方法之中。

### 文章與文件

- Dettmers, T., 等人 (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — 大型語言模型的訓練後替代方案，用於與訓練期方法比較。
