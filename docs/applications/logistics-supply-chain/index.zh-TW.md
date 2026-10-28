---
translation_reviewed: 2026-10-28
---

# 物流與供應鏈

AI 被用於貨物移動的各個環節：預測啟動供應鏈的需求、為卡車規劃路線、協調倉庫中的機器人、營運港口，以及在缺貨影響顧客之前發出警示。這些問題規模龐大、彼此相依，而且充滿不確定性。在機器學習加入之前，作業研究（operations research, OR）已研究這些問題數十年。

## 概述

供應鏈是由供應商、工廠、倉庫、貨運業者與門市組成的網絡，負責把原材料變成貨架上的商品。它的決策分屬好幾個時間尺度：網路設計與產能以年為單位設定，庫存與生產計畫以週為單位，路線、派車與倉庫揀貨則以小時或分鐘計。上游的決策依賴下游做出的預測，因此一個糟糕的預測會擴散成糟糕的庫存水準、白跑的車次與錯過的交貨。

這個問題有三項特點，使它特別困難。需求不確定，而且常常起伏劇烈，包括新產品與間歇性的銷售。組合性的選擇，例如哪台車去哪個停靠點、以什麼順序前往，其數量的增長快於任何窮舉搜尋所能處理的速度。此外，環境在執行期間還會變化：訂單陸續到達、車輛故障、港口壅塞。傳統的作業研究以數學規劃、啟發式方法與模擬來處理這些問題。機器學習則加入了從大量歷史資料學得的預測、從已解決的實例或試誤中學得的路線啟發式方法，以及依據局部觀測行動的機器人控制策略。

學習型方法在預測、路線規劃與倉儲機器人方面發展得最為成熟。港口作業仍主要依賴作業研究，而韌性則是最不成熟的領域。

## 關鍵概念

- **需求預測**：對每個品項與地點未來銷售量的估計。預測常需要在多個彙總層級上進行，例如依品項、門市與區域，這稱為階層式預測。
- **牛鞭效應（bullwhip effect）**：訂單的變異隨著自顧客往上游移動而放大的傾向。Lee 等人（1997）把它歸因於四個來源：需求信號的處理、配給賽局、訂單批次化與價格變動。[^1]
- **車輛路徑問題（vehicle routing problem, VRP）**：在容量、時間窗等限制下，把配送停靠點分派給車輛，使總成本最低。它是旅行推銷員問題的推廣。
- **動態路線規劃**：資訊（例如新訂單）在執行期間陸續到達，因而必須修正計畫的路線問題。Psaraftis（1995）回顧了這種設定。
- **多智能體路徑規劃（multi-agent path finding, MAPF）**：為共用同一張地圖的許多機器人找出無碰撞的路徑，例如在倉庫中搬運貨品的機器人。
- **可存續性與韌性**：供應鏈吸收干擾並恢復的能力。Ivanov（2020）把它與敏捷性、永續性一併考量。

## 運作方式

```mermaid
flowchart LR
  S[銷售與外部信號] --> F[機率預測]
  F --> P[庫存與生產計畫]
  P --> R[路線與排程]
  R --> W[倉儲機器人與港口作業]
  W --> D[配送與紀錄]
  D -.->|新資料| F
```

上圖的迴圈中，每個階段都使用不同的方法。預測最有用的形式是分布，而非單一數字，因為庫存水準取決於高需求發生的可能性，而不只是平均值。Petropoulos 等人（2020）回顧了跨領域的預測方法，從古典統計到機器學習都有涵蓋。[DeepAR](deepar/index.md) 透過同時在許多序列上訓練一個循環模型來產生分布。以 Transformer 為基礎的預測器，例如 Temporal Fusion Transformer，能把靜態共變量與已知的未來輸入（例如規劃中的促銷）和歷史序列一併納入（Lim 等人，2019）。M5 準確度競賽是針對階層式零售銷售的大型基準測試，它比較了許多預測方法並公布了結果（Makridakis 等人，2022）。

路線規劃把計畫轉為車輛的行駛路線。精確求解器與元啟發式方法仍是標準工具。神經網路方法則學習一個策略，逐一停靠地一步步建構路線。Nazari 等人（2018）以策略梯度訓練了這樣的策略來解 VRP。Kool 等人（2018）的[注意力模型](attention-model-routing/index.md)改進了這項工作，並以同一組超參數應用於數種路線變體。學習得到的策略在訓練完成後執行速度很快，但它們仍以強大的求解器作為比較基準，目前尚未能取代求解器。

