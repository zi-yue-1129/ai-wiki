---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 性別分類偏差
  - Gender Shades
  - Pilot Parliaments Benchmark
---

# Gender Shades (Buolamwini & Gebru, 2018)

Gender Shades is a disaggregated audit of three commercial gender classifiers. It showed that high average accuracy can hide large error gaps between skin tones and genders. It is a method page of [Surveillance, Facial Recognition and Human Rights](../index.md).

## Overview

Commercial face-analysis services were sold largely on their overall accuracy. Buolamwini and Gebru asked whether that average holds for everyone. Their answer is a benchmark balanced by gender and skin type, and an audit that reports error rates for each intersectional subgroup, such as darker-skinned women, not just for men and women or for light and dark skin alone. The audit is itself the method: a way for outsiders to measure a system they cannot inspect.

## Key concepts

- **Fitzpatrick skin type**: a six-point scale from dermatology that classifies how skin responds to sun. The paper groups types IV to VI as darker and I to III as lighter.
- **Intersectional subgroup**: a group defined by two attributes at once. The paper uses four: darker females, darker males, lighter females and lighter males.
- **Error rate**: the share of a subgroup's images that are misclassified, equal to one minus the true positive rate.
- **Black-box audit**: testing a system only through its public interface.

## How it works

1. **Build a balanced benchmark.** The authors assemble the Pilot Parliaments Benchmark (PPB), with images of 1,270 members of parliament from African and European countries. Its skin-type split is far more even than that of the existing benchmarks IJB-A and Adience, where lighter-skinned subjects make up 79.6% and 86.2% respectively, according to the abstract.
2. **Label each image** with gender and Fitzpatrick skin type.
3. **Submit each image** to three commercial classifiers, from Microsoft, IBM and Face++, through their public interfaces.
4. **Compute the error rate for each subgroup**:

$$
\text{Error}_g = 1 - \frac{TP_g}{TP_g + FN_g}
$$

where $g$ is a subgroup, $TP_g$ the correct positive predictions and $FN_g$ the missed positives.

5. **Compare the best and worst subgroups** for each classifier, and compare the overall figure with the disaggregated ones.

## Results

The figures below are from Table 4 of the paper, on the PPB benchmark.

| Classifier | Overall error | Darker females | Lighter males |
|---|---|---|---|
| Microsoft | 6.3% | 20.8% | 0.0% |
| Face++ | 10.0% | 34.5% | 0.8% |
| IBM | 12.1% | 34.7% | 0.3% |

The abstract reports that darker-skinned females have the highest error rates, up to 34.7%, and that the maximum error rate for lighter-skinned males is 0.8%. All three systems perform better on male faces than on female faces, with differences of 8.1 to 20.6 percentage points, and better on lighter faces than darker faces, with differences of 11.8 to 19.2 points. A South African subset shows the same pattern.

## Limitations

- **Small, posed benchmark.** The PPB has 1,270 people, and parliamentary portraits have relatively fixed poses, unlike most surveillance images.
- **Gender as a binary.** The authors note that their labels do not capture the complexity of gender or transgender identities, so the audit measures a narrow, binary task.
- **Snapshot.** The audit describes the systems at evaluation time. Vendors may have changed them since, and the paper cannot show current accuracy.
- **Classification, not identification.** Gender classification differs from face identification, which searches a gallery. The paper does not test identification directly.

## Connections

- Raji and Buolamwini (2019) follow this audit with a study of how publicly naming biased results affects the companies concerned.
- The benchmark problem applies to other face datasets too. Training-data composition matters, as the [ArcFace](../arcface/index.md) page discusses.
- The fairness definitions that disaggregated evaluation relies on, and the tensions between them, are covered in [Fairness definitions](../../ethics/fairness-definitions.md).

## Open questions

- Does an audit of one vendor's system transfer to other systems and to later versions of the same system?
- How can disaggregated audits be run when affected people cannot be sampled as a benchmark is?
- Kostka et al. (2021) find that public acceptance of facial recognition differs by country. Should audit results change acceptance, and how should that affect regulation?

## References

### Seminal papers

- Buolamwini, J. & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *FAT\**. https://proceedings.mlr.press/v81/buolamwini18a.html — The audit described on this page, with the Pilot Parliaments Benchmark and subgroup error rates.

### Surveys and textbooks

- Cao, Q. et al. (2017). VGGFace2: A dataset for recognising faces across pose and age. arXiv. https://arxiv.org/abs/1710.08092 — Large web-collected face dataset with variation in pose, age and ethnicity, used to train recognition models.

### Articles and documentation

- Raji, I. D. & Buolamwini, J. (2019). Actionable Auditing. *AAAI/ACM Conference on AI, Ethics, and Society*. https://doi.org/10.1145/3306618.3314244 — Follow-up on how publicly reporting audit results affects commercial AI products.
- Phillips, P. J. et al. (2011). An other-race effect for face recognition algorithms. *ACM Transactions on Applied Perception*. https://doi.org/10.1145/1870076.1870082 — Shows that face recognition algorithms, like human observers, perform better on the majority race in a database.
- Kostka, G., Steinacker, L. & Meckel, M. (2021). Between security and convenience: Facial recognition technology in the eyes of citizens in China, Germany, the United Kingdom, and the United States. *Public Understanding of Science*. https://doi.org/10.1177/09636625211001555 — Online surveys in four countries on public acceptance of facial recognition, which varies by country.
