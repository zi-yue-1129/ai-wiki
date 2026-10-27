# 醫療保健

## 概況

| 領域 | 例子 | 成熟度 |
|---|---|---|
| 醫學影像 | 放射科的偵測與分診（胸部 X 光、CT、乳房攝影）、病理切片、皮膚科、眼科（糖尿病視網膜病變） | 最成熟；獲監管機構核准的 AI 醫材多數屬於此類 |
| 臨床文件 | 環境式 AI 紀錄員（聆聽診間對話並草擬病歷）、病歷摘要 | 2023 年起快速普及 |
| 臨床決策支援 | 敗血症與病情惡化警示、風險評分、藥物交互作用檢查、以 LLM 進行鑑別診斷 | 證據參差；已有多起受矚目的失敗案例 |
| 病患溝通 | 草擬回覆病患訊息、分診聊天機器人、衛教材料 | 成長中 |
| 營運 | 排程、病床管理、編碼與計費、事前授權 | 普遍，但較不顯眼 |
| 訊號與穿戴裝置 | 心電圖心律不整偵測、智慧手錶的心房顫動偵測、連續血糖監測 | 在特定用途上已成熟 |
| 基因組學與精準醫療 | 變異解讀、多基因風險、癌症分型 | 見 [生命科學](../life-science/index.md) |
| 手術與機器人 | 手術影片分析、技術評估、自動縫合研究 | 早期 |

## 具代表性的成果

- **糖尿病視網膜病變**：IDx-DR（2018）是第一個獲 FDA 授權的自主 AI 診斷系統——它在沒有臨床醫師閱讀影像的情況下，直接做出篩檢判斷
- **皮膚科**：CNN 在皮膚病變分類上與皮膚科醫師表現相當（Esteva et al., 2017）
- **乳房攝影**：在瑞典的大型隨機試驗（MASAI）中，AI 輔助篩檢找出更多癌症，同時減少約 44% 的放射科醫師工作量（Lång et al., 2023；2025）
- **醫療 LLM**：Med-PaLM 2 及之後的通用前沿模型，在類似執照考試的題目上都已超過及格分數；考試表現並不等於臨床安全
- **監管數量**：FDA 公開列出的 AI 醫材在 2025 年已超過 1,000 項，約四分之三屬於放射科

## 慘痛的教訓

- **Epic 敗血症模型**：外部驗證發現，它漏掉了大部分的敗血症病例，卻產生大量警示（Wong et al., 2021, *JAMA Internal Medicine*）
- **捷徑學習**：COVID-19 胸部 X 光模型學到的是各醫院特有的假影；回顧研究發現，數百個已發表的模型幾乎沒有一個能用於臨床（Roberts et al., 2021）
- **偏見**：一套廣泛使用的演算法以醫療*花費*代替*需求*，導致黑人患者被少轉診（Obermeyer et al., 2019, *Science*）；脈搏血氧儀以及部分影像模型對深膚色族群的表現較差
- **IBM Watson for Oncology**：期望很高，但臨床採用有限

## 方法與資料

- 影像：CNN 與 ViT、在未標註掃描上的自監督預訓練、病理與放射學的基礎模型（例如 UNI、Virchow、Prov-GigaPath）
- 電子病歷：對就診紀錄做序列模型、對臨床筆記使用 LLM
- 多模態：結合影像、病歷筆記、檢驗數值與基因組資料
- 保護隱私的訓練：[聯邦式學習](../../foundations/paradigms/federated/index.md)
- 資料集：MIMIC（加護病房紀錄）、CheXpert 與 MIMIC-CXR、UK Biobank、The Cancer Genome Atlas、PhysioNet

## 真正重要的評估方式

1. 在其他醫院與族群上做**外部驗證**
2. **前瞻性與隨機化試驗**，而不只是回顧性的 AUC
3. **校準度**與各子群體的表現
4. **臨床效用**：它是否改變了決策與結果？
5. **人機協作**：有 AI 的臨床醫師、只有臨床醫師、只有 AI 三者的比較——兩者結合不一定最好
6. 報告規範：TRIPOD+AI、CONSORT-AI、SPIRIT-AI、DECIDE-AI、CLAIM

## 法規

- **美國 FDA**：將軟體視為醫療器材（SaMD）；預定變更管理計畫讓已核准的模型可以更新
- **歐盟**：醫療器材法規（MDR）加上 AI 法（多數醫療 AI 屬於「高風險」）
- 臨床責任通常仍由臨床醫師承擔；AI 錯誤的法律責任仍未定論

## 學習資源

- Topol，《Deep Medicine》
- Rajpurkar et al. (2022), "AI in health and medicine", *Nature Medicine*
- [FDA 的 AI 醫療器材清單](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices)
- Stanford AIMI、MIT Clinical ML 研究團隊的發表
- [MONAI](https://monai.io/)（開放的醫學影像框架）
