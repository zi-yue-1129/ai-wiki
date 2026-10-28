---
translation_reviewed: 2026-10-28
related:
  - applications/robotics/navigation
  - theory/paradigms/imitation
tags:
  - robotics
  - navigation
  - diffusion
  - exploration
aliases:
  - NoMaD
  - Goal Masked Diffusion Policy
  - 目標遮罩擴散策略
---

# NoMaD：目標遮罩擴散策略

NoMaD 由 Sridhar、Shah、Glossop 與 Levine（2023）提出，是一個同時做兩件事的擴散策略：目標已知時抵達目標影像，目標未知時探索新環境。這兩種行為來自同一個網路，由目標輸入上的二元遮罩切換。所屬的子主題是 [以視覺目標導航](index.md)。

## 概述

在陌生地方導航需要兩種能力，通常由不同的元件負責。以任務為導向的導航，是抵達機器人已經找到的目標。與任務無關的探索，則是在機器人沒見過的環境中搜尋目標。早期的系統為每種能力使用一個模型，或依賴子目標提議與規劃器。NoMaD 訓練單一策略同時做到兩者，作者報告，相較於使用生成模型子目標提議或較早的潛變數方法，這種做法在新環境中的整體表現較好（Sridhar et al., 2023）。

## 問題

探索與抵達目標會把策略拉向不同方向。探索中的機器人應該在沒有目的地的情況下覆蓋區域並避免碰撞，抵達目標的機器人則應朝特定影像前進。若要用同一個模型兩者兼顧，就需要一種方式告訴模型目前處於哪種模式，而且模型在兩種模式下都必須產生有用的動作。

## 核心想法

把目標當作一個輸入權杖給策略，並附上一個二元遮罩，控制網路是否可以注意該權杖。遮罩開啟時，策略忽略目標而進行探索；遮罩關閉時，策略以目標為條件並朝它導航。訓練時遮罩隨機抽樣，因此網路從同一份資料學會兩種行為。

## 方程式或演算法

NoMaD 是一個條件式去噪擴散策略：

1. **編碼器。** EfficientNet-B0 編碼器把過去五個觀測（各為 96 × 96 像素）與選擇性的目標影像轉換成 256 維的權杖。
2. **目標遮罩。** 二元遮罩 *m* 控制對目標權杖的注意力。訓練時 *m* 以 *p* = 0.5 的伯努利分布抽樣。測試時，*m* = 1 給出無方向的探索，*m* = 0 給出以目標為條件的導航。
3. **Transformer 與去噪器。** 一個四層、四頭的 Transformer 解碼器為一個一維條件 U-Net 提供上下文，該 U-Net 對一串未來動作進行去噪。論文的圖中顯示八個未來動作。
4. **訓練。** 去噪目標是加在真實動作序列上的雜訊與網路預測雜訊之間的均方誤差。另加一個權重較小的時間距離項。
5. **抽樣。** 測試時，策略透過十個去噪步驟抽取動作。探索在線上建立的拓撲圖中以無方向模式進行，子目標選擇沿用 ViKiNG 的邊界（frontier）方法。

模型約有 1,900 萬個參數，如論文的比較表所列。

## 結果

論文報告兩類評估。探索以成功的比例與碰撞次數評分。論文的表 I 給出 NoMaD 與比較方法在室內與室外情境的數值：

| 方法 | 探索成功率 | 每次執行的碰撞數 | 導航成功率 |
|---|---|---|---|
| 遮罩 ViNT | 50% | 1.0 | 30% |
| VIB | 30% | 4.0 | 15% |
| 自回歸 | 90% | 2.0 | 60% |
| 隨機子目標 | 70% | 2.7 | 90% |
| 子目標擴散（3.35 億參數） | 77% | 1.7 | 90% |
| NoMaD（1,900 萬參數） | 98% | 0.2 | 90% |

論文的表 II 報告 NoMaD 在無方向與以目標為條件兩種模式下的成功率分別為 98% 與 92%，對照之下，無方向模式的一般擴散策略為 98%，以目標為條件模式的 ViNT 策略為 92%。論文的實驗在未見過的環境中以行動機器人進行。正文在不同地方給出的評估環境數不同，因此環境清單應以論文的附錄為準。

## 限制

- 探索依賴標準的邊界規劃。論文提出較聰明的區域選擇，例如語意或先驗策略，作為未來工作。
- 目標影像雖然通用，但對使用者而言未必是最自然的指定目的地方式。本版本不支援語言與空間座標。
- 作者把結果描述為概念驗證。他們報告 NoMaD 在除了最困難環境以外都能成功，但對其他失敗模式的分析很少。

## 相關連結

- [GNM](gnm.md) 與 [ViNT](vint.md) 是 NoMaD 所比較的以目標為條件的策略，而 ViNT 的 Transformer 設計與 NoMaD 的編碼器最為接近。
- [擴散策略](../../../theory/paradigms/imitation/index.md) 透過模仿學習而得，與本頁多數導航策略屬於同一範式。
- [視覺教導與重播](visual-teach-and-repeat.md) 是不需要學習探索的經典替代方法。

## 開放問題

- 單一擴散策略在非常大或會改變的環境中，能否與使用度量地圖的規劃器探索得一樣好。
- 目標遮罩如何推廣到影像以外的其他目標類型。

## 參考文獻

- Sridhar, A., Shah, D., Glossop, C. & Levine, S. (2023). *NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration*. arXiv. https://arxiv.org/abs/2310.07896 — 目標遮罩策略、比較表與探索結果的來源。
- Chi, C. et al. (2023). *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*. arXiv. https://arxiv.org/abs/2303.04137 — 將機器人策略表示為對動作的條件式去噪擴散過程。
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. arXiv. https://arxiv.org/abs/2006.11239 — 策略抽樣器所依據的去噪擴散模型。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N. & Levine, S. (2023). *ViNT: A Foundation Model for Visual Navigation*. arXiv. https://arxiv.org/abs/2306.14846 — NoMaD 所比較的 Transformer 策略與子目標擴散基線。
- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N. & Levine, S. (2022). *GNM: A General Navigation Model to Drive Any Robot*. arXiv. https://arxiv.org/abs/2210.03370 — 同一研究群較早的共享導航模型，作為以目標為條件導航的背景。
