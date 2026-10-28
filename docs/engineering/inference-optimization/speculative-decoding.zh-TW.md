# 推測式解碼

推測式解碼讓一個較便宜的草稿模型先提出數個 token，再由大型模型在一次平行前向傳播中一起檢查，藉此加速大型模型的生成。與大型模型分布一致的 token 會被保留，因此輸出與大型模型的分布完全相同，品質不會改變。

## 概述

解碼之所以慢，是因為每個 token 都需要完整地執行一次大型模型的前向傳播，而該次傳播受記憶體頻寬限制，而非運算量。檢查幾個候選 token 的成本，與產生一個 token 相近，因為大型模型可以一起處理它們。若草稿夠常猜對，大型模型每次傳播就能接受好幾個 token。

## 關鍵概念

- **草稿模型**：較小、較快的模型，負責提出候選 token。它可以是獨立的模型，也可以是加在目標模型上的一個頭。
- **驗證**：目標模型在一次平行前向傳播中，為所有候選位置評分。
- **接受規則**：一種拒絕取樣的檢驗，使輸出分布與目標模型完全相等。
- **接受率**：草稿 token 被保留的比例，決定加速的幅度。

## 運作方式

草稿模型以自迴歸方式生成 $\gamma$ 個 token。目標模型在一次傳播中，計算這些位置的機率。對於每個草稿 token $x$，若其草稿機率為 $q(x)$、目標機率為 $p(x)$，則以機率 $\min\!\left(1, \frac{p(x)}{q(x)}\right)$ 接受它。在第一次被拒絕時，從 $\mathrm{norm}\big(\max(0, p - q)\big)$ 取樣一個替代 token，本輪結束。

```mermaid
flowchart LR
  D[草稿模型提出 γ 個 token] --> V[目標模型一次傳播完成驗證]
  V --> A{逐一判斷是否接受}
  A -->|全部接受| N[保留 γ 個 token 加上一個額外 token]
  A -->|在第 i 個被拒絕| R[保留前 i-1 個 token 與一個修正 token]
```

## 關鍵方法

這個方法就是上面的草稿加驗證迴圈，搭配拒絕規則。它的關鍵性質是輸出具有目標模型的分布，這是論文所證明的。

## 結果

論文指出，在 T5-XXL 的翻譯與摘要任務上，解碼速度快 2 至 3 倍，輸出分布不變。加速幅度取決於草稿與目標的吻合程度。

## 限制

- **草稿品質**：草稿品質差時，會經常被拒絕，幾乎或完全沒有加速。
- **批次處理**：批次很大時效益會縮小，因為目標模型此時受運算限制，而非記憶體限制。
- **額外成本**：獨立的草稿模型需要記憶體，並且必須與目標模型保持同步。

## 開放問題

- 無草稿模型的變體，例如 Medusa 與 EAGLE，會在目標模型上訓練額外的頭。在不同任務上，它們的接受率與獨立草稿模型相比如何？
- 草稿 token 數 $\gamma$ 在生成過程中，應如何依接受率調整？

## 參考文獻

### 奠基性論文

- Leviathan, Y., Kalman, M. & Matias, Y. (2023). *Fast Inference from Transformers via Speculative Decoding*. ICML 2023. https://arxiv.org/abs/2211.17192 — 提出草稿與驗證式解碼，以及保留目標分布的拒絕規則。

### 相關研究

- Chen, C. et al. (2023). *Accelerating Large Language Model Decoding with Speculative Sampling*. https://arxiv.org/abs/2302.01318 — 針對大型語言模型，獨立提出的推測取樣版本。
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. https://arxiv.org/abs/2309.06180 — 說明推測式解碼與批次處理並存於服務系統的脈絡。
- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM. https://escholarship.org/content/qt78h8v7mr/qt78h8v7mr.pdf — 解釋解碼為什麼受記憶體限制，這也是一次驗證多個 token 變得便宜的原因。
- Pope, R. et al. (2023). *Efficiently Scaling Transformer Inference*. MLSys 2023. https://arxiv.org/abs/2211.05102 — 分析推論的延遲與成本取捨，決定額外的驗證工作何時值得。
