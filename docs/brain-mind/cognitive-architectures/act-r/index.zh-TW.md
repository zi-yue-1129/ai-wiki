---
status: draft
last_reviewed: 2026-10-28
---

# ACT-R：心智的模組化架構（Anderson 等人，2004）

ACT-R 是一種認知架構：以程式實現的心智計算理論，旨在解釋並預測人類在多種認知任務中的行為。

!!! note "本頁的範圍"
    本頁根據參考文獻中列出的來源撰寫，這些來源都已讀過全文或摘要。標題所指的 2004 年論文並未在此摘述，因此它的詳細主張、方程式與結果都未收錄。機制的段落應視為對此架構的導覽，而非該論文的重現。

## 概覽

**認知架構**（cognitive architecture）是一組固定的機制，共同描述心智的結構與資訊處理方式。其構想是，同一個架構搭配同一組元件，應能解釋許多種任務，而不只是一種。ACT-R 是其中最為人所知的架構之一。Ritter 等人把它描述為由可程式化資訊處理機制組成的混合式認知架構，可用來預測並解釋人類行為，包括認知與和環境的互動。

此架構屬於更廣的[認知架構](../index.md)主題，與 Soar 等相關系統並列，也與[CoALA](../coala/index.md)所討論的代理人架構相關。

## 關鍵概念

- **認知架構**：一組機制，作為心智的一般理論，可在電腦上執行以產生行為。
- **混合式架構**（hybrid architecture）：Ritter 等人用來描述 ACT-R 的用語。其綜述追溯了塑造這種形式的歷史，並與其他架構對照。
- **工作記憶**（working memory）：短期儲存區，保存目前的感知輸入、目標與推理的中間結果。CoALA 論文在描述 Soar 時也使用同一個詞。
- **產生式規則**（production rule）：條件與動作的規則。當條件與工作記憶的內容相符時觸發，其動作會改變工作記憶的內容，或送出指令。這類規則構成產生式系統。
- **心智的標準模型**（standard model of the mind）：Laird 等人提出的社群共識模型，綜合了 ACT-R、Sigma 與 Soar。

## 問題

認知科學與人工智慧長期需要一套單一的心智計算解釋，同時涵蓋感知、記憶、學習與運動控制。為每一種能力分別建模比較容易，但這無法說明這些能力如何彼此配合。

Laird、Lebiere 與 Rosenbloom 描述了達成這種解釋的努力。他們提出的標準模型「涵蓋結構與處理、記憶與內容、學習，以及感知與運動」，並由三個既有的認知架構延伸而成：ACT-R、Sigma 與 Soar。他們的重點是，這些架構在許多方面一致，在另一些方面則分歧；一個共同的參照模型，能讓這種一致與分歧變得清楚可見。

## 核心想法

ACT-R 被呈現為一種以電腦程式實現的認知理論。在 Ritter、Tehranchi 與 Oury 的綜述中，此架構是一組可程式化的資訊處理機制，綜述也描述了使用它的工具。其目標是在具體任務中預測並解釋行為。同一綜述指出，ACT-R 在基礎與應用科學兩方面都有數項重大成果，包括對人類行為的見解。

因此，此架構的可信度取決於其機制預測行為的成效。它的設計是關於心智結構的主張，而不只是建造智慧系統的工具。

## 方程式或演算法

原始論文詳述了 ACT-R 自身的處理循環與方程式，本頁並未重現。本頁所讀來源確實描述了 CoALA 歸於 Soar 的產生式系統循環，而 Soar 是與 ACT-R 密切相關的架構。以下步驟呈現這種一般模式，應理解為此類架構如何運作的示意，而非 ACT-R 的確切程序。

1. 工作記憶保存目前的感知輸入、目標與推理的中間結果。
2. 每條產生式規則把其條件與工作記憶的內容比對。
3. 相符的規則提出候選動作，候選動作再經過評估與排序。
4. 選定的動作被執行。它可能是外部動作，例如運動指令，也可能是內部動作，例如修改記憶。

Soar 的決策循環會評估與工作記憶相符的產生式，並執行其中最相符的一條。ACT-R 有自己的產生式系統，但其精確的循環、時間與記憶方程式屬於原始論文的內容，不在本頁範圍內。

## 結果

Ritter 等人的綜述以一般性的方式描述 ACT-R 的成果：在基礎與應用科學兩方面都有數項重大成果，包括對人類行為的見解。綜述沒有給出單一的基準測試數字，本頁也不給出數字，因為撰寫本版時尚未讀取 2004 年論文的詳細結果。

標準模型論文報告的是另一類結果：綜合 ACT-R、Sigma 與 Soar 之間的一致之處。它指出架構一致與分歧的地方，並說明共識仍不完整的範圍。

## 限制

