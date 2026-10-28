---
translation_reviewed: 2026-10-28
aliases:
  - 機器人
  - 機器人學
  - Robotics
---

# 機器人

## 經典技術堆疊

```mermaid
flowchart LR
  S[感測器：相機、LiDAR、力覺、IMU] --> P[感知與狀態估計]
  P --> M[建圖與定位 SLAM]
  M --> PL[任務與動作規劃]
  PL --> C[控制]
  C --> A[致動器]
```

傳統機器人學使用明確的模型：運動學、動力學、SLAM、取樣式規劃器（RRT、PRM）、最佳控制與模型預測控制。學習方法正逐步取代或增強其中的每個模組。

## 關鍵方法

### 用於抓取的手眼協調學習（Levine 等人，2016）

- **問題：** 機器人抓取通常依賴已校正的相機與已知的機器人姿態。機器人能否只靠原始單眼影像，在不校正的情況下學會手眼協調？
- **核心想法：** 大型卷積網路估計某個夾爪動作能成功抓取的機率。它只使用相機影像，因此不需要校正，也不需要知道目前的機器人姿態。接著，網路即時引導夾爪運動。
- **方程式或演算法：**
  1. 收集數台機械手臂同時執行的抓取嘗試，記錄每張影像以及該次抓取是否成功。
  2. 訓練卷積網路，依影像與候選動作預測抓取成功的機率。
  3. 執行時，利用網路即時伺服控制夾爪，依相機畫面修正動作。
- **結果：** 訓練資料來自兩個月內超過 80 萬次抓取嘗試，任一時刻有 6 至 14 台機械手臂在運作。摘要沒有給出抓取成功率，需要查閱全文。
- **限制：** 方法依賴規模極大、成本高的資料集，少有實驗室能負擔。它只用單一相機視角與特定的機器人設定，摘要也沒有顯示能否遷移到其他機器人。

## 以學習為基礎的機器人

| 方法 | 例子 |
|---|---|
| 模擬中的強化學習與模擬到真實（sim-to-real） | 足式移動（ANYmal、Unitree）、靈巧的手中操作（OpenAI 2019 年的魔術方塊）、無人機競速在 2023 年擊敗人類冠軍（Kaufmann et al.） |
| 從遙操作進行模仿學習 | ALOHA、Diffusion Policy、ACT——見[模仿學習](../../theory/paradigms/imitation/index.md) |
| 視覺—語言—動作模型 | RT-2、OpenVLA、π0／π0.5、Gemini Robotics、GR00T |
| 以 LLM 作為規劃器 | SayCan、Code as Policies——由語言模型選擇並排序技能 |
| 世界模型 | 用於規劃的學習式動力學（Dreamer、影片世界模型） |
| 跨機體資料 | Open X-Embodiment、DROID |

## 應用領域

| 領域 | 現況 |
|---|---|
| 工業機械手臂 | 結構化任務已成熟；AI 增加了彈性（如揀箱、檢測） |
| 倉儲與物流 | 大型行動機器人車隊；揀貨仍然困難，但正在進步 |
| 手術機器人 | 遙操作系統已相當普及；自主研究（自動縫合、離體研究中的膽囊切除步驟） |
| 足式機器人 | 用於巡檢的商用四足機器人 |
| 人形機器人 | 多家公司（Figure、Agility、Tesla Optimus、Unitree、UBTech、1X、Apptronik、Boston Dynamics）正在工廠與家庭試點；可靠性與成本仍是未解問題 |
| 農業 | 採收、除草（見[農業](../agriculture/index.md)） |
| 家用與輔助 | 吸塵器已成熟；通用的家務操作仍處於早期 |
| 太空與野外機器人 | 行星探測車、水下機器人、災難應變 |

## 未解的問題

- 與文字和影像相比，**資料稀缺**
- 對新物體、場景與機體的**泛化**
- **靈巧度與觸覺**：觸覺感測與精細操作
- **長時程的可靠性**：每一步 99% 的成功率仍然不夠
- 與人近距離互動時的**安全性**與認證
- **評估**：真實世界的基準難以重現

## 與神經科學的連結

運動控制研究——內部的前向與反向模型（小腦）、最佳回饋控制（Todorov & Jordan, 2002）、行走的中樞模式產生器、運動協同——長期以來一直影響機器人學；而機器人也被用作檢驗感覺運動學習理論的實體測試平台。

## 學習資源

- Lynch & Park，*Modern Robotics*（免費線上版與 Coursera 課程）
- Siciliano 與 Khatib（編），*Springer Handbook of Robotics*
- Thrun、Burgard 與 Fox，*Probabilistic Robotics*
- [MuJoCo](https://mujoco.org/)、[Isaac Lab](https://isaac-sim.github.io/IsaacLab/)、[ROS 2](https://docs.ros.org/)、[LeRobot](https://github.com/huggingface/lerobot)

## 參考文獻

### 開創性論文

- Levine, S. et al. (2016). Learning Hand-Eye Coordination for Robotic Grasping with Deep Learning and Large-Scale Data Collection. arXiv. https://arxiv.org/abs/1603.02199 — 從單眼影像預測抓取成功率並伺服夾爪，訓練資料超過 80 萬次抓取嘗試。
- Levine, S., Finn, C., Darrell, T. & Abbeel, P. (2015). End-to-End Training of Deep Visuomotor Policies. arXiv. https://arxiv.org/abs/1504.00702 — 訓練把原始相機影像映射為馬達力矩的卷積策略，感知與控制一起學習。
- Pinto, L. & Gupta, A. (2015). Supersizing Self-supervision: Learning to Grasp from 50K Tries and 700 Robot Hours. arXiv. https://arxiv.org/abs/1509.06825 — 以約 5 萬次試驗進行自監督的抓取學習，主張規模能減少過擬合。
- Tobin, J. et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World. arXiv. https://arxiv.org/abs/1703.06907 — 以隨機化的模擬影像訓練的偵測器，可遷移到真實物體與抓取。
- Kalashnikov, D. et al. (2018). QT-Opt: Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation. arXiv. https://arxiv.org/abs/1806.10293 — 以影像為基礎的自監督強化學習抓取，使用超過 58 萬次真實抓取嘗試，對未見過的物體成功率為 96%。
