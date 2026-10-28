---
translation_reviewed: 2026-10-28
---

# 機械式可解釋性與電路

機械式可解釋性試圖對神經網路所學到的演算法進行逆向工程。它辨識網路用來運算的內部特徵，找出組合這些特徵的小型子網路（電路），並透過介入網路的激活來檢驗每一項主張。

## 概述

多數解釋方法問的是，哪些輸入或特徵對某個輸出有影響（見[可解釋性](index.md)）。機械式可解釋性問的是更困難的問題：網路正在執行什麼程式？這個方法源自視覺模型上的電路研究計畫，該計畫提出三項推測性的主張：特徵是神經網路的基本單位、特徵之間由電路相連，以及相似的特徵與電路會在不同模型間重複出現（Olah et al., 2020）。

Transformer 成為主要的研究對象。它的殘差流讓每一層都有一個共享的通道可供讀寫，使資訊流動更容易追蹤（見[Transformers 與注意力機制](../../theory/models/transformer/index.md)）。迄今多數結果都來自小型模型與狹窄的任務。

## 核心概念

- **特徵**：某層激活空間中的一個方向，或單一神經元，對應到輸入中可辨識的性質。
- **電路**：由特徵及其間權重組成的子圖，執行可辨識的運算。
- **疊加（superposition）**：網路表示的特徵數量多於其維度，做法是給予它們近似正交的方向。玩具模型顯示，當特徵稀疏、很少同時活躍時，就會出現這種情況（Elhage et al., 2022）。
- **多義性（polysemanticity）**：單一神經元回應多個不相干的特徵，是疊加最常見的表現。
- **歸納頭（induction head）**：當某個 token 再次出現時，會複製它先前出現時所接的 token 的注意力頭。它由兩個頭合作構成（Olsson et al., 2022）。
- **激活修補（activation patching）**：在乾淨輸入與受損輸入上分別執行模型，再把乾淨執行中的某個內部激活複製到受損執行中，以衡量它能恢復多少正確輸出。
- **探測（probing）**：在激活上訓練一個簡單的分類器，以檢驗某項資訊是否存在。探測可能找到模型從未使用的資訊，因此它顯示的是被表示了什麼，而不是被使用了什麼。

## 運作方式

這個領域的研究通常循環進行：觀察一種行為、提出候選特徵、追蹤電路，並透過介入來檢驗主張。

```mermaid
flowchart LR
    A[觀察一種行為] --> B[找出候選特徵<br/>探測、稀疏自編碼器]
    B --> C[追蹤電路<br/>修補、歸因]
    C --> D[介入：消融、修補或引導]
    D -->|預測成立| E[在新輸入上檢驗]
    D -->|預測失敗| B
```

特徵發現常使用稀疏自編碼器。它被訓練來從一個寬的編碼重建某層的激活，而編碼中多數項為零。由於疊加把特徵擠進共用的方向，稀疏性懲罰能找回單一神經元所隱藏的特徵（Cunningham et al., 2023）。

歸納頭展示了小規模的電路追蹤。在「Harry Potter … Harry」這類重複的文字中，模型會預測出「Potter」。前一 token 頭會在每個位置記錄其前一個 token。接著，歸納頭把目前的 token 與一個前一位置的 token 相符的較早位置配對，並複製其後接的 token。Olsson et al. (2022) 發現，這些頭在訓練期間形成，時間大約與情境學習明顯提升的時候相同。

一個較大的例子是 GPT-2 small 中的間接賓語電路。Wang et al. (2022) 追蹤模型如何以「Mary」完成「When Mary and John went to the store, John gave a drink to」。有些注意力頭會抑制重複的名字，另一些則把剩下的名字複製到輸出。對其注意力頭進行介入後，行為依預測改變。

## 關鍵方法

各方法在假設與能展示的內容上有所不同。

| 方法 | 想法 | 主要注意事項 |
|---|---|---|
| 因果追蹤與激活修補（Meng et al., 2022；Heimersheim & Nanda, 2024） | 在受損執行中還原一個乾淨的激活，並衡量恢復程度 | 結果取決於基準線，而且還原一個激活與消融它，可能得出不同的答案。 |
| 自動化電路發現（Conmy et al., 2023） | 在保留所選指標的同時，修剪計算圖的邊 | 在大型模型上成本高，且對指標與輸入敏感。 |
| 稀疏自編碼器（Cunningham et al., 2023；Gao et al., 2024） | 學習能重建激活的稀疏特徵 | 重建誤差使部分計算仍無法解釋。 |
| 激活引導（Turner et al., 2023） | 在激活上加入一個方向以改變行為 | 原本用來改變某一行為的方向，可能也會改變其他行為。 |

## 連結

- 上層總覽[可解釋性](index.md)把此方法與可解釋 AI 作對比。
- 稀疏自編碼器是一種稀疏字典學習，與初級視覺皮質的[稀疏編碼](../../brain-mind/computational-neuroscience/sparse-coding/index.md)模型背後的想法相同。兩者都在問：哪一小組單元能解釋一個稠密的訊號。
- Jonas 與 Kording (2017) 指出，即使在完全已知的系統上，標準的神經科學分析也可能產生誤導。同樣的警惕也適用於神經網路；另見 [NeuroAI](../../brain-mind/neuroai/index.md)。
- 許多安全提案都依賴觀察模型內部，以偵測欺騙、監控不良目標或引導行為。見[安全與對齊](../safety-alignment/index.md)。

