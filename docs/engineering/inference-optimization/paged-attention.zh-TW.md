# PagedAttention 與 vLLM

PagedAttention 把 KV 快取儲存在固定大小的區塊中，類似虛擬記憶體的分頁，而不是每個請求一塊連續的緩衝區。vLLM 服務系統即以此為核心。分頁大幅減少了碎片與過度預留所浪費的記憶體，使同一裝置能容納更多請求。

## 概述

服務系統必須把每個活躍請求的 key 與 value 保留在記憶體中。若每個請求的快取都預留為一塊連續緩衝區，大小以可能的最大長度計算，大部分記憶體就會被浪費：有些空間預留給永遠不會生成的 token，而不同長度的請求來來去去時，又會產生空隙。PagedAttention 借用作業系統的分頁概念：需要時才配置區塊，並透過區塊表對應到每個請求。

## 關鍵概念

- **區塊**：固定數量 token 的 key 與 value，儲存在同一塊實體記憶體區域中。
- **區塊表**：每個請求專屬的映射，從邏輯區塊位置對應到實體區塊，這些實體區塊不需要連續。
- **寫時複製共用**：具有共同前綴（例如共用的系統提示）的請求可以指向相同的區塊，直到其中一個開始分歧。

## 運作方式

請求開始時，系統為其提示配置區塊。解碼期間，只有在目前區塊填滿時才配置新區塊。注意力核心透過區塊表讀取 key 與 value，因此會從分散的區塊中收集資料。記憶體不足時，排程器可以搶佔某個請求，並換出或重新計算它的區塊。

<img data-source-asset-urls src="../../assets/concept-animations/paged-block-mapping-still.svg" data-motion-src="../../assets/concept-animations/paged-block-mapping-motion.svg" data-still-src="../../assets/concept-animations/paged-block-mapping-still.svg" width="640" height="360" alt="當詞元增加時，依序出現三個邏輯 KV 區塊；區塊表將它們對應至非連續的實體區塊 P2、P0、P3，P1 則保持空閒。">

*原創教學動畫，CC BY-SA 4.0。* 彩色路徑代表**邏輯區塊與實體區塊的映射關係**；移動的圓點示意沿已建立映射進行存取的導引，不代表 GPU 資料實際搬移的路徑或延遲量測。示例假設**每個區塊存放兩個示意詞元**，三個邏輯區塊依序映射至 P2、P0、P3，P1 維持未使用。只有新增一組雙詞元區塊時才需要配置下一個實體區塊，實體索引不必遵循詞元順序。動畫省略注意力核心、共用與搶佔細節。MkDocs 可使用**播放／暫停**（Enter 或 Space）；窄螢幕可聚焦圖像區域並以鍵盤水平捲動；偏好減少動態效果時預設暫停。[GitHub 可閱讀的最終映射](../../assets/concept-animations/paged-block-mapping-still.svg)。

### 教學算例：共用尾端區塊的寫時複製

<div tabindex="0" role="region" aria-label="可水平捲動的教學動畫，使用左右方向鍵" style="max-width:100%;overflow-x:auto">
<img data-source-asset-urls src="../../assets/concept-animations/paged-copy-on-write-still.svg" data-motion-src="../../assets/concept-animations/paged-copy-on-write-motion.svg" data-still-src="../../assets/concept-animations/paged-copy-on-write-still.svg" alt="兩個序列最初共用 P0 與 P1；B 先複製尾端有效槽位至 P2，再更新映射並加入 y；A 隨後在 P1 加入 x，P0 仍有兩個參照。" width="640" height="360" style="width:640px;min-width:640px;max-width:none;height:auto" />
</div>

[GitHub 靜態預覽](../../assets/concept-animations/paged-copy-on-write-still.svg) · MkDocs 可用 Enter 或 Space 操作**播放／暫停**，偏好減少動態效果時預設顯示靜態圖。

兩個平行取樣序列 A 與 B 共用三個詞元的前綴 `a b c`。若每個區塊有兩個詞元槽位，P0 已填滿，P1 只有一個有效槽位。兩者的區塊表最初都是 [P0, P1]，P0、P1 與尚未配置的 P2 的參照計數依序為 (2, 2, 0)。B 先保留 P2 並複製有效尾端狀態 c（移動圓點示意此相依性，不代表實際傳輸量），複製完成後才將映射更新為 [P0, P2]，參照計數變成 (2, 1, 1)。此時 B 能加入 y，A 也能獨立加入 x，而不會破壞彼此的序列。

| 狀態 | A 的區塊表 | B 的區塊表 | 已配置實體區塊數 |
|---|---|---|---:|
| 共用前綴 | P0, P1 | P0, P1 | 2 |
| 保留並複製 P2 | P0, P1 | P0, P1 | 3 |
| 更新映射並延伸 | P0, P1 | P0, P2 | 3 |

P0 的內容沒有被寫入修改，因此維持共用。最終只需三個實體區塊，而非各自配置時的四個。此計數不包含配置器中繼資料，也不預測實際頻寬；實作可能複製完整實體區塊，而非僅有效槽位。操作順序為教學示意，不是並行控制協定或實測軌跡。平行取樣與寫時複製機制見參考文獻 Kwon 等人（2023）。

*原創教學動畫，CC BY-SA 4.0。*

## 關鍵方法

這個方法是帶有隨需配置與共用的區塊表，並以自訂的注意力核心實作。論文的證據比較了記憶體浪費與服務吞吐量，對象是先前的系統。

## 結果

論文指出，先前的服務系統有大部分 KV 快取記憶體因碎片與過度預留而浪費，而 vLLM 在相近延遲下達到比那些系統更高的吞吐量。確切數字取決於模型與工作負載。

## 限制

- **核心複雜度**：注意力必須透過間接定址讀取 key 與 value，因此需要專門的核心。
- **依賴工作負載**：前綴共用帶來的效益，取決於有多少請求共用提示。
- **搶佔成本**：記憶體耗盡時，換出或重新計算區塊會增加延遲。

## 開放問題

- 針對特定模型與序列長度組合，區塊大小應如何選擇？
- 前綴共用與淘汰政策能否在不傷害尾端延遲的前提下一起運作？

## 參考文獻

### 奠基性論文

- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. https://arxiv.org/abs/2309.06180 — 提出分頁式 KV 快取管理與 vLLM 服務系統。

### 相關研究

- Yu, G.-I. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI 2022. https://www.usenix.org/conference/osdi22/presentation/yu — 提供 vLLM 所建立於其上的逐迭代排程。
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS 2022. https://arxiv.org/abs/2205.14135 — 說明注意力核心如何減少記憶體流量，與基於區塊的快取存取是相鄰的問題。
- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM. https://escholarship.org/content/qt78h8v7mr/qt78h8v7mr.pdf — 解釋為什麼受記憶體限制的解碼，使快取佈局成為效能問題。
- Pope, R. et al. (2023). *Efficiently Scaling Transformer Inference*. MLSys 2023. https://arxiv.org/abs/2211.05102 — 討論快取管理在大規模下所牽涉的記憶體與通訊成本。
