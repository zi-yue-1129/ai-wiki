---
translation_reviewed: 2026-10-28
---

# 基準測試套件：MMLU、HELM 與後續基準

基準測試套件（benchmark suite）是一組固定的任務，並以相同方式為每個模型評分，讓研究者能把語言模型放在同一把尺上比較。MMLU、HELM、BIG-bench、GPQA、HumanEval 與 MATH 是被引用最多的幾套基準。其中有幾套在分數逼近上限後，已被更難的後續基準取代。

## 概述

在共用基準出現之前，各實驗室都只在自己選定的任務上回報結果，使比較十分困難。基準測試套件固定了題目、提示格式、評分器與指標，因此不同開發者的分數可以並列比較。這些套件的範圍各不相同：HumanEval 要求撰寫短的 Python 函式，MATH 則是競賽數學。MMLU 涵蓋 57 個學科，從初等數學到法律都有。HELM 與 BIG-bench 的目標更廣，前者結合多種情境，後者則收集了數百項任務。

廣泛的基準套件通常會經歷同一種生命週期：一套基準推出時被視為很難，模型逐步進步，分數聚集在頂端，最後這套基準就無法再區分模型。[評估總覽](index.md)把飽和列為基準測試常見的陷阱之一。

## 關鍵概念

- **基準測試套件**：一組有版本的任務，附帶固定的提示協定、評分器與指標。
- **飽和（saturation）**：大多數模型都接近滿分，因此剩餘的差異與雜訊及提示效應相比已經很小。
- **資料污染（contamination）**：測試題目，或與之相近的改寫句，出現在預訓練資料中，使高分部分反映的是記憶。
- **構念效度（construct validity）**：分數是否真的衡量了其名稱所宣稱的能力。
- **排行榜（leaderboard）**：公開的分數表，由維護者執行，或由開發者自行回報。

## 運作方式

大多數知識類基準都採用選擇題。每一題被放進一個模板中，通常前面會附上幾個已解答的範例（少樣本提示，few-shot prompting）。模型生成一個選項的字母，或為每個選項指定一個似然值；答案被擷取出來後與標準答案比對，分數就是正確題數的比例，並依學科取平均。

程式與數學類基準的評分方式不同。對 HumanEval 而言，模型生成的函式會在單元測試上執行。重複取樣會提高解題率，因為只要任一樣本通過，該題就算解出（Chen et al., 2021）。對 MATH 而言，最終答案會在正規化後比對，這比聽起來困難，因為同一個數值可以有許多等價寫法。

```mermaid
flowchart LR
  Q[固定題目] --> P[提示模板與範例]
  P --> M[模型輸出]
  M --> X[答案擷取]
  X --> G[評分器或單元測試]
  G --> S[每項任務的分數]
  S --> L[排行榜條目]
```

### 執行排行榜

排行榜的可比較性取決於它的協定。有些維護者會讓每個模型都通過同一個共用的評估工具；另一些則接受開發者自行執行、使用自己提示與設定所得的數字。所示範例的數量、模板、答案解析與權杖預算，都可能改變分數。一份審慎的排行榜會記錄版本、日期、設定，以及維護者是否重現了每個分數。人類偏好競技場（arena）則採用另一套協定：使用者比較兩個匿名回應，投票結果再彙整成排名（Chiang et al., 2024）。

## 關鍵方法

| 基準 | 年份 | 衡量內容 | 格式 | 狀態 |
|---|---|---|---|---|
| MMLU | 2020 | 57 個學科的知識與問題解決 | 四選一選擇題 | 廣泛使用；其題目中發現錯誤 |
| MMLU-Pro | 2024 | 更難、以推理為主的題目 | 十個選項 | 針對 MMLU 的停滯而提出 |
| HELM | 2022 | 以七項指標評分的多種情境 | 混合 | 作者稱之為「活的基準」（living benchmark） |
| BIG-bench | 2022 | 204 項超出當時模型能力的任務 | 混合，附人類基線 | 大型協作式任務集 |
| GPQA | 2023 | 抗網路搜尋的研究生程度科學題 | 選擇題 | 即使是熟練的非專家也很難作答 |
| HumanEval | 2021 | 依 docstring 撰寫的 Python 函式 | 程式碼，以單元測試評分 | 已接近飽和（見[軟體開發](../../applications/software/index.md)） |
| MATH | 2021 | 附逐步解答的競賽數學 | 自由作答的最終答案 | 發表時即使是大型模型準確率也偏低 |

MMLU、HELM 與 BIG-bench 同時涵蓋許多能力，因此它們的分數概括的是廣泛的能力輪廓。GPQA 與 MATH 探測的是較窄、較深的專業能力，而 HumanEval 以客觀的評分器測試單一技能。

### 飽和與資料污染

在發表時，多數模型在 MMLU 上的表現接近隨機猜測，而最大的 GPT-3 模型也只比隨機猜測高出約 20 個百分點（Hendrycks et al., 2020）。MMLU-Pro 的提出部分是因為 MMLU 的分數已經停滯；其作者測得，在 MMLU 上提示風格造成的敏感度為 4% 至 5%，而在新基準上約為 2%。[^mmlupro]

