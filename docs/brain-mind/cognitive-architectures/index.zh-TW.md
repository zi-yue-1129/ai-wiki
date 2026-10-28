---
translation_reviewed: 2026-10-28
---

# 認知架構

**認知架構**是關於心智固定結構（記憶、處理模組、控制）的理論，並以軟體實作，能執行認知任務。它的目標是「統一的認知理論」（Newell, 1990），而不是單一任務的模型。

## 經典架構

| 架構 | 來源 | 關鍵想法 |
|---|---|---|
| **Soar** | Laird、Newell & Rosenbloom（1983 起） | 問題空間；產生式規則；僵局觸發子目標；組塊化學習新規則；後來加入 RL、情節與語意記憶 |
| **ACT-R** | Anderson（1990 年代起） | 模組（視覺、動作、陳述性、目標、想像）經由緩衝區溝通；產生式規則；陳述性記憶的啟動值依近期與頻率而定；模組時序對應腦區並以 fMRI 驗證 |
| **EPIC** | Kieras & Meyer | 細緻的知覺—動作處理；多工 |
| **CLARION** | Sun | 外顯（符號）與內隱（次符號）兩層互動 |
| **LIDA** | Franklin | 實作全域工作空間理論 |
| **Sigma** | Rosenbloom | 以圖模型統一 |
| **Spaun** | Eliasmith（2012） | 250 萬個脈衝神經元的大腦模型，完成八項任務；以神經工程框架建構 |
| **OpenCog／Hyperon** | Goertzel | 以 AGI 為目標的混合架構 |
| **認知通用模型** | Laird、Lebiere & Rosenbloom（2017） | 社群對 Soar、ACT-R、Sigma 共通元件的共識 |

### ACT-R 記憶方程式

陳述性組塊 \(i\) 的啟動值反映它被使用的頻率與近期程度：

\[
A_i = \ln \sum_{j=1}^{n} t_j^{-d} + \text{情境} + \text{雜訊}
\]

其中 \(t_j\) 是第 j 次使用至今的時間，\(d \approx 0.5\)。這能重現冪次遺忘與練習效果，也是一些適應性教學系統的基礎。

## 全域工作空間理論

Baars（1988）提出，許多專門化的無意識處理器會競爭進入容量有限的**全域工作空間**；勝出的內容會廣播給所有處理器，成為有意識的。Dehaene 的**全域神經元工作空間**提供了神經實現（前額葉—頂葉的「點燃」）。它啟發了 AI 中模組之間共享工作空間的提案（Goyal et al., 2022；VanRullen & Kanai, 2021），也是評估 LLM 代理人是否具有與意識相關性質時的一種視角（見 [意識](../consciousness/index.md)）。

## 其他架構層級的理論

- **心智社會**（Minsky, 1986）：心智是許多簡單代理人的集合
- **包容式架構**（Brooks, 1986）：沒有中央表徵、分層的反應式行為——行為導向機器人學
- **千腦理論**（Hawkins）：許多皮質柱各自學習物體模型並投票
- **階層式時間記憶**（Numenta）
- **LeCun 的自主機器智慧提案**（2022）：感知、世界模型、成本、行動者、短期記憶與配置模組

## LLM 代理人作為認知架構

LLM 代理人隱含地重現了認知架構的概念（見 [AI 代理人](../../theory/models/agents/index.md)）。

| 經典元件 | LLM 代理人版本 |
|---|---|
| 工作記憶／緩衝區 | 上下文視窗、草稿區 |
| 陳述性記憶 | 對文件與向量儲存的檢索 |
| 情節記憶 | 記錄的軌跡、反思（Generative Agents 的記憶流） |
| 程序記憶／產生式 | 工具、程式碼、技能庫（Voyager）、系統提示 |
| 決策循環 | 規劃 → 行動 → 觀察的循環（ReAct） |
| 學習（組塊化） | 把成功的程序存成可重用的技能 |
| 後設認知 | 自我批判、信心估計 |

**CoALA**（Sumers, Yao, Narasimhan & Griffiths, 2023）把這個對應系統化。數十年架構研究的實務教訓：明確的記憶管理、控制結構與學習機制，和核心推理引擎一樣重要。

## 為什麼架構仍然重要

- **整合**：真正的智慧把知覺、記憶、推理與行動結合在一個系統中
- **來自人類資料的限制**：反應時間、錯誤模式與學習曲線可以檢驗設計是否像人
- **應用**：智慧教學（Carnegie Learning 的認知導師源自 ACT-R）、航空與國防的人類表現建模、人機互動中的使用者建模
- **可解釋性**：明確的模組與軌跡比單一的大型網路更容易檢視

## 關鍵方法

每個方法各有專頁，此處的概述與比較從簡。

### ACT-R：心智的模組化架構（Anderson 等人，2004）

- **概述：** 獨立的模組透過緩衝區交換資訊，由產生式規則選擇下一步動作。
- **比較：** 是符號式架構。下方的 CoALA 把相同的模組化思路用於語言模型代理人。
- **完整內容：** [ACT-R](act-r/index.md)

### CoALA：語言代理人的認知架構（Sumers 等人，2023）

- **概述：** 為語言模型設計的代理人，具有模組化記憶與一組內部動作。
- **比較：** 把 ACT-R 式的模組化記憶改用於語言代理人。兩者是被比較的，而非合併的。
- **完整內容：** [CoALA](coala/index.md)

## 學習資源

- Newell,《Unified Theories of Cognition》（1990）
- Anderson,《How Can the Human Mind Occur in the Physical Universe?》（2007）
- Laird,《The Soar Cognitive Architecture》（2012）
- Kotseruba & Tsotsos (2020), "40 years of cognitive architectures", *Artificial Intelligence Review*
- [ACT-R 網站](http://act-r.psy.cmu.edu/)、[Soar 網站](https://soar.eecs.umich.edu/)
- Eliasmith,《How to Build a Brain》（Spaun）

## 參考文獻

### 開創性論文

- Anderson, J. R., 等人（2004）。An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R，在單一系統中模擬記憶、目標與學習的認知架構。
- Laird, J. E., Lebiere, C. & Rosenbloom, P. S.（2017）。A Standard Model of the Mind: Toward a Common Computational Framework. *AI Magazine*. https://doi.org/10.1609/aimag.v38i4.2744 — 提出 Soar、ACT-R 與 Sigma 共通元件的社群共識。
- Lake, B. M., 等人（2017）。Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — 主張類人學習需要因果模型、直覺理論與組合性。

### 綜述與教科書

- Kotseruba, I. & Tsotsos, J. K.（2020）。40 years of cognitive architectures: core cognitive abilities and practical applications. *Artificial Intelligence Review*. https://doi.org/10.1007/s10462-018-9646-y — 依涵蓋的認知能力與實際應用，綜述各種認知架構。
- Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L.（2023）。Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — 提出 CoALA，以記憶、行動與決策來組織語言代理人的框架。
