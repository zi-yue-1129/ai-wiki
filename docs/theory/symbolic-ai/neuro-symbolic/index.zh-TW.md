---
translation_reviewed: 2026-10-28
---

# 神經符號 AI（Neuro-Symbolic AI）

神經符號 AI 結合神經網路與符號方法。前者能從資料學習，並能處理有雜訊的感知；後者以規則、程式與邏輯明確表示知識並進行推理。其目標是能從範例學習、同時仍能解釋並檢驗自身結論的系統。它是[符號 AI 概述](../index.md)中的整合主軸，而其最新形式是會呼叫工具並執行程式碼的大型語言模型。

## 概述

神經與符號 AI 各有互補的長處。神經網路能從影像、文字等原始資料學習表示，並能平滑地推廣到與訓練資料相似的輸入。它們難以檢視，而且在多步驟問題上可能充滿自信地犯錯。符號系統把知識保存為離散的物件，可以組合、檢查與解釋，推理也很精確。但它們需要人工撰寫知識，而且一遇到有雜訊或模糊的輸入就容易失效。

Garcez 與 Lamb 主張，有根據的知識表示與推理應與深度學習整合，而這種整合有助於可靠的可解釋性。[^1] Lake 等人從認知科學得出相近的結論。他們主張，類人的學習需要世界的因果模型、以直覺理論為基礎的學習，以及組合性，而單靠模式辨識無法提供這些。[^2]

## 關鍵概念

- **符號（symbol）**：離散的物件，例如述詞、常項、規則或程式片段。符號可以組合、量化，也能被精確比較。
- **嵌入（embedding）**：代表符號或物件的實數向量。神經網路在嵌入上運算，古典符號系統則不然。
- **可微分邏輯（differentiable logic）**：邏輯的鬆弛形式。真值介於 0 與 1 之間，聯結詞是實數函數，因此梯度可以穿過一個邏輯式流動。
- **程式合成與歸納（program synthesis and induction）**：程式合成找出把給定輸入映射到給定輸出的程式；程式歸納則從範例學習這樣的程式，或一組可重用的部件。
- **驗證器（verifier）**：獨立的檢查者，例如直譯器、求解器或證明助手，負責接受或拒絕候選答案。符號系統的保證通常在這裡進入系統。

## 運作方式

神經符號系統通常遵循少數幾種模式，這些模式常同時出現在同一個系統中。

1. **神經前端，符號後端。** 網路把原始輸入轉為符號，再由符號模組對這些符號推理。神經符號概念學習器（Neuro-Symbolic Concept Learner）建立以物件為單位的場景表示，並把每個問題翻譯成可執行的程式，再在該表示上執行。它從配對的影像與問答中學習視覺概念、詞義與語法解析，無需對物件或詞彙加上標籤。[^3]
2. **以邏輯作為訓練訊號。** 背景規則變成可微分的約束或損失項。在邏輯張量網路（Logic Tensor Networks）中，公式在實數語意上取得 $[0,1]$ 的真值，因此網路可以被訓練去滿足它們。[^4] 對於真值 $a, b \in [0,1]$ 的軟性合取，兩種常見選擇是乘積 $a\,b$ 與 Łukasiewicz t-norm $\max(0, a+b-1)$。兩者都回傳 $[0,1]$ 中的值，而且當 $a$ 與 $b$ 為 0 或 1 時與一般邏輯一致。
3. **以神經網路引導符號搜尋。** 網路提出或評分步驟，符號引擎再推導或檢查後果。AlphaGeometry 是最清楚的例子：語言模型引導符號演繹引擎，走過幾何問題的各個分岔點。[^5]
4. **模型寫程式，執行環境計算。** 語言模型把問題轉為程式碼，由直譯器算出答案。程式輔助語言模型（program-aided language models）把求解步驟交給 Python 直譯器，因此模型只負責把問題拆成步驟。[^6]
5. **模型提出，驗證器裁定。** 模型產生候選答案，外部、可靠的檢查器接受或拒絕它們。Kambhampati 等人主張，自迴歸的 LLM 本身無法規劃或驗證自己的計畫，並提出一種框架：由 LLM 產生候選，再由外部的模型式驗證器檢查。[^7]

```mermaid
flowchart LR
    X[原始輸入：影像、文字或問題] --> N[神經網路：感知與提議]
    N -->|符號、程式或候選步驟| S[符號模組：邏輯、執行、搜尋或證明檢查]
    S -->|已驗證的結果或回饋| N
    S --> Y[附有可檢查理由的答案]
```

