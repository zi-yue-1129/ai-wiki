---
translation_reviewed: 2026-10-28
related:
- brain-mind/predictive-coding
- theory/paradigms/reinforcement-learning
tags:
- computational psychiatry
- psychosis
- prediction error
aliases:
  - 異常預測誤差
  - 精神病的預測誤差
  - 妄想與預測誤差
  - Aberrant prediction error
  - Delusions and prediction error
---

# 精神病中的異常預測誤差（Corlett 等人，2007）

一系列計算研究提出，當大腦的預測誤差訊號（即強化學習中的學習訊號）受到干擾時，妄想信念就可能形成。Corlett 等人（2007）以功能性磁振造影（fMRI），在 12 名有妄想信念的人與 12 名健康對照者身上，測量預測誤差相關的腦部反應，藉此檢驗這個假說。

本頁屬於[計算精神醫學](../index.md)。它描述一個研究假說及其證據，不是診斷測驗，而且研究發現針對的是群體，而非個別病患。

## 概述

學習取決於比較實際發生的事與預期的事，兩者的差異就是更新預期的預測誤差。Corlett 與同事提出，當這個誤差訊號受到干擾時，妄想（即持續存在、即使有反證也不改變的信念）就可能產生，使事件與信念之間形成連結，而這些連結並無證據支持。

## 問題

妄想是對世界的適應不良信念。先前的實驗研究已顯示，預測誤差會驅動信念的形成。待解的問題是：妄想是否因為大腦中的預測誤差歷程本身受到干擾而形成，而這種干擾能否解釋為何有些人比其他人更容易形成妄想。

## 核心想法

Corlett 等人（2007）以聯想的角度來構想這個解釋。當結果與預期不同時，預測誤差通常會更新信念的強度。在有妄想信念的人身上，大腦對這些誤差的反應應與健康參與者不同。作者也主張，注意力受干擾與聯想學習受干擾，屬於同一幅圖像。因此該假說做出一項具體預測：神經層面的預測誤差訊號本身（而不只是行為）應顯得異常，而且其異常程度應與一個人形成妄想的傾向相關。

沿用[以階層式貝氏強化學習模型進行計算表型分析](../computational-phenotyping/index.md)的記號，學習更新為 \(V_{t+1} = V_t + \alpha\,\delta_t\)，其中 \(\delta_t\) 為預測誤差。該假說涉及的是大腦如何表徵更新所依賴的 \(\delta_t\)。

相關的解釋從其他角度處理同一個問題。Fletcher 與 Frith（2009）把陽性症狀描述為信念更新的一種失常，Kapur（2003）則把精神病描述為異常顯著性的狀態。

## 方程式或演算法

此方法是一種實驗設計，而非單一的方程式。其程序如下：

1. 招募一組有妄想信念的人，以及一組健康對照組，並測量妄想傾向。
2. 在掃描儀中進行學習任務，其中結果可能違反預期。
3. 為逐試驗的預測誤差建立模型，並把它們作為 fMRI 分析中的迴歸變數。
4. 比較各組的預測誤差反應，並檢驗該反應是否與所有參與者的妄想信念程度相關。

## 結果

Corlett 等人（2007）研究了 12 名健康參與者與 12 名有妄想信念的人。其摘要報告，病患組的額葉皮質反應顯示預測誤差處理可能受到干擾，正文將其縮小到右側前額葉皮質。在所有參與者中，這種干擾的程度與每個人形成妄想的傾向有顯著關聯，而在病患組中，干擾與妄想嚴重程度相關。作者把此結果解讀為支持一種理論，即異常的預測誤差訊號、受干擾的注意力與聯想學習共同促成妄想信念。

Powers 等人（2017）把這個想法延伸到幻覺。其標題指出，巴夫洛夫式制約會因知覺先驗被過度加權而誘發幻覺，這把幻覺解釋與同一套更新機制連結起來。

## 限制

- **樣本大小。**2007 年的研究比較了 12 名有妄想者與 12 名對照者。小樣本的檢定力有限，因此這些發現需要在更大的樣本中重現。
- **證據有爭議。**Griffiths 等人（2014）重新檢驗妄想形成中，支持錯誤訊號受干擾的行為證據，因此該假說的支持仍有爭議。
- **特異性。**預測誤差的異常可能反映注意力、顯著性或一般的信念歷程，而不只是預測誤差本身。Sterzer 等人（2018）回顧精神病的預測編碼解釋整體。
- **相關性。**有妄想的人身上出現異常訊號，本身並不表示該異常導致了妄想。

