---
translation_reviewed: 2026-10-28
---

# VideoMAE

VideoMAE 是一種用於影片的遮罩自編碼器。它會遮住一段片段中約 90% 的時空方塊，並訓練一個樸素的視覺 Transformer 重建這些方塊。Tong 等人（2022）顯示，這種預訓練只需影片資料本身，不需要影像權重或任何額外資料。它是[影片理解與生成](../index.md)頁所列的方法之一。

## 概述

影片 Transformer 通常以影像模型為基礎。在影片資料集上從零訓練的樸素視覺 Transformer 表現不佳，因此常見的補救做法是影像預訓練。[^1] VideoMAE 探問影片資料本身是否足夠。它把影像的[遮罩自編碼器](../../../../paradigms/self-supervised/masked-prediction/index.md)構想改編到影片，並採用激進得多的遮罩，因為相鄰影格高度冗餘。

## 關鍵概念

- **方塊（tubelet）。** 大小為 $2\times16\times16$ 像素的區塊，即兩個影格乘以一個 $16\times16$ 的圖塊。每個方塊成為一個 token。
- **管狀遮罩。** 對每一影格套用相同的空間遮罩，使被遮住的區域在時間上始終被遮住。如此一來，被遮住的方塊無法靠其可見的時間鄰居來還原；隨機遮罩對靜止區域則會允許這種洩漏。[^2]
- **非對稱編碼器—解碼器。** 編碼器只看可見的 token，較輕量的解碼器負責重建被遮住的部分。

## 運作方式

1. 取樣一段片段，做時間下取樣，並切分為方塊。
2. 以管狀遮罩遮住約 90% 的 token。
3. 可見的 token 經過採用聯合時空注意力的[視覺 Transformer](../../../transformer/vision-transformer/vit/index.md)。
4. 將編碼器輸出與可學習的遮罩 token 送入淺層解碼器，預測被遮住部分的像素。

損失函數是在被遮住方塊上的均方誤差，計算於正規化後的像素值。對於被遮住 token 的集合 $\Omega$，以 $I(p)$ 為目標、$\hat I(p)$ 為預測，

$$
\mathcal{L} = \frac{1}{|\Omega|}\sum_{p\in\Omega}\left\lVert I(p)-\hat I(p)\right\rVert_2^2 .
$$

這就是以方塊取代圖塊的影像 MAE 目標。[^3] 只有約 10% 的 token 進入編碼器，因此即使週期較多，預訓練仍比對比式基準 MoCo v3 省成本。論文回報為 19.5 小時，相較之下 MoCo v3 為 61.7 小時。[^2]

## 結果

以 16 影格的 ViT-B 為例，各方法只在目標資料集的訓練切分上預訓練。VideoMAE 在每個資料集上都優於從零訓練與 MoCo v3：[^2]

| 資料集 | 訓練片段數 | 從零訓練 | MoCo v3 | VideoMAE |
|---|---|---|---|---|
| [Kinetics-400](https://arxiv.org/abs/1705.06950) | 24 萬 | 68.8 | 74.2 | 80.0 |
| Something-Something V2 | 16.9 萬 | 32.6 | 54.2 | 69.6 |
| UCF101 | 9,500 | 51.4 | 81.7 | 91.3 |
| HMDB51 | 3,500 | 18.0 | 39.2 | 62.6 |

在不使用額外資料的情況下，Kinetics-400 的準確率在 ViT-B 為 81.5%、ViT-L 為 85.2%、ViT-H 為 86.6%，而以較高解析度推論的 ViT-H 為 87.4%。[^2]

## 限制

- **領域很重要。** 先在 Kinetics 預訓練再遷移到 Something-Something V2，略遜於直接在目標資料上預訓練。作者將此歸因於領域偏移。[^2]
- **訓練時間長。** 消融實驗使用 800 個週期，Kinetics-400 的比較則為 1600 個，而最大的模型有 6.33 億參數。[^2]
- **二次方的注意力成本。** 聯合時空注意力的成本仍隨 token 數量呈二次方成長，高遮罩比率只能部分緩解。[^2]

## 開放問題

- 重建像素能否和重建外觀一樣有效地學到運動？[V-JEPA](https://arxiv.org/abs/2404.08471) 預測特徵而非像素，並報告了強勁的影片表徵，顯示預測目標的選擇很重要。[^4]
- 90% 的遮罩比率在識別以外的任務上，例如生成或影片與語言建模，是否仍是最佳值？

## 參考文獻

### 開創性論文

- Tong, Z., Song, Y., Wang, J. & Wang, L. (2022). *VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training*. NeurIPS. https://arxiv.org/abs/2203.12602 — 本論文：以 90% 遮罩比率與管狀遮罩進行方塊重建。
- He, K., et al. (2021). *Masked Autoencoders Are Scalable Vision Learners*. arXiv. https://arxiv.org/abs/2111.06377 — VideoMAE 所改編的影像 MAE，採用非對稱編碼器。
- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv. https://arxiv.org/abs/2010.11929 — VideoMAE 採用為骨幹的視覺 Transformer。
- Chen, X., Xie, S. & He, K. (2021). *An Empirical Study of Training Self-Supervised Vision Transformers*. arXiv. https://arxiv.org/abs/2104.02057 — MoCo v3，比較中的對比式基準。
- Kay, W., et al. (2017). *The Kinetics Human Action Video Dataset*. arXiv. https://arxiv.org/abs/1705.06950 — 用於預訓練與評估的 Kinetics-400 資料集。
- Goyal, R., et al. (2017). *The "something something" video database for learning and evaluating visual common sense*. arXiv. https://arxiv.org/abs/1706.04261 — Something-Something 資料集，用於測試對運動敏感的辨識。
- Soomro, K., Zamir, A. R. & Shah, M. (2012). *UCF101: A Dataset of 101 Human Actions Classes From Videos in The Wild*. arXiv. https://arxiv.org/abs/1212.0402 — 遷移實驗所用的 101 類動作資料集。
- Kuehne, H., Jhuang, H., Garrote, E., Poggio, T. & Serre, T. (2011). *HMDB: A large video database for human motion recognition*. ICCV. https://doi.org/10.1109/ICCV.2011.6126543 — 51 類動作資料集，也是此處使用的最小資料集。
- Bardes, A., et al. (2024). *Revisiting Feature Prediction for Learning Visual Representations from Video*. arXiv. https://arxiv.org/abs/2404.08471 — V-JEPA，透過預測特徵而非像素來學習影片表徵。

[^1]: Tong 等人（2022），引言：影片 Transformer 通常衍生自影像模型，從零訓練的結果並不理想。
[^2]: Tong 等人（2022）：第 3 節（管狀遮罩、編碼器與時程）、表 2（16 影格 ViT-B 比較）、表 3（預訓練時間）、表 7（Kinetics-400 的擴展），以及預訓練資料集段落中關於領域偏移的討論。
[^3]: He 等人（2021）：MSE 損失計算於被遮住圖塊經正規化後的像素。
[^4]: Bardes 等人（2024），摘要：不做像素重建、僅以特徵預測為目標，在兩百萬段影片上訓練。
