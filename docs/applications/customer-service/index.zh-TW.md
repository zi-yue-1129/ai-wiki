# 客戶服務與對話系統

客戶服務是最早的商業對話式 AI 應用之一，也是規模最大的之一。這個領域從電話語音選單與意圖分類器，發展到能回答問題、操作帳戶並把對話轉交真人的語言模型代理人。關於這些系統是否真正幫助客戶、又如何改變客服人員的工作，證據目前仍然稀少且不一致。

## 概況

| 階段 | 方法 | 說明 |
|---|---|---|
| 語音互動選單 | 按鍵與關鍵字選單 | 仍然常見；成本低，但對複雜需求令人挫折 |
| 意圖分類與槽位填充 | 固定意圖集合上的分類器，搭配以框架為基礎的對話 | Rasa 等框架（Bocklisch et al., 2017） |
| 檢索式回答 | 在知識庫中搜尋，為客服人員提供排序後的答案建議 | 品質取決於知識庫 |
| 生成式助理 | 微調過的語言模型，草擬或直接送出回覆 | 需要防範捏造政策的護欄 |
| 使用工具的代理人 | 呼叫帳戶、訂位與退款工具、並遵循政策的語言模型 | ReAct（Yao et al., 2022）；Toolformer（Schick et al., 2023） |
| 客服輔助 | 為真人客服即時提供建議、摘要與通話後紀錄 | 通常是最先部署的形式，由真人保持在迴圈中 |

## 部署系統的結構

多數正式系統把語言模型與確定性的檢查結合起來。模型理解訊息並草擬回覆。政策層決定模型可以做什麼，例如退款上限、身分驗證與轉接規則。紀錄會回饋到評估集，失敗的對話則轉交真人處理。

## 為什麼困難

- **政策遵循**：一個樂於助人卻忽略退款規則或揭露義務的代理人，會造成真實的法律責任。
- **工具可靠性**：一段看起來流暢的對話，仍可能根本沒有改變帳戶內容。
- **衡量**：解決率與處理時間容易衡量，客戶滿意度與解決品質則較難衡量。
- **轉接**：知道何時轉接，並在轉接時帶上完整脈絡，是設計問題，不只是模型問題。

## 關鍵方法

- [LLM 代理人](../../theory/models/agents/index.md)：在迴圈中規劃、呼叫工具並觀察結果的語言模型。
- [檢索增強生成](../../engineering/rag/index.md)：讓答案以政策文件與產品手冊為依據。
- [指令微調與 RLHF](../../theory/models/llm/instructgpt-rlhf/index.md)：使助理遵循指令並保持在任務上的訓練方法。
- [評估與基準](../../engineering/evaluation/index.md)：對代理人進行以任務為本的測試，例如 τ-bench（Yao et al., 2024），它模擬遵循政策的客戶。

## 相關連結

- 專家的語言介面與 LLM 助理的一般論點，見[大型語言模型](../../theory/models/llm/index.md)。
- 銀行的理財建議與客服有所重疊，見[金融](../finance/index.md)。
- 人們如何判斷對話夥伴是否有幫助、是否可信，是[心理學與 AI](../../brain-mind/psychology/index.md)的問題，包括人們如何回應一台聽起來像人的機器。

## 應用

- 帳戶、帳單與訂單狀態查詢
- 真人客服中心的客服輔助
- 通話後摘要與品質審查
- 針對退貨、續約與提醒的主動外展

## 風險與限制

- **捏造政策**：模型可能承諾不存在的退款或服務。
- **服務不均**：自動化的前門可能讓真人更難接觸，而最需要真人的客戶受影響最大。
- **勞動影響**：Brynjolfsson 等人（2023）對大型客服團隊中生成式助理的研究發現，生產力提升主要集中在經驗較少的客服人員身上，但勞動結果仍取決於企業如何運用這些工具。
- **揭露**：許多司法管轄區要求告知使用者正在與機器對話。

## 開放問題

- 哪些指標最能反映客戶的問題是否真正解決，而不只是對話是否結束。
- 如何設定轉接門檻，在成本與不同客戶群體的公平之間取得平衡。

## 參考文獻

### 開創性論文

- Budzianowski, P. & Vulić, I. (2019). Hello, It's GPT-2 — How Can I Help You? Towards the Use of Pretrained Language Models for Task-Oriented Dialogue Systems. arXiv. https://arxiv.org/abs/1907.05774 — 展示如何以少量資料，把預訓練語言模型微調為任務導向的客服對話。
- Bocklisch, T. et al. (2017). Rasa: Open Source Language Understanding and Dialogue Management. arXiv. https://arxiv.org/abs/1712.05181 — 介紹用於正式助理的意圖分類與對話管理開源框架。
- Yao, S. et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. arXiv. https://arxiv.org/abs/2210.03629 — 把推理步驟與工具動作交錯進行，是多數客服代理人所採用的模式。
- Schick, T. et al. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. arXiv. https://arxiv.org/abs/2302.04761 — 展示語言模型能學會何時、如何呼叫外部 API。

### 綜述與教科書

- Yao, S. et al. (2024). τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. arXiv. https://arxiv.org/abs/2406.12045 — 模擬客戶與代理人在領域政策下互動的基準，衡量代理人是否達到正確結果。
- Brynjolfsson, E., Li, D. & Raymond, L. (2023). Generative AI at Work. *NBER Working Paper 31161*. https://doi.org/10.3386/w31161 — 對客服人員使用生成式助理的實地研究，不同經驗水準的收益並不相同。
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. arXiv. https://arxiv.org/abs/2203.02155 — 以人類回饋進行指令微調，是多數已部署助理的訓練方法。
