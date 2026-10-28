---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation
  - theory/models/transformer
aliases:
  - ALOHA
  - Action Chunking with Transformers
  - ACT
  - 低成本雙臂操作
---

# ALOHA 與 ACT（Zhao 等人，2023）

Zhao 等人想知道：便宜、精度不高的機器人硬體，能否從少量真實示範學會精細的雙手任務。他們建置了一套低成本的雙臂系統 ALOHA，並提出學習方法 Action Chunking with Transformers（ACT）。本頁說明這篇論文；上層主題是[機器人](../index.md)。

## 問題

精細的雙臂操作，例如打開容器或插入電池，很難只靠模仿學會。誤差會在許多步驟中累積，人類示範也不一致。精密的機器人硬體昂貴，限制了能收集示範的人。

## 核心想法

ALOHA 由兩隻低成本的從動手臂，搭配兩隻可由人直接帶動的主動手臂組成，因此人能透過關節空間的遙操作直接示範任務（第 III 節）。整套系統的預算在 2 萬美元以下（第 III 節）。

ACT 一次預測一段未來的動作（一個 chunk），而不是每一步預測一個動作，因此減少了誤差累積的影響。它以條件變分自編碼器（CVAE）訓練，其 transformer 策略每次推論生成 100 步的目標關節位置（第 IV 節）。

## 程序

1. **示範**：每個真實任務收集 50 筆示範，綁魔鬼氈（Thread Velcro）為 100 筆。每個模擬任務有 50 筆腳本示範與 50 筆人類示範（第 V-B 節）。
2. **訓練**：每個任務從頭訓練 ACT，CVAE 目標的 β = 10。CVAE 編碼器只在訓練時使用，測試時潛變數設為零（第 IV-B 節，表 III）。
3. **推論與時間集成**：每個時間步都查詢策略，再以權重 exp(−m·i) 平均同一時間步的重疊預測，其中 i = 0 為最舊的預測。m 越小，新觀察的權重越大（第 IV-A 節，Alg. 2）。

每個相機的影像經過 ResNet-18 骨幹，所得特徵展平成 transformer 的 token。模型約有 8,000 萬個參數，在一張 11 GB 的 GPU 上約 5 小時完成訓練，推論約為 0.01 秒（第 IV-C 節）。

## 結果

論文以一個隨機種子、每個任務 25 次試驗，評估六個真實世界的雙臂任務。ACT 的最終階段成功率分別為：Slide Ziploc 88%、Slot Battery 96%、Open Cup 84%、Thread Velcro 20%、Prep Tape 64%、Put On Shoe 92%（表 I–II）。在 Slide Ziploc 與 Slot Battery 上，所有基線的最終階段成功率都是 0%。在其餘四項任務上，表現最好的基線 BeT 也是 0%。基線在早期子任務上確實有非零成功率，例如 VINN 在 Slide Ziploc 的抓取成功率為 28%。

在模擬中（表 I，3 個種子、50 次試驗），ACT 在腳本版的 Cube Transfer 上達 86%，人類示範版為 50%。Bimanual Insertion 的腳本版為 32%，人類示範版為 20%。BeT、RT-1、VINN 與 BC-ConvMLP 在腳本版 Cube Transfer 上最高為 27%，其他人類示範與插入的結果則為 3% 以下。

消融實驗（圖 8）顯示：

- **chunk 大小**：成功率從 k = 1 時的 1% 升到 k = 100 時的 44%，之後趨緩，在 k = 200 與 k = 400 時略有下降。為 BC-ConvMLP 與 VINN 加入 chunk 也能提升它們的表現。
- **時間集成**：為 BC-ConvMLP 增加 4%，為 ACT 增加 3.3%。VINN 則下降 20%。
- **CVAE**：移除後，在腳本資料上幾乎沒有差別；在人類資料上，表現從 35.3% 降到 2%。
- **控制頻率**：在六人的使用者研究中，把控制頻率從 50 Hz 降到 5 Hz，遙操作時間增加 62%（p < 0.001）（第 VI-C 節）。

## 限制

- **硬體**：ALOHA 難以處理需要雙手多指協作的任務，也難以處理高力量任務，因為低成本馬達的扭矩不足。依賴指甲的任務，例如掀起膠帶邊緣，同樣困難（附錄 F）。
- **策略**：ACT 未能學會拆糖果紙（一種協議下 10 次拆開 0 次）。拆開扁平的 ziploc 袋也很困難：策略能抓起袋子，但在空中的步驟上有困難（附錄 F）。綁魔鬼氈任務的成功率只有 20%（第 V-C 節）。
- **範圍**：結論指出，扣襯衫鈕扣等任務超出目前的系統（第 VII 節）。作者建議以預訓練、更多資料與更好的感知作為未來方向（附錄 F）。
- **作者未列為限制的部分**：論文沒有把力回饋、泛化或單任務訓練列為限制。論文確實說明 ACT 在每個任務上從頭訓練，並且每個任務依賴 50 筆示範（第 IV-C 節、第 V-B 節）。

## 連結

- 模仿學習的設定見[模仿學習](../../../theory/paradigms/imitation/index.md)。
- 針對類似任務的擴散式策略，見[Diffusion Policy](../diffusion-policy/index.md)。
- Transformer 架構見[Transformer](../../../theory/models/transformer/index.md)。

## 參考文獻

### 開創性論文

- Zhao, T. Z. et al. (2023). Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. arXiv. https://arxiv.org/abs/2304.13705 — 提出 ALOHA 硬體與預測動作 chunk 的 ACT 策略。
- Brohan, A. et al. (2022). RT-1: Robotics Transformer for Real-World Control at Scale. arXiv. https://arxiv.org/abs/2212.06817 — 以大量真實機器人資料訓練、用於真實世界控制的 transformer 策略。
- Chi, C. et al. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. arXiv. https://arxiv.org/abs/2303.04137 — 以條件去噪擴散模型生成機器人動作，是針對同類任務、與 ACT 並列的替代方案。

### 教科書與綜述

- Hussein, A. et al. (2017). Imitation Learning: A Survey of Learning Methods. *ACM Computing Surveys* 50(2). https://doi.org/10.1145/3054912 — 模仿學習方法的綜述，涵蓋 ACT 所用的設定。
- Kober, J., Bagnell, J. A. & Peters, J. (2013). Reinforcement learning in robotics: A survey. *The International Journal of Robotics Research* 32(11). https://doi.org/10.1177/0278364913495721 — 強化學習應用於機器人的綜述。
