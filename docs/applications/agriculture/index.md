---
related:
- theory/models/computer-vision
- applications/climate-energy
- applications/robotics
aliases:
  - 農業
  - 食品
---

# Agriculture & Food

## Landscape

| Area | Examples |
|---|---|
| Crop monitoring | Satellite and drone imagery for crop type, health (NDVI and learned indices), yield forecasting |
| Precision application | "See-and-spray" weeding that targets herbicide at individual weeds (e.g. John Deere See & Spray), variable-rate fertiliser |
| Pest and disease diagnosis | Smartphone image classifiers for plant disease (PlantVillage); pest outbreak forecasting |
| Robotics | Harvesting robots for strawberries and apples, laser weeding, autonomous tractors |
| Livestock | Computer vision for animal health and behaviour, lameness detection, precision feeding |
| Breeding and genomics | Genomic selection, phenotyping from images, gene-editing target discovery |
| Irrigation and water | Soil-moisture models, evapotranspiration estimation |
| Supply chain and food | Demand forecasting, food-safety inspection, reducing waste, alternative proteins |
| Advisory | LLM-based advisory services in local languages for smallholder farmers (e.g. Farmer.CHAT, Digital Green) |

## Challenges

- **Variability**: weather, soil, crop varieties and lighting differ field to field — distribution shift is the norm
- **Labelled data scarcity**, especially for smallholder and tropical systems
- **Connectivity and cost** in rural areas → edge models
- **Seasonality**: one experiment per year per site
- **Data ownership** between farmers, equipment makers and platforms

## Climate connection

Agriculture is both vulnerable to climate change and a major emitter. AI supports drought early warning, climate-resilient crop breeding, methane monitoring and carbon-farming verification (see [Climate & Energy](../climate-energy/index.md)).

## Key methods

Three methods are most relevant here. Each links to the page that explains it.

- [ResNet](../../theory/models/cnn/backbones-and-scaling/resnet/index.md): residual CNNs that classify crop disease and weeds from leaf and field images, as in PlantVillage work (He et al., 2016; Mohanty et al., 2016).
- [Active learning](../../theory/paradigms/active/index.md): choosing which field images to label first when labels are scarce.
- [InstructGPT and RLHF](../../theory/models/llm/instructgpt-rlhf/index.md): the training recipe behind dialogue assistants, such as advisory tools for farmers (Ouyang et al., 2022).

## References

### Seminal papers

- He, K. et al. (2016). Deep Residual Learning for Image Recognition. CVPR. https://doi.org/10.1109/CVPR.2016.90 — Residual connections that make very deep CNNs trainable.
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT, instruction tuning from human preference feedback.
- Hughes, Salathé (2015). An open access repository of images on plant health to enable the development of mobile disease diagnostics. arXiv. https://arxiv.org/abs/1511.08060 — The PlantVillage image repository behind many smartphone disease classifiers.
- Mohanty, Hughes & Salathé (2016). Using Deep Learning for Image-Based Plant Disease Detection. *Frontiers in Plant Science*. https://doi.org/10.3389/fpls.2016.01419 — Trains CNNs on PlantVillage leaf images to classify crop diseases.
- Chiu et al. (2020). Agriculture-Vision: A Large Aerial Image Database for Agricultural Pattern Analysis. CVPR. https://doi.org/10.1109/cvpr42600.2020.00290 — An annotated aerial image dataset for agricultural pattern analysis.

### Surveys and textbooks

- Kamilaris & Prenafeta-Boldú (2018). Deep learning in agriculture: A survey. *Computers and Electronics in Agriculture*. https://doi.org/10.1016/j.compag.2018.02.016 — Survey of deep learning applications across crop and livestock tasks.
