---
translation_reviewed: 2026-10-28
related:
tags:
  - world models
  - latent actions
  - imitation learning
aliases:
  - LAPO
  - Learning to Act without Actions
  - 無動作標籤的潛在動作學習
---

# LAPO：Learning to Act without Actions

LAPO 從沒有動作標籤的影片中學習潛在動作。逆動力學模型依據連續的觀測推斷潛在動作，前向模型則依據目前的觀測與該潛在動作預測下一個觀測。向量量化瓶頸能阻止潛在動作直接複製下一個觀測。家族層級的整體說明見[世界模型與具身智慧](index.md)頁面。

## 概述

Schmidt 與 Jiang（2024）探討：只靠畫面，能否還原影片背後的動作。他們在摘要中指出，LAPO 僅從影片就能還原潛在動作資訊，而這些資訊可支持潛在動作策略、世界模型與逆動力學模型。論文發表於 ICLR 2024，為 spotlight 論文。實驗使用 Procgen 基準，共 16 個遊戲。

兩個相近的方法以不同角度看待同一問題。[Genie](genie.md) 在沒有動作標籤的情況下學習潛在動作模型，目的是生成可互動的世界。[DINO-WM](dino-wm.md) 則假設動作已知。

## 關鍵概念

- **潛在動作** \(z_t\)：描述從觀測 \(o_t\) 到 \(o_{t+1}\) 之轉變的學習得到的編碼。它沒有標籤，也不是真實的控制指令。
- **逆動力學模型（IDM）**：讀取觀測（包括 \(o_{t+1}\)），輸出 \(z_t\)。論文中它使用目前的觀測與下一個觀測（一步的上下文）。
- **前向動力學模型（FDM）**：依據過去的觀測與量化後的潛在動作，預測 \(o_{t+1}\)。它看不到 \(o_{t+1}\)。
- **向量量化（VQ）**：把每個潛在向量換成學習得到的碼本中的一個項目，限制傳給前向模型的資訊量。
- **潛在動作策略** \(\pi\)：把觀測映射到潛在動作。之後，一個小型解碼器把潛在動作映射為真實動作。

## 運作方式

對於未含動作的影片中的每一次轉變，IDM 與 FDM 計算

\[
z_t = \mathrm{IDM}(o_t, o_{t+1}), \qquad \hat o_{t+1} = \mathrm{FDM}\big(o_t,\ \mathrm{VQ}(z_t)\big)
\]

兩個模型以梯度下降共同訓練，目標是最小化下一個狀態的誤差 \(\lVert \hat o_{t+1} - o_{t+1}\rVert^2\)。梯度透過量化器時使用直通估計器（straight-through estimator）。

論文的表 1 列出瓶頸的設定：128 維的連續潛在動作，以 2 個碼本量化，每個碼本有 4 個離散潛在變數，嵌入維度為 16，承諾成本（commitment cost）為 0.05。

IDM 訓練完成後，流程接著進行三個步驟：

1. 潛在策略 \(\pi(o_t)\) 以迴歸方式學習 IDM 給出的潛在動作標籤，損失為 \(\lVert \pi(o_t) - z_t\rVert^2\)。
2. 以一小組有動作標籤的轉變訓練解碼器 \(d\)，把潛在動作映射為真實動作。
3. 部署組合後的策略 \(d \circ \pi\)。論文另外還有一個以 PPO 進行的線上微調階段。

## 關鍵方法

### Learning to Act without Actions（Schmidt & Jiang, 2024）

