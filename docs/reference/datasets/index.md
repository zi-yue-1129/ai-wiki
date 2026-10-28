---
references: not-required  # lists and meta pages cite through their entries
---

# Datasets

Widely used datasets, grouped by field. Check each dataset's licence and terms before use. Where a dataset name is linked, the link goes to the paper that introduced it (or to the paper that describes it most closely). Entries without a link have no verified source yet.

## Vision

| Dataset | Content |
|---|---|
| [MNIST](https://doi.org/10.1109/5.726791), [Fashion-MNIST](https://arxiv.org/abs/1708.07747) | 28×28 digits / clothing; teaching |
| CIFAR-10/100 | 32×32 images, 10/100 classes |
| [ImageNet-1k](https://arxiv.org/abs/1409.0575) | 1.28M images, 1,000 classes |
| [COCO](https://arxiv.org/abs/1405.0312) | Detection, segmentation, captions |
| [Open Images](https://arxiv.org/abs/1811.00982) | ~9M images with boxes and labels |
| [ADE20K](https://arxiv.org/abs/1608.05442), [Cityscapes](https://arxiv.org/abs/1604.01685) | Scene parsing, urban driving segmentation |
| [LAION-5B](https://arxiv.org/abs/2210.08402) / Re-LAION, [DataComp](https://arxiv.org/abs/2304.14108) | Image–text pairs from the web |
| [SA-1B](https://arxiv.org/abs/2304.02643) | 1B+ masks (Segment Anything) |

## Language

| Dataset | Content |
|---|---|
| Common Crawl | Raw web crawl |
| [C4](https://arxiv.org/abs/1910.10683), [The Pile](https://arxiv.org/abs/2101.00027), RedPajama, [Dolma](https://arxiv.org/abs/2402.00159), [FineWeb / FineWeb-Edu](https://arxiv.org/abs/2406.17557) | Filtered pre-training corpora |
| Wikipedia dumps | Encyclopaedic text (CC BY-SA) |
| [The Stack](https://arxiv.org/abs/2211.15533) | Permissively licensed source code |
| [SQuAD](https://arxiv.org/abs/1606.05250), [Natural Questions](https://doi.org/10.1162/tacl_a_00276) | Question answering |
| [GLUE](https://arxiv.org/abs/1804.07461) / [SuperGLUE](https://arxiv.org/abs/1905.00537) | NLU benchmarks (largely saturated) |
| [MMLU](https://arxiv.org/abs/2009.03300), [GPQA](https://arxiv.org/abs/2311.12022), [Humanity's Last Exam](https://arxiv.org/abs/2501.14249) | Knowledge and reasoning evaluation |
| [GSM8K](https://arxiv.org/abs/2110.14168), [MATH](https://arxiv.org/abs/2103.03874) | Math word problems |

## Speech and audio

[LibriSpeech](https://doi.org/10.1109/ICASSP.2015.7178964), [Common Voice](https://arxiv.org/abs/1912.06670) (many languages, CC0), [VoxCeleb](https://arxiv.org/abs/1706.08612), [AudioSet](https://doi.org/10.1109/ICASSP.2017.7952261), [MusicCaps](https://arxiv.org/abs/2301.11325) (introduced in the MusicLM paper).

## Multimodal and video

[Kinetics](https://arxiv.org/abs/1705.06950), Something-Something, [Ego4D](https://arxiv.org/abs/2110.07058), [HowTo100M](https://arxiv.org/abs/1906.03327), [VQAv2](https://arxiv.org/abs/1612.00837), [MMMU](https://arxiv.org/abs/2311.16502).

## Robotics and driving

[Open X-Embodiment](https://arxiv.org/abs/2310.08864), [DROID](https://arxiv.org/abs/2403.12945), [nuScenes](https://arxiv.org/abs/1903.11027), [Waymo Open Dataset](https://arxiv.org/abs/1912.04838), [Argoverse](https://arxiv.org/abs/1911.02620), [KITTI](https://doi.org/10.1109/CVPR.2012.6248074).

## Science and health

| Dataset | Content |
|---|---|
| [Protein Data Bank (PDB)](https://doi.org/10.1093/nar/28.1.235) | Experimental protein structures |
| [AlphaFold DB](https://doi.org/10.1093/nar/gkab1061) | 200M+ predicted structures |
| [UniProt](https://doi.org/10.1093/nar/gkac1052) | Protein sequences |
| [Materials Project](https://doi.org/10.1063/1.4812323), [OQMD](https://doi.org/10.1007/s11837-013-0755-4) | Computed materials properties |
| [ERA5](https://doi.org/10.1002/qj.3803) | Global atmospheric reanalysis (weather/climate) |
| [MIMIC-III](https://doi.org/10.1038/sdata.2016.35)/IV, [MIMIC-CXR](https://doi.org/10.1038/s41597-019-0322-0) | ICU records, chest X-rays (credentialed access) |
| [CheXpert](https://arxiv.org/abs/1901.07031) | Chest X-rays |
| [UK Biobank](https://doi.org/10.1371/journal.pmed.1001779) | Genetic, imaging, health data (application required) |
| TCGA | Cancer genomics |
| [MoleculeNet](https://doi.org/10.1039/C7SC02664A), TDC | Molecular ML benchmarks |

## Neuroscience and cognition

| Dataset | Content |
|---|---|
| [Natural Scenes Dataset (NSD)](https://doi.org/10.1038/s41593-021-00962-x) | 7T fMRI of people viewing tens of thousands of images |
| Human Connectome Project | Structural and functional brain imaging |
| Allen Brain Observatory | Mouse visual-cortex activity (calcium imaging, Neuropixels) |
| International Brain Laboratory | Standardised mouse decision-making recordings |
| [FlyWire](https://doi.org/10.1038/s41586-024-07558-y) | Whole fly-brain connectome |
| MICrONS | Mouse cortex structure + function (cubic millimetre) |
| OpenNeuro, DANDI | Archives of neuroimaging and neurophysiology data |
| Brain-Score benchmarks | Neural and behavioural data for model comparison |
| Psych-101 | Trial-level data from 160 psychology experiments |
| [Moral Machine](https://doi.org/10.1038/s41586-018-0637-6) | Millions of moral judgements across cultures |

## Tabular and general ML

UCI Machine Learning Repository, [OpenML](https://doi.org/10.1145/2641190.2641198), Kaggle datasets.

## Where to find more

[Hugging Face Datasets](https://huggingface.co/datasets), [Google Dataset Search](https://datasetsearch.research.google.com/), [OpenML](https://www.openml.org/), [Zenodo](https://zenodo.org/).
