---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
  - theory/paradigms/federated
  - society/governance
tags:
  - privacy
  - data protection
aliases:
  - Privacy
  - 資料保護
  - 個人資料保護
---

# 隱私與資料保護

AI 系統從關於人的資訊中學習，而且有時會把這些資訊再次洩露出來。隱私的研究要回答三個問題：哪些資料可以被收集與使用、訓練完成的模型可能洩露哪些訓練資料，以及有哪些法律與技術上的保護措施能讓個人維持控制權。

## 概述

現代模型是在極大量的文字、影像與行為紀錄上訓練的，其中很多資料是從網路上收集的，描述的人事先並不知情。隱私問題會在三個地方出現：資料被**收集並用於訓練**時、**訓練完成的模型洩露**所學內容時，以及部署的系統從一般輸入**推論出敏感資訊**時。因此，AI 隱私的討論同時涉及資料治理的問題，以及模型記住了什麼的技術問題。更廣的倫理脈絡請見[倫理與公平](../ethics/index.md)。

## 關鍵概念

- **個人資料**：與已識別或可識別之人相關的任何資訊，包括推論出來而非直接收集的資料。
- **記憶化（memorisation）**：模型重現特定的訓練樣本，有時逐字重現，而不只是學到一般的模式。
- **成員推論（membership inference）**：判斷某筆紀錄是否在模型的訓練集中。
- **屬性推論（attribute inference）**：從未說明此事的資料中，預測健康狀況、政治立場等敏感屬性。
- **差分隱私（differential privacy）**：一種形式化的保證，表示任何單一個人的資料都不會明顯改變輸出的分布。參見[聯邦與隱私保護學習](../../theory/paradigms/federated/index.md)。
- **資料最小化與目的限制**：法律原則，要求資料只能用於既定目的，且保存時間不超過必要。

## 運作方式

大部分的資訊洩露可以由三種機制解釋。

