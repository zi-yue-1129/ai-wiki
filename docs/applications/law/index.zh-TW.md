# 法律

本頁討論 AI **用於**法律實務的情形。關於規範 AI 的法律，請見[法律、政策與治理](../../society/governance/index.md)。

## 概況

| 領域 | 例子 |
|---|---|
| 法律研究 | 由 LLM 驅動、搜尋判例與法規的工具（Westlaw 與 Lexis 的 AI 功能、Harvey、CoCounsel） |
| 合約審閱與起草 | 條款擷取、風險標示、修訂標記、依範本進行的協商 |
| 電子證據開示（e-discovery） | 文件審閱中使用的技術輔助審閱（預測編碼） |
| 盡職調查 | 併購案中審閱數千份文件 |
| 司法近用 | 自助工具、表格填寫、白話的法律說明 |
| 法院 | 案件管理、逐字稿、翻譯；部分司法管轄區已發布法官使用 AI 的指引 |
| 法律預測 | 預測案件結果（準確性與倫理仍有爭議） |
| 法遵 | 追蹤法規變動、對應政策 |

## 幻覺問題

- 律師曾因提交由 AI 工具生成的虛構判例書狀而遭到制裁
- 在史丹佛的一項評估中，即使是專門的法律 RAG 工具，在相當比例的查詢中仍會產生幻覺（Magesh et al., 2024）
- 專業團體已就律師使用生成式 AI 時的能力、保密與查證發布指引

## 評測基準

- GPT-4 通過了美國統一律師考試（Katz et al., 2023）
- LegalBench：集體建構的法律推理任務基準（Guha et al., 2023）
- 律師考試對法律實務只是微弱的代理指標

## 高風險法律決策的風險

- **刑事司法中的風險評估**：COMPAS 工具被發現錯誤率存在種族差異（Chouldechova, 2017），這說明了各種公平性定義之間的取捨（見[倫理與公平](../../society/ethics/index.md)）
- **正當程序**：當事人有要求說明與提出異議的權利
- 上傳客戶文件時的**保密與特權**問題
- 面向消費者的法律 AI 所引發的**未經授權執業**問題

## 關鍵方法

下列三種方法與本頁最相關。每一項都連結到解釋該方法的頁面。

- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md)：支撐法律研究與起草工具的 LLM 所用架構（Vaswani et al., 2017）。
- [InstructGPT 與 RLHF](../../theory/models/llm/instructgpt-rlhf/index.md)：以人類回饋做指令微調，是多數法律助手產品的基礎（Ouyang et al., 2022）。
- [檢索增強生成](../../engineering/rag/index.md)：以檢索到的判例與法規為答案依據，可減少但無法完全消除幻覺（Magesh et al., 2024）。

## 參考文獻

### 開創性論文

- Magesh et al. (2024). Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools. arXiv. https://arxiv.org/abs/2405.20362 — 評估主要法律研究工具，發現許多查詢出現幻覺。
- Katz et al. (2023). GPT-4 Passes the Bar Exam. *SSRN*. https://doi.org/10.2139/ssrn.4389233 — 報告 GPT-4 在統一律師考試上的表現。
- Guha et al. (2023). LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models. arXiv. https://arxiv.org/abs/2308.11462 — 集體建構的法律推理任務基準。
- Chouldechova (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*. https://doi.org/10.1089/big.2016.0047 — 研究再犯風險工具，以及各種公平性定義之間的取捨。
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力為核心。
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT，以人類偏好回饋進行指令微調。

### 綜述與教科書

- Surden (2025). Artificial Intelligence and Law – An Overview of Recent Technological Changes in Large Language Models and Law. *SSRN*. https://doi.org/10.2139/ssrn.5135305 — 概述大型語言模型如何改變法律實務。
