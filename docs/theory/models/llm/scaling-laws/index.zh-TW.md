---
translation_reviewed: 2026-10-28
---

# 縮放定律與湧現能力

縮放定律是描述語言模型損失如何隨參數量、訓練資料與運算量增加而下降的經驗法則。湧現能力則是指小模型似乎沒有、而大模型卻突然出現的能力；這些能力反映的是規模本身的真實性質，還是測量方式造成的假象，仍有爭議。

## 概述

神經網路在變大或使用更多資料訓練時，表現會以規律的方式提升。Hestness et al.（2017）在四個領域中量測此現象，發現泛化誤差會隨訓練集大小以冪律下降。[^1] 對 Transformer 語言模型而言，Kaplan et al.（2020）顯示，保留的測試文字上的交叉熵損失，在模型大小、資料集大小與運算量上都遵循冪律，橫跨超過七個數量級。[^2] 這種平滑且可預測的趨勢，讓實驗室可以用小而便宜的實驗擬合曲線，在投入大量資源之前，先估計更大訓練的損失。

由此衍生出三個問題。第一是如何在固定預算下分配參數與訓練 token。Kaplan et al. 的結論是，額外運算的最佳用途，是在相對有限的資料上訓練非常大的模型，並在遠未收斂前停止。之後的 Chinchilla 研究主張，當時的模型明顯訓練不足，模型大小與資料應該同步成長；這個論點是 [運算最佳化訓練](../compute-optimal-training/index.md) 的主題。第二個問題關乎損失與能力之間的落差。損失平滑下降的模型，仍可能在某些特定能力上突然躍升。Wei et al.（2022）把這類躍升稱為湧現能力。[^3] 第三個問題是這些躍升是否真實。Schaeffer et al.（2023）主張，表面上的陡峭程度有很大一部分來自評分指標的選擇。[^4]

縮放也已延伸到推論階段：投入更多運算，有時能換來更好的答案，而不需要更大的模型。見[測試時運算擴展](../../reasoning/test-time-scaling.md)。

## 關鍵概念

- **縮放定律**：損失等數量與參數量、token 數或運算量等尺度變數之間的經驗關係，通常是冪律。它是對測量結果的擬合，除了所量測的範圍外不作保證。詞彙表見[縮放定律](../../../../reference/glossary/index.md)。
- **冪律**：形如 $y \propto x^{-\alpha}$ 的關係。在對數—對數座標上是一條直線，因此這類擬合通常以此方式繪製。
- **運算預算**：訓練所花費的總運算量。對稠密 Transformer 而言，通常近似為參數量乘以訓練 token 數。
- **過擬合區**：模型相對於資料集而言過大時，即使訓練損失持續下降，在保留文字上的表現也不再改善。Kaplan et al. 給出了這種依賴關係的簡單方程式。
- **常數項**：許多擬合中的固定偏移量，使損失在規模增加時趨近一個下限。
- **湧現能力**：小模型沒有、大模型才有的能力，無法從小模型的表現外推得出（Wei et al., 2022）。
- **指標選擇**：任務所用的評分規則。不連續的分數（例如完全比對的準確率）會把平滑的底層進步，變成看似突然的躍升。

## 運作方式

一項縮放研究通常遵循相同的程序：

```mermaid
flowchart LR
  A[訓練許多模型<br/>變動 N、D 與 C] --> B[量測保留文字的損失]
  B --> C[擬合冪律<br/>常常含常數項]
  C --> D[為固定預算選擇 N 與 D]
  D --> E[外推到更大的訓練]
  E --> F[於下游任務上檢驗]
```

首先固定一個模型家族，通常是僅解碼器的 Transformer，並在大型文字語料上訓練數種大小的模型。接著記錄保留文字上的損失，並將其對應到參數數量 $N$、訓練 token 數 $D$ 與訓練運算量 $C$。量測點隨後以 Hoffmann et al.（2022）參數化擬合所用的形式來擬合：

$$L(N, D) \approx E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}$$

常數 $E$、$A$、$B$、$\alpha$ 與 $\beta$ 是由資料估計出來的。其數值載於原論文中，此處不再重複。Kaplan et al.（2020）則先分別擬合每個變數的單變數冪律，這種形式是此概念廣為人知的起點。