- **涵蓋不完整。** Ritter 等人的綜述列出了幾個它預期要加入的領域，包括情緒與生理學、可用性，以及非生成式模型的運用。這些是此架構目前呈現方式中的缺口，而非已解決的問題。
- **架構之間的分歧。** 標準模型論文強調 ACT-R、Sigma 與 Soar 在某些方面相異，因此沒有單一架構被接受為完整的解釋。
- **模型建構的選擇。** 認知架構要針對某一任務設定後才能預測行為。本頁所讀的來源並未說明，模型的吻合程度有多少來自架構，有多少來自設定時的選擇。

## 主要方法

- [CoALA](../coala/index.md)（Sumers 等人，2023）：把認知架構的語彙應用於語言代理人。它是概念框架，而非人類行為的模型。
- Soar：產生式系統架構，把產生式儲存於長期記憶，並對照工作記憶加以執行。它是標準模型綜合的三個架構之一。
- Sigma：標準模型綜合中提到的第三個架構。它與其他架構一樣，目標是心智的共同解釋，但本頁所讀的來源未描述其細節。

## 連結

- 母頁：[認知架構](../index.md)
- 同一主題的另一方法：[CoALA](../coala/index.md)
- [記憶與學習](../../memory-learning/index.md)：大腦的記憶系統，認知架構如 ACT-R 嘗試在功能層次上對其建模。
- [Building machines that learn and think like people](../../cognitive-science/building-machines-like-people/index.md)：Lake 等人主張，類人學習需要因果模型、直覺理論與組合性，這對任何架構都是高要求。
- [心理學與 AI](../../psychology/index.md)：ACT-R 等架構所依據並加以檢驗的認知心理學傳統。
- [全域工作空間](../../consciousness/global-workspace/index.md)：另一種心智的架構理論，較著重於資訊如何在整個系統中共享。
- [AI 代理人](../../../theory/models/agents/index.md)：在環境中採取行動的系統，CoALA 以類似架構的類別來分類它們。

大腦方面的連結屬於概念層次。標準模型論文以涵蓋認知科學與神經科學為寫作目標，正如其標題所述，因此這些架構被期望與兩個領域的解釋相互比較。

## 應用

- **人類行為建模**：如 Ritter 等人所述，ACT-R 被用來解釋並預測實驗室任務與應用情境中的表現。
- **研究的共同參照**：標準模型為人工智慧、認知科學、神經科學與機器人學的研究者提供一組可供比對的共同元件。
- **代理人設計**：CoALA 借用認知架構的記憶與決策循環語彙，來組織現代的語言代理人。

## 未解問題

- **單一架構能否作為標準模型？** Laird 等人提出一個共識模型，但指出它本身並不是一個架構，並列出需要解決的分歧。
- **情緒與生理學。** 如 Ritter 等人所建議，這些要素應如何加入目前以認知為核心的模型？
- **可用性。** 研究者要如何更容易地用此架構建立並測試模型？
- **非生成式模型。** 如綜述所建議，不產生行為的模型應如何在此架構中使用？

## 參考文獻

### 開創性論文

- Laird, J. E.、Lebiere, C. 與 Rosenbloom, P. S.（2017）。A Standard Model of the Mind: Toward a Common Computational Framework Across Artificial Intelligence, Cognitive Science, Neuroscience, and Robotics. *AI Magazine*. https://doi.org/10.1609/aimag.v38i4.2744 — 提出由 ACT-R、Sigma 與 Soar 綜合而成的社群共識心智模型，並指出各架構一致與分歧之處。
- Lake, B. M.、Ullman, T. D.、Tenenbaum, J. B. 與 Gershman, S. J.（2017）。Building machines that learn and think like people. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X16001837 — 主張類人學習需要因果模型、物理與心理的直覺理論，以及組合性。
- Park, J. S.、O'Brien, J. C.、Cai, C. J.、Morris, M. R.、Liang, P. 與 Bernstein, M. S.（2023）。Generative Agents: Interactive Simulacra of Human Behavior. arXiv. https://arxiv.org/abs/2304.03442 — 描述一種語言模型代理人，它儲存經驗、對其反思，並檢索這些記憶以規劃可信的行為。
- Sumers, T. R.、Yao, S.、Narasimhan, K. 與 Griffiths, T. L.（2023）。Cognitive Architectures for Language Agents. arXiv. https://arxiv.org/abs/2309.02427 — 依記憶、行動空間與決策程序來組織語言代理人，並借鑑認知架構。

### 綜述與教科書

- Ritter, F. E.、Tehranchi, F. 與 Oury, J. D.（2019）。ACT-R: A cognitive architecture for modeling cognition. *WIREs Cognitive Science*. https://doi.org/10.1002/wcs.1488 — 綜述 ACT-R 的歷史、以電腦程式實現的認知理論、其工具，以及在基礎與應用科學中的成果。
