---
translation_reviewed: 2026-11-02
---

# 投影梯度下降與對抗訓練

投影梯度下降（PGD）是一種迭代攻擊：重複小幅的梯度步伐，並在每步之後把擾動投影回允許的預算之內。對抗訓練則以 PGD 樣本作為訓練資料，Madry 等人（2018）證明這是一種強的防禦。本頁是[對抗樣本與穩健性](index.md)的一部分。

## 概述

單步 FGSM 可能錯過損失最高的區域。PGD 採取多步，並從預算內的隨機點重新開始，因此能找到更強的對抗樣本。Madry 等人（2018）把穩健訓練表述為極小極大問題：對參數取極小，同時對預算內的擾動取最壞情況的損失。

## 關鍵概念

- **投影**：每一步之後，把擾動裁回以乾淨輸入為中心的 \(\epsilon\) 球內。
- **隨機起點**：攻擊從球內的隨機點開始，有助於跳出損失函數的平坦區域。
- **極小極大目標**：\(\min_\theta \mathbb{E}\big[\max_{\|\delta\|\le\epsilon} J(\theta,x+\delta,y)\big]\)。

## 運作方式

從球內隨機的 \(\eta\) 出發，令 \(x^{(0)}=x+\eta\)，PGD 更新為

\[
x^{(t+1)}=\Pi_{\mathcal{B}_\epsilon(x)}\!\Big(x^{(t)}+\alpha\,\mathrm{sign}\big(\nabla_x J(\theta,x^{(t)},y)\big)\Big),
\]

其中 \(\Pi\) 為投影到球上，\(\alpha\) 為步長。對抗訓練在每個小批次上計算這個內層最大化，並以得到的樣本更新參數。此方法成本高，因為每個訓練步需要多次計算梯度。

## 威脅模型與可行集合

擾動範數與半徑是安全性主張的一部分，而不是可任意互換的超參數。典型影像分類設定假設攻擊者能取得模型與標籤，並在指定範數球及合法像素範圍內選擇擾動。\(\ell_\infty\) 預算限制每個座標的最大變動；\(\ell_2\) 預算則限制整體歐氏距離。在某個半徑下測得的穩健性，不能直接推論到另一個半徑、空間變換或改變任務語意的輸入。

對 \(\ell_\infty\) PGD，可以先將每個像素裁切到 \([x_i-\epsilon,x_i+\epsilon]\)，再裁切到合法像素範圍。這等同投影至兩個軸對齊方盒的交集。對 \(\ell_2\) PGD，更新方向與投影不同：可將梯度除以其歐氏範數，而超出半徑的擾動則依比例縮放至長度 \(\epsilon\)。使用梯度符號的更新特別適合 \(\ell_\infty\) 威脅模型，不是適用所有範數的通式。

也必須區分**非目標式攻擊**與**目標式攻擊**。非目標式 PGD 提高真實標籤的損失；目標式 PGD 嘗試增加指定目標類別的可能性，因此在最小化目標標籤損失時，最佳化方向會反轉。攻擊者是否具有查詢權限、能否對前處理微分，也應隨結果一併說明。

## 實作與可重現性

白箱評估應明確將模型設為評估模式，並確保計算輸入梯度時不會意外更新權重。以下為非目標式 \(\ell_\infty\) 版本的演算法示意，而非特定框架的完整程式碼。

```text
對每筆輸入 (x, y)：
    best_loss = -infinity
    重複 R 次隨機重啟：
        delta = 每座標從 uniform(-epsilon, epsilon) 取樣
        delta = clamp(x + delta, 合法範圍) - x
        重複 K 個步驟：
            g = gradient_x(loss(model(x + delta), y))
            delta = delta + alpha * sign(g)
            delta = clamp(delta, -epsilon, epsilon)
            delta = clamp(x + delta, 合法範圍) - x
        保留損失最高且符合限制的候選擾動
    評估 model(x + best_delta)
```

內層最大化通常只得到**近似解**。增加步數 \(K\)、隨機重啟次數，以及選擇合適步長，可能揭露較弱攻擊漏掉的失敗案例，但不構成全域最優的證明。報告應列出 \(\epsilon\)、範數、\(\alpha\)、步數、重啟次數、初始化、前處理、像素尺度，以及是否逐樣本挑選最大損失的候選。若沒有換算，就直接比較以 \([0,1]\) 與 \([0,255]\) 表示的擾動預算，結論會失真。

