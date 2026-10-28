---
translation_reviewed: 2026-10-28
---

# ReAct：語言模型中的推理與行動

ReAct（Yao 等人，2022）引導一個參數凍結的語言模型，把它的推理以文字寫在各個行動之間。每一個思考引導下一個行動，而環境回傳的每一個觀察則修正下一個思考。它是 [代理人工程](../index.md)概述頁所列的兩個里程碑方法之一。

## 概述

兩條研究路線各自發展。思維鏈提示讓模型以文字推理，但沒有外部資訊時，這種推理可能漂移成捏造的事實。另一些工作讓模型在環境中行動，但若缺乏明確的規劃，代理人可能會失去子目標的追蹤。ReAct 的問題是：一個提示能否把兩者結合起來。

## 關鍵概念

- **思考（thought）**：不改變環境的自由文字推理步驟，例如規劃、子目標或對例外狀況的註記。
- **行動（action）**：查詢或改變環境的步驟，例如一次搜尋或一則遊戲指令。
- **觀察（observation）**：環境在行動之後回傳的文字。
- **脈絡（context）**：模型到目前為止看過的全部內容。每一個新步驟都是依據脈絡產生的。
- **少樣本軌跡（few-shot trajectories）**：由人撰寫的示範執行過程，放在提示中新任務之前。

## 運作方式

論文描述一個代理人，它在每個時間點接收觀察 $o_t$，並從策略 $\pi(a_t \mid c_t)$ 中選擇行動 $a_t$，其中 $c_t = (o_1, a_1, \dots, o_{t-1}, a_{t-1}, o_t)$ 是脈絡。ReAct 把行動空間擴大為 $\hat{\mathcal{A}} = \mathcal{A} \cup \mathcal{L}$，其中 $\mathcal{L}$ 是語言空間。思考 $\hat{a}_t \in \mathcal{L}$ 不產生觀察，它只把脈絡延伸為 $c_{t+1} = (c_t, \hat{a}_t)$，使之後的步驟能夠使用它。

實際的迴圈如下：

1. 建立提示，內含幾個示範用的思考、行動與觀察序列，後面接著新任務。
2. 向凍結參數的模型要求下一個輸出，可能是思考，也可能是行動。
3. 若輸出是行動，就執行它，並把觀察加入脈絡。在問答中，行動包括維基百科搜尋、在目前頁面中查找，以及一個結束動作。
4. 重複執行，直到出現結束動作或達到步數上限。

在問答中，思考與行動交替出現。在行動很多的決策任務中，模型自行決定何時需要思考。格式本身並不要求每次行動前都先推理，因此示範範例承擔了大部分的行為塑造。

## 結果

主要實驗使用一個擁有 5,400 億參數、參數凍結、以少樣本範例提示的語言模型。

- **問答（HotpotQA）。** ReAct 優於只有行動的基準。與思維鏈相比，它的精確匹配略低（27.4 對 29.4）[^1]，但答案更以檢索到的文字為依據。作者的樣本中，幻覺是思維鏈的主要失敗模式。
- **決策（ALFWorld）。** 最佳的 ReAct 試驗達到 71% 的平均成功率。最佳的只有行動的試驗為 45%，而 ALFWorld 論文所提出的模仿學習代理人 BUTLER 為 37%。[^2]
- **微調。** 以約 3,000 筆訓練範例微調後，在 HotpotQA 上，微調過的 ReAct 成為所比較的四種方法中最好的一種。在較小規模、僅靠提示時，它則是最弱的。

## 限制

- **結構僵硬。** 交錯的格式限制了自由推理。在 HotpotQA 上，作者計算出的推理錯誤比思維鏈更多。
- **陷入迴圈。** 模型有時會重複先前的思考與行動，而不離開迴圈。作者推測，所用的貪婪解碼可能是原因之一。
- **依賴搜尋品質。** 無效的搜尋佔所研究錯誤案例的 23%，並會打亂之後的推理。[^3]
- **受控環境。** 文字式與沙箱式的任務，對開放式的真實系統說明有限。
- **無法跨嘗試學習。** ReAct 不會利用失敗嘗試的結果來改變下一次嘗試。[Reflexion](../reflexion/index.md) 正是針對這個缺口。

## 開放問題

- **何時思考、何時行動。** 論文把這個選擇交給模型。是否能學到或指定更好的策略，仍然未知。
- **會推理的模型。** 許多現今模型會在回答前進行長篇推理。當推理在模型內部完成時，ReAct 的收益還剩多少，是需要實證的問題。
- **提示或訓練。** 微調結果顯示，從軌跡中學習可能更能泛化，但證據僅涵蓋少數任務。

## 參考文獻

### 奠基性論文

- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — 提出 ReAct 的論文，在問答與互動式決策任務上進行實驗。
- Shridhar, M. et al. (2020). *ALFWorld: Aligning Text and Embodied Environments for Interactive Learning*. arXiv. https://arxiv.org/abs/2010.03768 — 決策實驗所用的文字式家居環境，並提出 BUTLER 代理人。
- Yang, Z. et al. (2018). *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering*. arXiv. https://arxiv.org/abs/1809.09600 — 問答實驗所用的多跳問答資料集。
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 提出思維鏈提示，也就是 ReAct 加上行動後所擴充的、只有推理的基準。

### 綜述與教科書

- Wang, L. et al. (2023). *A Survey on Large Language Model based Autonomous Agents*. arXiv. https://arxiv.org/abs/2308.11432 — 綜述 LLM 代理人，涵蓋記憶、規劃與行動，也就是 ReAct 式迴圈所處的情境。

### 文章與文件

- Anthropic (2024). *Building effective AI agents*. Anthropic Engineering. https://www.anthropic.com/engineering/building-effective-agents — 關於建構此類代理人迴圈的實用指引，以及何時較簡單的工作流程更為適合。

[^1]: Yao 等人（2022），ReAct 論文的表 1 與結果文字，https://arxiv.org/abs/2210.03629 — 以大型凍結模型進行提示的 HotpotQA 結果，此處的精確匹配數字即取自於此。
[^2]: Yao 等人（2022），ReAct 論文中 ALFWorld 的結果，https://arxiv.org/abs/2210.03629 — 最佳 ReAct 試驗、最佳僅行動試驗與 BUTLER 的成功率，依作者所報告的數字。
[^3]: Yao 等人（2022），對抽樣 HotpotQA 軌跡的錯誤分析，https://arxiv.org/abs/2210.03629 — 作者歸因於無效搜尋的錯誤案例所佔比例。