擬合之後，固定預算下的最佳分配便由最小化擬合損失而得。任何外推都假設同一條曲線在量測範圍之外仍然成立。

## 主要方法

每個方法都有自己的專頁。此處的比較從簡。

| 方法 | 核心主張 | 專頁 |
|---|---|---|
| Kaplan et al.（2020） | 損失在參數、資料與運算量上遵循冪律；大模型的樣本效率較高 | [Kaplan 縮放定律](kaplan-scaling-laws/index.md) |
| Chinchilla（Hoffmann et al., 2022） | 固定預算下，模型大小與訓練 token 數應同步成長 | [運算最佳化訓練](../compute-optimal-training/index.md) |
| Wei et al.（2022） | 某些能力在規模增加時突然出現，無法從小模型外推 | [湧現能力](emergent-abilities/index.md) |
| Schaeffer et al.（2023） | 表觀的湧現大多取決於指標；連續指標會給出平滑曲線 | [湧現是海市蜃樓](emergence-mirage/index.md) |

前兩個方法回答分配問題，也就是如何分配運算。後兩個方法回答能力是否能由規模預測。兩篇湧現論文對證據的看法不同，但並不是在規模是否重要這件事上有所分歧。

## 相關連結

- 上層主題：[大型語言模型](../index.md)。縮放決定了那裡所描述的預訓練階段的模型大小與資料。
- $D$ 計算的單位是 token，因此分詞器會改變 token 預算的意義。若某種語言表達同樣的文字需要更多 token，該語言的訓練成本就更高。見[分詞](../tokenisation/index.md)。
- 架構的一面見 [Transformer](../../transformer/index.md)。Kaplan et al. 報告，在他們測試的範圍內，寬度與深度的影響較小，這使模型大小與資料成為主要的研究變數。
- 少樣本提示是使湧現問題受到廣泛關注的能力，見 [GPT-3 少樣本學習](../gpt-3-few-shot/index.md)。
- 湧現的測量選擇與[評估](../../../../engineering/evaluation/index.md)的討論有所重疊。
- 腦與心智的角度：到青少年時，兒童聽到的詞數約為數千萬，而 LLM 的訓練資料為數兆 token。人類學習是否遵循類似的縮放曲線，是另一個問題，見[發展認知](../../../../brain-mind/developmental-cognition/index.md)。

## 應用

- **規劃訓練**。實驗室用小規模實驗擬合曲線，在正式訓練前決定模型大小與資料量。GPT-4 技術報告描述了以這種方式運用縮放預測。[^5]
- **推論預算**。Chinchilla 的分析忽略了服務模型的成本。Sardana et al.（2023）修正這項分析，把推論成本納入考量，因此較小、在更多資料上訓練的模型會更受青睞。
- **資料供應**。Villalobos et al.（2022）預測，若目前趨勢持續，訓練資料集可能在 2026 至 2032 年間達到公開人類撰寫文字的存量。Muennighoff et al.（2023）則研究重複使用資料的訓練。
- **推論時縮放**。Brown et al.（2024）顯示，在多次取樣的答案中，至少有一個正確解出問題的比例，會隨取樣數增加而上升，橫跨四個數量級。Snell et al.（2024）主張，妥善運用測試時運算，效果可能勝過單純擴大模型參數。

## 開放問題

- **湧現是否真實？** Wei et al. 與 Schaeffer et al. 的論文對於陡峭的躍升究竟是模型的性質，還是指標的性質，看法不同。Berti et al.（2025）綜述了這場爭論。由於這項主張取決於測試過哪些規模，兩方在最大規模上的證據都有限。
- **損失能否預測能力？** 損失隨規模的變化比單一任務的準確率更平滑。Gadre et al.（2024）研究下游表現何時也遵循可預測的趨勢，包括模型訓練超過運算最佳點之後的情況。
- **資料要多少才夠？** 重複資料能否取代新文字，以及高品質過濾能把固定的資料存量延伸到什麼程度，目前尚無定論。
- **定律能否移轉？** Henighan et al.（2020）在影像、影片、多模態與數學模型中，也發現了與文字相似的冪律縮放，指數相近。新架構、新目標或新模態是否維持相同的形狀，每次都需要重新測量。
- **訓練與推論的權衡。** 如何權衡服務成本與訓練成本，以及對於特定查詢，測試時運算能否取代參數，仍是開放問題。

