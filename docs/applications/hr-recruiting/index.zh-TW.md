---
translation_reviewed: 2026-10-28
---

# 人力資源與招募

AI 現在協助雇主尋找、篩選、排序並評估求職者，從履歷解析器到為錄影面試評分的系統都有。這些工具能減少招募人員處理大量應徵者所花的時間，但它們從過去的招募決策中學習，因此可能大規模地重現那些決策的模式。

## 概述

招募是一條漏斗：職缺公告發布，應徵資料陸續送達，接著挑出短名單、安排面試，最後決定發出或拒絕錄取通知。大型雇主的熱門職缺可能收到數千份應徵，這使自動化很有吸引力。廠商幾乎為每個階段都推出工具：搜尋候選人、解析履歷、比對技能與職缺說明、排程、聊天機器人初篩，以及面試分析。同樣的技術也用於內部調動、績效考核與留才，但本頁聚焦於招募。

其中的利害關係既涉及個人，也涉及法律。被拒絕的應徵者很少知道原因，而一次有瑕疵的篩選，可能讓一段求職過程就此結束，且沒有第二次機會。在許多司法管轄區，就業法禁止以種族、性別等受保護的特徵為由歧視，因此帶有偏見的篩選也是法遵風險。這正是招募成為 AI 監管機關最先點名的領域之一的原因（見[法律、政策與治理](../../society/governance/index.md)）。

## 關鍵概念

- **履歷解析（résumé parsing）**：把以自由文字寫成的文件，抽取成結構化欄位，例如職稱、雇主、日期、學歷與技能。
- **技能比對（skills matching）**：評估求職者的背景與職缺的契合程度，通常是比較兩段文字的學習型向量表示。技能常被對應到共通的分類體系，例如歐洲的 ESCO 分類。
- **自動化就業決策工具（automated employment decision tool，AEDT）**：紐約市偏見稽核法所用的用語，指實質協助或取代人工裁量招募決策的軟體。
- **選取率與影響比（selection rate and impact ratio）**：某一群體的應徵者中，能進入下一階段的比例，再除以選取率最高群體的比例。稽核會跨群體比較這些比值；美國長期沿用的「四分之五法則」（four-fifths rule）是經驗法則，把低於 0.8 的比值視為警訊。
- **目標偏誤（target bias）**：模型被訓練去預測「是否被錄用」或「是否獲得高績效評等」之類的標籤。如果這個標籤本身就反映過去的歧視，那麼即使輸入看起來中立，模型仍會學到歧視。
- **結構化面試（structured interview）**：每位候選人都被問相同的問題，並依同一套評分規準打分的面試。自動化面試分析常宣稱能為這個流程帶來一致性。

## 運作方式

多數招募流程是一連串的決策，每個步驟都可能被自動化：

```mermaid
flowchart LR
    A[職缺公告] --> B[應徵]
    B --> C[解析與技能正規化]
    C --> D[評分與排序]
    D --> E[短名單]
    E --> F[面試或評量]
    F --> G[決策]
```

**正規化**是把雜亂的文字對應到標準詞彙。「資料忍者」與「分析專員」之類的職稱，可能描述的是同一種工作，因此以所涉技能來表示職稱的模型，就能把它們歸為一組。Decorte 等人（2021）顯示，以這種方式表示職稱，比一般的句子編碼器更好。[^1]

**評分**是風險最高的地方。系統可能以過去的應徵資料及其結果來訓練；也可能只比較履歷與職缺說明的嵌入向量，而不使用任何招募結果來訓練；或者提示大型語言模型，為每位候選人評分。每種設計對「好的人選」有不同的假設，而廠商很少公開這些假設。[人職適配](person-job-fit/index.md)一頁描述的就是這類神經網路模型。

**評估**則包括面試、測驗與錄影。自動化面試分析在[獨立的頁面](interview-analysis/index.md)中討論。

最重要的設計問題是目標。招募結果只能觀察到被錄用的人，因此以過去決策訓練的模型，學到的是那些決策，而不是工作本身。這正是亞馬遜履歷篩選系統的核心教訓，該案例記述於[演算法偏見案例研究](../../society/ethics/bias-case-studies.md)。

## 關鍵方法

兩個具代表性的方法展現了不同的路線，各自有獨立的頁面。

- [人職適配（Zhu et al. 2018）](person-job-fit/index.md)：一個神經網路，學習候選人與職缺要求的聯合表示，並估計候選人滿足哪些要求。
- [自動化面試分析（Naim et al. 2015）](interview-analysis/index.md)：一個迴歸框架，從語言、臉部表情與韻律預測面試官的評分。

## 關聯

