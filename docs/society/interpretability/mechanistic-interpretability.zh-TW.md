---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - transformers
aliases:
  - Mechanistic interpretability
  - Circuits
  - 機械式可解釋性
  - 電路
---

# 機械式可解釋性與電路

機械式可解釋性試圖對訓練好的神經網路所學到的演算法進行逆向工程。它不問哪些輸入驅動了某個輸出，而是問哪些內部元件計算哪些中間結果，以及它們如何組合。**電路**是一個小型子網路，由神經元、注意力頭以及它們之間的連結組成，實現某個可辨識的計算。這個領域的核心假設是：訓練好的網路結構足夠清楚，使這類電路可以被找到並加以驗證。

## 概覽

像 LIME 或 SHAP 這類事後解釋方法（參見[可解釋性](index.md)）描述的是輸入與輸出的行為，而它們的解釋可能並不忠實。機械式可解釋性的目標是機制本身。一個好的機械式主張是因果性的、可檢驗的：如果移除或改動某個被認為支持某行為的元件，該行為應依預測的方式改變，而其他部分則不應有太大變化。

這個方法最早應用於視覺模型。Olah et al.（2020）描述卷積網路中的電路，例如由邊緣偵測器組合而成的曲線偵測器，並主張特徵及其連結可以用同樣的方式研究。在 Elhage et al.（2021）為 Transformer 電路提出數學框架之後，這個方法才延伸到語言模型。

## 核心概念

- **殘差流（residual stream）**：Transformer 中每一層讀取與寫入的激活向量。各元件透過讀寫殘差流來彼此溝通。
- **注意力頭（attention head）**：在不同 token 位置之間搬移資訊的元件。可以透過注意力模式，以及它寫入殘差流的內容來研究。
- **電路（circuit）**：執行特定計算的元件子圖。
- **因果介入（causal intervention）**：透過消融、修補或引導來改變激活，以檢驗某元件是否攜帶所主張的資訊。

## 主要發現

已有數個電路得到了良好的描述。

**歸納頭（induction heads）。** Olsson et al.（2022）找出一種完成重複序列的雙頭機制：一個頭記錄每個 token 前面是哪個 token，第二個頭則關注先前出現過的當前 token，並複製其後的 token。這個機制在訓練中的急劇轉變時出現，並與情境學習有關。論文把它視為一般機制的證據，但它與所有形式情境學習的關係仍是假說。

**事實回憶。** Meng et al.（2022）使用因果追蹤，顯示 GPT 類模型中的事實關聯是局部化的，主要位於主詞最後一個 token 的中層 MLP 模組。接著他們以名為 ROME 的方法，透過改動這些權重來編輯某個關聯。局部化的主張得到介入結果的支持，但編輯的結果描述的是被測試的事實，而不是所有事實。

**間接賓語識別。** Wang et al.（2022）在 GPT-2 small 中對一個電路進行逆向工程，這個電路能完成如「When John and Mary went to the store, John gave a drink to ___」這類句子。他們找出具有不同角色的注意力頭群組，例如偵測重複的名字並加以抑制，並以消融實驗檢驗所提出的電路。這是針對語言模型最完整的電路分析之一，但它只涵蓋一個小模型與一項任務。

**頓悟（grokking）。** Nanda et al.（2023）對一個小型 Transformer 學習模加法的過程進行逆向工程。在長時間延遲後才出現泛化，他們顯示網路逐步建立一個週期性的演算法，這可以用進展度量在測試準確率上升之前就測得。

## 疊加

具有 $d$ 個神經元的網路，如果把特徵儲存為近似正交、很少同時出現的方向，就能表示遠多於 $d$ 個特徵。Elhage et al.（2022）在小型玩具模型中研究這點，顯示網路會在表示的特徵數量與可接受的干擾之間取捨，因此單一神經元會對多個不相關的特徵產生反應。這就是**多義性（polysemanticity）**。疊加解釋了為何神經元通常難以逐一解讀，也促成了[稀疏自編碼器](sparse-autoencoders.md)的發展，後者試圖把特徵恢復為方向。

## 方法

