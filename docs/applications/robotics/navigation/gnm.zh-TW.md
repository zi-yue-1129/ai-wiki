---
translation_reviewed: 2026-10-28
tags:
  - robotics
  - navigation
  - foundation model
aliases:
  - GNM
  - General Navigation Model
  - 通用導航模型
---

# GNM：通用導航模型

GNM 由 Shah、Sridhar、Bhorkar、Hirose 與 Levine（2023）提出，是一個在多種不同機器人資料上訓練的單一導航模型。它接收目前影像與一張影像目標，輸出一小段正規化的路標序列。論文的主要比較在輸出空間：依機器人尺度正規化的路標表現最好，而速度輸出與未正規化的路標都沒有達到相同效果。上層子主題是[以視覺目標導航](index.md)。

## 概述

GNM 以模仿學習訓練，資料來自數台機器人的行駛紀錄；對於新機器人，只需以其少量資料微調。網路同時預測目前影像與目標相隔幾步，因此同一個模型可支援以影像為目標的導航與探索。其輸出是一小段未來位置序列，由低階控制器跟隨。

## 問題

導航策略通常只為一台機器人訓練，平台一換就失效。論文探討：一個模型能否跨越相機與動力學不同的機器人，以及哪種動作表示最適合以目標為導向的行駛。

## 核心想法

使用共用的視覺編碼器，為每台機器人配一個輸出頭，並預測正規化的路標，而不是速度。正規化讓不同大小與速度的機器人輸出可以互相比較。時間上下文（即數個過去的影格）則幫助模型處理單一畫面資訊不足的動作。

## 運作方式

1. 從數台機器人收集行駛資料，每台有自己的相機與動力學，並以其後來到達的相對位置做標註。
2. 在所有資料上訓練一個視覺編碼器，並為每種機器人本體加上一個輸出頭。
3. 從目前影像、目標影像與過去的影格預測一段正規化的路標序列。
4. 以少量資料微調到新機器人，並以控制器跟隨預測的路標。

## 結果

論文在十個環境上對輸出空間做消融，比較速度、未正規化路標與正規化路標。作者報告，正規化路標的成功率最高，而速度策略在需要急轉彎的環境中表現吃力。他們也報告，加入數個過去的影格能提高困難環境中的成功率。數字在重用前應先在論文中核對。

## 限制

- 大部分資料來自有輪的地面機器人，因此對空中或足式機器人的主張超出評估範圍。
- 模型以模仿學習訓練，因此繼承行為克隆的限制，包括對訓練資料分布的敏感性。
- 正規化依賴每台機器人的參考尺度，每換一個新平台都必須重新設定。

## 相關主題

- [ViNG](ving.md) 是較早的方法，其輸出頭在單一機器人上回歸相對位姿。
- [ViNT](vint.md) 把同樣的想法擴展到較大的 Transformer 與更大的資料集。
- [NoMaD](nomad.md) 把輸出改為擴散模型上的動作。

## 開放問題

- 正規化路標的表示，能否適用於控制介面不是平面速度的機器人。
- 要讓共用模型可靠地適應新平台，需要多少特定機器人的資料。

## 參考文獻

- Shah, D., Sridhar, A., Bhorkar, A., Hirose, N., & Levine, S. (2023). *GNM: A general navigation model to drive any robot*. ICRA 2023. arXiv:2210.03370. https://arxiv.org/abs/2210.03370 — 共用模型與輸出空間比較的來源。
- Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., & Levine, S. (2023). *ViNT: A foundation model for visual navigation*. CoRL 2023. arXiv:2306.14846. https://arxiv.org/abs/2306.14846 — 較大的 Transformer 後繼方法。
- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., & Levine, S. (2021). *ViNG: Learning open-world navigation with visual goals*. ICRA 2021. https://doi.org/10.1109/ICRA48506.2021.9561936 — 單一機器人的前身。
- Sridhar, A., Shah, D., Glossop, C., & Levine, S. (2023). *NoMaD: Goal masked diffusion policies for navigation and exploration*. arXiv:2310.07896. https://arxiv.org/abs/2310.07896 — 以擴散為基礎的後繼方法，用於以目標為條件的導航與探索。
- Hirose, N., Xia, F., Martín-Martín, R., Sadeghian, A., & Savarese, S. (2019). *Deep visual MPC-policy learning for navigation*. IEEE Robotics and Automation Letters, 4(4), 3184–3191. arXiv:1903.02749. https://arxiv.org/abs/1903.02749 — 較早朝影像子目標訓練的學習導航策略。
