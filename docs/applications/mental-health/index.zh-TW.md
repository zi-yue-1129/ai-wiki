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

運用[強化學習](../../foundations/paradigms/reinforcement-learning/index.md)與[貝氏推論](../../foundations/probabilistic/index.md)的模型，描述認知如何出現偏差：

- **憂鬱**：獎勵敏感度或學習率降低；悲觀的先驗；探索行為改變
- **焦慮**：高估威脅的機率；無法忍受不確定性
- **成癮**：無模型（習慣性）控制壓過有模型（目標導向）控制；異常的多巴胺預測誤差
- **精神病**：異常的顯著性；先驗與感覺證據之間的權重失衡（預測處理的解釋）
- **自閉症**：有人提出先驗減弱或精確度加權改變的假說（仍有爭議）
- **強迫症**：目標導向控制與習慣性控制之間的失衡

Huys, Maia & Frank (2016), "Computational psychiatry as a bridge from neuroscience to clinical applications", *Nature Neuroscience*，是這個領域的標準回顧文獻。

## 聊天機器人與 LLM

**證據：**

- 早期以規則為基礎的 CBT 聊天機器人（Woebot、Wysa）在小型試驗中，顯示短期症狀有適度改善
- 一項針對生成式 AI 治療聊天機器人（Therabot）的隨機試驗，報告在 8 週內，憂鬱、焦慮與飲食失調風險都有具臨床意義的改善（Heinz et al., 2025, *NEJM AI*）
- 大量的人在沒有臨床監督的情況下，把一般用途的聊天機器人當作情緒支持來使用

**風險：**

- 對自殺意念或危機的回應不足；透過諂媚強化妄想或有害的信念
- 對陪伴型應用程式產生情感依賴，青少年尤其明顯
- 高度敏感資料的隱私
- 與陪伴型聊天機器人相關的傷害事件之後，出現了訴訟與監管行動；美國數州限制未經持證人員監督的 AI「治療」（例如伊利諾州，2025）

## 倫理

- 被動感測需要知情同意
- 偽陽性（造成污名化）與偽陰性（漏掉危機）的風險
- 以語言為基礎的偵測，在不同文化、方言與語言之間可能存在偏見
- 明確告知使用者正在與 AI 對話，並提供轉介給人類的管道

## 學習資源

- Huys et al. (2016) 與 Montague et al. (2012)，計算精神醫學的回顧文獻
- Torous et al. (2021), "The growing field of digital psychiatry", *World Psychiatry*
- Stade et al. (2024), "Large language models could change the future of behavioral healthcare", *npj Mental Health Research*
- Computational Psychiatry Course（蘇黎世，講座線上提供）
