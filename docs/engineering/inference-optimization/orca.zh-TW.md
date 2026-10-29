---
translation_reviewed: 2026-10-29
---

# Orca：逐迭代排程

Orca 是以單次模型迭代為單位進行排程的服務系統。完成的請求會離開批次，等待中的請求會在迭代之間加入，因此避免了以請求為單位的批次處理，在短請求上造成的閒置。這個概念稱為連續批次處理（continuous batching），現在已是 LLM 服務引擎的標準做法。

## 概述

生成是逐步進行的：每個請求在每次迭代產生一個 token，直到結束。以請求為單位的批次處理會先把請求分組，然後等整批完成，因此同一批中的長請求仍在跑時，短請求只能閒置。Orca 把排程決策移到迭代層級，使 GPU 總是在仍然活躍的請求上運算。

## 關鍵概念

- **迭代**：模型的一次前向傳播，為每個活躍的請求產生一個新 token。
- **逐迭代排程**：在每次迭代之前重新決定批次，而不是在每個請求之前決定。
- **選擇性批次處理**：把可以在請求之間共用的計算合併批次，但由於序列長度不同，注意力則逐一請求處理。

## 運作方式

在每次迭代之前，排程器會移除已完成的請求、加入提示能放進記憶體的等待請求，然後對得到的批次執行一次迭代。線性層以一次批次矩陣乘法執行。注意力則逐請求執行，因為每個請求都有自己快取的 key 與 value。

![連續批次處理四個迭代的動畫：B 完成後 C 加入批次，之後 A 完成而 C 持續生成。](../../assets/concept-animations/orca-continuous-batching-motion.svg)

*原創教學動畫，CC BY-SA 4.0。* t1–t4 表示**模型迭代**，不是實測的經過時間。A、B、C 是示意請求；數字代表各請求在該步的示意輸出詞元數。B 在 t1 後完成，讓等待中的 C 於 t2 加入；A 在 t3 後完成，C 則繼續執行。移動外框標示目前迭代，GPU 批次標籤也隨之切換。此簡化時序假設新加入請求的提示已準備好處理，省略預填充與記憶體容量細節，**並非吞吐量實測軌跡**。MkDocs 網站提供可用鍵盤操作的「播放／暫停」及減少動態效果支援；GitHub 可查看[四次迭代的靜態時序圖](../../assets/concept-animations/orca-continuous-batching-still.svg)。詳見 [Orca 原始論文](https://www.usenix.org/conference/osdi22/presentation/yu)。

## 關鍵方法

Orca 的方法就是上面所述的逐迭代排程器與選擇性批次處理。論文的證據，是在相近延遲下，把生成式 GPT 類模型的吞吐量與以請求為單位的批次處理相比。

## 結果

論文指出，對生成式模型而言，相較於以請求為單位的批次處理，吞吐量有大幅提升，且延遲相近。確切數字取決於模型大小與工作負載，應以論文的評估章節為準。

## 限制

- **記憶體碎片**：在這個設計中，不同長度的請求仍需要連續的記憶體，這是之後的分頁 KV 快取工作所要解決的問題。
- **排程政策**：決定接納哪個等待中的請求，會影響公平性與延遲；論文採用的是簡單的政策。
- **依賴工作負載**：當請求的輸出長度差異很大時，增益最大。

## 開放問題

- 排程器應如何平衡佔用許多預填充迭代的長提示，與等待插槽的短請求？
- 分塊預填充把提示處理與解碼步驟混合，但它對延遲目標的影響取決於服務目標。

## 參考文獻

### 奠基性論文

- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — 提出生成式模型服務的逐迭代排程與選擇性批次處理。

### 相關研究

- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. https://arxiv.org/abs/2309.06180 — 在逐迭代排程之上加入分頁式 KV 快取記憶體管理，即 vLLM 的做法。
- Pope, R. et al. (2023). *Efficiently Scaling Transformer Inference*. MLSys 2023. https://arxiv.org/abs/2211.05102 — 分析推論工作負載與分割方式，如何與批次大小和延遲互動。
- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM. https://escholarship.org/content/qt78h8v7mr/qt78h8v7mr.pdf — 提供效能模型，解釋為什麼小批次會讓 GPU 利用率偏低。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS 2022. https://arxiv.org/abs/2205.14135 — 加速每次迭代中逐請求執行的注意力核心。
