#!/usr/bin/env python3
"""Real Chromium regression for static-first bilingual stochastic-bandit motion."""
import base64
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(os.environ.get('AIWIKI_LOCAL_TEST_ROOT', Path(__file__).resolve().parents[1]))
ASSETS = ROOT / 'docs/assets/concept-animations'
JS = ROOT / 'docs/javascripts/concept-motion.js'
CSS = ROOT / 'docs/stylesheets/concept-motion.css'
TOPICS = ('ucb1-optimism-switch', 'thompson-beta-posterior-draws')
ALTS = {'en': 'UCB and Thompson sampling update hypothetical arm preferences.', 'zh-TW': '多臂吃角子老虎教學動畫：呈現信賴上界與後驗分布的更新。'}

def uri(path):
    return 'data:image/svg+xml;base64,' + base64.b64encode(path.read_bytes()).decode() + '#concept-animations/' + path.name

def main():
    count=0
    with sync_playwright() as p:
        opts={'headless':True,'args':['--no-sandbox']}
        if os.environ.get('CHROMIUM_PATH'):
            opts['executable_path']=os.environ['CHROMIUM_PATH']
        browser=p.chromium.launch(**opts)
        for topic in TOPICS:
            still=uri(ASSETS/(topic+'-still.svg'))
            motion=uri(ASSETS/(topic+'-motion.svg'))
            for lang in ('en','zh-TW'):
                for width in (320,360,860,1024):
                    for reduced in (False,True):
                        page=browser.new_page(viewport={'width':width,'height':680},reduced_motion='reduce' if reduced else 'no-preference')
                        page.set_content('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;padding:10px}</style></head><body>'
                            '<div class="bandit-motion-viewport" role="region" tabindex="0" aria-label="Scrollable visual">'
                            '<img alt="'+ALTS[lang]+'" src="'+still+'" data-motion-src="'+motion+'" data-still-src="'+still+'"></div></body></html>')
                        page.add_style_tag(content=CSS.read_text())
                        page.add_script_tag(content=JS.read_text())
                        toggle=page.locator('.concept-motion-toggle')
                        img=page.locator('img')
                        assert toggle.count()==1,(topic,lang,width,reduced,'control missing')
                        expected=still if reduced else motion
                        assert img.get_attribute('src')==expected,(topic,lang,width,reduced,'initial state wrong')
                        page.wait_for_function("document.querySelector('img').complete && document.querySelector('img').naturalWidth > 0")
                        assert ('播放' in toggle.inner_text())==reduced if lang=='zh-TW' else True
                        dims=page.locator('.bandit-motion-viewport').evaluate('el=>({client:el.clientWidth,scroll:el.scrollWidth,img:el.querySelector("img").getBoundingClientRect().width})')
                        assert dims['img']>=855,(topic,lang,width,'label shrink',dims)
                        if width<=360:
                            assert dims['scroll']>dims['client'],(topic,lang,width,'no scroll',dims)
                            page.locator('.bandit-motion-viewport').focus()
                            page.keyboard.press('ArrowRight')
                            page.wait_for_timeout(80)
                            assert page.locator('.bandit-motion-viewport').evaluate('el=>el.scrollLeft')>0
                        toggle.click()
                        assert img.get_attribute('src')==(motion if reduced else still)
                        toggle.focus();page.keyboard.press('Space')
                        assert img.get_attribute('src')==expected
                        toggle.focus();page.keyboard.press('Enter')
                        assert img.get_attribute('src')!=expected
                        page.close();count+=1
            page=browser.new_page(viewport={'width':900,'height':520})
            page.set_content('<img src="'+motion+'" width="860" height="464">')
            page.wait_for_function("document.querySelector('img').complete && document.querySelector('img').naturalWidth>0")
            shot1=page.locator('img').screenshot();page.wait_for_timeout(7200 if topic.startswith('thompson') else 2900)
            shot2=page.locator('img').screenshot()
            assert shot1!=shot2,(topic,'SVG did not animate in Chromium')
            page.close()
        browser.close()
    print(f'PASS: {count}/{count} bilingual viewport/reduced-motion/player cases; 2/2 animated SVG image changes')

if __name__=='__main__':main()