人在招募中的表現已有大量研究。Bertrand 與 Mullainathan 把虛構的履歷寄給徵才廣告，發現帶有白人常見姓名的履歷，回電率比條件相近、帶有非裔美國人常見姓名的履歷高出約 50%。[^2] 這類結果來自[不確定條件下的人類判斷](../../brain-mind/cognitive-science/heuristics-and-biases/index.md)，人們會依賴快速的第一印象，以及與自己相似的人。Naim 等人發現，第一題被評為高分的受訪者，整體評分也較高，這顯示第一印象在面試中有分量。[^3] 以這類評分訓練的自動化系統，可能會承襲同樣的模式。

自動化也可能使人過度信任分數，這是自動化偏誤的一種形式。這方面的社會科學見[人機互動](../../society/human-ai-interaction/index.md)，更廣的倫理討論則見[倫理與公平](../../society/ethics/index.md)。

技術基礎與其他應用相同。履歷與職缺比對，在模型需要對照職缺說明閱讀長篇文件時，會使用[大型語言模型](../../theory/models/llm/index.md)與[檢索增強生成](../../engineering/rag/index.md)。嵌入式搜尋依賴[向量資料庫](../../engineering/vector-databases/index.md)。公平性主張則取決於[公平性定義](../../society/ethics/fairness-definitions.md)，以及[評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.md)中的評估方法。

## 應用

### 履歷篩選與排序

雇主會使用關鍵字過濾、排序模型，以及越來越多會對照職缺說明閱讀履歷的語言模型。Wilson 與 Caliskan（2024）稽核了數個用於此類檢索的文字嵌入模型。他們以九種職業、超過 500 份履歷與 500 份職缺說明進行測試，結果顯示，在 85.1% 的比較中，模型明顯偏好與白人相關的姓名；只有 11.1% 的比較偏好與女性相關的姓名。在某些比較中，與黑人男性相關的姓名受到不利對待的比例高達 100%。[^4] 作者也發現，文件長度與姓名在訓練語料中的出現頻率會影響結果，因此偏見不只是訓練標籤的問題。

### 技能比對與職稱

以技能為本的招募，嘗試以應徵者具備的技能，而非擔任過的職稱，來媒合人與工作。技能分類體系與職稱正規化，是這類做法的基礎設施。JobBERT（Decorte 等人，2021）從職缺中共同出現的技能，學習職稱的表示，並在職稱正規化上明顯優於一般的文字編碼器。[^1] 以分類體系為基礎的比對，比不透明的分數容易解釋，但它仍取決於分類體系記錄了哪些技能，以及如何加權。

### 面試分析

錄影與錄音面試可以自動評分。Naim 等人（2015）分析了 69 位麻省理工學院大學部實習求職學生的 138 場面試紀錄，並從用詞、臉部表情與語音特徵預測面試官的評分。[^3] Hickman 等人（2022）則在三個樣本、共 1,073 位參與者中，檢驗了自動化的錄影面試人格評估。結果顯示，以面試官評分訓練的模型，效度高於以自我報告訓練的模型，但信度的證據不一致。[^5] 兩項研究都使用研究樣本，因此結果無法說明這類工具在真實應徵者身上的表現。

### 偏見稽核與亞馬遜案例

最為人知的失敗案例，是亞馬遜的實驗性履歷排序系統，它學會了降低帶有女性特徵之應徵者履歷的評分；此案例及其教訓見於[演算法偏見案例研究](../../society/ethics/bias-case-studies.md)。Raghavan 等人（2020）檢視了應徵前評估廠商的宣稱，發現其對效度與偏見測試的揭露有限，而廠商也會在訓練資料與預測目標上做出影響重大的選擇。[^6] 稽核方法，包括依群體拆分的錯誤率與影響比，則說明於[演算法稽核與影響評估](../../society/ethics/algorithmic-auditing.md)。

### 法規：紐約市第 144 號地方法

紐約市的第 144 號地方法自 2023 年 7 月起施行。它要求在招募或升遷中使用 AEDT 的雇主與就業機構，每年委託獨立的偏見稽核、公布結果摘要，並通知求職者使用了此工具。Groves 等人（2024）訪談了參與此制度的 16 位專家與實務工作者。他們的結論是，這套制度尚未建立有效的稽核體系，因為 AEDT 與獨立稽核者等關鍵用語定義不清。[^7]

### 法規：歐盟《人工智慧法》

歐盟《人工智慧法》把用於招募與選才的 AI 列為高風險。其高風險類別列出了篩選應徵資料與評估候選人的就業工具。相關義務包括風險管理、資料治理、技術文件、紀錄保存、人類監督與符合性評估。該法也禁止在職場進行情緒辨識，這與錄影面試工具有關。Veale 與 Zuiderveen Borgesius（2021）分析了執委會的草案，以及草案對就業系統的高風險分類。[^8] 後續的修正案已提出延後其中部分義務，例如所謂的「數位綜合方案」（digital omnibus），因此在做任何合規決定前，應先在[法律與治理頁面](../../society/governance/index.md)查核目前的時程。

## 開放問題

