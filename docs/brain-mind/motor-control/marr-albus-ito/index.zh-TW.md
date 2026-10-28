---
translation_reviewed: 2026-10-28
tags:
- motor control
- cerebellum
- supervised learning
- neuroscience
aliases:
  - 馬爾—阿爾布斯—伊藤小腦學習理論
  - 小腦監督式學習
  - Marr–Albus–Ito theory
  - Cerebellar supervised learning
  - Marr-Albus-Ito
---

# 小腦監督式學習（Marr、Albus 與 Ito）

Marr–Albus–Ito 理論主張，小腦皮質是以監督式學習者的方式學習運動技能。攀爬纖維的輸入充當教導訊號，並改變浦肯野細胞對平行纖維輸入模式的反應。此理論把特定的迴路與特定的學習規則連結起來，是以學習演算法來解釋神經迴路的最清楚範例之一。

本頁屬於[運動控制與小腦](../index.md)。它詳細說明一種方法。學習者由教師提供指導的一般範式，見[監督式學習](../../../theory/paradigms/supervised/index.md)。

## 概述

小腦擁有大腦大部分的神經元（見[神經科學基礎](../../neuroscience/index.md)），但損傷它通常會損害協調與動作調整，而不是造成癱瘓。Marr–Albus–Ito 理論要問的是，小腦計算什麼，以及它的連結如何支持學習。

## 問題

神經迴路如何能在只偶爾得到誤差回饋的情況下，學會依情境產生正確的運動輸出？小腦迴路具有高度結構化的架構：顆粒細胞數量龐大，而每個浦肯野細胞只有一個輸出。問題在於這個結構計算什麼，以及它的突觸如何改變。

## 核心想法

Marr 於 1969 年提出，小腦皮質學習運動技能。他描述了兩種輸入—輸出關係，一種用於學習動作，另一種用於維持姿勢與平衡。在他的說法中，下橄欖核送出一個代表基本動作的訊號，攀爬纖維把它傳到相對應的浦肯野細胞。浦肯野細胞也透過苔狀纖維路徑與顆粒細胞，接觸到該動作發生時的情境。情境與攀爬纖維活動的反覆配對，使浦肯野細胞之後僅憑情境就能啟動該動作。

Albus（1971）發展了一個相關的模型。其核心想法是，攀爬纖維訊號充當誤差訊號，因此小腦會調整其輸出以降低誤差。依此觀點，小腦是一台由教師訓練的學習機器，這正是「監督式」在此處的意思。

Ito 的貢獻來自實驗。他對小腦皮質的研究發現，當平行纖維與浦肯野細胞之間的突觸與攀爬纖維輸入同時活動時，會發生一種突觸改變，即長期抑制（long-term depression）（見 Ito，2006 的回顧）。這為誤差驅動的權重改變提供了生物學機制，也把理論與可測量的突觸連結起來。Ito（2008）進一步主張，小腦學習的是身體與外在世界的內部模型，這是與[內部前向模型](../internal-forward-models/index.md)的連結。

## 方程式與演算法

這一類模型常見的簡化形式，把浦肯野細胞視為平行纖維活動的加權和：

\(y = \sum_i w_i x_i\)

其中 \(x_i\) 是第 \(i\) 條平行纖維的活動，\(w_i\) 是其突觸權重，\(y\) 是浦肯野細胞的輸出。學習會依攀爬纖維所攜帶的誤差訊號 \(e\) 與該突觸的活動，調整每個權重：

\(\Delta w_i = -\eta \, e \, x_i\)

其中 \(\eta\) 是學習率。這是監督式學習中感知器（perceptron）式的 delta 規則。它是簡化模型：原論文並未以這種形式陳述，精確的生物學規則目前仍有爭議。

## 結果

Marr 與 Albus 的論文都是理論性的。它們主張，具備假設連結性的迴路能以所述方式學習輸入—輸出的對應，並認為小腦符合此理論。實驗支持來自後來的研究，尤其是 Ito 對長期抑制的研究（見 Ito，2006 的回顧），它提供了此理論所需突觸改變的證據。

