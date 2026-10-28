---
translation_reviewed: 2026-10-28
---

# 資料投毒與後門

資料投毒是蓄意破壞訓練資料，使模型學到開發者並未想要的行為。後門則是一種被植入的行為，平時隱藏不顯，直到輸入中出現特定的觸發條件才會現身。

## 概述

模型的可信度取決於它的訓練資料，而大型模型所學的資料，往往是開發者既未蒐集也未檢查的。只要有人能發布一個網頁、或提供一個回饋標籤，就能影響模型學到什麼，而他根本不需要接觸模型本身。早期對影像分類器的研究顯示，被投毒的訓練資料可以植入一個觸發條件，使輸出被改變，而開發者自己的驗證資料上準確率仍然很高（Gu 等人，2017）。語言模型面臨的風險相同，規模更大，因為它們訓練於未經篩選的網路文字，之後又以來自許多人的資料進行調整。

## 關鍵概念

- **投毒（poisoning）**：新增、修改或刪除訓練樣本，使訓練後的模型在某些情境下表現失常。
- **後門（backdoor）**：一種只有在觸發條件存在時才會出現的隱藏行為。也稱為木馬（trojan）。
- **觸發條件（trigger）**：啟動後門的特徵，例如一個罕見的詞組或影像上的一塊圖案。
- **乾淨標籤投毒（clean-label poisoning）**：被投毒的樣本帶有正確的標籤，因此檢查標籤時看不出問題（Shafahi 等人，2018）。
- **潛伏代理人（sleeper agent）**：一種條件式後門在安全訓練之後仍然存續的模型（Hubinger 等人，2024）。

## 運作方式

投毒分為兩個步驟：把被投毒的內容放進某個資料來源，然後等待開發者用它來訓練。第二步通常不需要攻擊者介入，因為流程會自動蒐集資料。

```mermaid
flowchart LR
  A[攻擊者發布或修改資料] --> S[資料來源：網路爬取、資料集、回饋]
  S --> T[訓練或微調]
  T --> M[帶有隱藏後門的模型]
  M --> U[包含觸發條件的輸入]
  U --> B[攻擊者指定的行為]
```

最簡單的例子是 Wallace 等人（2020）的研究：他們在情緒分類的訓練集中加入 50 筆精心設計的樣本。之後，只要輸入中出現「James Bond」一詞，模型就頻繁地預測為「Positive」。這些被投毒的樣本刻意不包含觸發詞本身。

在網路規模下，資料來源這一步是弱點。Carlini 等人（2023）描述了兩種攻擊：分割視圖投毒（split-view poisoning）利用網頁內容在策展人檢視與之後使用者下載之間會改變的特性；搶先投毒（frontrunning poisoning）則是在週期性快照前，搶先編輯眾包網站（例如維基百科）。作者估計，LAION-400M 中 0.01% 的資料可以用約 60 美元完成投毒。

## 關鍵方法

下列幾種變體的差異在於攻擊者能控制什麼，以及毒素從流程的哪個環節進入。這些變體都沒有自己的頁面。

| 變體 | 攻擊者控制的內容 | 報告的規模 | 主要限制 |
|---|---|---|---|
| 觸發式投毒（Gu 等人，2017；Wallace 等人，2020） | 包含觸發條件的帶標籤樣本 | 情緒分類研究中約 50 筆樣本 | 異常樣本可能被發現 |
| 乾淨標籤投毒（Shafahi 等人，2018） | 標籤正確的樣本 | 遷移學習下僅一張影像 | 較難製作 |
| 調整階段投毒（Wan 等人，2023；Rando 與 Tramèr，2023） | 指令或偏好資料 | 指令微調中僅需約 100 筆 | 需要流程接受其貢獻 |
| 預訓練投毒（Carlini 等人，2023；Zhang 等人，2024；Souly 等人，2025） | 開放網路上的文件 | Zhang 等人為語料的 0.1%；Souly 等人為約 250 份文件 | 所需劑量如何隨規模變化並不清楚 |

Zhang 等人與 Souly 等人對劑量的描述不同：前者以佔語料的比例表示，後者以絕對數量表示。合併來看，兩者暗示在大規模下，絕對數量可能更重要，不過兩項研究的攻擊目標與模型規模並不相同。

Hubinger 等人（2024）探討的是：後門在被移除的嘗試之後是否還能存續。他們刻意建構的模型在提示寫明年份為 2023 時寫出安全程式碼，寫明 2024 時則插入漏洞。監督式微調、強化學習與對抗訓練都無法移除這種行為，而對抗訓練反而讓觸發條件更難被察覺。由於這些模型是刻意建構的，這項結果是一項壓力測試，而不是證明此類模型已經存在。

## 防禦

目前沒有完備的防禦，而且多數防禦是在影像分類器或較小的模型上測試的。

- **來源追溯**：記錄資料來源並固定快照。Carlini 等人（2023）通知了受影響資料集的維護者，並建議了低成本的防禦措施。
- **偵測**：啟動值分群（activation clustering）會對網路的激活值分組，使被投毒的樣本傾向形成自己的群組；它在文字與影像分類器上都有效（Chen 等人，2018）。過濾也有限：Wan 等人發現資料過濾只能提供中等程度的保護，Schuster 等人（2020）則發現，針對程式碼補全既有的防禦大多無效。
- **訓練後移除**：微調最少 500 步即可在權重可取得的情況下移除後門，但單靠提示工程則無效（Kandpal 等人，2023）。
- **稽核**：可能的觸發條件空間極為龐大，因此行為測試可能漏掉條件式的行為。

## 相關連結

