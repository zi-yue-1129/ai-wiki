---
related:
- theory/paradigms/unsupervised/autoencoders-and-representations
- theory/paradigms/reinforcement-learning
- theory/paradigms/federated
- engineering/on-device-edge
aliases:
  - 電信
  - 通訊
  - Telecom
---

# 電信

電信網路是大型的即時系統：它承載流量、每幾毫秒調整一次無線電資源，而且由人負責營運，每一次故障都必須能被理解。AI 用於三個層面：無線電實體層（訊號處理）、網路管理（排程、規劃與故障偵測），以及面向客戶與營運知識的工作。最成熟的應用在網路營運；實體層的研究大多仍在研究階段。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 實體層 | 神經接收器、通道估計、端到端學習式通訊 | 研究階段；與成熟的訊號處理方法比較 |
| 無線電資源管理 | 以強化學習決定功率、頻譜與排程 | 模擬中表現可期；在實際網路上難以驗證 |
| 流量與移動預測 | 基地台與使用者資料上的時間序列與圖模型 | 用於容量規劃與節能 |
| 故障與異常偵測 | 對告警、關鍵績效指標與日誌做無監督偵測 | 可減少告警洪流；誤報很重要 |
| 自組織網路 | 自動調整基地台參數 | 在行動網路中已標準化，並設有安全限制 |
| 邊緣智慧 | 在裝置與邊緣伺服器之間拆分模型訓練與推論 | 由延遲與隱私需求驅動 |
| 客服與營運知識 | 以標準、手冊與工單為基礎的語言模型 | 電信問題需要精確、即時的答案 |

## 電信為何要求很高

- **嚴格的即時限制。** 決策必須在毫秒內完成，因此模型必須放到裝置或邊緣伺服器上。
- **嚴格的可靠度。** 一次錯誤可能讓許多使用者中斷服務，因此變更需要安全的推出與回復機制。
- **標準規範。** 許多介面由標準組織定義，這決定了可以部署什麼、如何測試。
- **異質資料。** 日誌、告警、無線電量測與計費紀錄格式與速率各不相同。

## 關鍵方法

有四類方法涵蓋該領域的大部分內容。每一項都連結到解說該方法的頁面。

- [自編碼器與學習式表徵](../../theory/paradigms/unsupervised/autoencoders-and-representations/index.md)：學習訊號的緊湊表徵，這是端到端學習式通訊背後的想法（O'Shea & Hoydis, 2017）。
- [強化學習](../../theory/paradigms/reinforcement-learning/index.md)：用於排程與資源分配的序列決策，Mao 等人（2016）首先在運算叢集排程上展示。
- [聯邦學習](../../theory/paradigms/federated/index.md)：在不把原始資料集中到單一地點的前提下，跨多個裝置或基地台訓練。
- [大型語言模型](../../theory/models/llm/index.md)：回答關於標準與營運文件的問題；TeleQnA（Maatouk 等人，2023）是測試此能力的基準。

## 關聯

模型的邊緣部署見[裝置端與邊緣 AI](../../engineering/on-device-edge/index.md)。故障偵測的一側使用[異常偵測](../../theory/paradigms/unsupervised/anomaly-detection/index.md)，與資安共用的網路部分見[資訊安全](../cybersecurity/index.md)。

## 應用

- 預測流量並調整基地台設定，在離峰時段節省能源。
- 從告警與效能資料偵測故障，讓營運人員看到可能的根本原因，而不是數百則分散的告警。
- 學習式接收器與通道估計器，在模擬中與傳統設計比較。
- 為工程師提供問答助理，答案以標準與內部文件為依據。

## 開放問題

- 學習式的實體層元件，能否證明在各種可能遭遇的條件下都與傳統設計一樣可靠？
- 強化學習控制器如何在實際網路上安全地測試？
- 語言模型能否在標準變動時維持準確，而不必頻繁重新訓練？
- 如何在不洩漏商業資訊的前提下，為訓練共享多家營運商的資料？

## 參考文獻

### 開創性論文

- O'Shea, T. & Hoydis, J. (2017). An Introduction to Deep Learning for the Physical Layer. *IEEE Transactions on Cognitive Communications and Networking*. https://doi.org/10.1109/TCCN.2017.2758370 — 顯示自編碼器能以端到端的方式學習一套通訊系統，把發射端與接收端視為同一個神經網路。
- Mao, H., Alizadeh, M., Menache, I. & Kandula, S. (2016). Resource Management with Deep Reinforcement Learning. *Proceedings of the 15th ACM Workshop on Hot Topics in Networks*. https://doi.org/10.1145/3005745.3005750 — 把深度強化學習用於運算叢集的排程與資源分配，是網路控制的早期範例。
- Maatouk, A., Ayed, F., Piovesan, N., De Domenico, A., Debbah, M. & Luo, Z.-Q. (2023). TeleQnA: A Benchmark Dataset to Assess Large Language Models Telecommunications Knowledge. arXiv. https://arxiv.org/abs/2310.15051 — 用來測試大型語言模型電信知識的電信問題基準資料集。

### 綜述與教科書

- Zhang, C., Patras, P. & Haddadi, H. (2019). Deep Learning in Mobile and Wireless Networking: A Survey. *IEEE Communications Surveys & Tutorials*. https://doi.org/10.1109/COMST.2019.2904897 — 綜述行動與無線網路各類任務中的深度學習，包括流量、移動與資源分配。
- Qin, Z., Ye, H., Li, G. Y. & Juang, B.-H. F. (2019). Deep Learning in Physical Layer Communications. *IEEE Wireless Communications*. https://doi.org/10.1109/MWC.2019.1800601 — 回顧深度學習在通道估計、訊號偵測與解碼等實體層任務上的應用。

### 文章與文件

- Zhou, Z., Chen, X., Li, E., Zeng, L., Luo, K. & Zhang, J. (2019). Edge Intelligence: Paving the Last Mile of Artificial Intelligence With Edge Computing. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2019.2918951 — 綜述模型訓練與推論如何在裝置與邊緣伺服器之間拆分。
