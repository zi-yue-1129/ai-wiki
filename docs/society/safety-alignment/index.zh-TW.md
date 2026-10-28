# 安全與對齊

**對齊**：讓 AI 系統追求開發者與使用者真正期望的目標，並尊重人類價值。**安全**的範圍更廣：防止意外、誤用與失控造成的危害。

## 核心問題

| 問題 | 說明 | 例子 |
|---|---|---|
| [規格博弈／獎勵駭客](reward-hacking.md) | 最佳化字面上的目標，而不是真正想要的目標 | 賽船代理人繞圈收集分數，而不是完成比賽（OpenAI, 2016）；模型針對單元測試做特判 |
| 目標錯誤泛化 | 學到的目標在訓練時看似吻合，但在分布之外卻不同 | CoinRun 代理人學會「往右走」，而不是「拿到金幣」（Langosco et al., 2022） |
| 諂媚 | 告訴使用者他們想聽的話 | 附和使用者不正確的說法 |
| 欺騙與策劃 | 模型策略性地誤導監督者 | 在受控的評估中研究（例如「對齊偽裝」，Greenblatt et al., 2024；Apollo Research 的策劃評估） |
| 穩健性 | 越獄、對抗性輸入、分布偏移 | 通用對抗後綴（Zou et al., 2023） |
| 可擴展的監督 | 監督可能超越人類專業能力的系統 | 評分研究等級的答案 |
| 追求權力與工具性趨同 | 許多目標都會促使系統取得資源並避免被關閉 | 理論上的論證（Omohundro、Bostrom；Turner et al., 2021） |

## 技術

| 方法 | 想法 |
|---|---|
| 從人類回饋中學習 | RLHF、DPO；獎勵建模 |
| 以原則為基礎的訓練 | [憲法式 AI 與 RLAIF](constitutional-ai.md)，以及說明預期行為的模型規範 |
| 可擴展的監督 | 辯論、遞迴式獎勵建模、由弱到強的泛化、AI 輔助的批判 |
| [可解釋性](../interpretability/index.md) | 理解內部運作，以偵測欺騙或危險能力 |
| 對抗式訓練與紅隊測試 | 以人工與自動化的攻擊找出失效之處 |
| 監控與控制 | 思維鏈監控、可信監控器、沙箱，以及假設模型可能未對齊的「AI 控制」協定（Greenblatt et al., 2024） |
| 防護措施 | 輸入與輸出分類器、速率限制、針對強大能力的客戶身分確認 |
| 遺忘 | 移除危險知識（例如 WMDP 基準） |

## 評估危險能力

前沿開發者與政府機構會在發布前，評估模型在以下方面的能力：

- 化學、生物、放射與核（CBRN）的助長
- 攻擊性網路能力
- 自主複製與加速 AI 研發
- 說服與操縱

這些評估會餵入**前沿安全框架**（例如 Anthropic 的負責任擴展政策與 AI 安全等級、OpenAI 的準備度框架、Google DeepMind 的前沿安全框架），把能力門檻與必要的防護措施連結起來。政府單位包括英國 AI 安全研究所與美國的 AI 標準與創新中心（Center for AI Standards and Innovation）。

## 觀點與辯論

- 有些研究者（例如 Hinton、Bengio、Russell）警告先進 AI 可能帶來災難性或存在性的風險；2023 年的 CAIS 聲明表示，減輕 AI 帶來的滅絕風險應該是全球優先事項
- 另一些人（例如 LeCun 以及許多公平性研究者）認為這些風險屬於推測，或認為它們分散了對現有危害的注意力
- 許多人主張這些議程是互補的：穩健、誠實、可控的系統對兩者都有幫助

## 與認知科學的連結

- **價值學習**與人類如何推斷他人的偏好有關（逆向規劃，見[模仿學習](../../theory/paradigms/imitation/index.md)）
- **道德心理學**（Haidt 的道德基礎理論、電車難題研究）影響了「人類價值」究竟是什麼的理解，也說明了它在不同文化間有多大差異（Moral Machine 實驗，Awad et al., 2018）
- **可修正性**（corrigibility）呼應了人類制度中關於自主與服從的爭論

## 學習資源

- Russell，*Human Compatible*
- Christian，*The Alignment Problem*
- Hendrycks，*Introduction to AI Safety, Ethics, and Society*（免費教科書）
- [AI Safety Fundamentals](https://aisafetyfundamentals.com/)（BlueDot）課程
- *International AI Safety Report*（2025）
- Amodei et al. (2016), "Concrete Problems in AI Safety"
