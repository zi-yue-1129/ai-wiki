---
references: not-required  # lists and meta pages cite through their entries
last_reviewed: 2026-10-28
aliases:
  - 會議與期刊
  - Conferences and journals
  - Venues
---

# Conferences & Journals

Where AI and neuroscience research is published, how each venue reviews submissions, what preprints are for, and how far a venue's name tells you about the quality of a paper. Each row links to the venue's own page, or to its published proceedings where the main site could not be checked. Rows without a link name a venue that the page lists but could not check.

## Overview

Research in AI is published in two main ways. In a **conference**, authors submit by a deadline, reviewers read the papers within a few weeks, and the accepted papers appear in the proceedings and are presented at an annual meeting. In a **journal**, papers go through a longer review, often with rounds of revision, and appear in issues. Machine learning and computer science rely heavily on conferences. Neuroscience and psychology rely more on journals, so a reader moving between the fields will meet two different traditions.

Most papers now also appear as **preprints** on arXiv or bioRxiv, either before formal review or instead of it. A preprint is public and dated, but it has not been reviewed.

## Key concepts

- **Proceedings**: the collection of accepted papers from a conference, usually published as a numbered volume or on a dedicated site.
- **Single-blind and double-blind review**: in single-blind review, reviewers know who the authors are; in double-blind review, neither side knows the other.
- **Open review**: reviews, and sometimes author replies, are posted publicly. OpenReview hosts many venues this way.
- **Acceptance rate**: the share of submissions that are accepted. It changes from year to year and differs between venues.
- **Preprint**: a version of a paper posted publicly before, or instead of, peer review.

## Machine learning and AI conferences

