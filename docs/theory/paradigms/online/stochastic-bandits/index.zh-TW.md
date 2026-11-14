---
translation_reviewed: 2026-11-14
---

# 隨機多臂吃角子老虎（Stochastic Bandits）

隨機多臂吃角子老虎問題假設每個臂（arm）都有固定但未知的獎勵分布。學習者必須在**探索**各臂以估計期望獎勵，以及**利用**目前看起來最好的臂之間取得平衡。信賴上界（Upper Confidence Bound, UCB）與 Thompson 取樣是兩種代表性方法；在適當假設下，它們能達到對數級遺憾上界。

## 概述

遺憾（regret）比較學習者實際累積獎勵，與總是選擇最佳臂所能取得的期望累積獎勵。Lai 與 Robbins 證明，對典型的隨機多臂問題而言，對數級遺憾具有不可避免的下界。UCB 以**樂觀估計**選擇「經驗平均獎勵加上信賴寬度」最高的臂；Thompson 取樣則維持各臂獎勵參數的後驗分布，從中抽樣，選擇抽樣結果最佳的臂。

## 主要演算法

- **UCB1（信賴上界）**：在每個臂的經驗平均值上加入代表不確定性的信賴寬度，選擇總分最大的臂。
- **Thompson 取樣**：從各臂後驗分布抽取可能的期望獎勵，選擇抽樣結果最高的臂。此法在實務上經常有效，且容易應用於貝氏模型。
- **先探索再固定（explore-then-commit）與 ε-greedy**：較簡單的基準策略，但理論保證與適用條件不同。

## 教學動畫：樂觀探索與後驗抽樣

### UCB1：信賴寬度如何改變選擇

<div class="bandit-motion-viewport" role="region" tabindex="0" aria-label="可使用方向鍵水平捲動的 UCB1 教學動畫">
  <img src="../../../../assets/concept-animations/ucb1-optimism-switch-still.svg" data-motion-src="../../../../assets/concept-animations/ucb1-optimism-switch-motion.svg" data-still-src="../../../../assets/concept-animations/ucb1-optimism-switch-still.svg" alt="三個 UCB1 臂的經驗平均值與探索加分：起初連續兩次選擇 B，兩次假設的零獎勵使其分數下降，接著改由 A 領先。" />
</div>

*原創連續教學動畫（CC BY-SA 4.0）。* UCB1 對每個臂 $i$ 使用 $\bar X_i+\sqrt{2\ln(t)/n_i}$ 計分，並選擇最大者。示例在 $t=16$ 開始，三臂的抽樣次數為 $(6,2,8)$，經驗平均值為 $(0.65,0.45,0.60)$。B 在兩次被選擇後，都得到**人為設定的零獎勵**，因此抽樣次數從 2 增至 4，平均值從 0.45 降至 0.225；樂觀分數最高的臂便由 B 轉為 A。藍色表示經驗平均值、橘色表示信賴寬度，綠色框表示目前分數最大的臂。動畫轉場只是不同離散決策狀態間的**視覺插值，並非模型實測或連續訓練軌跡**；未被選擇的臂不會在該步獲得回饋。在 MkDocs 網站可使用**播放／暫停**按鈕（鍵盤 **Enter／Space**）；手機畫面可聚焦後水平捲動。GitHub 也有可直接閱讀的[靜態預覽](../../../../assets/concept-animations/ucb1-optimism-switch-still.svg)。原始來源為 References 中的 Auer、Cesa-Bianchi 與 Fischer（2002）。

### Thompson 取樣：後驗抽樣及局部更新

<div class="bandit-motion-viewport" role="region" tabindex="0" aria-label="可使用方向鍵水平捲動的 Thompson 取樣教學動畫">
  <img src="../../../../assets/concept-animations/thompson-beta-posterior-draws-still.svg" data-motion-src="../../../../assets/concept-animations/thompson-beta-posterior-draws-motion.svg" data-still-src="../../../../assets/concept-animations/thompson-beta-posterior-draws-still.svg" alt="三個 Beta 後驗密度與各臂一次抽樣的候選機率：第一輪選 C，接著 C 的一次假設成功回饋只更新 C 的後驗，新一輪抽樣改選 A。" />
</div>

*原創連續教學動畫（CC BY-SA 4.0）。* 在**伯努利獎勵**的示意中，三臂各自具有獨立的後驗分布：$A\sim\operatorname{Beta}(3,3)$、$B\sim\operatorname{Beta}(2,5)$、$C\sim\operatorname{Beta}(4,3)$。對每個臂各抽取一次所建構的樣本 $(0.47,0.22,0.71)$，第一輪選出 C。假設 C 收到一次成功回饋，**只有 C** 的後驗更新為 $\operatorname{Beta}(5,3)$；下一輪假設的抽樣 $(0.57,0.38,0.52)$ 則選出 A。移動的圓點是**人工指定的後驗抽樣結果**，不是後驗平均數、模型信心、可重現隨機種子或實測輸出；密度曲線的連續變化也只是兩個離散後驗之間的視覺轉場。在 MkDocs 網站可使用播放／暫停和 Enter／Space 操作；GitHub 提供[靜態回退預覽](../../../../assets/concept-animations/thompson-beta-posterior-draws-still.svg)。科學依據請參見 References 中的 Agrawal 與 Goyal（2012）以及 Russo 等人（2018）。

