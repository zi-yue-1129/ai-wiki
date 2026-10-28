# AI 用於 AI 研究

研究人員現在使用 AI 閱讀文獻、撰寫並執行程式、設計實驗與草擬論文。有些團隊已建立試圖走完整個循環的系統，而基準測試也開始衡量代理人能否重現或延伸已發表的研究。AI 能否加速自身的改進，是一個被認真討論的可能性，既被視為機會，也被視為風險來源。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 文獻回顧與搜尋 | 以論文為對象的檢索增強問答 | 引用準確度是主要顧慮 |
| 想法生成 | 語言模型提出研究方向 | 人類研究顯示，新穎性與品質的表現參差不齊 |
| 實驗設計與執行 | 撰寫、執行與除錯實驗的程式代理人 | 需要沙箱與運算預算 |
| 端到端研究代理人 | 生成想法、執行實驗並撰寫論文的系統 | The AI Scientist（Lu et al., 2024） |
| 研究能力基準 | 取材自機器學習工程與論文重現的任務 | MLE-bench、PaperBench |
| 軟體工程代理人 | 解決真實程式庫問題的代理人 | SWE-bench（Jimenez et al., 2024） |

## 自動化研究循環如何運作

典型的系統會提出一個想法，撰寫程式來測試它，執行實驗，閱讀結果，再決定下一步要嘗試什麼。有些系統還會草擬論文並自我審閱。每個步驟都可能使用語言模型，而實驗執行器與評估仍是傳統程式碼，使結果可以被檢查。

## 為什麼困難

- **評估是瓶頸**：判斷一個研究想法是否好，需要專家的時間，而自動評審可能被愚弄。
- **可重現性**：代理人可能回報無法重現的結果，或結果依賴於評估中的錯誤。
- **運算與成本**：每個實驗都要消耗資源，對大量想法進行搜尋會讓成本成倍增加。
- **新穎性**：看似新的想法，可能與系統沒有找到的既有工作非常接近。

## 關鍵方法

- [LLM 代理人](../../theory/models/agents/index.md)：在迴圈中規劃、使用工具並觀察結果，是研究代理人的核心。
- [思維鏈推理](../../theory/models/reasoning/chain-of-thought.md)：逐步推理，研究代理人用來規劃實驗。
- [大型語言模型](../../theory/models/llm/index.md)：負責閱讀論文與撰寫程式的語言元件。
- [評估與基準](../../engineering/evaluation/index.md)：如何衡量研究能力，以及基準在哪裡會誤導人。

## 相關連結

- 研究團隊使用的程式代理工具見[AI 程式助手](../../engineering/coding-assistants/index.md)與[軟體開發](../software/index.md)。
- 物理與生物領域的自動化科學見[科學發現](../science/index.md)。
- 遞迴式自我改進的爭論，以及它帶來的安全問題，見[安全與對齊](../../society/safety-alignment/index.md)。

## 應用

- 文獻回顧與摘要
- 撰寫並執行實驗程式
- 生成並篩選研究想法
- 重現已發表的結果，作為對論文的檢查
- 自動化機器學習工程任務

## 風險與限制

- **不可靠的報告**：自動產生的論文可能含有難以察覺的錯誤。
- **評估操弄**：一個針對可量測目標做最佳化的代理人，可能會利用這個量測。
- **研究誠信**：AI 撰寫的論文數量龐大，對同儕審查造成壓力。
- **遞迴式改進**：如果 AI 系統能改進 AI 研究，進步速度與監督的需求都會改變。專家對於這種情況多快會發生、有多可能發生，看法不一。

## 開放問題

- 在受控條件下評估時，AI 生成的想法比人類研究者的想法更新穎或更有用，還是較不新穎或較不有用。
- 如何設計不易被操弄的研究能力基準。
- 對於能獨立執行後繼系統研究的 AI，應施加什麼樣的監督。

## 參考文獻

### 開創性論文

- Lu, C. et al. (2024). The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv. https://arxiv.org/abs/2408.06292 — 描述一個從生成想法、撰寫程式、執行實驗到草擬論文都能端到端完成的系統。
- Si, C., Yang, D. & Hashimoto, T. (2024). Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers. arXiv. https://arxiv.org/abs/2409.04109 — 在受控研究中，比較專家對語言模型與人類研究想法的評審結果。
- Jimenez, C. E. et al. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? *ICLR*. https://arxiv.org/abs/2310.06770 — 以真實軟體問題為題的基準，衡量代理人能否產生可運作的程式庫修正。

### 綜述與教科書

- Chan, J. S. et al. (2024). MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering. arXiv. https://arxiv.org/abs/2410.07095 — 取材自機器學習工程競賽的基準，用以衡量代理人在真實機器學習任務上的能力。
- Starace, G. et al. (2025). PaperBench: Evaluating AI's Ability to Replicate AI Research. arXiv. https://arxiv.org/abs/2504.01848 — 基準中，代理人要重現機器學習論文的結果，並依作者制定的評分表評分。
- Huang, Q. et al. (2023). MLAgentBench: Evaluating Language Agents on Machine Learning Experimentation. arXiv. https://arxiv.org/abs/2310.03302 — 針對語言代理人的實驗任務基準，涵蓋閱讀、撰寫程式與迭代機器學習專案。
- Wei, J. et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS*. https://arxiv.org/abs/2201.11903 — 顯示逐步推理的範例能大幅提升語言模型在多步驟問題上的表現。
