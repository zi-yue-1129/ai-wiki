#!/usr/bin/env python3
"""Validate looped SVG teaching animations, static fallbacks, and bilingual links.

stdlib-only check; rendered/browser validation is performed separately.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET

DOCS = Path("docs")
ASSETS = DOCS / "assets" / "concept-animations"
NS = "{http://www.w3.org/2000/svg}"
TOPICS = {
    "moe-top2-routing": "theory/models/mixture-of-experts/index",
    "cfg-extrapolation": "theory/paradigms/unsupervised/density-and-generative-models/diffusion/classifier-free-guidance",
    "gradient-norm-clipping": "theory/optimization/norm-clipping",
    "swin-shifted-windows": "theory/models/transformer/vision-transformer/swin/index",
    "deformable-sampling": "theory/models/cnn/convolution-variants/deformable-convolution/index",
    "speculative-decoding": "engineering/inference-optimization/speculative-decoding",
    "orca-continuous-batching": "engineering/inference-optimization/orca",
    "disaggregated-handoff": "engineering/inference-optimization/disaggregated-serving",
    "streaming-kv-eviction": "engineering/inference-optimization/kv-cache-compression",
    "mcts-search-cycle": "theory/paradigms/reinforcement-learning/mcts-and-self-play/index",
    "dqn-target-sync": "theory/paradigms/reinforcement-learning/deep-q-networks/index",
    "adamw-decoupled-paths": "theory/optimization/adaptive/adamw",
    "td3-delayed-twin-critics": "theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/td3/index",
    "ppo-clipped-objective": "theory/paradigms/reinforcement-learning/proximal-policy-optimisation/index",
    "prioritized-replay-cycle": "theory/paradigms/reinforcement-learning/experience-replay/index",
    "sam-two-gradient": "theory/optimization/sharpness-aware-minimisation",
    "lbfgs-two-loop": "theory/optimization/lbfgs",
    "nesterov-lookahead": "theory/optimization/sgd-and-momentum/nesterov",
    "hyperband-budget": "theory/optimization/hyperparameter-optimisation/hyperband",
    "qmix-monotonic-greedy": "theory/paradigms/reinforcement-learning/multi-agent-rl/qmix/index",
    "muzero-latent-planning": "theory/paradigms/reinforcement-learning/model-based-rl/muzero/index",
    "gru-gate-flow": "theory/models/rnn/gated-cells/gru/index",
    "kfac-factor-preconditioning": "theory/optimization/kfac/index",
    "maml-inner-outer-loop": "theory/paradigms/meta-learning/optimisation-based/maml",
    "alpha-beta-cutoff": "theory/paradigms/symbolic-ai/search/alpha-beta-pruning",
    "vae-reparameterisation": "theory/paradigms/unsupervised/density-and-generative-models/vae/index",
    "realnvp-affine-coupling": "theory/paradigms/unsupervised/density-and-generative-models/flow/normalising-flows/realnvp",
    "mh-accept-reject": "theory/paradigms/probabilistic/mcmc/metropolis-hastings",
    "hmc-leapfrog-trajectory": "theory/paradigms/probabilistic/mcmc/hamiltonian-monte-carlo",
    "astar-frontier": "theory/paradigms/symbolic-ai/search/a-star",
    "dpll-backtrack": "theory/paradigms/symbolic-ai/theorem-proving/dpll",
    "viterbi-trellis": "theory/paradigms/probabilistic/graphical-models/hidden-markov-models",
    "tree-belief-propagation": "theory/paradigms/probabilistic/graphical-models/belief-propagation",
}
FORBIDDEN = {"script", "foreignObject", "iframe", "image"}
LIMIT = 50 * 1024


def verify_svg(path: Path, animated: bool) -> list[str]:
    errors = []
    if not path.is_file():
        return [f"{path}: missing"]
    if path.stat().st_size > LIMIT:
        errors.append(f"{path}: exceeds {LIMIT} bytes")
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [f"{path}: invalid XML: {exc}"]
    if root.tag != NS + "svg" or root.get("viewBox") != "0 0 640 360":
        errors.append(f"{path}: invalid SVG root/viewBox")
    for label in ("title", "desc"):
        if root.find(NS + label) is None:
            errors.append(f"{path}: missing accessible {label}")
    motions = []
    for element in root.iter():
        name = element.tag.split("}")[-1]
        if name in FORBIDDEN:
            errors.append(f"{path}: prohibited {name}")
        if name in ("animate", "animateMotion"):
            motions.append(element)
            if element.get("repeatCount") != "indefinite":
                errors.append(f"{path}: animation must loop indefinitely")
            if not element.get("dur", "").endswith("s"):
                errors.append(f"{path}: animation requires a duration in seconds")
        for key, value in element.attrib.items():
            local_key = key.split("}")[-1]
            if local_key.startswith("on"):
                errors.append(f"{path}: event handler prohibited")
            if local_key == "href" and (
                "://" in value or value.startswith(("data:", "javascript:"))
            ):
                errors.append(f"{path}: external or active asset reference")
    if animated and not motions:
        errors.append(f"{path}: no animation found")
    if not animated and motions:
        errors.append(f"{path}: still fallback contains animation")
    return errors


def main() -> int:
    errors = []
    for stem, page_stem in TOPICS.items():
        animated_path = ASSETS / f"{stem}-motion.svg"
        static_path = ASSETS / f"{stem}-still.svg"
        errors.extend(verify_svg(animated_path, True))
        errors.extend(verify_svg(static_path, False))
        if stem == "moe-top2-routing":
            errors.extend(verify_svg(ASSETS / "moe-top2-routing-token-b.svg", False))
        for suffix in (".md", ".zh-TW.md"):
            page = DOCS / (page_stem + suffix)
            if not page.is_file():
                errors.append(f"{page}: missing translation")
                continue
            text = page.read_text(encoding="utf-8")
            links = re.findall(r"!\[[^]]+\]\(([^)]+\.svg)\)", text)
            if animated_path.resolve() not in {
                (page.parent / link).resolve() for link in links
            }:
                errors.append(f"{page}: missing or incorrect animated SVG link")
            if stem in {"moe-top2-routing", "swin-shifted-windows", "deformable-sampling", "speculative-decoding", "orca-continuous-batching", "disaggregated-handoff", "streaming-kv-eviction", "mcts-search-cycle", "dqn-target-sync", "adamw-decoupled-paths", "td3-delayed-twin-critics", "ppo-clipped-objective", "prioritized-replay-cycle", "sam-two-gradient", "lbfgs-two-loop", "nesterov-lookahead", "hyperband-budget", "qmix-monotonic-greedy", "muzero-latent-planning", "gru-gate-flow", "kfac-factor-preconditioning", "maml-inner-outer-loop", "alpha-beta-cutoff", "vae-reparameterisation", "realnvp-affine-coupling", "astar-frontier", "dpll-backtrack", "viterbi-trellis", "tree-belief-propagation", "mh-accept-reject", "hmc-leapfrog-trajectory"}:
                static_links = re.findall(r"\[[^]]+\]\(([^)]+\.svg)\)", text)
                linked = {(page.parent / link).resolve() for link in static_links}
                fallbacks = (static_path, ASSETS / "moe-top2-routing-token-b.svg") if stem == "moe-top2-routing" else (static_path,)
                for fallback in fallbacks:
                    if fallback.resolve() not in linked:
                        errors.append(f"{page}: missing GitHub-readable fallback link {fallback.name}")
            if "CC BY-SA 4.0" not in text:
                errors.append(f"{page}: missing original-diagram attribution")
        print(
            f"Motion pair {stem}: "
            f"{animated_path.stat().st_size if animated_path.exists() else '-'} / "
            f"{static_path.stat().st_size if static_path.exists() else '-'} bytes"
        )
    config = Path("mkdocs.yml").read_text(encoding="utf-8")
    for path in (
        "javascripts/concept-motion.js",
        "stylesheets/concept-motion.css",
    ):
        if path not in config or not (DOCS / path).exists():
            errors.append(f"Missing registered player asset: {path}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"Checked {len(TOPICS)} motion/still pairs and bilingual pages: {len(errors)} error(s)")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
