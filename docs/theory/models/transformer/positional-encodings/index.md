---
related:
- theory/models/llm
aliases:
  - Positional Encodings
  - Positional Embeddings
  - Length Extrapolation
  - 位置編碼
  - 長度外推
tags:
  - positional encoding
  - length generalisation
  - long context
last_reviewed: 2026-10-28
---

# Positional Encodings

Attention treats its input as a set: permuting the tokens permutes the outputs in the same way. Position information therefore has to be added, either to the token embeddings, to the attention scores, or to the queries and keys. The choice matters for two reasons. The encoding determines what relationships the model can represent, and it determines whether a model trained on sequences of one length still works on longer ones. This page covers the families of encodings and the methods for extending them to longer contexts. The overview of the Transformer, including the original sinusoidal encoding, is on the [Transformers & Attention](../index.md) page.

## Overview

Encodings fall into three groups:

- **Absolute** encodings add a vector for each position index to the token embedding. They are simple, but a position seen only in training has no meaningful vector beyond the trained range.
- **Relative** encodings make the attention score depend on the distance between two tokens, which is the quantity that usually matters for language.
- **Rotary and bias-based** encodings build the relative dependence into the query–key product or add a distance penalty, without learned position vectors.

## Approaches

| Method | Where position enters | Key paper |
|---|---|---|
| Sinusoidal | Added to token embeddings, fixed functions of the index | Vaswani et al. (2017), [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) |
| Relative position representations | Learned vectors for clipped distances, added to keys and values | Shaw et al. (2018), [arXiv:1803.02155](https://arxiv.org/abs/1803.02155) |
| Rotary (RoPE) | Queries and keys rotated by angles proportional to position | Su et al. (2021), [arXiv:2104.09864](https://arxiv.org/abs/2104.09864) |
| ALiBi | Linear penalty on the score, proportional to the distance | Press et al. (2021), [arXiv:2108.12409](https://arxiv.org/abs/2108.12409) |
| Position interpolation | Position indices scaled down to fit the trained range, then briefly fine-tuned | Chen et al. (2023), [arXiv:2306.15595](https://arxiv.org/abs/2306.15595) |
| YaRN | Frequency-dependent interpolation plus a temperature change in attention | Peng et al. (2023), [arXiv:2309.00071](https://arxiv.org/abs/2309.00071) |

### Relative and rotary encodings

Shaw et al. added learned vectors for each relative distance, clipped beyond a maximum, to the keys and values. RoPE takes a different route: each pair of dimensions in a query or key is rotated by an angle that grows with the token's position. The dot product of two rotated vectors then depends only on the difference of their positions. RoPE needs no extra parameters, works with the usual key–value cache, and is the default in many current open models.

<img data-source-asset-urls class="concept-motion-wide" tabindex="0" src="../../../../assets/concept-animations/shaw-relative-clipping-still.svg" data-motion-src="../../../../assets/concept-animations/shaw-relative-clipping-motion.svg" data-still-src="../../../../assets/concept-animations/shaw-relative-clipping-still.svg" alt="A query sweeps across nine token indices while the unclipped relative offset and the clipped radius-two relation bucket follow different curves: far-away indices share the same boundary bucket.">

*Original CC BY-SA 4.0 instructional animation.* In the **clipped relative-position representation** of Shaw et al. (2018), a query at position $i$ and key at $j$ use the relation bucket $b(i,j)=\operatorname{clip}(j-i,-K,K)$. This constructed example fixes $j=4$, takes $K=2$, and moves the query across indices $i=0,\ldots,8$. The unbounded offset decreases from $4$ to $-4$, while its clipped bucket follows $2,2,2,1,0,-1,-2,-2,-2$. Thus several *distinct distant offsets* share a learned relation representation; clipping does not mean those tokens become identical in content or attention weight. The continuously moving marker interpolates between **discrete integer positions** only to show the mapping, and is **not a model trace**. [Open animated SVG](../../../../assets/concept-animations/shaw-relative-clipping-motion.svg). On MkDocs, use Play/Pause and keyboard controls; the figure scrolls locally on narrow screens, and GitHub displays the static fallback. The underlying clipped relative-distance mechanism is from Shaw et al. (2018; References).

![RoPE animation: query and key vectors rotate with their token positions, and shifting both positions by the same amount preserves their relative angle and dot product.](../../../../assets/concept-animations/rope-relative-rotation.gif)

*Original two-dimensional RoPE schematic, CC BY-SA 4.0.* For the **same underlying query and key vectors** and a fixed frequency, shifting positions from **(1, 3)** to **(4, 6)** adds the same rotation to both vectors. Their relative offset remains two positions, so their inner product is unchanged: $(R_m q)^\top(R_n k)=q^\top R_{n-m}k$. The animated arrows are schematic directions, **not measured attention scores**. In full RoPE, different pairs of dimensions use different rotation frequencies. See [Su et al. (2021)](https://arxiv.org/abs/2104.09864).

### Bias-based encodings

ALiBi adds to each attention score a penalty proportional to the distance between the query and the key, with a different slope for each head. The model learns no position vectors, and Press et al. showed that models trained on short sequences could be evaluated on longer ones without the collapse seen with sinusoidal encodings.



<img data-source-asset-urls class="concept-motion-wide" tabindex="0" src="../../../../assets/concept-animations/alibi-distance-softmax-still.svg" data-motion-src="../../../../assets/concept-animations/alibi-distance-softmax-motion.svg" data-still-src="../../../../assets/concept-animations/alibi-distance-softmax-still.svg" alt="With equal causal content logits across eight keys, increasing the ALiBi distance-bias slope moves normalised attention mass toward the current key; a static side-by-side comparison remains visible on GitHub.">

*Original CC BY-SA 4.0 teaching animation.* In the constructed eight-key causal example, all content logits are zero. For distance \(d\in\{0,\ldots,7\}\), a nonnegative head slope \(m\) gives \(a_d(m)=\exp(-md)/\sum_{r=0}^{7}\exp(-mr)\). At \(m=0\), every key has probability \(1/8\); at \(m=1\), the current key (\(d=0\)) has probability approximately **0.6323**. The animation sweeps through analytically evaluated slopes (with smooth visual interpolation between sampled states); it does **not** show learned content scores, head-specific slopes from a real model, or measured accuracy. The underlying ALiBi formulation is from Press et al. (2021; see References). [Open the SVG animation](../../../../assets/concept-animations/alibi-distance-softmax-motion.svg). On the MkDocs site, use **Play/Pause**; on narrow screens, focus or scroll the figure horizontally. The static image remains readable on GitHub and without JavaScript.


<img data-source-asset-urls class="concept-motion-wide" tabindex="0" src="../../../../assets/concept-animations/alibi-content-recency-still.svg" data-motion-src="../../../../assets/concept-animations/alibi-content-recency-motion.svg" data-still-src="../../../../assets/concept-animations/alibi-content-recency-still.svg" alt="Five causal keys with content score two at distance four; as the ALiBi slope increases, the older key's normalised attention crosses below the current key at slope 0.5. The static view shows their exact tie.">

*Original CC BY-SA 4.0 instructional motion.* Unlike the equal-content example above, let the **oldest** of five causal keys (distance $d=4$) have content logit $c_4=2$; the other four have zero content logits. ALiBi changes the logits to $s_d=c_d-md$, and attention weights are $\operatorname{softmax}(s)_d$. At $m=0$, the older content match wins. When $m=1/2$, its adjusted logit $2-4m=0$ ties the current key at $d=0$; their **normalised probabilities are therefore equal**, even though the other three keys remain in the softmax denominator. A larger slope favours the current key. The continuous cursor follows **analytically evaluated** probabilities with sampled visual interpolation, not actual trained-head attention. This is not an accuracy benchmark. [Open motion](../../../../assets/concept-animations/alibi-content-recency-motion.svg). The shared MkDocs control offers Play/Pause and keyboard access; narrow displays scroll the diagram locally, and the still fallback remains understandable on GitHub. This demonstrates the content–distance competition in Press et al. (2021; References).



<img data-source-asset-urls class="concept-motion-wide" tabindex="0" src="../../../../assets/concept-animations/alibi-head-prefix-still.svg" data-motion-src="../../../../assets/concept-animations/alibi-head-prefix-motion.svg" data-still-src="../../../../assets/concept-animations/alibi-head-prefix-still.svg" alt="Three ALiBi heads with slopes 0.25, 0.5 and 1.0 receive the same growing causal prefix. The per-key attention heatmaps update as the query advances, and steeper slopes keep more probability near the newest key.">

*Original CC BY-SA 4.0 instructional animation.* **Head-dependent recency is not merely a different bias line:** the softmax *renormalises* over every available key. For a growing causal prefix ending at query index $t$, let every content logit be zero and use illustrative ALiBi head slopes $m\in\{0.25,0.5,1\}$. Then $p_m(j\mid t)=\exp[-m(t-j)]/\sum_{r=0}^{t}\exp[-m(t-r)]$ for $0\le j\le t$. The 8-second animation shows those **discrete, analytically calculated distributions**, progressively adding keys as $t$ advances from 0 to 7. At eight visible keys, the newest key receives approximately **0.2558, 0.4008, and 0.6323** of the probability mass in the three heads, respectively. Neither these slopes nor the logits are claimed to come from a trained model, and concentration is not a measure of task accuracy. [Open the motion](../../../../assets/concept-animations/alibi-head-prefix-motion.svg). The MkDocs shared player provides Play/Pause and keyboard support; GitHub and reduced-motion environments use the eight-key static view. This is an illustration of the head-specific linear biases in Press et al. (2021; References).

### Extending the context

A RoPE model trained on 4,096 positions degrades when given 16,384, because the rotation angles reach values it never saw in training. Position interpolation divides the position indices so that the longer sequence maps back into the trained range, and then fine-tunes briefly. YaRN goes further: it leaves the high-frequency dimensions unchanged, interpolates only the low-frequency ones, and rescales attention so that its entropy stays comparable at longer lengths. A related idea, NTK-aware scaling, was first proposed in an informal community post rather than a paper, and YaRN analyses its behaviour.



<img data-source-asset-urls class="concept-motion-wide" tabindex="0" src="../../../../assets/concept-animations/rope-interpolation-angle-still.svg" data-motion-src="../../../../assets/concept-animations/rope-interpolation-angle-motion.svg" data-still-src="../../../../assets/concept-animations/rope-interpolation-angle-still.svg" alt="At a toy rotary frequency of 0.6 radians per position, a position advances from zero to sixteen. Its unscaled angle reaches 9.6 radians while halving the position index keeps the interpolated angle at 4.8 radians, the example training maximum.">

*Original CC BY-SA 4.0 teaching animation.* Consider **one** two-dimensional RoPE frequency pair with toy angular frequency \(\omega=0.6\) radians per position, and a hypothetical training range \(p=0,\ldots,8\). At the extended position \(p=16\), direct rotation has **unwrapped** angle \(\theta=\omega p=9.6\) radians; twofold position interpolation uses \(p'=p/2\), giving \(\theta'=\omega p'=4.8\) radians, inside the illustrated training-angle range. The arrows wrap modulo \(2\pi\) while the bottom bars display unwrapped angles. Interpolation changes relative rotary phases and requires empirical fine-tuning/evaluation; this toy angle calculation **does not** establish length-extrapolation quality or describe every frequency band. See Chen et al. (2023; References). [Open the SVG animation](../../../../assets/concept-animations/rope-interpolation-angle-motion.svg). MkDocs provides **Play/Pause**, keyboard-accessible controls and a reduced-motion still; GitHub displays the static endpoint comparison.


<img data-source-asset-urls class="concept-motion-wide" tabindex="0" src="../../../../assets/concept-animations/rope-frequency-bands-still.svg" data-motion-src="../../../../assets/concept-animations/rope-frequency-bands-motion.svg" data-still-src="../../../../assets/concept-animations/rope-frequency-bands-still.svg" alt="A fast and a slow RoPE frequency pair rotate continuously at different rates as relative distance increases. At distance four the fast pair has already wrapped around, while the slow pair still differs.">

*Original CC BY-SA 4.0 instructional motion.* RoPE rotates **different pairs of dimensions at different frequencies**, so one pair returning to its previous phase does not imply that the full rotary representation repeats. With fixed underlying two-dimensional query and key vectors $q=k=(1,0)$, each pair contributes a toy similarity $\cos(\omega\Delta)$ at relative distance $\Delta$. The figure uses $\omega_{\mathrm{fast}}=\pi/2$ and $\omega_{\mathrm{slow}}=\pi/10$ radians per position. At $\Delta=4$, the fast component completes $2\pi$ and returns to similarity $1$, while the slow component rotates $2\pi/5$ (72°), with similarity $\cos(2\pi/5)\approx 0.309$. The graph and two rotation arrows progress together through $\Delta\in[0,16]$. These deliberately chosen frequencies and aligned vectors are **analytic schematics**, not the frequency schedule, learned attention pattern, or length-extrapolation accuracy of any deployed model. The general rotation-pair construction is from Su et al. (2021; References). [Open motion](../../../../assets/concept-animations/rope-frequency-bands-motion.svg). MkDocs offers Play/Pause with a static, GitHub-readable fallback.


<img data-source-asset-urls class="concept-motion-wide" tabindex="0" src="../../../../assets/concept-animations/yarn-frequency-ramp-still.svg" data-motion-src="../../../../assets/concept-animations/yarn-frequency-ramp-motion.svg" data-still-src="../../../../assets/concept-animations/yarn-frequency-ramp-still.svg" alt="Six example RoPE frequencies change differently under YaRN-style wavelength-dependent interpolation: slow bands shrink, intermediate bands blend, and high-frequency bands remain unchanged.">

*Original CC BY-SA 4.0 instructional motion.* **YaRN combines** the NTK-by-parts frequency ramp with a separate **attention-logit temperature correction**; this figure illustrates **the frequency component only**. Write $r=L/\lambda$ for the number of rotations within the original context length, and choose illustrative $s=4$, $\alpha=1$, $\beta=4$. With $\gamma(r)=\operatorname{clip}((r-\alpha)/(\beta-\alpha),0,1)$, the effective frequency ratio is $\theta'(r)/\theta=\gamma(r)+(1-\gamma(r))/s$. For six made-up frequency bands $r=(0.5,1,1.5,2,3,4)$, the endpoint ratios are $(0.25,0.25,0.375,0.5,0.75,1)$. The bars **continuously shorten or remain fixed** as the reciprocal scale $1/s$ sweeps from $1$ to $1/4$ and back: long-wavelength bands interpolate, intermediate bands blend, and short-wavelength bands retain local phase sensitivity. **The bands and thresholds are teaching parameters, not fitted YaRN parameters, model outputs, or measured context quality.** See Peng et al. (2023; References) for the full method and attention scaling. [Open animated SVG](../../../../assets/concept-animations/yarn-frequency-ramp-motion.svg). MkDocs provides Play/Pause and keyboard access; GitHub and reduced-motion settings use the static endpoint view.


<img data-source-asset-urls class="concept-motion-wide" tabindex="0" src="../../../../assets/concept-animations/rope-cache-reindex-still.svg" data-motion-src="../../../../assets/concept-animations/rope-cache-reindex-motion.svg" data-still-src="../../../../assets/concept-animations/rope-cache-reindex-still.svg" alt="A toy key at original position two and query at six remain four steps apart after token eviction. Incorrectly repacking surviving token positions to zero through three changes the apparent offset to two and flips a rotary cosine contribution.">

*Original CC BY-SA 4.0 instructional animation.* **Compact KV memory addresses must not be confused with rotary position indices.** Imagine tokens at original positions $0,\ldots,6$; retain $\{0,2,5,6\}$ after evicting positions $1,3,4$. A query at original position 6 and key at position 2 have true offset $6-2=4$. If an implementation **incorrectly reassigns** the retained tokens positional indices $0,1,2,3$ (rather than merely compacting their storage), that pair's apparent offset becomes $3-1=2$. For one illustrative RoPE pair with $q=k=(1,0)$ and angular frequency $\omega=\pi/6$, the dot-product contribution consequently changes from $\cos(4\omega)=-1/2$ to $\cos(2\omega)=+1/2$. The animation reveals which tokens disappear before the incorrect remapping; the static fallback compares both layouts. **A uniform shift of all positions is different:** it preserves relative offsets; the failure here arises from *nonuniform gaps collapsing*. This example demonstrates positional correctness, not a measured attention score or the actual behaviour of any specific cache implementation. [Open motion](../../../../assets/concept-animations/rope-cache-reindex-motion.svg). On MkDocs, Play/Pause and keyboard operation are provided by the shared controller. The RoPE identity follows Su et al. (2021; References).

## Trade-offs

- **Extrapolation versus accuracy.** Encodings that extrapolate, such as ALiBi, may give up some accuracy at the trained length. Interpolated RoPE keeps accuracy within the trained range but needs fine-tuning to extend.
- **Cost of extension.** Interpolation methods need training data and compute for the longer context, while bias-based methods need none.
- **Interaction with caching.** Some cache-eviction methods drop tokens, which changes the relative distances the model sees. Positional handling must stay consistent with the cache.
- **Multimodal inputs.** Images and video are two- or three-dimensional, so one-dimensional rotations need generalising to grids of positions.

## Connections

Positional encodings matter for [attention variants](../attention-variants/index.md) because sparse and local patterns already encode some position through their structure. They also interact with [KV cache management](../kv-cache/index.md): evicting tokens from the middle of a sequence changes the positions that the remaining tokens expose to the model. The link to the brain is indirect. Recurrent positional encodings in trained Transformers can produce place-cell- and grid-cell-like representations, as discussed on the [Transformers & Attention](../index.md) page.

## Open issues and further variants

- **Length generalisation without fine-tuning.** Methods that extrapolate are still limited, and models often degrade well before the nominal limit. The exact causes are not settled.
- **Decoder-only models without explicit positions.** A causal mask alone lets a decoder infer order. Kazemnejad et al. (2023) studied when this works and found that it generalises well on some tasks and poorly on others.
- **Scaling choices.** The interpolation factor, the frequency bands and the attention temperature in YaRN-style methods are chosen by search. A principled rule for a target length is missing.
- **Two-dimensional and multimodal positions.** Extending RoPE to images, video and mixed text–image sequences is an active area, with several competing designs.
- **Position and memory.** Methods that keep a short window and summarise the rest raise the question of which positions to keep, and how to represent gaps in them.

## References

### Seminal papers

- Vaswani, A., et al. (2017). *Attention Is All You Need*. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) — Introduces sinusoidal position encodings added to the embeddings.
- Shaw, P., Uszkoreit, J. & Vaswani, A. (2018). "Self-Attention with Relative Position Representations". NAACL 2018. [arXiv:1803.02155](https://arxiv.org/abs/1803.02155) — Relative position vectors for clipped distances in self-attention.
- Su, J., et al. (2021). "RoFormer: Enhanced Transformer with Rotary Position Embedding". [arXiv:2104.09864](https://arxiv.org/abs/2104.09864) — Rotary position embedding, which makes the dot product depend only on relative position.
- Press, O., Smith, N. A. & Lewis, M. (2021). "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation". [arXiv:2108.12409](https://arxiv.org/abs/2108.12409) — ALiBi, a distance penalty on attention scores that extrapolates to longer inputs.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Chen, S., et al. (2023). "Extending Context Window of Large Language Models via Positional Interpolation". [arXiv:2306.15595](https://arxiv.org/abs/2306.15595) — Scales position indices to fit a longer context into the trained range, with brief fine-tuning.
- Peng, B., et al. (2023). "YaRN: Efficient Context Window Extension of Large Language Models". [arXiv:2309.00071](https://arxiv.org/abs/2309.00071) — Frequency-dependent interpolation and attention scaling for context extension.
- Kazemnejad, A., et al. (2023). "The Impact of Positional Encoding on Length Generalization in Transformers". NeurIPS. [arXiv:2305.19466](https://arxiv.org/abs/2305.19466) — Compares positional encodings for length generalisation, including no explicit encoding.
