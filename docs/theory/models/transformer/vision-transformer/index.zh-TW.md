---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
  - theory/models/cnn/backbones-and-scaling
  - theory/models/computer-vision
tags:
  - transformers
  - computer vision
  - image classification
aliases:
  - ViT
  - Vision Transformer
  - 視覺 Transformer
  - An Image is Worth 16x16 Words
translation_reviewed: 2026-10-28
---

# 視覺 Transformer（ViT）

視覺 Transformer（Vision Transformer，ViT）把影像切成固定大小的區塊（patch），每個區塊當作一個 token，再把標準的 Transformer 編碼器套用到整個序列上。Dosovitskiy 等人（2021）證明，在影像路徑中完全沒有卷積層的純 Transformer，只要有足夠的預訓練資料，就能在影像分類上追上甚至超越強大的卷積網路。

## 概述

在 ViT 之前，注意力機制在電腦視覺中只與卷積並用，或用來取代卷積的部分元件。卷積內建了局部性與平移等變性，這在資料少時很有幫助。ViT 則問：若模型看過足夠多的資料，這些內建先驗是否仍然必要？依照論文的設定，答案是否定的：模型會從位置嵌入與資料中自行學到空間結構。

代價是 ViT 的歸納偏置（inductive bias）比 CNN 弱。它需要更多資料才能發揮，資料不足時則依賴正則化與資料增強。

## 關鍵概念

- **區塊（patch）**：一個 \(P \times P\) 的像素方塊。一張 \(224 \times 224\) 的影像切成 \(16 \times 16\) 的區塊，會得到 \(N = 196\) 個 token。
- **區塊嵌入（patch embedding）**：把每個展平的區塊線性投影到模型寬度 \(D\)。
- **類別 token（class token）**：一個可學習的向量，接在 token 序列最前面。它的輸出即作為影像表示。
- **位置嵌入（position embedding）**：一組可學習的一維嵌入，加到每個 token 上，讓編碼器知道每個區塊在影像中的位置。
- **骨幹變體**：以尺寸命名，如 ViT-Base（86M 參數）、ViT-Large（307M）、ViT-Huge（632M），再加上區塊大小，例如 ViT-L/16。

## 運作方式

給定影像 \(x \in \mathbb{R}^{H \times W \times C}\) 與區塊大小 \(P\)，影像被重排為 \(N = HW / P^2\) 個展平的區塊 \(x_p^i\)。編碼器的輸入為

\[
z_0 = \big[\, x_{\text{class}};\ x_p^1 E;\ x_p^2 E;\ \dots;\ x_p^N E \,\big] + E_{\text{pos}}
\]

其中 \(E\) 是區塊投影矩陣，\(E_{\text{pos}}\) 是位置嵌入。每一層 \(\ell\) 都是標準的前置正規化（pre-norm）Transformer 區塊：