## 限制

- **原始理論先於測量。** Marr 與 Albus 的理論是在突觸改變被測量之前提出的。Ito 在平行纖維與浦肯野細胞突觸上發現了抑制，確定了改變的方向，而這在理論中並未由資料決定。
- **教導訊號尚未定論。** 把攀爬纖維視為誤差訊號是一種強烈的詮釋。它在不同任務中的確切內容仍在研究中。
- **模型是簡化的。** 它未納入深部小腦核、中間神經元以及塑造輸出的諸多連結。後續研究已把這些加入圖景中。
- **運動學習並非全部。** 小腦也與計時及部分認知功能有關，運動理論本身無法解釋這些（Ito，2008）。

## 連結

- **內部模型。** Ito 後期的觀點是小腦學習內部模型，這把此理論與前向預測連結起來。見[內部前向模型](../internal-forward-models/index.md)。
- **最優控制。** 小腦是否學習最優控制所預測的回饋增益，是一個開放的假設；見[最優回饋控制](../optimal-feedback-control/index.md)。
- **監督式學習。** 此理論是監督式學習的生物學實例，也就是由教師提供目標的範式。見[監督式學習](../../../theory/paradigms/supervised/index.md)。
- **分工。** Doya（1999）提出小腦、基底核與皮質分別實現監督式、強化式與非監督式學習。小腦所負責的是監督式的部分。更廣泛的程序性學習見[記憶與學習的神經機制](../../memory-learning/index.md)。

## 應用

- **機器人控制。** Albus（1975）提出小腦模型關節控制器（CMAC），這是一種以查表為基礎的函數近似器，用於操作器控制。它把小腦中稀疏、擴展編碼的概念應用到工程控制。見[機器人](../../../applications/robotics/index.md)。
- **神經網路設計。** 把擴展的輸入編碼與誤差驅動的權重改變配對，在 AI 學習系統中重複出現，包括上述類似感知器的模型。見[NeuroAI：大腦與 AI 的雙向啟發](../../neuroai/index.md)。

## 開放問題

- **教導訊號總是代表誤差嗎？** 有些研究顯示，攀爬纖維的活動所攜帶的資訊不只是單純的誤差。
- **學習還發生在哪裡？** 此理論把學習置於浦肯野細胞的突觸，但可塑性也可能發生在小腦的其他位置。

## 參考文獻

### 開創性論文

- Marr, D. (1969). A theory of cerebellar cortex. *Journal of Physiology*. https://doi.org/10.1113/jphysiol.1969.sp008820 — 提出小腦皮質學習運動技能，下橄欖核傳來的攀爬纖維輸入是教導訊號。
- Albus, J. S. (1971). A theory of cerebellar function. *Mathematical Biosciences*. https://doi.org/10.1016/0025-5564(71)90051-4 — 發展小腦學習模型，其中攀爬纖維訊號引導浦肯野細胞輸出的變化。
- Albus, J. S. (1975). A new approach to manipulator control: the cerebellar model articulation controller (CMAC). *Journal of Dynamic Systems, Measurement, and Control*. https://doi.org/10.1115/1.3426922 — 把小腦模型應用於機器人操作器控制。

### 綜述與回顧

- Ito, M. (2006). Cerebellar circuitry as a neuronal machine. *Progress in Neurobiology*. https://doi.org/10.1016/j.pneurobio.2006.02.006 — 回顧小腦皮質的迴路，以及支持其學習的突觸可塑性。
- Ito, M. (2008). Control of mental activities by internal models in the cerebellum. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2332 — 主張小腦學習內部模型，包括非運動功能的模型。
- Doya, K. (1999). What are the computations of the cerebellum, the basal ganglia and the cerebral cortex? *Neural Networks*. https://doi.org/10.1016/S0893-6080(99)00046-5 — 提出小腦、基底核與皮質的分工：分別為監督式、強化式與非監督式學習者。
