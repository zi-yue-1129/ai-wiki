---
translation_reviewed: 2026-10-28
---

# 主要模型目錄

依模型卡（model card）的格式列出多數讀者會接觸到的大型語言模型家族，並依廠商分組。每一列都提供發布月份、規模級別、開放程度與一行說明，並連結到支持該列的報告。來源無法查核的列已經刪去，本頁也不提供基準分數。

## 概述

下方的表格依家族分組：GPT、Claude、Gemini（含開放的 Gemma 系列）、Llama、Qwen、DeepSeek、Mistral，以及其他模型。每個家族各有一張表，因此可以先在家族內比較，再跨家族比較。

各欄的意義如下：

- **發布**是所引用報告首次張貼到 arXiv 的月份；Claude 模型則為廠商公告的發布日期。大多數情況下這與正式公開相差幾天，但兩者不一定是同一天。
- **規模級別**是所引用來源給出的參數量。若來源沒有給出數字，該格會註明。對混合專家（MoE）模型，會同時列出總參數與活躍參數，因為每個 token 實際使用的是活躍參數。
- **開放程度**說明來源對存取方式的描述，定義見下一節。
- **來源**連結到該列所用的報告或公告。

模型名稱變動很快，新版本經常出現。因此本表記錄的是所引用來源的說法，不宣稱完整。若要比較目前的模型，請參考即時的排行榜，並查看廠商自己的頁面以取得最新版本。[LLM 主題](../../theory/models/llm/index.zh-TW.md)的概述以大致相同的分組列出各家族。

## 核心概念

- **開放權重（Open weights）**：訓練後的參數可以下載並執行。授權條款仍可能限制商業使用，因此來源有說明時會寫出授權名稱。
- **完全開放（Fully open）**：權重與訓練資料、訓練與評估程式碼一併釋出。OLMo 報告作出這樣的區分，指出多數先前的釋出只分享權重與推論程式碼，而未分享訓練資料。[^1]
- **僅限託管（Hosted only）**：模型只能透過廠商的產品或 API 使用，所引用的來源沒有描述權重可以下載。
- **活躍參數（Active parameters）**：在混合專家模型中，每個 token 只由部分參數處理。因此模型總體可以很大，而每個 token 的成本卻較低，[詞彙表](../glossary/index.zh-TW.md)中的混合專家條目有相關說明。
- **技術報告、模型卡與系統卡**：廠商或實驗室隨模型發布的文件。技術報告通常提供架構與訓練細節，系統卡著重安全評估，模型卡則是摘要。若廠商沒有發布任何此類文件，則可能只有一份標註日期的公告可作來源。

## GPT（OpenAI）

