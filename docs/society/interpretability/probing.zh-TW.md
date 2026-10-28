---
translation_reviewed: 2026-10-28
---

# 探測分類器與表徵分析

探測是訓練一個簡單的監督式模型，從網路的內部激活中讀出某種性質。表徵分析則是把這些激活拿來比較，比較的對象可以是不同的網路、不同的任務，也可以是大腦。兩者問的都是某個表徵包含了什麼資訊，這與網路是否真的使用了這些資訊並不相同。

## 概述

**探測器（probe）**是一個小型分類器，它在凍結的激活上訓練，用來預測輸入的某種性質，例如一個詞的詞性、一句陳述是否為真，或一盤棋局的狀態。若探測器成功，代表該性質可以從表徵中還原出來。Alain 與 Bengio（2016）以現代的形式提出這個方法，他們在影像模型的每一層上訓練線性分類器，發現特徵的線性可分性隨深度增加。在自然語言處理中，Tenney 等人（2019）利用探測器顯示 BERT 各層以預期的順序編碼了古典 NLP 流程的各個階段。

表徵分析是更廣泛的一族方法。它問的是兩個表徵有多相似、兩個網路對同一組刺激的排列是否一致，以及某個網路的表徵是否與大腦吻合。這些工具支撐了 [NeuroAI](../../brain-mind/neuroai/index.md) 中的比較研究。

## 核心概念

- **探測器（probe）**：在凍結激活上訓練的監督式模型，用來預測外部標籤。只有探測器的參數被擬合，網路本身不變。
- **線性探測器（linear probe）**：激活的線性函數（或邏輯函數）。這項限制約束了探測器自行學習的能力，因此高分是關於表徵的證據。這是否是正確的限制，仍有爭議。
- **控制任務（control task）**：對每種輸入類型隨機指定、但固定的標籤，只能靠記憶來預測。Hewitt 與 Liang（2019）以它衡量**選擇性（selectivity）**，即真實任務的準確率減去控制任務的準確率。
- **表徵相似性矩陣（representational similarity matrix）**：一組刺激的反應兩兩之間相似度所組成的矩陣。RSA 比較的就是這些矩陣，因此單元數不同的系統也能互相比較。
- **線性表徵假說（linear representation hypothesis）**：高層次概念以激活空間中的方向來表示，因此可以用投影讀出，也可以沿著該方向移動來改變它（Park 等人，2023）。

## 運作方式

一項探測研究遵循固定的步驟：

1. 選定一個層與一個有標籤的資料集。
2. 執行凍結的網路，並記錄該層的激活。
3. 在一個切分上訓練探測器來預測標籤，通常使用邏輯迴歸。
4. 在保留的資料上評估，並與基線比較，例如隨機初始化網路上的探測器。
5. 對每一層重複。依深度繪出的準確率曲線，會顯示該性質出現在哪裡。

```mermaid
flowchart LR
    A[凍結的網路<br/>各層激活] --> B[在有標籤切分上<br/>訓練探測器]
    B --> C[保留資料上的準確率]
    C --> D[與控制任務與基線比較]
    D --> E[解釋：資訊存在，<br/>但不一定被使用]
```

對於選定層的激活 $h(x) \in \mathbb{R}^d$，線性探測器輸出 $\hat{y} = \mathrm{softmax}(W h(x) + b)$，其中 $W$ 與 $b$ 以交叉熵擬合。選擇性為

$$\mathrm{Sel} = \mathrm{Acc}_{\text{task}} - \mathrm{Acc}_{\text{control}},$$

兩者使用相同的探測器族與訓練預算。

RSA 與 CKA 比較的是表徵，而不是預測標籤。RSA 對同一組刺激，計算兩個系統相似性矩陣之間的等級相關（Kriegeskorte，2008）。線性中心化核對齊（CKA）比較兩個中心化的激活矩陣 $X$ 與 $Y$，每一列對應一個刺激：

$$\mathrm{CKA}(X, Y) = \frac{\lVert Y^{\top} X \rVert_F^2}{\lVert X^{\top} X \rVert_F \, \lVert Y^{\top} Y \rVert_F}.$$

對任一表徵作旋轉或均勻縮放，其值都不會改變（Kornblith 等人，2019）。

