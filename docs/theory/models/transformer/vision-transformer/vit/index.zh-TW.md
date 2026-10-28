---
translation_reviewed: 2026-10-28
---

# ViT：一張影像值 16x16 個字（Dosovitskiy et al., 2020）

ViT 是把 Transformer 編碼器應用於影像區塊序列、並以監督式分類損失訓練的方法。它是[視覺 Transformer](../index.md)主題中的里程碑式方法，並顯示在預訓練資料充足時，最先進的影像分類不需要卷積。

## 概觀

在 ViT 之前，視覺領域的 Transformer 大多與卷積一起使用。這篇論文的問題是：一個幾乎沒有影像特定結構的原始 Transformer，能否對影像進行分類？它的答案是肯定的，前提是模型要在足夠的資料上預訓練。論文把這個模型描述為接近 [Attention Is All You Need](../../attention-is-all-you-need/index.md) 中的 NLP Transformer，因此既有的大規模實作可以直接使用。

## 關鍵概念

- **區塊序列（patch sequence）**：影像被切成 N = HW/P² 個不重疊的區塊。每個區塊展平後經線性投影，得到寬度為 D 的向量。
- **分類 token（class token）**：加在序列前面的學得向量，借自 BERT。它的最終狀態即為影像的表徵。
- **學得的一維位置嵌入（learned 1D position embeddings）**：論文採用一般的學得嵌入，而非具二維感知的嵌入，因為後者並未帶來明顯的改進。
- **歸納偏誤（inductive bias）**：局部性與平移等變性只出現在切割區塊與 MLP 區塊中。自注意力在每一層都是全域的，因此模型必須從資料中學習空間結構。

## 運作方式

模型接收一張 H × W × C 的影像與區塊大小 P，並執行以下步驟：

1. 形成序列 [x_class; x_p¹E; …; x_pᴺE] + E_pos，其中 E 把每個區塊投影到寬度 D。
2. 對於每一層（共 L 層），對 LN(z) 套用多頭自注意力並加上殘差連接，再套用帶有 GELU 的 MLP，同樣搭配層正規化與殘差連接。
3. 取最後一層之後的分類 token LN(z_L⁰) 作為影像表徵 y。
4. 以包含一個隱藏層的分類頭進行預訓練。微調時，將分類頭換成單一、零初始化的線性層。

論文定義了三種遵循 BERT 的規模：Base 有 12 層、寬度 768、86M 參數；Large 有 24 層、寬度 1024、307M 參數；Huge 有 32 層、寬度 1280、632M 參數。模型以規模與區塊大小命名，因此 ViT-L/16 指的是區塊大小為 16 × 16 的 Large 模型。以較高解析度微調時，區塊大小保持不變，位置嵌入則以二維方式插值到新的網格上。

## 結果

論文表 2 的主要比較使用 ImageNet、CIFAR-100 與 19 項任務的 VTAB 套件上的 top-1 準確率。以下數字為論文報告的平均值。

| 模型（預訓練資料） | ImageNet | CIFAR-100 | VTAB（19 項任務） | TPUv3-core-days |
|---|---|---|---|---|
| ViT-H/14（JFT-300M） | 88.55 | 94.55 | 77.63 | 2.5k |
| ViT-L/16（JFT-300M） | 87.76 | 93.90 | 76.28 | 0.68k |
| BiT-L，ResNet152x4（JFT-300M） | 87.54 | 93.51 | 76.29 | 9.9k |
| ViT-L/16（ImageNet-21K） | 85.30 | 93.25 | 72.72 | 0.23k |

在 JFT-300M 上預訓練的 ViT-L/16 在這些基準上與 ResNet 基準持平或超越，而預訓練的運算成本只是其一小部分。單獨使用 ImageNet 時，ViT 模型落後於規模相近的 ResNet，而且只有在預訓練集變大後，這個差距才會消失。在五個資料集的平均表現上，ViT 以大約 ResNet 兩到四分之一的運算量達到相同的表現。論文也指出，部分注意力頭在最低層就已涵蓋影像的大部分範圍，作者據此認為模型很早就運用了全域脈絡。

## 限制

- **資料需求。** 若沒有大規模預訓練，ViT 會比成本相近的 ResNet 更容易過擬合。最強的結果依賴 JFT-300M，而該資料集並未公開（Steiner et al., 2021）。
- **單一解析度的特徵。** 論文的結論指出，偵測與分割對原始 ViT 而言仍是待解的挑戰。後來的 [Swin](../swin/index.md) 設計針對此問題。
- **自監督的差距。** 作者的遮罩區塊實驗相較於從頭訓練有所改進，但論文指出，它與監督式預訓練之間仍有很大差距。
- **較小區塊的成本。** token 數量與區塊大小的平方成反比成長，因此改用較小區塊所帶來的準確率提升，需要付出運算成本。

## 開放問題

- 在小資料量下的差距，是否會隨著更好的訓練配方而消失？[DeiT](../deit/index.md) 的結果後來探討了這個問題。
- 考慮到混合模型在小運算量預算下表現較好，ViT 的全域注意力究竟是一般性的優勢，還是只在大規模下才有利？
- ViT 學到的注意力模式與 CNN 學到的模式有多接近，仍不清楚。

## 參考文獻

### 開創性論文

- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv；ICLR 2021. https://arxiv.org/abs/2010.11929 — 原始論文，定義了 ViT 及其預訓練與遷移實驗。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — ViT 幾乎完全遵循的 Transformer 編碼器。
- Sun, C., et al. (2017). *Revisiting Unreasonable Effectiveness of Data in Deep Learning Era*. arXiv. https://arxiv.org/abs/1707.02968 — 測量視覺表現在訓練集大小達到 JFT-300M 時的變化，而 ViT 正是依賴該資料集。
- Kolesnikov, A., et al. (2019). *Big Transfer (BiT): General Visual Representation Learning*. arXiv；ECCV 2020. https://arxiv.org/abs/1912.11370 — 大型 ResNet 的遷移配方，ViT 在表 2 中與之比較。

### 文章與文件

- Cordonnier, J.-B., et al. (2020). *On the Relationship between Self-Attention and Convolutional Layers*. arXiv. https://arxiv.org/abs/1911.03584 — 一個關係密切的模型，使用 2×2 區塊與完整的自注意力，ViT 論文對此有所討論。
- Steiner, A., et al. (2021). *How to train your ViT? Data, Augmentation, and Regularization in Vision Transformers*. arXiv. https://arxiv.org/abs/2106.10270 — 顯示資料增強與正規化能部分取代 ViT 最初所依賴的資料。
- Zhai, X., et al. (2021). *Scaling Vision Transformers*. arXiv. https://arxiv.org/abs/2106.04560 — 刻畫 ViT 的誤差如何與資料、運算量與模型規模相關。
