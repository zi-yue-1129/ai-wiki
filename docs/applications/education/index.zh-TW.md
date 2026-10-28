# 教育

## 概況

| 領域 | 例子 |
|---|---|
| 智慧型教學系統（ITS） | Cognitive Tutor／MATHia（源自 ACT-R）、ASSISTments、AutoTutor |
| LLM 家教 | Khanmigo，以及會引導而非直接給答案的聊天機器人「學習模式」 |
| 適性練習 | 知識追蹤、間隔重複（Duolingo、Anki） |
| 評量 | 自動作文評分、簡答題評分、程式碼回饋 |
| 教師支援 | 課程規劃、差異化教材、批改輔助 |
| 無障礙 | 語音轉文字、文字轉語音、翻譯、簡化文本 |
| 學習分析 | 輟學的早期預警、參與度儀表板 |

## 證據

- **人類一對一家教**效果非常顯著。Bloom 的「2 sigma 問題」（1984）設定了讓團體教學達到一對一家教效果的目標（Bloom, 1984）
- **智慧型教學系統**平均帶來中等程度的學習成效（VanLehn, 2011；Kulik & Fletcher, 2016）
- **LLM 家教**：一項物理課程的隨機試驗發現，依教學最佳實務設計的 AI 家教，比課堂主動學習產生更大的學習成效（Kestin et al., 2025）
- **不加結構的 LLM 使用可能有害**：高中生在無限制使用 GPT-4 時，練習成績較好，但拿掉工具後考試成績變差；家教式的版本則減輕了這種傷害（Bastani et al., 2025, *PNAS*）

## 方法

- **知識追蹤**：貝氏知識追蹤（以隱藏馬可夫模型描述掌握程度）、深度知識追蹤（RNN／Transformer）
- **題目反應理論**用於適性測驗
- **間隔重複**的排程器以遺忘曲線建模（FSRS、SuperMemo）——見[記憶與學習](../../brain-mind/memory-learning/index.md)
- **教學導向的提示與微調**：蘇格拉底式提問、暫時不給答案、檢查理解程度（例如 LearnLM）

## 對 AI 工具的學習科學啟示

| 原則 | 意涵 |
|---|---|
| 提取練習、間隔、交錯學習 | 出測驗並分散安排，而不只是解釋 |
| 合意的困難 | 有成效的掙扎勝過立即的答案 |
| 認知負荷理論 | 把資訊切分成小塊；初學者需要範例解題 |
| 後設認知 | 提示學習者解釋並自我評估 |
| 回饋的時機與具體性 | 針對錯誤給予即時、有針對性的回饋 |
| 動機與歸屬感 | 人際關係仍然是核心 |

## 風險

- **學術誠信**：AI 文本偵測器並不可靠，而且對非母語寫作者有偏見（Liang et al., 2023）；應改為重新設計評量方式
- **認知卸載**與技能退化
- 解釋中的**幻覺內容**
- **兒童資料的隱私**（FERPA、COPPA、GDPR）
- **公平性**：裝置、網路與付費工具的取得不平等
- 自動評分中的**偏見**

## 關鍵方法

下列兩種方法與本頁最相關。每一項都連結到解釋該方法的頁面。

- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md)：用於深度知識追蹤的序列模型，依學習者的歷史預測其下一個回答（Vaswani et al., 2017）。
- [InstructGPT 與 RLHF](../../theory/models/llm/instructgpt-rlhf/index.md)：LLM 家教背後的訓練方法，可調整為引導而非直接給答案（Ouyang et al., 2022）。

## 參考文獻

### 開創性論文

- Bloom (1984). The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring. *Educational Researcher*. https://doi.org/10.3102/0013189X013006004 — 設定了一對一家教優於團體教學的基準。
- Kestin et al. (2025). AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting. *Scientific Reports*. https://doi.org/10.1038/s41598-025-97652-6 — 在物理課程中比較 AI 家教與課堂主動學習的隨機試驗。
- Bastani et al. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. *PNAS*. https://doi.org/10.1073/pnas.2422633122 — 無限制的 GPT-4 使用會損害考試成績，家教式版本可減輕傷害。
- Liang et al. (2023). GPT detectors are biased against non-native English writers. *Patterns*. https://doi.org/10.1016/j.patter.2023.100779 — 顯示 AI 文本偵測器會把非母語英文寫作誤判為機器生成。
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力為核心。
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT，以人類偏好回饋進行指令微調。

### 綜述與教科書

- VanLehn (2011). The Relative Effectiveness of Human Tutoring, Intelligent Tutoring Systems, and Other Tutoring Systems. *Educational Psychologist*. https://doi.org/10.1080/00461520.2011.611369 — 比較人類家教、智慧型教學系統與其他教學系統的效果。
- Kulik & Fletcher (2016). Effectiveness of Intelligent Tutoring Systems. *Review of Educational Research*. https://doi.org/10.3102/0034654315581420 — 智慧型教學系統學習成效的統合分析。
