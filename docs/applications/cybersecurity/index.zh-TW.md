# 資訊安全

AI 在資安領域是雙面刃：它強化防禦、賦能攻擊者，同時也創造了新的攻擊面。

## 用於防禦的 AI

| 領域 | 例子 |
|---|---|
| 威脅偵測 | 網路與端點遙測的異常偵測、惡意程式分類、釣魚偵測 |
| 資安營運（SOC） | 摘要警示、撰寫查詢、分流事件的 LLM 副駕駛 |
| 漏洞發現 | 機器學習引導的模糊測試；LLM 代理人在程式碼中搜尋真實漏洞 |
| 程式碼安全 | 以機器學習輔助的靜態分析、自動產生修補程式 |
| 身分與詐欺 | 行為生物辨識、帳號接管偵測 |
| 威脅情報 | 從報告中擷取入侵指標、將攻擊行動分群 |

## AI 助長的攻擊

- 大規模的**釣魚與社交工程**，能針對個人量身打造，並以任何語言流暢書寫
- 用於詐欺的**語音與影片深偽**，包括在視訊通話中冒充他人
- **惡意程式開發協助**，以及加速漏洞利用的開發
- **密碼猜測**與 CAPTCHA 破解

## 保護 AI 系統

| 威脅 | 說明 | 防禦 |
|---|---|---|
| 提示注入 | 隱藏在網頁、電子郵件或文件中的指令劫持 LLM 代理人 | 權限分離、把外部內容當作資料處理、敏感操作需人工確認、監控 |
| 越獄 | 繞過安全訓練的提示 | 對抗式訓練、分類器、多層防護 |
| 資料投毒 | 惡意的訓練資料可能植入後門（Carlini & Terzis, 2021） | 資料來源追溯、過濾、異常偵測 |
| 模型竊取 | 透過查詢竊取模型 | 速率限制、浮水印 |
| 訓練資料萃取 | 還原被記憶的私人資料 | 去重、差分隱私 |
| 對抗樣本 | 能騙過分類器的微擾 | 對抗式訓練、可證明的穩健性 |
| 供應鏈 | 惡意模型檔（pickle）、遭入侵的套件、被投毒的外掛或 MCP 伺服器 | 安全格式（safetensors）、簽章、沙箱 |

相關框架：[OWASP LLM 應用十大風險](https://genai.owasp.org/)、[MITRE ATLAS](https://atlas.mitre.org/)、NIST AI 100-2（對抗式機器學習分類法）。

## 關鍵方法

下列三種方法涵蓋上文多數防禦與攻擊面的重點。每一項都連結到解釋該方法的頁面。

- [異常偵測](../../theory/paradigms/unsupervised/anomaly-detection/index.md)：學習正常遙測資料並標出偏離的模型，用於入侵與詐欺偵測。
- [Transformer](../../theory/models/transformer/attention-is-all-you-need/index.md)：LLM 協作工具背後的架構，可摘要警示並撰寫查詢（Vaswani et al., 2017）。
- [代理人](../../theory/models/agents/index.md)：會呼叫工具的 LLM 代理人，而它們暴露於提示注入，是核心安全問題（Greshake et al., 2023）。

## 參考文獻

### 開創性論文

- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — 提出 Transformer，以多頭自注意力為核心。
- Greshake et al. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. arXiv. https://arxiv.org/abs/2302.12173 — 顯示隱藏在檢索內容中的指令，如何劫持整合 LLM 的應用。
- Carlini et al. (2020). Extracting Training Data from Large Language Models. arXiv. https://arxiv.org/abs/2012.07805 — 顯示語言模型可以重現被記住的訓練文字。
- Szegedy et al. (2013). Intriguing properties of neural networks. arXiv. https://arxiv.org/abs/1312.6199 — 提出對抗樣本：微小的輸入改動即可愚弄神經網路。
- Goodfellow, Shlens & Szegedy (2014). Explaining and Harnessing Adversarial Examples. arXiv. https://arxiv.org/abs/1412.6572 — 解釋對抗脆弱性，並提出快速梯度符號攻擊。
- Carlini & Terzis (2021). Poisoning and Backdooring Contrastive Learning. arXiv. https://arxiv.org/abs/2106.09667 — 顯示被投毒的訓練資料如何在對比式學習模型中植入後門。
- Vassilev et al. (2025). Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations. NIST AI 100-2e2025. https://doi.org/10.6028/nist.ai.100-2e2025 — NIST 對機器學習攻擊與緩解措施的分類。
