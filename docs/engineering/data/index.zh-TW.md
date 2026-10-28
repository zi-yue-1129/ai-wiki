# 資料

「以資料為中心的 AI」：對大多數實際專案來說，更好的資料勝過更好的模型。

## 生命週期

```mermaid
flowchart LR
  C[蒐集] --> L[標註] --> CL[清理與去重] --> S[切分] --> V[版本化與記錄] --> M[正式環境監控]
  M --> C
```

## 蒐集

- 第一方的日誌、感測器與紀錄；公開資料集；網路爬取（須遵守 robots.txt 與服務條款）；授權資料；模擬
- 抽樣必須符合實際部署的族群——要思考誰被遺漏了
- 從一開始就處理同意、隱私與著作權問題（GDPR 與各地的隱私法）

## 標註

| 方法 | 說明 |
|---|---|
| 專家標註 | 醫學、法律、科學領域的黃金標準；成本高 |
| 眾包 | 可擴大規模；需要品質控管（重複標註、黃金題、一致性指標） |
| 弱監督／程式化監督 | 標註函式與標籤模型；見[資料編程與弱監督](data-programming.zh-TW.md) |
| 主動學習 | 只標註有資訊量的樣本（[主動學習](../../theory/paradigms/active/index.md)） |
| 模型輔助或 LLM 標註 | 快速；需與人工標籤比對驗證，並留意系統性偏誤 |
| 偏好資料 | 用於 RLHF／DPO 的成對比較 |

撰寫附有範例與邊界案例的**標註指南**；測量標註者之間的一致性（Cohen's κ、Fleiss' κ、Krippendorff's α）。

## 清理與品質

- 去重（完全重複與近似重複）——對 LLM 預訓練至關重要，也能避免測試資料洩漏；見 [MinHash 去重](minhash-deduplication.zh-TW.md)
- 標籤錯誤偵測（confident learning／cleanlab）；見[置信學習](confident-learning.zh-TW.md)
- 離群值與損壞檢查、結構驗證（Great Expectations、pandera）
- 網路文字：語言辨識、品質分類器、毒性與個人資料過濾（例如 FineWeb、DCLM 流程）

## 避免洩漏的切分

- 依**實體**（病人、使用者、裝置）、依**時間**，或在意跨地點泛化時依**地點**切分
- 在切分之間做去重
- 保留一個鎖定的最終測試集

## 合成資料

- 用途：資料擴增、罕見事件、隱私、指令微調、推理軌跡、機器人與自動駕駛的模擬
- 風險：放大模型偏見；當模型在自己的輸出上遞迴訓練、又沒有新的真實資料時，會出現**模型崩潰**（Shumailov et al., 2024, *Nature*）；需要驗證（例如執行生成的程式碼、檢查數學答案）

## 文件記錄與治理

- **Datasheets for Datasets**（Gebru et al.）與**資料卡**；模型則使用**模型卡**
- 資料版本控制：DVC、lakeFS、Hugging Face 的資料集版本
- 資料血統與存取控管；保留政策
- 授權與來源：Data Provenance Initiative 的稽核報告指出，在廣泛使用的託管網站上，資料集授權的誤分類相當普遍

## 關鍵方法

每個具名方法都有自己的頁面，內容包括它要解決的問題、核心想法、演算法、報告的結果與限制。下表比較本頁的三個方法。

| 方法 | 要解決的問題 | 核心想法 | 主要取捨 | 頁面 |
|---|---|---|---|---|
| MinHash 去重 | 文件的近似複本會讓訓練文字重複 | 緊湊的簽章估計 Jaccard 相似度，LSH 找出候選配對 | 門檻的選擇；會漏掉改寫的文字 | [MinHash 去重](minhash-deduplication.zh-TW.md) |
| 置信學習 | 人工標註集中的標籤錯誤 | 樣本外機率與置信聯合矩陣找出可能的錯誤並剪除 | 需要交叉驗證的預測 | [置信學習](confident-learning.zh-TW.md) |
| 資料編程 | 標籤昂貴，但弱訊號便宜 | 標註函式由生成式標籤模型整合，不需要真實答案 | 品質取決於所寫的函式 | [資料編程與弱監督](data-programming.zh-TW.md) |

## 規模參考

| 領域 | 典型規模 |
|---|---|
| ImageNet-1k | 128 萬張有標註影像 |
| LAION-5B | 58.5 億組影像—文字配對；2023 年因一項研究指出含有非法內容的連結而下線，2024 年釋出清理後的版本 Re-LAION-5B |
| 開放的預訓練語料 | 數兆（trillion）個 token（Dolma 為三兆） |
| 指令微調 | 數千筆範例可能已足夠：LIMA 報告約 1,000 筆精選範例就能有很好的結果，因此品質比數量重要 |

## 參考文獻

### 重要論文

- Gebru, T. et al. (2018). *Datasheets for Datasets*. arXiv:1803.09010. https://arxiv.org/abs/1803.09010 — 提出標準化的資料集數據表，記錄資料集的動機、組成、蒐集方式與預期用途。
- Northcutt, C. G., Jiang, L. & Chuang, I. L. (2021). *Confident Learning: Estimating Uncertainty in Dataset Labels*. arXiv:1911.00068. https://arxiv.org/abs/1911.00068 — 由樣本外預測機率估計並剪除標籤錯誤。

### 相關工作

- Northcutt, C. G., Athalye, A. & Mueller, J. (2021). *Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks*. NeurIPS 2021 Datasets and Benchmarks Track. arXiv:2103.14749. https://arxiv.org/abs/2103.14749 — 在廣泛使用的基準測試集中找出標籤錯誤，並顯示它們會改變模型排名。
- Penedo, G. et al. (2024). *The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale*. arXiv:2406.17557. https://arxiv.org/abs/2406.17557 — 一個大型網頁文字語料，以及產生它的過濾流程。
- Zhou, C. et al. (2023). *LIMA: Less Is More for Alignment*. arXiv:2305.11206. https://arxiv.org/abs/2305.11206 — 顯示一小組精心整理的指令範例，就能得到很好的指令遵循結果。
- Longpre, S. et al. (2023). *The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution in AI*. arXiv:2310.16787. https://arxiv.org/abs/2310.16787 — 對廣泛使用的 AI 訓練資料集的授權與來源標示所做的大規模稽核。
- Shumailov, I. et al. (2024). *AI models collapse when trained on recursively generated data*. *Nature* 631, 755–759. https://doi.org/10.1038/s41586-024-07566-y — 顯示以模型生成資料遞迴訓練，會失去原始分布的尾部。

延伸閱讀：[以資料為中心的 AI 資源（MIT 課程）](https://dcai.csail.mit.edu/)。