\[
z'_\ell = \mathrm{MSA}\big(\mathrm{LN}(z_{\ell-1})\big) + z_{\ell-1}, \qquad
z_\ell = \mathrm{MLP}\big(\mathrm{LN}(z'_\ell)\big) + z'_\ell
\]

影像表示是最後一層經過層正規化的類別 token \(y = \mathrm{LN}(z_L^0)\)，再接一個線性分類器。除了區塊投影與位置嵌入之外，編碼器與語言用的 Transformer 相同。

## 關鍵方法

### An Image is Worth 16x16 Words（Dosovitskiy 等人，2021）

- **問題：** Transformer 已主導自然語言，但在視覺中注意力仍主要與 CNN 並用。問題是：純 Transformer 能否在沒有卷積結構的情況下把影像分類做好。
- **核心想法：** 把影像切成區塊，把每個區塊嵌入為一個 token，再餵入未經修改的 Transformer 編碼器。模型規模與預訓練資料同步擴大。
- **方程式或演算法：** 上述的區塊嵌入、類別 token 與各層方程式。訓練方式是監督式分類，在類別 token 上接線性分類頭。
- **結果：** 摘要指出，直接套用到影像區塊序列上的純 Transformer「能在影像分類任務上表現非常好」；在大量資料上預訓練後，ViT「相較於最先進的卷積網路取得優異結果，同時訓練所需的計算資源大幅減少」。論文的表 2 顯示，在內部資料集 JFT-300M 上預訓練後，ViT-H/14 在 ImageNet 上達到 88.55% top-1，ViT-L/16 為 87.76%，兩者都在較高解析度下微調。
- **限制：** 論文的優勢只在大規模預訓練下出現，摘要的措辭已清楚表明這一點。最佳結果依賴不公開的 JFT-300M。論文的主要證據是分類任務；偵測與分割是後來的工作。

### 變體與相關模型

以下是建立在 ViT 之上的具名方法。每一個都應該有自己的頁面，目前還沒有。

- **DeiT**（Touvron 等人，2021）只用 ImageNet 訓練 ViT。其 86M 參數的參考模型在 ImageNet 上不使用外部資料即達到 83.1% top-1，並加入一個蒸餾 token，讓學生模型透過注意力向教師學習。[arXiv:2012.12877](https://arxiv.org/abs/2012.12877)
- **Swin Transformer**（Liu 等人，2021）建立階層式的 ViT，在平移後的局部視窗內計算自注意力。其計算成本隨影像大小線性成長，並作為偵測與分割的通用骨幹。[DOI 10.1109/ICCV48922.2021.00986](https://doi.org/10.1109/ICCV48922.2021.00986)
- **ConvNeXt**（Liu 等人，2022）走了相反的方向：以 Transformer 式的設計選擇現代化 ResNet，仍然是純卷積網路。[卷積骨幹與縮放](../../cnn/backbones-and-scaling/convnext/index.md)

## 組件與變體

- **預訓練資料與正則化。** ViT 的歸納偏置較弱，因此結果取決於資料與訓練配方。Steiner 等人（2022）顯示，更多的計算加上資料增強與正則化（「AugReg」），可以追上資料多約十倍的模型；而在公開的 ImageNet-21k 上訓練的模型，能匹配或超越在較大、但不公開的 JFT-300M 上訓練的對照模型。
- **階層式與視窗式注意力。** Swin 等模型以局部視窗換取全域注意力，較適合密集預測任務。
- **蒸餾與資料高效訓練。** DeiT 顯示，卷積網路教師能幫助 ViT 只用 ImageNet 也能學好。

## 連結

- [Transformer 與注意力機制](../index.md)提供 ViT 所沿用的注意力與 Transformer 區塊。原始論文的介紹見 [Attention Is All You Need](../attention-is-all-you-need/index.md)。
- [卷積骨幹與縮放](../../cnn/backbones-and-scaling/index.md)是 ViT 所對照的卷積替代方案，主要參考為 ResNet 與 EfficientNet。
- [電腦視覺](../../computer-vision/index.md)把 ViT 列在影像分類模型中，並涵蓋 ViT 式骨幹的應用任務。
- [Diffusion Transformer](../dit/index.md)把同樣的「區塊即 token」概念應用到擴散模型中的潛在影像。
- 與大腦的連結較為間接：卷積模型中局部性的強烈作用，正是 ViT 捨棄的歸納偏置之一，這項比較也是在問視覺需要哪些先驗。

## 應用

- 大規模影像分類：預訓練的 ViT 模型作為骨幹，遷移到較小的基準資料集，如原論文在 ImageNet 與 CIFAR-100 上的評估。
- 以 ViT 式骨幹進行物件偵測與語意分割。Steiner 等人（2022）把這些任務列為 ViT 取得強勁結果的場域。
- 官方程式碼與預訓練權重由 Google Research 發布。[google-research/vision_transformer](https://github.com/google-research/vision_transformer)

## 未解問題

- **需要多少歸納偏置。** 以更多資料或更強的資料增強訓練後，模型與 CNN 的差距會縮小，但模型應該內建多少局部性或平移等變性，仍有爭論。
- **ViT 學到什麼。** Raghu 等人（2021）發現，ViT 各層的表示比 CNN 更均勻，且自注意力會及早彙整全域資訊。這種結構是否能解釋 ViT 的遷移行為，尚無定論。
- **全域注意力的成本。** 對所有區塊做全域注意力，成本隨區塊數量平方成長，因而限制了解析度。視窗式與階層式設計可以緩解此問題，但代價是結構變得更複雜。

## 參考文獻

### 開創性論文

- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929) — 原始的 ViT，顯示在大量資料上預訓練後，純 Transformer 處理影像區塊能與 CNN 競爭。
- Touvron, H., et al. (2021). *Training data-efficient image transformers & distillation through attention*. ICML 2021, PMLR 139, pp. 10347–10357. [arXiv:2012.12877](https://arxiv.org/abs/2012.12877) — DeiT，只用 ImageNet 訓練 ViT，並加入蒸餾 token。
- Liu, Z., et al. (2021). *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*. ICCV 2021. [DOI 10.1109/ICCV48922.2021.00986](https://doi.org/10.1109/ICCV48922.2021.00986) — 具平移局部視窗的階層式 ViT，可作為通用視覺骨幹。
- Steiner, A., et al. (2022). *How to train your ViT? Data, Augmentation, and Regularization in Vision Transformers*. Transactions on Machine Learning Research. [arXiv:2106.10270](https://arxiv.org/abs/2106.10270) — 系統性研究資料、資料增強、計算量與模型大小如何交互影響 ViT。
- Raghu, M., et al. (2021). *Do Vision Transformers See Like Convolutional Neural Networks?* [arXiv:2108.08810](https://arxiv.org/abs/2108.08810) — 比較 ViT 與 CNN 的內部表示，以及自注意力與殘差連接的角色。
- Liu, Z., et al. (2022). *A ConvNet for the 2020s*. CVPR 2022. [DOI 10.1109/CVPR52688.2022.01167](https://doi.org/10.1109/CVPR52688.2022.01167) — ConvNeXt，一種與 Transformer 基線相當的純 ConvNet，是 ViT 與 CNN 比較的參照點。

### 綜述與教科書

（本頁尚未查核）

### 講座

（本頁尚未查核）

### 文章與文件

- Google Research, *vision_transformer*, GitHub. [google-research/vision_transformer](https://github.com/google-research/vision_transformer) — 官方的微調程式碼與預訓練 ViT 模型，由原論文的 arXiv 頁面連結。

## 延伸學習

（尚未新增）
