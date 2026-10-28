---
related:
- society/governance
- society/safety-alignment
- theory/models/computer-vision
- theory/paradigms/reinforcement-learning
aliases:
  - 軍事
  - 國防
  - Defence
---

# 軍事與國防

AI 在國防上用於情報分析、後勤、規劃、模擬與訓練，近年也越來越多用於平台與武器的自主功能。公共討論多集中在最後一項，但軍事 AI 的大部分支出其實流向前面幾項。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 情報、監視與偵察（ISR） | 對衛星、無人機與雷達影像做電腦視覺與多感測器融合；對訊號做異常偵測 | 分析人員面對的資料遠超過能審閱的量；偵測品質與誤報率決定實用價值 |
| 後勤與維護 | 需求預測、載具與飛機的預測性維護 | 較不顯眼，卻常是最早的大規模部署 |
| 規劃與決策支援 | 最佳化、模擬，以及摘要報告的語言模型 | 通常由人審閱；風險在於過度信任 |
| 訓練與模擬 | 在模擬器中做強化學習、合成環境 | 模擬到真實的轉移是主要缺口 |
| 網路防禦 | 入侵偵測、惡意程式分類、自動化回應 | 與[資訊安全](../cybersecurity/index.md)重疊 |
| 自主平台 | 無人機、地面載具與船艦的導航、目標辨識與控制 | 爭議最大的領域，見政策一節 |

## 國防為何不同

- **對手會適應。** 依照昨天的戰術訓練的系統，可能被刻意改變的行為擊敗，這是分布偏移更困難的版本。
- **資料稀少。** 真實作戰資料少且屬機密，系統常以模擬資料或其他領域的資料訓練。
- **後果嚴重，有時無法挽回。** 目標判定或升級衝突的錯誤代價，高於多數其他應用，因此評估標準格外重要。
- **軍民兩用。** 為民用目的建立的方法與模型，很快就會轉用於軍事，同樣的技術可能出現在衝突的雙方。

## 自主性與武裝衝突法

核心政策問題是：使用武力時，人類必須保留多少判斷權。常被引用的兩種立場如下：

- **國際紅十字委員會（ICRC）** 主張禁止效果無法預測或控制的武器，並限制以人為目標的自主系統。其立場以國際人道法為基礎。
- **美國** 並未禁止自主武器。其 2023 年的指令要求，自主與半自主武器系統需保留「適當程度的人類判斷，以決定武力的使用」，而且具自主功能的新系統在部署前須經高層審查。

民用 AI 法規常將軍事用途排除在外。歐盟 AI 法（AI Act）規定，其不適用於僅用於軍事、國防或國家安全目的的 AI 系統（第 2 條第 3 項）。

## 戰略競爭

各國政府把 AI 視為軍事優勢的來源，這種競爭推動了投資。Horowitz（2018）主張 AI 可能改變權力平衡，而其影響取決於技術擴散的速度。國家之間的競賽會縮短測試與審慎的時間，這也是軍備管制提案除了技術本身，還著重於查證與規範的原因之一。

## 關鍵方法

有四類方法承擔了大部分工作。每一項都連結到解說該方法的頁面。

- [電腦視覺](../../theory/models/computer-vision/index.md)：影像中的偵測與追蹤，是多數 ISR 與目標辨識流程的基礎。
- [強化學習](../../theory/paradigms/reinforcement-learning/index.md)：在模擬環境中學習控制策略與規劃，用於訓練與自主研究。
- [異常偵測](../../theory/paradigms/unsupervised/anomaly-detection/index.md)：在感測器與網路資料中標記異常活動，用於網路防禦與監控的初步篩選。
- [領域適應](../../theory/paradigms/transfer/domain-adaptation/index.md)：在標記的軍事資料稀少的情況下，把在模擬或民用資料上訓練的模型轉移到實際作業環境。

## 關聯

這些系統的民用對應技術見[自駕車與交通](../autonomous-driving/index.md)與[資訊安全](../cybersecurity/index.md)。治理與安全問題見[法規、政策與治理](../../society/governance/index.md)與[安全與對齊](../../society/safety-alignment/index.md)。

## 應用

- 以自動分析衛星與無人機影像進行測繪與災損評估，這項用途也見於人道救援工作。
- 軍用載具與飛機的預測性維護，因為停機的作戰成本很直接。
- 用語言模型摘要報告、搜尋大型文件庫，輸出仍由人審閱。

## 開放問題

- 有意義的人類控制能否以可在實務上查核的方式定義，而不只是寫在政策文字裡？
- 當對手的行為未知、真實資料又稀少時，系統該如何測試？
- 能否在不洩漏敏感技術細節的前提下，查證自主武器的國際規範？
- 民用 AI 法規對軍事用途的排除，會不會留下責任歸屬的缺口？

## 參考文獻

### 開創性論文

- Horowitz, M. C. (2018). Artificial Intelligence, International Competition, and the Balance of Power. *Texas National Security Review*, 1(3). https://tnsr.org/2018/05/artificial-intelligence-international-competition-and-the-balance-of-power/ — 主張軍事 AI 可能改變各國之間的權力，並探討技術擴散的速度。

### 文章與文件

- Boulanin, V. & Verbruggen, M. (2017). *Mapping the Development of Autonomy in Weapon Systems*. SIPRI. https://www.sipri.org/publications/2017/other-publications/mapping-development-autonomy-weapon-systems — 獨立研究機構對武器系統自主性發展的調查，並整理其帶出的政策議題。
- International Committee of the Red Cross (2021). *ICRC position on autonomous weapon systems*. https://www.icrc.org/en/document/icrc-position-autonomous-weapon-systems — ICRC 關於依國際人道法，自主武器需要哪些法律限制的立場。
- U.S. Department of Defense (2023). *DoD Directive 3000.09, Autonomy in Weapon Systems*. https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/300009p.PDF — 美國現行的政策，規範人類對武力使用的判斷，以及部署前必須經過的高層審查。
- European Union (2024). *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*, Article 2(3). https://eur-lex.europa.eu/eli/reg/2024/1689/oj — 排除僅用於軍事、國防或國家安全目的之 AI 系統的法律條文。