## 與其他主題的關聯

- **多巴胺與預測誤差**：動物實驗中的誤差訊號證據，見[多巴胺的獎勵預測誤差](../../neuroscience/dopamine-reward-prediction-error/index.md)。精神病假說則探問，這類訊號在人類身上是否異常。決策方面的連結見[決策、多巴胺與獎勵](../../decision-reward/index.md)。
- **預測編碼**：認為精神病反映預測改變的觀點，見[預測編碼與自由能](../../predictive-coding/index.md)。
- **注意力與顯著性**：異常顯著性的解釋，與[大腦與機器中的注意力](../../attention-brain-machine/index.md)相關。
- **個體差異與影像**：跨人追蹤此訊號與[計算表型分析](../computational-phenotyping/index.md)相關，而 fMRI 測量則見[神經影像與記錄方法](../../neuroimaging-methods/index.md)。

## 應用

- **實驗設計**：以病患組與對照組進行的聯想學習任務，被用來研究信念如何形成與修正。
- **理解幻覺**：Powers 等人的制約範式，能把知覺先驗的效應與感官證據區分開來。
- **臨床研究**：此假說引導機制性研究，但目前還不是臨床測驗。

## 開放問題

- **特異性。**預測誤差的異常是否只出現在精神病中，還是也出現在其他疾病中？
- **時序。**異常是在症狀之前出現，還是隨症狀一起發展？
- **機制。**干擾是發生在誤差訊號本身、注意力，還是誤差所更新的先驗之中？
- **重現性。**這些效應在更大、更多元的樣本中是否成立？

## 參考文獻

### 開創性論文

- Corlett, P. R., Murray, G. K., Honey, G. D., Aitken, M. R. F., Shanks, D. R., Robbins, T. W., Bullmore, E. T., Dickinson, A. & Fletcher, P. C.（2007）。Disrupted prediction-error signal in psychosis: evidence for an associative account of delusions。*Brain*, 130(9), 2387–2400。https://doi.org/10.1093/brain/awm173 — 一項 fMRI 研究，納入 12 名健康參與者與 12 名有妄想信念者，報告病患組的額葉預測誤差反應受到干擾，且與形成妄想的傾向相關。
- Powers, A. R., Mathys, C. & Corlett, P. R.（2017）。Pavlovian conditioning–induced hallucinations result from overweighting of perceptual priors。*Science*, 357(6351), 596–600。https://doi.org/10.1126/science.aan3458 — 報告巴夫洛夫式制約會誘發幻覺，並把此效應歸因於知覺先驗被過度加權。
- Fletcher, P. C. & Frith, C. D.（2009）。Perceiving is believing: a Bayesian approach to explaining the positive symptoms of schizophrenia。*Nature Reviews Neuroscience*, 10(1), 48–58。https://doi.org/10.1038/nrn2536 — 提出以貝氏方式解釋思覺失調症陽性症狀的理論，這是信念更新觀點所依據的基礎。
- Kapur, S.（2003）。Psychosis as a State of Aberrant Salience: A Framework Linking Biology, Phenomenology, and Pharmacology in Schizophrenia。*American Journal of Psychiatry*, 160(1), 13–23。https://doi.org/10.1176/appi.ajp.160.1.13 — 提出異常顯著性作為一個框架，連結思覺失調症的生物學、現象學與藥理學。

### 綜述與教科書

- Sterzer, P. 等人（2018）。The Predictive Coding Account of Psychosis。*Biological Psychiatry*。https://doi.org/10.1016/j.biopsych.2018.05.015 — 回顧精神病中預測編碼異常的證據，以及此一經典解釋所面臨的挑戰。
- Griffiths, O., Langdon, R., Le Pelley, M. E. & Coltheart, M.（2014）。Delusions and prediction error: re-examining the behavioural evidence for disrupted error signalling in delusion formation。*Cognitive Neuropsychiatry*, 19(5), 439–467。https://doi.org/10.1080/13546805.2014.897601 — 重新檢驗妄想形成中異常錯誤訊號的行為證據。
