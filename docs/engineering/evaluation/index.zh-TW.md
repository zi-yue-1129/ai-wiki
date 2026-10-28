# 評估與基準

評估衡量 AI 系統在特定條件下的表現。基準測試提供一個共同的比較任務；應用層級的評估則問整個系統是否滿足使用者的需求。單靠排行榜，無法確立系統在每種情境中都有用。[^validity]

## 主要基準（作為參考點）

以下範例是一份入門目錄，並非當前模型的排名。每次報告結果時，都應記錄基準版本、評估日期與評估協定。

| 領域 | 基準 | 解讀 |
|---|---|---|
| 一般知識 | MMLU、MMLU-Pro | 檢查學科與語言的涵蓋範圍 |
| 高難度專家問題 | GPQA Diamond、Humanity's Last Exam | 記錄題目選擇與工具存取權限 |
| 數學 | GSM8K、MATH、AIME、FrontierMath | 記錄答案檢查方式與嘗試次數上限 |
| 程式碼 | HumanEval、SWE-bench Verified、LiveCodeBench | 見[軟體開發](../../applications/software/index.md) |
| 推理／抽象 | ARC-AGI-1/2 | 檢查開發任務與測試任務是否分開 |
| 代理人 | GAIA、WebArena、OSWorld、τ-bench、Terminal-Bench | 記錄工具權限與失敗處理方式 |
| 長脈絡 | 大海撈針（needle-in-a-haystack）、RULER、LongBench | 檢索 ≠ 對長輸入進行推理 |
| 多模態 | MMMU、MathVista、Video-MME | |
| 中文／繁體中文 | C-Eval、CMMLU、TMMLU+ | |
| 人類偏好 | Chatbot Arena | 評分者的組成與呈現方式會影響解讀 |
| 安全性 | HarmBench、StrongREJECT、WMDP、危險能力評估 | 見[安全與對齊](../../society/safety-alignment/index.md) |

上表中的一般知識、推理與程式碼基準（MMLU、HELM、BIG-bench、GPQA、HumanEval、MATH）已在[基準測試套件](benchmark-suites.md)中比較，包括飽和問題與排行榜的執行方式。

## 設計評估協定

### 定義任務與要做的決定

在選擇指標之前，先寫下預期用途、目標族群與失敗的代價。文件助理可能同時需要正確的答案、支持的證據，以及在缺乏證據時適當地拒答。單一的偏好分數無法同時測試這三者。HELM 示範了跨越多種情境與面向的評估，包括準確度、穩健性與效率。[^helm]

關於監督式學習的指標與驗證方法，見[評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.md)。這裡的重點是周邊的系統：提示、檢索、工具、評分者與報告方式。

### 區分開發與最終測試

開發用的範例用來修改提示、選擇模型與調整檢索。把測試集保留給最終比較；若反覆在它上面挑選改進，它就變成了開發資料。切分方式要與部署情境相符：評估新群體時，把每個人或每個群體的觀察放在一起；做預測時，保留時間順序。[^splits]

像是縮放或特徵選擇等學習得到的前處理，只能在訓練資料上擬合。Pipeline 會把這些操作限制在訓練折（fold）內；若在切分前就對整個資料集做前處理，就會洩漏資訊。[^leakage] 對語言模型而言，應記錄已知的訓練資料重疊情況。保留一組應用層的測試集，並不能證明預訓練模型從未見過其內容。

### 凍結比較條件

保存一份執行紀錄，包括模型識別碼、資料集版本、評估程式碼版本、提示模板、示範範例、取樣設定、嘗試次數上限與權杖預算。對於使用工具的系統，還要包括檢索語料的快照、工具版本、權限與執行環境。記錄評分者版本、評分量表、逾時設定，以及無效輸出如何計分。

這是一份實用的報告檢查表。使用不同工具或預算的系統，是不同的組態系統，結果中應說明這項區別。除了平均值，也要保留每個範例的輸出與失敗案例。Inspect 提供可組合的資料集、執行、評分與評估紀錄。[^inspect]

## 檢查評分者與不確定性

若任務有明確的標準，就使用確定性的檢查：精確答案、結構驗證或可執行的測試。通過結構檢查只能確立格式正確，不能確立事實正確。

**LLM 作為評審**會用另一個語言模型與評分量表為輸出評分。Zheng et al. 記錄了位置偏誤、冗長偏誤與自我增強偏誤，以及推理上的限制。[^judge] 應把評審的判斷與人工評分的樣本比對，檢查分歧之處，並在成對比較中交換答案順序，以診斷位置效應。在一個資料集上達成一致，不保證在另一個領域或語言中也一致。評分量表改變時，也要重新評分基準線。[LLM 作為評審與成對評估](llm-as-judge.md)更詳細地介紹評審的設計、成對排名，以及與人類的一致性。

