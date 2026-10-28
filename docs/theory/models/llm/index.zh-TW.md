---
translation_reviewed: 2026-10-28
---

# 大型語言模型

## 一句話說明

LLM 是在海量文字（以及程式碼與其他模態）上訓練、用來**預測下一個 token** 的超大型 Transformer；再經過指令微調與偏好對齊，成為能對話、寫作、推理、寫程式與使用工具的通用模型。

## 生命週期

```mermaid
flowchart LR
  A[資料蒐集與過濾<br/>數兆個 token] --> B[預訓練<br/>預測下一個 token]
  B --> C[中期訓練<br/>長脈絡、高品質、程式碼與數學]
  C --> D[監督式微調<br/>指令與對話]
  D --> E[偏好對齊<br/>RLHF / DPO / RLAIF]
  E --> F[推理強化學習<br/>可驗證的獎勵]
  F --> G[評估、紅隊測試、部署]
```

### 1. 分詞（Tokenisation）

文字會被切分成 token（BPE、SentencePiece、Unigram）。分詞器的設計會影響多語言的效率（一個中文字可能需要一個或多個 token），甚至影響算術能力。方法與其取捨見[分詞](tokenisation/index.md)。

### 2. 預訓練

目標：最小化 \(-\sum_t \log p_\theta(x_t\mid x_{<t})\)。

資料：經過過濾的網路爬取（Common Crawl）、書籍、論文、程式碼、多語言語料與合成資料。品質過濾與去重是主要的競爭優勢。

### 3. 後訓練

| 階段 | 方法 | 目的 |
|---|---|---|
| SFT | 在高品質的指令—回應配對上微調 | 遵循指令與對話格式（[模仿學習](../../paradigms/imitation/index.md)） |
| RLHF | 人類比較回答 → 獎勵模型 → PPO | 更有幫助、誠實、無害 |
| DPO 及其變體 | 直接在偏好配對上最佳化，不需獨立的獎勵模型 | 更簡單、更穩定 |
| RLAIF／憲法式 AI | 由依據成文原則的 AI 回饋引導 | 擴大監督規模 |
| 可驗證獎勵的強化學習（RLVR） | 自動評分（數學答案、單元測試） | 訓練推理能力 |

## 能力與現象

- **上下文學習**：從提示中的少量範例學會一項任務（GPT-3）
- **思維鏈**：逐步推理大幅提升數學與邏輯表現（Wei et al., 2022）
- **縮放與湧現**：隨著模型、資料與運算量增加，損失可預測地下降，但某些能力似乎突然出現；這些跳躍是否真實仍有爭議。見[縮放定律與湧現能力](scaling-laws/index.md)
- **推理模型**：經強化學習訓練，在回答前產生很長的推理過程（OpenAI o 系列、DeepSeek-R1、Claude 的延伸思考、Gemini 的思考模型等）；在競賽數學、程式設計與科學問題上大幅進步（方法見[推理模型與測試時運算](../reasoning/index.md)）
- **工具使用**：搜尋、程式執行、API——見 [AI 代理人](../agents/index.md)
- **長脈絡**：從 2K token 發展到百萬 token 等級
- **多模態**：見[多模態模型](../multimodal/index.md)

## 已知限制

| 問題 | 說明 | 緩解方式 |
|---|---|---|
| 幻覺 | 以肯定語氣輸出錯誤內容 | RAG、引用、校準、訓練模型學會拒答 |
| 知識截止 | 訓練資料在某個日期就結束 | 搜尋工具、RAG |
| 脆弱的推理 | 細微的改寫就可能讓解法失效 | 推理訓練、工具、驗證器 |
| 諂媚 | 傾向附和使用者 | 對齊訓練、評估 |
| 提示注入 | 外部內容中隱藏的指令劫持模型 | 權限分離、輸入標記、監控 |
| 偏見 | 訓練資料帶來的社會偏見 | 資料策展、評估、對齊 |
| 成本與延遲 | 大模型執行成本高 | 蒸餾、量化、MoE、推測解碼 |

## 模型生態系（2026 年概觀）

