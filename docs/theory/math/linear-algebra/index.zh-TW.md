---
translation_reviewed: 2026-10-28
---

# AI 的線性代數

線性代數研究向量、矩陣，以及它們之間的線性映射。AI 系統用它來儲存資料、權重與中間激活值，模型所執行的大部分運算都是矩陣運算。

## 概述

神經網路的核心是一長串矩陣乘法，中間穿插簡單的非線性函數。一個全連接層把輸入向量 $x$ 映射為 $h = \sigma(Wx + b)$，其中 $W$ 是學習得到的權重矩陣，$\sigma$ 是逐元素的非線性函數。影像、句子與感測器記錄都是數字陣列，比較兩者通常就是計算內積或距離。整個領域反覆用到一小組概念：內積衡量相似度，矩陣表示線性映射，矩陣分解則揭示資料或模型變化最大的方向。

線性代數也是 AI 與古典數值計算的交會處。加速器就是為了快速做大型矩陣乘法而設計的，因此模型的成本很大程度上就是其矩陣乘積的成本。本頁深入說明 [AI 的數學基礎](../index.md)概述中最大的一塊。

## 核心概念

- **向量**：有順序的一串數字，$x \in \mathbb{R}^d$。它可以是特徵向量、詞嵌入，或某一瞬間一群神經元的活動。
- **矩陣與張量**：二維的數字陣列，以及其高維推廣。做乘法時形狀必須吻合：$A \in \mathbb{R}^{m\times n}$ 乘以 $B \in \mathbb{R}^{n\times p}$ 得到 $m\times p$ 的矩陣。
- **內積與餘弦相似度**：$a^\top b$ 衡量兩個向量的對齊程度。餘弦 $\cos\theta = \frac{a^\top b}{\lVert a\rVert\,\lVert b\rVert}$ 則消除了長度的影響。
- **範數**：衡量向量大小的函數。常用的是歐氏（$\ell_2$）範數 $\lVert x\rVert_2 = \sqrt{\sum_i x_i^2}$ 與 $\ell_1$ 範數 $\sum_i |x_i|$。範數也定義了[嶺迴歸與 lasso](../../paradigms/supervised/linear-models/index.md)的懲罰項。
- **秩**：矩陣中線性獨立的行（或列）的數目，也是其輸出空間的維度。秩為 $r$ 的矩陣可以寫成兩個較瘦矩陣的乘積，其內部維度為 $r$。Strang（1993）以淺顯的方式說明秩如何組織矩陣的四個基本子空間。
- **特徵向量與特徵值**：非零向量 $v$ 與純量 $\lambda$，滿足 $Av = \lambda v$。對稱矩陣的特徵值為實數，且其特徵向量可以組成一組正交單位向量。
- **奇異值分解（SVD）**：每個實矩陣都可分解為 $A = U\Sigma V^\top$，其中 $U$ 與 $V$ 的行向量為正交單位向量，$\Sigma$ 的對角線上是非負的奇異值 $\sigma_1 \ge \sigma_2 \ge \cdots$。Golub 與 Kahan（1965）提出了計算它的穩定演算法。
- **投影**：滿足 $P^2 = P$ 的線性映射 $P$，會把向量映到某個子空間上。若 $Q$ 的行向量為正交單位向量，則 $QQ^\top$ 是到其張成空間的正交投影。

## 運作方式

**層即矩陣乘積。** 若某一層接收 $n$ 個輸入並有 $m$ 個單元，其權重矩陣形狀為 $m \times n$。把一批輸入堆疊為矩陣的各列後，整層就是一次矩陣乘積。這就是訓練主要由大型矩陣乘法組成的原因。

**以內積衡量相似度。** 嵌入模型把項目放進向量空間，使相關的項目有較大的餘弦相似度。從文本學得的詞向量具有這種性質，Mikolov 等人（2013）在大規模資料上展示了這一點。[Transformer](../../models/transformer/index.md) 的注意力機制則建立在同樣的運算之上：每個查詢與每個鍵做內積，分數經縮放並以 softmax 正規化，最後用來加權並求和各個值（Vaswani 等人，2017）。

**協方差矩陣的特徵分解。** 對已中心化的資料 $X \in \mathbb{R}^{n\times d}$，協方差矩陣為 $C = \frac{1}{n}X^\top X$。它是對稱且半正定的，因此具有一組正交的特徵基底。對應最大特徵值的特徵向量指向變異最大的方向。[主成分分析](pca/index.md)便是建立在這一事實之上。