## 關鍵方法

三個代表性方法各有專頁。它們分別涵蓋可微分邏輯、程式歸納與神經定理證明，共同顯示符號部分可以被學習，而不只能靠人工撰寫。

| 方法 | 提出時間 | 核心想法 | 專頁 |
|---|---|---|---|
| ∂ILP（可微分歸納邏輯程式設計） | 2017 年預印本；2018 年期刊 | 以梯度下降在似然目標上學習邏輯規則，因此能容忍有雜訊的範例，並可接上神經網路 | [∂ILP](differentiable-ilp/index.md) |
| DreamCoder | 2020 年預印本 | 覺醒—睡眠學習，逐步建立可重用的程式抽象庫，並訓練神經網路引導程式搜尋 | [DreamCoder](dreamcoder/index.md) |
| 神經定理證明器 | 2017 年預印本 | 反向鏈結的證明搜尋，以學得向量之間的相似度取代符號比對 | [神經定理證明器](neural-theorem-prover/index.md) |

語言模型那一側的內容見「關聯」一節，因為其機制屬於工具呼叫。

## 關聯

- **古典符號 AI。** 神經符號工作沿用較早的技術。[思維樹](../search/tree-of-thoughts/index.md)把語言模型放在搜尋樹中啟發式函數的位置。[SayCan](../planning/saycan/index.md)讓語言模型提出機器人技能，再由價值函數判斷其可行性。[GraphRAG](../knowledge-graphs/graphrag/index.md)把知識圖譜與語言模型的檢索結合。
- **使用工具與程式碼的 LLM。** 會呼叫工具的 LLM 就是一種神經符號系統。模型是讀取語言並提出動作的學習元件，工具則是精確計算並回傳可檢查結果的符號元件。工具結構描述與協定的機制見[工具呼叫與 Model Context Protocol](../../../engineering/agents/tool-calling-and-mcp/index.md)。程式碼是實用的介面，因為直譯器會給出確定的結果；[CodeAct](../../../engineering/agents/sandboxing-and-computer-use/codeact/index.md)則把可執行的程式碼當作代理人的動作。
- **代理人與推理。** [AI 代理人](../../models/agents/index.md)與[推理模型](../../models/reasoning/index.md)描述模型如何選擇步驟。本頁關注的則是用來檢查這些步驟的符號結構。
- **腦與心智。** 雙歷程的對比（快速直覺與緩慢審慎）是符號與神經分工在心理學上的一種對應（見[心理學與 AI](../../../brain-mind/psychology/index.md)）。[認知架構](../../../brain-mind/cognitive-architectures/index.md)如 ACT-R，把認知建模為作用於事實記憶之上的產生式規則。[Lake 等人的論證](../../../brain-mind/cognitive-science/building-machines-like-people/index.md)另有專頁。

## 應用

- **數學。** AlphaGeometry 結合語言模型與符號演繹引擎，在其測試集的 30 題奧林匹亞幾何題中解出 25 題。[^8] AlphaProof 是在 Lean 證明助手中搜尋證明的強化學習系統，在 2024 年國際數學奧林匹亞中解出五道非幾何題中的三題。[^9] 見[數學與形式證明](../../../applications/mathematics/index.md)，並有 [AlphaGeometry](../../../applications/mathematics/alphageometry/index.md) 與 [AlphaProof](../../../applications/mathematics/alphaproof/index.md) 專頁。
- **軟體與機器人。** 歸納出的程式與語言模型產生的程式碼，只有在通過測試後才被接受；SayCan 則以學得的檢查過濾語言模型提出的計畫。
- **知識庫。** 從知識圖譜檢索的事實，能讓語言模型的回答以儲存的資料為根據。見 [GraphRAG](../knowledge-graphs/graphrag/index.md)。

## 開放問題

- **符號從何而來？** 人工撰寫的本體論成本高昂。像 DreamCoder 這樣會自行學習抽象的系統，能產生可讀的程式庫，但目前主要在精心設計的任務族上得到示範，能擴展到多遠仍不清楚。
- **誰來檢查檢查者？** 形式驗證器只保證它所檢查的規格得到滿足，因此一個機器驗證過、卻證明錯誤陳述的證明，仍然是失敗。
- **語言模型能自我驗證嗎？** LLM-Modulo 主張它們無法單獨做到。若存在便宜且可靠的檢查器，例如單元測試或證明助手，外部驗證就很實用。許多開放式任務沒有這樣的檢查器。
- **這種分工是心智的模型嗎？** 人類推理是否有符號核心，以及神經符號系統能否說明這件事，仍有爭議。

