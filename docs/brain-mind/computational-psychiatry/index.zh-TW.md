---
translation_reviewed: 2026-10-28
related:
- brain-mind/decision-reward
- brain-mind/predictive-coding
- theory/paradigms/reinforcement-learning
tags:
- computational psychiatry
- psychiatry
- reinforcement learning
- machine learning
aliases:
  - 計算精神醫學
  - 計算精神病學
  - Computational psychiatry
  - Computational models of psychiatric symptoms
---

# 計算精神醫學

計算精神醫學以學習、決策與知覺的數學模型來描述精神症狀，並把症狀理解為背後的運算過程。這些模型是用來測量這些運算的研究工具，而不是診斷測驗。

本頁屬於[腦與心智](../index.md)。它介紹這個領域，並比較兩個代表性方法；這兩個方法各有獨立的頁面。

## 概述

精神症狀通常透過自我報告與臨床觀察來描述。這些描述在不同的人之間、以及同一個人的不同時期都差異很大，即使兩人有相同的症狀，也可能在許多方面不同。計算精神醫學探問，這些變異能否用少數幾個模型參數來捕捉。例子包括：一個人在出現意外後，更新預期的速度有多快；或者先前的信念，相對於雜訊較大的感官證據，有多大的分量。如果一個參數能從行為中估計出來，它就能在不同的人、群體與治療之間比較。

這個領域使用三類工具。強化學習（reinforcement learning, RL）模型描述選擇如何受獎勵與預測誤差塑造，也就是 [決策、多巴胺與獎勵](../decision-reward/index.md) 所討論的同一種更新。貝氏模型描述信念如何隨證據改變，以及先前的預期如何塑造知覺。機器學習方法在大型資料集中尋找模式，用來預測診斷或治療反應。

Huys、Maia 與 Frank（2016）把這個領域分為兩個互補的分支。資料驅動的方法把機器學習應用於高維資料，一般不去建模其機制。理論驅動的方法則建立編碼某種機制假設的模型。該綜述強調兩者結合的價值，並著重於臨床應用。

## 核心概念

- **計算表型（computational phenotype）**：從行為估計出的一組模型參數，總結一個人如何學習或決策。
- **內表型（endophenotype）**：與某種疾病相關、可測量的特質，可能在不同的人或不同疾病之間共享。
- **預測誤差（prediction error）**：實際發生的與預期的之間的差異。它在學習中的角色，見 [多巴胺的獎勵預測誤差](../neuroscience/dopamine-reward-prediction-error/index.md)，此處不再重複。
- **階層式模型（hierarchical model）**：個別參數取自共享的群體分布的模型，因此每個人的估計也參考了其他人的資料。

## 核心想法

該領域有三個反覆出現的想法。

第一，精神症狀可以視為沿著連續向度變化的現象，而不只是固定的類別。Wang 與 Krystal（2014）主張，計算模型能找出跨越多種疾病的核心缺陷，並能把細胞與迴路連結到行為。

第二，模型只有在與可檢驗的機制相連時才有用。學習模型對選擇以及追蹤學習的腦部訊號都會做出具體預測，兩者皆可檢驗。這也是該領域與 [神經影像與記錄方法](../neuroimaging-methods/index.md) 相互配合的原因。

第三，測量才是困難所在。模型參數是推論出來的，不是直接觀察到的，其意義取決於所用的模型。Wilson 與 Collins（2019）提供把模型與行為資料連結起來的實用規則，使結論有意義。

## 主要方法

每個方法都有自己的頁面。此列表僅作比較。

- [以階層式貝氏強化學習模型進行計算表型分析（Ahn 等人，2017）](computational-phenotyping/index.md)：為每個人的選擇擬合一個學習模型，同時估計群體層級的參數分布。它與單人擬合的差別在於，它會在人與人之間共享資訊。
- [精神病中的異常預測誤差（Corlett 等人，2007）](aberrant-prediction-error-psychosis/index.md)：從一個腦部訊號出發，探問它在有妄想信念的人身上是否失常。它與表型分析的差別在於，它檢驗的是一個神經機制，而不是一組行為參數。

這個領域中以機器學習進行診斷與治療預測的工作，在此沒有獨立的方法頁面，相關內容見「應用」一節。

## 與其他主題的關聯