!!! note "變化快速"
    此處只列出模型家族。目前的版本請查閱官方網站，以及 [LMArena](https://lmarena.ai/) 與 [Artificial Analysis](https://artificialanalysis.ai/) 等排行榜。

| 類型 | 家族（例子） |
|---|---|
| 封閉的前沿模型 | OpenAI GPT、Anthropic Claude、Google Gemini、xAI Grok |
| 開放權重模型 | Meta Llama、阿里巴巴 Qwen、DeepSeek、Mistral、Google Gemma、Microsoft Phi、月之暗面 Kimi、智譜 GLM、OpenAI gpt-oss |
| 地區性／主權模型 | 許多國家資助針對在地語言與文化調校的模型（例如台灣的 TAIDE，以及聯發科針對繁體中文的 Breeze） |

## LLM 與人類語言認知

- **LLM 能預測語言區的腦活動**：預測下一個詞越準的模型，也越能預測人類語言網路的反應（Schrimpf et al., 2021, *PNAS*）
- **形式語言能力與功能語言能力**：Mahowald、Fedorenko 等人（2024）主張，LLM 掌握了形式能力（文法），但功能能力（推理、世界知識、社會認知）——由語言網路以外的腦網路支持——仍較不可靠
- **資料效率**：兒童到青少年時聽到的詞數約在數千萬量級（遠低於一億）；LLM 則看過數兆 token。BabyLM 挑戰研究的是在兒童規模資料上的學習
- **心智理論測試**：LLM 通過許多錯誤信念任務，但對微擾很敏感；它們是否「具有」心智理論仍有爭議（Kosinski, 2023 對 Ullman, 2023；Strachan et al., 2024）
- 見[心理學與 AI](../../../brain-mind/psychology/index.md)與 [NeuroAI](../../../brain-mind/neuroai/index.md)

## 關鍵方法

每個方法各有專頁，此處的概述與比較從簡。

### GPT-3：從提示中進行少樣本學習（Brown 等人，2020）

- **概述：** 一個 1,750 億參數的自回歸 Transformer，以提示中的零、一或少數範例進行測試。
- **比較：** 展示單靠規模與提示能達到的效果。下方的 InstructGPT 則加入人類回饋來改變行為。
- **完整內容：** [GPT-3 少樣本學習](gpt-3-few-shot/index.md)

### 運算最佳化訓練（Hoffmann 等人，2022）

- **概述：** 在固定的運算預算下，透過跨多次訓練的擬合，找出最佳的模型大小與訓練 token 數。
- **比較：** 修正了 GPT-3 只重規模的看法，把模型大小與訓練資料量綁在一起考慮。
- **完整內容：** [運算最佳化訓練](compute-optimal-training/index.md)

### InstructGPT：從人類回饋中進行強化學習（Ouyang 等人，2022）

- **概述：** 分三個階段微調 GPT-3：示範資料的監督學習、獎勵模型，以及以該獎勵模型為標的的強化學習。
- **比較：** 在 GPT-3 頁描述的基礎模型上加入人類偏好。強化學習的演算法見強化學習相關頁面。
- **完整內容：** [InstructGPT 與 RLHF](instructgpt-rlhf/index.md)

## 學習資源

- [mlabonne/llm-course](https://github.com/mlabonne/llm-course)
- Raschka，*Build a Large Language Model (From Scratch)*
- Stanford CS336，*Language Modeling from Scratch*
- Hugging Face [LLM Course](https://huggingface.co/learn/llm-course)
- Karpathy，"Intro to Large Language Models" 與 "Deep Dive into LLMs like ChatGPT"

## 參考文獻

### 開創性論文

- Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — GPT-3 論文，顯示非常大的模型能從提示中給出的少量範例學會新任務。
- Kaplan, J., et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — 顯示隨著模型大小、資料與運算量增加，損失如何可預測地下降。
- Hoffmann, J., et al. (2022). *Training Compute-Optimal Large Language Models*. arXiv. https://arxiv.org/abs/2203.15556 — Chinchilla 研究，主張在固定運算預算下，模型大小與訓練 token 數應該同步成長。
- Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. arXiv. https://arxiv.org/abs/2203.02155 — InstructGPT，結合監督式微調與來自人類偏好的強化學習。
- Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — 顯示要求模型寫出中間推理步驟，可改善多步驟問題的解題能力。

### 綜述與教科書

- Zhao, W. X., et al. (2023). *A Survey of Large Language Models*. arXiv. https://arxiv.org/abs/2303.18223 — 對 LLM 的預訓練、適應與評估進行廣泛綜述，並附有模型時間線。

### 講座與影片

- Karpathy, A. (2023). *[1hr Talk] Intro to Large Language Models*. YouTube. https://www.youtube.com/watch?v=zjkBMFhNj_g — 一小時、非技術性的概述，介紹 LLM 如何訓練、能做什麼、在哪裡失敗。

### 文章與文件

- Hugging Face. *LLM Course*. https://huggingface.co/learn/llm-course — 使用 Hugging Face 函式庫來使用、微調與建構 LLM 的實作課程。