## 關鍵方法

| 變體 | 想法 | 主要注意事項 |
|---|---|---|
| 線性探測器（Alain & Bengio, 2016） | 在某一層上擬合線性分類器 | 準確率顯示的是可解碼性，而非被使用 |
| 控制任務探測器（Hewitt & Liang, 2019） | 比較任務準確率與隨機控制的準確率 | 選擇性取決於探測器族及其預算 |
| 資訊理論探測（Pimentel 等人，2020） | 估計表徵與性質之間的互資訊 | 估計值取決於探測器；作者主張採用表現最好的探測器 |
| RSA（Kriegeskorte, 2008） | 關聯兩個系統在相同刺激上的相似性矩陣 | 取決於刺激集與相似度量 |
| 線性 CKA（Kornblith 等人，2019） | 經正規化的相似度，對旋轉與縮放不變 | 只給出一個數值，不說明哪些特徵相互對應 |
| 線性表徵檢驗（Park 等人，2023；Marks & Tegmark, 2023） | 找出概念方向，再檢驗它能否讀出概念並能否引導行為 | 方向取決於如何從資料定義概念 |

## 連結

- 上層概述 [可解釋性](index.md) 涵蓋歸因與機械式研究。探測位於兩者之間：它問的是表徵包含了什麼，而其他兩者問的是什麼驅動了輸出。
- [機械式可解釋性與電路](mechanistic-interpretability.md) 把探測列為眾多工具之一。它的因果測試（例如激活修補）補足了探測留下的缺口，也就是網路是否真的使用了這些資訊。
- [特徵歸因](feature-attribution.md) 問的是哪些輸入驅動了某一個輸出；探測問的則是某個內部激活攜帶了哪種性質。
- **大腦與心智。** 編碼模型與 RSA 把模型特徵與神經記錄聯繫起來，見 [NeuroAI](../../brain-mind/neuroai/index.md)。Yamins 等人（2014）顯示，為物件辨識最佳化的網路能預測高階視覺皮質的反應。在語言方面，[Goldstein 等人（2022）](../../brain-mind/language-in-brain/goldstein-2022/index.md) 比較語言模型的表徵與聽者的腦部記錄。神經科學也會解碼腦部活動，這正是把探測應用在大腦上；Kriegeskorte 與 Diedrichsen（2019）則提醒，把腦部活動解讀為表徵需要審慎論證。
- **模型與訓練。** 探測是 [Transformers 與注意力機制](../../theory/models/transformer/index.md) 與 [NLP](../../theory/models/nlp/index.md) 系統的常規做法。探測器本身就是建立在凍結特徵上的一般[線性模型](../../theory/paradigms/supervised/linear-models/index.md)。線性探測也是評估[自監督](../../theory/paradigms/self-supervised/index.md)編碼器的標準方法。

## 應用

- **語言結構。** Tenney 等人（2019）在 BERT 的各層中找到了 NLP 流程的各個階段。
- **世界模型。** Li 等人（2022）在一個以 Othello 棋步訓練的序列模型中，找到了棋盤狀態的表徵。對它進行介入會改變模型預測的棋步。
- **真假。** Marks 與 Tegmark（2023）在 LLM 激活中找到一個能區分真假陳述的方向。它能跨資料集遷移，沿該方向介入甚至能讓模型把假陳述當成真的。
- **模型與大腦的比較。** RSA 與編碼模型把網路各層與皮質區域進行比較。

## 開放問題

### 存在與使用

探測器可能在模型從未使用的資訊上成功。Ravichander 等人（2020）顯示，模型可以編碼其訓練任務並不需要的性質。Belinkov（2022）回顧了這項限制以及方法的其他局限。

### 探測器應該多強

Hewitt 與 Liang 以選擇性來評斷探測器，會懲罰那些在記憶的探測器。Pimentel 等人（2020）則主張，從資訊理論的角度看，表現最好的探測器能給出較佳的估計。兩種立場回答的是不同的問題，這個領域至今仍未決定哪一種量度才是正確的。

### 表徵是否為線性？

線性表徵假說與數個結果相符（Park 等人，2023；Marks & Tegmark, 2023），但 Othello 的棋盤表徵是非線性的（Li 等人，2022）。高層次概念是否普遍為線性，仍是開放問題。

