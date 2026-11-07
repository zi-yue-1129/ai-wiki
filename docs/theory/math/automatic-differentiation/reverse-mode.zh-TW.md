---
status: draft
last_reviewed: 2026-11-07
translation_reviewed: 2026-11-07
related:
  - theory/math/automatic-differentiation
  - theory/deep-learning
tags:
  - reverse-mode differentiation
  - backpropagation
  - adjoint
aliases:
  - 反向模式自動微分
  - Reverse-mode automatic differentiation
  - Reverse mode
---

# 反向模式微分

反向模式微分在一次前向執行並記錄中間值之後，只需對程式做一次反向掃描，就能計算純量輸出對所有輸入的梯度。當輸出是純量、輸入數量很多時（例如神經網路的損失與其參數），這比對每個輸入各算一次方向導數便宜得多。反向傳播就是把這個方法套用到神經網路上。

## 概觀

[自動微分章節](index.zh-TW.md)描述了兩種模式。本頁說明反向模式，也就是訓練大型模型所用的模式。它可以理解為鏈式法則從輸出往輸入套用，並為每個中間值攜帶一個敏感度。

## 問題

假設一個函數 $f: \mathbb{R}^n \to \mathbb{R}$ 把數百萬個參數映射到一個損失。梯度有 $n$ 個分量。前向模式每次只能算出一個分量，因此完整梯度需要大約 $n$ 次掃描。訓練模型時，每次更新的時間就會與參數數量成正比，這在實務上不可行。

## 核心想法

反向模式分為兩個階段。前向階段執行程式，並把每個中間值 $v_i$ 儲存在計算圖中。反向階段從輸出的伴隨值 $\bar{y} = 1$ 開始，沿圖往回走。在每個節點，它利用該運算的局部導數，把伴隨值傳給輸入；若某個值被多次使用，則累加各項貢獻：

$$\bar{v}_j = \sum_{i \in \text{children}(j)} \bar{v}_i \,\frac{\partial v_i}{\partial v_j}$$