[^1]: Hestness et al.（2017）測試了四個領域：機器翻譯、語言模型、影像處理與語音辨識。見參考文獻。
[^2]: 損失隨規模變化的結果，以及「橫跨超過七個數量級」一語，皆取自 Kaplan et al.（2020）的摘要。擬合常數載於原論文中，此處不再重複。
[^3]: Wei et al.（2022）在引言中定義了此詞。他們所舉的例子此處不再重複，因為本頁撰寫時未檢視全文。
[^4]: 此論點是在固定的模型輸出上改變指標而提出的；見參考文獻中的 Schaeffer et al.（2023）。
[^5]: 此報告是作為由較小的訓練進行預測這一做法的出處而引用。其中的具體數字此處不再重複。

## 參考文獻

### 開創性論文

- Hestness, J., et al. (2017). *Deep Learning Scaling is Predictable, Empirically*. arXiv. https://arxiv.org/abs/1712.00409 — 報告在機器翻譯、語言模型、影像處理與語音辨識中，泛化誤差隨訓練集大小呈冪律縮放。
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — 顯示 Transformer 語言模型的損失在模型大小、資料與運算量上遵循冪律，並說明如何分配固定預算。
- Henighan, T., et al. (2020). *Scaling Laws for Autoregressive Generative Modeling*. arXiv. https://arxiv.org/abs/2010.14701 — 在影像、影片、多模態與數學模型中發現「冪律加常數」形式的縮放。
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — 訓練了 400 多個模型，主張在固定預算下，模型大小與訓練 token 數應同步成長。
- Wei, J., et al. (2022). *Emergent Abilities of Large Language Models*. arXiv. https://arxiv.org/abs/2206.07682 — 將湧現能力定義為小模型沒有、大模型才有，且無法由外推預測的能力。
- Schaeffer, R., Miranda, B. & Koyejo, S. (2023). *Are Emergent Abilities of Large Language Models a Mirage?* arXiv. https://arxiv.org/abs/2304.15004 — 主張表觀的湧現取決於不連續的指標，並在連續指標下顯示平滑曲線。
- Snell, C., et al. (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv. https://arxiv.org/abs/2408.03314 — 研究如何分配固定的推論運算量，並與訓練更大的模型作比較。

### 綜述與教科書

- Berti, L., Giorgi, F. & Kasneci, G. (2025). *Emergent Abilities in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2503.05788 — 綜述湧現的文獻，以及這些能力是否真正湧現的爭論。

### 文章與文件

- OpenAI et al. (2023). *GPT-4 Technical Report*. arXiv. https://arxiv.org/abs/2303.08774 — 大型多模態模型的技術報告；其開發章節描述了如何由較小的訓練預測訓練表現。
- Villalobos, P., et al. (2022). *Will we run out of data? Limits of LLM scaling based on human-generated data*. arXiv. https://arxiv.org/abs/2211.04325 — 將訓練資料的需求，與公開人類撰寫文字的估計存量相比較作預測。
- Muennighoff, N., et al. (2023). *Scaling Data-Constrained Language Models*. arXiv. https://arxiv.org/abs/2305.16264 — 研究在獨特文字有限、訓練期間必須重複使用資料時的縮放。
- Sardana, N., et al. (2023). *Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws*. arXiv. https://arxiv.org/abs/2401.00448 — 修正 Chinchilla 分析，在選擇模型大小與資料量時納入推論成本。
- Gadre, S. Y., et al. (2024). *Language models scale reliably with over-training and on downstream tasks*. arXiv. https://arxiv.org/abs/2403.08540 — 研究模型訓練超過運算最佳點、並於下游任務上評估時，縮放預測是否仍然成立。
- Brown, B., et al. (2024). *Large Language Monkeys: Scaling Inference Compute with Repeated Sampling*. arXiv. https://arxiv.org/abs/2407.21787 — 顯示至少有一次取樣解出問題的比例，會隨取樣次數增加而上升。