## 應用

- **除錯。** 狹窄的電路能對特定錯誤提供可檢驗的解釋。
- **模型編輯。** 因果追蹤把事實回想定位到主體最後一個 token 上、中間層的 MLP 模組；Meng et al. (2022) 據此編輯儲存的事實。這類編輯的可靠性仍有爭議。
- **引導與監控。** 在激活上加入一個方向，可以不重新訓練就改變行為（Turner et al., 2023）。綜述探討了這些工具如何支持安全工作（Bereska & Gavves, 2024）。
- **科學發現。** Nanda et al. (2023) 發現，一個在模加法上訓練的小型 Transformer 學到了一種以離散傅立葉變換為基礎的演算法。

## 開放問題

### 目前已被逆向工程的部分

歸納頭、GPT-2 small 中的間接賓語電路、事實回想的定位，以及小型模型中完整的模加法演算法，是最清楚的案例。每個案例都涉及小型模型或狹窄的任務。

### 尚未解決的部分

- **規模。** 這些方法能否解釋前沿規模的模型與複雜的多步驟行為，目前大多未知。
- **正確的單位。** 稀疏自編碼器的特徵是否為網路真正的單位，尚不清楚。重建誤差、被分裂的特徵，以及從不激活的特徵，都使答案變得複雜（Gao et al., 2024）。
- **忠實性。** 在某一分布上吻合行為的電路，未必是一般性的機制。陳述的推理也不一定忠實：思維鏈解釋可能遺漏真正影響答案的線索（Turpin et al., 2023）。
- **可行性。** Jonas 與 Kording 的警告提出一個問題：對大型網路做完整的機制性解釋，是否根本可以達成。

## 參考文獻

### 開創性論文

- Olah, C., et al. (2020). *Zoom In: An Introduction to Circuits*. Distill. https://doi.org/10.23915/distill.00024.001 — 提出電路研究計畫的三項主張：特徵、電路與普遍性。
- Elhage, N., et al. (2022). *Toy Models of Superposition*. arXiv. https://arxiv.org/abs/2209.10652 — 在小型模型中顯示，當特徵稀疏時，網路如何儲存多於維度數的特徵。
- Olsson, C., et al. (2022). *In-context Learning and Induction Heads*. arXiv. https://arxiv.org/abs/2209.11895 — 辨識歸納頭為情境內複製背後的電路，並把它與學習連結起來。
- Meng, K., et al. (2022). *Locating and Editing Factual Associations in GPT*. arXiv. https://arxiv.org/abs/2202.05262 — 提出因果追蹤，將事實回想定位到中間層的 MLP 模組，並加以編輯。
- Wang, K., et al. (2022). *Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small*. arXiv. https://arxiv.org/abs/2211.00593 — 對一項自然語言任務，逆向工程出完整的注意力頭電路。
- Cunningham, H., et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv. https://arxiv.org/abs/2309.08600 — 在殘差流激活上訓練稀疏自編碼器，發現其特徵比神經元更易解讀。
- Heimersheim, S. & Nanda, N. (2024). *How to use and interpret activation patching*. arXiv. https://arxiv.org/abs/2404.15255 — 激活修補的實用指南，涵蓋其變體與解讀結果時的陷阱。
- Conmy, A., et al. (2023). *Towards Automated Circuit Discovery for Mechanistic Interpretability*. arXiv. https://arxiv.org/abs/2304.14997 — 透過修剪計算圖的邊，自動化尋找電路。
- Nanda, N., et al. (2023). *Progress measures for grokking via mechanistic interpretability*. arXiv. https://arxiv.org/abs/2301.05217 — 逆向工程小型 Transformer 學到的模加法演算法，並追蹤其在訓練中的變化。
- Jonas, E. & Kording, K. P. (2017). Could a neuroscientist understand a microprocessor? *PLOS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1005268 — 把標準的神經科學分析用於一個功能完全已知的模擬處理器。
- Turner, A. M., et al. (2023). *Steering Language Models With Activation Engineering*. arXiv. https://arxiv.org/abs/2308.10248 — 顯示把激活向量加入模型的殘差流，可以引導其輸出。
- Turpin, M., et al. (2023). *Language Models Don't Always Say What They Think*. arXiv. https://arxiv.org/abs/2305.04388 — 顯示思維鏈解釋可能遺漏真正影響答案的輸入線索。
- Gao, L., et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv. https://arxiv.org/abs/2406.04093 — 研究稀疏自編碼器的品質如何隨字典大小變化，並提出評估方法。

### 綜述與教科書

- Bereska, L. & Gavves, E. (2024). *Mechanistic Interpretability for AI Safety — A Review*. arXiv. https://arxiv.org/abs/2404.14082 — 綜述機械式可解釋性的方法，以及它們與 AI 安全目標的關係。
