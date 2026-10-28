---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - statistics
---

# 評估協定

協定定義資料如何切分、進行哪些比較，以及如何報告不確定性。協定上的錯誤，常常比指標的選擇更能改變結論。

## 方法

每個方法都有自己的頁面。

| 方法 | 用途 |
|---|---|
| [交叉驗證](methods/cross-validation.md) | 以多種切分估計泛化能力 |
| [配對自助法](methods/paired-bootstrap.md) | 兩個方法差異的區間 |
| [LLM 作為評審](methods/llm-as-judge.md) | 以模型為開放式輸出打分 |
| [MT-Bench](methods/mt-bench.md) | 交換順序的成對評審，以及它與人類專家的一致性 |
| [長度控制 AlpacaEval](methods/length-controlled-alpacaeval.md) | 修正自動評審偏好較長答案的傾向 |
| [人工評估](methods/human-evaluation.md) | 由人判斷輸出，並報告一致性 |
| [Elo 評分與競技場](methods/elo-rating.md) | 從成對結果為系統排名 |
| [污染偵測](methods/contamination-detection.md) | 檢查基準項目是否在訓練資料中 |
| [N-gram 重疊去污染](methods/ngram-overlap-decontamination.md) | 移除與語料共享長詞序列的基準項目 |
| [Min-K% Prob](methods/min-k-percent-prob.md) | 只用模型的 token 機率偵測預訓練資料 |
| [LiveBench](methods/livebench.md) | 更新基準題目，使其晚於訓練資料 |

## 切分資料

- **訓練、驗證與測試。** 在驗證集上調校，測試集只報告一次。
- **交叉驗證**在多種切分上取平均。類別不平衡時使用分層摺。
- **依群組與依時間切分。** 把同一位病人、使用者或對話的所有範例放在同一摺。預測任務只能用比訓練資料更晚的資料來驗證。
- **讓測試集不參與決策。** 測試集一旦用來指導模型選擇，就變成開發資料；要提出最終主張時，需要一組新的測試集。

scikit-learn 關於交叉驗證的指南說明了這些切分方式（見參考文獻）。

## 避免資料洩漏

- 縮放或特徵選擇等前處理，只能在訓練資料上擬合。Pipeline 會強制執行這點；若在切分前就對整個資料集做前處理，就會洩漏資訊。
- 移除出現在超過一個切分中的重複資料。
- 對語言模型，應記錄測試題目與訓練語料之間的重疊情況。保留一組應用資料，並不能證明預訓練模型從未見過其內容。

## 公平比較方法

- **固定條件。** 每個方法應使用相同的切分、資料預算與調校投入。讓某個方法獲得更多調校，是常見的錯誤結論來源。
- **在相同的範例上比較。** 配對比較比比較兩個獨立的平均值更靈敏。
- **保存執行紀錄。** 每個結果都應附上模型版本、資料集版本、提示詞、隨機種子與嘗試次數上限。Inspect 與 lm-evaluation-harness 等工具都以此為核心（見參考文獻）。

## 報告不確定性

除了分數，也要報告範例數。在 100 個任務上從 80 題答對變成 82 題，只多了兩次成功，單靠這點不足以證明系統更好。

**配對自助法（paired bootstrap）**會把配對的範例一起重抽樣，用來估計兩個方法差異的不確定性（SciPy 有文件說明此選項）。重抽樣的單位要與資料的依賴結構相符：同一段對話中的多個回合，不是獨立的範例。訓練的隨機性是另一個變異來源，若主張依賴於此，應以多個種子重複訓練。

## 評審與人工評分

**LLM 評審**依照評分量表為輸出打分。Zheng et al. (2023) 記錄了位置偏誤、冗長偏誤與自我偏好偏誤。良好的做法是：把評審與人工評分的樣本比對、在成對比較中交換答案順序，並且每當評分量表改變時重新評分基準線。

**人工評估**應報告評分者是誰、收到什麼指示，以及他們彼此之間的一致程度。缺少這些資訊，結果就無法重現。

## 基準分數能說明什麼

基準是一個有固定計分規則的共同任務。它的分數說明的是：在該協定下，系統在該任務上的表現。它不能說明系統在所有相似任務上的表現。Liang et al. (2022) 主張同時跨情境與指標評估，讓準確率與穩健性、成本之間的取捨變得清楚。Raji et al. (2021) 則討論超出基準所衡量範圍的主張有何限制。

## 開放問題

當訓練資料不公開時，很難偵測資料污染。評估需要多步驟、使用工具的代理人時，協定除了記錄答案，也要記錄環境。在多個基準上比較多個方法的統計方法，仍不如單一基準的情況成熟。

## 工具

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) 用來執行共用的語言模型評估任務。[Inspect](https://inspect.aisi.org.uk/) 提供可組合的資料集、解題器、評分器與評估紀錄。

## 參考文獻

### 開創性論文

- Raji, I. D. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. https://arxiv.org/abs/2111.15366 — 探討構念效度，以及根據基準表現做出廣泛主張的限制。
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. https://arxiv.org/abs/2211.09110 — 跨多個情境與指標評估語言模型，揭露能力缺口與取捨。
- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. https://arxiv.org/abs/2306.05685 — 研究以模型為基礎的評審、它與人類的一致性以及其偏誤。

### 文章與文件

- scikit-learn contributors. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — 說明保留測試、模型選擇、分組切分與考慮時間的評估。
- scikit-learn contributors. *Common pitfalls and recommended practices*. https://scikit-learn.org/stable/common_pitfalls.html — 示範前處理洩漏，以及 Pipeline 如何把擬合限制在訓練資料上。
- SciPy contributors. *scipy.stats.bootstrap*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html — 說明自助法信賴區間，以及對配對觀察做配對重抽樣。
- UK AI Security Institute and Meridian Labs. *Inspect*. https://inspect.aisi.org.uk/ — 說明可組合的資料集、解題器、評分器、代理人評估與評估紀錄。
- EleutherAI. *Language Model Evaluation Harness*. https://github.com/EleutherAI/lm-evaluation-harness — 提供可重複使用的語言模型評估任務、設定與執行工具。
