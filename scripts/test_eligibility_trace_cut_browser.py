"""Chromium semantic and accessibility regression for tabular eligibility traces."""
from __future__ import annotations
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets/concept-animations"
OUT = ROOT / "artifacts/eligibility-trace-cut"
NS = "{http://www.w3.org/2000/svg}"

def main() -> None:
    motion = ASSETS / "eligibility-trace-cut-motion.svg"
    still = ASSETS / "eligibility-trace-cut-still.svg"
    for asset in (motion, still):
        root = ET.parse(asset).getroot()
        assert root.get("viewBox") == "0 0 440 598"
        for el in root.iter():
            assert el.tag.split("}")[-1] not in {"script", "image", "foreignObject", "iframe"}
            for k,v in el.attrib.items():
                assert not k.split("}")[-1].startswith("on")
                assert not v.startswith(("javascript:", "http:", "https:", "data:"))
    animated = ET.parse(motion).getroot()
    static = ET.parse(still).getroot()
    assert len(animated.findall(".//"+NS+"animate")) >= 7
    assert not static.findall(".//"+NS+"animate")
    assert {"0.52","0.72","1.00","0.00"}.issubset({(e.text or "").strip() for e in static.iter()})
    for topic in ("sarsa","q-learning"):
        for lang in ("index.md","index.zh-TW.md"):
            page = ROOT / "docs/theory/paradigms/reinforcement-learning/value-based-methods" / topic / lang
            chapter = page.read_text(encoding="utf-8")
            assert "eligibility-trace-cut-still.svg" in chapter and "eligibility-trace-cut-motion.svg" in chapter
            assert "Sutton" in chapter
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        opts = {"headless":True,"args":["--no-sandbox"]}
        if os.environ.get("CHROMIUM_EXECUTABLE"):
            opts["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
        browser = p.chromium.launch(**opts)
        for width in (320,360,720,1024):
            for sec in (.7,4.6,8.4,10.6):
                page = browser.new_page(viewport={"width":width,"height":max(900,width*2)})
                page.set_content('<style>body{margin:0}svg{display:block;width:100%;height:auto}</style>'+motion.read_text(encoding="utf-8"))
                page.locator("svg").evaluate("(el,t)=>{el.pauseAnimations();el.setCurrentTime(t)}",sec)
                assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
                boxes = page.locator("svg text").evaluate_all("els=>els.map(e=>{let b=e.getBBox();return [b.x,b.y,b.width,b.height]})")
                assert all(x>=-.5 and y>=-.5 and x+w<=440.5 and y+h<=598.5 for x,y,w,h in boxes), (width,sec)
                def bar(y:int,c:str)->float:
                    return page.locator(f'svg rect[y="{y}"][fill="{c}"]').evaluate("e=>e.getBBox().width")
                if sec==.7:
                    assert bar(229,"#159f89")>250 and bar(429,"#e49a39")>250
                if sec==4.6:
                    assert 175<bar(229,"#159f89")<190 and bar(270,"#159f89")>250
                if sec>=8.4:
                    assert 125<bar(229,"#159f89")<140 and 175<bar(270,"#159f89")<190
                    assert bar(311,"#159f89")>250
                    assert bar(429,"#e49a39")<1 and bar(470,"#e49a39")<1
                    assert bar(511,"#e49a39")>250
                page.locator("svg").screenshot(path=str(OUT/f'motion-{width}-{str(sec).replace(".","_")}.png'))
                page.close()
            page = browser.new_page(viewport={"width":width,"height":max(900,width*2)})
            page.set_content('<style>body{margin:0}svg{width:100%;height:auto}</style>'+still.read_text(encoding="utf-8"))
            assert page.locator("svg animate").count()==0
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
            page.locator("svg").screenshot(path=str(OUT/f'still-{width}.png'))
            page.close()
        player = (ROOT/"docs/javascripts/concept-motion.js").read_text(encoding="utf-8")
        host = "https://local.invalid/concept-animations/"
        for alt in ("Eligibility traces for a non-greedy action","非貪婪動作的資格跡比較"):
            for mode in ("no-preference","reduce"):
                context = browser.new_context(reduced_motion=mode)
                pg=context.new_page()
                pg.route(host+"**",lambda route:route.fulfill(
                    body=motion.read_text(encoding="utf-8") if "-motion.svg" in route.request.url else still.read_text(encoding="utf-8"),
                    content_type="image/svg+xml"))
                pg.set_content(f'<img alt="{alt}" src="{host}eligibility-trace-cut-still.svg" '
                               f'data-motion-src="{host}eligibility-trace-cut-motion.svg" '
                               f'data-still-src="{host}eligibility-trace-cut-still.svg">')
                pg.add_script_tag(content=player)
                button=pg.locator(".concept-motion-toggle")
                button.wait_for(state="visible",timeout=8000)
                expected="-motion.svg" if mode=="no-preference" else "-still.svg"
                assert expected in pg.locator("img").get_attribute("src")
                button.focus()
                pg.keyboard.press("Enter")
                opposite="-still.svg" if mode=="no-preference" else "-motion.svg"
                assert opposite in pg.locator("img").get_attribute("src")
                button.focus()
                pg.keyboard.press("Space")
                assert expected in pg.locator("img").get_attribute("src")
                context.close()
        browser.close()
    print("PASS: 20 screenshots; trace decay/cut, bilingual keyboard, reduced motion")

if __name__=="__main__":
    main()
