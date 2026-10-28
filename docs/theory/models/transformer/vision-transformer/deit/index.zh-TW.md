---
translation_reviewed: 2026-10-28
---

# DeiT：資料高效的影像 Transformer（Touvron et al., 2020）

DeiT 只使用 ImageNet-1K 訓練 [ViT](../vit/index.md)，採用強資料增強的配方，並加入一個從卷積教師模型學習的蒸餾 token。它屬於[視覺 Transformer](../index.md)主題，回答了原始 ViT 留下的資料問題。

## 概觀

原始的 ViT 需要 JFT-300M（約三億張影像的資料集）才能超越 CNN。DeiT 要問的是：同一個架構能否只用 ImageNet-1K 也訓練出具競爭力的模型？作者從 ViT 的設計出發，保持架構不變，只改變訓練配方以及模型接受監督的方式。論文報告，一個 86M 參數的模型在 384 × 384 下達到 83.1% 的 top-1 準確率，且不使用外部資料，在單一機器上不到三天即可完成訓練（Touvron et al., 2020）。

## 關鍵概念

- **資料高效訓練（data-efficient training）**：配方使用 AdamW、餘弦衰減、比 ViT 更低的權重衰減，並採用強資料增強。移除了 dropout。
- **強資料增強（strong augmentation）**：配方結合 RandAugment、混合式增強、隨機抹除與隨機深度。消融實驗發現幾乎每一項技術都有幫助，dropout 是例外。
- **蒸餾 token（distillation token）**：與分類 token 並列加入的第二個學得 token，其輸出被訓練去匹配教師的預測，而非真實標籤。
- **硬標籤蒸餾（hard-label distillation）**：以教師的 top-1 預測作為目標，而不是使用其完整的 softmax。

## 運作方式

架構與 ViT 相同，只多了一個 token。區塊與兩個 token 一起經過自注意力，分類 token 與蒸餾 token 各自產生輸出。蒸餾以教師的硬決策 y_t = argmax_c Z_t(c) 作為第二個目標。損失函數為

$$
\mathcal{L}^{\text{hardDistill}}_{\text{global}} = \tfrac{1}{2}\,\mathcal{L}_{\text{CE}}(\psi(Z_s), y) + \tfrac{1}{2}\,\mathcal{L}_{\text{CE}}(\psi(Z_s), y_t)
$$

其中 Z_s 與 Z_t 分別是學生與教師的 logits，ψ 是 softmax。論文將其與一般的軟蒸餾比較，後者會以溫度參數匹配完整的 softmax。對 Transformer 而言，硬標籤的效果較好。測試時，兩個頭的輸出可以以後期融合（late fusion）的方式結合。

預設的教師是 RegNetY-16GF，它以相同配方在 ImageNet-1K 上訓練，top-1 準確率為 82.9%。論文發現，卷積教師比 Transformer 教師更有幫助，並認為教師的歸納偏誤會傳遞給學生。作者以 Abnar et al.（2020）支持這個解釋。

## 結果

論文的表 5 報告兩種解析度下 ImageNet-1K 的 top-1 準確率。以下數值為論文所報告者。

| 模型 | 解析度 224 | 解析度 384 |
|---|---|---|
| DeiT-B（無蒸餾） | 81.8 | 83.1 |
| DeiT-B（有蒸餾） | 83.4 | 84.5 |
| DeiT-B（有蒸餾，1000 個週期） | 84.2 | 85.2 |

在表 3 的蒸餾比較中，DeiT-B 的硬標籤蒸餾在 224 解析度下達到 83.0%，而軟蒸餾為 81.8%。論文報告，蒸餾後的模型在 384 解析度下超越在 JFT-300M 上預訓練的 ViT-B（85.2% 對 84.15%）。遷移結果與具競爭力的 CNN 相當，DeiT-B 在 CIFAR-10 上達到 99.1%，在 Oxford Flowers 上達到 98.4%。

## 限制

- **依賴教師模型。** 最佳結果需要強大的卷積教師，因此這個配方並未消除 CNN 的作用。
- **超參數敏感。** 作者指出，Transformer 對學習率與權重衰減很敏感，而且此配方依賴數個相互作用的要素，其中包括重複增強。
- **訓練成本。** 這個配方仍需要 GPU 硬體上數天的訓練時間，而最佳結果使用了 1000 個週期。
- **效率的主張。** 論文指出，DeiT-B 在速度與準確率的權衡上略低於 EfficientNet，只有蒸餾後的模型據稱能超越它。

## 開放問題

- 為什麼卷積教師對 Transformer 學生的幫助如此之大？現有解釋都與歸納偏誤有關，但直接證據有限。
- 只用 ImageNet 的配方能否延伸到密集預測任務？[Swin](../swin/index.md) 報告其偵測準確率高於 DeiT-S。
- 增強帶來的效益與最佳化器的選擇如何交互作用？消融實驗只部分回答了這個問題。

## 參考文獻

### 開創性論文

- Touvron, H., et al. (2020). *Training data-efficient image transformers & distillation through attention*. arXiv；ICML 2021. https://arxiv.org/abs/2012.12877 — 原始論文，介紹只用 ImageNet 的配方與蒸餾 token。
- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv；ICLR 2021. https://arxiv.org/abs/2010.11929 — DeiT 保留的 ViT 架構，DeiT 處理的是它的資料需求問題。
- Hinton, G., et al. (2015). *Distilling the Knowledge in a Neural Network*. arXiv. https://arxiv.org/abs/1503.02531 — 提出軟目標知識蒸餾，是 DeiT 比較的基準方法。
- Abnar, S., et al. (2020). *Transferring Inductive Biases through Knowledge Distillation*. arXiv. https://arxiv.org/abs/2006.00555 — 研究知識蒸餾如何把教師的歸納偏誤轉移給學生。

### 文章與文件

- Cubuk, E. D., et al. (2019). *RandAugment: Practical automated data augmentation with a reduced search space*. arXiv. https://arxiv.org/abs/1909.13719 — DeiT 在消融之後採用的資料增強策略。
- Zhang, H., et al. (2017). *mixup: Beyond Empirical Risk Minimization*. arXiv. https://arxiv.org/abs/1710.09412 — 以影像與標籤的凸組合進行訓練，是該配方中的增強方法之一。
- Yun, S., et al. (2019). *CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features*. arXiv. https://arxiv.org/abs/1905.04899 — 剪下並貼上影像區域，並混合標籤，是該配方中的另一種增強。
- Huang, G., et al. (2016). *Deep Networks with Stochastic Depth*. arXiv. https://arxiv.org/abs/1603.09382 — 訓練時隨機丟棄殘差區塊，該配方用於較深的 Transformer。
