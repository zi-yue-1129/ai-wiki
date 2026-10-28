---
translation_reviewed: 2026-10-28
---

# 視覺 Transformer（ViT）

視覺 Transformer（Vision Transformer, ViT）把標準的 Transformer 編碼器應用於影像：先將影像切成固定大小的區塊，再把每個區塊當作一個 token 處理。它由 Dosovitskiy 等人於 2020 年提出，證明了在有足夠預訓練資料的前提下，不含卷積的模型也能在影像分類上與卷積網路匹敵。

## 概觀

在 2010 年代的大部分時間裡，影像辨識都建立在[卷積神經網路](../../cnn/index.md)（CNN）之上。卷積在網路中內建了兩個假設：相鄰的像素彼此相關，而且有用的圖樣可以出現在影像的任何位置。Transformer 對輸入做出的假設較少：每一層自注意力都讓任一 token 與其他所有 token 建立關聯。若直接把注意力用在原始像素上，成本太高，因為成本會隨像素數的平方成長。早期的視覺研究要麼把注意力限制在局部鄰域，要麼把它與 CNN 結合。

ViT 採用較簡單的做法。它幾乎完整保留原始的 Transformer 編碼器，只改變輸入：影像被切成區塊，每個區塊被展平並做線性投影，得到的序列則像一個由詞嵌入組成的句子一樣處理。

核心發現與資料有關。若只在 ImageNet-1K 上訓練，ViT 的表現低於規模相近的 ResNet。若在 ImageNet-21K（約 1,400 萬張影像）或內部的 JFT-300M 資料集（約 3.03 億張影像）上預訓練，它便能接近甚至超越最好的 CNN，同時所需的預訓練資源更少（Dosovitskiy et al., 2020）。架構與實驗的完整說明見 [ViT 方法頁](vit/index.md)。

## 關鍵概念

- **影像區塊嵌入（patch embedding）**：一個具有 C 個通道、大小為 P × P 的區塊被展平後，乘上一個學得的矩陣，得到寬度為 D 的 token。這是唯一把影像的二維結構切成片段的步驟。
- **分類 token（class token）**：加在序列最前面的一個額外可學習向量。它在最後一層的輸出就是影像的表徵。這個做法借自 BERT（見[架構家族](../architecture-families/index.md)）。
- **位置嵌入（position embedding）**：加在每個 token 上的可學習向量，用來表示該區塊的位置。若沒有它，注意力層會把各個區塊視為無序的集合。一般情形見[位置編碼](../positional-encodings/index.md)。
- **歸納偏誤（inductive bias）**：讓模型能用較少範例學習的內建假設。CNN 在每一層都有局部性與平移等變性；ViT 只在切割區塊與 MLP 區塊中具有這些性質，這解釋了它在小資料上的大部分行為。
- **階層式表徵（hierarchical representation）**：像 CNN 一樣，特徵圖會被反覆降採樣，使較深的層看到較粗的解析度。原始的 ViT 則在各層都維持同一種解析度。

## 運作方式

一張 224 × 224 的 RGB 影像被切成 16 × 16 的區塊後，會得到 196 個區塊，加上分類 token 後 Transformer 看到的是 197 個 token。步驟如下：

1. 把影像切成 N = HW / P² 個區塊，並將每個區塊展平。
2. 用同一個線性映射，把每個展平的區塊投影到寬度 D。
3. 加入學得的分類 token，並加上位置嵌入。
4. 讓序列通過 L 個前置正規化的 Transformer 區塊，每個區塊都由多頭自注意力與 MLP 組成，並附有殘差連接。
5. 把分類頭套用在分類 token 的輸出上。

```mermaid
flowchart LR
  A["影像 H × W × C"] --> B["N 個大小為 P × P 的區塊"]
  B --> C["線性投影與位置嵌入"]
  C --> D["加入分類 token"]
  D --> E["L 個 Transformer 編碼器區塊"]
  E --> F["分類 token 輸出"]
  F --> G["分類頭"]
```

以方程式表示，分類 token 位於第一個位置，各區塊的計算為

$$
z_0 = [x_{\text{class}};\, x_p^1 E;\, \dots;\, x_p^N E] + E_{\text{pos}}
$$

$$
z'_\ell = \text{MSA}(\text{LN}(z_{\ell-1})) + z_{\ell-1}, \qquad z_\ell = \text{MLP}(\text{LN}(z'_\ell)) + z'_\ell
$$

其中 \(E\) 是區塊投影矩陣，\(\text{LN}\) 是層正規化。注意力與 MLP 的方程式與 [Attention Is All You Need](../attention-is-all-you-need/index.md) 中的語言 Transformer 相同，差別只在 token 的內容。

token 的數量由區塊大小決定。把區塊的邊長減半，token 數量會變為四倍，而注意力的成本隨 token 數的平方成長。這也是模型以區塊大小命名的原因：ViT-L/16 是 Large 規模、區塊大小為 16 × 16 的模型。

