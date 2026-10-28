---
translation_reviewed: 2026-10-28
---

# Reflexion：以語言進行的強化學習代理人

Reflexion（Shinn 等人，2023）在不更新權重的情況下改進語言代理人。一次失敗的嘗試結束後，代理人會以語言寫下對錯誤原因的反思，存入記憶，並讓下一次嘗試以這些反思為條件。它是 [代理人工程](../index.md)概述頁所列的第二個里程碑方法。

## 概述

強化學習通常透過多次嘗試、調整參數來改進代理人。為每項任務微調大型模型成本高昂，而純量獎勵也很難說明一次嘗試為何失敗。Reflexion 改用語言作為回饋管道：代理人用文字解釋自己為何失敗，並在下一次嘗試前讀取這段解釋。論文在決策、問答與程式生成任務上測試這個方法。

## 關鍵概念

- **行動者（actor）**：產生行動或文字的語言模型，其輸出以記憶為條件。論文也嘗試了只有推理的行動者，以及 [ReAct](../react/index.md)。
- **評估者（evaluator）**：為一段軌跡評分。論文在推理任務中使用精確匹配，在決策任務中使用啟發式規則，在程式任務中使用單元測試，部分設定中也使用另一個語言模型。
- **自我反思模型（self-reflection model）**：讀取失敗的軌跡及其分數，然後寫出一段簡短教訓的語言模型。
- **記憶（memory）**：目前的軌跡是短期記憶，儲存的反思則是長期記憶。論文把長期記憶限制在約一到三則反思的視窗內，以符合脈絡長度的限制。

## 運作方式

論文的演算法 1 依下列步驟進行：

1. 讓行動者執行一次，以評估者為軌跡評分，並把一則初始反思寫入記憶。
2. 只要評估者尚未通過該軌跡，且尚未達到嘗試次數上限，就讓行動者再執行一次，其提示中包含記憶。
3. 為新的軌跡評分，並由它產生自我反思。
4. 把反思加入記憶，然後回到第 2 步。

論文把代理人的策略寫成 $\pi_\theta$，其中 $\theta = \{M_a, \text{mem}\}$，$M_a$ 為行動者模型。模型權重保持不變，學習完全發生在記憶之中。

## 結果

- **程式生成。** 摘要報告 HumanEval 上的 pass@1 為 91%，對照 GPT-4 基準的 80%。[^1]
- **ALFWorld。** 搭配 Reflexion 的 ReAct 完成了 134 個任務中的 130 個。單獨的 ReAct 在第 6 到第 7 次嘗試之間便不再進步，而 Reflexion 則在連續 12 次嘗試中持續學習。[^2]
- **整體摘要。** 論文把它相對於強基準的收益總結為：ALFWorld 上 22%、HotpotQA 上 20%、HumanEval 上 11%。

論文也報告了較弱的結果：在 MBPP Python 上，Reflexion 落後於 GPT-4 基準。

## 限制

- **局部最佳解。** 作者把 Reflexion 描述為以自然語言進行的策略最佳化，它可能停在不佳的解上。
- **記憶有上限。** 滑動視窗限制了能被記住的內容。作者建議以向量或 SQL 儲存作為未來工作。
- **自產生的測試。** 在程式任務中，模型自行撰寫單元測試，而測試可能在錯誤的程式碼上通過。偽陽性率，即程式通過測試後仍然失敗的機率，在 MBPP Python 上為 16.3%，在 HumanEval Python 上為 1.4%。[^3]
- **難以測試的函式。** 具有非確定性、副作用、依賴硬體或並行執行的函式，很難用輸入輸出測試來檢查。
- **成本。** 每一次嘗試都是代理人的一次完整執行，因此收益必須與延遲和成本一併權衡。

## 開放問題

- **反思的品質。** 錯誤的教訓可能留在記憶中，並影響之後的嘗試。如何偵測並淘汰這類教訓，目前尚不清楚。
- **回饋訊號的品質。** 當評估者是語言模型時，它的錯誤會變成代理人的錯誤。
- **記憶設計。** 超出小視窗之後，教訓應如何儲存、檢索，並在不同任務之間合併？
- **遷移。** 一項任務中的反思是否能幫助其他任務，是需要實證的開放問題。

## 參考文獻

### 奠基性論文

- Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. arXiv. https://arxiv.org/abs/2303.11366 — 提出 Reflexion 的論文，在 ALFWorld、HotpotQA、HumanEval 與 MBPP 上有實驗結果。
- Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv. https://arxiv.org/abs/2210.03629 — 決策實驗所使用的推理與行動行動者。
- Shridhar, M. et al. (2020). *ALFWorld: Aligning Text and Embodied Environments for Interactive Learning*. arXiv. https://arxiv.org/abs/2010.03768 — 決策任務結果所依據的文字式家居環境。
- Yang, Z. et al. (2018). *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering*. arXiv. https://arxiv.org/abs/1809.09600 — 推理實驗所用的多跳問答資料集。
- Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv. https://arxiv.org/abs/2107.03374 — 提出 HumanEval，以文件字串描述的 Python 程式題，依功能正確性評分。
- Austin, J. et al. (2021). *Program Synthesis with Large Language Models*. arXiv. https://arxiv.org/abs/2108.07732 — 提出 MBPP 基準，收錄簡短的 Python 程式任務。
- Park, J. S. et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv. https://arxiv.org/abs/2304.03442 — 模擬角色從儲存的經驗中綜合出反思，並以此規劃，是反思在記憶中的另一種用法。

### 文章與文件

- Anthropic (2026). *Demystifying evals for AI agents*. Anthropic Engineering. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — 描述代理人評估中的評分器與追蹤紀錄，與 Reflexion 所依賴的評估者設計相關。

[^1]: Shinn 等人（2023），Reflexion 論文的摘要，https://arxiv.org/abs/2303.11366 — HumanEval 上 91% 的 pass@1，以及與 GPT-4 的 80% 比較的來源。
[^2]: Shinn 等人（2023），Reflexion 論文中的 ALFWorld 結果，https://arxiv.org/abs/2303.11366 — 134 個任務中完成 130 個的來源，以及與單獨 ReAct 逐次嘗試的比較。
[^3]: Shinn 等人（2023），Reflexion 論文中對自產生單元測試的分析，https://arxiv.org/abs/2303.11366 — MBPP Python 與 HumanEval Python 偽陽性率的來源。
