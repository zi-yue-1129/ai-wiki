---
translation_reviewed: 2026-10-28
tags:
  - world models
  - latent actions
  - imitation learning
aliases:
  - LAPO
  - Learning to Act without Actions
  - 無動作標籤的潛在動作學習
---

# LAPO（Learning to Act without Actions）

LAPO 是一種從沒有動作標籤的影片中學習潛在動作的方法。它訓練一個逆動力學模型，從連續幀推斷潛在動作；並訓練一個前向模型，依據目前的幀與該潛在動作預測下一幀。量化瓶頸讓潛在動作無法直接複製下一幀。

## 問題

有動作標籤的機器人與遊戲資料收集成本高，而人在做事的影片很多。LAPO 探討：能否只從畫面還原影片背後的動作，以及還原出的動作是否足以訓練策略、世界模型或逆動力學模型。

## 核心想法

同時訓練兩個模型。逆模型看到整段觀測序列，為每次轉變預測一個潛在動作。前向模型依據目前的觀測與該潛在動作預測下一個觀測。由於逆模型能看到下一幀，它有一條捷徑：直接把下一幀編碼進去。作者在潛在動作送入前向模型前加入向量量化，以阻止這條捷徑。Schmidt 與 Jiang（2024）指出，若沒有量化，逆模型「很可能會學到直接複製」下一個觀測。

## 運作方式

1. 觀察未含動作的影片中的連續幀。
2. 逆動力學模型讀取完整的觀測序列，為每次轉變輸出一個潛在動作。
3. 對潛在動作做向量量化，限制其資訊量。
4. 前向動力學模型依據目前的觀測與量化後的潛在動作，預測下一個觀測。
5. 以預測損失端對端訓練兩個模型。之後，一個小型解碼器可以把少量有標籤的轉變對應到真實動作，這就是潛在動作策略的使用方式。

摘要指出，學到的潛在動作可支持潛在動作策略、世界模型與逆動力學模型。確切的損失函數與解碼步驟見論文。

## 關鍵方法

- 相對於 [Genie](genie.md)，後者同樣使用這類潛在動作來生成可互動的世界；LAPO 則著重於從影片訓練策略與模型。
- 相對於 [DINO-WM](dino-wm.md)，後者假設動作已知；LAPO 則從影片還原動作，因此瓶頸的設計很重要。

## 結果

摘要指出，LAPO 僅從影片就能還原潛在動作資訊，且這些資訊可支持上述下游模型。基準測試的結果應直接從論文抄錄。

## 限制

- 量化瓶頸是一種設計選擇，用資訊換取阻止捷徑。容量太小會失去動作細節，太大則會重新啟用複製捷徑。
- 以這種方式學到的潛在動作，不保證與真實機器人指令的意義相符。需要少量有標籤的資料，才能把它對應到真實動作。
- 當環境中有干擾項時，潛在動作是否仍依賴於動作本身，是可控性的問題，見[動作可控性](action-controllability.md)。

## 與其他主題的連結

LAPO 是[動作可控性](action-controllability.md)中所述複製捷徑的代表方法。它也與模仿學習相關，潛在動作可以作為策略的輸出空間，見[模仿學習](../../paradigms/imitation/index.md)。上層總覽在[世界模型與具身智慧](index.md)。

## 應用

從未標註的遊戲或機器人影片訓練潛在動作策略，以及在加入少量有標籤動作之前，先從影片初始化世界模型。

## 開放問題

- 要把潛在動作可靠地對應到真實動作，需要多少有標籤的資料。
- 瓶頸的設計能否轉移到不同的機器人本體與視覺領域。

## 參考文獻

### 奠基性論文

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024（spotlight）. https://arxiv.org/abs/2312.10812 — 提出 LAPO，從無動作的影片中學習潛在動作，並以向量量化阻止逆模型複製下一個觀測。

### 文章與預印本

- Bruce, J. 等人 (2024). *Genie: Generative Interactive Environments*. ICML 2024. https://proceedings.mlr.press/v235/bruce24a.html — 在生成式設定中，使用從未標註影片學到的潛在動作模型，是相近的方法。
- Rudolph, M. 等人 (2024). *Learning Action-based Representations Using Invariance*. Reinforcement Learning Conference 2024. https://arxiv.org/abs/2403.16369 — 分析 LAPO 瓶頸所要阻止的單步逆動力學捷徑。
- Zhang, Z. 等人 (2026). *Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding*. arXiv 預印本. https://arxiv.org/abs/2606.31232 — 針對同一洩漏問題的較新工作，從潛在差值解碼動作。預印本，尚未經同儕審查。
- Shi, Y. 等人 (2026). *Overcoming Statistical Bias in Action-Controllable World Models*. arXiv 預印本. https://arxiv.org/abs/2608.04653 — 以反事實一致性規範作為另一種補救方法。預印本，尚未經同儕審查。
