#!/usr/bin/env python3
"""Real Chromium visual and bilingual player checks for REINFORCE / GRPO."""
from pathlib import Path
from shutil import which
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
JS = ROOT / "docs/javascripts/concept-motion.js"
CSS = ROOT / "docs/stylesheets/concept-motion.css"
STEMS = ["reinforce-return-credit", "grpo-group-advantages"]

def check_svg(page, stem, kind):
    page.set_content((ASSETS / f"{stem}-{kind}.svg").read_text(encoding="utf-8"),
                     wait_until="domcontentloaded")
    for t in ([0, 2, 4, 6, 9, 11] if kind == "motion" else [0]):
        if kind == "motion":
            page.evaluate('(t) => document.querySelector("svg").setCurrentTime(t)', t)
        boxes = page.evaluate("""() => Array.from(document.querySelectorAll('svg text')).map(e => {
          const b=e.getBBox(); return {label:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height};
        })""")
        for b in boxes:
            assert b["x"] >= -2 and b["y"] >= -2, (stem, kind, t, b)
            assert b["x"] + b["w"] <= 762 and b["y"] + b["h"] <= 402, (stem, kind, t, b)
        for i, a in enumerate(boxes):
            for b in boxes[i+1:]:
                dx = max(0, min(a["x"]+a["w"],b["x"]+b["w"])-max(a["x"],b["x"]))
                dy = max(0, min(a["y"]+a["h"],b["y"]+b["h"])-max(a["y"],b["y"]))
                assert dx <= 3 or dy <= 3, (stem, kind, t, a["label"], b["label"])

def check_player(browser, stem, lang, width, reduced=False):
    context=browser.new_context(viewport={"width":width,"height":550},
              reduced_motion="reduce" if reduced else "no-preference")
    page=context.new_page()
    base="https://aiwiki.test/assets/concept-animations/"
    def route_svg(route):
        name=route.request.url.split("/")[-1]
        assert name in (f"{stem}-still.svg",f"{stem}-motion.svg"), name
        route.fulfill(status=200, content_type="image/svg+xml", body=(ASSETS/name).read_bytes())
    page.route("https://aiwiki.test/assets/concept-animations/*",route_svg)
    alt=("回報與群組優勢動畫" if lang=="zh" else "Policy gradient animation")
    html=f"""<main style="max-width:100%;padding:8px">
    <div role="region" tabindex="0" aria-label="Scroll horizontally to inspect"
         style="max-width:100%;overflow-x:auto">
      <img style="width:760px;max-width:none;height:auto"
           src="{base}{stem}-still.svg"
           data-motion-src="{base}{stem}-motion.svg"
           data-still-src="{base}{stem}-still.svg" alt="{alt}">
    </div></main>"""
    page.set_content(html,wait_until="domcontentloaded")
    page.add_style_tag(content=CSS.read_text(encoding="utf-8"))
    page.add_script_tag(content=JS.read_text(encoding="utf-8"))
    img=page.locator("img")
    button=page.locator("button.concept-motion-toggle")
    button.wait_for(timeout=5000)
    assert img.evaluate("(i)=>i.complete && i.naturalWidth===760")
    assert button.count()==1
    assert img.get_attribute("src").endswith("-still.svg" if reduced else "-motion.svg")
    region=page.locator('[role=region]')
    dimensions=region.evaluate("(e)=>({client:e.clientWidth,scroll:e.scrollWidth})")
    if width<=360:
        assert dimensions["scroll"]>=760 and dimensions["scroll"]>dimensions["client"], dimensions
        region.focus()
        region.evaluate("(e)=>{e.scrollLeft=e.scrollWidth-e.clientWidth}")
        assert region.evaluate("(e)=>e.scrollLeft>0")
    button.click()
    assert img.get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg")
    button.focus()
    page.keyboard.press("Enter")
    assert img.get_attribute("src").endswith("-still.svg" if reduced else "-motion.svg")
    button.focus()
    page.keyboard.press("Space")
    assert img.get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg")
    if not img.get_attribute("src").endswith("-still.svg"):
        button.click()
    assert img.get_attribute("src").endswith("-still.svg")
    assert img.evaluate("(i)=>i.complete && i.naturalWidth===760")
    context.close()

def main():
    count=0
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=which("chromium") or None)
        for stem in STEMS:
            page=browser.new_page(viewport={"width":760,"height":400})
            for kind in ("motion","still"):
                check_svg(page,stem,kind)
                count+=1
            page.close()
            for lang in ("en","zh"):
                for width in (320,360,720,1024):
                    check_player(browser,stem,lang,width)
                    count+=1
                check_player(browser,stem,lang,320,reduced=True)
                count+=1
        browser.close()
    print(f"Policy-gradient motion Chromium checks: {count} successful cases")

if __name__=="__main__":
    main()