| Venue | Field | Where the papers are | Note |
|---|---|---|---|
| [NeurIPS](https://proceedings.neurips.cc/) | Machine learning and neural computation | Yearly volumes on the proceedings site; the 2020 volume is titled *Neural Information Processing Systems 33* | Publishes much work with neuroscience links, see [NeuroAI](../../brain-mind/neuroai/index.md) |
| [ICML](https://proceedings.mlr.press/v139/) | Machine learning | Numbered volumes in the Proceedings of Machine Learning Research; volume 139 is the 2021 meeting | Papers are freely available in PMLR |
| [ICLR](https://openreview.net/group?id=ICLR.cc/2025/Conference) | Deep learning and representation learning | Submissions and reviews are handled on OpenReview; the 2025 group page is linked | Known for open review |
| [CVPR](https://openaccess.thecvf.com/CVPR2024) | Computer vision | CVF Open Access repository; the 2016 and 2024 meetings are listed there | Main venue for vision research, see [Computer Vision](../../theory/models/computer-vision/index.md) |
| ICCV | Computer vision | CVF Open Access repository, for example the [2025 meeting](https://openaccess.thecvf.com/ICCV2025) | Companion conference to CVPR |
| [ACL](https://aclanthology.org/venues/acl/) | Computational linguistics and natural language processing | ACL Anthology, with papers from the annual meeting by year | Community archive for language research |
| AAAI | Broad AI, including reasoning and planning | Proceedings papers carry DOIs; the 2016 paper [Deep Reinforcement Learning with Double Q-Learning](https://doi.org/10.1609/aaai.v30i1.10295) is one example | The conference's own site could not be checked |

The main homepages of NeurIPS, ICML, ICLR, CVPR and AAAI could not be checked from the environment used to write this page, so the links above point to each venue's proceedings or repository host. Check the venue's own site for the current call for papers and review rules.

## Journals and journal-style venues

| Venue | Field | Note |
|---|---|---|
| JMLR, *Journal of Machine Learning Research* | Machine learning | A long-running journal for machine learning research; its own site could not be checked |
| [TMLR](https://openreview.net/group?id=TMLR) | Machine learning | A journal-style venue that reviews submissions on OpenReview, without fixed conference deadlines |
| [TACL](https://aclanthology.org/venues/tacl/) | Computational linguistics | The journal of the ACL, indexed in the ACL Anthology |

## Neuroscience and cognitive-science venues

| Venue | Type | Where it fits | Note |
|---|---|---|---|
| Cognitive Computational Neuroscience (CCN) | Annual meeting | Computational models of brain and cognition | Official site could not be checked |
| Cognitive Science Society conference (CogSci) | Annual meeting | Cognitive science, with proceedings | Official site could not be checked |
| Society for Neuroscience (SfN) | Annual meeting | Experimental neuroscience; a very large meeting | Official site could not be checked |
| COSYNE | Annual meeting | Computational and systems neuroscience | Official site could not be checked |
| [*Behavioral and Brain Sciences*](https://doi.org/10.1017/S0140525X16001837) | Journal | Publishes target articles with open peer commentary, as in the paper by Lake et al. | Good example of debate in print |
| [*Nature Neuroscience*](https://doi.org/10.1038/nn.4244) | Journal | Experimental and computational neuroscience, for example goal-driven deep networks as models of sensory cortex | Wide-audience neuroscience journal |
| [bioRxiv](https://doi.org/10.1101/029876) | Preprint server | Life-science preprints, including neuroscience | Example: Kriegeskorte's early preprint on deep networks and the brain |

For the brain-side venues and the people who publish in them, see [Brain & Mind](../../brain-mind/index.md) and [Cognitive Science](../../brain-mind/cognitive-science/index.md).

## arXiv and preprint culture

[arXiv](https://arxiv.org/) is the preprint archive where most machine learning and many physics and mathematics papers first appear. Paul Ginsparg's 2011 article in *Nature*, [*arXiv at 20*](https://doi.org/10.1038/476145a), describes the first two decades of the archive and how researchers came to share work before formal publication. A posting on arXiv is dated and public, which lets a result be read and cited quickly. Moderation mainly checks whether a submission fits the subject area and is well formatted, not whether its results are correct.

Many well-known papers appear on arXiv before the conference that accepts them. The Transformer paper, [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762), was posted on 12 June 2017, months before the NeurIPS 2017 meeting, and the ResNet paper appeared on arXiv in December 2015 before the CVPR 2016 meeting.[^1] This habit means a reader may find two versions of the same work, one on arXiv and one in a venue, and that the arXiv version may be revised or rewritten. When citing, give the venue version when one exists and note the arXiv id.

Reproducibility is a related concern. [Pineau and colleagues (2020)](https://arxiv.org/abs/2003.12206) report on the NeurIPS 2019 reproducibility program and on what makes published machine learning results easier to check.

## Review processes and their problems

Conference review is fast, and the time available for each paper is limited. Shah and colleagues analysed the review data from the NIPS 2016 cycle, including an experiment on the review process itself.[^2] Rogers and Augenstein argue that reviewers in natural language processing often face a poorly defined task, which makes scores hard to compare across papers.[^3] Shah's 2022 overview in *Communications of the ACM* covers the main problems in peer review, the experiments that have studied them, and the computational fixes proposed so far.

Blinding is one of the most studied questions. [Tomkins and colleagues (2017)](https://doi.org/10.1073/pnas.1707323114) ran an experiment comparing single-blind and double-blind review in computer science and measured reviewer bias. Their results are a useful reminder that a venue's review rules are a design choice, not a fixed standard.

Journal review usually takes longer and includes revisions, but it has its own weaknesses. [Lipton and Steinhardt (2018)](https://arxiv.org/abs/1807.03341) discuss recurring problems in how machine learning papers make claims and present evidence, a critique that applies to both conferences and journals.

## How to read venue prestige

A venue's name is a weak signal on its own. Use it together with the following questions:

- **Who reviews it, and how?** Look for the review model (blind, open, or rolling), the reviewer pool, and whether reviews are published.
- **What does acceptance mean?** Acceptance rates vary by year and by venue, and they depend on how many papers are submitted. Use the venue's own report for the year, not a rule of thumb.
- **How is the work used?** Citation counts and rankings measure different things, change over time, and differ between fields. [Fortunato and colleagues (2018)](https://doi.org/10.1126/science.aao0185) review the "science of science", the research that uses large data sets to study how science is done, including its citations and careers.
- **Conferences or journals?** [Vardi (2009)](https://doi.org/10.1145/1506409.1506410) discusses the trade-offs of conference-based publication in computing, a norm that other fields do not share.
- **Is the paper itself sound?** A paper is judged by its claims, evidence and code, not by its venue. Read the paper and any public reviews.

## Connections

The venues above are where the topics in this wiki are published. The model families are in [Theory](../../theory/index.md), and the brain side in [Brain & Mind](../../brain-mind/index.md). The [Landmark Papers](../papers/index.md) list gives the papers that defined many of these fields, and [People & Labs](../people-and-labs/index.md) names the groups behind them. For the datasets used in most benchmark papers, see [Datasets](../datasets/index.md). The [History of AI](../../start/history/index.md) gives the wider timeline.

## Open questions

- Can conference review keep up as submission counts grow, and what should change in reviewer workload and incentives?
- Does preprint-first publishing speed up science, or does it make the record harder to follow?
- How should prestige be measured across fields where journals, conferences and preprints play different roles?

## References

### Articles and documentation

- arXiv. *arXiv.org e-Print archive*. https://arxiv.org/ — The preprint archive discussed above, where most machine learning papers are first posted.
- NeurIPS. *List of Proceedings*. https://proceedings.neurips.cc/ — Index of NeurIPS proceedings by year, with the accepted papers of each meeting.
- PMLR. *Proceedings of Machine Learning Research*. https://proceedings.mlr.press/v139/ — Proceedings volumes for ICML and other meetings; volume 139 is the 2021 ICML volume.
- OpenReview. *ICLR 2025 Conference*. https://openreview.net/group?id=ICLR.cc/2025/Conference — OpenReview group page for the ICLR 2025 conference, showing how ICLR uses open review.
- OpenReview. *TMLR*. https://openreview.net/group?id=TMLR — Group page for TMLR, a journal-style venue with rolling review.
- ACL Anthology. *Annual Meeting of the Association for Computational Linguistics*. https://aclanthology.org/venues/acl/ — Index of ACL papers by year, the main archive for language research.
- ACL Anthology. *Transactions of the Association for Computational Linguistics*. https://aclanthology.org/venues/tacl/ — Index of papers in the TACL journal.
- CVF. *CVPR 2024 Open Access Repository*. https://openaccess.thecvf.com/CVPR2024 — Accepted papers of CVPR 2024; the same repository lists earlier CVPR and ICCV meetings.

### Seminal papers

- Ginsparg, P. (2011). *ArXiv at 20*. Nature. https://doi.org/10.1038/476145a — Account of the arXiv preprint archive over its first two decades and of how researchers came to share work before publication.
- Vardi, M. Y. (2009). *Conferences vs. journals in computing research*. Communications of the ACM. https://doi.org/10.1145/1506409.1506410 — Editorial on the role of conference and journal publication in computing research.
- Tomkins, A., Zhang, M. & Heavlin, W. D. (2017). *Reviewer bias in single- versus double-blind peer review*. PNAS. https://doi.org/10.1073/pnas.1707323114 — Experimental comparison of single-blind and double-blind review in computer science, measuring reviewer bias.
- Shah, N. B., Tabibian, B., Muandet, K., Guyon, I. & von Luxburg, U. (2017). *Design and Analysis of the NIPS 2016 Review Process*. arXiv:1708.09794 — Analysis of the review data from the NIPS 2016 cycle, including an experiment on the review process.
- Shah, N. B. (2022). *Challenges, experiments, and computational solutions in peer review*. Communications of the ACM. https://doi.org/10.1145/3528086 — Overview of the problems in conference peer review, the experiments that studied them, and proposed computational fixes.
- Rogers, A. & Augenstein, I. (2020). *What Can We Do to Improve Peer Review in NLP?* arXiv:2010.03863 — Argues that reviewing in natural language processing conferences has a poorly defined task, and proposes ways to improve it.
- Lipton, Z. C. & Steinhardt, J. (2018). *Troubling Trends in Machine Learning Scholarship*. arXiv:1807.03341 — Discusses recurring problems in how machine learning papers make claims and present evidence.
- Pineau, J. et al. (2020). *Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)*. arXiv:2003.12206 — Report on the NeurIPS 2019 reproducibility program and on how to make published results easier to check.
- Fortunato, S. et al. (2018). *Science of science*. Science. https://doi.org/10.1126/science.aao0185 — Review of the science of science, which uses large data sets to study how research is done, including citations and careers.
- Lake, B. M., Ullman, T. D., Tenenbaum, J. B. & Gershman, S. J. (2016). *Building machines that learn and think like people*. Behavioral and Brain Sciences. https://doi.org/10.1017/S0140525X16001837 — Target article with open peer commentary, an example of how cognitive science publishes debate.
- Yamins, D. L. K. & DiCarlo, J. J. (2016). *Using goal-driven deep learning models to understand sensory cortex*. Nature Neuroscience. https://doi.org/10.1038/nn.4244 — Example of a neuroscience journal paper that uses machine learning models as models of the brain.
- Kriegeskorte, N. (2015). *Deep neural networks: a new framework for modelling biological vision and brain information processing*. bioRxiv. https://doi.org/10.1101/029876 — Early preprint on deep networks as models of biological vision and brain information processing.
- Van Hasselt, H., Guez, A. & Silver, D. (2016). *Deep Reinforcement Learning with Double Q-Learning*. AAAI. https://doi.org/10.1609/aaai.v30i1.10295 — Example of an AAAI proceedings paper, showing that AAAI papers carry DOIs.

[^1]: Posting dates from the arXiv records: [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) (12 June 2017) and [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) (December 2015). The CVPR 2016 meeting is documented in the [CVPR 2016 Open Access Repository](https://openaccess.thecvf.com/CVPR2016).
[^2]: Shah et al. (2017), arXiv:1708.09794.
[^3]: Rogers & Augenstein (2020), arXiv:2010.03863.
