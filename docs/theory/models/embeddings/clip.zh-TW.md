---
translation_reviewed: 2026-11-18
---

# CLIP

CLIP（Contrastive Language–Image Pre-training）學習影像與文字編碼器，使兩者共享嵌入空間。它以四億組網路圖文配對預訓練，之後可藉類別文字描述進行分類，不需針對下游任務的標註資料微調。此處**零樣本**描述的是適應流程，不保證網路預訓練資料中完全沒有重疊影像。父頁[嵌入與表徵學習](index.md)將它歸於跨模態對齊。

## 問題

以 ImageNet 等固定標籤集合訓練的分類器，輸出類別受訓練標籤限制。Radford 等人（2021）研究能否利用網路上影像伴隨的自然語言，學習更廣泛的視覺概念，再以文字描述新任務。

## 核心概念

每批包含 \(N\) 組圖文配對。正規化後的嵌入構成 \(N\times N\) 個相似度；對比損失讓真正配對的圖文相較批次其他配對更具優勢。非配對項作為負例，即使其中有些也可能在語義上相容。影像找文字與文字找影像兩個方向共同構成對稱目標。

負例直接來自批次，不需另建負例集合。相似度乘上可學習的反溫度。論文第 2.5 節記載初始溫度為 0.07，並把乘在 logits 上的尺度限制在不超過 100，以穩定訓練。

## 方程與演算法

令每列均為單位向量的影像、文字嵌入矩陣為 \(I_e,T_e\in\mathbb R^{N\times d}\)，則

\[
S=I_eT_e^\top\exp(t)=I_eT_e^\top/\tau,\qquad t=\log(1/\tau).
\]

所以 \(t\) 是**反溫度的對數**，也就是 logit scale，不是溫度本身的對數。對稱損失為 \(L=(L_{I\to T}+L_{T\to I})/2\)：前者讓每張影像在該批文字中選出配對文字，後者方向相反。

零樣本分類先把類別名稱放入文字提示並編碼，再將影像向量與各類別向量比較；以反溫度縮放後做 softmax，取最高分的類別。論文第 3.1.4 節指出，預設提示「A photo of a {label}」使 ImageNet 準確率增加約 1.3 個百分點，集成 80 種提示再增加約 3.5 個百分點。

## 結果

**ViT-L/14@336px** 的 ImageNet 零樣本 top-1 準確率為 **76.2%**，較早 Visual N-Grams 方法為 11.5%（[原論文表 1 與第 2.5 節](https://arxiv.org/abs/2103.00020)）。作者將其描述為與原始監督式 ResNet-50 相當，不是與後來最強的 ImageNet 系統相當。提示工程與集成合計帶來接近五個百分點的提升。訓練使用作者建立的 WIT（WebImageText）四億組圖文資料。

## 限制

- **不是全面最佳**：零樣本 CLIP 在許多資料集上可與簡單監督式基準比較，但非所有任務最佳。作者外推當時的規模趨勢，估計若要達到 2021 年 ImageNet 最佳水準，可能需要約千倍計算量；這不是已完成的實驗。
- **專門與抽象任務**：細粒度表現差異很大：Flowers102 與 FGVCAircraft 落後論文的 ResNet-50 特徵線性分類器，但 Stanford Cars 與 Food101 優於該基準（第 3.1.5 節）。計數、最近汽車距離等抽象或新任務可能接近隨機猜測；不能據此說所有細粒度分類都接近隨機。
- **分布差異**：MNIST 手寫數字準確率約 88%，低於直接使用像素的邏輯斯迴歸。
- **候選集合限制**：分類時只能在給定文字概念中選擇，不像影像描述模型能直接生成新句子。
- **社會偏差**：網路圖文會帶入社會偏差。
- **評估限制**：開發過程多次使用驗證集，評估任務集合也與模型開發共同調整。

## 參考資料

### 奠基論文

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. & Sutskever, I. (2021). *Learning Transferable Visual Models From Natural Language Supervision*. arXiv. https://arxiv.org/abs/2103.00020 — 定義對比預訓練、WIT 與零樣本評估。
- Oord, A. van den, Li, Y. & Vinyals, O. (2018). *Representation Learning with Contrastive Predictive Coding*. arXiv. https://arxiv.org/abs/1807.03748 — 以負例建立對比預測編碼目標。

### 綜述與教科書

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — 學習表示與下游遷移的背景。

### 文章與文件

- Khosla, P. et al. (2020). *Supervised Contrastive Learning*. arXiv. https://arxiv.org/abs/2004.11362 — 以標籤建立批次對比目標。
- Wang, T. & Isola, P. (2020). *Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere*. arXiv. https://arxiv.org/abs/2005.10242 — 分析正規化表示的對齊與均勻性。
