---
translation_reviewed: 2026-10-28
---

# 監控、人臉辨識與人權

人臉辨識讓軟體判斷兩張臉影像是否屬於同一人，或判斷一張臉最接近已登錄的哪一個人。本頁說明這些系統的準確度如何、對哪些人較準確或較不準確，預測性警務與大規模監控如何使用相似的資料驅動工具，以及禁令與法律如何回應。

## 概述

人臉辨識是電腦視覺中部署最廣的應用之一。它能解鎖手機、支援護照查驗，也協助調查人員搜尋影像。在公共空間使用時，它能辨識出沒有做任何引人注意之事的人，而且規模遠超人類觀察者所能達到。

有三個疑慮反覆出現。第一，準確度並不一致：錯誤率取決於膚色、性別與拍攝條件，因此平均表現良好的系統，仍可能對特定群體失效。第二，比對結果常被當成證據，一次錯誤就可能導致攔查、搜索或逮捕。第三，支撐辨識的基礎設施，包括攝影機、資料庫與資料分享，很容易被挪作設計者未曾預期的用途。

預測性警務帶來相關的問題。以警察活動紀錄訓練的模型，可能學到的是警察曾經去過哪裡，而不是犯罪實際發生在哪裡。這類公平性問題的討論見[倫理與公平](../ethics/index.md)。

國際人權法保護隱私與集會自由，而這些保護也適用於人臉辨識。Gabrielli（2025）分析 *Glukhin v Russia* 一案，這是歐洲人權法院的案例，涉及對一名和平抗議者使用人臉辨識，並主張抗議活動中的大規模監控需要嚴格的保障措施。

## 關鍵概念

- **驗證（1:1）**：確認兩張影像是否為同一人，例如手機為其主人解鎖。
- **辨識（1:N）**：在大量已登錄的人臉中搜尋比對對象。這裡的錯誤影響更大，因為一張待查影像要與資料庫中的每一位候選人比較。
- **閾值與錯誤類型**：相似度分數會與閾值比較。移動閾值時，假比對（假陽性）與漏比對（假陰性）會互相消長。[公平性定義](../ethics/fairness-definitions.md)說明了為何各群體間的錯誤率與決策比率同時相等，可能互相衝突。
- **分組評估（disaggregated evaluation）**：分別報告每個人口子群體的準確度，而不只是一個平均值。[Gender Shades](gender-shades/index.md) 稽核是最著名的例子。
- **回饋迴圈**：系統的輸出會改變它之後學習的資料。在預測性警務中，記錄到的犯罪來自模型派出的巡邏。
- **即時與事後使用**：在公共場所即時辨識人員，與之後搜尋錄影紀錄不同。法律常對兩者有不同的規範。
- **大規模監控**：對整體人口進行系統性、無差別的監視，不同於針對特定嫌疑人的定向使用。

## 運作方式

典型的人臉辨識流程包含數個階段，每一階段都可能引入錯誤。

```mermaid
flowchart LR
  A[攝影機或照片] --> B[人臉偵測]
  B --> C[嵌入模型]
  C --> D[與資料庫比對]
  D --> E{分數高於閾值}
  E -- 是 --> F[候選比對結果]
  E -- 否 --> G[無比對結果]
  F --> H[人工審查與行動]
```

1. **偵測**在影像中找出人臉。光線、角度與解析度決定後續階段可用的細節多寡。
2. **嵌入**把每張臉對應到一組數字向量。在大量人臉資料上訓練的深度網路學會這個對應，而訓練所用的損失函數決定不同人的向量分得多開。[ArcFace](arcface/index.md) 是這類損失函數的一個著名例子。
3. **比對**依相似度比較向量，並回傳超過閾值的最佳候選者。
4. **決策**通常由人員審查候選結果。[自動化偏誤](../human-ai-interaction/automation-bias.md)的研究顯示，審查者傾向信任系統的排序，因此人工把關的實際效果比看起來弱。

準確度不只取決於演算法，也取決於訓練資料。大多以淺膚色臉孔訓練的模型，在深膚色臉孔上往往表現較差；若基準資料缺少人口統計標記，就完全無法看出這種落差。

## 關鍵方法

三項里程碑式的研究讓這個領域的主要問題具體化。每項研究各有一頁，說明問題、方法、結果與限制。