- **問題：** 多數策略與世界模型需要動作標籤，但大量影片沒有動作標籤。問題在於，從畫面還原出的潛在動作能否取代它們。
- **核心想法：** 共同訓練一個能看到下一個觀測的 IDM，與一個預測下一個觀測的 FDM，兩者之間加入向量量化瓶頸。瓶頸的目的，是阻止 IDM 把 \(o_{t+1}\) 複製進潛在動作。作者寫道，若沒有瓶頸，IDM「很可能會學到直接複製」下一個觀測。
- **方程式或演算法：** 上述 IDM/FDM 組合、潛在策略的迴歸損失，以及解碼器步驟。碼本設定見表 1。
- **結果：** 在 Procgen 上，第 6.1 節指出，LAPO 在 4M 幀內於 16 個任務中的 9 個超越專家。同樣的預算下，從頭以 PPO 訓練的策略只達到專家表現的 44%。引言指出，約 200 筆有標籤的轉變，就足以超越 4M 步的 PPO。第 6.2 節指出，以少於 256 筆有標籤轉變訓練的解碼器，可與從頭訓練的策略相當。
- **限制：** 本頁引用的實驗皆在 Procgen 上進行，因此並未展示能否轉移到機器人或真實世界影片。解碼器仍需要有標籤的轉變，而訓練目標本身無法決定哪個潛在值對應哪個真實動作。瓶頸是以資訊換取阻止捷徑的權衡：容量太小會失去動作細節，表 1 只給出一組所選設定，而非完整的掃描比較。

## 與其他主題的連結

- LAPO 瓶頸所阻止的複製捷徑，是[動作可控性](action-controllability.md)中的核心失效模式。
- Genie 與 LAPO 都從未標註的影片學習動作，但 Genie 用潛在動作來生成世界，LAPO 則用它們訓練策略並在遊戲任務上檢驗。
- DINO-WM 假設動作有標籤，因此不會遇到 LAPO 所要回答的問題。
- 潛在策略屬於行為複製問題，見[行為複製](../../paradigms/imitation/behavioural-cloning/index.md)。

## 開放問題

- 要在不同遊戲與機器人本體上可靠地解碼潛在動作，需要多少有標籤的轉變。
- 瓶頸的設計能否轉移到 Procgen 式以外的視覺領域。
- 當影片含有干擾項時，潛在動作是否仍依賴代理人的動作。這是可控性的問題，見[動作可控性](action-controllability.md)。

## 參考文獻

### 奠基性論文

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024（spotlight）. https://arxiv.org/abs/2312.10812 — 提出 LAPO，從無動作的影片中還原潛在動作，並以向量量化瓶頸阻止逆模型複製下一個觀測。

### 相關方法

- Bruce, J. 等人 (2024). *Genie: Generative Interactive Environments*. ICML 2024（PMLR 235）. https://proceedings.mlr.press/v235/bruce24a.html — 在沒有動作標籤的情況下學習潛在動作模型，用於生成可互動的環境。
- Zhou, G.、Pan, H.、LeCun, Y. 與 Pinto, L. (2025). *DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning*. ICML 2025（PMLR 267）. https://proceedings.mlr.press/v267/zhou25t.html — 以凍結的 DINOv2 特徵為基礎的動作條件世界模型，動作視為已知輸入。
- Rudolph, M.、Chuck, C.、Black, K.、Lvovsky, M.、Niekum, S. 與 Zhang, A. (2024). *Learning Action-based Representations Using Invariance*. Reinforcement Learning Journal, vol. 1（發表於 RLC 2024）. https://rlj.cs.umass.edu/2024/papers/Paper39.html — 分析逆動力學在有限時程內如何捕捉可控性，並提出動作雙模擬。

### 文章與預印本

- Zhang, Z. 等人 (2026). *Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding*. arXiv 預印本 2606.31232. https://arxiv.org/abs/2606.31232 — 從觀測間的潛在位移解碼動作，而非從串接的端點嵌入解碼。預印本，尚未經同儕審查。
- Shi, Y. 等人 (2026). *Overcoming Statistical Bias in Action-Controllable World Models*. arXiv 預印本 2608.04653. https://arxiv.org/abs/2608.04653 — 提出 CoCo，以反事實一致性框架作為另一種補救方法。預印本，尚未經同儕審查。
