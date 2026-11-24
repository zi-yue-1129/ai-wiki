---
translation_reviewed: 2026-11-22
---

# CLIP

CLIP（Contrastive Language–Image Pre-training）學習影像與文字編碼器，使兩者共享嵌入空間。它以四億組網路圖文配對預訓練，之後可藉類別文字描述進行分類，不需針對下游任務的標註資料微調。此處**零樣本**描述的是適應流程，不保證網路預訓練資料中完全沒有重疊影像。父頁[嵌入與表徵學習](index.md)將它歸於跨模態對齊。

## 問題

以 ImageNet 等固定標籤集合訓練的分類器，輸出類別受訓練標籤限制。Radford 等人（2021）研究能否利用網路上影像伴隨的自然語言，學習更廣泛的視覺概念，再以文字描述新任務。

## 核心概念

每批包含 $N$ 組圖文配對。正規化後的嵌入構成 $N\times N$ 個相似度；對比損失讓真正配對的圖文相較批次其他配對更具優勢。非配對項作為負例，即使其中有些也可能在語義上相容。影像找文字與文字找影像兩個方向共同構成對稱目標。

負例直接來自批次，不需另建負例集合。相似度乘上可學習的反溫度。arXiv 論文第 2.5 節記載初始溫度為 0.07，並把乘在 logits 上的尺度限制在不超過 100，以穩定訓練。[^training]

## 方程與演算法

令每列均為單位向量的影像、文字嵌入矩陣為 $I_e,T_e\in\mathbb R^{N\times d}$，則

$$
S=I_eT_e^\top\exp(t)=I_eT_e^\top/\tau,\qquad t=\log(1/\tau).
$$

### 以配對位置作為訓練目標

因此 $t$ 是可學習的**反溫度對數**，也就是 logit scale。令 $S_{ij}$ 表示影像 $i$ 與文字 $j$ 的分數，並把配對樣本放在相同索引位置。兩個方向的交叉熵為[^training]

$$
L_{I\to T}=-\frac{1}{N}\sum_{i=1}^{N}\log\frac{\exp(S_{ii})}{\sum_{j=1}^{N}\exp(S_{ij})},
$$

$$
L_{T\to I}=-\frac{1}{N}\sum_{i=1}^{N}\log\frac{\exp(S_{ii})}{\sum_{j=1}^{N}\exp(S_{ji})},
\qquad L=\frac{L_{I\to T}+L_{T\to I}}{2}.
$$

第一個分母固定影像，遍歷該列的文字。第二個固定文字，遍歷該欄的影像。目標是配對的**批次位置**，因此另一位置即使包含重複或語義相容的描述，在此目標中仍與正確位置競爭。對稱損失表示平均兩個方向，並不要求 $S=S^\top$ 或兩個方向損失相等。

### 兩組配對的例子

取單位影像向量 $(1,0)$、$(0.6,0.8)$，單位文字向量 $(1,0)$、$(0,1)$，反溫度 $\exp(t)=2$。得到的 logit 矩陣為

$$
S=\begin{pmatrix}2&0\\1.2&1.6\end{pmatrix}.
$$

代入前述公式，可得以下結果，四捨五入至小數點後四位。

| 量 | 影像找文字，沿列 softmax | 文字找影像，沿欄 softmax |
|---|---|---|
| 第一組配對位置的機率 | 0.8808 | 0.6900 |
| 第二組配對位置的機率 | 0.5987 | 0.8320 |
| 平均負對數機率 | 0.3200 | 0.2775 |

使用自然對數，平均損失為 $L\approx0.2987$。這些是為了展示計算而建構的數值，不是已訓練 CLIP 模型的量測。

### 零樣本分類與提示集成

給定候選類別集合 $C$，為每類編碼文字提示，再將嵌入正規化為 $v_c$。令 $u$ 為單位影像嵌入，零樣本分類器使用[^transfer]

$$
p_C(c\mid u)=\frac{\exp\!\left(\exp(t)u^\top v_c\right)}
{\sum_{k\in C}\exp\!\left(\exp(t)u^\top v_k\right)}.
$$

預測取此分數最大的類別。固定嵌入並共用正的反溫度時，餘弦相似度、縮放後的 logits 與 softmax 排序相同。改變尺度會改變機率，但不改變此排序。

