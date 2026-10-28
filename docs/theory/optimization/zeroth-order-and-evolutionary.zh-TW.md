---
translation_reviewed: 2026-10-28
---

# 零階與演化最佳化

有些目標可以計算數值，卻無法求導：例如模擬器、黑箱分數、環境給出的獎勵，或經過不可微步驟的損失。零階方法只用函數值來估計搜尋方向。演化方法則是取樣候選解，並保留較好的那些。兩者都以較多的函數評估，換取不需要梯度的好處。

## 概述

本子章屬於[最佳化](index.md)資料夾。每種方法都有獨立頁面，本頁負責比較。同一想法的族群觀點見[演化與群體智慧](../paradigms/evolutionary/index.md)。

## 核心概念

- **零階神諭**：可以取得 \(f(\theta)\)，但無法取得 \(\nabla f(\theta)\)。
- **由差分估計梯度**：在擾動後的點上評估 \(f\)，可得方向導數的有限差分估計。每步只用一個方向所需的評估很少，但其變異數隨參數數量增加。
- **平滑化**：許多估計器會對高斯平滑後的目標求導，即 \(F_\sigma(\theta) = \mathbb{E}_\varepsilon[f(\theta+\sigma\varepsilon)]\)。即使 \(f\) 本身不可微，這個目標仍然存在。
- **族群**：演化方法保有一組候選解的分布，並把分布移向分數較好的候選解。

## 運作方式

每一步都先擾動目前的參數，在擾動後的點上評估目標，再把結果合併成更新。由此有兩類方法。像 SPSA 這樣的估計器方法，把少量評估轉換成類似梯度的步長，再交給一般的更新規則。像演化策略這樣的族群方法，則取樣許多候選解，依分數加權，並把取樣分布移向較好的解。

每一步都比反向傳播慢，但不需要導數。當目標不可微、系統是黑箱，或只能取得帶雜訊的量測時，這種做法特別有用。

## 關鍵方法

| 方法 | 想法 | 每步的函數評估次數 | 子頁 |
|---|---|---|---|
| SPSA（Spall，1992） | 以隨機正負號向量同時擾動所有參數 | 2 | [SPSA](spsa.md) |
| 演化策略（Salimans 等人，2017） | 由族群估計平滑獎勵的梯度 | 族群大小 | [演化策略](evolution-strategies.md) |
| CMA-ES（Hansen，2016） | 依好解區域的形狀調整協方差矩陣 | 族群大小 | [CMA-ES](cma-es.md) |

MeZO（Malladi 等人，2023）把 SPSA 式估計器用於微調語言模型，其記憶體用量在 [SPSA](spsa.md) 頁中討論。

## 關聯

- [演化與群體智慧](../paradigms/evolutionary/index.md)涵蓋族群觀點，以及更廣的自然啟發搜尋家族。
- [強化學習](../paradigms/reinforcement-learning/index.md)在獎勵不可微時使用零階估計。在該領域中，演化策略是政策梯度的替代方案。
- [二階方法](second-order.md)使用比這些方法更多關於目標的資訊，但每步成本較高。

## 應用

- 在模擬環境中訓練策略，此時獎勵可取得但不可微。
- 當儲存梯度與最佳化器狀態的成本過高時微調大型模型，如 MeZO。
- 調整參數不多、量測帶有雜訊的系統，此時 CMA-ES 是常用的基準。

## 開放問題

- 現代網路有數百萬到數十億參數，族群方法每步的成本如何隨之擴展？
- 零階估計在評估次數很少時，何時能與梯度方法在同一問題上匹敵？需要多少次評估？

## 參考文獻

### 開創性論文

- Spall, J. C.（1992）。Multivariate stochastic approximation using a simultaneous perturbation gradient approximation。*IEEE Transactions on Automatic Control*，37(3)，332–341。https://doi.org/10.1109/9.119632 — 提出 SPSA，以所有參數的同時擾動建構梯度近似。
- Salimans, T., 等人（2017）。*Evolution Strategies as a Scalable Alternative to Reinforcement Learning*。arXiv。https://arxiv.org/abs/1703.03864 — 顯示演化策略能擴展到超過一千個平行工作者，並在 MuJoCo 與 Atari 上與強化學習競爭。
- Hansen, N.（2016）。*The CMA Evolution Strategy: A Tutorial*。arXiv。https://arxiv.org/abs/1604.00772 — CMA-ES 的教學文件，這是一種用於非線性、非凸實數參數最佳化的隨機方法。
- Malladi, S., 等人（2023）。*Fine-Tuning Language Models with Just Forward Passes*。arXiv。https://arxiv.org/abs/2305.17333 — 以零階估計器微調語言模型（MeZO），記憶體用量接近推論。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 基於梯度的隨機方法綜述，是這些無梯度方法比較時的基準。
