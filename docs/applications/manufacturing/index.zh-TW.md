# 製造與工業

## 概況

| 領域 | 方法 | 價值 |
|---|---|---|
| 視覺品質檢測 | CNN、異常偵測（PatchCore、PaDiM）、少樣本缺陷偵測 | 更快、更一致地發現刮痕、裂縫與錯位 |
| 預測性維護 | 針對振動、溫度、電流的時間序列模型；剩餘使用壽命估計 | 減少非計畫停機 |
| 製程最佳化 | 貝氏最佳化、強化學習、製程的替代模型 | 良率、能耗、產能 |
| 數位分身 | 與感測器資料同步的模擬模型 | 假設性分析、虛擬試車 |
| 供應鏈與規劃 | 需求預測、庫存最佳化、排程 | 韌性與成本 |
| 機器人與自動化 | 彈性揀取、組裝、協作型機器人 | 見[機器人](../robotics/index.md) |
| 生成式設計 | 拓撲最佳化、生成式 CAD | 更輕、更堅固的零件 |
| 知識保存 | 以說明書、維修紀錄與標準作業程序為基礎的 LLM 助理 | 降低對即將退休專家的依賴 |

## 半導體與電子

- **晶片設計**：強化學習輔助的平面規劃（Mirhoseini et al., 2021）；ML 驅動的 EDA 工具用於佈局、繞線與驗證；LLM 生成 RTL
- **晶圓廠良率**：晶圓圖缺陷分類、虛擬量測、製程管制模型
- **微影**：以 GPU 與機器學習加速的計算微影

## 實務挑戰

- **缺陷範例少**：缺陷很罕見 → 非監督式異常偵測、合成資料、少樣本方法
- **領域偏移**：新產品線、光線與感測器的更換
- **邊緣部署**：在工廠硬體上做即時推論；低功耗的選項包括[神經形態與脈衝式方法](../../brain-mind/snn-neuromorphic/index.md)
- **資料孤島**與 OT／IT 整合
- 面向操作員的**可解釋性**與安全認證

## 關鍵方法

下列三種方法與本頁最相關。每一項都連結到解釋該方法的頁面。

- [異常偵測](../../theory/paradigms/unsupervised/anomaly-detection/index.md)：PatchCore 與 PaDiM 依正常零件的分布為瑕疵評分，適合稀少瑕疵（Roth et al., 2021；Defard et al., 2020）。
- [殘差 CNN](../../theory/models/cnn/backbones-and-scaling/resnet/index.md)：用於視覺品質檢測與瑕疵分類的骨幹網路（He et al., 2016）。
- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md)：支撐以手冊與維修紀錄為基礎之 LLM 助手的架構（Vaswani et al., 2017）。

## 參考文獻

### 開創性論文

- Roth et al. (2021). Towards Total Recall in Industrial Anomaly Detection. arXiv. https://arxiv.org/abs/2106.08265 — PatchCore 以比較影像區塊特徵與正常區塊記憶庫的方式為異常評分。
- Defard et al. (2020). PaDiM: a Patch Distribution Modeling Framework for Anomaly Detection and Localization. arXiv. https://arxiv.org/abs/2011.08785 — PaDiM 對正常區塊特徵的分布建模，用於定位異常。
- Bergmann et al. (2019). MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection. CVPR. https://doi.org/10.1109/CVPR.2019.00982 — 工業影像基準資料集，用於無監督瑕疵偵測。
- Mirhoseini et al. (2021). A graph placement methodology for fast chip design. *Nature*. https://doi.org/10.1038/s41586-021-03544-w — 以強化學習進行晶片平面規劃，是上文晶片設計敘述的依據。
- He, K. et al. (2016). Deep Residual Learning for Image Recognition. CVPR. https://doi.org/10.1109/CVPR.2016.90 — 殘差連接，使非常深的 CNN 能夠訓練。
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力為核心。