**截斷 SVD 與最佳低秩近似。** 只保留最大的 $k$ 個奇異值，得到

$$
A_k = \sum_{i=1}^{k} \sigma_i\, u_i v_i^\top .
$$

Eckart–Young 定理指出，就 Frobenius 範數而言，$A_k$ 是與 $A$ 最接近的秩至多為 $k$ 的矩陣，其平方誤差為 $\lVert A - A_k\rVert_F^2 = \sum_{i>k}\sigma_i^2$，即被捨棄的奇異值平方和（Eckart 與 Young，1936）。這就是[截斷 SVD](truncated-svd/index.md) 方法的基礎。

```mermaid
flowchart LR
  W["權重矩陣 W（m × n）"] --> S["SVD：W = U Σ Vᵀ"]
  S --> T["保留最大的 k 個 σᵢ"]
  T --> F["因子 U_k、Σ_k、V_kᵀ"]
  F --> C["約 k(m + n) 個數字，取代 mn 個"]
```

## 關鍵方法

有三個里程碑式的方法涵蓋了實務上大部分的內容，每個方法都有自己的頁面。

| 方法 | 計算什麼 | 出現的地方 |
|---|---|---|
| [截斷 SVD（Eckart–Young）](truncated-svd/index.md) | 矩陣的最佳秩 $k$ 近似 | 壓縮權重、低秩分解、LoRA 背後的想法 |
| [主成分分析](pca/index.md) | 變異最大的正交方向，來自協方差矩陣的特徵向量或資料的 SVD | 降維、視覺化、特徵臉、神經群體活動分析 |
| [隨機化 SVD](randomized-svd/index.md) | 透過投影到隨機子空間，計算近似的截斷 SVD | 非常大的矩陣，精確 SVD 成本過高時 |

## 關聯

- **神經網路。** 每一層都是矩陣乘積，通過它的反向傳播會把梯度乘上權重矩陣的轉置。驅動[自動微分](../automatic-differentiation/index.md)的連鎖律因此是在線性代數上運作的。[深度學習](../../deep-learning/index.md)頁說明這些層如何堆疊。
- **注意力。** 注意力分數是查詢與鍵之間的內積，因此查詢空間與鍵空間的幾何結構決定了模型注意什麼。架構請見 [Attention Is All You Need](../../models/transformer/attention-is-all-you-need/index.md) 頁。
- **降維與表徵。** PCA 是線性的降維方法，屬於包括非線性方法在內的家族，而[自編碼器](../../paradigms/unsupervised/autoencoders-and-representations/index.md)學習的是同一想法的非線性推廣。[降維](../../paradigms/unsupervised/dimensionality-reduction/index.md)頁比較了這些方法。
- **壓縮。** 近似低秩的權重矩陣可以用兩個較瘦的因子取代，這是[模型壓縮](../../model-compression/index.md)的策略之一。[LoRA 與 QLoRA](../../../engineering/training/peft-lora.md) 在微調時對凍結的模型套用低秩更新；[向量資料庫](../../../engineering/vector-databases/index.md)則以內積與近似最近鄰搜尋，大規模地檢索嵌入。
- **腦與心智。** 記錄到的神經群體活動是一個矩陣，一軸是神經元，另一軸是時間或條件。對運動皮質的研究常用少數幾個主成分來描述這些活動（Churchland 等人，2012；Gallego 等人，2017）。表徵相似度分析（representational similarity analysis）則透過成對相異度的矩陣，比較大腦與模型的表徵（Kriegeskorte，2008）。請見[稀疏編碼](../../../brain-mind/computational-neuroscience/sparse-coding/index.md)與 [NeuroAI](../../../brain-mind/neuroai/index.md)。

## 應用

- **語意搜尋與檢索。** 文件與查詢被嵌入為向量，並以餘弦相似度或內積排序。FAISS 等函式庫即在大規模資料上執行這類運算。
- **模型壓縮與微調。** 低秩分解可縮小一層的參數量，低秩更新則讓微調更便宜。Hu 等人（2021）依其摘要報告，相較於以 Adam 做的全參數微調，LoRA 在 GPT-3 175B 上可將可訓練參數減少為 1/10,000。
- **視覺化與前處理。** 把資料投影到前兩或前三個主成分，是檢視資料集的常用第一步。Sirovich 與 Kirby（1987）以及 Turk 與 Pentland（1991）用同樣的投影來表示人臉。

## 未解問題