錯誤本身也是另一個問題。對 MMLU 的重新標註發現，題目的標準答案存在錯誤，這些錯誤會掩蓋模型真正的能力（Gema et al., 2024）。[^gema] 資料污染則較難察覺。Deng et al. (2023) 提出兩種方法：一是與預訓練語料進行重疊比對，二是猜測遮蔽答案的測試，後者可用於封閉模型。

## 連結

基準設計借用了心理計量學（psychometrics），也就是編製測驗的科學。題目難度、信度與構念效度都可以直接套用；一個分數是否反映了其名稱所宣稱的能力，正是心理學家對智力測驗所提出的問題（Raji et al., 2021）。人類的那一面請見[心理學與 AI](../../brain-mind/psychology/index.md)。BIG-bench 連結了兩者：其中數項任務取材自兒童發展與語言學，而它的人類基線來自執行相同任務的專家評分者。

這些基準回報的分數，也是擴展定律研究（scaling studies）的標尺。[計算最佳訓練](../../theory/models/llm/compute-optimal-training/index.md)頁面回報了在固定運算預算下訓練的模型之 MMLU 結果。至於比較兩個分數的統計方法，請見[評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.md)。

## 應用

- **模型選擇**：開發者會在 MMLU 或 HumanEval 等基準上比較候選模型，然後再檢驗自己任務上的表現。
- **回歸測試**：每當提示、模型或檢索設定有所變動，團隊就重新執行一套公開基準或其中的子集。
- **重新分析**：HELM 釋出了原始的提示與生成結果，因此其他研究者可以重新計算它的指標（Liang et al., 2022）。
- **程式助理**：像 HumanEval 這樣的功能性測試用來評判程式碼生成，但它們涵蓋的是短而獨立的函式，而非完整專案。見[程式助理](../coding-assistants/index.md)。

## 開放問題

- **維持難度**：動態基準（由標註者與模型共同參與、不斷重新建構題目）是一項提案（Kiela et al., 2021）。
- **格式與能力**：改變格式是否會改變所衡量的內容？MMLU-Pro 回報，思維鏈提示在其較難的題目上有幫助，而在 MMLU 上則沒有（Wang et al., 2024）。
- **隱藏的訓練資料**：對於訓練語料不可見的封閉模型，如何偵測資料污染？
- **誰的偏好**：競技場的排名取決於誰投票，而與專家評分者的一致性，並無法說明該競技場代表的是哪些人。

[^mmlupro]: Wang et al. (2024)，見參考文獻。該論文指出，MMLU-Pro 把選項數量由四個擴增為十個，並以 24 種提示風格測量提示敏感度。
[^gema]: Gema et al. (2024)，見參考文獻。作者估計 MMLU 題目中有 6.49% 含有錯誤，而在所分析的病毒學（Virology）題目中，有 57% 含有錯誤。

## 參考文獻

### 開創性論文

- Hendrycks, D. et al. (2020). *Measuring Massive Multitask Language Understanding*. arXiv. https://arxiv.org/abs/2009.03300 — 提出 MMLU，一套涵蓋 57 個學科、用來衡量廣泛知識的選擇題測試。
- Hendrycks, D. et al. (2021). *Measuring Mathematical Problem Solving With the MATH Dataset*. arXiv. https://arxiv.org/abs/2103.03874 — 提出 12,500 道附有逐步解答的競賽數學題。
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — 提出 HumanEval，並說明重複取樣如何提高解題率。
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 提出 BIG-bench，這是一組經協作建立、刻意選為困難的 204 項任務。
- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — 提出 HELM，一種跨多種情境與多項指標的評估，並釋出其原始輸出。
- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — 提出由專家撰寫、旨在抵抗網路搜尋的科學題目。
- Wang, Y. et al. (2024). *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark*. arXiv. https://arxiv.org/abs/2406.01574 — 提出 MMLU 的較難後繼者，具有十個選項且對提示的敏感度較低。

### 相關工作

- Raji, I. D. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — 探討被當作進步代理指標的重要基準之構念效度問題。
- Gema, A. P. et al. (2024). *Are We Done with MMLU?* arXiv. https://arxiv.org/abs/2406.04127 — 找出 MMLU 題目中的標準答案錯誤，並釋出重新標註的子集。
- Deng, C. et al. (2023). *Investigating Data Contamination in Modern Benchmarks for Large Language Models*. arXiv. https://arxiv.org/abs/2311.09783 — 提出重疊比對與猜測遮蔽答案的測試，用來偵測資料污染。
- Chiang, W.-L. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. arXiv. https://arxiv.org/abs/2403.04132 — 描述一個群眾外包、成對比較的排行榜，以及其投票的分析方法。
- Kiela, D. et al. (2021). *Dynabench: Rethinking Benchmarking in NLP*. arXiv. https://arxiv.org/abs/2104.14337 — 提出動態基準，由標註者撰寫目前模型會誤判的範例。
