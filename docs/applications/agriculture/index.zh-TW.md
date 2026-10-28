# 農業與食品

## 概況

| 領域 | 例子 |
|---|---|
| 作物監測 | 以衛星與無人機影像判斷作物種類與健康狀況（NDVI 及學習式指標）、產量預測 |
| 精準施作 | 「看到就噴」的除草系統，把除草劑精準噴在個別雜草上（例如 John Deere See & Spray）、變量施肥 |
| 病蟲害診斷 | 用於植物病害的手機影像分類器（PlantVillage）；病蟲害爆發預測 |
| 機器人 | 草莓與蘋果採收機器人、雷射除草、自動駕駛拖拉機 |
| 畜牧 | 以電腦視覺監測動物健康與行為、跛行偵測、精準餵養 |
| 育種與基因組學 | 基因組選拔、以影像進行表型分析、基因編輯標靶發現 |
| 灌溉與水資源 | 土壤濕度模型、蒸發散估算 |
| 供應鏈與食品 | 需求預測、食品安全檢測、減少浪費、替代蛋白質 |
| 諮詢服務 | 以當地語言提供給小農的 LLM 諮詢服務（例如 Farmer.CHAT、Digital Green） |

## 挑戰

- **變異性大**：天氣、土壤、作物品種與光線因田區而異——分布偏移是常態
- **標註資料稀缺**，對小農與熱帶農業系統尤其明顯
- 農村地區的**連線與成本**限制 → 需要邊緣模型
- **季節性**：每個地點每年只能做一次實驗
- 農民、設備製造商與平台之間的**資料所有權**

## 與氣候的連結

農業既容易受到氣候變遷的衝擊，也是主要的排放來源。AI 可支援乾旱早期預警、氣候韌性作物育種、甲烷監測與碳農法的查證（見[氣候與能源](../climate-energy/index.md)）。

## 關鍵方法

下列三種方法與本頁最相關。每一項都連結到解釋該方法的頁面。

- [ResNet](../../theory/models/cnn/backbones-and-scaling/resnet/index.md)：殘差 CNN，可從葉片與田間影像分類作物病害與雜草，如 PlantVillage 相關研究（He et al., 2016；Mohanty et al., 2016）。
- [主動學習](../../theory/paradigms/active/index.md)：標註稀少時，決定先標註哪些田間影像。
- [InstructGPT 與 RLHF](../../theory/models/llm/instructgpt-rlhf/index.md)：對話式助手背後的訓練方法，例如給農民的諮詢工具（Ouyang et al., 2022）。

## 參考文獻

### 開創性論文

- He, K. et al. (2016). Deep Residual Learning for Image Recognition. CVPR. https://doi.org/10.1109/CVPR.2016.90 — 殘差連接，使非常深的 CNN 能夠訓練。
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT，以人類偏好回饋進行指令微調。
- Hughes, Salathé (2015). An open access repository of images on plant health to enable the development of mobile disease diagnostics. arXiv. https://arxiv.org/abs/1511.08060 — PlantVillage 植物健康影像資料庫，是許多手機病害分類器的基礎。
- Mohanty, Hughes & Salathé (2016). Using Deep Learning for Image-Based Plant Disease Detection. *Frontiers in Plant Science*. https://doi.org/10.3389/fpls.2016.01419 — 在 PlantVillage 葉片影像上訓練 CNN，以分類作物病害。
- Chiu et al. (2020). Agriculture-Vision: A Large Aerial Image Database for Agricultural Pattern Analysis. CVPR. https://doi.org/10.1109/cvpr42600.2020.00290 — 用於農業圖樣分析的標註航拍影像資料集。

### 綜述與教科書

- Kamilaris & Prenafeta-Boldú (2018). Deep learning in agriculture: A survey. *Computers and Electronics in Agriculture*. https://doi.org/10.1016/j.compag.2018.02.016 — 綜述深度學習在作物與畜牧任務上的應用。
