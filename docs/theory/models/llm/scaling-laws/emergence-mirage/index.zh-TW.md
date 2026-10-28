---
translation_reviewed: 2026-10-28
---

# 湧現是海市蜃樓（Schaeffer 等人，2023）

Schaeffer、Miranda 與 Koyejo 主張，湧現能力的突然出現，往往是研究者所選擇的指標造成的結果，而非模型本身發生了突然的改變。若改用連續指標，同樣的輸出會呈現平滑、可預測的進步。整體主題見上層頁面[縮放定律與湧現能力](../index.md)。

## 概述

Wei et al.（2022）指出，語言模型的某些能力會在較大規模時突然出現。Schaeffer et al.（2023）檢驗了同樣的主張，並提出一個較窄的問題：若模型實際產生的輸出，改變了評分方式，那麼看似的躍升還會存在嗎？他們的答案是，對許多任務而言，躍升並不存在。表觀的湧現取決於分數是不連續的（例如完全比對的準確率），還是連續的（例如衡量答案接近程度的分數）。


## 關鍵概念

- **不連續指標**：把答案只分為對或錯、中間沒有過渡的分數。完全比對的準確率就是一例。
- **連續指標**：隨答案與目標的接近程度平滑變化的分數，例如正確答案的對數機率，或與正確答案之間的編輯距離。
- **表觀湧現**：不連續分數的上升看起來很突然，但底層的行為其實是逐漸改變的。

## 運作方式

論文提出一個簡單的數學論證，並以三種方式加以檢驗。論證是：對於某項任務與模型家族，湧現是否出現，取決於套用於相同輸出的評分函數。

為了看清楚機制，考慮一個答案有 $L$ 個 token 的任務，並假設每個 token 答對的機率為 $p$。此時完全比對的準確率大約為 $p^L$。它是 $p$ 的凸函數，因此 $p$ 的穩定上升會使分數先維持低位、然後迅速攀升。相對地，連續分數（例如正確答案的平均每 token 對數似然）會隨同一個 $p$ 平滑上升。這個計算是我們以自己的話對該機制所作的說明，並非論文原文的引述。

論文報告的三項檢驗如下：

1. 關於指標選擇效應的預測，在 InstructGPT 與 GPT-3 模型家族、以及曾被主張湧現的任務上檢驗。
2. 關於 BIG-bench 上湧現能力後設分析中指標選擇的預測。
3. 證明指標選擇可在數種跨深度網路的視覺任務上產生表觀湧現；這些任務先前並未被主張有湧現。

## 結果

摘要概括了這些發現。在不連續指標下，所主張的能力呈現陡峭的躍升；在線性或連續指標下，它們則呈現平滑、可預測的進步。作者的結論是，所宣稱的湧現能力在不同指標或更好的統計方法下會消失，而且它們未必是擴大 AI 模型規模時的根本性質。

## 限制

- **分析的範圍。** 論文處理的是已經存在的輸出，因此無法說明在未測試的規模下，模型會產生什麼。
- **並非每個案例。** 論證說明了指標可以產生躍升，但並未證明每一項被主張的湧現能力都是指標造成的假象。論文的措辭因此保持保留。
- **與能力的關聯。** 即使是平滑的曲線，當有用的門檻位置很重要時仍具實務意義，例如使用者需要的答案必須完全正確。

## 開放問題

- 在任何合理的指標下都仍然陡峭的能力有哪些？這類案例會比論文所重新評分的案例，更有力地支持真正的湧現。
- 當使用者關心的是全有或全無的成功（例如完整正確地解出一題），而連續分數低估了風險時，預測者應如何回報能力？
- 視覺與語言的結果，是共享同一機制，還是只是在不連續評分下看起來相似的不同現象？

## 相關連結

- 上層主題：[縮放定律與湧現能力](../index.md)。它所挑戰的主張見[湧現能力](../emergent-abilities/index.md)。
- 分析所用的模型家族，見 [InstructGPT 與 RLHF](../../instructgpt-rlhf/index.md) 與 [GPT-3 少樣本學習](../../gpt-3-few-shot/index.md)。
- 指標選擇是[評估](../../../../../engineering/evaluation/index.md)中的一般性議題，並不只限於湧現。
- 腦與心智的角度：心理物理學長期研究，反應測量方式如何能讓知覺上的漸進變化看起來像門檻。這是論文本身未提出的類比。見[心理學](../../../../../brain-mind/psychology/index.md)。

## 參考文獻

### 開創性論文

- Schaeffer, R., Miranda, B. & Koyejo, S. (2023). *Are Emergent Abilities of Large Language Models a Mirage?* arXiv. https://arxiv.org/abs/2304.15004 — 論文本身：主張指標選擇會產生表觀湧現，並在語言與視覺任務上加以檢驗。
- Wei, J., et al. (2022). *Emergent Abilities of Large Language Models*. arXiv. https://arxiv.org/abs/2206.07682 — 本文所檢驗的主張：在規模增加時突然出現、無法由小模型外推的能力。
- Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT 模型，是本文重新評分的任務所屬的模型家族之一。
- Srivastava, A., et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — 用於湧現能力後設分析的 BIG-bench 任務。
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — 平滑的冪律損失趨勢，湧現主張正是與之對照。

### 綜述與教科書

- Berti, L., Giorgi, F. & Kasneci, G. (2025). *Emergent Abilities in Large Language Models: A Survey*. arXiv. https://arxiv.org/abs/2503.05788 — 回顧湧現的文獻，包括以指標為基礎的批評，以及真正湧現的論點。

### 文章與文件

- Ganguli, D., et al. (2022). *Predictability and Surprise in Large Generative Models*. arXiv. https://arxiv.org/abs/2202.07785 — 討論大型生成模型中，可預測的損失與不可預測的特定能力並存的現象。