每個伴隨值都是一個向量雅可比積。重點在於，所有輸入的梯度只靠一次反向掃描就能得到，而其成本是計算函數本身的一個小常數倍，這個結果稱為廉價梯度原理 [(Griewank and Walther, 2008)](https://doi.org/10.1137/1.9780898717761)。

![反向模式自動微分的四階段動畫：從純量輸出設定伴隨值、反向傳遞敏感度，並在共用輸入累加梯度。](../../../assets/concept-animations/reverse-ad-vjp-motion.svg)

*原創四階段教學動畫，CC BY-SA 4.0。* 使用相同的示意程式 $a=xy$、$b=x+x$、$z=a+b$ 與 $(x,y)=(2,3)$。先計算並保留中間值，再從 $\bar{z}=1$ 反向傳播，得到 $\bar{a}=\bar{b}=1$。兩條回到 $x$ 的路徑分別貢獻 $y\bar{a}=3$ 與 $2\bar{b}=2$，**必須累加**成 $\bar{x}=5$；另一個輸入得到 $\bar{y}=x\bar{a}=2$。因此一次反向掃描即可得到純量輸出的 $\nabla f=(5,2)$。這是手算示意，非模型梯度實測。MkDocs 網站提供播放／暫停及減少動態效果的回退顯示；[GitHub 可直接閱讀的靜態最終狀態](../../../assets/concept-animations/reverse-ad-vjp-still.svg)。

## 方程式

對於向量值運算 $y = g(x)$，其雅可比為 $J$，伴隨規則把輸出敏感度 $\bar{y}$ 映射為輸入敏感度，而不需要顯式形成 $J$：

$$\bar{x} = J^{\top} \bar{y}$$

對於層 $y = Wx + b$ 與損失 $L$，這給出 $\bar{W} = \bar{y}\, x^{\top}$ 與 $\bar{x} = W^{\top} \bar{y}$。沿圖串接這些規則，就正是反向傳播 [(Rumelhart et al., 1986)](https://doi.org/10.1038/323533a0)。

## 執行模型：具體的反向掃描

考慮 $u=xy$、$v=x+x$、$L=u+v$，在 $x=2$、$y=3$ 時，前向計算得到 $u=6$、$v=4$、$L=10$。設定 $\\bar L=1$，加法節點把敏感度各傳給 $u$ 與 $v$；乘法節點對 $x$ 貢獻 $y\\bar u=3$，對 $y$ 貢獻 $x\\bar u=2$；$v$ 中兩次使用 $x$ 再各貢獻一個單位。因此累積得到 $\\bar x=5$、$\\bar y=2$。

這也說明計算圖不一定是樹：同一個輸入可能被多個下游運算使用。反向實作必須**累加**所有路徑的 cotangent，而不是覆寫前一次貢獻。對張量節點則以局部向量－雅可比積（VJP）取代純量偏導數。若輸出為向量，反向傳播的初始 cotangent 也可以是指定向量，而不一定是純量一。

Tape-based 引擎通常為每個可微運算記錄輸入、反向所需的前向值與 pullback 函式，再以反向拓樸順序執行 pullback 並累加輸入的 cotangent。這是 Baydin 等人所述的鏈式法則與 PyTorch 等命令式框架之間的實作橋梁。[^1][^2]

```text
values, tape = evaluate_forward(program, inputs)
cotangent[loss] = 1
for node in reverse_topological_order(tape):
    if node has no accumulated cotangent: continue
    contributions = node.pullback(cotangent[node], saved_values[node])
    for input, contribution in contributions:
        cotangent[input] += contribution
return cotangent[inputs]
```

這段虛擬碼省略了記憶體配置、張量別名、原地修改檢查、broadcast 維度縮減與分散式執行。正式系統不能忽略這些問題；例如 broadcast 加法的梯度必須沿擴張維度做加總，才能還原輸入張量的形狀。

## 複雜度與記憶體成本

令 $C_f$ 為可微純量輸出程式的前向計算成本，$n$ 為純量輸入數。若前向模式逐一使用基底方向求出完整梯度，工作量一般隨 $nC_f$ 成長；反向模式則在一次前向與一次反向遍歷中完成。當基本運算的 pullback 成本低時，梯度計算的工作量通常是 $C_f$ 的小常數倍。但這是**運算量**層級的比較，不保證特定框架的實際執行時間倍率；記憶體頻寬、控制流、自訂運算與裝置同步都會影響效能。[^1][^3]

反向模式的主要代價之一是保存前向中間值。Pullback 可能需要原始輸入、輸出、遮罩或其他 activation。完整保存時，即使最終梯度很小，尖峰記憶體仍可能隨展開後的計算長度成長。Activation checkpointing 只保存部分邊界，反向時重新計算其餘中間值，以額外運算換取記憶體；最佳效果取決於圖結構與重算排程。[^3]

對 $f: \\mathbb{R}^n\\to\\mathbb{R}^m$，一次反向掃描計算的是指定 $v\\in\\mathbb{R}^m$ 的 $J_f(x)^\\top v$。若要建立**完整**雅可比矩陣，可能需要最多 $m$ 次反向掃描。前向模式則對指定 $u$ 計算 $J_f(x)u$。選擇哪種模式應取決於目標導數的形狀，而非只看程式是否為神經網路。[^1]

## 可微分契約與常見失敗模式

實際程式可能包含不可微、不連續或條件數很差的運算。例如 ReLU 的折點沒有唯一的古典導數，框架會採用特定導數慣例；整數索引、argmax 與離散取樣的決策本身，也無法直接透過一般反向模式得到有用的梯度。替代梯度與連續鬆弛是對最佳化問題的建模調整，不能視為原始離散運算的精確微分。

原地修改可能破壞 pullback 所需的儲存值；detach 會刻意切斷梯度路徑；誤把參數當常數或把中間結果轉為不可微表示，也可能在沒有語法錯誤的情況下造成梯度缺失。訓練流程應確認預期參數確實收到有限梯度，並區分「沒有梯度」與「梯度數值為零」。[^2]

在小型、平滑的測試函數上，可用不同步長的中央有限差分檢查反向結果，或比較方向導數 $u^\\top\\nabla f(x)$ 與沿 $u$ 的擾動結果。不過有限差分只是診斷工具，會受截斷誤差與浮點抵消影響。測試應避開不可微點、隨機非決定性與具有狀態副作用的運算。[^1]

## Key methods

- [反向模式微分](reverse-mode.zh-TW.md)：本頁說明的 tape-based adjoint 累加，適用於純量目標。
- [前向模式微分](forward-mode.zh-TW.md)：沿前向運算傳播 tangent，適合少量輸入方向。

## 工程解讀

一般神經網路訓練步驟並不會自動微分整個訓練程序。典型流程只對目前參數計算目前 loss 的梯度，之後由 optimizer 消耗梯度並更新參數。若在 meta-learning 等情境需要**穿過 optimizer 更新步驟**求導，就必須保留或重建更新計算，並明確決定 optimizer state 如何表示。這會改變高階梯度與記憶體成本。

反向模式提供的是局部且可組合的保證：只要實際執行的基本運算具有正確導數規則，且程式符合可微分契約，反向累加便實作了該計算路徑的鏈式法則。它本身不保證損失函數適當、梯度數值尺度穩定，或最佳化一定收斂。[^1][^4]

## 結果

反向模式的梯度在浮點捨入之內是精確的，這與有限差分不同，後者需要在截斷誤差與捨入誤差之間取捨。Baydin 等人的綜述檢視了反向模式在機器學習中的用法，並將其與前向模式及符號微分相比較 [(Baydin et al., 2018)](https://arxiv.org/abs/1502.05767)。具體的執行時間比較見該綜述及其所引用的各項工作。

## 限制

- 反向模式必須儲存前向傳播的中間值，因此記憶體隨計算長度成長。對於長序列或深層模型，這可能成為主要成本。
- 檢查點（checkpointing）以記憶體換取重算：部分中間值會被丟棄，並在反向掃描時重新計算。使額外工作最少的排程是一個已知的最佳化問題 [(Griewank and Walther, 2008)](https://doi.org/10.1137/1.9780898717761)。
- 具有依資料而定之分支的控制流，只會沿實際執行的路徑微分。對該路徑而言梯度是正確的，但函數在分支邊界上可能不可微。

## 關聯

反向模式是[反向傳播](../../deep-learning/index.zh-TW.md)背後的機制，而它所產生的梯度驅動訓練中使用的最佳化器。它的對偶，即前向模式，見[前向模式微分](forward-mode.zh-TW.md)。梯度的記號見[符號與記號表](../../../reference/notation/index.zh-TW.md)。

## 應用

訓練任何架構的神經網路、對模擬器進行基於梯度的最佳化，以及在輸出為純量目標的科學計算中進行敏感度分析。

## 開放問題

- 對於無法儲存完整前向傳播的極長序列，反向模式應如何組織？
- 對於具有動態結構與離散選擇的程式，能否有效率地建構圖並微分？

## 參考文獻

### 奠基性論文

- Rumelhart、Hinton 與 Williams，*Learning representations by back-propagating errors*，Nature（1986）。https://doi.org/10.1038/323533a0 — 推廣反向傳播，即套用於分層網路的反向模式。
- Pearlmutter 與 Siskind，*Reverse-mode AD in a functional framework: Lambda the ultimate backpropagator*，ACM Transactions on Programming Languages and Systems（2008）。https://doi.org/10.1145/1330017.1330018 — 在函數式設定中，把反向模式視為程式變換。

### 綜述與教科書

- Baydin、Pearlmutter、Radul 與 Siskind，*Automatic differentiation in machine learning: a survey*，Journal of Machine Learning Research（2018）。https://arxiv.org/abs/1502.05767 — 涵蓋兩種模式及其在機器學習中應用的綜述。
- Griewank 與 Walther，*Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*，SIAM（2008）。https://doi.org/10.1137/1.9780898717761 — 涵蓋廉價梯度原理與檢查點的標準教科書。
- Goodfellow、Bengio 與 Courville，*Deep Learning*，MIT Press（2016）。https://www.deeplearningbook.org/ — 在訓練神經網路的脈絡下說明反向傳播。

### 文章與文件

- Paszke 等人，*PyTorch: An Imperative Style, High-Performance Deep Learning Library*（2019）。https://arxiv.org/abs/1912.01703 — 說明一個在前向傳播時記錄圖、並以反向方式執行的框架。

[^1]: Baydin 等人（2018），*Automatic differentiation in machine learning: a survey*，連結見參考文獻。
[^2]: Paszke 等人（2019），*PyTorch*，連結見參考文獻。
[^3]: Griewank 與 Walther（2008），*Evaluating Derivatives*，連結見參考文獻。
[^4]: Goodfellow 等人（2016），*Deep Learning*，連結見參考文獻。
