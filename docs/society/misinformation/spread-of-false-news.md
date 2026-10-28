---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 假新聞傳播
  - How false news spreads
---

# How False News Spreads

!!! info "Part of Misinformation & Deepfakes"
    This method page belongs to [Misinformation & Deepfakes](index.md). It explains one study in detail; the parent page compares it with other work.

Vosoughi, Roy and Aral (2018) measured how true and false stories spread on Twitter, using a large set of rumour cascades that had been checked against fact-checking verdicts. Their main finding is that false news travelled farther, faster, deeper and more broadly than true news, and that people, rather than automated accounts, were the main reason for the difference.

## Problem

Misinformation is often blamed on bots or on the algorithms that rank content. If that is right, interventions should focus on the machines. The question is whether false news spreads differently from true news, and if so, whether automated accounts explain the difference.

## Core idea

Reconstruct the spread of each story as a cascade of retweets, then compare true and false cascades on the same measures: how many people they reach, how quickly, how deep the chains of resharing go, and how broadly they spread across communities. Separately, measure how much automated accounts contribute to each kind of story.

## How the method works

1. **Collect and label.** Gather rumour stories that were checked by fact-checking organisations, and label each as true or false by the verdict.
2. **Reconstruct cascades.** For each story, follow the retweets to build the cascade of people who passed it on.
3. **Compare on four measures.** Compare true and false cascades on reach, depth, breadth and speed.
4. **Separate humans from bots.** Measure the effect of automated accounts, and compare how they spread true and false stories.

The method is observational. It records what happened on the platform and does not run controlled experiments on users.

## Results

The abstract reports that about 126,000 stories, tweeted by about 3 million people more than 4.5 million times, show that false news spread farther, faster, deeper and more broadly than true news across all categories of information. The effect was stronger for false political news than for other categories. Robots accelerated the spread of true and false news at the same rate, so the authors conclude that false news spreads more because humans are more likely to share it.

## Limitations

- **One platform and one period.** The results come from Twitter in the years covered by the data, and they may not apply to other platforms or later periods.
- **Observational data.** The study shows what people shared, not why they shared it, so it cannot establish motives.
- **Dependence on fact-checks.** Labels come from fact-checking verdicts, so the study is only as good as those verdicts and the stories they cover.
- **Scope of categories.** The abstract says the effect was strongest for political news, which makes the result harder to generalise to other topics.

## Connections

- The same spread question applies to synthetic media, where the content may be fake but realistic. See [FaceForensics++](facial-manipulation-detection.md) for the detection side.
- The shared-evidence harm that results from doubt is discussed in the liar's dividend section of the [Misinformation & Deepfakes](index.md) overview.
- Psychological work on why false claims persist is covered in [Psychology & AI](../../brain-mind/psychology/index.md).

## Open questions

- How much of the spread difference survives when platforms change ranking and labelling?
- Does the same pattern hold for synthetic media, where the content can be more convincing?
- How can corrections be made to travel as far as the original false story?

## References

### Seminal papers

- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359, 1146–1151. https://doi.org/10.1126/science.aap9559 — The study described on this page, comparing the spread of true and false stories on Twitter.
- Chesney, B. & Citron, D. (2019). Deep fakes: A looming challenge for privacy, democracy, and national security. *California Law Review*, 107. https://www.californialawreview.org/print/deep-fakes-a-looming-challenge-for-privacy-democracy-and-national-security — Legal analysis of deepfake harms, including the liar's dividend, which depends on doubt spreading as fakes become common.
- Rössler, A. et al. (2019). FaceForensics++: Learning to detect manipulated facial images. *ICCV*. https://arxiv.org/abs/1901.08971 — A detection benchmark for manipulated faces, covered on its own page.

### Articles and documentation

- C2PA. *Content Credentials: C2PA Technical Specification*, version 2.0. https://c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html — A signed provenance standard, an alternative to detecting fakes after the fact.
- EUR-Lex. *Regulation (EU) 2022/2065 (Digital Services Act)*. https://eur-lex.europa.eu/eli/reg/2022/2065/oj/eng — The official text of the DSA. Recitals 82 and 84 mention negative effects on civic discourse and the dissemination of disinformation.
