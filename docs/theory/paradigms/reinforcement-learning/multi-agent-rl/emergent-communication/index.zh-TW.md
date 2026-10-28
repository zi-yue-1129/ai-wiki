---
translation_reviewed: 2026-10-28
---

# 湧現式通訊

湧現式通訊研究的是學會彼此說話的智能體。訊息通道不是事先設計好的：智能體同時學習協定（每則訊息代表什麼）與依據訊息行動的策略。核心問題是：為了合作，有用的符號，甚至類似語言的東西，會不會自然出現。

## 問題

在部分可觀測的任務中，一個智能體可能掌握另一個智能體需要的資訊。若通道由人手動設定，學習問題就只剩下選擇動作。若通道也要學習，智能體就得同時解決兩個問題：決定要傳送什麼，並學會訊息對接收者的意義。訊息的學習訊號也是間接的，因為它只能透過團隊的獎勵傳遞。

## 主要方法

- **[RIAL 與 DIAL](rial-dial/index.md)**（Foerster 等人，2016）以深度 Q 學習學習通訊。RIAL 把訊息當成離散動作；DIAL 則在訓練時讓誤差梯度穿過帶雜訊的通道。
- **[CommNet](commnet/index.md)**（Sukhbaatar 等人，2016）使用連續訊息。每個智能體接收其他智能體所傳送向量的總和，策略與通訊一起以反向傳播訓練。
- **參照遊戲**（Lazaridou 等人，2017）給說話者與聽者一張圖片，並要求聽者從一組圖片中選出同一張。智能體會就符號達成協調，而這項研究進一步檢驗這些符號能否與人類語言建立關聯。

## 比較

| 方法 | 訊息型態 | 訓練訊號 | 主要問題 |
|---|---|---|---|
| RIAL | 離散符號 | 對訊息動作做深度 Q 學習 | 訊息是否能被學會？ |
| DIAL | 訓練時為連續值，執行時離散化 | 穿過通道的梯度 | 信用能否在智能體之間傳遞？ |
| CommNet | 連續向量 | 透過策略的獎勵 | 通訊是否有助於合作任務？ |
| 參照遊戲 | 離散符號 | 配對圖片的獎勵 | 符號是否承載意義？ |

## 關聯

- 通訊是[馬可夫博弈](../index.md)的一種特例，具有部分可觀測性與共享獎勵。
- 不通訊的多智能體方法，例如 [MADDPG](../maddpg/index.md) 與 [QMIX](../qmix/index.md)，通常在訓練時以集中式評論家取代通訊通道。
- 參照遊戲中的基礎化問題，與[語言模型](../../../../models/llm/index.md)的研究相近；語言模型是從文字而非互動中學習語言。

## 未解問題與其他變體

- 湧現出的協定常常無法轉移到新的夥伴或新任務。
- 學到的符號可能人類無法理解，這限制了可解釋性。
- 簡單的獎勵訊號不一定會產生組合式語言，因此訓練設定與模型同樣重要。

## 參考文獻

### 奠基性論文

- Foerster 等人（2016），"Learning to communicate with deep multi-agent reinforcement learning"，[arXiv:1605.06676](https://arxiv.org/abs/1605.06676)——提出 RIAL 與 DIAL，並包含 switch riddle 等通訊任務。
- Sukhbaatar, Szlam & Fergus（2016），"Learning multiagent communication with backpropagation"，[arXiv:1605.07736](https://arxiv.org/abs/1605.07736)——提出 CommNet，一個與策略共同訓練的連續通訊模型。
- Lazaridou, Peysakhovich & Baroni（2017），"Multi-agent cooperation and the emergence of (natural) language"，[arXiv:1612.07182](https://arxiv.org/abs/1612.07182)——研究參照遊戲中湧現的符號，以及如何與人類語言建立關聯。
- Lowe 等人（2017），"Multi-agent actor-critic for mixed cooperative-competitive environments"，[arXiv:1706.02275](https://arxiv.org/abs/1706.02275)——集中式評論家，許多湧現式通訊研究都以它作為基準。

### 綜述與教科書

- Busoniu, Babuska & De Schutter（2008），"A comprehensive survey of multiagent reinforcement learning"，*IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172。https://doi.org/10.1109/tsmcc.2007.913919——多智能體學習設定的綜述，包含作為協調工具的通訊。
