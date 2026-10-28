---
translation_reviewed: 2026-10-28
---

# 評估與基準

評估衡量 AI 系統在指定條件下的表現。基準測試提供共同的比較任務；應用評估則檢驗整個系統是否符合使用者需求。排行榜本身無法證明系統在所有情境中都有用。[^validity]

## 主要基準測試（作為參考）

以下例子是入門目錄，而非當前模型排名。每項結果都應記錄基準版本、評估日期與測試流程。

| 領域 | 基準測試 | 解讀方式 |
|---|---|---|
| 一般知識 | MMLU、MMLU-Pro | 檢查學科與語言涵蓋範圍 |
| 高難度專家問題 | GPQA Diamond、Humanity's Last Exam | 記錄任務選擇與工具使用條件 |
| 數學 | GSM8K、MATH、AIME、FrontierMath | 記錄答案檢查方式與嘗試次數上限 |
| 程式碼 | HumanEval、SWE-bench Verified、LiveCodeBench | 參見[軟體開發](../../applications/software/index.md) |
| 推理／抽象能力 | ARC-AGI-1/2 | 檢查開發與測試任務的分離方式 |
| 代理人 | GAIA、WebArena、OSWorld、τ-bench、Terminal-Bench | 記錄工具權限與失敗處理方式 |
| 長上下文 | Needle-in-a-haystack、RULER、LongBench | 檢索不等於對長輸入進行推理 |
| 多模態 | MMMU、MathVista、Video-MME | |
| 中文／繁體中文 | C-Eval、CMMLU、TMMLU+ | |
| 人類偏好 | Chatbot Arena | 評分者群體與呈現方式會影響解讀 |
| 安全性 | HarmBench、StrongREJECT、WMDP、危險能力評估 | 參見[安全與對齊](../../society/safety-alignment/index.md) |

## 設計評估流程

### 定義任務與決策

在選擇指標前，先寫下預期用途、目標使用者與失敗代價。文件助理可能需要回答正確、提供支持證據，並在缺乏證據時適當表明無法回答。單一偏好分數無法同時檢驗這三件事。HELM 展示了跨情境與多面向的評估，包括準確度、穩健性與效率。[^helm]

監督式學習的指標與驗證方法，請參見[評估與驗證](../../foundations/paradigms/supervised/evaluation-and-validation/index.md)。本頁聚焦於周邊系統：提示、檢索、工具、評分機制與結果報告。

### 分開開發與最終測試

使用開發樣本修改提示、選擇模型與調整檢索。保留測試集供最終比較；若反覆根據測試集挑選改進，它就成了開發資料。資料切分應對應部署情境：評估對新群體的泛化時，同一個人或群體的觀察資料應放在同一分區；預測未來時則應保留時間順序。[^splits]

標準化或特徵選擇等需要學習的前處理，只能在訓練資料上擬合。Pipeline 可將這些操作限制在各訓練折內；先對整份資料進行前處理再切分，會造成資訊洩漏。[^leakage] 語言模型還應記錄已知的訓練資料重疊情況。保留一份應用測試集，不代表預訓練模型從未見過其中的內容。

### 固定比較條件

每次執行應保留模型識別碼、資料集版本、評估程式版本、提示範本、示範樣本、取樣設定、嘗試次數與 token 預算。使用工具的系統還應包含檢索語料快照、工具版本、權限與執行環境。另須記錄評分機制版本、評分準則、逾時設定，以及無效輸出的計分方式。

這是一份實務報告清單。工具或預算不同，代表比較的是不同設定的系統；結果應說明這項差異。除了平均值，也應保留逐筆輸出與失敗紀錄。Inspect 提供可組合的資料集、執行、評分與評估日誌功能。[^inspect]

## 檢查評分機制與不確定性

當任務有明確標準時，使用確定性的檢查，例如答案完全匹配、結構描述驗證或可執行測試。通過格式檢查只能證明格式符合要求，無法證明事實正確。

**以大型語言模型作為評審（LLM-as-judge）**，是讓另一個語言模型根據準則評分。Zheng 等人記錄了位置、冗長度與自我偏好等偏誤，以及推理能力限制。[^judge] 應以人工評分樣本比較判斷、檢查分歧，並在成對比較時交換答案順序，以診斷位置效應。在一份資料集上的一致程度，無法保證能延伸到其他領域或語言。評分準則改變時，也應重新評分基準系統。