### 互動計算實驗：UCB1 對獎勵的敏感度

<div class="bandit-lab" data-bandit-lab="ucb" data-lang="zh-TW">
  <p>若 MkDocs 無法載入互動程式，仍可閱讀上方不需 JavaScript 的靜態教學圖。</p>
</div>

本實驗會依照抽取次數 $(6,2,8)$ 與累積獎勵 $(3.9,0.9,4.8)$，在 $t=16,17,18$ **重新計算 UCB1**。調整 B 接下來兩次抽取各收到的假設獎勵 $r\in[0,1]$；當 B 新增 $k=0,1,2$ 次觀察後，其經驗平均值為 $(0.9+kr)/(2+k)$。在滑桿允許的獎勵範圍內，前兩次選擇 B 都符合當時的 UCB 最大分數。當 $r=0$，三個決策狀態最高分依序是 **B → B → A**；當 $r=1$，第二次觀察後 B 仍領先。不同臂的彩色長條表示經驗平均獎勵，金色表示探索加分。數值是**解析式計算的人工示例**，不是實際遺憾或訓練曲線。

### 互動計算實驗：Beta 後驗更新

<div class="bandit-lab" data-bandit-lab="thompson" data-lang="zh-TW">
  <p>若 MkDocs 無法載入互動程式，仍可閱讀上方不需 JavaScript 的靜態教學圖。</p>
</div>

透過**上一步／下一步、播放／暫停、步驟滑桿、速度調整與重設**，依序查看初始後驗、人工指定的首次抽樣、觀察結果與第二次抽樣。第一次抽樣選出 C；切換 C 的伯努利觀察獎勵 $r\in\{0,1\}$，可立即重新計算其後驗 $\operatorname{Beta}(4+r,4-r)$：成功時為 Beta(5,3)，失敗時為 Beta(4,4)，**其他兩臂的後驗維持不變**。第二組人工指定的抽樣為 $(0.57,0.38,0.52)$，這組候選值在任一假設結果下都選 A，但並非真正執行亂數抽樣所得的實驗紀錄。請勿把離散後驗的切換視為連續貝氏更新。控制項可透過鍵盤操作；開啟減少動態效果時不會自動播放，仍可手動逐步檢視。手機可聚焦於 720px 圖面後水平捲動。

## 關聯

多臂吃角子老虎是沒有狀態轉移的[強化學習](../../reinforcement-learning/index.md)單步特例。Thompson 取樣使用的後驗推論，與[機率式模型](../../supervised/instance-based-and-probabilistic/index.md)的貝氏推論概念相通。若每個決策還可利用外部特徵，則延伸為[情境式多臂吃角子老虎](../contextual-bandits/index.md)。

## 應用

適應性分流的 A/B 測試、臨床試驗中的劑量探索，以及在固定的提示或模型候選之間進行選擇。

## 開放問題

重尾獎勵、延遲回饋、非平穩的獎勵分布可能破壞標準理論保證。在實際系統中，UCB 與 Thompson 取樣的適用性也取決於獎勵模型如何更新。

## 參考文獻

### 奠基性論文

- Lai & Robbins（1985），"Asymptotically efficient adaptive allocation rules"，*Advances in Applied Mathematics*。https://doi.org/10.1016/0196-8858(85)90002-8 — 建立遺憾的漸近對數下界。
- Auer, Cesa-Bianchi & Fischer（2002），"Finite-time analysis of the multiarmed bandit problem"，*Machine Learning*。https://homes.di.unimi.it/~cesabian/Pubblicazioni/ml-02.pdf — 提出 UCB1 及其有限時間遺憾上界。
- Agrawal & Goyal（2012），"Analysis of Thompson sampling for the multi-armed bandit problem"，COLT。[arXiv:1111.1797](https://arxiv.org/abs/1111.1797) — Thompson 取樣的對數級遺憾分析。

### 綜述及教科書

- Bubeck & Cesa-Bianchi（2012），"Regret analysis of stochastic and nonstochastic multi-armed bandit problems"，*Foundations and Trends in Machine Learning*。[arXiv:1204.5721](https://arxiv.org/abs/1204.5721) — 同時整理隨機式與對抗式多臂問題。
- Lattimore & Szepesvári（2020），*Bandit Algorithms*，Cambridge University Press。https://cambridge.org/core/books/bandit-algorithms/introduction/022B0BDCFDC5B66E5EF2C2690467D928 — 完整介紹 UCB、Thompson 取樣及理論下界。

### 更多正式教學資源

- Russo, Van Roy, Kazerouni, Osband & Wen（2018），"A tutorial on Thompson sampling"，*Foundations and Trends in Machine Learning*。[arXiv:1707.02038](https://arxiv.org/abs/1707.02038) — 從貝氏推論說明後驗抽樣與探索。

## 延伸學習

- Slivkins（2019），"Introduction to multi-armed bandits"。[arXiv:1904.07272](https://arxiv.org/abs/1904.07272) — 多臂問題與情境式擴充的入門整理。