1. **記憶化。** 大型模型可以儲存罕見或重複出現的序列。Carlini 等人（2021）展示了可以透過從語言模型取樣，還原出訓練文字（見[關鍵方法](#關鍵方法)）。重複出現的資料更容易被記住，因此在訓練前去除重複能降低風險。
2. **成員推論。** 模型對訓練過的樣本通常會更有把握。能夠查詢模型的攻擊者可以利用這個差距，把成員與非成員區分開來。
3. **從看似無害的資料推論。** 在公開資料上訓練的模型，可以從相關訊號（例如寫作風格、購買紀錄或位置）推測私人特質。這是學習本身的特性，而不是程式錯誤，因此只限制資料的存取權限無法完全解決問題。

**遺忘學習（unlearning）**，即在訓練後從模型中移除某人的資料，相當困難。重新訓練的成本很高，而近似的方法提供的保證較弱，也難以驗證。

## 關鍵方法

每個方法都有自己的頁面，說明問題、方法、結果與限制。下表做簡要比較。

| 方法 | 所問的問題 | 主要結果（依摘要） | 延伸閱讀 |
|---|---|---|---|
| 差分隱私（Dwork 等人，2006） | 發布的結果如何對任何單一個人不敏感？ | 形式化的保證與雜訊校準方法，而非實證的基準測試 | [差分隱私](differential-privacy.zh-TW.md) |
| 成員推論（Shokri 等人，2017） | 攻擊者能否判斷某筆紀錄是否在訓練集中？ | 商業機器學習服務所提供的模型可能受到攻擊 | [成員推論](membership-inference.zh-TW.md) |
| 訓練資料萃取（Carlini 等人，2021） | 能否還原語言模型的訓練文字？ | 從 GPT-2 萃取出數百段逐字的序列 | [訓練資料萃取](training-data-extraction.zh-TW.md) |

## 保護技術

| 技術 | 保護的對象 | 取捨 |
|---|---|---|
| 去除重複與過濾 | 避免重複或敏感的字串進入訓練 | 偵測不完美，可能移除有用的資料 |
| 訓練時的差分隱私（DP-SGD） | 限制單一樣本的影響 | 準確度較低，訓練較慢 |
| 聯邦學習 | 把原始資料留在使用者裝置上 | 共享的更新仍可能洩露資訊；見[聯邦學習](../../theory/paradigms/federated/index.md) |
| 存取控制與資料最小化 | 限制誰能看到資料，以及保留多少資料 | 可用於學習的資料減少 |
| 機器遺忘（machine unlearning） | 在訓練後移除某人的影響 | 難以驗證，通常只是近似 |

## 法律與規範

- **GDPR**：歐盟第 2016/679 號規則（Regulation (EU) 2016/679），2016 年 4 月 27 日通過，賦予個人存取與刪除資料的權利，並要求處理個人資料須有合法依據。訓練完成的模型本身是否屬於個人資料，目前仍有爭議。
- **歐盟 AI 法（AI Act）**：第 2024/1689 號規則（Regulation (EU) 2024/1689），日期為 2024 年 6 月 13 日，採取風險分級的做法，並限制部分生物辨識的用途。它與資料保護法並行適用，而非取代後者。
- 其他司法管轄區採取不同的做法。各國與國際的努力請見[法律、政策與治理](../governance/index.md)。

## 與其他主題的連結

- 隱私是[倫理與公平](../ethics/index.md)中共通的原則之一，該頁主要將其視為價值判斷的問題。
- 神經資料與大腦資料是最敏感的個人資料之一。[腦機介面](../../brain-mind/bci/index.md)可能記錄出揭示意圖或健康狀況的訊號，以新的形式帶出相同的問題。
- 隱私保護學習的技術面，詳見[聯邦與隱私保護學習](../../theory/paradigms/federated/index.md)。

## 應用

- **健康紀錄**：臨床模型在資料離開醫院前，需要存取控制與去識別化。
- **官方統計與分析**：統計機構與大型科技公司以差分隱私發布彙總數據。
- **裝置端處理**：鍵盤與語音助理越來越多在本地執行模型，原始輸入不會離開裝置。

## 開放問題

- 訓練完成的模型在法律意義上是否包含個人資料？如果是，該如何將其刪除？
- 隨著模型與訓練資料集變大，如何可靠地衡量記憶化的程度？
- 差分隱私對小群體的準確度影響最大，應如何權衡隱私與公平？
- 網路爬取資料用於訓練，屬於同意、正當利益，還是兩者都不是？

## 參考資料

### 開創性論文

- Dwork, C., McSherry, F., Nissim, K. & Smith, A. (2006). Calibrating noise to sensitivity in private data analysis. *Theory of Cryptography Conference (TCC)*. https://doi.org/10.1007/11681878_14 — 提出差分隱私與領域廣泛使用的雜訊校準框架。
- Shokri, R., Stronati, M., Song, C. & Shmatikov, V. (2017). Membership inference attacks against machine learning models. *IEEE Symposium on Security and Privacy*. https://arxiv.org/abs/1610.05820 — 顯示黑箱查詢即可揭露訓練集成員身分，包括對商業機器學習服務的攻擊。
- Carlini, N. et al. (2021). Extracting training data from large language models. *USENIX Security Symposium*. https://arxiv.org/abs/2012.07805 — 示範從 GPT-2 萃取出逐字的訓練序列。
- Abadi, M. et al. (2016). Deep learning with differential privacy. *ACM CCS*. https://arxiv.org/abs/1607.00133 — DP-SGD，在訓練時對梯度進行裁剪並加入雜訊。

### 綜述與教科書

- Dwork, C. & Roth, A. (2014). *The Algorithmic Foundations of Differential Privacy*. Foundations and Trends in Theoretical Computer Science, 9(3–4). https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf — 差分隱私的標準教科書，完整收錄機制與證明。

### 文章與官方文件

- EUR-Lex. *Regulation (EU) 2016/679 (General Data Protection Regulation)*. https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng — GDPR 的官方條文，是歐洲個人資料保護的主要法律。
- EUR-Lex. *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng — 歐盟 AI 法的官方條文，包含風險分級的規定。