報告樣本數、分數定義與不確定性。100 題中從答對 80 題進步到 82 題，代表多答對兩題；光憑這點無法確立系統在目標母體中的表現更好。成對 bootstrap 會將對應樣本的索引一起重抽樣，用來估計分數差異的不確定性；SciPy 文件說明了此選項。[^bootstrap] 重抽樣單位必須符合資料結構：同一段對話中的多個回合，不能直接視為彼此獨立的對話。應說明假設與區間計算方法；信賴區間無法補救不具代表性的測試集。

也應報告重要任務、語言與使用者群體的分項結果，以及延遲、成本與失敗案例。某一面向改善時，其他面向可能退步。[^helm]

## 常見陷阱

- **資料汙染**：測試題目進入訓練資料；可使用保留、動態或私有測試集。
- **飽和**：模型接近滿分後，基準難以區分表現。
- **古德哈特定律**：針對基準最佳化，會削弱它的衡量意義。
- **提示敏感性**：微小格式變動可能改變分數；應報告設定。
- **統計雜訊**：報告信賴區間；小型測試集容易誤導。
- **建構效度**：基準是否真的衡量了人們宣稱其分數代表的能力？[^validity]
- **基準表現不等於真實世界的實用性**。

## 評估自己的應用

1. **寫下成功標準**，對應真實使用者任務。
2. **建立開發與保留測試集**，使用真實或合理模擬的輸入，涵蓋邊界案例、缺乏證據與對抗樣本；根據決策需求說明涵蓋範圍與樣本數。
3. **選擇評分方式**：
    - 優先使用答案完全匹配、單元測試或程式化檢查。
    - 使用有評分準則的 **LLM 評審**，並對照人工評分驗證；注意位置、冗長度與自我偏好偏誤。
    - 對高風險或主觀品質採取人工審查。
4. **追蹤每次變更的退步**，包括提示、模型與檢索設定。
5. **在正式環境持續監測**，搭配抽樣審查與使用者回饋。

## 心理學與測量科學的方法

- **試題反應理論**：估計模型能力與題目難度。
- 心理計量學中的**信度與效度**概念。
- **控制實驗**與順序平衡，例如交換答案順序以檢查位置偏誤。[^judge]
- **認知科學式探測**：測試特定能力，參見[心理學與 AI](../../brain-mind/psychology/index.md)。

## 工具

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) 提供共用的語言模型評估任務與設定；[HELM](https://crfm.stanford.edu/helm/) 支援跨情境與多指標評估；[Inspect](https://inspect.aisi.org.uk/) 提供可組合的任務、評分器、代理人與日誌。

[^validity]: Raji et al. (2021)，詳見參考資料。
[^helm]: Liang et al. (2022)，詳見參考資料。
[^splits]: scikit-learn，*Cross-validation: evaluating estimator performance*，詳見參考資料。
[^leakage]: scikit-learn，*Common pitfalls and recommended practices*，詳見參考資料。
[^inspect]: Inspect 文件，詳見參考資料。
[^judge]: Zheng et al. (2023)，詳見參考資料。
[^bootstrap]: SciPy，*scipy.stats.bootstrap*，詳見參考資料。

## 參考資料

### 研究論文

- Raji, I. D. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. https://arxiv.org/abs/2111.15366 — 探討建構效度，以及根據基準表現提出廣泛能力主張的限制。
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. https://arxiv.org/abs/2211.09110 — 透過不同情境與指標評估語言模型，呈現能力缺口與權衡。
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. https://arxiv.org/abs/2306.05685 — 研究模型評審、與人類的一致程度，以及開放式助理評估中的偏誤。

### 文章與文件

- scikit-learn contributors. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — 說明保留測試、模型選擇、群組切分與考慮時間順序的評估。
- scikit-learn contributors. *Common pitfalls and recommended practices*. https://scikit-learn.org/stable/common_pitfalls.html — 示範前處理洩漏，以及如何透過 Pipeline 限制擬合只使用訓練資料。
- SciPy contributors. *scipy.stats.bootstrap*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html — 說明 bootstrap 信賴區間，以及對應觀察資料的成對重抽樣。
- UK AI Security Institute and Meridian Labs. *Inspect*. https://inspect.aisi.org.uk/ — 說明可組合的資料集、執行器、評分器、代理人評估與評估日誌。
- EleutherAI. *Language Model Evaluation Harness*. https://github.com/EleutherAI/lm-evaluation-harness — 提供可重用的語言模型評估任務、設定與執行工具。
