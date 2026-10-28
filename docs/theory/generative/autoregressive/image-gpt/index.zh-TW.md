---
translation_reviewed: 2026-10-28
---

# Image GPT

Image GPT（iGPT）訓練一個 GPT-2 風格的 Transformer，預測低解析度影像的下一個像素，且不使用卷積或其他影像專屬的結構。Chen 等人（2020）證明，它學到的特徵足以在標準基準上與有監督及自監督的表徵一較高下。它是 [自回歸生成模型](../index.md)概述中的代表性方法之一，也是語言中下一個詞元預測在影像上的對應方法。

## 概述

下一個詞元預測讓大型 Transformer 能在語言上預訓練，例如 GPT 風格的[大型語言模型](../../../models/llm/index.md)。Chen 等人想知道，同樣的生成式預訓練是否也適用於影像。一張 32 × 32 的 RGB 影像已經有 3,072 個值，而密集自注意力的成本隨序列長度呈平方成長。

作者因此降低解析度並量化顏色，以縮短序列，接著在未標註的 ImageNet 上預訓練，並以線性探測與微調來衡量結果。最佳的特徵不在最後一層，而且品質會隨模型規模提升。

## 核心概念

- **光柵序列**：影像被展開為一維的像素序列，依列排列。每個位置只由它之前的位置預測。
- **顏色調色盤**：以 k-means 把 (R, G, B) 值聚類為 512 種顏色，因此每個像素成為一個詞元。
- **線性探測**：在凍結的某一層特徵上訓練的線性分類器。它衡量學到的表徵在線性上可分離的程度。

## 運作方式

模型以序列的負對數似然為目標進行訓練，損失函數即下一個詞元的交叉熵：

\[
\mathcal{L}_{\text{AR}} = \mathbb{E}_{x}\Big[-\sum_{i} \log p\big(x_i \mid x_1, \dots, x_{i-1}\big)\Big]
\]

步驟如下：

1. 把影像調整為例如 32 × 32 的大小，並把每個像素對應到最接近的調色盤顏色。較大的輸入則使用詞彙表大小為 4,096 的 VQ-VAE。
2. 嵌入詞元並加上可學習的位置嵌入。接著經過一疊 Transformer 區塊，其注意力邏輯上套用因果遮罩，每個位置得到一個向量。
3. 由最後的向量投影出每個位置 512 個 logits，訓練時最小化上述損失。
4. 分類時，線性探測讀取某一選定層的特徵，微調則加上分類頭。

生成時與其他自回歸模型相同，一次抽取一個詞元。[KV 快取](../../../models/transformer/kv-cache/index.md)讓每一步更便宜，但過程仍是依序進行的。

## 結果

- **CIFAR-10。** 線性探測的準確度為 96.3%，作者指出這高於有監督的 Wide ResNet。完整微調則達到 99.0%。
- **ImageNet。** 最佳單層的線性探測在 32 × 32 的模型解析度下為 60.3%，在 48 × 48 下為 65.2%。串接 11 層的特徵並使用 VQ-VAE 前處理後為 69.0%，作者認為這與當時的對比式學習方法不相上下。
- **模型規模。** 在 32 × 32 的模型解析度下，ImageNet 最佳單層的線性探測準確度，最小的模型（iGPT-S，7,600 萬參數）為 41.9%，iGPT-M（4.55 億參數）為 54.5%，iGPT-L（14 億參數）為 60.3%。
- **層的深度。** 表徵品質隨深度上升，之後下降。在 CIFAR-10 上，最後一層比最佳層低 2.4%。
- **與 BERT 的比較。** 以 BERT 式遮罩目標訓練的模型，線性探測較弱，但在 CIFAR-10 上微調可達 98.6%。

作者表示，他們的目標是表徵學習，而非高品質的樣本，因此只展示了定性的無類別條件樣本。

## 限制

- **二次方的注意力成本。** 密集自注意力的成本隨序列長度的平方增長，因此只能使用低解析度。作者稱之為重大限制，並指出稀疏注意力是可能的解法。
- **規模。** 結果依賴大型模型與大量運算。作者指出，iGPT-L 的參數量是在 ImageNet 上表現相近的模型的兩到三倍，並且使用了更多運算。
- **沒有空間先驗。** 模型必須從資料中學習空間結構，作者也指出，要與卷積編碼器相比並縮小差距並不容易。

## 未解問題

- **生成式與判別式訓練。** 像素預測能否在高解析度下匹敵對比式方法，而且不必依賴大得多的模型，目前尚無定論。
- **詞元化的選擇。** 顏色調色盤是一種粗糙的分詞方式。[VQ-VAE](../../vae/vq-vae/index.md) 學得的編碼能在相同長度下保留更多細節。

## 與其他主題的連結

- **母主題。** iGPT 是 [自回歸生成模型](../index.md)家族在影像上的案例，與 [PixelCNN](../pixelcnn/index.md) 並列。
- **語言模型。** 其目標與預測下一個詞元的[大型語言模型](../../../models/llm/index.md)一致。另見[分詞](../../../models/llm/tokenisation/index.md)與[多模態模型](../../../models/multimodal/index.md)。
- **遮罩預測。** BERT 式的另一種方法見[遮罩預測](../../../paradigms/self-supervised/masked-prediction/index.md)。

## 應用

- **影像生成。** 以文字與影像詞元為對象的 Transformer，能依文字提示生成影像（Ramesh 等人，2021）。VQGAN 式的 Transformer 在類別條件的 ImageNet 合成上，曾是自回歸模型中的最佳成果（Esser 等人，2021）。

## 參考文獻

### 開創性論文

- Chen, M., Radford, A., Child, R., Wu, J., Jun, H., Luan, D. & Sutskever, I. (2020). *Generative Pretraining From Pixels*. ICML (PMLR 119). https://proceedings.mlr.press/v119/chen20s.html — 論文本身：以 GPT-2 風格的 Transformer 預測像素，並報告可用於分類的特徵。
- Vaswani, A. et al. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — 提出 iGPT 所建立於其上的 Transformer。
- Child, R. et al. (2019). *Generating Long Sequences with Sparse Transformers*. arXiv. https://arxiv.org/abs/1904.10509 — 提出稀疏注意力分解，以降低二次方的成本。
- van den Oord, A., Vinyals, O. & Kavukcuoglu, K. (2017). *Neural Discrete Representation Learning*. arXiv. https://arxiv.org/abs/1711.00937 — 提出 VQ-VAE，其編碼用於較高解析度的輸入。
- Ramesh, A. et al. (2021). *Zero-Shot Text-to-Image Generation*. arXiv. https://arxiv.org/abs/2102.12092 — 把文字與影像詞元建模為單一的自回歸序列。
- Esser, P., Rombach, R. & Ommer, B. (2021). *Taming Transformers for High-Resolution Image Synthesis*. arXiv. https://arxiv.org/abs/2012.09841 — 以 Transformer 對 VQ 碼本序列建模，用於高解析度合成。

### 綜述與教科書

- Bond-Taylor, S., Leach, A., Long, Y. & Willcocks, C. G. (2021). *Deep Generative Modelling: A Comparative Review of VAEs, GANs, Normalizing Flows, Energy-Based and Autoregressive Models*. arXiv. https://arxiv.org/abs/2103.04922 — 比較自回歸模型與其他生成模型家族。
