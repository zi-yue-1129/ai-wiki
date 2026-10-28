---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/computer-vision
tags:
  - computer vision
  - pose estimation
aliases:
  - OpenPose
  - 姿態估計
  - 部位親和場
  - Part affinity fields
---

# OpenPose (Cao et al. 2017)

OpenPose is a system that finds the joints of every person in an image in one pass, linking them into skeletons with a learned field of limb directions. It made real-time multi-person pose estimation practical, and it is the pose tool most often used for sports video. It is one of the methods described on the parent page [Sports Analytics and Performance](../index.md).

## Overview

Estimating the pose of one person in a photograph is a manageable problem. Estimating the poses of a whole team is harder, because the system must decide which elbow belongs to which player when bodies overlap. Early approaches first detected every person with a box and then estimated the pose inside each box. That top-down strategy is accurate, but its cost grows with the number of people. OpenPose takes the opposite route: it detects all body parts in the image first and then groups them into people. Its running time therefore depends mostly on the image, not on how many people appear in it. Sports footage, with players in close contact, is the setting where this property matters most.

## Key concepts

- **Body part (joint) confidence map**: for each joint type, an image whose value at each pixel estimates how likely that joint is to be there.
- **Part affinity field (PAF)**: for each limb, a two-channel vector field whose value on a limb points from one joint to the next. It encodes where a limb is and which way it points.
- **Bottom-up parsing**: detecting all joints first and then assembling them into people, rather than detecting people first.
- **Stages**: the network refines its predictions over several sequential stages, each one receiving the image features and the previous stage's output.
- **Keypoint**: a labelled joint location, such as an ankle or a wrist. The usual output is a set of keypoints per person.

## How it works

Let $x_{j_1}$ and $x_{j_2}$ be the two joints at the ends of a limb $c$, and let $v$ be the unit vector pointing from $x_{j_1}$ to $x_{j_2}$. The ground-truth PAF is

$$
L_c^{*}(p) = \begin{cases} v & \text{if } p \text{ lies on limb } c, \\ 0 & \text{otherwise.} \end{cases}
$$

For two candidate joints $d_{j_1}$ and $d_{j_2}$ detected in the image, the paper scores whether they belong to the same limb by integrating the predicted field along the segment between them:

$$
E = \int_{u=0}^{1} L_c\big(p(u)\big)\cdot \frac{d_{j_2}-d_{j_1}}{\lVert d_{j_2}-d_{j_1}\rVert}\,du, \qquad p(u) = (1-u)\,d_{j_1} + u\,d_{j_2}.
$$

A high score means the field points along the segment, so the two joints are probably connected. Training minimises an L2 loss on the PAFs and on the confidence maps, at every stage $t$, with a mask $W$ that ignores unlabelled regions.

1. **Features.** A shared convolutional backbone, initialised from an image classification network, turns the image into feature maps.
2. **Refine.** Each stage predicts PAFs and confidence maps from the features and the previous stage. The paper reports that refining only the PAFs is both faster and more accurate than refining both outputs.
3. **Find joints.** Local maxima of the final confidence maps are the candidate joint locations.
4. **Associate.** For each limb type, the algorithm scores all pairs of candidates with $E$ and selects a set of non-conflicting connections with a greedy matching, so that each joint attaches to at most one partner.
5. **Assemble.** The connected limbs are merged into one skeleton per person.

## Results

The arXiv abstract of the CVPR paper reports two main results. The method placed first in the inaugural COCO 2016 keypoint challenge, and it significantly exceeded the previous state of the art on the MPII multi-person benchmark, in both accuracy and efficiency. It runs in real time whatever the number of people in the image. The extended journal version (preprint arXiv:1812.08008) adds a combined body and foot keypoint detector trained on an annotated foot dataset, and reports that the combined model is faster than running two detectors one after the other while keeping the accuracy of each part. These benchmarks are general-purpose image collections, not sports footage, so the evidence concerns generic images.

## Limitations

- **Two dimensions.** The system estimates joints in the image plane. Biomechanical analysis or 3D positioning needs several calibrated cameras or a separate lifting model.
- **Occlusion and crowding.** Players in a scrum or a wall of defenders hide one another's joints. The grouping step can then attach a limb to the wrong person.
- **Motion blur and camera angle.** Fast sprints, kicks and broadcast zooms produce blurred or unusual views that are rarely present in the benchmark data.
- **No temporal model.** A single-frame system does not keep identities across frames. Tracking players through a match needs a further step; see [video models](../../../theory/models/computer-vision/video/index.md) for the wider context.
- **Domain shift.** Uniforms, pitch markings and kit colours differ from the general image sets on which the model was trained, so accuracy on sports footage should be measured, not assumed.

## Open questions

- How well does a 2D pose system transfer to professional match footage, and how much sports-specific training data does it need?
- Can pose estimates from several cameras be fused into reliable 3D joint positions during play?
- Do small errors in joint positions change the injury-risk or technique conclusions drawn from them? This links to the injury discussion in the [topic overview](../index.md).
- The same kind of joint-and-limb representation supports motion perception studies. Johansson (1973) showed that observers see human motion from a few points of light, so it is an open question how closely the machine's representation resembles the one people use. The [motor control](../../../brain-mind/motor-control/index.md) page covers how people coordinate movement.

## References

### Seminal papers

- Cao, Z. et al. (2017). Realtime multi-person 2D pose estimation using part affinity fields. *CVPR*. https://doi.org/10.1109/CVPR.2017.143 — Introduces part affinity fields and the bottom-up pipeline that became OpenPose.
- Cao, Z. et al. (2021). OpenPose: realtime multi-person 2D pose estimation using part affinity fields. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. https://doi.org/10.1109/TPAMI.2019.2929257 — Journal extension that adds a combined body and foot keypoint detector and the PAF-only refinement analysis.
- Cao, Z. et al. (2016). Realtime multi-person 2D pose estimation using part affinity fields. arXiv. https://arxiv.org/abs/1611.08050 — Preprint of the conference paper, with the abstract reporting first place in the COCO 2016 keypoint challenge.
- Cao, Z. et al. (2018). OpenPose: realtime multi-person 2D pose estimation using part affinity fields. arXiv. https://arxiv.org/abs/1812.08008 — Preprint of the journal extension, describing the combined body and foot detector and its speed against running two detectors.
- Wei, S.-E. et al. (2016). Convolutional pose machines. arXiv. https://arxiv.org/abs/1602.00134 — Sequential convolutional predictors that refine part locations across stages, a precursor to the staged design used here.
- Newell, A., Yang, K. & Deng, J. (2016). Stacked hourglass networks for human pose estimation. arXiv. https://arxiv.org/abs/1603.06937 — Network for human pose estimation that processes features across scales in repeated hourglass modules.

- Johansson, G. (1973). Visual perception of biological motion and a model for its analysis. *Perception & Psychophysics*. https://doi.org/10.3758/BF03212378 — Shows that observers recognise human motion from a few points of light placed on the joints.

### Surveys and textbooks

- Chen, Y., Tian, Y. & He, M. (2020). Monocular human pose estimation: a survey of deep learning-based methods. arXiv. https://arxiv.org/abs/2006.01423 — Survey of deep learning approaches to estimating human pose from single images and video.
- Sun, K. et al. (2019). Deep high-resolution representation learning for human pose estimation. arXiv. https://arxiv.org/abs/1902.09212 — Keeps high-resolution features throughout the network, a widely used later architecture for the same task.