- **權重與激活值的低秩結構是否來自正確的原因？** 訓練後的網路常有快速衰減的奇異值，但要達到某個準確度需要多少這種結構，取決於層與任務。
- **低秩適應為何有效？** LoRA 把權重更新限制在低秩子空間中，仍能在多個基準上與全參數微調相當（Hu 等人，2021）。哪些方向必須改變，目前仍缺乏完整的解釋。
- **線性座標與非線性特徵。** PCA 與 SVD 假設有用的結構是線性的。深度自編碼器找到的非線性表徵（Hinton 與 Salakhutdinov，2006）可能更精簡，但較難分析。
- **神經群體的結構反映的是大腦還是分析方法？** 答案取決於前處理方式與所用的降維方法。

## 參考文獻

### 開創性論文

- Eckart, C. & Young, G.（1936）. The Approximation of One Matrix by Another of Lower Rank. *Psychometrika*. https://doi.org/10.1007/BF02288367 — 說明如何找到與某矩陣最接近的低秩矩陣，是截斷 SVD 的基礎。
- Pearson, K.（1901）. LIII. On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*. https://doi.org/10.1080/14786440109462720 — 找出與一團點最吻合的直線與平面，是主成分分析的幾何起源。
- Hotelling, H.（1933）. Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*. https://doi.org/10.1037/h0071325 — 把主成分定義為變異最大、彼此不相關的變數連續組合。
- Golub, G. & Kahan, W.（1965）. Calculating the Singular Values and Pseudo-Inverse of a Matrix. *Journal of the Society for Industrial and Applied Mathematics Series B Numerical Analysis*. https://doi.org/10.1137/0702016 — 提出穩定的演算法：先把矩陣化為雙對角形式，再將其對角化。
- Vaswani, A. 等人（2017）. Attention Is All You Need. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，其注意力層完全由查詢與鍵之間的內積建構。
- Mikolov, T. 等人（2013）. Efficient Estimation of Word Representations in Vector Space. https://arxiv.org/abs/1301.3781 — 從大型語料中學習連續的詞向量，向量空間中的相似度反映詞語的相似程度。
- Hinton, G. E. & Salakhutdinov, R. R.（2006）. Reducing the Dimensionality of Data with Neural Networks. *Science*. https://doi.org/10.1126/science.1127647 — 訓練深度自編碼器，其低維編碼依摘要所述，效果優於主成分分析。
- Hu, E. J. 等人（2021）. LoRA: Low-Rank Adaptation of Large Language Models. https://arxiv.org/abs/2106.09685 — 在凍結的預訓練權重上訓練低秩更新矩陣，以降低微調成本。
- Turk, M. & Pentland, A.（1991）. Eigenfaces for Recognition. *Journal of Cognitive Neuroscience*. https://doi.org/10.1162/jocn.1991.3.1.71 — 描述一套人臉辨識系統，把影像投影到作者所稱的特徵臉（人臉影像的主成分）上。
- Churchland, M. M. 等人（2012）. Neural population dynamics during reaching. *Nature*. https://doi.org/10.1038/nature11129 — 以低維投影分析伸手動作期間的運動皮質群體活動。
- Gallego, J. A. 等人（2017）. Neural Manifolds for the Control of Movement. *Neuron*. https://doi.org/10.1016/j.neuron.2017.05.025 — 主張與動作相關的群體活動可以用低維神經流形來描述。
- Kriegeskorte, N.（2008）. Representational similarity analysis – connecting the branches of systems neuroscience. *Frontiers in Systems Neuroscience*. https://doi.org/10.3389/neuro.06.004.2008 — 透過成對相異度的矩陣，比較大腦與模型的表徵。

### 綜述與教科書

- Kolda, T. G. & Bader, B. W.（2009）. Tensor Decompositions and Applications. *SIAM Review*. https://doi.org/10.1137/07070111X — 綜述高階張量分解，並將其視為矩陣 SVD 與 PCA 的延伸。
- Strang, G.（1993）. The Fundamental Theorem of Linear Algebra. *The American Mathematical Monthly*. https://doi.org/10.2307/2324660 — 以說明性文章介紹矩陣的四個基本子空間及其相互關係。
- Martinsson, P.-G. & Tropp, J. A.（2020）. Randomized numerical linear algebra: Foundations and algorithms. *Acta Numerica*. https://doi.org/10.1017/S0962492920000021 — 綜述機率演算法，涵蓋低秩近似、子空間迭代與誤差估計。
