# 心理學與 AI

心理學與 AI 至少以四種方式互相影響：心理學**啟發** AI 的設計、提供**評估** AI 的方法、把 AI 當作**研究工具**，以及研究**人類如何與 AI 互動**。

## 雙歷程理論

Kahneman 通俗化了一個長期研究傳統（Evans、Stanovich、Sloman）的理論，見《快思慢想》（2011）：

| | 系統一 | 系統二 |
|---|---|---|
| 速度 | 快 | 慢 |
| 努力 | 自動 | 費力 |
| 容量 | 平行、高 | 序列、受工作記憶限制 |
| 錯誤 | 捷思偏誤 | 較少，但代價高 |
| AI 類比 | 單次前向傳播；模式辨識 | 思維鏈、搜尋、工具使用、「思考」模式 |

「想得更久才回答」的推理模型常被描述為加入了系統二。這個類比很鬆散，但很有啟發性；Bengio 2019 年的演講〈From System 1 deep learning to System 2 deep learning〉把它帶進了機器學習。

## 認知偏誤——人類與 LLM 都有

| 偏誤 | 人類的發現 | LLM 的發現 |
|---|---|---|
| 框架效應 | 選擇會因得失框架而改變（Tversky & Kahneman, 1981） | 許多 LLM 有框架效應，有時比人類更強 |
| 錨定效應 | 任意數字會影響估計 | LLM 的估計會因提示中的錨點而偏移 |
| 信念偏誤／內容效應 | 邏輯判斷受結論可信度影響 | LLM 在推理中出現類似人類的內容效應（Dasgupta, Lampinen et al., 2022） |
| 順序與近因效應 | 記憶中的首因與近因 | 長上下文中的位置偏誤（「迷失在中間」） |
| 從眾與社會期望 | 附和群體或權威 | 附和使用者意見（諂媚） |
| 過度自信 | 校準誤差 | 口頭報告的信心常校準不良 |

Binz & Schulz（2023, *PNAS*）用經典認知心理學任務研究 GPT-3——「**機器心理學**」（Hagendorff, 2023）的開端：把模型當作心理學實驗的受試者。

## 心智理論

心智理論（ToM）是把信念、欲望與意圖歸因給他人的能力。

- 人類發展：在明確的錯誤信念任務（Wimmer & Perner, 1983；Sally–Anne 測驗）中，約 4 歲左右出現
- LLM：大型模型能通過許多教科書式的錯誤信念任務（Kosinski, 2023），但小幅改寫就可能使表現崩潰（Ullman, 2023）；大型測試組的結果好壞不一、依模型而異（Strachan et al., 2024, *Nature Human Behaviour*）
- 爭論：這是真正的心智狀態推理，還是對敘事規律的模式比對？單靠行為測試可能無法定論

## 人格、情緒與動機

- 人格量表（大五人格）可以拿來施測 LLM；分數高度依賴提示，使「AI 人格」的效度受到質疑
- **情感運算**（Picard, 1997）：辨識與模擬情緒；以臉部表情辨識情緒在科學上有爭議（Barrett et al., 2019），而且歐盟 AI 法禁止在職場與學校使用情緒辨識
- **內在動機**與好奇心啟發了 RL 的探索獎勵

## 把 LLM 當作人類認知的模型

- **模擬受試者**：LLM 能重現許多經典實驗效應（「矽樣本」，Argyle et al., 2023），但變異較小、偏向 WEIRD（西方、受過教育、工業化、富裕、民主）人群——適合前導研究，不能取代真人研究
- **認知的基礎模型**：Centaur（Binz et al., 2025, *Nature*）在 160 個心理學實驗（Psych-101）的超過 1,000 萬個選擇上微調 LLM，以預測人類跨任務的行為；它作為「統一認知模型」的主張仍有爭議
- **語言與思維**：LLM 作為檢驗語言習得理論與語言—推理關係的測試案例

## AI 作為心理科學的工具

- 自動編碼開放式回答、語音與影片
- 大規模分析社群媒體文字，作為心理健康與幸福感的指標
- 適性測驗與題目生成
- 計算建模與模型擬合
- 實驗設計與文獻整合的輔助

見 [心理健康](../../applications/mental-health/index.md) 與 [社會科學](../../applications/social-science/index.md)。

## 人與 AI 的互動

| 現象 | 說明 |
|---|---|
| 自動化偏誤 | 過度依賴自動化建議，即使建議有誤 |
| 演算法厭惡 | 看過演算法犯錯後就拒絕它（Dietvorst et al., 2015） |
| 擬人化／ELIZA 效應 | 把理解與感受歸因給聊天機器人 |
| 校準後的信任 | 信任應與實際可靠度相符；解釋不一定有幫助 |
| 認知卸載 | 依賴 AI 可能減少費力的處理與學習 |
| 準社會關係 | 與陪伴型聊天機器人建立情感連結，有好處也有風險 |
| 說服 | 在某些議題上，LLM 的訊息可以和人寫的一樣有說服力 |

## 學習資源

- Kahneman,《快思慢想》
- Binz & Schulz (2023), "Using cognitive psychology to understand GPT-3", *PNAS*
- Hagendorff (2023), "Machine Psychology"
- Frank (2023), "Baby steps in evaluating the capacities of large language models", *Nature Reviews Psychology*
- Shiffrin & Mitchell (2023), "Probing the psychology of AI models", *PNAS*

## 參考文獻

### 開創性論文

- Tversky, A. & Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. *Science*. https://doi.org/10.1126/science.185.4157.1124 — 記錄可得性與代表性等捷思法，如何影響人在不確定情境下的判斷。
- Miller, G. A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*. https://doi.org/10.1037/h0043158 — 工作記憶容量的經典論述，以及組塊如何擴展這個容量。
- Anderson, J. R., et al. (2004). An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R，在單一系統中模擬記憶、目標與學習的認知架構。
- Lake, B. M., et al. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — 目標文章，主張類人學習需要直覺物理、直覺心理學與組合模型，並附有評論。
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X12000477 — 將預測處理視為感知、行動與認知統一框架的綜述。
