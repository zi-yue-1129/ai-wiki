---
related:
- theory/models/computer-vision
- theory/models/gnn
- theory/paradigms/unsupervised/density-and-generative-models/generative-models
- applications/climate-energy
aliases:
  - 建築
  - 城市規劃
  - Urban Planning
---

# Architecture, Construction and Urban Planning

Buildings and cities generate large amounts of sensor, mobility and design data, and they change slowly and expensively. AI is used to forecast how buildings and cities will behave, to inspect structures, to explore designs and to support planning decisions. Most uses are still analytical; generative design is growing but is less tested in practice.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Building energy prediction | Regression, neural networks and other data-driven models on meter and weather data | A long-running field; Zhao & Magoulès (2012) and Wei et al. (2018) review the methods |
| Structural health monitoring | Image classification and transfer learning on crack and damage images; vibration analysis | Transfer from labelled images reduces the labelling cost (Gao & Mosalam, 2018) |
| Construction site monitoring | Computer vision for progress tracking, safety and equipment use | Camera coverage and privacy limit where it can be used |
| Urban mobility and planning | Models of trips, traffic and land use from mobile and transit data | Urban computing treats the city as a data source (Zheng et al., 2014) |
| Generative and parametric design | Conditional image-to-image models, optimisation, and generative models for layouts | Early; outputs need structural and code checks |
| Digital twins | Simulation models synchronised with sensor data | Data integration is the main obstacle |

## Why buildings and cities are hard

- **Long life.** A building is designed once and used for decades, so models must hold up as use changes.
- **Sparse labels.** Failures are rare and inspections are costly, so supervised datasets are small.
- **Local conditions.** Climate, materials and building codes differ between regions, which causes distribution shift.
- **Codes and liability.** Design outputs must meet structural and safety codes, and responsibility for errors is shared among designer, engineer and contractor.

## Key methods

Four method families cover most of the field. Each links to the page that explains it.

- [Computer vision](../../theory/models/computer-vision/index.md): classifying cracks and damage in photographs, and tracking progress on site.
- [Domain adaptation](../../theory/paradigms/transfer/domain-adaptation/index.md): reusing models trained on labelled structures in new buildings, which is the central idea in Gao & Mosalam (2018).
- [Graph neural networks](../../theory/models/gnn/index.md): modelling street networks, transit lines and building interactions as graphs.
- [Generative models](../../theory/paradigms/unsupervised/density-and-generative-models/generative-models/index.md): proposing layouts and facades; Isola et al. (2017) is the seminal example of paired image translation.

## Connections

Building energy use links directly to [Climate & Energy](../climate-energy/index.md). The data side of urban computing overlaps with [Privacy](../../society/privacy/index.md), since mobility and camera data identify people. The methods used for buildings are the same as those in [Manufacturing & Industry](../manufacturing/index.md) for inspection.

## Applications

- Forecasting building energy demand to support control and retrofit decisions.
- Automated screening of structures after earthquakes or storms, to prioritise human inspections.
- Modelling urban trips and traffic to test the effects of new transit lines or road changes.
- Generative tools that propose layouts and façade options for architects to review.

## Open questions

- How can generative design outputs be checked against building codes automatically and reliably?
- How well do energy models trained in one climate or building type carry over to another?
- Who is responsible when a model-supported design or inspection fails?
- How can urban data be used for planning without exposing the people in it?

## References

### Seminal papers

- Batty, M. (2018). Artificial intelligence and smart cities. *Environment and Planning B: Urban Analytics and City Science*. https://doi.org/10.1177/2399808317751169 — Argues that AI is changing how cities are planned and run, and what that change requires of planners.
- Zheng, Y., Capra, L., Wolfson, O. & Yang, H. (2014). Urban Computing: Concepts, Methodologies, and Applications. *ACM Transactions on Intelligent Systems and Technology*. https://doi.org/10.1145/2629592 — Defines urban computing as the use of city-scale data to understand and improve urban life.
- Isola, P., Zhu, J.-Y., Zhou, T. & Efros, A. A. (2017). Image-to-Image Translation with Conditional Adversarial Networks. *CVPR 2017*. https://arxiv.org/abs/1611.07004 — Shows that conditional adversarial networks translate between paired images, including label maps to building facades.

### Surveys and textbooks

- Zhao, H.-x. & Magoulès, F. (2012). A review on the prediction of building energy consumption. *Renewable and Sustainable Energy Reviews*. https://doi.org/10.1016/j.rser.2012.02.049 — Reviews the methods used to predict building energy use, from engineering models to data-driven ones.
- Wei, Y., Zhang, X., Shi, Y., Xia, L., Pan, S., Wu, J., Han, M. & Zhao, X. (2018). A review of data-driven approaches for prediction and classification of building energy consumption. *Renewable and Sustainable Energy Reviews*. https://doi.org/10.1016/j.rser.2017.09.108 — A survey of data-driven methods for building energy prediction and classification, covering methods and data sources.

### Articles and documentation

- Gao, Y. & Mosalam, K. M. (2018). Deep Transfer Learning for Image-Based Structural Damage Recognition. *Computer-Aided Civil and Infrastructure Engineering*. https://doi.org/10.1111/mice.12363 — Shows that transfer learning from pretrained image models reduces the labelled data needed to recognise structural damage.
