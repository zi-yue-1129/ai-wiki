"""Local Chromium checks for interactive T5 / DeiT lab teaching arithmetic and visual geometry."""
from pathlib import Path
import math
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts' / 't5-deit-labs'
OUT.mkdir(parents=True, exist_ok=True)
JS = (ROOT / 'docs' / 'javascripts' / 't5-deit-labs.js').read_text()
CSS = (ROOT / 'docs' / 'stylesheets' / 't5-deit-labs.css').read_text()

def html(lang):
    return f'''<!doctype html><html lang="{lang}"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{max-width:1080px;margin:20px auto;padding:0 12px;font-family:system-ui;background:#fff}}</style><style>{CSS}</style>
    <article><h1>Teaching labs</h1><p>Static GitHub SVG previews appear above labs in the actual Markdown chapter.</p>
    <div class="t5-deit-lab" id="t5" data-lab="t5"></div>
    <div class="t5-deit-lab" id="deit" data-lab="deit"></div></article><script>{JS}</script></html>'''

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
    count=0
    for lang in ('en','zh-TW'):
        for width in (320,360,760,1024):
            for reduce in (False,True):
                page=browser.new_page(viewport={'width':width,'height':900}, reduced_motion='reduce' if reduce else 'no-preference')
                errors=[]
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.set_content(html(lang),wait_until='load')
                assert page.locator('#t5 svg').count()==1 and page.locator('#deit svg').count()==1
                assert not errors, errors
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (lang,width,'document overflow')
                assert page.locator('#t5 .td-viewport').evaluate('(x)=>x.scrollWidth>x.clientWidth') if width<=360 else True
                # Stage 0 must not leak the future reconstructed target or training loss.
                assert 'Target:' not in page.locator('#t5 .td-state').inner_text()
                assert 'Encoder:' not in page.locator('#t5 .td-state').inner_text()
                assert 'CE(' not in page.locator('#deit .td-state').inner_text()
                assert page.locator('#t5 [data-length="Input"][data-count="10"]').count()==1
                assert page.locator('#t5 [data-length="Encoder"]').count()==0
                assert page.locator('#t5 [data-length="Target"]').count()==0
                assert page.locator('#deit [data-diagnostic="loss-contributions"]').count()==0
                # All SVG text elements must fit inside canvas at default/intermediate/final states.
                for root in ('t5','deit'):
                    for _ in range(3):
                        page.locator(f'#{root} [data-action="next"]').click()
                        bad=page.locator(f'#{root} svg').evaluate('s=>[...s.querySelectorAll("text")].filter(t=>{let b=t.getBBox();return b.x < -1 || b.y < -1 || b.x+b.width > 760 || b.y+b.height > Number(s.viewBox.baseVal.height)}).map(t=>t.textContent)')
                        assert not bad,(lang,width,root,bad)
                # The complete stages now reveal mathematically meaningful diagnostics.
                assert page.locator('#t5 [data-length="Encoder"][data-count="8"]').count()==1
                assert page.locator('#t5 [data-length="Target"][data-count="7"]').count()==1
                assert 'B C' in page.locator('#t5 .td-state').inner_text() and 'H I' in page.locator('#t5 .td-state').inner_text()
                assert page.locator('#deit [data-diagnostic="loss-contributions"]').count()==1
                assert abs(float(page.locator('#deit .td-state').inner_text().split('L ')[1].split(' ·')[0]) - ((-math.log(.75)-math.log(.4))/2)) <.002
                # These are visual shares, not new output heads: both must sum to the total loss.
                assert page.locator('#deit [data-diagnostic="loss-contributions"] rect').count()==3
                # Changed student head probability affects CE in correct direction.
                page.locator('#deit .td-params input').first.fill('0.9')
                assert 'CE(CLS) 0.105' in page.locator('#deit .td-state').inner_text()
                # T5 variable span position and length recompute target and encoder.
                page.locator('#t5 .td-params input').nth(0).fill('3')
                assert 'C D' in page.locator('#t5 .td-state').inner_text()
                page.locator('#t5 [data-action="reset"]').click()
                assert 'Target:' not in page.locator('#t5 .td-state').inner_text()
                page.locator('#t5 .td-seek').fill('3')
                assert 'B C' in page.locator('#t5 .td-state').inner_text()
                assert page.locator('#t5 [data-lane="Target"]').count()==1
                # Keyboard step control, active playback speed and pause all remain operable.
                seek = page.locator('#t5 .td-seek')
                seek.fill('1')
                seek.focus()
                page.keyboard.press('ArrowRight')
                expected_step = 'Construct encoder input' if lang == 'en' else '組成編碼器輸入'
                assert expected_step in page.locator('#t5 .td-state').inner_text()
                page.locator('#t5 [data-action="play"]').click()
                assert (page.locator('#t5 [data-action="play"]').inner_text() == ('Pause' if lang == 'en' else '暫停'))
                page.locator('#t5 .td-speed').select_option('0.5')
                assert (page.locator('#t5 [data-action="play"]').inner_text() == ('Pause' if lang == 'en' else '暫停'))
                page.locator('#t5 [data-action="play"]').click()
                assert (page.locator('#t5 [data-action="play"]').inner_text() == ('Play' if lang == 'en' else '播放'))
                # Swapping the teacher's fixed hard label changes CE(DIST), not student logits.
                page.locator('#deit .td-params select').select_option('A')
                assert 'CE(DIST) 0.511' in page.locator('#deit .td-state').inner_text()
                page.locator('#deit .td-seek').fill('4')
                assert 'Avg heads' in page.locator('#deit svg').text_content()
                if width in (320,1024) and not reduce:
                    page.screenshot(path=str(OUT/f'{lang}-{width}.png'), full_page=True)
                page.close();count+=1
    browser.close()
print('PASS',count,'Chromium scenarios')