| 方法 | 問題 | 論文的主要結果 | 延伸閱讀 |
|---|---|---|---|
| Gender Shades（Buolamwini & Gebru, 2018） | 商業性別分類器在不同膚色與性別上的準確度如何？ | 深膚色女性的錯誤率最高達 34.7%，淺膚色男性最多僅 0.8% [^1] | [Gender Shades](gender-shades/index.md) |
| ArcFace（Deng et al., 2019） | 哪一種訓練損失能讓人臉嵌入更具區分力？ | 在論文的消融實驗中，角度間隔損失在 LFW、CFP-FP 與 AgeDB 上優於 softmax | [ArcFace](arcface/index.md) |
| 失控回饋迴圈（Ensign et al., 2017） | 為什麼預測性警務會偏離真實的犯罪率？ | 模擬中，類 PredPol 的部署無法追上真實犯罪率；修正事件資料後則可以 | [失控回饋迴圈](runaway-feedback-loops/index.md) |

三者回答的是不同的問題：已部署的系統表現如何（Gender Shades）、辨識模型如何訓練（ArcFace），以及整個警務系統如何運作（回饋迴圈的論文）。

## 與其他主題的連結

- **大腦與心智。**人類的臉部知覺是專門化的：Kanwisher et al.（1997）發現梭狀回中有一區域對臉的反應強於對其他物件的反應。[知覺與視覺系統](../../brain-mind/visual-perception/index.md)討論了這種選擇性。所謂的「其他種族效應」是指人們辨識自己族群臉孔的準確度較高，這種效應也出現在人臉辨識演算法中（Phillips et al., 2011），因此訓練資料中的偏誤，可能重現長期記錄在人身上的模式。
- **電腦視覺。**偵測與嵌入模型的說明見[電腦視覺](../../theory/models/computer-vision/index.md)。
- **倫理與公平。**分組評估本身就是公平性問題。見[倫理與公平](../ethics/index.md)與[公平性定義](../ethics/fairness-definitions.md)。
- **隱私。**在歐洲法律中，生物特徵資料屬於特殊類別的個人資料，臉部影像是典型例子。見[隱私與資料保護](../privacy/index.md)。

## 應用

- **裝置與門禁。**手機與大樓門禁系統會把一張臉與一個已登錄的範本比較：這是驗證，也是最簡單的情況。
- **邊境管制與旅行。**機場以人臉比對，把旅客與護照照片進行比較。
- **刑事調查。**警方把攝影機與其他來源的影像，與影像資料庫進行比對。錯誤比對在此造成的後果最嚴重，因此這個領域的規範也最嚴格。
- **預測性警務。**軟體依預期犯罪率為社區或人員排序，用以指派巡邏。Lum & Isaac（2016）探討以偏誤資料訓練這類系統會發生什麼事，Hung & Yen（2023）則詳細檢視芝加哥的一個案例。

### 禁令與暫停使用

從 2019 年起，美國數個城市限制或禁止市府使用人臉辨識，舊金山是最早的城市之一。之後，部分州通過了時間有限的暫停使用規定。在一項針對德國公民的調查中，Kieslich & Lünich（2024）發現，感受到的歧視會提高對更嚴格規範的需求，而對 AI 與執法機關的信任則會降低對禁令的需求。

### 歐盟 AI 法的禁止條款

《歐盟人工智慧法》（Regulation (EU) 2024/1689）第 5 條列出一律禁止的做法。這些禁令自 2025 年 2 月 2 日起適用，違反者最高可處以全球營業額 7% 的罰款，[法律、政策與治理](../governance/index.md)有摘要說明。與本頁最相關的禁止事項包括：

- 從網路或 CCTV 影像中無差別地爬取臉部影像，用以建立或擴充人臉辨識資料庫；
- 僅根據剖析或人格特質，評估某人犯罪的風險，這是預測性警務的核心法律問題；
- 在工作場所與教育機構中進行情緒辨識，僅有狹窄的例外；
- 推論出種族、政治意見或性傾向的生物特徵分類；
- 執法機關在公開場所進行即時遠端生物特徵辨識，原則上禁止，只有需事先授權的狹窄例外。

Veale & Borgesius（2021）分析的是委員會的草案，它早於最終條文。他們發現部分條款有出人意料的法律後果，並對執行機制與各國政策空間提出疑慮。請以最終條文核對細節。

## 開放問題

