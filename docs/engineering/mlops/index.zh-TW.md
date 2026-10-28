# MLOps 與部署

MLOps 把軟體工程的紀律套用到整個機器學習生命週期。Sculley et al.（2015）的 "Hidden Technical Debt in Machine Learning Systems" 指出，模型程式碼只佔真實機器學習系統的一小部分。

## 生命週期

```mermaid
flowchart LR
  D[資料管線] --> T[訓練與實驗]
  T --> R[模型登錄]
  R --> V[驗證與核准]
  V --> S[服務化]
  S --> M[監控]
  M -->|漂移、回饋| D
```

## 關鍵實務

| 實務 | 工具／說明 |
|---|---|
| 可重現性 | 對程式碼、資料、設定與環境做版本控制；盡可能固定隨機種子 |
| 實驗追蹤 | MLflow、Weights & Biases |
| 管線與編排 | Airflow、Dagster、Kubeflow、Prefect |
| 特徵儲存 | Feast、Tecton——訓練與服務化使用一致的特徵 |
| 模型登錄 | 有版本、經核准、附血統紀錄的模型 |
| 機器學習的 CI/CD | 發布前對資料、模型品質與公平性進行自動化測試 |
| 部署策略 | 影子模式、金絲雀發布、A/B 測試、回滾 |
| 監控 | 資料漂移、預測漂移、以延遲標籤衡量的表現、延遲、成本 |

## 高效地服務 LLM

| 技術 | 效果 |
|---|---|
| 連續批次處理、PagedAttention（vLLM） | 提高吞吐量 |
| KV 快取重用／前綴（提示）快取 | 重複脈絡的延遲與成本降低 |
| 量化（INT8、INT4、FP8；GPTQ、AWQ、GGUF） | 模型更小、更快，品質損失很小 |
| 推測解碼 | 小型草稿模型提出權杖，由大型模型驗證 |
| 蒸餾與較小的模型 | 把簡單的查詢導向便宜的模型 |
| 模型路由與級聯 | 依難度為每個請求選擇模型 |
| 串流輸出 | 改善使用者感受的延遲 |

## LLMOps 的特殊事項

- **提示與模型版本控制**——模型供應商會更新模型；應鎖定版本
- **在 CI 中進行評估**（見[評估](../evaluation/index.md)）
- 多步驟代理人執行的**追蹤**（Langfuse、基於 OpenTelemetry 的追蹤）
- **護欄**：輸入與輸出過濾、個人資料遮蔽、政策分類器
- **成本管理**：權杖預算、快取、批次 API
- **人類回饋迴路**：讚／倒讚、升級處理、標註佇列

## 邊緣與裝置端 AI

- 行動裝置的 NPU 與框架（Core ML、LiteRT、ExecuTorch、ONNX Runtime）
- 在筆記型電腦與手機上執行的小型語言模型（1–8B 參數、量化）
- 隱私與延遲的好處；記憶體與功耗的限制
- 微控制器：用於感測器與穿戴裝置的 TinyML

## 負責任的營運

- AI 失敗的事件應變；模型卡與系統卡
- 在保護隱私的前提下進行紀錄
- 代理人的存取控制與機密管理
- 法規紀錄保存（例如歐盟 AI 法對高風險系統的義務）

## 學習資源

- Huyen，*Designing Machine Learning Systems* 與 *AI Engineering*
- Google，"Rules of Machine Learning" 與 "MLOps: Continuous delivery and automation pipelines"
- [Made With ML](https://madewithml.com/)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/) 教材