- **激活修補（activation patching）**（Meng et al., 2022；Wang et al., 2022）：以另一次執行的激活取代某些激活，以測試哪些元件攜帶某個結果。
- **路徑修補與電路發現**（Conmy et al., 2023）：自動搜尋電路的邊，其消融會最大程度改變行為，而不是手動檢查元件。
- **特徵分析**：把激活分解為特徵，通常使用稀疏自編碼器，並檢驗這些特徵是否被因果地使用。

## 相關連結

神經科學面臨同樣的問題：一個分散式系統如何運算。但神經科學家無法檢視每個單元，也無法設定每個權重。Jonas 與 Kording（2017）主張，即使在設計完全已知的微處理器上，標準的神經科學方法也會有困難，這對兩個領域都是警示。可解釋性也為神經科學提供類比，例如對某個概念調諧的單元，這在[計算神經科學](../../brain-mind/computational-neuroscience/index.md)中有所討論。關於 Transformer 架構的背景，見[Transformer](../../theory/models/transformer/index.md)。

## 應用

- 除錯：找出造成失效的電路（例如虛假相關），並加以移除。
- 稽核隱藏行為，這與[欺騙性對齊](../safety-alignment/deceptive-alignment.md)相關。
- 透過加入或移除與某概念相關的方向來引導行為。

## 開放問題

- 哪些電路是通用的，哪些只屬於某個模型或任務？
- 在小模型中找到的電路，能否在大數倍的模型中持續存在？
- 模型的行為有多少能被有限的一組電路解釋？
- 解釋對實際計算的忠實度如何？一個電路可能是有用的故事，卻不是完整的機制。

## 參考文獻

### 開創性論文

- Olah, C. et al. (2020). *Zoom In: An Introduction to Circuits*. Distill. https://doi.org/10.23915/distill.00024.001 — Argues that features and the connections between them in vision networks can be studied as circuits.
- Elhage, N. et al. (2021). *A Mathematical Framework for Transformer Circuits*. Transformer Circuits Thread. https://transformer-circuits.pub/2021/framework/index.html — Frames the attention and MLP components of small transformers as linear algebra on the residual stream.
- Elhage, N. et al. (2022). *Toy Models of Superposition*. Transformer Circuits Thread. https://transformer-circuits.pub/2022/toy_model/index.html — Studies how networks represent more features than they have neurons, using toy models.
- Olsson, C. et al. (2022). *In-context Learning and Induction Heads*. Transformer Circuits Thread. https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html — Identifies induction heads as a mechanism for copying sequences and links them to in-context learning.
- Meng, K. et al. (2022). *Locating and Editing Factual Associations in GPT*. NeurIPS 2022. https://arxiv.org/abs/2202.05262 — Uses causal tracing to localise factual recall and edits it by changing mid-layer weights.
- Wang, K. et al. (2022). *Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small*. arXiv:2211.00593. https://arxiv.org/abs/2211.00593 — Reverse-engineers a complete circuit for a language-understanding task in GPT-2 small.
- Nanda, N. et al. (2023). *Progress Measures for Grokking via Mechanistic Interpretability*. ICLR 2023. https://arxiv.org/abs/2301.05217 — Reverse-engineers the algorithm a small transformer learns for modular addition.

### 綜述與教科書

- Jonas, E. & Kording, K. P. (2017). *Could a Neuroscientist Understand a Microprocessor?* PLOS Computational Biology. https://doi.org/10.1371/journal.pcbi.1005268 — Shows that standard neuroscience analysis methods struggle to explain a microprocessor whose design is fully known.
- Conmy, A. et al. (2023). *Towards Automated Circuit Discovery for Mechanistic Interpretability*. NeurIPS 2023. https://arxiv.org/abs/2304.14997 — Automates the search for circuits by testing which edges matter for a behaviour.

### 文章與文件

- Olah, C. et al. *Transformer Circuits Thread*. https://transformer-circuits.pub/ — Ongoing series of mechanistic interpretability papers, including the primary sources above.

## 延伸學習

- [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) — 用於檢視與介入 Transformer 激活的開源函式庫。
