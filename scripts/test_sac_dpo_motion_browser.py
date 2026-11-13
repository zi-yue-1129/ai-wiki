#!/usr/bin/env python3
"""Browser integration for bilingual SAC/DPO motion, static fallback and mobile scroll.

Run from the repository root after `python -m playwright install chromium`.
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
CSS = ROOT / 'docs/stylesheets/concept-motion.css'
JS = ROOT / 'docs/javascripts/concept-motion.js'
TOPICS = ('sac-entropy-temperature', 'dpo-preference-margin')
SVG_NS = '{http://www.w3.org/2000/svg}'


def verify_assets():
    for stem in TOPICS:
        for variant in ('motion', 'still'):
            path = ASSETS / f'{stem}-{variant}.svg'
            root = ET.parse(path).getroot()
            assert root.tag == SVG_NS + 'svg'
            assert root.get('viewBox') == '0 0 760 420'
            assert root.find(SVG_NS+'title') is not None
            assert root.find(SVG_NS+'desc') is not None
            nodes = [n for n in root.iter() if n.tag == SVG_NS + 'animate']
            assert bool(nodes) is (variant == 'motion')
            assert all(n.get('repeatCount') == 'indefinite' for n in nodes)
            assert all('://' not in v and not v.startswith(('javascript:', 'data:')) for n in root.iter() for v in n.attrib.values())
        for topic in ('theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/sac/index',
                      'theory/paradigms/reinforcement-learning/learning-from-human-feedback/dpo/index'):
            if stem.startswith(topic.split('/')[-2]) or (stem.startswith('dpo') and '/dpo/' in topic):
                for suffix in ('.md', '.zh-TW.md'):
                    data = (ROOT/'docs'/f'{topic}{suffix}').read_text()
                    assert f'{stem}-motion.svg' in data and f'{stem}-still.svg' in data
                    assert 'CC BY-SA 4.0' in data


def main():
    verify_assets()
    js = JS.read_text()
    css = CSS.read_text()
    successes=0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None, args=['--no-sandbox'])
        for stem in TOPICS:
            for lang, alt in [('en', 'Animated SAC or DPO learning diagram'), ('zh', '概念動畫：動作或偏好資料更新')]:
                for viewport in (320,360,760,1024):
                    for reduced in (False, True):
                        page=browser.new_page(viewport={'width':viewport,'height':660},reduced_motion='reduce' if reduced else 'no-preference')
                        def handle(route):
                            file_name=route.request.url.rsplit('/',1)[-1]
                            path=ASSETS/file_name
                            if path.is_file() and path.name.startswith(stem):
                                route.fulfill(body=path.read_bytes(),content_type='image/svg+xml',status=200)
                            else: route.fulfill(status=404,body='not found')
                        page.route('https://aiwiki.invalid/assets/concept-animations/*',handle)
                        url='https://aiwiki.invalid/assets/concept-animations/'
                        html=f'''<html><head><style>body{{margin:0}}{css}</style></head><body><div class="concept-motion-wide" tabindex="0"><img src="{url}{stem}-still.svg" data-motion-src="{url}{stem}-motion.svg" alt="{alt}"></div></body></html>'''
                        page.set_content(html,wait_until='load')
                        page.add_script_tag(content=js)
                        img=page.locator('.concept-motion-wide img')
                        toggle=page.locator('.concept-motion-toggle')
                        assert toggle.count()==1
                        img.evaluate('(el)=>el.decode()')
                        assert ('-still.svg' if reduced else '-motion.svg') in img.get_attribute('src')
                        assert page.locator('.concept-motion-wide').evaluate('(el)=>el.scrollWidth>el.clientWidth') == (viewport < 760)
                        if not reduced:
                            toggle.click()
                            assert '-still.svg' in img.get_attribute('src')
                            toggle.focus()
                            toggle.press('Enter')
                            assert '-motion.svg' in img.get_attribute('src')
                            toggle.press('Space')
                            assert '-still.svg' in img.get_attribute('src')
                        else:
                            toggle.click()
                            assert '-motion.svg' in img.get_attribute('src')
                        img.evaluate('(el)=>el.decode()')
                        assert img.evaluate('(el)=>el.naturalWidth') == 760
                        page.close()
                        successes+=1
        browser.close()
    print(f'SAC / DPO SVG, bilingual play/pause, keyboard, reduced-motion, 320–1024px: {successes}/{successes} passed')

if __name__=='__main__':
    main()
