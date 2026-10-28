---
translation_reviewed: 2026-10-28
---

# MADDPG（Lowe 等人，2017）

MADDPG 是用於[多代理人強化學習](../index.md)的 Actor-Critic 方法。每個代理人有自己的策略，只看自己的局部觀測；也有自己的評論家，在訓練時能看到所有代理人的動作。由於每個評論家都以其他代理人的動作為條件，每個學習者看到的環境都近似平穩，而且此方法適用於合作、競爭與混合獎勵的情境。

## 概述

Lowe 等人（2017）解釋，獨立的 Actor-Critic 學習者在多代理人情境中會失敗，原因有二。Q 學習受到環境非平穩性的挑戰，因為其他代理人不斷改變；策略梯度方法則受到變異數隨代理人數量增加而變大的困擾。MADDPG 保留策略梯度的做法，但讓每個評論家取得它說明其他代理人所需的資訊。此方法建立在 DDPG（Lillicrap 等人，2015）之上；DDPG 是一種用於連續動作的確定性 Actor-Critic，MADDPG 把它延伸到多個代理人。它也是[父主題頁](../index.md)所描述的中心化訓練思路的一個實例。

## 關鍵概念

- **確定性演員**：代理人 $i$ 的策略 $\mu_i(o_i)$ 把自己的觀測 $o_i$ 映射到一個動作。
- **中心化評論家**：代理人 $i$ 的價值函數 $Q_i^\mu(x, a_1, \dots, a_N)$ 接收全域資訊 $x$ 與每個代理人的動作。
- **策略集成**：每個代理人訓練數個策略，並在每一回合開始時抽取一個。這使代理人較不容易過度擬合其他代理人當前的策略。
- **混合獎勵**：每個代理人都最大化自己的獎勵，因此此方法不假設共享的團隊獎勵。

## 運作方式

對代理人 $i$ 而言，演員以下列梯度更新：

$$
\nabla_{\theta_i} J(\mu_i) = \mathbb{E}\Big[\nabla_{\theta_i}\mu_i(o_i)\, \nabla_{a_i} Q_i^{\mu}(x, a_1, \dots, a_N)\big|_{a_i = \mu_i(o_i)}\Big],
$$

因此評論家對「自己的動作如何影響回報」的估計，會告訴演員應往哪個方向調整。評論家則最小化一個時序差分損失：

$$
L(\phi_i) = \mathbb{E}\big[(Q_i^{\mu}(x, \mathbf{a}) - y)^2\big], \qquad y = r_i + \gamma\, Q_i^{\mu'}(x', \mu'_1(o'_1), \dots, \mu'_N(o'_N)),
$$

其中 $\mu'$ 表示目標策略。步驟如下：

1. 初始化每個代理人的演員與評論家、它們的目標副本，以及一個儲存聯合轉移的回放緩衝區。
2. 每一回合開始時，每個代理人從自己的策略集成中抽取一個策略，並加入探索雜訊行動。
3. 把聯合轉移 $(x, \mathbf{a}, r, x')$ 存入緩衝區。
4. 抽取一個小批次，並以上述損失更新每個評論家，目標動作取自所有代理人的目標策略。
5. 以上述梯度更新每個演員，梯度由其評論家提供。
6. 把目標網路緩慢地拉向學習中的網路。

## 結果

論文在一組多代理人粒子環境上評估 MADDPG，其中包括需要協調的任務（如導航與溝通），以及讓代理人彼此對抗的任務（如捕食者與獵物）。摘要指出，此方法在合作與競爭情境中都優於既有方法，而代理人族群在實體與資訊兩方面都發現了協調策略。比較的數字請見論文。

## 限制

- **訓練時需要所有動作。** 評論家在訓練時需要每個代理人的動作，輸入大小隨代理人數量增長，而且這些資訊在實際部署中未必取得。
- **連續動作。** 確定性策略梯度是為連續動作空間設計的。
- **過時的回放。** 緩衝區中儲存的聯合轉移是由其他代理人較舊的策略產生的，這會削弱訓練訊號。
- **策略集成是經驗性的設計。** 從策略集成中抽樣可以減少對特定對手的過度擬合，但不保證對新對手的穩健性。

## 開放問題

評論家能否在代理人很多時仍能擴展，同時不喪失考慮其他代理人的能力？平均場近似以其平均效應取代其他代理人（Yang 等人，2018），提供了一條路，但取捨尚未有定論。第二個問題是如何完全避免需要其他代理人的真實動作。[QMIX](../qmix/index.md) 以不同的方式繞過這個需求，它分解的是聯合價值。Lanctot 等人（2017）提出以策略混合為對象進行訓練，以減少對最新對手的過度擬合。

## 參考文獻

### 開創性論文

- Lowe, R. 等人 (2017). *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments*. arXiv:1706.02275. https://arxiv.org/abs/1706.02275 — MADDPG 論文，包含中心化評論家、策略集成，以及合作與競爭任務上的實驗。
- Lillicrap, T. P. 等人 (2015). *Continuous control with deep reinforcement learning*. arXiv:1509.02971. https://arxiv.org/abs/1509.02971 — DDPG，MADDPG 所延伸的單一代理人確定性 Actor-Critic。
- Foerster, J. 等人 (2017). *Counterfactual Multi-Agent Policy Gradients*. arXiv:1705.08926. https://arxiv.org/abs/1705.08926 — COMA，另一種中心化評論家方法，以反事實基線取代每個代理人各自的評論家。
- Lanctot, M. 等人 (2017). *A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning*. arXiv:1711.00832. https://arxiv.org/abs/1711.00832 — 顯示獨立學習者會相互過度擬合，並提出以策略混合為對象進行訓練。

### 綜述與教科書

- Hernandez-Leal, P., Kartal, B. & Taylor, M. E. (2018). *A Survey and Critique of Multiagent Deep Reinforcement Learning*. arXiv:1810.05587. https://arxiv.org/abs/1810.05587 — 深度多代理人強化學習的綜述，包括 MADDPG 所屬的 Actor-Critic 方法。

### 文章與文件

- Yang, Y. 等人 (2018). *Mean Field Multi-Agent Reinforcement Learning*. arXiv:1802.05438. https://arxiv.org/abs/1802.05438 — 以平均效應近似大量代理人之間的互動，使學習可以處理。
- Papoudakis, G. 等人 (2020). *Benchmarking Multi-Agent Deep Reinforcement Learning Algorithms in Cooperative Tasks*. arXiv:2006.07869. https://arxiv.org/abs/2006.07869 — 在共同的合作式任務上對各類多代理人強化學習方法進行經驗性比較，並以 EPyMARL 公開程式碼。
