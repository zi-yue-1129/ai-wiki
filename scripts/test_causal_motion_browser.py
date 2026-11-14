"""Chromium regression for the two bilingual causal inference SVG pairs."""
from pathlib import Path
from tempfile import TemporaryDirectory
from html import escape
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
SCRIPT = ROOT / "docs/javascripts/concept-motion.js"
PAIRS = ("backdoor-standardisation", "collider-selection")


def exercise(page, name, chinese, reduced, width, html_file):
    still = (ASSETS / (name + "-still.svg")).as_uri()
    animated = (ASSETS / (name + "-motion.svg")).as_uri()
    alt = "連續因果教學動畫" if chinese else "Continuous causal teaching animation"
    html_file.write_text(f"""<!doctype html><meta charset="utf-8"><style>
    body {{padding:0;margin:8px;font-family:system-ui}}
    .figure {{overflow-x:auto;max-width:100%;width:100%;box-sizing:border-box}}
    .figure img {{display:block;width:800px;max-width:none;height:auto}}
    </style><div class="figure" tabindex="0" role="group" aria-label="Causal diagram">
    <img src="{escape(still)}" data-motion-src="{escape(animated)}"
         alt="{alt}" width="800" height="430"></div>
    <script src="{SCRIPT.as_uri()}"></script>""", encoding="utf-8")
    page.goto(html_file.as_uri())
    img = page.locator(".figure img")
    toggle = page.locator(".concept-motion-toggle")
    toggle.wait_for()
    assert img.evaluate("(el) => [el.naturalWidth,el.naturalHeight]") == [800,430]
    src = img.get_attribute("src")
    assert src.endswith("-still.svg" if reduced else "-motion.svg"), (src,reduced)
    assert toggle.count() == 1 and toggle.get_attribute("aria-label")
    if reduced:
        toggle.click()
        assert img.get_attribute("src").endswith("-motion.svg")
    else:
        toggle.focus()
        toggle.press("Space")
        assert img.get_attribute("src").endswith("-still.svg"), "Space must pause"
        toggle.press("Enter")
        assert img.get_attribute("src").endswith("-motion.svg"), "Enter must resume"
    metrics = page.locator(".figure").evaluate(
        "el => ({scroll:el.scrollWidth,client:el.clientWidth})")
    if width <= 360:
        assert metrics["scroll"] > metrics["client"],metrics
        page.locator(".figure").focus()
        page.keyboard.press("End")
    else:
        assert metrics["scroll"] >= metrics["client"]


def main():
    for name in PAIRS:
        for suffix in ("-motion.svg","-still.svg"):
            root=ET.parse(ASSETS/(name+suffix)).getroot()
            assert root.attrib["viewBox"] == "0 0 800 430"
            assert not any(
                "http://" in str(x.attrib) or "https://" in str(x.attrib)
                for x in root.iter())
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        with TemporaryDirectory() as tmp:
            html_file=Path(tmp)/"case.html"
            for name in PAIRS:
                for chinese in (False,True):
                    for width in (320,800):
                        page=browser.new_page(
                            viewport={"width":width,"height":560},
                            reduced_motion="no-preference")
                        exercise(page,name,chinese,False,width,html_file)
                        page.close()
                    page=browser.new_page(
                        viewport={"width":320,"height":560},
                        reduced_motion="reduce")
                    exercise(page,name,chinese,True,320,html_file)
                    page.close()
                page=browser.new_page(
                    java_script_enabled=False,viewport={"width":360,"height":560})
                html_file.write_text(
                    f'<img src="{(ASSETS/(name+"-still.svg")).as_uri()}" alt="Static fallback">',
                    encoding="utf-8")
                page.goto(html_file.as_uri())
                assert page.locator("img").evaluate("(e)=>e.naturalWidth") == 800
                assert page.locator(".concept-motion-toggle").count() == 0
                page.close()
        browser.close()
    print("PASS: 12 bilingual/motion/reduced-motion checks + 2 no-JS fallbacks")

if __name__ == "__main__":
    main()
