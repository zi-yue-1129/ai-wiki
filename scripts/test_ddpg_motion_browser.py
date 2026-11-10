#!/usr/bin/env python3
"""Chromium visual/interaction regression for bilingual DDPG teaching motion.

Run after `pip install playwright && python -m playwright install chromium`.
"""
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
ART = ROOT / 'artifacts/ddpg-motion'
ART.mkdir(parents=True, exist_ok=True)
TOPICS = ('ddpg-actor-gradient', 'ddpg-polyak-target')
WIDTHS = (320, 360, 720, 1024)
TIMES = (0.3, 3.2, 6.1, 9.4)

def embed(path: Path):
    return '<!doctype html><html><body style="margin:0">' + path.read_text(encoding='utf-8').replace('<svg ', '<svg style="display:block;width:100%;height:auto" ', 1) + '</body></html>'

def visible_text_errors(page):
    return page.evaluate('''() => {
        const nodes=[...document.querySelectorAll('svg text')].filter(e=>getComputedStyle(e).display!=='none' && Number(getComputedStyle(e).opacity)>0.01);
        const a=nodes.map(e=>({t:e.textContent.trim(),b:e.getBBox()}));const err=[];
        for(let i=0;i<a.length;i++) {
          const p=a[i].b;
          if(p.x < -0.01 || p.y < -0.01 || p.x+p.width > 640.01 || p.y+p.height > 360.01)err.push('outside: '+a[i].t);
          for(let j=i+1;j<a.length;j++) {
            const q=a[j].b;
            if(Math.min(p.x+p.width,q.x+q.width)>Math.max(p.x,q.x)+1 && Math.min(p.y+p.height,q.y+q.height)>Math.max(p.y,q.y)+1)err.push('overlap: '+a[i].t+' <> '+a[j].t);
          }
        }
        return err;
      }''')

def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=shutil.which('chromium') or None, headless=True, args=['--no-sandbox'])
        try:
            for name in TOPICS:
                motion = ASSETS / f'{name}-motion.svg'; still = ASSETS / f'{name}-still.svg'
                for width in WIDTHS:
                    page = browser.new_page(viewport={'width':width,'height':round(width*360/640)})
                    for typ,time in [("motion",t) for t in TIMES]+[("still",None)]:
                        page.set_content(embed(motion if time is not None else still))
                        if time is not None:
                            page.evaluate('t => {const s=document.querySelector("svg");s.pauseAnimations();s.setCurrentTime(t)}', time)
                            assert page.evaluate('document.querySelector("svg").animationsPaused()')
                        errs = visible_text_errors(page)
                        assert not errs, f'{name}/{width}/{time}: {errs}'
                        page.screenshot(path=str(ART/f'{name}-{width}-{typ}-{time}.png'))
                    page.close()
                page=browser.new_page(reduced_motion='reduce', viewport={'width':640,'height':360})
                page.set_content(embed(motion))
                assert page.locator('.moving').first.evaluate('(e)=>getComputedStyle(e).display')=='none'
                assert page.locator('.complete').first.evaluate('(e)=>getComputedStyle(e).display')!='none'
                if name=='ddpg-polyak-target':
                    assert all(x=='1' for x in page.locator('.reveal').evaluate_all('(els)=>els.map(e=>getComputedStyle(e).opacity)'))
                page.screenshot(path=str(ART/f'{name}-reduced-motion.png'))
                page.close()
            print('DDPG Chromium: 40 screenshots, no visible text overlaps/cropping; pause/seek/reduced-motion passed')
        finally:
            browser.close()

if __name__ == '__main__':main()
