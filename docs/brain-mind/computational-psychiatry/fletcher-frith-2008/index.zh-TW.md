---
translation_reviewed: 2026-10-28
---

# Fletcher and Frith 2008（陽性症狀的貝氏解釋）

Fletcher 與 Frith（2008）主張，精神分裂症的陽性症狀，例如妄想與幻覺，可以用一種知覺的貝氏解釋來說明：其中預測誤差被不正常地加權。本頁是[計算精神醫學](../index.md)的子頁。上層頁面提供概述，本頁說明這套解釋、其方程式以及證據的限制。

## 概述

陽性症狀是在正常功能之上額外出現的經驗或信念。妄想是一種固執的信念，即使有相反的證據仍然堅持。幻覺則是沒有外在來源的知覺。Fletcher 與 Frith 問的是：正常的知覺系統出現哪一種改變，會產生這些經驗。他們的答案借用了一個想法：知覺結合期待與感覺輸入，而大腦會在兩者不一致時發出訊號。

這套解釋建立在大腦皮質的[預測編碼](../../predictive-coding/index.md)觀點之上。如果預測誤差訊號異常，期待與證據之間的平衡便會改變。原本應被修正的信念可能持續存在，而某些經驗也可能看似來自外部，即使並非如此。同一框架也與報告獎勵預測誤差的多巴胺訊號相連，見[多巴胺的獎勵預測誤差](../../neuroscience/dopamine-reward-prediction-error/index.md)。

## 核心概念

- **先驗**：新證據到來之前，系統所持有的期待。在這套解釋中，先驗可以是關於世界的信念，也可以是關於自身的信念。
- **概似**：感覺證據與各個假設的吻合程度。
- **預測誤差**：預測與實際到來的輸入之間的落差。它驅動信念的修正。
- **精確度**：賦予預測誤差的權重。精確度高，表示該誤差對信念有大的影響；精確度低，則表示該誤差大多被忽略。
- **異常顯著性**：Kapur（2003）提出的相關概念，主張精神病經驗反映一種錯置的事件重要性感受。

## 運作方式

貝氏定理描述了在證據 $e$ 出現後，關於假設 $h$ 的信念應如何改變：

$$p(h \mid e) \propto p(e \mid h)\, p(h).$$

在預測編碼模型中，信念依預測誤差 $\varepsilon = e - \hat{e}$ 更新，其中 $\hat{e}$ 為預測，並以精確度 $\pi$ 加權。更新量大致與 $\pi\,\varepsilon$ 成正比。

這套解釋可以分四個步驟來說明。

1. 系統依其目前的信念產生一個預測。
2. 把預測與到來的感覺輸入比較，並算出誤差。
3. 誤差以其精確度加權，用來更新信念。
4. 若誤差被不正常地加權，信念的修正就會不足，使先驗在面對證據時仍然持續存在；或者，系統自己的預測被當作外部輸入。

Fletcher 與 Frith 把第四步應用於妄想與幻覺。他們主張，過強的先驗，或對誤差的不正常加權，都可能產生這兩類經驗。

## 結果

這篇論文是理論性回顧，因此沒有單一的基準結果。它主張，來自精神病患者的行為與神經影像發現，以及健康受試者在操弄下的發現，都與這套解釋相符。本頁以文字描述這項論證，不引述具體數字。

## 限制

- 這套解釋是一個框架，而非擬合出的模型，它可以容納許多發現。這種彈性使它較難被檢驗。
- 從先驗與精確度到特定症狀之間的對應，仍有爭議。
- 這套解釋主要處理陽性症狀，對陰性症狀與認知變化的涵蓋不夠細緻。
- 它與多巴胺的連結是一項假說，證據好壞不一。

## 開放問題

- 異常是在於先驗、在於精確度，還是兩者皆是？不同的答案會預測不同的實驗結果。
- 同樣的機制是否也能解釋沒有精神病的人身上的妄想？
- 哪些神經調節物質實現精確度？它們與多巴胺訊號有何關係？
- 異常的預測誤差是症狀的成因，還是症狀的結果？Sterzer et al.（2018）更新了這套解釋並回顧了證據。

## 參考文獻

### 開創性論文

- Fletcher, P. C. & Frith, C. D. (2008). Perceiving is believing: a Bayesian approach to explaining the positive symptoms of schizophrenia. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2536 — 主張陽性症狀可以由先驗信念與感覺預測誤差的異常加權來解釋。
- Kapur, S. (2003). Psychosis as a state of aberrant salience: a framework linking biology, phenomenology, and pharmacology in schizophrenia. *American Journal of Psychiatry*. https://doi.org/10.1176/appi.ajp.160.1.13 — 一個有影響力的框架，以異常顯著性解釋精神病症狀，並連結生物學、經驗與藥理作用。
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A neural substrate of prediction and reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — 顯示多巴胺神經元的活動反映了時序差分學習所用的獎勵預測誤差。

### 綜述與教科書

- Sterzer, P. et al. (2018). The Predictive Coding Account of Psychosis. *Biological Psychiatry*. https://doi.org/10.1016/j.biopsych.2018.05.015 — 回顧精神病症狀的預測編碼解釋及其證據。
- Adams, R. A., Huys, Q. J. M. & Roiser, J. P. (2015). Computational Psychiatry: towards a mathematically informed understanding of mental illness. *Journal of Neurology, Neurosurgery & Psychiatry*. https://doi.org/10.1136/jnnp-2015-310737 — 回顧形式模型如何有助於理解精神疾病，包括貝氏解釋。
- Montague, P. R., Dolan, R. J., Friston, K. J. & Dayan, P. (2012). Computational psychiatry. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2011.11.018 — 回顧文獻，把計算精神醫學界定為以學習與決策模型理解精神疾病的研究取向。
