---
translation_reviewed: 2026-10-28
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - theory/evaluation/protocols/methods/llm-as-judge.md
tags:
  - evaluation
  - protocols
  - llm-as-judge
aliases:
  - MT-Bench
  - 多輪對話評估基準
---

# MT-Bench

!!! info "屬於 LLM 作為評審"
    本方法頁隸屬於 [LLM 作為評審](llm-as-judge.zh-TW.md)。它詳細說明 MT-Bench 的評審研究；上層頁面則比較各種評審方法。

MT-Bench 是一組由 80 個多輪問題組成的基準。提出它的研究顯示，一個強大的語言模型評審這些問題的答案時，其一致性大致與人類專家相當。同一研究也記錄了這類評審會出現的偏誤；它所提出的協定，也就是交換答案順序的成對比較，後來成為以模型為基礎的評估中常見的範本。

## 問題

開放式答案（例如對話中的一則回覆）沒有單一的正確字串可供比對。人工評分準確，但緩慢且昂貴；自動的詞彙重疊指標，又無法反映答案是否有幫助。問題在於：語言模型能否作為這類答案便宜且一致的評分者，以及它會犯哪些錯誤。

## 核心想法

以一個強大的模型作為評審，搭配固定的提示與固定的題目集。題目分為八類，每類十題：寫作、角色扮演、資訊擷取、推理、數學、程式設計、STEM 知識，以及人文與社會科學知識。每題都有第二回合，用來測試後續的回應能力。答案以成對方式比較，並交換順序；只有在兩種順序下判定一致時，才算數。否則，該次比較記為平手。

## 程序

1. 對每個題目，向待比較的各模型取得一則答案。
2. 把題目與兩則標示為 A 與 B 的答案交給評審，並要求其給出判定。
3. 以相反的答案順序重做一次比較。
4. 只有在兩種順序都支持同一答案時，才計為勝出；否則計為平手。
5. 把各題的判定彙總成排名，例如使用 [Elo 評分與競技場](elo-rating.zh-TW.md) 中的方法。

論文也測試了單一答案評分：評審一次只為一則答案依固定尺度打分。

## 結果

與人類專家評分者的一致程度如下（Zheng et al., 2023，表 13，第一回合）：

| 比較 | 含平手 | 不含平手 |
|---|---|---|
| GPT-4 對人類專家 | 66% | 85% |
| 人類專家彼此之間 | 63% | 81% |

作者描述 GPT-4 與人類的一致程度，與人類彼此之間的一致程度處於相同水準。第二回合的數字與第一回合接近。在 Chatbot Arena 的投票中，GPT-4 與人類投票者的一致率為：含平手 64%，不含平手 87%（表 6）。

位置一致性是指評審在兩種順序下給出相同判定的比率。以預設提示計算，GPT-4 為 65.0%，GPT-3.5 為 46.2%（表 2）。作者報告了以下緩解方法，但每項都只在小型測試集上驗證，因此數字只能作為參考：

- 少樣本評審把 GPT-4 的一致性從 65.0% 提高到 77.5%，而 API 成本約為四倍。
- 思維鏈提示與參考答案引導的評分，把作者 20 題測試中的失敗率從 20 題失敗 14 題，降至失敗 6 題與 3 題。
- 經過微調的 Vicuna-13B 評審，把一致性從 15.0% 提高到 65.0%，其與人類的一致率在含平手時為 56.8%。

## 已知偏誤

- **位置偏誤。** 多數評審偏好先出現的答案。交換順序並只計入一致的判定，是論文提出的主要處理方式。
- **冗長偏誤。** 在對 23 則答案進行的「重複列表」測試中，Claude-v1 的失敗率為 91.3%，GPT-3.5 為 91.3%，GPT-4 為 8.7%。
- **自我增強。** GPT-4 讓自己的答案在勝率上高出 10%，Claude-v1 則高出 25%。作者表示，這些資料無法確定地證明此偏誤。
- **已給出的答案。** 在數學與推理中，參考答案可能誤導評審；即使評審單獨作答時能正確解題，也會受影響。

## 限制

- 題目集與人類評分小組都不大，因此一致性數字的不確定性很高。
- 研究主要涵蓋有用性。作者指出，安全性、誠實性與無害性大多被忽略，而有用性的各個子面向也被合併為單一分數。
- 結果描述的是 2023 年測試的評審。託管的評審模型會隨時間改變，因此任何新結果都需要自己的一致性檢查。

## 關聯

- 評審協定本身，以及其他評審方法，見[LLM 作為評審](llm-as-judge.zh-TW.md)頁面。
- 自動評審的長度偏誤，以及 AlpacaEval 所用的修正，見[長度控制 AlpacaEval](length-controlled-alpacaeval.zh-TW.md)。
- 由成對判定為多個模型排名，見[Elo 評分與競技場](elo-rating.zh-TW.md)。
- 評審也是一種以模型為基礎的評估，其應用層面的指引見[評估與基準](../../../../engineering/evaluation/index.zh-TW.md)。

## 開放問題

- 人類評分的一致性，在其他語言、領域與任務類型中能保持多少？
- 能否訓練評審減少位置與冗長偏誤，同時不大幅增加成本？
- 當人類評分小組本身對哪個答案較好有分歧時，應如何為評審打分？

## 參考文獻

### 開創性論文

- Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. NeurIPS Datasets and Benchmarks Track. https://arxiv.org/abs/2306.05685 — 提出 MT-Bench 與成對評審協定，並報告與人類的一致性及主要的評審偏誤。
- Chiang, W.-L. et al. (2024). *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. arXiv. https://arxiv.org/abs/2403.04132 — 描述眾包的成對競技場，MT-Bench 評審即以其投票作為比較對象。
- Wang, P. et al. (2023). *Large Language Models are not Fair Evaluators*. arXiv. https://arxiv.org/abs/2305.17926 — 顯示候選答案的順序，會改變 LLM 評估者偏好的答案。
- Liu, Y. et al. (2023). *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*. arXiv. https://arxiv.org/abs/2303.16634 — 以思維鏈步驟與表單填寫進行 LLM 評分；報告其與人類在摘要任務上的 Spearman 相關係數為 0.514。
- Dubois, Y. et al. (2024). *Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators*. arXiv. https://arxiv.org/abs/2404.04475 — 顯示自動評審偏好較長的答案，並提出長度控制的勝率。
