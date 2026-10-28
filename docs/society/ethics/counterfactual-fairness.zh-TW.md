---
status: complete
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - causal inference
  - counterfactuals
aliases:
  - 反事實公平
  - Counterfactual fairness
---

# 反事實公平

!!! info "屬於公平性定義"
    本方法頁屬於[公平性定義與不可能性結果](fairness-definitions.md)。它詳細說明此準則；概述頁則比較各個準則。

反事實公平詢問：若某個人屬於另一個人口群體，決定是否會相同。它運用因果推理，因此需要一個模型來描述受保護屬性如何影響其他變數。Kusner、Loftus、Russell 與 Silva（2017）運用因果推論的工具提出了此準則。

## 問題

群體準則比較的是統計量，它們無法指出哪些特徵承載了群體身分的影響。單純把受保護屬性從輸入中移除也無法解決問題，因為其他特徵可能成為它的代理變數。問題是為個人的決定定義公平，並把受保護屬性的效果與結果的其他成因區分開來。

## 核心想法

建立一個因果模型，描述受保護屬性如何影響其他變數。若在給定個人已觀察資料的條件下，預測結果的分布不因屬性保持原值或在因果模型中被設為另一個值而改變，則此預測器具有反事實公平。論文的一個關鍵引理是：若預測器只依賴因果圖中不屬於受保護屬性後代的變數，則它具有反事實公平。因此此準則既取決於資料，也取決於因果模型。

## 公式

以受保護屬性 \(A\)，若對實際值 \(a\) 與反事實值 \(a'\)，預測器 \(\hat{Y}\) 滿足

\[
\Pr\bigl[\hat{Y}_{A \leftarrow a}(U) = y \mid X = x, A = a\bigr] = \Pr\bigl[\hat{Y}_{A \leftarrow a'}(U) = y \mid X = x, A = a\bigr]
\]

則具有反事實公平。其中 \(U\) 表示因果模型中未觀察到的背景變數，\(\hat{Y}_{A \leftarrow a}\) 是在 \(A\) 被設為 \(a\) 的世界中的預測。

## 結果

Kusner 等人（2017）在一項由法學院招生委員會（Law School Admission Council）調查的資料上，建立法學院成績預測模型，資料涵蓋 163 所學校、21,790 名學生，變數包括 LSAT、GPA 與第一年平均成績。各模型的均方根誤差（RMSE）如下：

| 模型 | RMSE |
|---|---|
| 完整模型（使用種族、性別與其他所有變數） | 0.873 |
| 無感知模型（移除受保護屬性） | 0.894 |
| Fair K（反事實公平，第二層） | 0.929 |
| Fair Add（反事實公平，第三層） | 0.918 |

作者寫道：「為了確保反事實公平的預測，我們必須犧牲少量準確率。」完整模型對除性別以外的每個受保護屬性都不具反事實公平；論文將性別的結果歸因於性別與 GPA、LSAT 之間非常微弱的因果關係，而非歸因於此方法。論文也給出三層因果假設：第一層只使用可觀察、且不屬於該屬性後代的變數；第二層假設存在潛在背景變數；第三層假設一個具有加性誤差項的確定性模型。

## 限制

- **因果模型。** 此準則需要以因果圖作為輸入。作者指出，反事實主張「一律需要強假設」，而且即使有所有變數的介入資料，這些假設通常也無法被檢驗。
- **未觀察變數。** 反事實預測依賴未被觀察到的背景變數，必須由模型加以推斷。
- **合成資料的評估。** 實驗假設真實模型與所設定的模型一致，因此未測試對模型設定錯誤的穩健性。
- **第一層通常不實用。** 一般而言，可觀察變數中不屬於受保護屬性後代的很少。
- **是個體層級的準則，而非平均效果的準則。** 平均效果為零可能掩蓋方向相反的個別效果，它也不保證反事實公平。

## 參考文獻

### 開創性論文

- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). Counterfactual Fairness. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1703.06856 — 定義反事實公平，並以因果推論為基礎提出框架，附有法學院案例研究。
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*, 214–226. https://doi.org/10.1145/2090236.2090255 — 反事實公平常與之對照的個體層級準則。
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — 群體準則，因果方法即是與之對照。

### 綜述與教科書

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — 綜述機器學習中偏誤的來源，以及用來衡量偏誤的公平性定義。
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — 可免費線上閱讀的教科書，涵蓋公平性定義及其假設。
