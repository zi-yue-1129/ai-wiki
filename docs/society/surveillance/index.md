---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
  - society/privacy
  - society/governance
tags:
  - surveillance
  - facial recognition
  - human rights
aliases:
  - 監控
  - 臉部辨識
  - 人臉辨識
  - Facial recognition
---

# Surveillance, facial recognition and human rights

AI makes it cheaper to match faces, track movement and sort large volumes of video and text. Those capabilities can serve public safety and convenience, and they can also erode privacy, chill free assembly and fall unevenly on particular groups. This page covers the accuracy problems of facial recognition, the use of predictive systems in policing, and the legal responses.

## Overview

**Facial recognition** compares a face image against a gallery of stored images to verify an identity (one-to-one) or to find candidates (one-to-many). **Surveillance** here means the systematic observation of people, using cameras, databases and automated analysis. The human-rights concern is that these systems can be used without people's knowledge or consent, and that their errors are not spread evenly across the population.

## Key concepts

- **False positive**: the system declares a match for someone who is not in the gallery. In policing, this can lead to a wrongful stop or arrest.
- **False negative**: the system fails to match someone who is in the gallery.
- **Demographic differential**: a difference in error rates between groups defined by sex, age, skin tone or national origin.
- **Predictive policing**: the use of statistical models on past crime records to decide where officers should patrol.

## How it works

A face recognition pipeline detects a face, converts it into a numerical template and compares that template with stored ones. Each step can fail. Accuracy depends on image quality, on the training data, and on the threshold chosen for a match, which sets the trade-off between false positives and false negatives.

Accuracy differences were first documented in commercial gender classification. Buolamwini and Gebru tested three commercial systems and found that error rates were highest for darker-skinned women, reaching 34.7%, while the highest error rate for lighter-skinned men was 0.8% [(Buolamwini and Gebru, 2018)](https://proceedings.mlr.press/v81/buolamwini18a.html). The US National Institute of Standards and Technology then tested a large number of face recognition algorithms. It found that false positive rates often differed by factors of 10 to more than 100 across demographic groups, that false positives were 2 to 5 times higher for women than for men in the technical summary, and that false negative differentials were smaller and more algorithm-specific [(Grother, Ngan and Hanaoka, 2019)](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8280.pdf). The false positive problem matters most for surveillance, because a single false match can lead to a stop, a search or an arrest.

Predictive policing shows a related problem. When models are trained on records that reflect past enforcement rather than underlying crime, they can repeat and amplify existing bias [(Lum and Isaac, 2016)](https://doi.org/10.1111/j.1740-9713.2016.00960.x).

## Scale of deployment

A 2016 study by the Center on Privacy & Technology at Georgetown Law reported that law enforcement face recognition networks include over 117 million American adults, and that one in two American adults is in such a network [(Garvie, Bedoya and Frankle, 2016)](https://www.perpetuallineup.org/). The figures are from a decade ago and the systems have grown since, so they show the direction of the trend rather than its current size.

## Legal responses

The EU AI Act prohibits several uses. These include untargeted scraping of facial images from the internet or CCTV to build recognition databases, and, with narrow exceptions, real-time remote biometric identification in publicly accessible spaces for law enforcement [(Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj). Some cities and US states have restricted police use of face recognition, while others have expanded it. The debate is about whether accuracy improvements can justify wider use, or whether some uses should be banned whatever their accuracy.

## Connections

Surveillance raises the privacy questions covered in [Privacy and data protection](../privacy/index.md) and the fairness questions covered in [Ethics and fairness](../ethics/index.md). Evaluation methods for demographic differentials are closely related to the metrics discussed in [Evaluation](../../theory/evaluation/index.md).

## Applications

Face recognition is used to unlock phones, verify travellers at borders, find missing persons and identify suspects. Automated video analysis is used in retail, transport and public-space monitoring. Each application raises a different balance of benefit, consent and error cost.

## Open questions

- Can accuracy differentials be reduced enough that deployment is fair, and who verifies that claim in real conditions?
- What oversight should apply when a face match is only one piece of evidence?
- Should some uses be prohibited outright, such as mass monitoring of public spaces, rather than regulated case by case?
- How can people affected by a wrong match obtain redress?

## References

### Seminal papers

- Buolamwini and Gebru, *Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification*, Proceedings of Machine Learning Research 81 (2018). https://proceedings.mlr.press/v81/buolamwini18a.html — Shows large accuracy gaps by skin type and gender in three commercial classifiers.
- Lum and Isaac, *To Predict and Serve?*, Significance (2016). https://doi.org/10.1111/j.1740-9713.2016.00960.x — Shows how predictive policing models trained on biased records can reproduce that bias.

### Surveys and textbooks

- Grother, Ngan and Hanaoka, *Face Recognition Vendor Test (FRVT) Part 3: Demographic Effects*, NIST Interagency Report 8280 (2019). https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8280.pdf — Large-scale evaluation of demographic differentials in face recognition algorithms.

### Articles and documentation

- Garvie, Bedoya and Frankle, *The Perpetual Line-Up: Unregulated Police Face Recognition in America*, Center on Privacy & Technology at Georgetown Law (2016). https://www.perpetuallineup.org/ — Documents the scale of police face recognition networks and the access they give to driver's licence photos.
- European Union, *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*, Official Journal of the European Union (2024). https://eur-lex.europa.eu/eli/reg/2024/1689/oj — Sets prohibited practices and limits on remote biometric identification.
