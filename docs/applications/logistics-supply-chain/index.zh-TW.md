# 物流與供應鏈

物流把預測變成實際的移動：哪些貨物要送去哪裡、搭哪一輛車、在什麼時間、庫存維持多少。AI 在三個層面發揮作用。它預測需求與中斷；它解決過於龐大、精確方法無法處理的路線與排程問題；它引導倉庫與港口內的機器人和車輛。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 需求預測 | 梯度提升樹、機率式遞迴與 Transformer 預測器 | 預測必須是機率式的，才能支援庫存決策 |
| 庫存與補貨 | 以學習得到的需求分布進行報童式最佳化 | 預測誤差與前置時間同樣重要 |
| 路線與排程 | 學習式建構啟發法、神經組合最佳化、帶有學習元件的古典求解器 | 車輛路徑、配送順序、人員排班 |
| 倉儲機器人 | 揀貨與分揀機器人、學習式抓取、機隊協調 | 見[機器人](../robotics/index.md) |
| 港口與貨運作業 | 碼頭排程、貨櫃追蹤、海關風險評分 | 資料共享常受限 |
| 韌性與短缺預測 | 供應商依賴關係的網路模型；早期預警訊號 | 在中斷發生前很難驗證 |

## 為什麼困難

- **組合規模**：路線與排程問題的規模增長快於任何精確方法能處理的速度，遑論全國等級。
- **預測驅動決策**：平均上準確的預測，仍可能在尾端導致缺貨，因此校準與準確度同樣重要。
- **資料分散**：供應商、承運商與倉庫很少共用同一個系統的資料。
- **體制轉變**：疫情、罷工與貿易規則會打破歷史模式。

## 關鍵方法

- [圖神經網路](../../theory/models/gnn/index.md)：把供應商與運輸網路建模為圖，適合用於韌性分析。
- [強化學習](../../theory/paradigms/reinforcement-learning/index.md)：在模擬中透過試錯學習派遣與庫存策略，再轉移到實際營運。
- [Sim-to-real 轉移](../../theory/paradigms/transfer/sim-to-real/index.md)：在模擬倉庫或車隊中學到的策略，必須先經過調整才能用於真實硬體。
- [串流與概念漂移](../../theory/paradigms/online/streaming-and-concept-drift/index.md)：隨情況改變而持續更新的需求模型。

## 相關連結

- 路線與排程背後的最佳化方法見[最佳化](../../theory/optimization/index.md)頁。
- 自駕車與運輸網路見[自動駕駛與運輸](../autonomous-driving/index.md)。
- 製造業規劃與本頁共用許多預測與排程方法，見[製造與工業](../manufacturing/index.md)。

## 應用

- 零售與製造業的需求預測與庫存規劃
- 最後一哩配送的路線與派遣
- 倉儲揀貨與分揀機器人
- 港口排程與貨櫃風險篩檢
- 供應商短缺的早期預警

## 風險與限制

- **脆弱的最佳化**：針對歷史網路調校的解，可能在某條路線關閉或某家供應商停止供貨時失效。
- **牛鞭效應**：許多企業使用相似的預測模型，會放大訂單的波動。
- **勞動與安全**：自動化倉庫改變了工作設計與傷害型態，需要持續監測。
- **基準**：許多神經路線結果基於合成題目；在真實道路網路與限制條件下，表現可能不同。

## 開放問題

- 學習式路線啟發法能否擴展到真實營運所施加的附加限制（時間窗、載重、法規）。
- 企業應如何共享資料以提升韌性，同時不暴露商業機密。

## 參考文獻

### 開創性論文

- Kool, W., van Hoof, H. & Welling, M. (2019). Attention, Learn to Solve Routing Problems! *ICLR*. https://arxiv.org/abs/1803.08475 — 以強化學習訓練注意力模型來建構路線問題的解，是許多神經路線求解器的基礎。
- Vinyals, O., Fortunato, M. & Jaitly, N. (2015). Pointer Networks. arXiv. https://arxiv.org/abs/1506.03134 — 提出輸出指向輸入位置的序列模型，很適合排序類問題，例如路線。
- Bello, I. et al. (2016). Neural Combinatorial Optimization with Reinforcement Learning. arXiv. https://arxiv.org/abs/1611.09940 — 以強化學習為旅行推銷員問題學習神經策略，不需人工設計的啟發法。
- Salinas, D. et al. (2020). DeepAR: Probabilistic forecasting with autoregressive recurrent networks. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2019.07.001 — 對眾多相關時間序列產生機率式需求預測，是供應鏈中常見的設定。

### 綜述與教科書

- Bengio, Y., Lodi, A. & Prouvost, A. (2021). Machine learning for combinatorial optimization: A methodological tour d'horizon. *European Journal of Operational Research*. https://doi.org/10.1016/j.ejor.2020.07.063 — 綜述機器學習如何用於組合最佳化求解器之內與之旁。
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2021.11.013 — 報告一場大型零售需求預測競賽，比較統計方法與機器學習方法。
