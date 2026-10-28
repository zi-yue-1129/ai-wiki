---
translation_reviewed: 2026-10-28
---

# 重生神經網路

重生網路是與其教師架構相同的學生，在教師的預測上訓練。Furlanello 等人表明，這些學生可以超越它們的教師，這與「蒸餾需要更大的教師」的假設相反。此方法是[自我蒸餾](../index.zh-TW.md)的一種，必要時可以重複多個世代。

## 問題

人們原本認為，只有學生比教師小時蒸餾才有效，因此需要一個更大的教師。

## 核心想法

訓練一個與教師架構相同的學生，以教師經軟化的預測作為目標。作者發現，所得的重生網路優於其教師，而且這種增益可以跨世代重複。

## 公式或演算法

每一代都以相同架構，最小化與前一代經軟化預測之間的蒸餾損失，不需要更大的模型。第一代以標籤訓練，之後每一代都以前一代作為教師。

## 結果

摘要表示，重生網路在電腦視覺與語言建模任務上都顯著優於其教師。

## 限制

每一代都需要完整的訓練。報告的改善取決於設定與世代數。

## 開放問題與相關變體

- **飽和。** 重複的世代會持續改善，還是對大型模型會飽和，目前尚不清楚。
- **相關：** [做你自己的老師](../be-your-own-teacher/index.zh-TW.md)在單次訓練中達到相似的效果。

## 相關連結

此方法顯示，網路可以透過重新學習自己的預測而改進。同樣的想法也出現在[持續學習](../../../../../theory/paradigms/continual/index.zh-TW.md)中，其中模型的早期狀態用來引導後續訓練。

## 參考文獻

### 開創性論文

- Furlanello, T., et al. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — 與教師架構相同的學生，在視覺與語言任務上表現優於教師。
- Zhang, L., et al. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — 同一網路內的深層自我蒸餾，是相關的自我教學方法。
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — 每一代所重用的蒸餾損失。

### 綜述與教科書

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — 綜述蒸餾方法，包括自我蒸餾。

### 講座與影片

（本頁尚未查核任何項目）

### 文章與文件

- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — 顯示教師與學生之間的差距，會影響學生的表現，這正是自我蒸餾所消除的問題。
