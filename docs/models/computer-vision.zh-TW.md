# 電腦視覺

## 任務地圖

| 任務 | 輸出 | 代表模型 |
|---|---|---|
| 影像分類 | 類別 | ResNet、EfficientNet、ViT、ConvNeXt |
| 物件偵測 | 框＋類別 | Faster R-CNN、YOLO 系列、DETR、RT-DETR |
| 語意／實例／全景分割 | 像素標籤 | U-Net、Mask R-CNN、Mask2Former |
| 通用分割 | 任意物件遮罩 | SAM、SAM 2（影片） |
| 開放詞彙偵測 | 用文字描述找物件 | Grounding DINO、OWL-ViT |
| 姿態估計 | 關節點 | OpenPose、ViTPose |
| 深度估計 | 深度圖 | Depth Anything、MiDaS |
| 3D 重建與新視角合成 | 3D 場景 | NeRF、3D Gaussian Splatting、DUSt3R |
| 影片理解 | 動作、事件 | SlowFast、VideoMAE、影片 VLM |
| 追蹤 | 物件軌跡 | SORT、ByteTrack |
| OCR 與文件理解 | 文字、版面 | PaddleOCR、Donut、VLM |
| 影像生成與編輯 | 影像 | 見 [生成模型](generative.md) |

## 架構演進

1. **手工特徵時代**：SIFT、HOG＋SVM
2. **CNN 時代**（2012–2020）：AlexNet → VGG → GoogLeNet → ResNet → EfficientNet
3. **Transformer 時代**（2020–）：ViT 把影像切成 16×16 的塊當 token；Swin Transformer 引入階層與局部視窗
4. **自監督視覺基礎模型**：DINO/DINOv2/DINOv3、MAE、CLIP——不需標註就學到通用視覺特徵
5. **視覺語言整合**：見 [多模態模型](multimodal.md)

## 卷積的直覺

卷積核在影像上滑動，偵測局部模式。三個關鍵性質：

- **局部感受野**：每個神經元只看一小塊
- **權重共享**：同一個核在每個位置使用
- **階層結構**：堆疊後感受野變大，特徵越來越抽象

這三點直接來自視覺神經科學：

| 視覺皮質 | CNN |
|---|---|
| 感受野（Hubel & Wiesel） | 卷積核的局部連結 |
| V1 簡單細胞偵測方向邊緣 | 第一層卷積核學到類 Gabor 濾波器 |
| 複雜細胞對位置有容忍度 | 池化層 |
| V1 → V2 → V4 → IT 階層 | 淺層 → 深層 |
| IT 皮質對物體類別選擇性 | 深層特徵 |

Yamins et al.（2014）發現：在物體辨識上表現越好的 CNN，越能預測猴子 IT 皮質的神經反應。這開啟了「以任務最佳化的深度網路作為大腦模型」的研究範式，見 [NeuroAI](../brain-mind/neuroai.md)。

## 人類視覺 vs 電腦視覺

| 面向 | 人類 | 深度網路 |
|---|---|---|
| 偏好的線索 | 形狀 | ImageNet 訓練的 CNN 偏好紋理（Geirhos et al., 2019），可透過訓練改善 |
| 對抗樣本 | 幾乎不受影響 | 微小擾動就可能誤判 |
| 分布外泛化 | 強 | 較弱，但大規模預訓練模型大幅改善 |
| 少樣本學習 | 看一兩次就會 | 需要預訓練基礎 |
| 錯覺 | 會被某些錯覺欺騙 | 部分網路也會出現類似錯覺 |
| 能耗 | 視覺皮質約數瓦 | GPU 數百瓦 |

## 應用

醫療影像（見 [醫療](../applications/healthcare.md)）、自駕車（見 [自駕車](../applications/autonomous-driving.md)）、工業瑕疵檢測（見 [製造](../applications/manufacturing.md)）、農作物監測、衛星遙測、零售、安防、運動分析、AR/VR。

## 學習資源

- Stanford CS231n
- [d2l-zh 電腦視覺章節](https://zh.d2l.ai/chapter_computer-vision/index.html)
- Szeliski《Computer Vision: Algorithms and Applications》第二版（免費 PDF）
- [Ultralytics](https://docs.ultralytics.com/)、[Detectron2](https://github.com/facebookresearch/detectron2)、[timm](https://github.com/huggingface/pytorch-image-models)
