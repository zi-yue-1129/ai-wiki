---
translation_reviewed: 2026-10-28
---

# 認知科學

認知科學把心智當作資訊處理系統來研究，結合心理學、神經科學、語言學、哲學、人類學與 AI。

## 主要理論框架

| 框架 | 核心主張 | 時期 |
|---|---|---|
| 行為主義 | 只研究可觀察的行為（Watson、Skinner） | 1910s–1950s |
| 認知主義／計算主義 | 心智操作符號表徵（Newell & Simon、Fodor） | 1950s– |
| 連結主義 | 認知從簡單單元的網路中湧現（Rumelhart & McClelland, PDP） | 1980s– |
| 貝氏認知科學 | 認知近似機率推論（Tenenbaum、Griffiths、Chater） | 2000s– |
| 具身、嵌入、生成、延展（4E） | 認知依賴身體、環境與行動（Varela、Clark） | 1990s– |
| 預測處理 | 大腦是階層式的預測機器（Friston、Clark、Hohwy） | 2000s– |

## 知覺

- **知覺是推論**：視網膜影像不足以決定外在世界；大腦結合先驗（Helmholtz 的「無意識推論」）
- **完形原則**：接近、相似、封閉、良好連續
- **兩條視覺路徑**：腹側「是什麼」、背側「在哪裡／怎麼做」（Ungerleider & Mishkin；Goodale & Milner）
- **錯覺**揭露大腦的假設；有些深度網路也有同樣的錯覺，有些則暴露不同的假設

## 注意力

- 選擇性注意：過濾理論（Broadbent）、特徵整合理論（Treisman）
- 由下而上的顯著性 vs 由上而下的目標
- 容量有限；**不注意盲視**（「看不見的大猩猩」）
- 神經機制：增益調節、偏向競爭（Desimone & Duncan）、振盪同步
- Transformer 的注意力借用了這個詞，但機制不同——是學出來、依內容加權的機制，除了算力外沒有容量限制

## 語言

- **能力 vs 表現**（喬姆斯基）；「刺激貧乏」論證支持先天語法
- **基於使用與統計學習**的觀點（Tomasello；Saffran）
- 處理：漸進、預測性、對驚訝度敏感；ERP 成分 N400（語意）與 P600（句法）
- **語言網路**（Fedorenko）對語言有選擇性，可與推理、數學、社會認知分離——對解讀 LLM 能力很重要
- LLM 重新點燃了可學性、組合性與意義的辯論；見 [NLP](../../models/nlp/index.md) 與 [LLM](../../models/llm/index.md)

## 概念與類別

- 古典（定義）觀 → 原型觀（Rosch）→ 範例觀 → 理論觀
- **具身／落地的概念**：理解「踢」會活化運動區（Barsalou；Pulvermüller）
- **概念隱喻**（Lakoff & Johnson）：抽象思考建立在身體經驗上
- **組合性與系統性**（Fodor & Pylyshyn, 1988）——長期對神經網路的挑戰；近年元學習研究顯示網路可以習得類似人類的系統性泛化（Lake & Baroni, 2023, *Nature*）

## 推理與決策

- 演繹、歸納、溯因推理；心智模型（Johnson-Laird）
- 捷思與偏誤（Kahneman & Tversky）；有限理性（Simon）；生態理性（Gigerenzer）
- **雙歷程理論**——見 [心理學與 AI](../psychology/index.md)
- **類比**是認知核心（Hofstadter；Gentner 的結構映射）
- 兒童與成人的**因果推理**（Gopnik；Sloman）

## 預測處理與自由能原理

**預測編碼**（Rao & Ballard, 1999）：皮質每一層預測下一層的活動，只有**預測誤差**往上傳。學習就是最小化預測誤差。

**自由能原理**（Friston）：自組織系統最小化變分自由能——驚訝度的上界。依此觀點：

- **知覺**更新信念以解釋感官輸入（變分推論）
- **行動**改變世界讓輸入符合預測（**主動推論**）
- **注意力**是對預測誤差的精確度加權