報告範例數量、分數定義與不確定性。在 100 個任務上從 80 個正確增加到 82 個，只是多了兩次成功；單靠這點，並不能證明在目標族群上表現更好。成對自助法（paired bootstrap）會以配對的範例索引一起重抽樣，用來估計分數差異的不確定性；SciPy 有文件說明此選項。[^bootstrap] 選擇與資料結構相符的重抽樣單位：同一段對話中的多個回合，不會自動成為獨立的對話。應說明假設與區間估計方法；區間無法修正不具代表性的測試集。

另外也要報告重要的任務、語言與使用者群體切片、延遲、成本與失敗案例。在一個面向的改進，可能伴隨另一個面向的退步。[^helm]

## 常見陷阱

- **資料污染**：測試題目洩漏到訓練資料中——使用保留、動態或私有的資料集；見[基準測試污染](contamination.md)
- **飽和**：模型接近天花板時，基準便失去鑑別力
- **古德哈特定律**：為基準而最佳化，會侵蝕它的意義
- **對提示敏感**：細微的格式改變就可能使分數大幅波動；應報告設定
- **統計雜訊**：報告信賴區間；小型測試集會造成誤導
- **構念效度**：這個基準真的衡量了它的分數所代表的東西嗎？[^validity]
- **基準 ≠ 真實世界的實用性**

## 評估自己的應用

1. **寫下真實使用者任務中「好」的樣子**
2. **從真實的輸入建立開發集與保留集**，包括邊界案例、缺乏證據的情況與對抗性案例；為覆蓋範圍與樣本量提出理由，並與要做的決定相符
3. **選擇評分者**：
    - 盡可能使用精確比對、單元測試或程式化檢查
    - **以量表為基礎的 LLM 作為評審**——以人工評分驗證；留意位置、冗長與自我偏好偏誤
    - 高風險或主觀品質需要人工審閱
4. **每次變更都追蹤退步**（提示、模型、檢索設定）
5. **在正式環境監控**：抽樣審閱與使用者回饋

## 來自心理學與測量科學的方法

- **題目反應理論**，用來估計模型能力與題目難度
- 心理計量學中的**信度與效度**概念
- **控制實驗**與平衡設計（例如交換答案順序以偵測位置偏誤）[^judge]
- **認知科學式的探測**，用來測試特定能力（見[心理學與 AI](../../brain-mind/psychology/index.md)）

## 工具

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) 提供共用的語言模型評估任務與設定；[HELM](https://crfm.stanford.edu/helm/) 支援多情境、多指標的評估；[Inspect](https://inspect.aisi.org.uk/) 提供可組合的任務、評分器、代理人與紀錄。

[^validity]: Raji et al. (2021)，見參考文獻。
[^helm]: Liang et al. (2022)，見參考文獻。
[^splits]: scikit-learn，*Cross-validation: evaluating estimator performance*，見參考文獻。
[^leakage]: scikit-learn，*Common pitfalls and recommended practices*，見參考文獻。
[^inspect]: Inspect 文件，見參考文獻。
[^judge]: Zheng et al. (2023)，見參考文獻。
[^bootstrap]: SciPy，*scipy.stats.bootstrap*，見參考文獻。

## 參考文獻

### 研究論文

- Raji, I. D. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及根據基準表現做出廣泛主張的限制。
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. https://arxiv.org/abs/2211.09110 — 跨多個情境與指標評估語言模型，揭露能力缺口與取捨。
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. https://arxiv.org/abs/2306.05685 — 研究以模型為基礎的評審、與人類的一致性，以及開放式助理評估中的偏誤。

### 文章與文件

- scikit-learn contributors. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — 說明保留測試、模型選擇、分組切分與考慮時間的評估。
- scikit-learn contributors. *Common pitfalls and recommended practices*. https://scikit-learn.org/stable/common_pitfalls.html — 示範前處理洩漏，以及 Pipeline 如何把擬合限制在訓練資料上。
- SciPy contributors. *scipy.stats.bootstrap*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html — 說明自助法信賴區間，以及對配對觀察做配對重抽樣。
- UK AI Security Institute and Meridian Labs. *Inspect*. https://inspect.aisi.org.uk/ — 說明可組合的資料集、解題器、評分器、代理人評估與評估紀錄。
- EleutherAI. *Language Model Evaluation Harness*. https://github.com/EleutherAI/lm-evaluation-harness — 提供可重複使用的語言模型評估任務、設定與執行工具。
