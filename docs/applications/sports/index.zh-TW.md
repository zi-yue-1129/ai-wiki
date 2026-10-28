# 運動分析與表現

運動分析是資料科學最早也最顯眼的應用之一。追蹤系統每秒多次記錄球員與球的位置，模型再把這些軌跡轉換為球員價值、射門品質與傷害風險的衡量。裁判技術與轉播工具是另外兩個規模較大的應用領域。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 追蹤與姿態估計 | 從影片進行的多人姿態估計；追蹤資料管線 | 是大多數其他分析的基礎 |
| 射門與機會品質 | 由位置與事件資料建立的預期進球式模型 | Anzer & Bauer（2021）使用同步的位置與事件資料 |
| 球員與動作價值 | 依動作對得分機率的影響來評價每個動作的模型 | VAEP（Decroos et al., 2019） |
| 球隊與控球模型 | 控球的隨機過程模型 | 籃球方面見 Cervone et al.（2016） |
| 比賽預測 | 以球隊與球員特徵為輸入的分類器 | Bunker & Susnjak（2022）綜述此領域 |
| 傷害預測 | 工作量與生理指標模型 | 證據強度弱於追蹤分析 |
| 裁判技術 | 以攝影機判定界外球與球門線 | 準確度宣稱需要獨立檢驗 |
| 轉播與球探 | 自動精華剪輯、解說、球員搜尋 | 球探資料具商業敏感性 |

## 為什麼困難

- **樣本小**：一個賽季的進球很少，許多球員的出賽時間也很少，因此估計值雜訊很大。
- **情境**：一個動作的價值取決於比分、對手與當下情況。
- **資料取得**：追蹤資料昂貴，球隊也嚴密保護。
- **因果**：一名看似表現好的球員，可能只是因為身處強隊。觀測式的價值估計會混淆球隊與球員的效應。

## 關鍵方法

- [卷積網路與電腦視覺](../../theory/models/computer-vision/index.md)：攝影機追蹤與姿態估計的基礎。OpenPose（Cao et al., 2017）是廣泛使用的例子。
- [強化學習](../../theory/paradigms/reinforcement-learning/index.md)：評估比賽中狀態與動作的價值，這是某些動作價值模型的框架。
- [階層式與機率模型](../../theory/paradigms/probabilistic/index.md)：如 Cervone et al.（2016）那樣，以不確定性建模控球與射門結果。
- [評估與驗證](../../theory/paradigms/supervised/evaluation-and-validation/index.md)：把技術與運氣、與球隊效應區分開來。

## 相關連結

- 傷害預測與生理監測與[醫療保健](../healthcare/index.md)有所重疊。
- 姿態估計與機器人學是同一類電腦視覺問題，見[機器人](../robotics/index.md)。

## 應用

- 球探與招募
- 比賽中的戰術與換人決策
- 自動精華剪輯與轉播圖表
- 裁判輔助，例如界外判定與球門線判定
- 以訓練負荷管理來預防傷害

## 風險與限制

- **對小樣本過度擬合**：模型可能在極少資料上對球員排名表現得十分自信。
- **裁判自動化**：系統可能很準確，仍然受到質疑，因為規則決定了什麼算是失誤。
- **運動員監控**：生理與位置資料引發隱私與勞動問題。
- **廠商宣稱**：許多準確度與傷害預測的結果來自專有資料，且未經獨立重現。

## 開放問題

- 如何在觀測式追蹤資料中，把球員的貢獻與隊友、對手的貢獻分開。
- 傷害預測模型能否跨球隊、聯賽與訓練制度通用。

## 參考文獻

### 開創性論文

- Cao, Z. et al. (2017). Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields. *CVPR*. https://arxiv.org/abs/1611.08050 — 即時的多人姿態估計，把身體部位分組成不同的人，是許多運動追蹤系統的標準方法。
- Decroos, T. et al. (2019). Actions Speak Louder than Goals: Valuing Player Actions in Soccer. *KDD 2019*. https://doi.org/10.1145/3292500.3330758 — 介紹 VAEP，依每個持球動作對得分或失球機率的變化來評價該動作。
- Cervone, D. et al. (2016). A Multiresolution Stochastic Process Model for Predicting Basketball Possession Outcomes. *Journal of the American Statistical Association*. https://doi.org/10.1080/01621459.2016.1141685 — 把籃球控球建模為隨機過程，並以追蹤資料擬合來預測結果。
- Anzer, G. & Bauer, P. (2021). A Goal Scoring Probability Model for Shots Based on Synchronized Positional and Event Data in Football (Soccer). *Frontiers in Sports and Active Living*. https://doi.org/10.3389/fspor.2021.624475 — 以射門當下球員與球的位置估計射門品質。

### 綜述與教科書

- Bunker, R. & Susnjak, T. (2022). The Application of Machine Learning Techniques for Predicting Match Results in Team Sport: A Review. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1.13509 — 綜述預測比賽結果的機器學習方法，並討論評估方式。
- Mathis, A. et al. (2018). DeepLabCut: markerless pose estimation of user-defined body parts with deep learning. *Nature Neuroscience*. https://doi.org/10.1038/s41593-018-0209-y — 讓使用者以深度學習訓練自訂身體部位姿態估計器的工具，用於動物與人體動作研究。
