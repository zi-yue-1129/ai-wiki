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

- **糖尿病視網膜病變**：IDx-DR（2018）是第一個獲 FDA 授權的自主 AI 診斷系統——它在沒有臨床醫師閱讀影像的情況下，直接做出篩檢判斷（Abràmoff et al., 2018）
- **皮膚科**：CNN 在皮膚病變分類上與皮膚科醫師表現相當（Esteva et al., 2017）
- **乳房攝影**：在瑞典的大型隨機試驗（MASAI）中，AI 輔助閱片與標準雙人閱片相比，評估其安全性與篩檢準確度（Lång et al., 2023）
- **醫療 LLM**：Med-PaLM 在類似執照考試的題目上達到及格分數（Singhal et al., 2023）；考試表現並不等於臨床安全

## 慘痛的教訓

- **Epic 敗血症模型**：外部驗證發現，它漏掉了大部分的敗血症病例，卻產生大量警示（Wong et al., 2021, *JAMA Internal Medicine*）
- **捷徑學習**：COVID-19 胸部 X 光模型學到的是各醫院特有的假影；回顧研究發現，數百個已發表的模型幾乎沒有一個能用於臨床（Roberts et al., 2021）
- **偏見**：一套廣泛使用的演算法以醫療*花費*代替*需求*，導致黑人患者被少轉診（Obermeyer et al., 2019, *Science*）；脈搏血氧儀以及部分影像模型對深膚色族群的表現較差
- **IBM Watson for Oncology**：期望很高，但臨床採用有限

## 方法與資料

- 影像：CNN 與 ViT、在未標註掃描上的自監督預訓練、病理與放射學的基礎模型（例如 UNI、Virchow、Prov-GigaPath）
- 電子病歷：對就診紀錄做序列模型、對臨床筆記使用 LLM
- 多模態：結合影像、病歷筆記、檢驗數值與基因組資料
- 保護隱私的訓練：[聯邦式學習](../../theory/paradigms/federated/index.md)
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

## 關鍵方法

下列三種方法是上文多數系統的基礎。每一項都連結到解釋該方法的頁面。

- [ResNet](../../theory/models/cnn/backbones-and-scaling/resnet/index.md)：殘差卷積網路，是醫學影像分類器與偵測器常用的骨幹網路（He et al., 2016）。
- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md)：對 token 序列做自注意力（Vaswani et al., 2017）。上述臨床語言模型與基於 Transformer 的視覺編碼器都以它為基礎。
- [InstructGPT 與 RLHF](../../theory/models/llm/instructgpt-rlhf/index.md)：以人類偏好回饋做指令微調，讓預訓練語言模型變成能以對話回答的助手（Ouyang et al., 2022）。許多聊天式助手，包括用於患者溝通的助手，都以此方法為基礎。

## 參考文獻

### 開創性論文

- He, K. et al. (2016). Deep Residual Learning for Image Recognition. CVPR. https://doi.org/10.1109/CVPR.2016.90 — 殘差連接，使非常深的 CNN 能夠訓練。
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力為核心。
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT，以人類偏好回饋進行指令微調。
- Esteva, A. et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. *Nature*. https://doi.org/10.1038/nature21056 — 以皮膚科影像訓練的 CNN，並與皮膚科專科醫師比較。
- Abràmoff, M. D. et al. (2018). Pivotal trial of an autonomous AI-based diagnostic system for detection of diabetic retinopathy in primary care offices. *npj Digital Medicine*. https://doi.org/10.1038/s41746-018-0040-6 — IDx-DR 的關鍵性試驗，即上文描述的自主篩檢系統。
- Obermeyer, Z. et al. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*. https://doi.org/10.1126/science.aax2342 — 說明以醫療成本代替健康需求，如何使黑人患者處於不利地位。
- Wong, A. et al. (2021). External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. *JAMA Internal Medicine*. https://doi.org/10.1001/jamainternmed.2021.2626 — 對 Epic 敗血症模型的外部驗證，發現它漏掉了大多數敗血症病例。
- Roberts, M. et al. (2021). Common pitfalls and recommendations for using machine learning to detect and prognosticate for COVID-19 using chest radiographs and CT scans. *Nature Machine Intelligence*. https://doi.org/10.1038/s42256-021-00307-0 — 回顧已發表的 COVID-19 胸部影像模型，列出常見缺陷與建議。
- Lång, K. et al. (2023). Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. *The Lancet Oncology*. https://doi.org/10.1016/s1470-2045(23)00298-x — 隨機試驗，比較 AI 輔助閱片與標準雙人閱片。
- Singhal, K. et al. (2023). Large language models encode clinical knowledge. *Nature*. https://doi.org/10.1038/s41586-023-06291-2 — Med-PaLM，在類似醫師執照考試的題目上評估。
- Liu, X. et al. (2020). Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension. *Nature Medicine*. https://doi.org/10.1038/s41591-020-1034-x — CONSORT-AI，AI 介入試驗的報告檢核表。

### 綜述與教科書

- Rajpurkar, P. et al. (2022). AI in health and medicine. *Nature Medicine*. https://doi.org/10.1038/s41591-021-01614-0 — 回顧 AI 在臨床實務中的成效與尚未證實之處。

## 延伸學習

- [MONAI](https://monai.io/) — 開源的醫學影像模型訓練與部署框架。