- **強化學習**：多數表型分析所依據的模型類別，見[強化學習](../../theory/paradigms/reinforcement-learning/index.md)；這些模型所區分的控制器，見[有模型與無模型控制](../decision-reward/model-based-vs-model-free/index.md)。
- **預測編碼**：數種精神病理論把它視為預測的障礙。見[預測編碼與自由能](../predictive-coding/index.md)。
- **注意力**：異常顯著性的概念，即事件感覺比實際更重要，與[大腦與機器中的注意力](../attention-brain-machine/index.md)相關。
- **心理學**：選擇的人為面向，包括認知偏誤，見[心理學與 AI](../psychology/index.md)。
- **機率方法**：貝氏擬合使用的推論工具，與[機率方法](../../theory/paradigms/probabilistic/index.md)相同。

## 應用

- **研究性表型分析**：研究者把學習與決策模型擬合到行為上，並比較不同群體的參數。hBayesDM 套件讓這件事只需很少的程式碼即可完成（Ahn 等人，2017）。
- **從資料進行預測**：機器學習已被用來預測憂鬱症患者是否會對某種治療有反應。Chekroud 等人（2016）檢驗了這類預測是否能跨越不同的臨床試驗。
- **生物標記**：以腦部資料訓練的模型，正被評估為轉譯神經影像中的潛在生物標記（Woo 等人，2017）。這些仍是研究工具。

## 開放問題

- **參數是否穩定？**目前不清楚擬合出的參數在不同時間與不同任務間是否一致，以及它們能否預測症狀或治療反應。
- **共享還是特異？**Wang 與 Krystal 所提出、跨疾病共享缺陷的想法很有吸引力，但同一個模型族是否能適用於多種疾病，尚無定論。
- **預測能否推廣？**在某一樣本中有效的分類器，未必能轉移到其他診所、族群或試驗。
- **兩個分支如何結合？**Huys 等人（2016）強調結合資料驅動與理論驅動研究的價值，但最好的結合方式仍待釐清。

## 參考文獻

### 開創性論文

- Montague, P. R., Dolan, R. J., Friston, K. J. & Dayan, P.（2012）。Computational psychiatry。*Trends in Cognitive Sciences*。https://doi.org/10.1016/j.tics.2011.11.018 — 介紹計算精神醫學，把精神功能異常描述為異常的運算，並強調強化學習與賽局理論的研究。
- Chekroud, A. M. 等人（2016）。Cross-trial prediction of treatment outcome in depression: a machine learning approach。*The Lancet Psychiatry*。https://doi.org/10.1016/S2215-0366(15)00471-X — 以一項試驗訓練機器學習模型來預測憂鬱症的治療結果，並在另一項獨立試驗中檢驗。
- Ahn, W.-Y., Haines, N. & Zhang, L.（2017）。Revealing Neurocomputational Mechanisms of Reinforcement Learning and Decision-Making With the hBayesDM Package。*Computational Psychiatry*。https://doi.org/10.1162/cpsy_a_00002 — 介紹 hBayesDM，一個以階層式貝氏方法擬合強化學習與決策模型的 R 套件，並提供模型比較與潛在變數輸出。
- Corlett, P. R. 等人（2007）。Disrupted prediction-error signal in psychosis: evidence for an associative account of delusions。*Brain*。https://doi.org/10.1093/brain/awm173 — 一項 fMRI 研究，納入 12 名健康參與者與 12 名有妄想信念者，報告額葉預測誤差反應受到干擾，且與形成妄想的傾向相關。

### 綜述與教科書

- Huys, Q. J. M., Maia, T. V. & Frank, M. J.（2016）。Computational psychiatry as a bridge from neuroscience to clinical applications。*Nature Neuroscience*。https://doi.org/10.1038/nn.4238 — 區分資料驅動與理論驅動的方法，回顧兩者的臨床應用，並強調兩者結合的價值。
- Wang, X.-J. & Krystal, J. H.（2014）。Computational Psychiatry。*Neuron*。https://doi.org/10.1016/j.neuron.2014.10.018 — 主張計算模型能找出跨越多種疾病的核心缺陷，並能為診斷與治療提供資訊，同時呼籲跨領域的訓練。
- Maia, T. V. & Frank, M. J.（2011）。From reinforcement learning models to psychiatric and neurological disorders。*Nature Neuroscience*。https://doi.org/10.1038/nn.2723 — 回顧強化學習模型如何描述精神與神經疾病中的行為。
- Woo, C.-W. 等人（2017）。Building better biomarkers: brain models in translational neuroimaging。*Nature Neuroscience*。https://doi.org/10.1038/nn.4478 — 回顧如何發展並驗證預測性腦部模型作為生物標記。
- Wilson, R. C. & Collins, A. G.（2019）。Ten simple rules for the computational modeling of behavioral data。*eLife*。https://doi.org/10.7554/eLife.49547 — 一份適合初學者的指南，說明如何把計算模型與行為資料連結起來，並提出十條使結論有意義的規則。
