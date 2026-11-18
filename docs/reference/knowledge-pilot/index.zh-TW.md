---
status: draft
references: not-required
---

# 證據與檢索試點

這個小型 **LoRA／QLoRA 試點**，把精簡的雙語主張連到有版本的原始來源、來源位置與明確限制。它不是全站準確性認證，也不能取代原論文，更不代表已重現實驗。

## 閱讀與檢查

- 概念解說與圖像見 [LoRA 章節](../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.zh-TW.md)與 [QLoRA 章節](../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.zh-TW.md)。
- 下載[八張證據卡 JSON](../../assets/knowledge/lora-qlora.json)。每張卡包含英文與繁體中文的摘要**及限制**、wiki 頁面與章節、有版本的原始來源及位置，以及限定範圍的來源閱讀日期。
- 本次查閱 [LoRA v2](https://arxiv.org/abs/2106.09685v2) 第 4.1–4.2 節，以及 [QLoRA v1](https://arxiv.org/abs/2305.14314v1) 第 3–4 節與附錄 B.2。閱讀來源不等於獨立實驗重現或專家認證；核對範圍僅限列出的主張，不是整個連結章節。

| 證據卡 ID | 要查清楚的問題 |
|---|---|
| `lora-update` | 低秩限制作用於基底還是更新？ |
| `lora-merge` | 適配器分支在什麼條件下可以合併？ |
| `qlora-precision` | 4-bit 儲存是否等於 4-bit 運算或全參數訓練？ |
| `qlora-nf4` | NF4 的分布前提是什麼？ |
| `qlora-double` | 雙重量化量化的是什麼？ |
| `qlora-paging` | 分頁搬移什麼，又不保證什麼？ |
| `qlora-65b` | 48 GB 微調 65B 是特定配置結果，還是通用容量保證？ |
| `qlora-comparison` | 哪些規模與全參數微調比較，哪些與 16-bit LoRA 比較？ |

## 不用帳號或 API 的查詢

在本倉庫的本機副本使用 Python 3.12 或更新版本；查詢工具只使用標準函式庫，不需模型呼叫、網路、向量服務或 MCP 伺服器。

```bash
python scripts/knowledge.py search 'QLoRA 運算精度'
python scripts/knowledge.py search 'full fine-tuning baseline'
python scripts/knowledge.py get qlora-comparison
```

工具回傳 JSON 證據**候選項目**，不是生成答案。`lexical_score` 是排序分數，不是機率或可信度。英文詞與中文雙字配對刻意保持簡單，不是通用語意搜尋。相關結果不一定支持問題的每個前提。沒有重疊詞的查詢回傳 `no_matching_evidence`，不代表其他地方也沒有答案。遇到未涵蓋的問題，應繼續查閱原始來源，或明確說試點未涵蓋。

Agent 應保留限制與來源版本；回答重要或當下狀態的問題時要開啟原始來源，並引用來源，而不是把自動檢查當真相。比較檢索結果時，應固定 wiki commit 與來源版本。一般使用者仍使用原網站的導覽與搜尋；這個 CLI 是獨立且範圍有限的試點，不取代全站搜尋。

## 驗證與誠實評估

```bash
python scripts/knowledge.py validate
python -m unittest discover -s scripts -p 'test_knowledge.py'
python -m unittest discover -s scripts -p 'test_wiki_review_status.py'
python scripts/knowledge.py evaluate
```

驗證會檢查卡片 ID、必填雙語欄位、頁面與章節是否存在、證據參照及審核資料。它**不會**判斷來源在科學上是否支持主張、查詢即時網址、核對所有翻譯，也不會訓練模型；這些仍要查閱來源及另外驗證。

版本控制中的測試題包含 16 題英／中文檢索問題，以及三題不相關或沒有證據的對照題。`evaluate` 檢查預期卡片是否進入前三名，或不相關對照是否回傳空結果。這些公開、人工撰寫的題目只測試小型索引是否正常，不是未見過題目的 agent 回答、引用正確率、通用召回率或優於網搜的評測；不得把分數宣傳為知識準確率。

後續比較應使用未用於開發的真實問題、固定模型與預算，分成不使用 wiki、一般網搜、使用 wiki 三組，分別評估事實正確性、來源支持、遺漏限制、拒答、延遲及 token 成本。目前尚未執行這種實驗。

## 維護規範

1. 原章節仍是完整解說的主要位置；證據卡是限定範圍的檢索視圖，不是第二套百科。
2. 主張或來源改變時，同步更新雙語摘要、限制與來源位置。重新閱讀來源才變更 `checked_on`；局部卡片核對不能刷新整頁審核日期。
3. 頁面標題消失會使驗證失敗；同標題下的內容改變**不會**自動觸發語意重驗。修改 LoRA／QLoRA 時，審查者須檢查對應卡片。CI 通過無法偵測所有過期摘要。
4. `status: complete` 與證據審核分開；它只代表寫作進度，不代表事實驗證，詳見[風格指南](../style-guide/index.zh-TW.md)。
5. 唯讀使用者可下載靜態 JSON 或使用 CLI，不需要憑證、上傳或第三方追蹤。主張與摘要維持 wiki 的 CC BY-SA 4.0 授權，查詢程式採 MIT 程式碼授權。