- **權重與上下文。** 投毒改變的是權重，而[間接提示注入](indirect-prompt-injection.zh-TW.md)改變的是推論時的上下文，因此兩者需要不同的防禦。
- **紅隊測試。** 依賴觸發條件的後門，對於從未使用該觸發條件的測試來說是看不見的。Rando 與 Tramèr（2023）展示了這類越獄後門。見[越獄與紅隊測試](jailbreaks-and-red-teaming.zh-TW.md)。
- **護欄。** [護欄](guardrails.zh-TW.md)並不知道觸發條件，因此無法可靠地攔截被觸發的有害輸出。
- **安全與欺騙。** 潛伏代理人與[安全與對齊](../../society/safety-alignment/index.zh-TW.md)中的相關疑慮有關。偏好資料進入模型的方式，見[偏好最佳化](../training/preference-optimisation.zh-TW.md)。
- **大腦與心智。** 動物學習提供了一個粗略的類比：刺激與反應之間的關聯，可以被消弱學習（消退）所抑制而未被抹除，之後仍可能重現。兩者的機制並不相同，但這個比較有其參考價值；見[記憶與學習](../../brain-mind/memory-learning/index.zh-TW.md)。

## 應用

- **程式碼助理**：在公開儲存庫上訓練，少數精心設計的檔案就可能改變其建議（Schuster 等人，2020）。
- **以使用者貢獻進行調整的模型**：會承受上述調整階段的風險。
- **第三方檢查點**：這正是 BadNets 原本關切的問題：使用者無法檢視下載的模型是如何訓練出來的。

## 開放問題

- **需要多少毒素才足夠？** 兩項預訓練研究在網路規模下暗示了不同的成本，這個問題目前仍無定論。
- **訓練後是否能移除預訓練的後門？** Zhang 等人發現多種攻擊仍然存續，而生產規模的證據仍然有限。
- **規模化的偵測。** 多數防禦是在影像分類器或小型模型上測試的，因此它們在前沿語言模型上的表現大多未知。

## 參考文獻

### 開創性論文

- Gu, T., Dolan-Gavitt, B. & Garg, S. (2017). *BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain*. arXiv:1708.06733. https://arxiv.org/abs/1708.06733 — 外包訓練中的後門，即使為另一任務重新訓練仍然存續。
- Shafahi, A. et al. (2018). *Poison Frogs! Targeted Clean-Label Poisoning Attacks on Neural Networks*. arXiv:1804.00792. https://arxiv.org/abs/1804.00792 — 乾淨標籤投毒，單張被投毒的影像即可控制以遷移學習訓練的分類器。
- Wallace, E. et al. (2020). *Concealed Data Poisoning Attacks on NLP Models*. arXiv:2010.12563. https://arxiv.org/abs/2010.12563 — 以梯度方法製作的投毒文字，使觸發詞控制情緒分類模型。
- Carlini, N. et al. (2023). *Poisoning Web-Scale Training Datasets is Practical*. arXiv:2302.10149. https://arxiv.org/abs/2302.10149 — 針對網路規模圖文資料集的分割視圖與搶先投毒攻擊，並附成本估計。
- Wan, A. et al. (2023). *Poisoning Language Models During Instruction Tuning*. arXiv:2305.00944. https://arxiv.org/abs/2305.00944 — 顯示約 100 筆被投毒的指令樣本，即可使觸發詞在多種任務上產生偏向。
- Rando, J. & Tramèr, F. (2023). *Universal Jailbreak Backdoors from Poisoned Human Feedback*. arXiv:2311.14455. https://arxiv.org/abs/2311.14455 — 被投毒的 RLHF 資料植入一個觸發詞，使其成為通用的越獄指令。
- Kandpal, N. et al. (2023). *Backdoor Attacks for In-Context Learning with Language Models*. arXiv:2307.14692. https://arxiv.org/abs/2307.14692 — 能在不同提示策略下存續的後門，並在白箱與黑箱設定下測試防禦。
- Schuster, R. et al. (2020). *You Autocomplete Me: Poisoning Vulnerabilities in Neural Code Completion*. arXiv:2007.02220. https://arxiv.org/abs/2007.02220 — 經過精心設計的儲存庫檔案，可引導神經程式碼補全工具給出不安全的建議。
- Zhang, Y. et al. (2024). *Persistent Pre-Training Poisoning of LLMs*. arXiv:2410.13722. https://arxiv.org/abs/2410.13722 — 以被投毒的資料從頭預訓練模型，並測試其在後續訓練後是否存續。
- Souly, A. et al. (2025). *Poisoning Attacks on LLMs Require a Near-constant Number of Poison Samples*. arXiv:2510.07192. https://arxiv.org/abs/2510.07192 — 在 600M 至 13B 參數的模型規模範圍內，約 250 份被投毒的文件即足以成功。
- Hubinger, E. et al. (2024). *Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training*. arXiv:2401.05566. https://arxiv.org/abs/2401.05566 — 條件式後門在監督式微調、強化學習與對抗訓練後仍然存續。
- Chen, B. et al. (2018). *Detecting Backdoor Attacks on Deep Neural Networks by Activation Clustering*. arXiv:1811.03728. https://arxiv.org/abs/1811.03728 — 以激活值分群偵測被投毒的樣本，並在無受信任資料集的情況下修復模型。

### 綜述與教科書

- Li, Y. et al. (2020). *Backdoor Learning: A Survey*. arXiv:2007.08745. https://arxiv.org/abs/2007.08745 — 首篇針對後門攻擊與防禦的完整綜述，並提出統一的分析框架。
