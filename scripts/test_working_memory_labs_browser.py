from pathlib import Path
import math
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/working-memory-labs';OUT.mkdir(parents=True,exist_ok=True)
JS=ROOT/'docs/javascripts/working-memory-labs.js';CSS=ROOT/'docs/stylesheets/working-memory-labs.css'

def run():
    config=(ROOT/'mkdocs.yml').read_text(encoding='utf-8') if (ROOT/'mkdocs.yml').exists() else ''
    if config:
        assert 'javascripts/working-memory-labs.js' in config
        assert 'stylesheets/working-memory-labs.css' in config
        topics=(('pbwm','gate','pbwm-gate'),('activity-silent-working-memory','silent','activity-silent-trace'))
        for topic,kind,stem in topics:
            for suffix,lang in (('','en'),('.zh-TW','zh-TW')):
                page=ROOT/'docs/brain-mind/working-memory-executive-function'/topic/('index'+suffix+'.md')
                content=page.read_text(encoding='utf-8')
                assert 'data-wm-lab="'+kind+'" data-lang="'+lang+'"' in content, page
                assert stem+'-still.svg' in content and stem+'-motion.svg' in content, page
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,args=['--no-sandbox'])
        for lang in ('en','zh-TW'):
            for width in (320,360,720,1024):
                for reduce in (False,True):
                    page=browser.new_page(viewport={'width':width,'height':840},reduced_motion='reduce' if reduce else 'no-preference')
                    html=f'''<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="{CSS}"><style>body{{font-family:system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:0 12px;box-sizing:border-box}}*,*::before,*::after{{box-sizing:border-box}}</style><body><h2>Working memory</h2><div data-wm-lab="gate" data-lang="{lang}"></div><h2>Activity-silent memory</h2><div data-wm-lab="silent" data-lang="{lang}"></div><script src="{JS}"></script></body></html>'''
                    page.set_content(html)
                    page.add_style_tag(content=CSS.read_text())
                    page.add_script_tag(content=JS.read_text())
                    page.wait_for_selector('[data-wm-lab="gate"][data-ready="true"]')
                    assert page.locator('[data-wm-lab="silent"] .wm-lab-pan svg').count()==1
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),f'document overflow width={width}'
                    assert page.locator('[data-wm-lab="gate"] .wm-lab-pan').evaluate('(e)=>e.scrollWidth>=e.clientWidth')
                    gate=page.locator('[data-wm-lab="gate"]')
                    gctrl=gate.locator('.wm-lab-controls button')
                    gctrl.nth(2).click();gctrl.nth(2).click()
                    assert 'A' in gate.locator('.wm-lab-status').inner_text(), 'closed distractor must retain A'
                    gate.locator('input[type=checkbox]').first.check()
                    assert gate.get_attribute('data-current-memory')=='X', 'open distractor must overwrite A'
                    memory_label = 'Memory' if lang == 'en' else '記憶'
                    assert gate.locator('.wm-lab-status').inner_text().endswith(memory_label + ': X')
                    assert gate.locator('svg text[x="580"][y="154"]').text_content() == 'X'
                    assert gate.locator('svg text[x="580"][y="154"]').is_visible()
                    gate.locator('input[type=checkbox]').first.uncheck()
                    gctrl.nth(2).click();assert gate.get_attribute('data-current-memory')=='B'
                    assert gate.locator('.wm-lab-status').inner_text().endswith(memory_label + ': B')
                    assert gate.locator('svg text[x="580"][y="154"]').text_content() == 'B'
                    assert gate.locator('svg text[x="580"][y="154"]').is_visible()
                    gctrl.nth(3).click();assert '0/3' in gate.locator('.wm-lab-status').inner_text()
                    gctrl.nth(2).focus();page.keyboard.press('Enter')
                    assert '1/3' in gate.locator('.wm-lab-status').inner_text()
                    gctrl.nth(3).click()
                    gate.locator('.wm-lab-speed select').select_option('300')
                    gctrl.nth(1).click();assert gctrl.nth(1).inner_text() in ('Pause','暫停')
                    gctrl.nth(1).click();assert gctrl.nth(1).inner_text() in ('Play','播放')
                    silent=page.locator('[data-wm-lab="silent"]')
                    sctrl=silent.locator('.wm-lab-controls button')
                    silent.locator('input[type=range]').first.fill('4')
                    silent.locator('.wm-lab-seek input').fill('4')
                    expected=math.exp(-1)+.55
                    assert f'{expected:.3f}' in silent.locator('.wm-lab-status').inner_text()
                    silent.locator('input[type=checkbox]').uncheck()
                    assert f'{math.exp(-1):.3f}' in silent.locator('.wm-lab-status').inner_text()
                    sctrl.nth(3).click()
                    assert '0/8' in silent.locator('.wm-lab-status').inner_text()
                    if width in (320,1024) and not reduce:
                        page.screenshot(path=str(OUT/f'{lang}-{width}.png'),full_page=True)
                    page.close()
                    print('PASS',lang,width,'reduce' if reduce else 'regular')
        browser.close()
if __name__=='__main__':run()
