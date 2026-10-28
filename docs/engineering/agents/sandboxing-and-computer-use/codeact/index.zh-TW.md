---
translation_reviewed: 2026-10-28
---

# CodeAct：LLM 代理人的可執行程式碼動作

CodeAct（Wang et al., 2024）讓 LLM 代理人的行動成為一段可執行的 Python 程式碼，由直譯器執行，而不是 JSON 呼叫或一行文字。直譯器提供一個有界限的地方，用來執行並觀察代理人的行動，這也是本方法與沙箱相關的原因。它是 [沙箱與電腦操作代理人](../index.md)頁面中三個里程碑方法之一。

## 概述

多數使用工具的代理人，都以固定格式表達每個行動：一個指定工具與參數的 JSON 物件，或是由解析器對應到函式的一行文字。這種做法簡單，但可能的行動受限於開發者所定義的工具。組合工具也很麻煩。把一個工具的輸出傳給另一個工具，或是對清單中的每一項重複呼叫，每一步都需要一次獨立的模型回合。

CodeAct 以單一的行動空間取代這些格式：可執行的 Python。工具呼叫成為程式碼中的函式呼叫，重複呼叫成為迴圈，一個工具回傳的值可以存入變數，供下一個工具使用。代理人送出程式碼，直譯器執行它，結果再以觀察的形式回到代理人。

## 關鍵概念

- **行動空間（action space）**：代理人在一步之中可以做的事情的集合。CodeAct 把這個集合定義為所有 Python 程式。
- **控制流（control flow）**：迴圈與條件判斷，使一個行動可以處理多個項目。
- **資料流（data flow）**：存放在變數中的值，使一步的輸出可以直接成為下一步的輸入，而不必繞經模型的文字。
- **直譯器（interpreter）**：執行程式碼的 Python 程序。行動在此被執行、觀察，並在需要時受到限制。
- **多回合修正（multi-turn revision）**：代理人可以讀取錯誤或結果，並輸出修正後的行動。

## 運作方式

每一段互動都遵循以下迴圈：

1. 代理人接收使用者的請求，並以 Python 函式的形式描述可用的工具。
2. 模型撰寫一段程式碼，表達其下一個行動或一組行動。
3. 直譯器執行程式碼，擷取輸出、回傳值與錯誤訊息。
4. 擷取的輸出以觀察的形式附加到對話中。
5. 模型撰寫後續程式碼、在錯誤後修正先前的程式碼，或給出最終答案。迴圈在出現最終答案或達到最大回合數時結束。

作者在 M³ToolEval 上評估此方法，這是一組需要多個工具共同運作的問題基準；另在 API-Bank 上評估，測試單次工具呼叫。在 M³ToolEval 上，若答案與參考答案相符即視為成功；論文同時報告平均回合數。作者進一步以 CodeActInstruct 對 Llama 2 與 Mistral 進行微調，建立開源模型 CodeActAgent。CodeActInstruct 是 7,000 段多回合互動，其中的行動皆為程式碼。作者報告，這種訓練可以在不損及一般能力的情況下改善代理人任務。

## 結果

- **M³ToolEval。** 在所評估的 17 個 LLM 中，有 12 個在 CodeAct 下的成功率高於 JSON 或文字基線。摘要報告成功率最多高出 20%，正文則報告行動數最多減少 30%。隨著模型能力提升，差距會擴大。
- **API-Bank。** 在單次工具呼叫上，結果不一。論文的表格顯示，最佳格式因模型而異。
- **CodeActAgent。** 微調後的模型在收到錯誤訊息後，修正行動的能力有限。論文將其視為早期原型。

主要的量化結論取自論文摘要與結果文字。

## 限制

- **原型性質。** 作者指出 CodeActAgent 可能產生幻覺，例如描述一個它從未印出的變數的值。
- **對執行的信任。** 因為代理人會執行程式碼，安全性取決於直譯器周圍的沙箱。論文指出，一個可以自由執行程式碼的代理人，在最壞情況下可能突破其沙箱，並呼籲發展更好的安全機制。
- **基準範圍。** 基準是具有已知答案的工具使用問題，並非在有真實副作用的系統上進行的開放式工作。

## 開放問題

- **邊界應設在哪裡。** 行動空間越豐富，就必須越小心地限制直譯器。能否以模型無法繞過的方式設定檔案、網路與程序的限制，是尚待解決的工程問題，已在[沙箱主題頁](../index.md)中討論。
- **執行前驗證程式碼。** 程式碼可以靜態檢查、依政策核對，或以試執行模式執行。哪一種方式能抓到真正重要的失敗，尚無定論。
- **自我改進。** 作者提出，代理人可以透過延伸的環境互動，從自身錯誤中學習。這是否能在不削弱執行周圍保護機制的前提下成立，目前未知。

## 參考文獻

### 奠基性論文

- Wang, X. et al. (2024). *Executable Code Actions Elicit Better LLM Agents*. arXiv. https://arxiv.org/abs/2402.01030 — 提出 CodeAct，以可執行的 Python 作為 LLM 代理人的統一行動空間，並在 17 個 LLM 上進行評估。
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — 提出推理與行動的迴圈，其行動採用固定的文字格式，CodeAct 即以此為比較對象。

### 綜述與教科書

- Wang, L. et al. (2023). *A Survey on Large Language Model based Autonomous Agents*. arXiv. https://arxiv.org/abs/2308.11432 — LLM 代理人綜述，涵蓋 CodeAct 所要取代的工具與行動格式。

### 文章與文件

- Anthropic (2024). *Building effective AI agents*. Anthropic Engineering. https://www.anthropic.com/engineering/building-effective-agents — 關於代理人迴圈與工具的實用指引，以及何時簡單的工作流程優於自主代理人。
- Anthropic (2025). *Making Claude Code safer with sandboxing*. Anthropic Engineering. https://www.anthropic.com/engineering/claude-code-sandboxing — 說明會執行指令的程式助手，如何受到檔案系統與網路邊界的限制。