[^1]: Garcez 與 Lamb（2020），見上文。
[^2]: Lake 等人（2016），見上文。
[^3]: Mao 等人（2019），見上文。
[^4]: Serafini 與 d'Avila Garcez（2016），見上文。
[^5]: Trinh 等人（2024），見上文。
[^6]: Gao 等人（2022），見上文。
[^7]: Kambhampati 等人（2024），見上文。
[^8]: Trinh 等人（2024），見上文。所列數字為摘要所報告，測試集為 30 題。
[^9]: Hubert 等人（2025），見上文。結果依摘要所述；摘要並提到，AlphaProof 與 AlphaGeometry 2 合併後，達到相當於銀牌的分數。

## 參考文獻

### 開創性論文

- Garcez, A. d'Avila, & Lamb, L. C. (2020). *Neurosymbolic AI: The 3rd Wave*. arXiv. https://arxiv.org/abs/2012.05876 — 主張有根據的知識表示與推理應與深度學習整合。
- Lake, B. M. et al. (2016). *Building Machines That Learn and Think Like People*. arXiv. https://arxiv.org/abs/1604.00289 — 主張類人學習需要因果模型、直覺理論與組合性。
- Evans, R. & Grefenstette, E. (2018). *Learning Explanatory Rules from Noisy Data*. Journal of Artificial Intelligence Research. https://doi.org/10.1613/jair.5714 — 提出可微分歸納邏輯程式設計，以梯度下降學習邏輯規則，並能容忍有雜訊的訓練資料。
- Rocktäschel, T. & Riedel, S. (2017). *End-to-End Differentiable Proving*. arXiv. https://arxiv.org/abs/1705.11040 — 建立以反向鏈結證明知識庫查詢的神經網路，其中的軟性符號比對由資料學得。
- Ellis, K. et al. (2020). *DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning*. arXiv. https://arxiv.org/abs/2006.08381 — 透過交替的覺醒與睡眠階段，學習領域專用的程式語言與神經搜尋引導。
- Mao, J. et al. (2019). *The Neuro-Symbolic Concept Learner: Interpreting Scenes, Words, and Sentences From Natural Supervision*. arXiv. https://arxiv.org/abs/1904.12584 — 從影像與問答配對中，透過在場景表示上執行學得的程式，學習視覺概念與語意解析。
- Serafini, L. & d'Avila Garcez, A. (2016). *Logic Tensor Networks: Deep Learning and Logical Reasoning from Data and Knowledge*. arXiv. https://arxiv.org/abs/1606.04422 — 定義真值在單位區間內的一階邏輯 Real Logic，並以張量網路實作。

### 綜述與教科書

- Besold, T. R. et al. (2017). *Neural-Symbolic Learning and Reasoning: A Survey and Interpretation*. arXiv. https://arxiv.org/abs/1711.03902 — 綜述神經符號學習與推理，連結計算邏輯與連結主義的認知模型。
- Hitzler, P. et al. (2022). *Neuro-symbolic approaches in artificial intelligence*. National Science Review. https://doi.org/10.1093/nsr/nwac035 — 綜述在人工智慧中結合符號方法與神經方法的途徑。

### 文章與文件

- Trinh, T. H. et al. (2024). *Solving olympiad geometry without human demonstrations*. Nature. https://doi.org/10.1038/s41586-023-06747-5 — 介紹 AlphaGeometry，它把以合成資料訓練的語言模型與符號演繹引擎結合。
- Hubert, T. et al. (2025). *Olympiad-level formal mathematical reasoning with reinforcement learning*. Nature. https://doi.org/10.1038/s41586-025-09833-y — 描述 AlphaProof，它透過強化學習學會找出形式化的 Lean 證明，並在困難問題上進行測試時適應。
- Kambhampati, S. et al. (2024). *LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks*. arXiv. https://arxiv.org/abs/2402.01817 — 立場論文，主張 LLM 無法單獨規劃或自我驗證，並提出與外部模型式驗證器搭配的 LLM。
- Gao, L. et al. (2022). *PAL: Program-aided Language Models*. arXiv. https://arxiv.org/abs/2211.10435 — 讓語言模型撰寫程式，由 Python 直譯器執行，以得出推理問題的答案。
- de Moura, L. & Ullrich, S. (2021). *The Lean 4 Theorem Prover and Programming Language*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-030-79876-5_37 — 描述 Lean 4，即 AlphaProof 所用的證明助手與程式語言。
