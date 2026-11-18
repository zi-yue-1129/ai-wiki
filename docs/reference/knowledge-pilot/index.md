---
status: draft
references: not-required
aliases:
  - Evidence cards
  - Agent knowledge access
  - 主張證據
---

# Evidence and retrieval pilot

This small **LoRA/QLoRA pilot** connects concise bilingual claims to versioned primary sources, source locations, and explicit limitations. It is not an accuracy certificate for the wiki, a replacement for the papers, or a claim that experiments were reproduced.

## Read and inspect

- Read the [LoRA chapter](../../theory/model-compression/low-rank-and-efficient-architectures/lora/index.md) and [QLoRA chapter](../../theory/model-compression/low-rank-and-efficient-architectures/lora/qlora.md) for explanation and figures.
- Download the [eight evidence cards as JSON](../../assets/knowledge/lora-qlora.json). Each card contains English and Traditional Chinese summaries **and limits**, a wiki page and section, a versioned source with a locator, and a scoped source-reading date.
- The cards were checked against [LoRA v2](https://arxiv.org/abs/2106.09685v2), §4.1–4.2, and [QLoRA v1](https://arxiv.org/abs/2305.14314v1), §3–4 and Appendix B.2. Reading a source is not independent experimental replication or expert certification. The review covers only the listed claims, not the entire linked chapters.

| Card ID | Question to investigate |
|---|---|
| `lora-update` | Is the low-rank constraint on the base or on its update? |
| `lora-merge` | Under what condition can an adapter branch be merged? |
| `qlora-precision` | Does 4-bit storage mean 4-bit computation or full-parameter training? |
| `qlora-nf4` | What distribution assumption motivates NF4? |
| `qlora-double` | What is quantized in double quantization? |
| `qlora-paging` | What does paging move, and what does it not guarantee? |
| `qlora-65b` | Is 65B on 48 GB a configuration-specific report or a universal capacity guarantee? |
| `qlora-comparison` | Which scales were compared with full fine-tuning, versus 16-bit LoRA? |

## Query without an account or API

From a clone of this repository, use Python 3.12 or newer; the query tool uses only the standard library. No model call, network access, embedding service, or MCP server is required.

```bash
python scripts/knowledge.py search 'QLoRA 運算精度'
python scripts/knowledge.py search 'full fine-tuning baseline'
python scripts/knowledge.py get qlora-comparison
```

The tool returns JSON evidence **candidates**, not a generated answer. `lexical_score` is a ranking value, not a probability or confidence score. English word and Chinese bigram matching is deliberately simple; it is not general semantic search. A loosely related result is not evidence for every premise in a question. A query with no overlap returns `no_matching_evidence`; this is not proof that no answer exists elsewhere. For an unsupported question, follow the linked sources or explicitly say that the pilot does not cover it.

An agent should preserve the card's limitations and source version, open the original source when making consequential or current claims, and cite the source rather than treating an automated check as truth. For retrieval comparisons, pin the wiki commit along with the source versions. The human-facing website keeps normal navigation and search; this CLI is a separate, bounded pilot, not a replacement for full-site search.

## Verification and honest evaluation

```bash
python scripts/knowledge.py validate
python -m unittest discover -s scripts -p 'test_knowledge.py'
python -m unittest discover -s scripts -p 'test_wiki_review_status.py'
python scripts/knowledge.py evaluate
```

Validation checks card IDs, required bilingual fields, page/section existence, evidence references and review metadata. It **does not** check that the source scientifically supports a claim, fetch live links, verify all translations, or run model training. Read the source to assess those things.

The versioned question fixture contains 16 English/Chinese retrieval questions and three unrelated/no-evidence controls. `evaluate` reports whether an expected card appears in the top three, or an unrelated control returns no matches. These public, hand-authored cases are a smoke test of this tiny index, not a held-out benchmark of agent answers, citation correctness, general recall, or improvement over web search. Do not market the score as knowledge accuracy.

A future comparison should use held-out real questions, fixed model and budget, and three arms: no wiki, normal web search, and wiki access. Score factual correctness, source support, missing caveats, abstention, latency and token cost separately. No such experiment has yet been run here.

## Maintenance contract

1. Keep the original chapters as the explanatory home. The cards are a bounded retrieval view, not a second encyclopedia.
2. When a claim or its source changes, update its summary, limitations and source locator in both languages. Check the source before changing its `checked_on` date; do not change the whole page's review date after a partial card review.
3. A page heading disappearing fails validation. A content change under the same heading **does not** automatically trigger semantic revalidation; reviewers must check the linked cards when editing LoRA/QLoRA. A passing CI job cannot detect every stale paraphrase.
4. Keep `status: complete` separate from evidence review. It describes writing progress, not factual verification. See the [style guide](../style-guide/index.md).
5. Read-only consumers may download the static JSON or use the CLI. No credentials, uploads or third-party telemetry are needed. Claims and summaries retain the wiki's CC BY-SA 4.0 content license; the query script is MIT code.
