---
translation_reviewed: 2026-10-28
related:
  - theory/models/llm/index.md
  - theory/models/speech/index.md
---

# 自迴歸生成模型（Autoregressive Generative Models）

自迴歸生成模型把資料物件的聯合機率寫成條件機率的乘積，一次處理一個元素。對影像、聲音或句子而言，這把同時建模所有東西的困難問題，轉換為一連串較容易的問題：給定前面的所有內容，預測下一個像素、下一個音訊樣本或下一個詞元。語言模型是最為人知的例子，同樣的想法也能生成影像與聲音。

## 概述

機率的鏈式法則指出，對於序列 $x_1, \dots, x_n$，

$$
p(x_1, \dots, x_n) = \prod_{i=1}^{n} p(x_i \mid x_1, \dots, x_{i-1}),
$$

因此，一個能由前面元素預測每個元素的模型，就定義了整個序列上的完整分布。訓練是最大化資料上各條件對數機率之和，這是精確的最大似然，沒有潛在變數，也不需要對似然做近似。取樣則沿著鏈向前執行：先抽出 $x_1$，再依 $x_1$ 抽出 $x_2$，依此類推。

代價在取樣。生成需要逐元素的一步步進行，而這些步驟通常無法像其他計算那樣在序列上平行化。元素的排列順序也是一項設計選擇，因為分解依賴於排序，即使聯合分布本身並不依賴。

## 關鍵概念

- **分解**：元素被建模的順序選擇。對影像而言，通常是逐列的光柵順序。
- **似然**：模型對資料的對數機率，可以精確計算，並能在不同模型間比較。
- **教師強迫（teacher forcing）**：訓練時，每個條件都用真實的前序元素來擬合，因此所有位置可以平行訓練。
- **詞元（token）**：條件分布所定義於其上的離散單位，例如詞或碼本項目。影像或音訊通常先被映射為詞元。
- **取樣成本**：生成一個物件所需的連續步驟數。

## 運作方式

**像素。** PixelRNN（van den Oord、Kalchbrenner 與 Kavukcuoglu，2016）沿兩個空間維度依序預測影像的像素，使每個像素依賴於排序中在它之前的像素。論文摘要描述了一個以這種方式依序預測影像像素的深度網路。以卷積實作的變體稱為 PixelCNN，遵循相同的分解，在訓練時能更有效率地計算。

**原始音訊。** WaveNet（van den Oord 等人，2016）是用於生成原始音訊波形的深度網路。它依前面的樣本預測每一個音訊樣本，因此能一次一個樣本地生成語音與音樂。

**以 Transformer 處理像素。** Image GPT（Chen 等人，2020）訓練一個序列 Transformer 以自迴歸方式預測像素，且不內建輸入的二維結構知識。這個方法與語言建模採用同一種下一元素目標，只是把它應用於影像像素。Transformer 架構本身見[注意力就是你所需要的一切](../../../../models/transformer/attention-is-all-you-need/index.md)，論文把它描述為「完全只基於注意力機制，捨棄了遞迴與卷積」（Vaswani 等人，2017）。

**詞元與潛在編碼。** 對每個像素建模的成本很高，因此許多系統先壓縮資料。VQ-VAE（van den Oord、Vinyals 與 Kavukcuoglu，2017）把向量量化納入自編碼器，學習離散的潛在表示。之後便可以在這些離散編碼上擬合自迴歸先驗，其長度遠短於原始資料。

## 關鍵方法

簡要比較。上面提到的每個方法都可以有自己的方法頁面；這些頁面尚未撰寫，因此目前在本節提供細節。

- **PixelRNN 與 PixelCNN（像素層級）**：排序是空間性的，模型預測每個像素的值。對影像可精確計算似然，但在全解析度下取樣很慢。
- **WaveNet（樣本層級）**：把同一種分解應用於音訊樣本，這是非常長的序列。
- **Image GPT（像素上的 Transformer）**：以 Transformer 取代循環或卷積模型，使用與語言相同的下一元素目標。
- **基於詞元的自迴歸先驗（VQ-VAE）**：自迴歸模型在一段短的離散編碼序列上運作，而非在像素上運作。

## 關聯

同樣的目標也是[大型語言模型](../../../../models/llm/index.md)的基礎，這些模型逐個詞元地生成文字；另外[語音與音訊](../../../../models/speech/index.md)頁面中的語音模型亦然。在其他生成模型家族中，[擴散模型](../diffusion/index.md)是透過迭代去噪而非固定順序來生成；兩者的比較是[生成模型](../generative-models/index.md)總覽的一部分。

與大腦的連結在預測的層級。神經科學中的預測框架主張大腦會預期它的下一個輸入，這與下一元素預測是同一種目標。神經迴路是否以自迴歸模型的方式實現這一點，是一個開放的問題，在 [NeuroAI](../../../../../brain-mind/neuroai/index.md) 中討論。

## 應用

- **文字。** 逐個詞元生成文字的語言模型。
- **語音與音訊。** 生成語音或音樂的波形與編解碼模型。
- **影像。** 用於影像生成與補全的像素層級與詞元層級模型。

## 開放問題

- 取樣是依序進行的，因此生成長物件很慢。平行解碼方法縮小了差距，但增加了複雜度。
- 序列前段的錯誤會累積，因為後面的條件依賴於它們。
- 影像與其他非序列資料的最佳排序並不明顯，不同的排序會得到不同的模型。
- 自迴歸模型與擴散模型在精確似然、取樣速度與樣本品質之間有不同的取捨，最佳選擇取決於資料與任務。

## 參考文獻

### 開創性論文

- van den Oord, A., Kalchbrenner, N. & Kavukcuoglu, K. (2016). *Pixel Recurrent Neural Networks*. arXiv. https://arxiv.org/abs/1601.06759 — 沿空間維度依序預測像素來建模影像，是 PixelRNN 家族的基礎。
- van den Oord, A., Dieleman, S., Zen, H., Simonyan, K., Vinyals, O., Graves, A., Kalchbrenner, N., Senior, A. & Kavukcuoglu, K. (2016). *WaveNet: A Generative Model for Raw Audio*. arXiv. https://arxiv.org/abs/1609.03499 — 逐樣本生成原始音訊波形的深度網路。
- Chen, M., Radford, A., Child, R., Wu, J., Jun, H., Luan, D. & Sutskever, I. (2020). Generative Pretraining from Pixels. 收錄於 *Proceedings of the 37th International Conference on Machine Learning (ICML 2020)*, PMLR 108。https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V1_ICML.pdf — 訓練序列 Transformer 以自迴歸方式預測像素，且不內建二維結構。
- van den Oord, A., Vinyals, O. & Kavukcuoglu, K. (2017). *Neural Discrete Representation Learning*. arXiv. https://arxiv.org/abs/1711.00937 — VQ-VAE，以向量量化學習離散潛在編碼，使先驗能在短的詞元序列上擬合。
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — Transformer，作為自迴歸生成中的序列模型。
