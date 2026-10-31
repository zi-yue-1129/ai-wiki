---
translation_reviewed: 2026-10-28
---

# 循環學習率

循環學習率（CLR）讓學習率在較低與較高的上下界之間反覆變動，而不是單調下降。Smith（2017）提出此方法，並以一段學習率線性增加的短測試找出上下界。上層總覽為[學習率排程與預熱](learning-rate-schedules.zh-TW.md)。

## 概述

多數排程都假設學習率應隨時間只降不升。Smith 認為，較大的學習率能讓最佳化器更快越過鞍點附近的平坦區域，而較小的學習率則讓它穩定落在極小值。在兩者之間循環，可以同時兼顧，且不必事先決定何時降低學習率。

## 問題

論文稱學習率是深度網路「最重要的超參數」。要找到好的固定學習率或衰減排程，通常需要許多次訓練。Smith 想知道，能否用一個簡單又便宜的規則找出可用的學習率範圍，然後在範圍內循環。

## 核心概念

以學習率範圍測試估計兩個上下界 \(\eta_{\min}\) 與 \(\eta_{\max}\)：在數個 epoch 中讓學習率線性增加，並觀察準確率。接著，在其餘的訓練中讓學習率在這兩個界限之間循環。

### 動態排程示意

<div style="max-width:640px;width:100%" role="group" aria-label="學習率排程動畫">
<div style="width:100%">
<img src="../../assets/concept-animations/clr-triangular2-still.svg" data-motion-src="../../assets/concept-animations/clr-triangular2-motion.svg" style="display:block;width:100%;height:auto" alt="Triangular2 學習率排程的三個週期，每個週期的振幅依序減半。">
</div>
</div>

*AI Wiki 原創動畫，CC BY-SA 4.0。*

移動標記沿著三個等長三角週期運行，每輪先線性上升再線性下降，下一輪的振幅減半，而下界固定。圖中數值為正規化示意值，不是模型實測學習率或準確率。

從圖中的三個峰值可直接看出 triangular2 的振幅包絡：相對於固定下界的增量，在第 1–3 輪依序為 \(1,\;1/2,\;1/4\)。一般而言，若循環索引 \(k\) 從零開始，峰值為 \(\eta_{\min}+(\eta_{\max}-\eta_{\min})/2^k\)。這是排程示意，不是實際訓練紀錄。

## 演算法

**範圍測試。** 訓練數個 epoch，同時讓學習率從很小的值線性增加到很大的值，並繪製準確率與學習率的關係。下界是準確率開始上升之處；上界是準確率增長趨緩、變得不穩定，或開始下降之處。論文建議將下界設為上界的三分之一或四分之一。論文中，CIFAR-10 的測試為 8 個 epoch，GoogLeNet 為 4 個 epoch。

**循環策略。** 令步長 \(s\)（以迭代次數計），\(t\) 為目前的迭代次數。*三角*策略為

\[
\mathrm{cycle} = \left\lfloor 1 + \frac{t}{2s} \right\rfloor,\qquad x = \left|\frac{t}{s} - 2\,\mathrm{cycle} + 1\right|,\qquad \eta_t = \eta_{\min} + (\eta_{\max} - \eta_{\min})\max(0,\, 1 - x)
\]

學習率因此每 \(2s\) 次迭代線性上升並下降一次。*三角2*策略在每個循環後將振幅減半。*exp_range* 策略則讓上下界隨時間指數式縮小。論文指出，視窗形狀的選擇影響不大，因此採用最簡單的三角視窗。

**步長。** 論文發現結果對循環長度「相當穩健」，並建議步長為每個 epoch 迭代次數的 2 至 10 倍。對於每個 epoch 有 500 次迭代的 CIFAR-10，步長設為 2,000（即 4,000 次迭代的循環）。對於 ImageNet 上的 AlexNet 與 GoogLeNet，步長則為 30,000 次迭代。

## 結果

- **CIFAR-10，Caffe。** 固定學習率在 70,000 次迭代時達到 81.4% 準確率。三角2策略在 25,000 次迭代時即達到 81.4%。
- **五次執行的平均。** 以 ResNet、Stochastic Depth 與 DenseNet 網路，在 CIFAR-10 與 CIFAR-100 上使用 CLR 的準確率分別為 93.6/72.5、94.5/75.4 與 94.9/75.9。固定學習率的基準在 CIFAR-10 上為 91.8 至 94.6，在 CIFAR-100 上為 71.2 至 75.3。
- **ImageNet。** AlexNet 以固定學習率在 400,000 次迭代時達 58.0%，三角2策略在相同次數時達 58.4%。GoogLeNet 以固定學習率在 420,000 次迭代時達 63.0%，三角2策略在相同次數時達 64.4%。

## 限制

- **上下界依架構而定。** 範圍測試需針對每種架構與資料集執行，因此新模型必須重新估計上下界。
- **停止時機。** 論文建議在循環結束時停止訓練，使學習率處於低點。若在峰值停止，模型可能仍帶有較大的雜訊。
- **取代既有排程。** 論文建議，將每個固定學習率階段替換為至少三個循環，四個或更多更好。因此循環的次數同時也是一項成本決策。
- **當時的基準。** 比較對象是 2015 至 2016 年的網路，採用固定學習率與階梯衰減的訓練。論文沒有測試 Transformer，也沒有測試之後普及的預熱排程。

## 變體與相關排程

- **三角、三角2與 exp_range** 是論文中的三種策略，差別在於振幅在各循環間如何變化。
- **[附暖重啟的餘弦退火](cosine-annealing-warm-restarts.zh-TW.md)**同樣會重啟學習率，但它在每一輪內沿餘弦曲線下降，且輪次長度會隨時間增加。

## 與其他頁面的連結

- [學習率排程與預熱](learning-rate-schedules.zh-TW.md)是將此方法與其他方法放在一起比較的總覽。
- [漸進式預熱](gradual-warm-up.zh-TW.md)同樣使用線性上升的學習率，而本方法中的範圍測試扮演類似的角色。
- [損失曲面](theory-and-landscapes.zh-TW.md)說明了為何較大的學習率可能幫助最佳化器通過平坦區域與鞍點。

## 開放問題

- 循環排程何時會優於調校良好的衰減排程，何時不會？
- 對於給定的預算，應如何選擇循環長度？
- 循環學習率是否對[Adam](adaptive/adam.zh-TW.md)等自適應方法也有幫助，而這些方法本來就會調整每個參數的步長？

## 參考文獻

### 開創性論文

- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV 2017, pp. 464–472. doi:[10.1109/WACV.2017.58](https://doi.org/10.1109/WACV.2017.58) — 提出在以線性範圍測試找到的上下界之間循環學習率。預印本：https://arxiv.org/abs/1506.01186
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR 2017. https://arxiv.org/abs/1608.03983 — 週期性重啟，每輪內為餘弦衰減，用於與循環學習率比較。
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — 漸進式預熱與線性縮放規則，是訓練開頭改變學習率的另一種方式。
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS 2017. https://arxiv.org/abs/1706.03762 — 線性預熱後接平方根倒數衰減，是循環學習率常被拿來比較的單調排程。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review, 60(2), 223–311. doi:[10.1137/16M1080173](https://doi.org/10.1137/16M1080173) — 隨機梯度方法的步長選擇綜述，是範圍測試的理論背景。
