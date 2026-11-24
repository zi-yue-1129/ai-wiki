#!/usr/bin/env python3
"""Render emergent-communication animations and test the real shared MkDocs player."""
from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets" / "concept-animations"
OUT = ROOT / "artifacts" / "emergent-communication"
STEMS = ("rial-dial-credit-path", "commnet-leave-one-out", "dial-dru-train-execute", "commnet-layer-iterations")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS), **kwargs)
    def log_message(self, *args):
        pass
    def do_GET(self):
        if urlparse(self.path).path == "/__concept_test__":
            html = """<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font:16px system-ui;margin:0;padding:8px;box-sizing:border-box}main{max-width:680px;margin:auto}</style>
<link rel="stylesheet" href="/stylesheets/concept-motion.css"><main>
<img alt="RIAL versus DIAL communication paths" src="/assets/concept-animations/rial-dial-credit-path-motion.svg">
<img alt="CommNet 排除自身訊息後的平均通訊" src="/assets/concept-animations/commnet-leave-one-out-motion.svg">
<img alt="DIAL 訓練與執行期間的訊息處理" src="/assets/concept-animations/dial-dru-train-execute-motion.svg">
<img alt="CommNet 多層訊息傳遞" src="/assets/concept-animations/commnet-layer-iterations-motion.svg">
</main><script src="/javascripts/concept-motion.js"></script></html>"""
            data=html.encode("utf-8")
            self.send_response(200);self.send_header("Content-Type","text/html;charset=utf-8")
            self.send_header("Content-Length",str(len(data)));self.end_headers();self.wfile.write(data)
        else:
            super().do_GET()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
    Thread(target=server.serve_forever,daemon=True).start()
    checks=0
    try:
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=True)
            for stem in STEMS:
                for width in (320,360,720,1024):
                    for time in (0.2,4.2,6.7,9.5,None):
                        page=browser.new_page(viewport={"width":width,"height":440})
                        file=ASSETS / f'{stem}-{"still" if time is None else "motion"}.svg'
                        svg=file.read_text(encoding="utf-8")
                        page.set_content(f'<html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{margin:0}}svg{{display:block;width:100vw;max-width:640px;height:auto}}</style>{svg}</html>')
                        if time is not None:
                            page.eval_on_selector("svg","(el,t)=>{el.pauseAnimations();el.setCurrentTime(t)}",time)
                        if stem == "commnet-layer-iterations" and time in (0.2, 6.7, 9.5):
                            reveals = page.eval_on_selector_all('svg > g[opacity="0"]', 'els=>els.map(e=>Number(getComputedStyle(e).opacity))')
                            expected = {0.2: [0, 0], 6.7: [1, 0], 9.5: [1, 1]}[time]
                            assert reveals == expected, (time, reveals, expected)
                        assert page.eval_on_selector("svg","el=>el.getBoundingClientRect().width") <= width+0.1
                        clipped=page.eval_on_selector_all("svg text", """nodes=>nodes.filter(el=>{const b=el.getBBox();return b.x < -1 || b.y < -1 || b.x+b.width>641 || b.y+b.height>361}).map(el=>el.textContent)""")
                        assert not clipped,(stem,width,time,clipped)
                        tag="still" if time is None else str(time).replace(".","-")
                        page.locator("svg").screenshot(path=str(OUT/f"{stem}-{width}-{tag}.png"))
                        page.close()
                        checks+=1
            url=f"http://127.0.0.1:{server.server_port}/__concept_test__"
            for reduced in (False,True):
                page=browser.new_page(viewport={"width":320,"height":800},reduced_motion="reduce" if reduced else "no-preference")
                page.goto(url)
                page.locator("button.concept-motion-toggle").first.wait_for()
                assert page.locator(".concept-motion-player").count()==4
                for i in range(len(STEMS)):
                    img=page.locator(".concept-motion-player img").nth(i)
                    button=page.locator("button.concept-motion-toggle").nth(i)
                    assert (img.get_attribute("src") or "").endswith("-still.svg" if reduced else "-motion.svg")
                    button.focus();page.keyboard.press("Enter")
                    assert (img.get_attribute("src") or "").endswith("-motion.svg" if reduced else "-still.svg")
                    button.focus();page.keyboard.press("Space")
                    assert (img.get_attribute("src") or "").endswith("-still.svg" if reduced else "-motion.svg")
                    checks+=1
                assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
                page.screenshot(path=str(OUT/f"player-reduced-{reduced}.png"),full_page=True)
                page.close()
            browser.close()
    finally:
        server.shutdown();server.server_close()
    print(f"PASS: {checks} rendered/interactivity checks, including 80 screenshots")

if __name__=="__main__":
    main()
