---
translation_reviewed: 2026-10-28
aliases:
  - 手眼協調
  - Hand-eye coordination
---

# 用於抓取的手眼協調學習（Levine 等人，2016）

Levine 等人問：機器人能否只靠原始單眼影像，在不做相機校正、也不知道機器人姿態的情況下，學會抓取的手眼協調？方法從大量真實抓取嘗試中學習。本主題屬於[機器人](../index.md)。

## 問題

機器人抓取通常依賴已校正的相機與已知的機器人姿態。問題在於：相機看到的東西與夾爪應該移動的方向之間的關係，能否直接從資料學出來？

## 核心想法

大型卷積網路估計某個夾爪動作能成功抓取的機率。它只使用相機影像，因此不需要校正，也不需要知道目前的機器人姿態。接著，網路即時引導夾爪，依相機畫面修正動作。

## 程序

1. 收集數台機械手臂同時執行的抓取嘗試，記錄每張影像以及該次抓取是否成功。
2. 訓練卷積網路，依影像與候選動作預測抓取成功的機率。
3. 執行時，利用網路即時伺服控制夾爪，依相機畫面修正動作。

## 結果

訓練資料來自兩個月內超過 80 萬次抓取嘗試，任一時刻有 6 至 14 台機械手臂在運作。摘要沒有給出抓取成功率，需要查閱全文。

## 限制

- 方法依賴規模極大、成本高的資料集，少有實驗室能負擔。
- 它只用單一相機視角與特定的機器人設定，摘要也沒有顯示能否遷移到其他機器人。
- 不必收集真實資料的模擬方法，由下方列出的領域隨機化研究處理。

## 連結

- 從原始影像到控制的同樣想法也出現在自動駕駛中，見[從像素到方向盤的端到端學習](../../autonomous-driving/end-to-end-steering/index.md)。
- 強化學習用於抓取，見[強化學習](../../../theory/paradigms/reinforcement-learning/index.md)。

## 參考文獻

### 開創性論文

- Levine, S. et al. (2016). Learning Hand-Eye Coordination for Robotic Grasping with Deep Learning and Large-Scale Data Collection. arXiv. https://arxiv.org/abs/1603.02199 — 從單眼影像預測抓取成功率並伺服夾爪，訓練資料超過 80 萬次抓取嘗試。
- Levine, S., Finn, C., Darrell, T. & Abbeel, P. (2015). End-to-End Training of Deep Visuomotor Policies. arXiv. https://arxiv.org/abs/1504.00702 — 訓練把原始相機影像映射為馬達力矩的卷積策略，感知與控制一起學習。
- Pinto, L. & Gupta, A. (2015). Supersizing Self-supervision: Learning to Grasp from 50K Tries and 700 Robot Hours. arXiv. https://arxiv.org/abs/1509.06825 — 以約 5 萬次試驗進行自監督的抓取學習，主張規模能減少過擬合。
- Tobin, J. et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World. arXiv. https://arxiv.org/abs/1703.06907 — 以隨機化的模擬影像訓練的偵測器，可遷移到真實物體與抓取。
- Kalashnikov, D. et al. (2018). QT-Opt: Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation. arXiv. https://arxiv.org/abs/1806.10293 — 以影像為基礎的自監督強化學習抓取，使用超過 58 萬次真實抓取嘗試，對未見過的物體成功率為 96%。
