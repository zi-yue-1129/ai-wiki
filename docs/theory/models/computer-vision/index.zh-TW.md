# 電腦視覺

## 任務地圖

| 任務 | 輸出 | 代表性模型 |
|---|---|---|
| 影像分類 | 類別 | ResNet、EfficientNet、ViT、ConvNeXt |
| [物件偵測](object-detection/index.md) | 邊界框加類別 | Faster R-CNN、YOLO 系列、DETR、RT-DETR |
| [語意／實例／全景分割](segmentation/index.md) | 逐像素標籤 | U-Net、Mask R-CNN、Mask2Former |
| 可提示的分割 | 任意物件的遮罩 | SAM、SAM 2（影片） |
| 開放詞彙偵測 | 找出以文字描述的物件 | Grounding DINO、OWL-ViT |
| 姿態估計 | 關鍵點 | OpenPose、ViTPose |
| 深度估計 | 深度圖 | Depth Anything、MiDaS |
| [3D 重建／新視角合成](3d-and-neural-rendering/index.md) | 3D 場景 | NeRF、3D Gaussian Splatting、DUSt3R |
| [影片理解與生成](video/index.md) | 動作、事件、生成的片段 | SlowFast、VideoMAE、影片擴散模型 |
| 追蹤 | 軌跡 | SORT、ByteTrack |
| OCR 與文件理解 | 文字、版面 | PaddleOCR、Donut、視覺語言模型 |
| 影像生成與編輯 | 影像 | 見[生成模型](../../generative/index.md) |

## 架構的演進

1. **人工設計的特徵**：SIFT、HOG 加 SVM
2. **CNN 時代**（2012–2020）：AlexNet → VGG → GoogLeNet → ResNet → EfficientNet
3. **Transformer 時代**（2020 起）：ViT 把 16×16 的影像區塊視為 token；Swin 加入階層結構與局部視窗
4. **自監督的視覺基礎模型**：DINO／DINOv2／DINOv3、MAE、CLIP——不需標籤即可得到通用的視覺特徵
5. **視覺與語言的整合**：見[多模態模型](../multimodal/index.md)

## 卷積的直覺

一個小型的核在影像上滑動，偵測局部的圖樣。三個關鍵性質：

- **局部感受野**
- **跨位置的權重共享**
- **階層性**：堆疊的層能看到更大的區域與更抽象的特徵

這三點直接來自視覺神經科學：

| 視覺皮質 | CNN |
|---|---|
| 感受野（Hubel & Wiesel） | 核的局部連接 |
| V1 簡單細胞偵測有方向的邊緣 | 第一層的核學到類似 Gabor 的濾波器 |
| 複雜細胞容忍位置的偏移 | 池化 |
| V1 → V2 → V4 → IT 的階層 | 淺層到深層 |
| IT 神經元對物件有選擇性 | 深層特徵 |

Yamins et al.（2014）發現，在物件辨識上表現較好的 CNN，也更能預測猴子 IT 皮質的神經反應，從而開啟了「以任務最佳化的深度網路作為大腦模型」的研究方向——見 [NeuroAI](../../../brain-mind/neuroai/index.md)。

## 人類與機器的視覺比較

| 面向 | 人類 | 深度網路 |
|---|---|---|
| 偏好的線索 | 形狀 | 在 ImageNet 上訓練的 CNN 偏好紋理（Geirhos et al., 2019）；可透過訓練改善 |
| 對抗樣本 | 幾乎不受影響 | 微小的擾動就能翻轉預測 |
| 分布外泛化 | 強 | 較弱，但大規模預訓練已縮小差距 |
| 少樣本學習 | 一兩個視角就已足夠 | 需要預訓練 |
| 錯覺 | 容易受到許多錯覺影響 | 有些網路會出現類似的錯覺 |
| 功耗 | 視覺皮質：幾瓦 | GPU：數百瓦 |

## 應用

醫學影像（[醫療保健](../../../applications/healthcare/index.md)）、自動駕駛（[自動駕駛](../../../applications/autonomous-driving/index.md)）、工業檢測（[製造](../../../applications/manufacturing/index.md)）、作物監測、遙測、零售、安防、運動分析、AR／VR，以及神經科學中的動物行為追蹤（DeepLabCut）。

## 學習資源

- Stanford CS231n
- [d2l：電腦視覺](https://d2l.ai/chapter_computer-vision/index.html)
- Szeliski，*Computer Vision: Algorithms and Applications*，第二版（免費 PDF）
- [Ultralytics](https://docs.ultralytics.com/)、[Detectron2](https://github.com/facebookresearch/detectron2)、[timm](https://github.com/huggingface/pytorch-image-models)

## 參考文獻

### 開創性論文

- Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). *ImageNet Classification with Deep Convolutional Neural Networks*. NeurIPS. https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — AlexNet 的成果，開啟了視覺領域的深度學習時代。
- Redmon, J., et al. (2016). *You Only Look Once: Unified, Real-Time Object Detection*. CVPR. https://arxiv.org/abs/1506.02640 — 把物件偵測表述為單次迴歸，使即時偵測成為可能。
- Ronneberger, O., et al. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. arXiv. https://arxiv.org/abs/1505.04597 — 帶有跳躍連接的編碼器—解碼器，是像素級分割的標準架構。
- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR. https://arxiv.org/abs/2010.11929 — 視覺 Transformer，把一般的 Transformer 套用在影像區塊上。

### 綜述與教科書

- Szeliski, R. *Computer Vision: Algorithms and Applications*，第二版。https://szeliski.org/Book/ — 涵蓋古典與學習式視覺的完整教科書；作者提供供個人使用的免費 PDF。

### 講座與影片

- Li, F.-F., Adeli, E., Johnson, J., et al. *CS231n: Deep Learning for Computer Vision*. Stanford University. https://cs231n.stanford.edu/ — 史丹佛的課程，講授用於視覺辨識的神經網路，附有講義與作業。
