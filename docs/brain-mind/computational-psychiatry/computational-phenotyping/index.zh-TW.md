---
translation_reviewed: 2026-10-28
related:
- brain-mind/decision-reward
- theory/paradigms/reinforcement-learning
tags:
- computational psychiatry
- reinforcement learning
- Bayesian inference
aliases:
  - 計算表型分析
  - 階層式貝氏強化學習模型
  - hBayesDM
  - Computational phenotyping
  - Hierarchical Bayesian reinforcement learning
---

# 以階層式貝氏強化學習模型進行計算表型分析（Ahn、Haines 與 Zhang，2017）

計算表型分析為每個人在某項任務中的選擇擬合一個計算模型，然後把擬合出的參數當作該人如何學習或決策的數值摘要。階層式貝氏擬合則同時為所有人估計這些參數。本頁說明 hBayesDM 套件（Ahn 等人，2017）所封裝的這個方法。

本頁屬於[計算精神醫學](../index.md)。它是一種研究方法，所產生的參數並非診斷。

## 概述

行為任務會給每個人一串選擇與結果。常見的摘要，例如整體正確率或平均選擇比例，會把好幾種歷程混在一起。兩個正確率相同的人，可能在從結果中學習的速度、探索的程度，或是損失改變其選擇的力度上有所不同。一個只有少數參數的模型試圖把這些歷程分開，而擬合出的數值便成為個體差異的候選量數。

## 問題

逐人擬合模型很簡單，但當每個人只貢獻少數試驗時，效果很差。估計值會有很大的雜訊，甚至可能取得不合理的數值。精神醫學的樣本通常很小。

## 核心想法

每個人的選擇，都由一個帶有少數自由參數的模型來描述，例如學習率與選擇敏感度參數。階層式貝氏擬合假設個別參數來自一個共享的群體分布。它同時估計個別參數與群體分布，因此每個人的估計也參考了其他人的資料。資料少的人會被拉向群體平均，而群體分布本身也從樣本中學得。Ahn 等人（2017）描述了 hBayesDM，這是一個把階層式貝氏建模應用於一組決策任務的 R 套件，讓研究者不必自行撰寫擬合程式。

## 方程式或演算法

一個常見的例子是用於二選一任務的 delta 規則強化學習模型。被選選項的價值，會以預測誤差來更新：

\(\delta_t = r_t - Q_t(a)\)，且 \(Q_{t+1}(a) = Q_t(a) + \alpha\,\delta_t\)

選擇以 softmax 規則進行，其中 \(\beta\) 控制對價值較高選項的偏好強度：

\(P(a_t = a) = \dfrac{\exp(\beta\,Q_t(a))}{\sum_b \exp(\beta\,Q_t(b))}\)

以階層方式擬合此類模型的步驟如下：

1. 從理論中選擇一項任務與一或多個候選模型。
2. 寫出概似函數，即在模型與其參數下，觀察到每個選擇的機率。
3. 把每個人的參數置於轉換後的尺度上，例如 \(\alpha_i = \Phi(\mu_\alpha + \sigma_\alpha z_i)\)，其中 \(z_i \sim \mathcal{N}(0,1)\)，\(\Phi\) 為標準常態分布函數；並為群體層級參數 \(\mu\) 與 \(\sigma\) 設定各自的先驗分布。
4. 以貝氏抽樣同時估計個別與群體參數。
5. 比較候選模型，並報告參數估計值及其不確定性。

第 3 步是一般形式，並非來自單一論文的公式。經驗先驗（即從資料設定的先驗）是選擇群體層級先驗的一種方式（Gershman，2016）。

## 結果

Ahn 等人（2017）把 hBayesDM 介紹為一個能在決策任務上擬合這些模型的工具。本頁不引用該論文的基準數字，因為其所主張的是套件的可用性，而非可量測的效果。

## 限制

- **模型依賴。**參數的意義取決於模型所說的內容。對同樣的行為，不同模型可能給出不同的參數值。Wilson 與 Collins（2019）強調，模型必須謹慎使用，才能產生有意義的洞見。
- **收縮效應。**把個別估計拉向群體平均，在資料稀少時能使估計更穩定，但也可能模糊人與人之間的真實差異。收縮的程度取決於先驗，因此先驗的選擇很重要。
- **任務特異性。**參數是在某一任務內測得的。參數可能捕捉的是該任務特有的策略，而不是穩定的特質。
- **效度。**模型能擬合行為，並不表示其參數就是症狀背後的機制。

## 與其他主題的關聯

- **強化學習**：delta 規則與 softmax 選擇規則，是[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)中的標準模型。更新式中的預測誤差，與[多巴胺的獎勵預測誤差](../../neuroscience/dopamine-reward-prediction-error/index.md)中多巴胺理論所用的量相同。
- **控制器**：當任務能區分習慣性與規劃性的選擇時，表型分析可估計各控制器被使用的程度。見[有模型與無模型控制](../../decision-reward/model-based-vs-model-free/index.md)與[決策、多巴胺與獎勵](../../decision-reward/index.md)。
- **貝氏推論**：階層式擬合把[機率方法](../../../theory/paradigms/probabilistic/index.md)中的工具應用於模型參數。
- **神經影像**：逐試驗的潛在變數在有模型的 fMRI 中被用作迴歸變數。見[神經影像與記錄方法](../../neuroimaging-methods/index.md)。

## 應用

- **群體比較**：研究者比較臨床樣本與對照樣本的學習與決策參數，以檢驗兩者是否不同。
- **有模型的影像分析**：由擬合模型估計的預測誤差，與每個試驗的腦部活動相關。

## 開放問題

- **穩定性。**擬合出的參數在不同時段是否保持一致，它們能否預測症狀或治療反應？
- **模型選擇。**對於某種疾病，哪一個候選模型最合適？結論在多大程度上取決於這個選擇？
- **小樣本。**當資料有限時，群體層級先驗的選擇會如何改變結論？

## 參考文獻

### 開創性論文

- Ahn, W.-Y., Haines, N. & Zhang, L.（2017）。Revealing Neurocomputational Mechanisms of Reinforcement Learning and Decision-Making With the hBayesDM Package。*Computational Psychiatry*, 1, 24。https://doi.org/10.1162/cpsy_a_00002 — 介紹 hBayesDM，一個以階層式貝氏方法擬合強化學習與決策模型的 R 套件，並提供模型比較與潛在變數輸出。
- Gershman, S. J.（2016）。Empirical priors for reinforcement learning models。*Journal of Mathematical Psychology*, 71, 1–6。https://doi.org/10.1016/j.jmp.2016.01.006 — 介紹適用於強化學習模型的經驗先驗，即從資料設定的先驗。

### 綜述與教科書

- Wilson, R. C. & Collins, A. G.（2019）。Ten simple rules for the computational modeling of behavioral data。*eLife*, 8, e49547。https://doi.org/10.7554/eLife.49547 — 一份適合初學者的指南，說明如何把計算模型與行為資料連結起來，並提出十條使結論有意義的規則。
- Maia, T. V. & Frank, M. J.（2011）。From reinforcement learning models to psychiatric and neurological disorders。*Nature Neuroscience*, 14(2), 154–162。https://doi.org/10.1038/nn.2723 — 回顧強化學習模型如何描述精神與神經疾病中的行為。
- Huys, Q. J. M., Maia, T. V. & Frank, M. J.（2016）。Computational psychiatry as a bridge from neuroscience to clinical applications。*Nature Neuroscience*, 19(3), 404–413。https://doi.org/10.1038/nn.4238 — 區分資料驅動與理論驅動的計算精神醫學方法，並回顧兩者的臨床應用。
