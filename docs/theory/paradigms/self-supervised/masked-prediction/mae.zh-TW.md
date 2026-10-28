---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
  - theory/paradigms/self-supervised/contrastive-learning
  - theory/models/transformer/vision-transformer
  - theory/models/cnn
---

# MAE：遮罩自編碼器是可擴展的視覺學習者

遮罩自編碼器（MAE）透過遮住影像的大部分區塊並重建被遮住的區塊，來預訓練視覺 Transformer。編碼器只處理可見的區塊，因此訓練快速；一個小型解碼器負責補上其餘部分。家族層級的全貌見[遮罩預測](index.md)頁。

## 概述

He 等人（2022）顯示，當遮罩比例夠大時，類似 BERT 的遮罩預測也能用於影像。摘要指出，此方法的訓練速度可達「3 倍或更快」，並能提升準確率。摘要也報告，僅以 ImageNet-1K 預訓練的原始 ViT-Huge，微調準確率為 87.8%，並描述這是僅使用 ImageNet-1K 的方法中最佳的準確率。

## 核心概念

- **區塊與遮罩**：影像被切成方形區塊，隨機移除其中 75%。論文指出，75% 「對線性探測與微調都很好」。
- **非對稱的編碼器–解碼器**：編碼器只看可見區塊，不含遮罩符號。解碼器接收編碼後的可見區塊與遮罩符號，重建整張影像。
- **輕量解碼器**：預設解碼器有 8 個 Transformer 區塊，寬度為 512，比編碼器小。它只在預訓練時使用。
- **重建目標**：像素值。論文報告正規化像素目標相較原始像素能提升表徵品質。
- **只計算遮罩區塊的損失**：均方誤差，且只在被遮住的區塊上計算，與 BERT 相同。

## 運作方式

1. 把影像切成區塊並加以嵌入，與視覺 Transformer 相同。
2. 隨機保留一部分區塊（25%），其餘丟棄。
3. 只用視覺 Transformer 編碼器處理保留的區塊。
4. 在被丟棄的位置加入遮罩符號，由輕量解碼器重建所有區塊的像素。
5. 只在被遮住的區塊上計算均方誤差。
6. 預訓練後丟棄解碼器，把完整、未遮罩的影像送進編碼器做辨識任務。

由於編碼器只處理 25% 的可見區塊，預訓練遠比編碼所有區塊便宜。這正是摘要所述加速的來源。

## 關鍵方法

### 遮罩自編碼器是可擴展的視覺學習者（He、Chen、Xie、Li、Dollár 與 Girshick，2022）

- **問題：**BERT 的遮罩語言方法已在文字上奏效。問題是類似的遮罩目標能否有效訓練大型視覺 Transformer。影像有很大的空間冗餘，少量遮罩的區塊往往可以從鄰近區塊推得。
- **核心想法：**遮住大比例的隨機區塊，只編碼可見區塊，並由編碼後的可見區塊加上遮罩符號解碼出像素。
- **方程式或演算法：**只在遮罩區塊上計算的均方誤差、75% 遮罩比例、非對稱編碼器與 8 區塊、寬度 512 的解碼器，以及正規化像素目標，如上述六個步驟所示。
- **結果：**以 MAE 預訓練的 ViT-L 在 ImageNet-1K 上微調，於 224 輸入下達到 85.9% top-1 準確率。ViT-H 於 448 輸入下為 87.8%。ViT-L 的線性探測為 75.8%。在論文針對 ViT-L 於 ImageNet-1K 進行的消融實驗中，正規化像素目標將微調準確率由 84.9% 提升到 85.4%，線性探測由 73.5% 提升到 73.9%。在論文的計時實驗中，讓編碼器不含遮罩符號的設計，使 ViT-L 的牆鐘時間加速 2.8 倍。
- **限制：**線性探測遠落後於微調（ViT-L 為 75.8% 對 85.9%），因此特徵高度依賴微調。解碼器是另一個需要調整的設計選擇，而 75% 的遮罩比例是在影像資料上調整的。

## 關聯

- 此方法的遮罩語言來源，在[遮罩預測](index.md)頁中說明，該頁也涵蓋 BERT 與其他遮罩模型。
- 編碼器是[視覺 Transformer](../../../models/transformer/vision-transformer/index.md)，因此 MAE 預訓練的是與監督式影像分類相同的架構。
- [對比學習](../contrastive-learning/index.md)是另一條路線：它比對視角，而非重建內容。[SimCLR](../contrastive-learning/simclr.md) 是參照範例。
- MAE 的重建目標是[自編碼器與表徵](../../unsupervised/autoencoders-and-representations/index.md)中去噪想法的遮罩形式。
- 影像模型的一般內容見[電腦視覺](../../../models/computer-vision/index.md)。
- 線性探測與微調之間的差距，屬於[理論與評估](../theory-and-evaluation/index.md)的更廣泛討論。

## 開放問題

- 重建像素是否是最好的目標？預測特徵或符號而非像素是自然的替代方案，BEiT 與 SimMIM 等平行方法探索了這個方向。
- 最佳遮罩比例如何隨影像解析度、模型大小與資料類型改變？論文的 75% 設定來自其自身的影像實驗。
- 能否在不付出微調成本的情況下，讓表徵更容易被線性分離？

## 參考文獻

### 代表性論文

- He, K., Chen, X., Xie, S., Li, Y., Dollár, P. & Girshick, R. (2022). *Masked Autoencoders Are Scalable Vision Learners*. CVPR. https://arxiv.org/abs/2111.06377 — 本頁介紹的論文。
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL-HLT. https://arxiv.org/abs/1810.04805 — 遮罩語言預訓練，MAE 沿用其只在遮罩位置計算損失的設計。
- Dosovitskiy, A. et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR. https://arxiv.org/abs/2010.11929 — MAE 所預訓練的視覺 Transformer 架構。
- Bao, H. et al. (2022). *BEiT: BERT Pre-Training of Image Transformers*. ICLR. https://arxiv.org/abs/2106.08254 — 與 MAE 平行發展、用於視覺 Transformer 的遮罩影像建模方法。
- Xie, Z. et al. (2022). *SimMIM: A Simple Framework for Masked Image Modeling*. CVPR. https://arxiv.org/abs/2111.09886 — 設計較簡單的遮罩影像建模框架，與 MAE 同期發展。

### 綜述與教科書

- Balestriero, R. et al. (2023). *A Cookbook of Self-Supervised Learning*. arXiv:2304.12210. https://arxiv.org/abs/2304.12210 — 自監督設計選擇的實務性綜述，包含遮罩建模。
