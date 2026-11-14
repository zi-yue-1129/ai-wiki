"""Chromium tests for bilingual causal numerical demonstrations and static fallback."""
from pathlib import Path
import base64
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs/javascripts/causal-labs.js"
STYLE = ROOT / "docs/stylesheets/causal-labs.css"
ASSETS = ROOT / "docs/assets/concept-animations"
REVIEW = ROOT / "artifacts/causal-labs"

def html(lang):
    figures = []
    for name in ("backdoor-standardisation", "collider-selection"):
        fallback = base64.b64encode((ASSETS / (name + "-still.svg")).read_bytes()).decode("ascii")
        kind = "backdoor" if name.startswith("backdoor") else "collider"
        figures.append(f'<img alt="Static fallback" width="800" height="430" src="data:image/svg+xml;base64,{fallback}"><section class="causal-lab" data-causal-lab="{kind}" data-lang="{lang}"></section>')
    return f'<html lang="{lang}"><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><style>body{{margin:0;padding:12px;font:15px system-ui}}img{{max-width:100%;height:auto;display:block}}</style></head><body>' + "".join(figures) + "</body></html>"

def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        count = 0
        for lang in ("en","zh"):
            for width in (320,360,800,1024):
                for reduced in (False,True):
                    page = browser.new_page(viewport={"width":width,"height":930},
                        reduced_motion="reduce" if reduced else "no-preference")
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.set_content(html(lang))
                    page.add_style_tag(content=STYLE.read_text(encoding="utf-8"))
                    page.add_script_tag(content=SCRIPT.read_text(encoding="utf-8"))
                    assert not errors, errors
                    a,b=page.locator(".causal-lab").all()
                    assert page.locator('img[alt="Static fallback"]').count()==2
                    assert a.locator('[data-value="a"]').inner_text()=="0.30"
                    assert a.locator('[data-value="b"]').inner_text()=="0.70"
                    assert a.locator('[data-delta]').inner_text()=="+0.40"
                    assert b.locator('[data-value="a"]').inner_text()=="1.00"
                    assert b.locator('[data-value="b"]').inner_text()=="0.50"
                    assert b.locator('[data-delta]').inner_text()=="-0.50"
                    a.locator("[data-control]").fill("100")
                    assert a.locator('[data-value="a"]').inner_text()=="0.50"
                    assert a.locator('[data-value="b"]').inner_text()=="0.90"
                    assert a.locator('[data-delta]').inner_text()=="+0.40"
                    b.locator("[data-control]").fill("100")
                    assert b.locator('[data-delta]').inner_text()=="0.00"
                    b.locator("[data-control]").focus()
                    b.locator("[data-control]").press("ArrowLeft")
                    assert b.locator("[data-current]").inner_text()=="0.95"
                    a.locator("[data-reset]").click()
                    b.locator("[data-reset]").click()
                    assert a.locator("[data-current]").inner_text()=="0.50"
                    assert b.locator("[data-current]").inner_text()=="0.00"
                    assert a.locator("[data-control]").get_attribute("aria-valuetext")=="0.50"
                    assert page.evaluate("document.documentElement.scrollWidth") <= width+1
                    for lab in (a,b):
                        rect = lab.bounding_box()
                        assert rect["x"]>=0 and rect["width"]<=width, rect
                    if width in (320,1024) and not reduced:
                        page.screenshot(path=str(REVIEW/f"{lang}-{width}.png"),full_page=True)
                    page.close()
                    count += 1
        page = browser.new_page(java_script_enabled=False)
        page.set_content(html("en"))
        assert page.locator('img[alt="Static fallback"]').count()==2
        assert page.locator(".causal-lab-panel").count()==0
        assert page.locator("img").first.evaluate("(img) => img.naturalWidth")==800
        page.close()
        browser.close()
    print(f"PASS: {count} bilingual responsive/reduced-motion numerical cases + no-JS SVG fallback")

if __name__ == "__main__":
    main()