與 AI 的連結：變分自編碼器最佳化同一個自由能（ELBO）目標；自監督預測學習類似預測編碼；主動推論是獎勵最大化 RL 之外的另一種框架。批評者認為自由能原理太過一般而難以否證；支持者則視它為統一框架。

## 發展

- **皮亞傑的階段論**——影響深遠但已被修正
- **核心知識**（Spelke）：嬰兒很早就有物體、主體、數量、空間的系統
- **兒童是科學家**（Gopnik）：兒童透過實驗學習，像貝氏學習者
- **社會學習**與共同注意（Tomasello）
- AI 的啟示：課程、內在動機、具身與社會互動的角色；「能不能造一台像孩子一樣學習的機器？」（圖靈在 1950 年就提過）

## 打造像人一樣思考的機器

Lake、Ullman、Tenenbaum 與 Gershman（2017）〈Building machines that learn and think like people〉主張 AI 應納入：

1. **直覺物理與直覺心理學**（「開機軟體」）
2. **組合性**
3. **學會學習**
4. **因果模型**，而不只是模式辨識

至今仍是評估現代模型的重要清單。

## 關鍵方法

### 啟發法與偏誤（Tversky & Kahneman，1974）

- **問題：** 在無法精確計算答案時，人們如何判斷機率與頻率？
- **核心想法：** 不確定情況下的判斷依賴少數啟發法，即代表性、可得性，以及錨定與調整。每一種通常都有用，但也會產生系統性的錯誤。
- **方法：** 以說明性的問題與實驗進行，將受試者的判斷與機率論給出的答案相比較。
- **結果：** 判斷會朝可預測的方向偏離規範性答案。例子包括：當描述看起來像某類別時，會忽略基礎比率；估計值會被任意的起始值拉過去。
- **限制：** 啟發法是以文字描述，並非形式化模型，因此論文沒有說明每種啟發法確切適用於何時。後續研究認為，許多啟發法是適應性的，而不只是有偏誤。

### 打造像人一樣學習與思考的機器（Lake 等人，2017）

- **問題：** 為什麼深度網路需要的資料比人多得多？它們在學什麼、怎麼學的方面，與人有何不同？
- **核心想法：** 提出三個要素：世界的因果模型；以物理與心理的直覺理論為基礎的學習；以及組合性與學習如何學習，使模型能快速泛化到新任務。
- **方法：** 這是附有公開評論的目標文章，主張上述三個要素。其證據是對既有模型與實驗的回顧，並以一個從單一範例學習手寫字符的模型作為實例。
- **結果：** 本文是立場論文，沒有報告新的基準結果。
- **限制：** 各評論對機器需要多少內建結構的看法不一。2017 年後大型模型的進展，也改變了這套論點有多少仍然適用。

## 學習資源

- Bermúdez,《Cognitive Science: An Introduction to the Science of the Mind》
- Thagard,《Mind: Introduction to Cognitive Science》
- [Stanford Encyclopedia of Philosophy：Cognitive Science](https://plato.stanford.edu/entries/cognitive-science/)
- Clark,《Surfing Uncertainty》（預測處理）
- Griffiths, Chater & Tenenbaum,《Bayesian Models of Cognition》
- MIT 9.66《Computational Cognitive Science》（OCW）

## 參考文獻

### 開創性論文

- Miller, G. A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*. https://doi.org/10.1037/h0043158 — 工作記憶容量的經典論述，以及組塊如何擴展這個容量。
- Anderson, J. R., et al. (2004). An Integrated Theory of the Mind. *Psychological Review*. https://doi.org/10.1037/0033-295X.111.4.1036 — ACT-R，在單一系統中模擬記憶、目標與學習的認知架構。
- Lake, B. M., et al. (2017). Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — 目標文章，主張類人學習需要直覺物理、直覺心理學與組合模型，並附有評論。
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X12000477 — 將預測處理視為感知、行動與認知統一框架的綜述。
- Tversky, A. & Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. *Science*. https://doi.org/10.1126/science.185.4157.1124 — 記錄可得性與代表性等捷思法，如何影響人在不確定情境下的判斷。
