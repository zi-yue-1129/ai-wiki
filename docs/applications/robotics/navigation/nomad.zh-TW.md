---
translation_reviewed: 2026-10-28
tags:
  - robotics
  - navigation
  - diffusion policy
  - exploration
aliases:
  - NoMaD
  - Goal masked diffusion policy
  - 目標遮罩擴散策略
---

# NoMaD：目標遮罩擴散策略

NoMaD 由 Sridhar、Shah、Glossop 與 Levine（2023）提出，是一個以擴散模型取代單一回歸輸出的導航策略，擴散模型作用於動作序列上。它的目標遮罩讓同一個網路既能抵達目標影像，也能在沒有目標時探索。論文的核心論點是：單峰的回歸不適合路口這類情境，因為此時有幾種動作同樣好；取樣得到的分布則能保留這些選項。上層子主題是[以視覺目標導航](index.md)。

## 概述

NoMaD 是擴散策略：它以目前觀測為條件，對隨機樣本做去噪，產生未來的動作序列。訓練時，目標影像會在部分樣本中被遮掉，因此同一個網路同時學會以目標為條件的導航，以及無目標的探索。模型體積不大，論文報告它能在小型嵌入式電腦上執行。

## 問題

每個觀測只輸出一個動作的回歸策略，會對各種模式取平均。在機器人可以左轉或右轉的路口，平均結果可能是直直撞向牆壁。論文探討：生成式策略能否避免這個問題，以及同一模型能否同時做以目標為導向的導航與探索。

## 核心想法

以擴散過程對動作序列的分布建模，並以觀測（有目標時還包括目標）為條件。訓練時遮掉目標，讓模型學會無目標時的行為，因此不需要另外訓練第二個網路。

## 運作方式

1. 編碼目前的觀測，以及有目標時的目標影像。
2. 從一個動作序列的隨機樣本開始，以編碼後的輸入為條件做去噪。
3. 執行取樣所得序列的前幾個動作，然後再重新取樣。
4. 訓練時，在部分樣本中遮掉目標，使模型學會無目標的行為。

## 結果

論文報告，以目標為條件的成功率與 ViNT 相當；在探索方面，模型的碰撞次數少，且體積遠小於作者比較的子目標擴散基線。作者也報告，模型能在小型嵌入式電腦上即時執行。數字取決於所用的環境，應在重用前於論文中核對。

## 限制

- 擴散取樣需要數個去噪步驟，因此每個動作的運算量高於單次前向傳播。
- 相較於回歸，優勢在路口等多模態情境中最明顯；在開闊的走廊中，優勢較小。
- 評估是在作者所用的機器人平台與環境上進行，因此對其他平台的泛化並未展示。

## 相關主題

- [ViNT](vint.md) 是 NoMaD 比較以目標為條件的表現時所用的回歸 Transformer 策略。
- [GNM](gnm.md) 是共用模型的前身，同一研究團隊的導航工作即建立於其上。
- [Hirose 等人（2019）](https://arxiv.org/abs/1903.02749) 較早顯示，把打分的目標蒸餾成策略，可以勝過執行時打分。

## 開放問題

- 當去噪步數減少以加快控制時，擴散策略相對於回歸的優勢是否仍然成立。
- 目標遮罩如何與需要不同長程行為的探索與抵達目標互動。

## 參考文獻

- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv:2310.07896. https://arxiv.org/abs/2310.07896 — 目標遮罩擴散策略與其導航結果的來源。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — 以目標為條件導航的回歸基線。
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — 共用模型與輸出空間比較。
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep visual MPC-policy learning for navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. arXiv:1903.02749. https://arxiv.org/abs/1903.02749 — 把打分的目標蒸餾成策略。
- Meng, X., Ratliff, N., Xiang, Y., & Fox, D. (2020). *Scaling local control to large-scale topological navigation*. ICRA 2020. arXiv:1909.12329. https://arxiv.org/abs/1909.12329 — 拓撲地圖上控制輸出的比較。
