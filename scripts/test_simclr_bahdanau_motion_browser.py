#!/usr/bin/env python3
"""Chromium QA: actual SVG timelines and bilingual static-first MkDocs controls."""
from __future__ import annotations
import os
import re
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets" / "concept-animations"
OUT = ROOT / "artifacts" / "simclr-bahdanau-motion"
TOPICS = {
    "simclr-temperature-competition": "theory/paradigms/self-supervised/contrastive-learning/simclr",
    "bahdanau-alignment-context": "theory/models/transformer/bahdanau-attention/index",
}

def assert_svg(stem):
    for kind in ("motion", "still"):
        path = ASSETS / f"{stem}-{kind}.svg"
        assert path.is_file() and path.stat().st_size < 50000, path
        root = ET.parse(path).getroot()
        ns = "{http://www.w3.org/2000/svg}"
        assert root.tag == ns + "svg" and root.get("viewBox") == "0 0 640 360"
        assert root.find(ns+"title") is not None and root.find(ns+"desc") is not None
        anim = [e for e in root.iter() if e.tag == ns+"animate"]
        assert bool(anim) == (kind == "motion"), path
        for e in root.iter():
            assert e.tag.split("}")[-1] not in {"script", "foreignObject", "iframe", "image"}
            assert all(not k.split("}")[-1].startswith("on") for k in e.attrib)
            assert not any("javascript:" in v or "http://" in v or "https://" in v for v in e.attrib.values())
        for e in anim:
            assert e.get("repeatCount") == "indefinite" and e.get("dur") == "12s"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem in TOPICS: assert_svg(stem)
    cases = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_EXECUTABLE"))
        js = (DOCS/"javascripts"/"concept-motion.js").read_text("utf-8")
        css = (DOCS/"stylesheets"/"concept-motion.css").read_text("utf-8")
        for stem in TOPICS:
            for kind in ("motion", "still"):
                markup = (ASSETS/f"{stem}-{kind}.svg").read_text("utf-8")
                for width in (320, 360, 720, 1024):
                    for time in ((0, 3, 6, 9, 11.5) if kind == "motion" else (0,)):
                        page = browser.new_page(viewport={"width":width,"height":500})
                        page.set_content('<html><body style="margin:0">'+markup+'</body></html>')
                        if kind == "motion":
                            page.evaluate('(s)=>document.querySelector("svg").setCurrentTime(s)', time)
                        bounds = page.evaluate("""() => [...document.querySelectorAll('svg text')].map(el => {
                            const b=el.getBBox();return [b.x,b.y,b.width,b.height];
                        })""")
                        assert all(x>=-.5 and y>=-.5 and x+w<=640.5 and y+h<=360.5 for x,y,w,h in bounds), (stem,kind,width,time,bounds)
                        if width in (320,720):
                            page.screenshot(path=str(OUT/f"{stem}-{kind}-{width}-{time}.png"))
                        page.close(); cases+=1
            for lang in (".md",".zh-TW.md"):
                page_path = DOCS/(TOPICS[stem]+lang)
                markdown = page_path.read_text("utf-8")
                match = re.search(r'<img\s+[^>]*data-motion-src=[^>]*>',markdown)
                assert match, page_path
                image = match.group()
                assert stem+"-still.svg" in image and stem+"-motion.svg" in image
                assert "CC BY-SA 4.0" in markdown
                for reduced in (False,True):
                    for width in (320,360,720,1024):
                        context = browser.new_context(viewport={"width":width,"height":520},reduced_motion="reduce" if reduced else "no-preference")
                        page = context.new_page()
                        base = f'https://qa.example/docs/{page_path.parent.relative_to(DOCS)}/__qa__.html'
                        html = f'''<!doctype html><html><head><base href="{base}"><style>{css}
body{{margin:0;padding:8px;font-family:Arial}} .scroll{{max-width:100%;overflow-x:auto;overscroll-behavior-x:contain}}</style></head><body><div class="scroll" tabindex="0"><div style="width:640px">{image}</div></div></body></html>'''
                        def intercept(route):
                            name = Path(urlparse(route.request.url).path).name
                            file = ASSETS/name
                            if file.is_file() and name.endswith(".svg"):
                                route.fulfill(status=200,content_type="image/svg+xml",body=file.read_bytes())
                            else:
                                route.abort()
                        page.route("**/assets/concept-animations/*.svg",intercept)
                        page.set_content(html)
                        page.add_script_tag(content=js)
                        page.locator("img").evaluate("(img)=>img.decode()")
                        button = page.locator(".concept-motion-toggle")
                        assert button.count()==1,(stem,lang,width)
                        src = page.locator("img").get_attribute("src")
                        assert src.endswith("-still.svg" if reduced else "-motion.svg"),(stem,lang,width,src)
                        if width<640:
                            dims = page.locator(".scroll").evaluate("(e)=>({client:e.clientWidth,scroll:e.scrollWidth,focusable:e.tabIndex})")
                            assert dims["client"]<dims["scroll"] and dims["focusable"]==0,(stem,lang,dims)
                        button.focus();page.keyboard.press("Space")
                        assert page.locator("img").get_attribute("src").endswith("-motion.svg" if reduced else "-still.svg")
                        button.focus();page.keyboard.press("Enter")
                        assert page.locator("img").get_attribute("src")==src
                        page.locator("img").evaluate("(img)=>img.decode()")
                        assert page.locator("img").evaluate("(img)=>img.naturalWidth")==640
                        if width==320:page.screenshot(path=str(OUT/f'{stem}-{lang.strip(".")}-reduced{reduced}.png'))
                        context.close();cases+=1
        browser.close()
    print(f"SimCLR/Bahdanau browser QA: {cases} cases passed")

if __name__=="__main__":main()