### 哪一種相似度量？

RSA 與 CKA 對兩個表徵有多相似的判斷可能不一致。高相似度也不代表共享了計算方式，因為不同的機制可能產生相似的幾何結構。NeuroAI 中「可預測性不等於機制」的提醒，在這裡同樣適用。

## 參考文獻

### 開創性論文

- Alain, G. & Bengio, Y. (2016). *Understanding intermediate layers using linear classifier probes*. arXiv. https://arxiv.org/abs/1610.01644 — 在影像分類器的各層上引入線性探測器，顯示特徵的可分性隨深度增加。
- Hewitt, J. & Liang, P. (2019). *Designing and Interpreting Probes with Control Tasks*. EMNLP. https://arxiv.org/abs/1909.03368 — 引入控制任務與選擇性，把探測器的能力與表徵的內容區分開來。
- Tenney, I., Das, D. & Pavlick, E. (2019). *BERT Rediscovers the Classical NLP Pipeline*. ACL. https://arxiv.org/abs/1905.05950 — 逐層探測 BERT，發現古典 NLP 流程的各階段以預期的順序出現。
- Pimentel, T., Valvoda, J., Hall Maudslay, R., Zmigrod, R., Williams, A. & Cotterell, R. (2020). *Information-Theoretic Probing for Linguistic Structure*. ACL. https://arxiv.org/abs/2004.03061 — 把探測視為估計互資訊，並主張採用表現最好的探測器。
- Ravichander, A., Belinkov, Y. & Hovy, E. (2020). *Probing the Probing Paradigm: Does Probing Accuracy Entail Task Relevance?* arXiv. https://arxiv.org/abs/2005.00719 — 顯示模型可以編碼其訓練任務不需要的性質，因此探測準確率並不能證明模型使用了該資訊。
- Kriegeskorte, N. (2008). *Representational similarity analysis – connecting the branches of systems neuroscience*. Frontiers in Systems Neuroscience. https://doi.org/10.3389/neuro.06.004.2008 — 提出以相似性矩陣來比較系統，使大腦與模型能被直接比較。
- Kornblith, S., Norouzi, M., Lee, H. & Hinton, G. (2019). *Similarity of Neural Network Representations Revisited*. ICML. https://arxiv.org/abs/1905.00414 — 提出中心化核對齊作為跨網路比較表徵的相似度指標。
- Yamins, D. L. K., Hong, H., Cadieu, C. F., Solomon, E. A., Seibert, D. & DiCarlo, J. J. (2014). *Performance-optimized hierarchical models predict neural responses in higher visual cortex*. PNAS. https://doi.org/10.1073/pnas.1403112111 — 顯示為物件辨識最佳化的網路能預測 V4 與顳下皮質的反應。
- Li, K., Hopkins, A. K., Bau, D., Viégas, F., Pfister, H. & Wattenberg, M. (2022). *Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task*. arXiv. https://arxiv.org/abs/2210.13382 — 在以 Othello 棋步訓練的模型中找到非線性的棋盤狀態表徵，並可用於介入。
- Marks, S. & Tegmark, M. (2023). *The Geometry of Truth: Emergent Linear Structure in Large Language Model Representations of True/False Datasets*. arXiv. https://arxiv.org/abs/2310.06824 — 在 LLM 激活中找到線性的真假方向，它能跨資料集遷移，並可進行因果介入。
- Park, K., Choe, Y. J. & Veitch, V. (2023). *The Linear Representation Hypothesis and the Geometry of Large Language Models*. arXiv. https://arxiv.org/abs/2311.03658 — 形式化「概念在語言模型中以線性方式表示」的意義。

### 綜述與教科書

- Belinkov, Y. (2022). *Probing Classifiers: Promises, Shortcomings, and Advances*. Computational Linguistics. https://doi.org/10.1162/coli_a_00422 — 對探測分類器的批判性回顧，說明它能與不能證明什麼。
- Kriegeskorte, N. & Diedrichsen, J. (2019). *Peeling the Onion of Brain Representations*. Annual Review of Neuroscience. https://doi.org/10.1146/annurev-neuro-080317-061906 — 回顧如何把腦部活動詮釋為表徵，以及這樣做的困難。
