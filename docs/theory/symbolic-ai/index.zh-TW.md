# 符號 AI、搜尋與規劃

## 符號 AI 是什麼？

「好老式 AI」（GOFAI）：用明確的**符號**（概念、規則、邏輯式）表示知識，用**推理**操作符號。Newell 與 Simon 的**物理符號系統假說**（1976）主張：符號系統是一般智慧行為的必要且充分條件。

## 知識表示

| 方法 | 說明 | 例子 |
|---|---|---|
| 命題邏輯、一階邏輯 | 用邏輯式表達事實與規則 | ∀x 人(x) → 會死(x) |
| 產生式規則 | IF-THEN 規則 | 專家系統 MYCIN |
| 語意網路與框架 | 概念節點與關係 | Minsky 的框架理論 |
| 描述邏輯與本體論 | 嚴謹的概念階層 | OWL、醫學 SNOMED CT、基因本體 GO |
| 知識圖譜 | (實體, 關係, 實體) 三元組 | Wikidata、Google Knowledge Graph |
| 常識知識庫 | 日常常識 | Cyc、ConceptNet、ATOMIC |

## 搜尋

| 類型 | 演算法 | 用途 |
|---|---|---|
| 無資訊搜尋 | BFS、DFS、迭代加深、均一成本 | 基礎 |
| 啟發式搜尋 | 貪婪最佳優先、A*、IDA* | 路徑規劃、導航 |
| 對抗搜尋 | Minimax、α-β 剪枝 | 西洋棋（Deep Blue） |
| 蒙地卡羅樹搜尋 MCTS | 隨機模擬＋UCT | 圍棋（AlphaGo） |
| 局部搜尋 | 爬山、模擬退火、禁忌搜尋 | 排程、組合最佳化 |
| 約束滿足 CSP | 回溯、弧一致性 | 數獨、排課 |

A* 的評估函數：\( f(n) = g(n) + h(n) \)，若 \(h\) 不高估（可容許），A* 保證找到最佳解。

## 自動規劃

- **STRIPS / PDDL**：以前提條件與效果描述行動，規劃器自動找出行動序列
- **階層任務網路（HTN）**：把高階任務分解成子任務
- **部分可觀察與機率規劃**：POMDP
- **應用**：物流、太空任務（NASA 的 Remote Agent）、遊戲 AI、機器人任務規劃

## 自動推理與定理證明

- SAT／SMT 求解器（Z3）：晶片驗證、軟體驗證、排程
- 互動式定理證明：Lean、Coq（Rocq）、Isabelle
- **AI × 數學**：LLM 搭配 Lean 自動證明（AlphaProof 在 2024 IMO 達銀牌水準；之後多個系統在 IMO 題目上達到金牌水準）、Mathlib 社群形式化數學

## 符號 AI 的優缺點

| 優點 | 缺點 |
|---|---|
| 可解釋、可驗證 | 知識獲取瓶頸（要人手寫） |
| 能做精確多步推理 | 處理不確定與模糊困難 |
| 小資料即可運作 | 感知（影像、語音）困難 |
| 容易加入硬約束 | 脆弱，遇到規則外情況就失效 |

## 神經符號 AI（Neuro-Symbolic AI）

結合神經網路的感知與學習能力，和符號系統的推理與可解釋性：

- **神經網路＋搜尋**：AlphaGo、AlphaZero
- **LLM＋工具**：LLM 寫程式或呼叫求解器、計算機、資料庫（見 [AI 代理人](../models/agents/index.md)）
- **LLM＋形式驗證**：產生 Lean 證明、程式合成並以測試驗證
- **可微分邏輯**：邏輯張量網路、∂ILP
- **程式歸納**：DreamCoder 從範例學出可重用的程式庫
- **知識圖譜＋LLM**：GraphRAG

認知科學中的對應是**雙歷程理論**：快速直覺的「系統一」像神經網路，緩慢審慎的「系統二」像符號推理（見 [心理學與 AI](../../brain-mind/psychology/index.md)）。也有學者主張人類思考依賴「思維語言」（Fodor）這種符號結構。

## 學習資源

- Russell & Norvig《Artificial Intelligence: A Modern Approach》第 3–11 章
- [aima-python](https://github.com/aimacode/aima-python)（MIT）
- Microsoft AI-For-Beginners 第 2 課（符號 AI）
- Marcus & Davis《Rebooting AI》（神經符號觀點）

## 參考文獻

### 開創性論文

- Garcez, A. d'Avila, & Lamb, L. C. (2020). *Neurosymbolic AI: The 3rd Wave*. arXiv. https://arxiv.org/abs/2012.05876 — 綜述文章，主張結合學習表示與符號推理是 AI 的下一個主要階段。
- Lake, B. M., et al. (2016). *Building Machines That Learn and Think Like People*. arXiv. https://arxiv.org/abs/1604.00289 — 主張類人學習需要直覺理論、組合性與因果模型，並指出模式比對系統的不足之處。

### 綜述與教科書

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — AI 標準教科書，涵蓋搜尋、邏輯、規劃與學習；配套網站提供免費投影片與程式碼。

### 課程與影片

- Winston, P. H. *6.034 Artificial Intelligence*. MIT OpenCourseWare, Fall 2010. https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/ — MIT 錄製的課程，涵蓋知識表示、搜尋與規則式系統，是古典符號 AI 的核心。

### 文章與文件

- Marcus, G. (2020). *The Next Decade in AI: Four Steps Towards Robust Artificial Intelligence*. arXiv. https://arxiv.org/abs/2002.06177 — 批判純統計式 AI，並提出包含結構化知識的混合系統。