- **稽核能否看見目標偏誤？** 以有偏見的流程之結果所做的指標，可能看起來公平，而流程本身卻不公平。以工作表現等更好的標籤取代，建置成本很高。
- **以語言模型進行的篩選，在不同語言、職業與地區之間是否表現不同？** 目前的證據主要來自英文研究。
- **自動化是減少人的偏見，還是把偏見轉移到別處？** 在同一批應徵者中比較人與機器決策的證據仍然有限。
- **誰負責？** 廠商、雇主與設定工具的人，各自可能承擔部分責任，而法律仍在釐清這種劃分。

[^1]: Decorte 等人（2021），JobBERT。所列的改進是作者在其基準上的結果。
[^2]: Bertrand 與 Mullainathan（2004）報告，白人常見姓名的履歷回電率比非裔美國人常見姓名的履歷高 50%，且此差距在各職業與雇主規模間一致。
[^3]: Naim 等人（2015）報告，對興奮、友善與投入度的面試官評分可以預測，相關係數為 0.75 或更高；第一題的評分也能預測整體評分。樣本規模小，且來自單一大學。
[^4]: Wilson 與 Caliskan（2024）。百分比指的是其稽核中的比較結果，並非真實的招募決策。
[^5]: Hickman 等人（2022）。當模型跨樣本交叉驗證時，信度證據不一致；以自我報告訓練的模型，幾乎沒有信度或效度的證據。
[^6]: Raghavan 等人（2020）。本文是對廠商宣稱的研究，並非對工具本身的測試。
[^7]: Groves 等人（2024）。研究結果來自與參與者的訪談，而非對稽核報告的審閱。
[^8]: Veale 與 Zuiderveen Borgesius（2021）分析的是草案，因此其分類應與通過的文本核對。

## 參考文獻

### 開創性論文

- Bertrand, M. & Mullainathan, S. (2004). *Are Emily and Greg More Employable Than Lakisha and Jamal? A Field Experiment on Labor Market Discrimination*. American Economic Review. https://doi.org/10.1257/0002828042002561 — 現場實驗，把配對的虛構履歷寄給徵才廣告，使用與種族相關的不同姓名，並測量回電率。
- Zhu, C. et al. (2018). *Person-Job Fit: Adapting the Right Talent for the Right Job with Joint Representation Learning*. arXiv 預印本. https://arxiv.org/abs/1810.04040 — 神經網路模型，從歷史應徵資料中學習候選人資格與職缺要求的聯合表示。
- Naim, I. et al. (2015). *Automated Analysis and Prediction of Job Interview Performance*. arXiv 預印本. https://arxiv.org/abs/1504.03425 — 框架，從語言、臉部與韻律特徵預測麻省理工學院面試影片的面試官評分。
- Wilson, K. & Caliskan, A. (2024). *Gender, Race, and Intersectional Bias in Resume Screening via Language Model Retrieval*. arXiv 預印本. https://arxiv.org/abs/2407.20371 — 稽核文字嵌入模型以履歷排序職缺的表現，橫跨九種職業，並回報系統性的姓名差異。

### 綜述與教科書

- Mehrabi, N. et al. (2019). *A Survey on Bias and Fairness in Machine Learning*. arXiv 預印本. https://arxiv.org/abs/1908.09635 — 綜述偏見的來源、公平性定義與應用領域，包括招募。

### 文章與文件

- Raghavan, M., Barocas, S., Kleinberg, J. & Levy, K. (2020). *Mitigating Bias in Algorithmic Hiring: Evaluating Claims and Practices*. FAT* 2020. https://arxiv.org/abs/1906.09208 — 檢視應徵前演算法評估廠商所揭露的效度與偏見測試資訊。
- Groves, L. et al. (2024). *Auditing Work: Exploring the New York City algorithmic bias audit regime*. FAccT 2024. https://arxiv.org/abs/2402.08101 — 對紐約市自動化招募工具偏見稽核制度的訪談研究。
- Hickman, L. et al. (2022). Automated video interview personality assessments: Reliability, validity, and generalizability investigations. *Journal of Applied Psychology*. https://doi.org/10.1037/apl0000695 — 在三個樣本中檢驗以模擬錄影面試訓練的人格評估機器學習模型，發現信度證據不一致。
- Veale, M. & Zuiderveen Borgesius, F. (2021). Demystifying the Draft EU Artificial Intelligence Act. *Computer Law Review International*. https://doi.org/10.9785/cri-2021-220402 — 對執委會 2021 年草案的法律分析，包括草案對就業系統的高風險分類；定案文本在細節上有所不同。
- Decorte, J.-J. et al. (2021). *JobBERT: Understanding Job Titles through Skills*. arXiv 預印本. https://arxiv.org/abs/2109.09605 — 以職缺中的技能來表示職稱，在職稱正規化上優於一般的句子編碼器。
