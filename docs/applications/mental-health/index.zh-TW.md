# 心理健康

## 概況

| 領域 | 例子 |
|---|---|
| 計算精神醫學 | 以形式化模型（強化學習、貝氏推論）描述症狀；把模型參數當作生物標記 |
| 數位表型 | 以智慧型手機感測器、打字、睡眠、移動與語音，作為情緒與復發的訊號 |
| 語言評估 | 從文字與語音中偵測憂鬱、自殺風險或精神病風險 |
| 對話式支持 | 提供認知行為療法（CBT）風格練習的聊天機器人；一般 LLM 被非正式地用於情緒支持 |
| 臨床人員輔助 | 會談摘要、治療師訓練模擬、以測量為基礎的照護 |
| 危機服務 | 訊息的分診與優先排序 |
| 神經影像與神經調節 | 預測治療反應；個人化經顱磁刺激（TMS）的刺激位置 |

## 計算精神醫學

運用[強化學習](../../theory/paradigms/reinforcement-learning/index.md)與[貝氏推論](../../theory/paradigms/probabilistic/index.md)的模型，描述認知如何出現偏差：

- **憂鬱**：獎勵敏感度或學習率降低；悲觀的先驗；探索行為改變
- **焦慮**：高估威脅的機率；無法忍受不確定性
- **成癮**：無模型（習慣性）控制壓過有模型（目標導向）控制；異常的多巴胺預測誤差
- **精神病**：異常的顯著性；先驗與感覺證據之間的權重失衡（預測處理的解釋）
- **自閉症**：有人提出先驗減弱或精確度加權改變的假說（仍有爭議）
- **強迫症**：目標導向控制與習慣性控制之間的失衡

Huys, Maia & Frank (2016), "Computational psychiatry as a bridge from neuroscience to clinical applications", *Nature Neuroscience*，是這個領域的標準回顧文獻。

## 聊天機器人與 LLM

**證據：**

- 一項針對規則式 CBT 聊天機器人 Woebot、以年輕成人為對象的隨機試驗，發現兩週內憂鬱與焦慮症狀減輕（Fitzpatrick et al., 2017）
- 大量的人在沒有臨床監督的情況下，把一般用途的聊天機器人當作情緒支持來使用

**風險：**

- 對自殺意念或危機的回應不足；透過諂媚強化妄想或有害的信念
- 對陪伴型應用程式產生情感依賴，青少年尤其明顯
- 高度敏感資料的隱私
- 關於 AI 作為治療工具的政策變化很快，各司法管轄區的規則不同

## 倫理

- 被動感測需要知情同意
- 偽陽性（造成污名化）與偽陰性（漏掉危機）的風險
- 以語言為基礎的偵測，在不同文化、方言與語言之間可能存在偏見
- 明確告知使用者正在與 AI 對話，並提供轉介給人類的管道

## 關鍵方法

下列三種方法與本頁最相關。每一項都連結到解釋該方法的頁面。

- [強化學習](../../theory/paradigms/reinforcement-learning/index.md)：描述學習與獎賞的模型，可解釋減少的獎賞敏感度等症狀（Huys et al., 2016）。
- [機率推論](../../theory/paradigms/probabilistic/index.md)：描述信念更新的貝氏模型，用於說明悲觀的先驗與對不確定性的不耐受（Huys et al., 2016）。
- [InstructGPT 與 RLHF](../../theory/models/llm/instructgpt-rlhf/index.md)：上文聊天式工具背後的訓練方法（Ouyang et al., 2022）。

## 參考文獻

### 開創性論文

- Fitzpatrick et al. (2017). Delivering Cognitive Behavior Therapy to Young Adults With Symptoms of Depression and Anxiety Using a Fully Automated Conversational Agent (Woebot). *JMIR Mental Health*. https://doi.org/10.2196/mental.7785 — 以規則式 CBT 聊天機器人進行、針對年輕成人的試驗。
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力為核心。
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT，以人類偏好回饋進行指令微調。

### 綜述與教科書

- Huys, Maia & Frank (2016). Computational psychiatry as a bridge from neuroscience to clinical applications. *Nature Neuroscience*. https://doi.org/10.1038/nn.4238 — 回顧計算模型如何連結神經科學與精神醫療實務。
- Torous et al. (2021). The growing field of digital psychiatry: current evidence and the future of apps, social media, chatbots, and virtual reality. *World Psychiatry*. https://doi.org/10.1002/wps.20883 — 回顧精神醫學數位工具（包括聊天機器人）的證據。
- Stade et al. (2024). Large language models could change the future of behavioral healthcare: a proposal for responsible development and evaluation. *npj Mental Health Research*. https://doi.org/10.1038/s44184-024-00056-z — 提出在行為健康照護中負責任地開發與評估 LLM 的建議。
