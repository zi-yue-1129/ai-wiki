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
# Only the calculated acceptance metrics are a live stage announcement.
# The title remains visible/readable, but cannot generate a second alert.
assert "note.setAttribute('aria-live', 'off')" in player
assert "calculation.setAttribute('aria-live', 'polite')" in player
assert "calculation.setAttribute('aria-atomic', 'true')" in player
assert "if (index !== announcedIndex)" in player
# A second click can arrive before the initial SVG fetch resolves. Only the
# latest intent may resume a pending handler; Chromium covers the actual race.
assert "makeLinkedPlot(filename, zh, chooseStage)" in player
assert "hit.setAttribute('role', 'button')" in player
assert "hit.setAttribute('tabindex', '0')" in player
assert "hit.addEventListener('keydown'" in player
assert "stageSelectors.forEach" in player
# Both plots expose bounded keyboard traversal as an alternative to pointer input.
assert "const keyboardStage = (key, index, last) =>" in player
assert "stageSelectors[target].focus()" in player
assert "classChoices[target].control.focus()" in player
assert "'ArrowRight'" in player and "'ArrowLeft'" in player
assert "'Home'" in player and "'End'" in player
# The class-conditional chart exposes two semantic, keyboard-selectable states.
assert "classChoices.forEach" in player
assert "Compare all accepted, 8/8" in player
assert "Compare selective acceptance, 5/8" in player
assert "control.setAttribute('aria-pressed'" in player
# Focus and selection are visually independent; never skip repainting the
# active keyboard button when its semantic acceptance state changes.
assert "const focused = document.activeElement === control" in player
assert "if (document.activeElement !== control) paint" not in player
assert "paint(i===index)" in player
assert "Accepted 5/8" in player and "接受 5/8" in player
# Exact non-monotonic synthetic risk for every integer cutoff, with the
# selectable animation scenes remaining k=2,4,6.
assert "const allAccepted = [1,2,3,4,5,6]" in player
assert "const allIncorrect = [0,0,1,1,2,2]" in player
assert "allAccepted.forEach((count,i) =>" in player
assert "'data-risk-k':count" in player
assert "const overall = write(116,155" in player
assert "overall.textContent=index===0?" in player
assert "let intentVersion = 0" in player
assert "intent !== intentVersion" in player
assert player.count("const intent = ++intentVersion") == 3
assert "++intentVersion; pause(); current = lesson.stops[1]" in player
# Hidden tabs cancel an in-flight Play intent, stop the running animation,
# and never fast-forward a large requestAnimationFrame gap on return.
assert "document.addEventListener('visibilitychange', onVisibilityChange)" in player
assert "document.removeEventListener('visibilitychange', onVisibilityChange)" in player
assert "if (document.hidden)" in player
assert "if (playing) pause();" in player
assert "intent !== intentVersion || document.hidden" in player
assert "Math.min(0.1, Math.max(0, (now - previous) / 1000))" in player
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
