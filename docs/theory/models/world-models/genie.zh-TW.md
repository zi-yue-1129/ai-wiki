---
translation_reviewed: 2026-10-28
tags:
  - world models
  - video generation
  - latent actions
aliases:
  - Genie
  - 生成式互動環境
---

# Genie

Genie 是一種生成模型，能把單張影像或提示轉換成可互動、可操控的環境。它的特色是自行學會控制方式：潛在動作模型從未標註的網路影片中找出一小組離散動作，因此不需要動作標籤，就能讓生成的世界對輸入產生反應。

## 問題

影片生成模型能產生合理的影片片段，但觀看者無法在其中行動。訓練可控的模擬器通常需要記錄下來的動作，而大多數網路影片沒有動作記錄。Genie 探討：能否只從畫面推斷影片背後的動作，以及推斷出的動作能否讓使用者逐幀控制生成的世界。

## 核心想法

Genie 有三個學習得來的部分：影片分詞器（tokenizer）、預測下一幀 token 的動態模型，以及潛在動作模型。潛在動作模型在沒有動作標籤的情況下訓練，它讀取影格，並在每一步選出一個潛在動作；動態模型則利用該潛在動作預測下一幀。作者指出，潛在動作讓生成的環境能在沒有動作標籤的情況下逐幀控制。

## 運作方式

1. 用學習得來的影片分詞器，把每一幀切成 token。
2. 在未標註的影片上訓練潛在動作模型，推斷相鄰幀之間的離散潛在動作。
3. 訓練動態模型，依據過去的 token 與潛在動作預測下一幀的 token。
4. 遊玩時，使用者的輸入在學到的潛在動作中做選擇，動態模型生成下一幀。

## 關鍵方法

- 相對於 [LAPO](lapo.md)，後者學習潛在動作是為了從影片訓練策略與逆模型；Genie 則著重於生成可互動的世界，並把潛在動作當作控制介面。
- 相對於 [V-JEPA 2](v-jepa-2.md)，後者在表徵空間中預測以供規劃；Genie 則生成使用者可以操作的像素。

## 結果

摘要指出，在沒有標籤下學到的潛在動作空間，可以逐幀控制生成的環境；學到的動作也能用來訓練代理人，模仿未見過的影片中的行為。定量結果見論文。

## 限制

- 潛在動作是離散的，不保證與真實控制器的輸入意義相符。一個潛在動作可能合併了數種效果。
- 生成世界的一致性取決於動態模型對先前幀的記憶。論文將長時程一致性視為尚未解決的限制。

## 與其他主題的連結

Genie 屬於[世界模型總覽](index.md)中的影片分支，那裡稱之為「影片生成作為世界模擬器」。它的潛在動作模型與 [LAPO](lapo.md) 共享瓶頸的概念，這在[動作可控性](action-controllability.md)中有討論。遊戲是很自然的應用領域，見[遊戲](../../../applications/games/index.md)。

## 應用

可互動的生成環境、具身代理人的訓練資料，以及研究代理人動作如何被表徵的研究工具。

## 開放問題

- 從遊戲影片學到的潛在動作，能否轉移到控制方式不同的機器人。
- 如何讓生成的世界在長時間的操作中保持一致。

## 參考文獻

### 奠基性論文

- Bruce, J.、Dennis, M.、Edwards, A. 等人 (2024). *Genie: Generative Interactive Environments*. ICML 2024. https://proceedings.mlr.press/v235/bruce24a.html — 提出 Genie，從未標註影片中學習潛在動作空間，並提供生成環境的逐幀控制。arXiv 版本見 https://arxiv.org/abs/2402.15391。

### 文章與預印本

- Schmidt, D. & Jiang, M. (2024). *Learning to Act without Actions*. ICLR 2024（spotlight）. https://arxiv.org/abs/2312.10812 — 以量化瓶頸從無動作的影片學習潛在動作，是相近的方法。
- Yang, S. 等人 (2023). *Learning Interactive Real-World Simulators*. arXiv 預印本. https://arxiv.org/abs/2310.06114 — 會對動作做出反應的影片模擬器，在影像、機器人與導航資料的組合上訓練。
- Micheli, V.、Alonso, E. 與 Fleuret, F. (2022). *Transformers are Sample-Efficient World Models*. arXiv 預印本. https://arxiv.org/abs/2209.00588 — IRIS，由離散自編碼器與自回歸 transformer 組成的世界模型，與 Genie 使用的「先分詞、再預測」模式相同。
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv 預印本. https://arxiv.org/abs/1803.10122 — 早期的潛在世界模型：特徵來自無監督訓練的世界模型，策略可在模型自身模擬的環境中訓練後再轉移。