訓練時，外層最佳化器應根據最終對抗批次更新 \(\theta\)，內層迴圈則更新輸入擾動。常見實作在計算外層梯度時，將找到的擾動視為固定，而非對所有攻擊迭代步驟進行反向傳播。這個差異直接影響記憶體需求，以及 Madry 等人（2018）穩健最佳化基準的重現。

## 評估協定與常見失敗

**乾淨準確率**與**穩健準確率**應在相同的保留測試資料上分開報告。穩健準確率是受允許攻擊後仍正確分類的比例，並且依賴所選威脅模型與攻擊實作。可靠的經驗性評估應檢查不同步長、擾動預算及重啟次數，而不是把單次 PGD 結果視為認證保證。

**梯度遮蔽（gradient masking）**是重要的失敗模式：不可微分的前處理、飽和的活化函數或隨機元件，可能讓天真的梯度攻擊失效，卻沒有真正提升模型穩健性。當攻擊後準確率異常偏高，應檢查損失是否隨迭代增加、梯度量值、隨機性，以及更強或不同類型的攻擊。隨機平滑的認證回答的是另一個問題：在指定 \(\ell_2\) 半徑下提供形式化保證；PGD 測試則是特定攻擊下的經驗證據（Cohen 等人，2019）。

**計算成本**應包含每個訓練小批次的攻擊步數、評估時的重啟次數與實際硬體吞吐量。如果兩種防禦使用不同批次大小、資料管線或總最佳化更新次數，就不是控制良好的比較。還須區分有界擾動穩健性、分布偏移、資料損毀與適應性攻擊；其中一種情境成功不代表其他情境也成功。

## 關聯

PGD 是用於穩健經驗風險最小化內層對手的第一階最佳化程序，其訓練目標與[機器學習](../index.zh-TW.md)相關，單步前身則是 [FGSM](fgsm.zh-TW.md)。評估的核心問題是攻擊是否足夠強，能合理近似內層最大值，而不是分類器是否通過一次任意選擇的擾動測試。

## 變體

- **TRADES** 以兼顧乾淨準確率與攻擊下輸出變化的損失進行訓練，得到不同的準確率與穩健性取捨。
- **免費對抗訓練**重用一次傳遞的梯度，以降低攻擊的成本。
- **快速對抗訓練**使用帶隨機初始化的單步 FGSM 以節省計算，但有[FGSM](fgsm.md)頁中提到的災難性過擬合風險。

## 結果與限制

- PGD 對抗訓練在影像基準上產生的模型，其穩健準確率遠高於標準訓練（Madry 等人，2018）。
- 穩健性提高時，乾淨準確率通常會下降，Tsipras 等人（2019）將其解釋為某些設定中固有的取捨。
- 穩健準確率取決於評估所用的攻擊。Carlini 與 Wagner（2017）顯示，只針對較弱攻擊訓練的防禦，可能被更強的攻擊打破。
- 訓練成本是標準訓練的數倍，收益需與這個成本權衡。

## 應用

- **穩健的影像分類器**：用於小幅雜訊就可能改變判斷的情境。
- **基準測試**：使用多步與多次隨機重啟的 PGD，是標準的評估攻擊。
- **遷移到其他領域**：對抗訓練的想法已應用於語音、文字嵌入與圖資料，成本問題也相同。

## 開放問題

- 各領域訓練時應採用的預算與攻擊尚無定論，而穩健性也未必能遷移到新的攻擊類型。
- 在不損失穩健性的前提下降低對抗訓練的成本，仍是研究目標。

## 參考文獻

### 奠基性論文

- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — 提出 PGD 攻擊與極小極大的對抗訓練。
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — 提出基於梯度的攻擊與最早的對抗訓練實驗。
- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — 顯示更強的攻擊會打破僅以較弱攻擊評估的防禦。

### 綜述與教科書

- Tsipras, D., Santurkar, S., Engstrom, L., Turner, A. & Madry, A. (2019). Robustness may be at odds with accuracy. In *International Conference on Learning Representations*. arXiv:1805.12152. https://arxiv.org/abs/1805.12152 — 說明對抗訓練所呈現的準確率與穩健性取捨。
- Cohen, J., Rosenfeld, E. & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97. https://proceedings.mlr.press/v97/cohen19c.html — 比較經驗性的對抗訓練與認證保證。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；把對抗訓練視為極小極大問題。
