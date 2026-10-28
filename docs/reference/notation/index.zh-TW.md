---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - notation
  - mathematics
  - reference
aliases:
  - 符號
  - 數學符號
  - Notation
---

# 符號表

本頁列出全站使用的符號，讓讀者在不同頁面間移動時，能保持相同的意義。若某頁因特定理由使用不同的慣例，該頁會說明。符號慣例沿用標準的機器學習教科書，目標是易讀，而不是符合某一篇論文。

## 純量、向量與矩陣

- 小寫斜體字母，例如 $x$ 或 $\alpha$，表示純量。
- 小寫粗體字母，例如 $\mathbf{x}$，表示向量。預設向量為行向量。
- 大寫粗體字母，例如 $\mathbf{W}$，表示矩陣。$\mathbf{W} \in \mathbb{R}^{m \times n}$ 表示 $m$ 列、$n$ 行。
- $\mathbf{x}^\top$ 是轉置，$\|\mathbf{x}\|$ 是歐氏範數，$\odot$ 是逐元素乘積。

## 資料與模型

- $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^{N}$ 是包含 $N$ 個樣本的標記資料集。
- $\theta$ 表示模型 $f_\theta$ 的參數。對神經網路而言，$\theta$ 包含所有權重與偏置。
- $\hat{y} = f_\theta(\mathbf{x})$ 是預測值，$y$ 是目標值。

## 損失、梯度與最佳化

- $\mathcal{L}(\theta)$ 是損失，通常是資料集上的經驗平均：$\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^{N} \ell(f_\theta(\mathbf{x}_i), y_i)$。
- $\nabla_\theta \mathcal{L}$ 是對 $\theta$ 的梯度。梯度由自動微分計算，見[自動微分](../../theory/math/automatic-differentiation/index.zh-TW.md)。
- $\eta$ 是學習率，$t$ 是步數索引。

## 機率

- $p(x)$ 是密度函數或質量函數，$p(x \mid y)$ 是條件版本。
- $\mathbb{E}_{x \sim p}[f(x)]$ 是 $f$ 在 $p$ 下的期望值。
- $\mathrm{KL}(p \,\|\, q)$ 是 Kullback-Leibler 散度。

## 強化學習

- $s$ 是狀態，$a$ 是動作，$r$ 是獎勵，$\gamma \in [0, 1)$ 是折扣因子。
- $\pi_\theta(a \mid s)$ 是策略，$V^\pi(s)$ 是狀態價值函數，$Q^\pi(s, a)$ 是動作價值函數。
- 從時間 $t$ 開始的回報為 $G_t = \sum_{k \ge 0} \gamma^k r_{t+k}$。

## 衝突與例外

- 有些論文用 $x$ 表示輸入、$z$ 表示潛在編碼，也有相反的用法。各頁會說明其所採用的慣例。
- 在 Transformer 中，$d$ 通常表示模型寬度，$n$ 或 $T$ 表示序列長度。

## 參考文獻

### 重要論文

- Rumelhart、Hinton 與 Williams，*Learning representations by back-propagating errors*，Nature（1986）。https://doi.org/10.1038/323533a0 — 推廣了用於訓練多層網路的反向傳播。
- Silver、Huang、Maddison、Guez、Sifre、van den Driessche 等人，*Mastering the game of Go with deep neural networks and tree search*，Nature（2016）。https://doi.org/10.1038/nature16961 — 強化學習頁面中策略與價值符號的參考點。

### 綜述與教科書

- Goodfellow、Bengio 與 Courville，*Deep Learning*，MIT Press（2016）。https://www.deeplearningbook.org/ — 教科書，其符號章節列出純量、向量、矩陣與機率的慣例。
- Bishop，*Pattern Recognition and Machine Learning*，Springer（2006）。https://doi.org/10.1007/978-0-387-45528-0 — 教科書，對機率模型與貝氏推論使用一致的符號。

### 文章與文件

- Griewank 與 Walther，*Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*，SIAM（2008）。https://doi.org/10.1137/1.9780898717761 — 涵蓋導數符號，以及梯度計算背後的機制。
