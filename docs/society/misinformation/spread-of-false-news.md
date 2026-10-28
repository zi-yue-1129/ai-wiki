---
status: complete
last_reviewed: 2026-10-28
aliases:
  - 假新聞傳播
  - How false news spreads
---

# How False News Spreads

!!! info "Part of Misinformation & Deepfakes"
    This method page belongs to [Misinformation & Deepfakes](index.md). It explains one study in detail; the parent page compares it with other work.

Vosoughi, Roy and Aral (2018) measured how true and false stories spread on Twitter, using a large set of rumour cascades that had been checked against fact-checking verdicts. Their main finding is that false news travelled farther, faster, deeper and more broadly than true news. They report that removing automated accounts from the data did not remove the difference, which they take as evidence that humans, more than bots, drive the spread of false news.

## Overview

Misinformation is often blamed on bots or on the algorithms that rank content. If that is right, interventions should focus on the machines. This study tests that view by comparing how true and false stories spread on the same platform, and by checking what happens when automated accounts are removed.

## Key concepts

- **Cascade**: the tree of retweets that follows one story from its first share onward.
- **Reach, depth, breadth and speed**: four measures of how a cascade spreads, covering how many people it reaches, how long its resharing chains run, how widely it spreads across communities, and how quickly it spreads.
- **Fact-checking verdict**: the label, true or false, assigned to each story by an independent fact-checking organisation.

## Problem

Misinformation is often blamed on bots or on the algorithms that rank content. If that is right, interventions should focus on the machines. The question is whether false news spreads differently from true news, and if so, whether automated accounts explain the difference.

## Core idea

Reconstruct the spread of each story as a cascade of retweets, then compare true and false cascades on the same measures: how many people they reach, how quickly, how deep the chains of resharing go, and how broadly they spread across communities. Separately, measure how much automated accounts contribute to each kind of story.

## How the method works

1. **Collect and label.** Gather rumour stories that were checked by fact-checking organisations, and label each as true or false by the verdict.
2. **Reconstruct cascades.** For each story, follow the retweets to build the cascade of people who passed it on.
3. **Compare on four measures.** Compare true and false cascades on reach, depth, breadth and speed.
4. **Separate humans from bots.** Remove automated accounts from the data and check whether the difference between true and false spread remains.

The method is observational. It records what happened on the platform and does not run controlled experiments on users.

## Key methods

This study is a measurement rather than a model, so its method is the cascade comparison above. The alternatives it is set against are explanations that blame automated accounts, and the ranking algorithms that some accounts of misinformation blame.

## Results

The MIT News summary of the study reports roughly 126,000 cascades of news stories on Twitter, tweeted by about 3 million people more than 4.5 million times in total. The authors report that false news spread farther, faster, deeper and more broadly than true news. Removing bots from the dataset did not remove the difference, and the authors conclude that humans are more likely than automated accounts to share false news.

## Limitations

- **One platform and one period.** The results come from Twitter in the years covered by the data, and they may not apply to other platforms or later periods.
- **Observational data.** The study shows what people shared, not why they shared it, so it cannot establish motives.
- **Dependence on fact-checks.** Labels come from fact-checking verdicts, so the study is only as good as those verdicts and the stories they cover.
- **Ranking not isolated.** The observed spread reflects Twitter's own ranking and sharing features, which the study does not separate from human behaviour.

## Variants and more variants

- **Bot-removal analysis**: the check in step 4, which tests whether automated accounts explain the difference.
- **Synthetic media spread**: the same question for fakes that look realistic, which later work examines.

## Connections

- The same spread question applies to synthetic media, where the content may be fake but realistic. See [FaceForensics++](facial-manipulation-detection.md) for the detection side.
- The shared-evidence harm that results from doubt is discussed in the liar's dividend section of the [Misinformation & Deepfakes](index.md) overview.
- Psychological work on why false claims persist is covered in [Psychology & AI](../../brain-mind/psychology/index.md).

## Applications

- Designing interventions on sharing and labelling, where the study suggests that human sharing decisions matter as much as the machines.
- Fact-checking prioritisation, where stories with fast, deep spread warrant attention early.

## Open questions

- How much of the spread difference survives when platforms change ranking and labelling?
- Does the same pattern hold for synthetic media, where the content can be more convincing?
- How can corrections be made to travel as far as the original false story?

## References

### Seminal papers

- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359, 1146–1151. https://doi.org/10.1126/science.aap9559 — The study described on this page, comparing the spread of true and false stories on Twitter.
- Chesney, B. & Citron, D. (2019). Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — Legal analysis of deepfake harms, including the liar's dividend, which depends on doubt spreading as fakes become common.
- Rössler, A. et al. (2019). FaceForensics++: Learning to Detect Manipulated Facial Images. arXiv. https://arxiv.org/abs/1901.08971 — A detection benchmark for manipulated faces, covered on its own page.

### Articles and documentation

- C2PA. *Content Credentials: C2PA Technical Specification*. https://spec.c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html — The technical specification for signed provenance records, an alternative to detecting fakes after the fact.
- EUR-Lex. *Regulation (EU) 2022/2065 (Digital Services Act)*. https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng — The official text of the Digital Services Act, the EU regulation on online intermediary services.