- 基準測試的準確度數字，能否預測實際場域的表現？特別是影像模糊、光線不足或距離遠的情況。
- 更好的訓練資料能否消除差異，還是差異也取決於系統的部署方式？
- 公共空間的辨識應該全面禁止，還是在嚴格條件下允許？歐盟選擇一般禁止加上狹窄的例外，其他法域則有不同選擇。
- 預測性警務的回饋迴圈應如何打破：改變模型、改變資料，還是改變系統的部署方式？Ensign et al.（2017）提出修正事件資料，Hung & Yen（2023）則提出治理措施。
- 大眾接受度因國家而異：Kostka et al.（2021）發現中國的接受度最高，德國最低，而人們在判斷時，便利與安全比監控更為突出。這些態度是否應影響規範，是民主程序需要回答的問題。

## 參考資料

### 開創性論文

- Buolamwini, J. & Gebru, T.（2018）. Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *FAT\**. https://proceedings.mlr.press/v81/buolamwini18a.html — 對三款商業性別分類器的稽核，顯示錯誤率因膚色與性別而有明顯差異。
- Ensign, D. et al.（2017）. Runaway Feedback Loops in Predictive Policing. arXiv. https://arxiv.org/abs/1706.09847 — 預測性警務的模型與模擬，說明回饋迴圈的形成。
- Phillips, P. J. et al.（2011）. An other-race effect for face recognition algorithms. *ACM Transactions on Applied Perception*. https://doi.org/10.1145/1870076.1870082 — 演算法與人類觀察者一樣，對其他種族的臉孔表現較差。
- Kanwisher, N., McDermott, J. & Chun, M. M.（1997）. The Fusiform Face Area: A Module in Human Extrastriate Cortex Specialized for Face Perception. *The Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.17-11-04302.1997 — 以 fMRI 證明人腦皮質中有一區域對臉孔有選擇性的反應。

### 綜述與教科書

- Alikhademi, K. et al.（2021）. A review of predictive policing from the perspective of fairness. *Artificial Intelligence and Law*. https://doi.org/10.1007/s10506-021-09286-4 — 從公平性角度回顧預測性警務系統及其引發的問題。

### 文章與官方文件

- Lum, K. & Isaac, W.（2016）. To Predict and Serve? *Significance*. https://doi.org/10.1111/j.1740-9713.2016.00960.x — 主張以偏誤資料訓練的預測性警務，會重現偏誤。
- Raji, I. D. & Buolamwini, J.（2019）. Actionable Auditing. *AAAI/ACM Conference on AI, Ethics, and Society*. https://doi.org/10.1145/3306618.3314244 — 公開報告稽核結果，如何影響商業 AI 產品。
- Chapman, A. et al.（2022）. A Data-driven analysis of the interplay between Criminological theory and predictive policing algorithms. *ACM FAccT*. https://doi.org/10.1145/3531146.3533071 — 以資料驅動的方式，研究犯罪學理論與預測性警務演算法。
- Hung, T.-W. & Yen, C.-P.（2023）. Predictive policing and algorithmic fairness. *Synthese*. https://doi.org/10.1007/s11229-023-04189-0 — 檢視芝加哥一個預測性警務系統中的種族歧視。
- Veale, M. & Zuiderveen Borgesius, F.（2021）. Demystifying the Draft EU Artificial Intelligence Act. *Computer Law Review International*. https://doi.org/10.9785/cri-2021-220402 — 分析歐盟 AI 法草案及其執行問題。
- Kieslich, K. & Lünich, M.（2024）. Regulating AI-Based Remote Biometric Identification. Investigating the Public Demand for Bans, Audits, and Public Database Registrations. arXiv. https://arxiv.org/abs/2401.13605 — 針對德國公民的調查，探討遠端生物特徵辨識的規範。
- Gabrielli, G.（2025）. The Use of Facial Recognition Technologies in the Context of Peaceful Protest. *European Journal of Risk Regulation*. https://doi.org/10.1017/err.2025.26 — 把人權標準套用到抗議活動中的人臉辨識。
- Kostka, G., Steinacker, L. & Meckel, M.（2021）. Between security and convenience: Facial recognition technology in the eyes of citizens in China, Germany, the United Kingdom, and the United States. *Public Understanding of Science*. https://doi.org/10.1177/09636625211001555 — 在四個國家進行的線上調查，比較大眾對人臉辨識的接受度。

[^1]: Buolamwini & Gebru（2018），摘要與表 4。數字取自 Pilot Parliaments Benchmark，三款分類器在其中對深膚色女性的錯誤率都是最高的。
