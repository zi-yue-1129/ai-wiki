"""Selective-classification interactive-player integration and safety contract.

These are source/integration checks. Real browser behavior is separately exercised
in QA; this file does not claim to replace MkDocs or Chromium E2E checks.
"""
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "docs/javascripts"
ASSETS = ROOT / "docs/assets/concept-animations"
DOCS = ROOT / "docs/theory/evaluation/metrics/classification"
player = (SCRIPTS / "selective-accuracy-player.js").read_text(encoding="utf-8")
config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

# Dedicated reviewed player gets first access; the generic player must never
# insert a second Play/Pause bar for the same <img>.
assert config.count("javascripts/selective-accuracy-player.js") == 1
assert config.index("javascripts/selective-accuracy-player.js") < config.index(
    "javascripts/concept-motion.js"
)
assert "javascripts/concept-motion-detailed.js" in config
assert "stylesheets/concept-motion-detailed.css" in config
assert "img.dataset.conceptMotionEnhanced = 'yes'" in player

# Only same-origin, repository-owned SVGs may be inlined. The original static
# <img> must survive disabled JavaScript, failed network loads and GitHub previews.
for required in (
    "new URL(source, document.baseURI)",
    "url.origin !== location.origin",
    "/assets/concept-animations/",
    "fetch(url.href, {credentials:'same-origin'})",
    "new DOMParser()",
    "validate(doc.documentElement)",
    "blocked.has(node.localName)",
    "if (/^on/i.test(attr.name) || /href$/i.test(attr.name))",
    "img.hidden = false",
    "svg.pauseAnimations()",
    "svg.setCurrentTime(current)",
    "cancelAnimationFrame(frame)",
    "requestAnimationFrame(tick)",
    "reduced.addEventListener",
    "status.setAttribute('role', 'status')",
    "slider.setAttribute('aria-valuetext'",
    "current = target",
    "if (!host.isConnected)",
):
    assert required in player, required
assert "innerHTML" not in player and "eval(" not in player
# A second click can arrive before the initial SVG fetch resolves. Only the
# latest intent may resume a pending handler; Chromium covers the actual race.
assert "let intentVersion = 0" in player
assert "intent !== intentVersion" in player
assert player.count("const intent = ++intentVersion") == 3
assert "++intentVersion; pause(); current = lesson.stops[1]" in player
workflow = (ROOT / ".github/workflows/concept-animation-validation.yml").read_text(encoding="utf-8")
assert "python scripts/test_selective_player_race_browser.py" in workflow

cases = {
    "accuracy-selective-coverage": ("12s", [0, 4, 8], ["2/6", "4/6", "6/6"]),
    "accuracy-selective-class-coverage": ("8s", [0, 4], ["6/8", "5/5"]),
}
ns = "{http://www.w3.org/2000/svg}"
for name, (duration, stops, values) in cases.items():
    assert ("'" + name + "-motion.svg'") in player
    for time in stops:
        assert str(time) in player
    motion = ET.parse(ASSETS / (name + "-motion.svg")).getroot()
    still = ET.parse(ASSETS / (name + "-still.svg")).getroot()
    assert motion.get("viewBox") == still.get("viewBox") == "0 0 640 360"
    assert any(e.tag == ns + "animate" and e.get("dur") == duration
               for e in motion.iter()), name
    assert not any(e.tag in (ns + "animate", ns + "script", ns + "foreignObject")
                   for e in still.iter()), name
    for language in ("accuracy.md", "accuracy.zh-TW.md"):
        page = (DOCS / language).read_text(encoding="utf-8")
        assert 'data-motion-src="../../../../assets/concept-animations/' + name + '-motion.svg"' in page
        assert 'data-still-src="../../../../assets/concept-animations/' + name + '-still.svg"' in page
        assert "[GitHub" in page or "[GitHub" in page
    for fraction in values:
        assert fraction in player, (name, fraction)

en = (DOCS / "accuracy.md").read_text(encoding="utf-8")
zh = (DOCS / "accuracy.zh-TW.md").read_text(encoding="utf-8")
assert "interactive cutoff player" in en and "interactive class-coverage player" in en
assert "互動門檻播放器" in zh and "各類別覆蓋率互動播放器" in zh
assert "0.5×" in en and "0.5×" in zh
assert "Reduced-motion" in en or "reduced-motion" in en
assert "減少動態效果" in zh
print("Selective player source, safety, localized Markdown and asset contracts OK")