倉儲機器人屬於多智能體路徑規劃問題。機器人隊伍在格狀地圖上搬運貨架或貨箱，核心任務是為每台機器人找出不會碰撞或陷入僵局的路徑。[PRIMAL](primal/index.md) 為每台機器人訓練一個共用策略，結合強化學習與對中央專家規劃器的模仿，使機器人能依據自身的局部視野線上重新規劃。

港口與貨運作業涉及規劃碼頭泊位、岸吊、堆場設備與卡車。一篇關於貨櫃碼頭作業研究的回顧，將這些規劃問題與其所使用的方法加以分類（Voß 等人，2004）。在這個領域，最佳化仍居核心，學習則主要透過船舶與卡車到港時間的預測進入。

韌性與短缺預測，是把訂單、出貨、供應商前置時間與新聞等傳入信號，與正常營運時的預期模式相比較。偏離這些模式的情況，是[異常偵測](../../theory/paradigms/unsupervised/anomaly-detection/index.md)的一種形式。作業研究的文獻已對供應鏈在干擾下的情況建模（Snyder 等人，2015）。Ivanov（2020）提出可存續供應鏈模型，透過既定的機制調整網路結構。

## 關鍵方法

三個具代表性的方法涵蓋了主要的幾個階段。每個方法都有獨立的頁面。

| 方法 | 問題 | 核心想法 | 頁面 |
|---|---|---|---|
| DeepAR（Salinas 等人，2020） | 需求預測 | 在許多相關序列上訓練的一個自回歸 LSTM，輸出預測分布 | [DeepAR](deepar/index.md) |
| 注意力模型（Kool 等人，2018） | 車輛路徑規劃 | 以注意力為基礎的編碼器－解碼器，逐停靠地建構路線，以 REINFORCE 搭配貪婪展開基線訓練 | [注意力模型](attention-model-routing/index.md) |
| PRIMAL（Sartoretti 等人，2019） | 倉庫路徑規劃 | 以強化學習與模仿學習訓練的去中心化策略，依局部視野線上規劃 | [PRIMAL](primal/index.md) |

三者處理的是不同的決策。DeepAR 估計將來需要什麼，注意力模型決定車輛要拜訪哪些停靠點、以什麼順序，而 PRIMAL 則決定機器人如何在不碰撞的前提下移動。

## 相關連結

- **強化學習與規劃。**路線規劃與多機器人路徑規劃都是序列決策問題。[強化學習](../../theory/paradigms/reinforcement-learning/index.md)頁面涵蓋學習型路線規劃器所用的策略梯度方法。傳統的替代方案則是在問題的明確模型上進行搜尋，相關內容見[自動規劃](../../theory/symbolic-ai/planning/index.md)與 [A* 搜尋](../../theory/symbolic-ai/search/a-star/index.md)。
- **變動的資料。**需求會隨季節、趨勢與新產品而改變，這正是[串流與概念漂移](../../theory/paradigms/online/streaming-and-concept-drift/index.md)所處理的情境。
- **校準的不確定性。**預測區間與短缺警報只有在其宣稱的機率可靠時才有用，這個問題在[共形預測](../../theory/machine-learning/uncertainty-and-calibration/conformal-prediction/index.md)中討論。
- **機器人與模擬。**倉儲政策常在模擬器中訓練，部署到實體機器人時便產生[模擬到真實遷移](../../theory/paradigms/transfer/sim-to-real/index.md)的問題。
- **大腦與心智。**動物會利用周遭環境的內部地圖來規劃路線，見[空間導航與認知地圖](../../brain-mind/navigation-cognitive-maps/index.md)。在以學得的內部模型規劃，與依循學得的習慣行動之間如何取捨，則見[以模型為基礎與無模型控制](../../brain-mind/decision-reward/model-based-vs-model-free/index.md)。[預測編碼](../../brain-mind/predictive-coding/index.md)認為大腦持續預測其輸入，並以誤差修正預測；這與上面的預測迴圈只是粗略的類比。
- **相關應用。**[自動駕駛與運輸](../autonomous-driving/index.md)、[機器人](../robotics/index.md)與[製造與工業](../manufacturing/index.md)共用許多這些方法。
- **社會。**倉庫與運輸的自動化會影響就業，見[經濟與工作](../../society/economics/index.md)。貨運的排放則與[氣候與能源](../climate-energy/index.md)相關。

## 應用

- **零售需求。**零售商預測各品項的銷售量，以決定補貨數量。DeepAR 正是為這種情境設計的，其五個評估資料集中有兩個是 Amazon 品項的每週銷售資料（Salinas 等人，2020）。
- **最後一哩配送。**包裹與食品配送公司每天都在解決路線問題。OR-Tools 等開源求解器是常見的基準，學習型路線規劃器則與之比較（Kool 等人，2018）。
- **倉庫自動化。**行動機器人如今已在許多倉庫中搬運貨品。PRIMAL 的研究動機正是這種情境，並在工廠模型中以實體與模擬機器人進行了測試（Sartoretti 等人，2019）。
- **港口與貨運。**貨櫃碼頭的規劃涵蓋泊位、岸吊與堆場，並圍繞船舶與卡車的時程展開（Voß 等人，2004）。

