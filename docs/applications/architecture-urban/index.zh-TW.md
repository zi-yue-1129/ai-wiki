---
related:
- theory/models/computer-vision
- theory/models/gnn
- theory/paradigms/unsupervised/density-and-generative-models/generative-models
- applications/climate-energy
aliases:
  - 建築
  - 城市規劃
  - Urban Planning
---

# 建築、營造與城市規劃

建築與城市會產生大量感測、移動與設計資料，而且改變緩慢、代價高昂。AI 用於預測建築與城市的運作、檢查結構、探索設計方案，以及支援規劃決策。多數應用仍偏分析性質；生成式設計成長迅速，但實務上的檢驗仍較少。

## 概況

| 領域 | 方法 | 說明 |
|---|---|---|
| 建築能源預測 | 以電表與氣象資料為基礎的迴歸、神經網路等資料驅動模型 | 已發展多年；Zhao & Magoulès（2012）與 Wei 等人（2018）整理了相關方法 |
| 結構健康監測 | 對裂縫與損傷影像做影像分類與遷移學習；振動分析 | 從已標註的影像遷移，可降低標註成本（Gao & Mosalam, 2018） |
| 工地監控 | 以電腦視覺追蹤施工進度、安全與設備使用 | 攝影機覆蓋範圍與隱私限制了可使用的場所 |
| 城市移動與規劃 | 從行動與大眾運輸資料建立出行、交通與土地利用模型 | 城市運算把城市視為資料來源（Zheng 等人，2014） |
| 生成式與參數化設計 | 條件式影像轉換模型、最佳化，以及用於配置的生成模型 | 仍在早期；輸出需要結構與法規檢查 |
| 數位孿生 | 與感測器資料同步的模擬模型 | 資料整合是主要障礙 |

## 建築與城市為何困難

- **壽命長。** 建築設計一次、使用數十年，模型必須在用途改變後仍然可靠。
- **標籤稀少。** 失效很少見，檢查成本又高，因此監督式資料集很小。
- **在地條件。** 氣候、建材與建築法規因地區而異，容易造成分布偏移。
- **法規與責任。** 設計結果必須符合結構與安全規範，錯誤的責任由設計者、工程師與營造商共同分擔。

## 關鍵方法

有四類方法涵蓋該領域的大部分內容。每一項都連結到解說該方法的頁面。

- [電腦視覺](../../theory/models/computer-vision/index.md)：在照片中分類裂縫與損傷，並追蹤工地進度。
- [領域適應](../../theory/paradigms/transfer/domain-adaptation/index.md)：把在已標註結構上訓練的模型，用於新建築，這是 Gao & Mosalam（2018）的核心想法。
- [圖神經網路](../../theory/models/gnn/index.md)：把街道網路、交通路線與建築之間的互動建模成圖。
- [生成模型](../../theory/paradigms/unsupervised/density-and-generative-models/generative-models/index.md)：提出配置與立面方案；Isola 等人（2017）是成對影像轉換的開創性範例。

## 關聯

建築能源使用與[氣候與能源](../climate-energy/index.md)直接相關。城市運算的資料面與[隱私](../../society/privacy/index.md)重疊，因為移動與攝影機資料能識別個人。建築方法在檢查上與[製造與工業](../manufacturing/index.md)所用的方法相同。

## 應用

- 預測建築能源需求，支援控制與翻修決策。
- 地震或風災後自動篩選結構，優先安排人工檢查。
- 模擬城市出行與交通，測試新的大眾運輸路線或道路變更的影響。
- 生成式工具提出配置與立面方案，供建築師審閱。

## 開放問題

- 生成式設計的輸出，如何能自動、可靠地對照建築法規檢查？
- 在一種氣候或建築類型上訓練的能源模型，能在多大程度上轉移到另一種？
- 當模型輔助的設計或檢查出錯時，責任該由誰承擔？
- 如何在規劃中使用城市資料，又不暴露其中的人？

## 參考文獻

### 開創性論文

- Batty, M. (2018). Artificial intelligence and smart cities. *Environment and Planning B: Urban Analytics and City Science*. https://doi.org/10.1177/2399808317751169 — 主張 AI 正在改變城市的規劃與營運方式，以及這種改變對規劃者的要求。
- Zheng, Y., Capra, L., Wolfson, O. & Yang, H. (2014). Urban Computing: Concepts, Methodologies, and Applications. *ACM Transactions on Intelligent Systems and Technology*. https://doi.org/10.1145/2629592 — 把城市運算定義為利用城市尺度的資料，來理解並改善城市生活。
- Isola, P., Zhu, J.-Y., Zhou, T. & Efros, A. A. (2017). Image-to-Image Translation with Conditional Adversarial Networks. *CVPR 2017*. https://arxiv.org/abs/1611.07004 — 顯示條件式對抗網路能在成對影像之間轉換，包括從標籤圖到建築立面。

### 綜述與教科書

- Zhao, H.-x. & Magoulès, F. (2012). A review on the prediction of building energy consumption. *Renewable and Sustainable Energy Reviews*. https://doi.org/10.1016/j.rser.2012.02.049 — 回顧預測建築能耗的方法，從工程模型到資料驅動模型。
- Wei, Y., Zhang, X., Shi, Y., Xia, L., Pan, S., Wu, J., Han, M. & Zhao, X. (2018). A review of data-driven approaches for prediction and classification of building energy consumption. *Renewable and Sustainable Energy Reviews*. https://doi.org/10.1016/j.rser.2017.09.108 — 綜述建築能耗預測與分類的資料驅動方法，涵蓋方法與資料來源。

### 文章與文件

- Gao, Y. & Mosalam, K. M. (2018). Deep Transfer Learning for Image-Based Structural Damage Recognition. *Computer-Aided Civil and Infrastructure Engineering*. https://doi.org/10.1111/mice.12363 — 顯示從預訓練影像模型遷移學習，可減少辨識結構損傷所需的標註資料。
