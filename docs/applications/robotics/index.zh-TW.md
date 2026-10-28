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