| 模型 | 發布 | 規模級別 | 開放程度 | 說明 | 來源 |
|---|---|---|---|---|---|
| GPT-4 | 2023 年 3 月 | 未公開 | 封閉；報告未提供架構或規模 | 接受影像與文字輸入；報告表示不公開架構與訓練細節 | [arXiv:2303.08774](https://arxiv.org/abs/2303.08774) |
| GPT-4o | 2024 年 10 月 | 未說明 | 僅限託管（所述為 API 存取） | 以同一個網路處理文字、音訊、影像與影片輸入，並輸出文字、音訊與影像 | [arXiv:2410.21276](https://arxiv.org/abs/2410.21276) |
| gpt-oss-120b 與 gpt-oss-20b | 2025 年 8 月 | 總計 116.8B、活躍 5.1B；總計 20.9B、活躍 3.6B | 開放權重，Apache 2.0 | 兩個採用混合專家的開放權重推理模型 | [arXiv:2508.10925](https://arxiv.org/abs/2508.10925) |

較早的 GPT-3 模型記述於 [GPT-3 頁面](../../theory/models/llm/gpt-3-few-shot/index.zh-TW.md)。表中未列出它，因為無法從論文確認其權重的狀態。

## Claude（Anthropic）

| 模型 | 發布 | 規模級別 | 開放程度 | 說明 | 來源 |
|---|---|---|---|---|---|
| Claude 2 | 2023 年 7 月 | 未說明 | 僅限託管（API 與測試版網站） | 表現提升，回應較長 | [Anthropic](https://www.anthropic.com/news/claude-2) |
| Claude 3（Haiku、Sonnet、Opus） | 2024 年 3 月 | 三個層級；未說明規模 | 僅限託管（API） | 推出時 Opus 與 Sonnet 即可透過 API 使用 | [Anthropic](https://www.anthropic.com/news/claude-3-family) |
| Claude 3.5 Sonnet | 2024 年 6 月 | 未說明 | 僅限託管（API 與雲端平台） | 可透過 Anthropic API 及兩個雲端平台使用 | [Anthropic](https://www.anthropic.com/news/claude-3-5-sonnet) |
| Claude 3.7 Sonnet | 2025 年 2 月 | 未說明 | 僅限託管（API） | 延伸思考，API 使用者可設定思考預算 | [Anthropic](https://www.anthropic.com/news/claude-3-7-sonnet) |
| Claude Sonnet 4.5 | 2025 年 9 月 | 未說明 | 僅限託管（API） | 在 Claude API 中加入脈絡編輯與記憶工具 | [Anthropic](https://www.anthropic.com/news/claude-sonnet-4-5) |
| Claude Opus 4.5 | 2025 年 11 月 | 未說明 | 僅限託管（應用程式、API 與雲端平台） | 可在 Anthropic 的應用程式、API 及三大雲端平台使用 | [Anthropic](https://www.anthropic.com/news/claude-opus-4-5) |

Anthropic 對這些模型發布的是公告，而非 arXiv 技術報告，因此來源是公告頁面。這些頁面未提供參數量，且在所查核的來源中，這些模型都沒有開放權重。

## Gemini 與 Gemma（Google）

| 模型 | 發布 | 規模級別 | 開放程度 | 說明 | 來源 |
|---|---|---|---|---|---|
| Gemini 1.0 | 2023 年 12 月 | Ultra、Pro 與 Nano 三個層級 | 僅限託管（產品與 API） | 三個層級，從雲端推理到裝置端使用 | [arXiv:2312.11805](https://arxiv.org/abs/2312.11805) |
| Gemini 1.5 Pro 與 Flash | 2024 年 3 月 | 未說明 | 僅限託管（API） | 長脈絡，召回測試可達一千萬個 token | [arXiv:2403.05530](https://arxiv.org/abs/2403.05530) |
| Gemini 2.5 Pro 與 Flash | 2025 年 7 月 | 未說明 | 僅限託管（API） | Pro 是思考模型，可處理長達三小時的影片 | [arXiv:2507.06261](https://arxiv.org/abs/2507.06261) |
| Gemma | 2024 年 3 月 | 2B 與 7B | 開放權重 | 首個 Gemma 版本，以 Gemini 研究為基礎，附預訓練與調校後的檢查點 | [arXiv:2403.08295](https://arxiv.org/abs/2403.08295) |
| Gemma 2 | 2024 年 7 月 | 2B 至 27B | 開放權重 | 2B 與 9B 模型以知識蒸餾訓練 | [arXiv:2408.00118](https://arxiv.org/abs/2408.00118) |
| Gemma 3 | 2025 年 3 月 | 1B 至 27B | 開放權重 | 加入視覺理解，並支援至少 128K token 的脈絡 | [arXiv:2503.19786](https://arxiv.org/abs/2503.19786) |

## Llama（Meta）

| 模型 | 發布 | 規模級別 | 開放程度 | 說明 | 來源 |
|---|---|---|---|---|---|
| LLaMA | 2023 年 2 月 | 7B 至 65B | 釋出給研究社群 | 根據報告，僅以公開可得的資料集訓練 | [arXiv:2302.13971](https://arxiv.org/abs/2302.13971) |
| Llama 2 | 2023 年 7 月 | 7B 至 70B | 開放權重，自訂商業授權 | 基礎模型與針對對話調校的 Llama 2-Chat | [arXiv:2307.09288](https://arxiv.org/abs/2307.09288) |
| Llama 3 | 2024 年 7 月 | 最大為 405B 稠密模型 | 開放權重（405B 已公開釋出） | 一組支援多語言、程式、推理與工具使用的模型；多模態擴充未廣泛釋出 | [arXiv:2407.21783](https://arxiv.org/abs/2407.21783) |

## Qwen（阿里巴巴）

| 模型 | 發布 | 規模級別 | 開放程度 | 說明 | 來源 |
|---|---|---|---|---|---|
| Qwen | 2023 年 9 月 | 開源 7B 與 14B | 7B 與 14B 基礎模型及對話模型為開放權重 | 報告也涵蓋程式與數學變體 | [arXiv:2309.16609](https://arxiv.org/abs/2309.16609) |
| Qwen2 | 2024 年 7 月 | 0.5B 至 72B，稠密與 MoE | 開放權重（Hugging Face 與 ModelScope） | 包含經指令調校的變體 | [arXiv:2407.10671](https://arxiv.org/abs/2407.10671) |
| Qwen2.5 | 2024 年 12 月 | 最高 72B（開放旗艦） | 開放尺寸為開放權重；Turbo 與 Plus 僅限託管 | 預訓練規模擴大至 18 兆 token | [arXiv:2412.15115](https://arxiv.org/abs/2412.15115) |
| Qwen3 | 2025 年 5 月 | 0.6B 至 235B，稠密與 MoE | 開放權重，Apache 2.0 | 同一模型支援思考與非思考兩種模式 | [arXiv:2505.09388](https://arxiv.org/abs/2505.09388) |

## DeepSeek

| 模型 | 發布 | 規模級別 | 開放程度 | 說明 | 來源 |
|---|---|---|---|---|---|
| DeepSeek LLM | 2024 年 1 月 | 7B 與 67B | 開源 | 7B 與 67B 模型背後的規模法則研究，以 2 兆 token 訓練 | [arXiv:2401.02954](https://arxiv.org/abs/2401.02954) |
| DeepSeek-V2 | 2024 年 5 月 | 總計 236B、活躍 21B（MoE） | 開放權重（檢查點於 GitHub 提供） | 多頭潛在注意力與 DeepSeekMoE，降低訓練與推論成本 | [arXiv:2405.04434](https://arxiv.org/abs/2405.04434) |
| DeepSeek-V3 | 2024 年 12 月 | 總計 671B、活躍 37B（MoE） | 開放權重（檢查點於 GitHub 提供） | 以 14.8 兆 token 訓練，且未出現無法復原的損失尖峰 | [arXiv:2412.19437](https://arxiv.org/abs/2412.19437) |
| DeepSeek-R1 | 2025 年 1 月 | 以 V3 基礎模型為底；蒸餾模型從 1.5B 起 | 開放權重（報告所述為 MIT 授權） | 以強化學習訓練的推理模型；蒸餾模型為另一項釋出，見 [R1 蒸餾](../../theory/model-compression/knowledge-distillation/llm-distillation/deepseek-r1/index.zh-TW.md) | [arXiv:2501.12948](https://arxiv.org/abs/2501.12948) |

## Mistral AI

| 模型 | 發布 | 規模級別 | 開放程度 | 說明 | 來源 |
|---|---|---|---|---|---|
| Mistral 7B | 2023 年 10 月 | 7B | 開放權重，Apache 2.0 | 分組查詢注意力與滑動視窗注意力；另有指令調校變體 | [arXiv:2310.06825](https://arxiv.org/abs/2310.06825) |
| Mixtral 8x7B | 2024 年 1 月 | 總計 47B、活躍 13B（稀疏 MoE） | 開放權重，Apache 2.0 | 每層八個專家，每個 token 選用其中兩個 | [arXiv:2401.04088](https://arxiv.org/abs/2401.04088) |

Mistral 較後期的模型記錄在其自家的新聞頁面。撰寫本頁時的環境無法連上這些頁面，因此未列出。

## 其他模型

| 模型 | 發布 | 規模級別 | 開放程度 | 說明 | 來源 |
|---|---|---|---|---|---|
| BERT | 2018 年 10 月 | BASE 110M；LARGE 340M | 開放（釋出程式碼與預訓練模型） | 雙向編碼器，先預訓練再微調；見 [BERT](../../theory/models/transformer/architecture-families/bert/index.zh-TW.md) | [arXiv:1810.04805](https://arxiv.org/abs/1810.04805) |
| T5 | 2019 年 10 月 | 最大 11B | 開放（釋出程式碼、資料與預訓練模型） | 將每項任務都視為文字輸入、文字輸出；見 [T5](../../theory/models/transformer/architecture-families/t5/index.zh-TW.md) | [arXiv:1910.10683](https://arxiv.org/abs/1910.10683) |
| Falcon | 2023 年 11 月 | 7B、40B 與 180B | 開放權重，採寬鬆授權 | 以網頁資料訓練，並釋出網頁資料集的一部分 | [arXiv:2311.16867](https://arxiv.org/abs/2311.16867) |
| OLMo | 2024 年 2 月 | 1B 與 7B | 完全開放（權重、訓練資料、程式碼） | 與多數先前的開放釋出不同，同時公開訓練資料與程式碼 | [arXiv:2402.00838](https://arxiv.org/abs/2402.00838) |
| Kimi K2 | 2025 年 7 月 | 總計 1T、活躍 32B（MoE） | 開放權重（基礎與後訓練檢查點） | 以 MuonClip 優化器訓練的代理型模型 | [arXiv:2507.20534](https://arxiv.org/abs/2507.20534) |
| GLM-4.5 | 2025 年 8 月 | 總計 355B、活躍 32B（MoE）；Air 為 106B | 開源 | 混合推理，同時支援思考與直接回應模式 | [arXiv:2508.06471](https://arxiv.org/abs/2508.06471) |

## 關聯

上述語言模型建立在 [Transformer](../../theory/models/transformer/index.zh-TW.md) 之上，而 [規模法則](../../theory/models/llm/scaling-laws/index.zh-TW.md)頁面說明了其規模為何如此選擇。[知識蒸餾](../../theory/model-compression/knowledge-distillation/index.zh-TW.md)可以從較大的模型產生較小的模型，例如蒸餾版的 DeepSeek-R1。[開源資源調查](../../start/open-source-survey/index.zh-TW.md)介紹圍繞開放模型的工具與資源。這些報告發表的場域列於[會議與期刊](../venues/index.zh-TW.md)，預訓練所用的資料集列於[資料集](../datasets/index.zh-TW.md)，模型背後的實驗室則列於[人物與研究室](../people-and-labs/index.zh-TW.md)。

## 未解問題

- 當廠商不提供參數量時，如何公平比較不同家族的模型？
- 若只釋出權重，而未釋出資料與程式碼，是否應算作開放？還是應如 OLMo 一樣，三者都要公開才算？
- 混合專家模型應以總參數、活躍參數，還是單次請求的成本來比較？

## 參考資料

### 里程碑論文

- OpenAI (2023). *GPT-4 Technical Report*. arXiv. https://arxiv.org/abs/2303.08774 — 描述 GPT-4，並說明報告未提供架構、模型規模與訓練的進一步細節。
- OpenAI (2024). *GPT-4o System Card*. arXiv. https://arxiv.org/abs/2410.21276 — GPT-4o 的系統卡，涵蓋文字、音訊、影像與影片的全能模型，並附安全評估。
- OpenAI (2025). *gpt-oss-120b & gpt-oss-20b Model Card*. arXiv. https://arxiv.org/abs/2508.10925 — 兩個以 Apache 2.0 釋出的開放權重混合專家推理模型之模型卡。
- Gemini Team (2023). *Gemini: A Family of Highly Capable Multimodal Models*. arXiv. https://arxiv.org/abs/2312.11805 — 介紹 Ultra、Pro 與 Nano 三種 Gemini 模型，以及它們的部署方式。
- Gemini Team (2024). *Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context*. arXiv. https://arxiv.org/abs/2403.05530 — 描述 Gemini 1.5 Pro 與 Flash，以及其長脈絡召回能力，可達一千萬個 token。
- Gemini Team (2025). *Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities*. arXiv. https://arxiv.org/abs/2507.06261 — 涵蓋 Gemini 2.X 家族，包括 Gemini 2.5 Pro 與 Flash，以及先前的 2.0 模型。
- Gemma Team (2024). *Gemma: Open Models Based on Gemini Research and Technology*. arXiv. https://arxiv.org/abs/2403.08295 — 介紹首批 2B 與 7B 參數的 Gemma 模型，附預訓練與微調檢查點。
- Gemma Team (2024). *Gemma 2: Improving Open Language Models at a Practical Size*. arXiv. https://arxiv.org/abs/2408.00118 — 描述 2B 至 27B 參數的 Gemma 2，並以知識蒸餾訓練較小的模型。
- Gemma Team (2025). *Gemma 3 Technical Report*. arXiv. https://arxiv.org/abs/2503.19786 — 描述 1B 至 27B 參數的 Gemma 3，加入視覺理解與更長的脈絡。
- Touvron, H. et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. arXiv. https://arxiv.org/abs/2302.13971 — LLaMA 家族，參數從 7B 到 65B，以公開可得的資料集訓練。
- Touvron, H. et al. (2023). *Llama 2: Open Foundation and Fine-Tuned Chat Models*. arXiv. https://arxiv.org/abs/2307.09288 — 參數從 7B 到 70B 的 Llama 2，含對話模型與自訂商業授權。
- Grattafiori, A. et al. (2024). *The Llama 3 Herd of Models*. arXiv. https://arxiv.org/abs/2407.21783 — 描述 Llama 3 家族，其最大模型為 405B 參數的稠密 Transformer。
- Bai, J. et al. (2023). *Qwen Technical Report*. arXiv. https://arxiv.org/abs/2309.16609 — 介紹最早的 Qwen 模型，以及開源的 7B 與 14B 基礎版與對話版。
- Qwen Team (2024). *Qwen2 Technical Report*. arXiv. https://arxiv.org/abs/2407.10671 — 描述參數從 0.5B 到 72B 的 Qwen2 系列，權重釋出於 Hugging Face 與 ModelScope。
- Qwen Team (2024). *Qwen2.5 Technical Report*. arXiv. https://arxiv.org/abs/2412.15115 — 描述 Qwen2.5、其開放權重尺寸，以及託管的 Turbo 與 Plus 變體。
- Qwen Team (2025). *Qwen3 Technical Report*. arXiv. https://arxiv.org/abs/2505.09388 — 描述參數從 0.6B 到 235B 的 Qwen3 稠密與混合專家模型，以 Apache 2.0 釋出。
- DeepSeek-AI (2024). *DeepSeek LLM: Scaling Open-Source Language Models with Longtermism*. arXiv. https://arxiv.org/abs/2401.02954 — 開源 DeepSeek LLM（7B 與 67B 參數）背後的規模研究。
- DeepSeek-AI (2024). *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*. arXiv. https://arxiv.org/abs/2405.04434 — 描述一個 236B 參數、活躍 21B 的混合專家模型及其檢查點。
- DeepSeek-AI (2024). *DeepSeek-V3 Technical Report*. arXiv. https://arxiv.org/abs/2412.19437 — 描述一個 671B 參數、活躍 37B 的混合專家模型及其檢查點。
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv. https://arxiv.org/abs/2501.12948 — 描述以 DeepSeek-V3 基礎模型為底的推理模型，以及一併釋出的蒸餾模型。
- Jiang, A. Q. et al. (2023). *Mistral 7B*. arXiv. https://arxiv.org/abs/2310.06825 — 描述以 Apache 2.0 釋出的 7B Mistral 模型，採用分組查詢與滑動視窗注意力。
- Jiang, A. Q. et al. (2024). *Mixtral of Experts*. arXiv. https://arxiv.org/abs/2401.04088 — 描述總計 47B、活躍 13B 參數的稀疏混合專家模型。
- Devlin, J. et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv. https://arxiv.org/abs/1810.04805 — 介紹 BERT 編碼器，以雙向方式預訓練，並為語言理解任務微調。
- Raffel, C. et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. arXiv. https://arxiv.org/abs/1910.10683 — 介紹最大 11B 參數的文字到文字模型 T5，並釋出其預訓練模型與程式碼。
- Almazrouei, E. et al. (2023). *The Falcon Series of Open Language Models*. arXiv. https://arxiv.org/abs/2311.16867 — 描述 7B、40B 與 180B 參數的 Falcon 模型，以寬鬆授權釋出。
- Groeneveld, D. et al. (2024). *OLMo: Accelerating the Science of Language Models*. arXiv. https://arxiv.org/abs/2402.00838 — 描述 OLMo，與權重一併釋出訓練資料以及訓練與評估程式碼。
- Kimi Team (2025). *Kimi K2: Open Agentic Intelligence*. arXiv. https://arxiv.org/abs/2507.20534 — 描述一個總計一兆參數、活躍 32B 的混合專家模型及其釋出的檢查點。
- GLM-4.5 Team (2025). *GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models*. arXiv. https://arxiv.org/abs/2508.06471 — 描述開源的 355B 混合專家模型，以及 106B 的 GLM-4.5-Air 版本。

### 文章與文件

- Anthropic (2023). *Claude 2*. Anthropic news. https://www.anthropic.com/news/claude-2 — Claude 2 於 2023 年 7 月 11 日的公告，說明 API 與測試版網站的存取方式。
- Anthropic (2024). *Introducing the next generation of Claude*. Anthropic news. https://www.anthropic.com/news/claude-3-family — Claude 3 家族（Haiku、Sonnet 與 Opus）的公告，說明推出時即可透過 API 使用。
- Anthropic (2024). *Introducing Claude 3.5 Sonnet*. Anthropic news. https://www.anthropic.com/news/claude-3-5-sonnet — Claude 3.5 Sonnet 的公告，說明其可透過 API 與兩個雲端平台使用。
- Anthropic (2025). *Claude 3.7 Sonnet and Claude Code*. Anthropic news. https://www.anthropic.com/news/claude-3-7-sonnet — Claude 3.7 Sonnet 的公告，包含延伸思考，以及可透過 API 設定的思考預算。
- Anthropic (2025). *Introducing Claude Sonnet 4.5*. Anthropic news. https://www.anthropic.com/news/claude-sonnet-4-5 — Claude Sonnet 4.5 的公告，說明透過 Claude API 的使用方式。
- Anthropic (2025). *Introducing Claude Opus 4.5*. Anthropic news. https://www.anthropic.com/news/claude-opus-4-5 — Claude Opus 4.5 的公告，說明其可在應用程式、API 與三大雲端平台使用。

[^1]: Groeneveld et al. (2024), arXiv:2402.00838，摘要：多數先前的努力只釋出模型權重與推論程式碼，而 OLMo 另外釋出開放的訓練資料與訓練及評估程式碼。