提示用字會改變 $v_c$，因此也可能改變排序。論文第 3.1.4 節指出，預設提示「A photo of a {label}.」相較直接使用類別名稱，使 ImageNet 準確率增加約 1.3 個百分點。集成 80 種提示再增加約 3.5 個百分點。[^transfer] 官方範例先正規化每個提示的嵌入，對每類的嵌入取平均，再將平均向量正規化為一個類別向量。[^ensemble]

分母也依賴候選清單。另取一個建構例子，logits $(2,0)$ 給第一類的機率為 $0.8808$。加入 logit 為 $2$ 的第三類後，第一類機率降為 $0.4683$，原先兩個 logits 完全不變。若改為把原本兩個 logits 加倍成 $(4,0)$，第一類機率則升為 $0.9820$。只有一個候選時，softmax 必定回傳 $1$。因此，高 softmax 分數本身不能證明候選清單包含正確類別，也不能證明信心程度已針對目標任務校準。模型卡記載了類別設計對表現的影響，並要求針對特定類別體系進行測試。[^taxonomy]

## 結果

**ViT-L/14@336px** 的 ImageNet 零樣本 top-1 準確率為 **76.2%**，較早 Visual N-Grams 方法為 11.5%（[原論文表 1 與第 2.5 節](https://arxiv.org/abs/2103.00020)）。作者將其描述為與原始監督式 ResNet-50 相當，不是與後來最強的 ImageNet 系統相當。提示工程與集成合計帶來接近五個百分點的提升。訓練使用作者建立的 WIT（WebImageText）四億組圖文資料。

## 限制

- **不是全面最佳**：零樣本 CLIP 在許多資料集上可與簡單監督式基準比較，但非所有任務最佳。作者外推當時的規模趨勢，估計若要達到 2021 年 ImageNet 最佳水準，可能需要約千倍計算量；這不是已完成的實驗。
- **專門與抽象任務**：細粒度表現差異很大：Flowers102 與 FGVCAircraft 落後論文的 ResNet-50 特徵線性分類器，但 Stanford Cars 與 Food101 優於該基準（第 3.1.5 節）。計數、最近汽車距離等抽象或新任務可能接近隨機猜測；不能據此說所有細粒度分類都接近隨機。
- **分布差異**：MNIST 手寫數字準確率約 88%，低於直接使用像素的邏輯斯迴歸。
- **候選集合限制**：分類時只能在給定文字概念中選擇，不像影像描述模型能直接生成新句子。
- **社會偏差**：網路圖文會帶入社會偏差。
- **評估限制**：開發過程多次使用驗證集，評估任務集合也與模型開發共同調整。

[^training]: Radford 等人（2021），arXiv 第 2.3、2.5 節與圖 3，說明投影後正規化的嵌入、對角線批次目標、對稱交叉熵與 logit 尺度。
[^transfer]: Radford 等人（2021），arXiv 第 3.1.2 與 3.1.4 節，說明零樣本分類器及在嵌入空間進行的提示集成。
[^ensemble]: OpenAI，*Prompt Engineering for ImageNet*，下列官方筆記本的 `zeroshot_classifier` 函式。
[^taxonomy]: OpenAI，*Model Card: CLIP* 的「Out-of-Scope Use Cases」與「Bias and Fairness」。前述候選集合與尺度數例由 softmax 直接計算。

## 參考資料

### 奠基論文

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. & Sutskever, I. (2021). *Learning Transferable Visual Models From Natural Language Supervision*. arXiv. https://arxiv.org/abs/2103.00020 — 定義對比預訓練、WIT 與零樣本評估。
- Oord, A. van den, Li, Y. & Vinyals, O. (2018). *Representation Learning with Contrastive Predictive Coding*. arXiv. https://arxiv.org/abs/1807.03748 — 以負例建立對比預測編碼目標。

### 綜述與教科書

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — 學習表示與下游遷移的背景。

### 文章與文件

- Khosla, P. et al. (2020). *Supervised Contrastive Learning*. arXiv. https://arxiv.org/abs/2004.11362 — 以標籤建立批次對比目標。
- Wang, T. & Isola, P. (2020). *Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere*. arXiv. https://arxiv.org/abs/2005.10242 — 分析正規化表示的對齊與均勻性。
- OpenAI. *Prompt Engineering for ImageNet*. https://github.com/openai/CLIP/blob/main/notebooks/Prompt_Engineering_for_ImageNet.ipynb — 官方範例展示每個提示的正規化、取平均與類別向量的再次正規化。
- OpenAI. *Model Card: CLIP*. https://github.com/openai/CLIP/blob/main/model-card.md — 記載預期用途、限制與候選類別體系對結果的影響。