### 為什麼資料規模重要

這個架構內建的結構很少，因此結構必須由預訓練資料提供。只在 ImageNet-1K 上訓練時，Large 模型的表現反而不如 Base 模型。在 ImageNet-21K 上兩者相近，只有在 JFT-300M 上，較大的模型才展現完整優勢。在小資料量下，ViT 比規模相近的 ResNet 更容易過擬合；在最大的資料量下，ViT 則超越 ResNet（Dosovitskiy et al., 2020）。作者把這解讀為內建偏誤與從資料學習之間的權衡。

後續研究從其他角度檢驗了這個問題。Sun et al.（2017）發現視覺任務的表現大致隨訓練集大小的對數成長。Steiner et al.（2021）指出，較強的資料增強與正規化可以替代部分資料：在 ImageNet-21K 上以較多運算量訓練的 ViT，與在 JFT-300M 上訓練的模型相當，甚至更好。DeiT 論文則顯示，只用 ImageNet-1K，配合仔細的訓練，也能達到具競爭力的準確率（Touvron et al., 2021）。

## 關鍵方法

下表比較三個里程碑式的變體，每個方法各有專頁。

| 方法 | 年份 | 主要改變 | 頁面 |
|---|---|---|---|
| ViT（Dosovitskiy et al.） | 2020 | 直接在影像區塊上使用原始的 Transformer，需要大規模預訓練 | [ViT](vit/index.md) |
| DeiT（Touvron et al.） | 2020 | 只用 ImageNet-1K 訓練 ViT，並採用強資料增強與蒸餾 token | [DeiT](deit/index.md) |
| Swin（Liu et al.） | 2021 | 階層式特徵，注意力限於移位的局部視窗內，使成本隨影像大小線性成長 | [Swin](swin/index.md) |

## 關聯

- **CNN 骨幹網路。** ViT 是 [骨幹網路與縮放](../../cnn/backbones-and-scaling/index.md)中 CNN 設計的直接挑戰者。[ConvNeXt](../../cnn/backbones-and-scaling/convnext/index.md) 從 [ResNet](../../cnn/backbones-and-scaling/resnet/index.md) 出發，逐步採用 Transformer 式的設計選擇，在相近成本下與 Swin 相當，甚至更好（Liu et al., 2022）。
- **影像中的注意力。** 只要頭數足夠，多頭自注意力層就能表達任何卷積，而訓練後的注意力也常常學會這麼做（Cordonnier et al., 2020）。
- **架構家族。** ViT 是僅編碼器模型，與 [BERT](../architecture-families/bert/index.md) 相同，其分類 token 扮演 BERT 中 `[CLS]` token 的角色。
- **自監督預訓練。** ViT 論文包含一個初步的遮罩區塊目標。[遮罩預測](../../../paradigms/self-supervised/masked-prediction/index.md)方法則對此加以延伸，而遮罩自編碼器僅用 ImageNet-1K 資料就能達到很高的準確率（He et al., 2021）。
- **知識蒸餾。** DeiT 的額外 token 複製教師模型的輸出，因此與[知識蒸餾](../../../model-compression/knowledge-distillation/index.md)相連。ViT 也常作為[多模態模型](../../multimodal/index.md)中的影像編碼器。
- **腦與心智。** 經過表現最佳化的階層式網路能預測 V4 與顳下皮質的反應（Yamins et al., 2014），見[視覺感知](../../../../brain-mind/visual-perception/index.md)。CNN 高度依賴紋理（Geirhos et al., 2019），而 ViT 較少依賴紋理，且對遮擋具有穩健性（Naseer et al., 2021）。它的錯誤模式也比 CNN 更接近人類的錯誤（Tuli et al., 2021）。更廣泛的脈絡見 [NeuroAI](../../../../brain-mind/neuroai/index.md)。

## 應用

- **影像分類。** 在 JFT-300M 上預訓練的 ViT-H/14 在 ImageNet 上達到 88.55% 的 top-1 準確率，而在 ImageNet-21K 上預訓練的 ViT-L/16 達到 85.30%（Dosovitskiy et al., 2020）。
- **密集預測。** 原始 ViT 只有單一的特徵解析度，這限制了物件偵測與分割的表現。Swin 的階層式骨幹即為解決此問題而設計，並與 Cascade Mask R-CNN 及 UperNet 搭配使用（Liu et al., 2021）。見[物件偵測](../../computer-vision/object-detection/index.md)。
- **遷移學習。** DeiT-B 遷移到 CIFAR-10、Oxford Flowers 與 Stanford Cars 上，論文報告的準確率分別為 99.1%、98.4% 與 92.1%（Touvron et al., 2021）。

## 開放問題

