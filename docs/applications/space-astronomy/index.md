---
related:
- theory/models/cnn
- theory/paradigms/active
- theory/paradigms/unsupervised/anomaly-detection
- applications/science
aliases:
  - 太空與天文
  - 天文學
  - Astronomy
---

# Space and Astronomy

Astronomy produces more data than people can inspect by eye: telescope surveys record billions of images, gravitational-wave detectors record continuous strain, and spacecraft return imagery and telemetry from distant planets. Machine learning is now routine in this work, and in space operations it is also used for autonomy and for tracking objects in orbit.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Galaxy and object classification | Convolutional networks on survey images; citizen-science labels as training data | Mature; Galaxy Zoo style crowd labels are a key data source |
| Exoplanet detection | Neural networks on light curves from Kepler and TESS; transit-signal classifiers | Found new planets in archival data (Shallue & Vanderburg, 2018) |
| Gravitational waves | Convolutional networks on detector strain for real-time detection and parameter estimation | Fast inference; results checked against matched filtering |
| Transients and anomalies | Anomaly detection, active learning with astronomer feedback | Human experts decide what is interesting |
| Simulation and emulation | Neural emulators replacing expensive cosmological and galaxy-formation simulations | Speed-up is the main gain |
| Space operations | Onboard autonomy, satellite imagery analysis, tracking of objects in orbit | Limited by radiation-hardened compute and communication delays |

## Why astronomy is a good test case

- **Labelled data is scarce.** Most sky objects have never been inspected by a person, so models must work with few labels.
- **Physics constrains the answer.** Models that respect known symmetries or physical laws generalise better than generic ones.
- **Surveys shift.** Instruments, filters and observing conditions change over time, which causes the same problems as distribution shift elsewhere.
- **Trust needs follow-up.** A claimed detection is confirmed by further observation, so the evaluation is partly done by telescope time, not by a test set.

## Key methods

Three method families do most of the work, and the survey of the field (Fluke & Jacobs, 2019) shows how widely they have spread.

- [Convolutional neural networks](../../theory/models/cnn/index.md): classifying images and one-dimensional signals such as light curves and gravitational-wave strain.
- [Active learning](../../theory/paradigms/active/index.md): choosing which objects an expert should label next, so that limited labelling time goes furthest. Astronomaly (Lochner & Bassett, 2021) applies this to anomaly search.
- [Anomaly detection](../../theory/paradigms/unsupervised/anomaly-detection/index.md): finding objects that do not match the population of known types, the basis of most discovery pipelines.

## Connections

The science side of AI is covered in [Scientific Discovery](../science/index.md). The method of learning with few labels is treated under [Active Learning](../../theory/paradigms/active/index.md), and the shift between instruments and survey conditions under [Domain Adaptation](../../theory/paradigms/transfer/domain-adaptation/index.md).

## Applications

- Automated classification of galaxy morphology in large surveys, using crowd-sourced labels to train the models (Dieleman et al., 2015).
- Real-time detection of gravitational-wave events from detector data, to alert telescopes that can follow up quickly (George & Huerta, 2018).
- Detecting exoplanet transits in archival space-telescope data, including planets missed by earlier searches (Shallue & Vanderburg, 2018).

## Open questions

- How can models trained on one survey be transferred to the next instrument without relabelling everything?
- Can emulators be validated well enough to replace full simulations in published results?
- How should discoveries made by automated pipelines be credited and confirmed?
- How much autonomy should spacecraft have when communication delays prevent human intervention?

## References

### Seminal papers

- Dieleman, S., Willett, K. W. & Dambre, J. (2015). Rotation-invariant convolutional neural networks for galaxy morphology prediction. arXiv. https://arxiv.org/abs/1503.07077 — Shows that convolutional networks can predict galaxy morphology from images, using crowd-sourced labels, with rotation invariance built in.
- George, D. & Huerta, E. A. (2018). Deep Learning for real-time gravitational wave detection and parameter estimation: Results with Advanced LIGO data. *Physics Letters B*. https://doi.org/10.1016/j.physletb.2017.12.053 — Reports that neural networks detect gravitational-wave signals in real detector data at speeds suited to real-time alerts.
- Shallue, C. J. & Vanderburg, A. (2018). Identifying Exoplanets with Deep Learning: A Five-planet Resonant Chain around Kepler-80 and an Eighth Planet around Kepler-90. *The Astronomical Journal*. https://doi.org/10.3847/1538-3881/aa9e09 — Uses a neural network on Kepler light curves to find new planets in archival data.
- Lochner, M. & Bassett, B. A. (2021). Astronomaly: Personalised active anomaly detection in astronomical data. *Astronomy and Computing*. https://doi.org/10.1016/j.ascom.2021.100481 — Combines anomaly detection with active learning so that an astronomer's feedback steers the search.

### Surveys and textbooks

- Fluke, C. J. & Jacobs, C. (2019). Surveying the reach and maturity of machine learning and artificial intelligence in astronomy. *WIREs Data Mining and Knowledge Discovery*. https://doi.org/10.1002/widm.1349 — A survey of how machine learning has been adopted across astronomy and where it is still immature.