## 開放問題

- **準確度與成本。**預測誤差低的模型，仍可能導致糟糕的庫存決策，而牛鞭效應顯示小誤差會如何沿上游放大。以成本衡量預測的價值，比衡量其誤差困難得多。
- **學習型啟發式方法與求解器。**學習型路線策略速度快，但它與強大求解器的差距會隨問題規模擴大；而時間窗、動態訂單與隨機需求等實際限制，也更難學習。
- **大規模的去中心化控制。**學習得到的機器人策略能很好地處理大片開放區域，但在密集、雜亂的佈局中表現不佳，這裡集中式規劃器仍較強。
- **第一階層以外的可見度。**企業往往看不清供應商的供應商，這限制了短缺預測可用的資料。
- **罕見事件。**歷史資料中的干擾很少，因此基準測試可能無法反映疫情或港口關閉等衝擊。

## 參考文獻

### 開創性論文

- Lee, H. L., Padmanabhan, V. & Whang, S. (1997). Information distortion in a supply chain: the bullwhip effect. *Management Science*. https://doi.org/10.1287/mnsc.43.4.546 — 分析訂單變異如何沿供應鏈上游放大，並指出造成失真的四個來源。
- Nazari, M. et al. (2018). Reinforcement learning for solving the vehicle routing problem. arXiv. https://arxiv.org/abs/1802.04240 — 以策略梯度訓練端到端策略來建構車輛路線，只使用獎勵信號與可行性規則。
- Salinas, D. et al. (2020). DeepAR: probabilistic forecasting with autoregressive recurrent networks. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2019.07.001 — 在許多相關序列上訓練一個循環模型，以輸出完整的預測分布，並在零售銷售資料上測試。
- Kool, W., van Hoof, H. & Welling, M. (2018). Attention, learn to solve routing problems! arXiv. https://arxiv.org/abs/1803.08475 — 以 REINFORCE 訓練的注意力模型，應用於旅行推銷員問題與數種車輛路徑變體。
- Sartoretti, G. et al. (2019). PRIMAL: Pathfinding via reinforcement and imitation multi-agent learning. *IEEE Robotics and Automation Letters*. https://doi.org/10.1109/lra.2019.2903261 — 結合強化學習與專家規劃器示範所訓練的去中心化多機器人路徑規劃策略。
- Lim, B. et al. (2019). Temporal fusion transformers for interpretable multi-horizon time series forecasting. arXiv. https://arxiv.org/abs/1912.09363 — 以 Transformer 為基礎的多期預測器，結合靜態共變量、已知的未來輸入與歷史序列。

### 綜述與教科書

- Psaraftis, H. N. (1995). Dynamic vehicle routing: status and prospects. *Annals of Operations Research*. https://doi.org/10.1007/bf02098286 — 較早的綜述，探討車輛在行駛途中才有新資訊到達的路線問題。
- Voß, S., Stahlbock, R. & Steenken, D. (2004). Container terminal operation and operations research - a classification and literature review. *OR Spectrum*. https://doi.org/10.1007/s00291-003-0157-z — 對貨櫃碼頭作業的規劃問題加以分類，並回顧所用的作業研究方法。
- Snyder, L. V. et al. (2015). OR/MS models for supply chain disruptions: a review. *IIE Transactions*. https://doi.org/10.1080/0740817x.2015.1067735 — 回顧以作業研究為基礎、用於應對供應鏈干擾風險的規劃模型。
- Petropoulos, F. et al. (2020). Forecasting: theory and practice. arXiv. https://arxiv.org/abs/2012.03854 — 對跨領域預測理論與實務的非系統性回顧，涵蓋從古典統計到機器學習的方法。
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2022). M5 accuracy competition: results, findings, and conclusions. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2021.11.013 — 報告階層式零售銷售預測基準測試的結果。

### 文章與文件

- Ivanov, D. (2020). Viable supply chain model: integrating agility, resilience and sustainability perspectives. *Annals of Operations Research*. https://doi.org/10.1007/s10479-020-03640-6 — 提出供應鏈的架構，使其能適應變化並吸收衝擊，撰寫於 COVID-19 疫情之後。

[^1]: 四個來源列於 Lee, Padmanabhan & Whang（1997）的摘要中，即「開創性論文」下的第一筆文獻。