- **架構的差距有多大？** ConvNeXt 認為，Transformer 所獲得的優勢，很大一部分應歸功於訓練配方與設計選擇，而非注意力本身（Liu et al., 2022）。Steiner et al.（2021）顯示訓練配方極為重要。這個問題尚未定論。
- **規模能否取代偏誤？** Zhai et al.（2021）指出，在他們嘗試的各種規模下，ViT 的表現並未飽和。在最大規模下，偏誤是否仍有幫助，尚不清楚。
- **類人性是真實的嗎？** Tuli et al.（2021）與 Naseer et al.（2021）發現，ViT 在某些指標上的行為更接近人類。這究竟反映了基於形狀的推理，還是另一組不同的捷徑，仍有待釐清。
- **高解析度下的成本。** 對所有區塊的全域注意力仍與 token 數的平方成正比。像 Swin 這樣的視窗式設計，以部分全域感受野換取線性成本。

## 參考文獻

### 開創性論文

- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv；ICLR 2021. https://arxiv.org/abs/2010.11929 — 提出視覺 Transformer，即直接套用於影像區塊的原始 Transformer，並報告其預訓練結果。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — ViT 幾乎完整沿用的 Transformer 編碼器。
- Touvron, H., et al. (2020). *Training data-efficient image transformers & distillation through attention*. arXiv；ICML 2021. https://arxiv.org/abs/2012.12877 — 只用 ImageNet-1K，搭配強資料增強與蒸餾 token 訓練 ViT。
- Liu, Z., et al. (2021). *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*. arXiv；ICCV 2021. https://arxiv.org/abs/2103.14030 — 具有移位局部視窗注意力的階層式視覺 Transformer，作為通用骨幹網路使用。
- He, K., et al. (2016). *Deep Residual Learning for Image Recognition*. arXiv；CVPR 2016. https://arxiv.org/abs/1512.03385 — 殘差 CNN，是 ViT 在資料規模實驗中最常被比較的對象。
- Sun, C., et al. (2017). *Revisiting Unreasonable Effectiveness of Data in Deep Learning Era*. arXiv. https://arxiv.org/abs/1707.02968 — 研究視覺表現如何隨訓練資料量成長，使用的是 JFT-300M 資料集。
- Yamins, D. L. K., et al. (2014). Performance-optimized hierarchical models predict neural responses in higher visual cortex. *PNAS*. https://doi.org/10.1073/pnas.1403112111 — 顯示為物件辨識最佳化的階層式網路能預測 IT 皮質的反應，是腦部連結的基礎。
- Geirhos, R., et al. (2019). *ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness*. arXiv；ICLR 2019. https://arxiv.org/abs/1811.12231 — 顯示以 ImageNet 訓練的 CNN 主要依賴紋理，而針對形狀的訓練能提升穩健性。

### 綜述與教科書

- Khan, S., et al. (2021). *Transformers in Vision: A Survey*. arXiv. https://arxiv.org/abs/2101.01169 — 綜述 Transformer 模型在辨識、生成、影片與 3D 視覺中的應用，並列出開放方向。

### 文章與文件

- Steiner, A., et al. (2021). *How to train your ViT? Data, Augmentation, and Regularization in Vision Transformers*. arXiv. https://arxiv.org/abs/2106.10270 — 一項受控研究，顯示資料增強與運算量能與較大的預訓練資料集相抗衡。
- Zhai, X., et al. (2021). *Scaling Vision Transformers*. arXiv. https://arxiv.org/abs/2106.04560 — 測量 ViT 的誤差如何隨資料與運算量下降，並訓練一個二十億參數的 ViT。
- Cordonnier, J.-B., et al. (2020). *On the Relationship between Self-Attention and Convolutional Layers*. arXiv. https://arxiv.org/abs/1911.03584 — 證明多頭自注意力可以表達任何卷積，並顯示訓練後的注意力常會學會這麼做。
- Liu, Z., et al. (2022). *A ConvNet for the 2020s*. arXiv；CVPR 2022. https://arxiv.org/abs/2201.03545 — ConvNeXt，一個現代化的 CNN，在相近成本下與 Swin Transformer 相當或更好。
- Naseer, M., et al. (2021). *Intriguing Properties of Vision Transformers*. arXiv. https://arxiv.org/abs/2105.10497 — 顯示 ViT 對遮擋具有穩健性，且比 CNN 更不依賴紋理。
- Tuli, S., et al. (2021). *Are Convolutional Neural Networks or Transformers more like human vision?* arXiv. https://arxiv.org/abs/2105.07197 — 比較 CNN 與 ViT 的錯誤模式和人類在影像辨識上的錯誤模式。
- He, K., et al. (2021). *Masked Autoencoders Are Scalable Vision Learners*. arXiv；CVPR 2022. https://arxiv.org/abs/2111.06377 — 為 ViT 設計的遮罩區塊自監督方法，僅用 ImageNet-1K 資料即可達到很高的準確率。
