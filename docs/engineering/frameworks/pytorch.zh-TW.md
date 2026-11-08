---
related:
  - engineering/frameworks
  - engineering/frameworks/compilers-and-kernels
  - engineering/training
tags:
  - deep learning frameworks
  - automatic differentiation
  - eager execution
  - PyTorch
aliases:
  - PyTorch paper
  - PyTorch: An Imperative Style, High-Performance Deep Learning Library
  - PyTorch 論文
translation_reviewed: 2026-11-01
---

# PyTorch：命令式風格的高效能深度學習函式庫

PyTorch 論文（Paszke 等人，2019）描述一個深度學習函式庫，其程式會以即時執行的方式運行，就像一般的 Python 程式，而其自動微分在執行時建構。論文主張，放棄圖形元程式設計以換取命令式模型，所付出的速度代價是可以接受的，並報告了與當時其他框架的基準比較。本文發表於 NeurIPS 2019。框架的整體版圖見[框架](index.md)頁面。

## 概述

在 PyTorch 之前，許多框架要求使用者先建構靜態圖，再執行它。論文的設計保留了 Python 的模型：層、模型與訓練迴圈都是普通的 Python 程式碼，使用者可以控制流程的每個部分。這使程式容易撰寫，也能以標準工具除錯，代價是損失一些編譯期最佳化，而論文把這部分留給後續工作。

## 設計原則

第 3 節列出四項原則。

- **符合 Python 風格。** PyTorch 應是 Python 生態系的一等成員，具有簡單且一致的介面。
- **以研究者為先。** 模型、資料載入器與最佳化器應易於撰寫，複雜性隱藏在直觀的 API 之後，且沒有令人意外的效能斷崖。
- **實用的效能。** 速度很重要，但不能以犧牲簡潔為代價。作者願意為更簡單的模型接受小幅的速度損失，但不接受大幅損失。
- **較差反而更好。** 相較於完整但難以維護的實作，較簡單、略不完整的實作更受偏好，因為省下的功夫可以用於功能開發與跟上領域的步伐。

## 自動微分與即時執行

第 4.3 節說明自動微分。PyTorch 不是轉換原始碼，而是使用運算子重載，因此計算在執行時被記錄下來。目前的實作是反向模式，適合純量輸出與大量輸入的情況。前向模式被描述為可行，但不屬於目前的實作。

張量的修改是支援的。一個版本控制系統會追蹤修改，確保反向傳播使用正確的值。作者決定不採用寫時複製。複雜的原地操作會擲出使用者錯誤，而不是靜默地複製，以避免隱藏的效能成本。大多數梯度公式以 C++ 實作，並由不持有 Python 全域直譯器鎖的多執行緒引擎計算。

由於程式是即時執行的，列印敘述、標準除錯器與視覺化工具都能直接使用，不需要編譯步驟。

## 效能

第 6 節在兩顆 Intel Xeon CPU 與一張 NVIDIA Quadro GP100 GPU 上，以 32 位元浮點數比較訓練速度。下表為論文所報告的數值。單位為影像模型的每秒影像數、GNMTv2 的每秒 token 數，以及 NCF 的每秒樣本數。

| 框架 | AlexNet | VGG-19 | ResNet-50 | MobileNet | GNMTv2 | NCF |
|---|---|---|---|---|---|---|
| Chainer | 778 ± 15 | N/A | 219 ± 1 | N/A | N/A | N/A |
| CNTK | 845 ± 8 | 84 ± 3 | 210 ± 1 | N/A | N/A | N/A |
| MXNet | 1554 ± 22 | 113 ± 1 | 218 ± 2 | 444 ± 2 | N/A | N/A |
| PaddlePaddle | 933 ± 123 | 112 ± 2 | 192 ± 4 | 557 ± 24 | N/A | N/A |
| TensorFlow | 1422 ± 27 | 66 ± 2 | 200 ± 1 | 216 ± 15 | 9631 ± 1.3% | 4.8e6 ± 2.9% |
| **PyTorch** | 1547 ± 316 | 119 ± 1 | 212 ± 2 | 463 ± 17 | 15512 ± 4.8% | 5.4e6 ± 3.4% |

以這些數字看，PyTorch 在 VGG-19、GNMTv2 與 NCF 上最快。MXNet 在 AlexNet 上最快，Chainer 在 ResNet-50 上最快，PaddlePaddle 在 MobileNet 上最快。PyTorch 在 AlexNet 上的數字有很大的波動範圍。作者把常見模型上的接近結果歸因於共用相同的廠商核心函式庫，並報告 GPU 的工作與 CPU 排程重疊，使裝置保持忙碌。

## 限制

論文沒有獨立的限制章節，但內文指出了幾項。

- 最複雜的原地修改會擲出使用者錯誤，而不是自動處理。
- 前向模式微分尚未實作。
- 記憶體保證依賴參照計數，這排除了部分語言執行環境。
- 每個串流一個記憶體池的配置器在某些邊角情況下可能失效，不過作者表示這在實務上很少發生。
- Python 的全域直譯器鎖限制了執行緒數量，設計上以多程序來緩解。

論文所列的未來工作包括：可在 Python 直譯器之外執行程式的 JIT、高效的資料平行原語，以及基於遠端程序呼叫、符合 Python 風格的模型平行函式庫。

## 關聯

- 論文提出的 JIT 構想，指向[編譯器與核心](compilers-and-kernels/index.md)章節。
- 依賴框架的訓練實務，見[訓練](../training/index.md)頁面。
- PyTorch 的即時模型所對照的圖形式框架，見[框架](index.md)總覽。

## 未解問題

- 編譯器能在不改變 Python 程式的前提下，回收即時模型多少速度？
- 資料平行與模型平行，能否以論文所描述的同樣簡單介面表達？
- 在大量多串流工作負載下，記憶體配置應如何運作？

## 參考文獻

### 奠基論文

- Paszke, A. 等人（2019）。PyTorch: An Imperative Style, High-Performance Deep Learning Library. NeurIPS. [arXiv:1912.01703](https://arxiv.org/abs/1912.01703) — 本頁討論的設計、自動微分與基準結果。
- Abadi, M. 等人（2016）。TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems. [arXiv:1603.04467](https://arxiv.org/abs/1603.04467) — 論文所對照的靜態圖框架。
- Kingma, D. P. & Ba, J.（2014）。Adam: A Method for Stochastic Optimization. [arXiv:1412.6980](https://arxiv.org/abs/1412.6980) — PyTorch 訓練迴圈常用的最佳化器。
- He, K., Zhang, X., Ren, S. & Sun, J.（2015）。Deep Residual Learning for Image Recognition. [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — ResNet-50，是基準模型之一。
- Howard, A. G. 等人（2017）。MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. [arXiv:1704.04861](https://arxiv.org/abs/1704.04861) — MobileNet，是基準模型之一。

### 綜述與教科書

（本頁未核對）

### 講座與影片

（本頁未核對）

### 文章與文件

（本頁未核對）
