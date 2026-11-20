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
# Each hollow intermediate risk point is inspectable by keyboard and pointer.
# The inspector shows the exact cumulative error ratio and finite difference
# to the previous integer cutoff, without selecting an unsupported SVG scene.
assert "viewBox:riskPlot?'0 0 640 208':'0 0 640 260'" in player
# Preserve 640px chart typography on phones; native horizontal scrolling belongs
# to the focusable figure. width:100% made 12px labels ~6px at 320px.
assert "width:640px;min-width:640px;max-width:none" in player
assert "'data-risk-inspection':'true'" in player
assert "const showInspection = (count, fromHover = false) =>" in player
assert "const restoreInspection = () =>" in player
assert "dot.setAttribute('role','button')" in player
assert "dot.setAttribute('tabindex','0')" in player
assert "dot.setAttribute('cursor','help')" in player
assert "const deltaWords = count === 1 ?" in player
assert "選擇性風險 " in player
assert "percentage points" in player
assert "dot.addEventListener('focus'" in player
assert "dot.addEventListener('keydown'" in player
assert "dot.addEventListener('click', () => showInspection(count))" in player
assert "'data-risk-touch-k':count" in player
assert "'aria-hidden':'true'" in player
assert "dot.focus(); showInspection(count)" in player
assert "plot.insertBefore(hit, anchor.nextSibling)" in player
assert "if (inspecting === null) restoreInspection()" in player
assert "return 'k=' + count + ' · +' + (newError ? 'WRONG' : 'CORRECT') +" in player
assert "' wrong · ' + fmt(risk * 100) + '% · ' + delta" in player
assert "const newError = errors - (count > 1 ? allIncorrect[count - 2] : 0)" in player
assert "' · +' + (newError ? 'WRONG' : 'CORRECT')" in player
assert "新增' + (newError ? '錯誤' : '正確')" in player
assert "'incorrect' : 'correct'" in player
assert "fmt(Math.abs(change) * 100) + ' pp'" in player
# Keyboard focus pins the mathematical inspector during scroll-induced hover;
# pointer-only events must not steal focus or overwrite the HUD.
assert "const focusedRiskCount = () =>" in player
assert "plot.contains(active)" in player
assert "fromHover && focused !== null && focused !== count" in player
assert "showInspection(focusedRiskCount() ?? accepted[activeRiskIndex])" in player
assert "showInspection(accepted[i], true)" in player
assert "const overall = write(116,155" in player
assert "'data-class-gap':'true'" in player
assert "'data-rejected-metrics':'true'" in player
assert "'data-correct-balance':'true'" in player
assert "'data-wrong-balance':'true'" in player
assert "rightBalance.textContent = 'RIGHT 6 = ' + keptCorrect" in player
assert "wrongBalance.textContent = 'WRONG 2 = ' + keptWrong" in player
assert "const rejectedCount = 8 - (positive + 4)" in player
assert "const keptCorrect = index === 0 ? 6 : 5" in player
assert "const rejectedCorrect = 6 - keptCorrect" in player
assert "const keptWrong = positive + 4 - keptCorrect" in player
assert "rejectedWrong = rejectedCount - rejectedCorrect" in player
assert "rejectedCount === 0" in player
assert "rejected-only accuracy is undefined" in player
assert "拒答樣本正確率未定義" in player
assert "const gapPp = Math.abs(positive / 4 - 1) * 100" in player
assert "gap.textContent = 'GAP ' + gapPp + ' pp'" in player
assert "absolute class coverage gap" in player and "類別覆蓋差距" in player
# The SVG writer must return its text node; Element.append() returns undefined.
# Otherwise the live OVERALL ratio throws on first update and restores the still.
assert "plot.append(text);" in player and "return text;" in player
assert "img.style.setProperty('display', 'none', 'important')" in player
assert "if (svg) { svg.remove(); svg = null; }" in player
assert "if (linkedPlot) { linkedPlot.element.remove(); linkedPlot = null; }" in player
assert "fallbackDisplayPriority" in player
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
assert "hover, tap/click, or keyboard-focus the hollow" in en
assert "does **not** change the main SVG" in en
assert "all six discrete cutoffs" in en
assert "空心的 k=1、3、5 資料點" in zh
assert "完整顯示六個整數門檻" in zh
assert "R_k-R_{k-1}" in en and "R_k-R_{k-1}" in zh
assert "$k=0$" in en and "$k=0$" in zh
assert "undefined" in en and "未定義" in zh
assert "75 percentage points" in en and "75 個百分點" in zh
assert "**REJECTED**" in en and "**REJECTED（拒答）**" in zh
assert "**0/8**" in en and "**0/8**" in zh
assert "**3/8**" in en and "**3/8**" in zh
assert "**2/3" in en and "**2/3" in zh
assert "conservation of outcomes" in en and "守恆分解" in zh
assert "\\Delta_C" in en and "\\Delta_C" in zh
assert "+CORRECT" in en and "+WRONG" in zh
assert "interactive cutoff player" in en and "interactive class-coverage player" in en
assert "互動門檻播放器" in zh and "各類別覆蓋率互動播放器" in zh
assert "0.5×" in en and "0.5×" in zh
assert "Reduced-motion" in en or "reduced-motion" in en
assert "減少動態效果" in zh
print("Selective player source, safety, localized Markdown and asset contracts OK")
