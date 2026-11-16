"""Chromium end-to-end checks of the original sharpness numerical teaching labs."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / 'docs/javascripts/sharpness-geometry-labs.js').read_text('utf-8')
CSS = (ROOT / 'docs/stylesheets/sharpness-geometry-labs.css').read_text('utf-8')

OUT = ROOT / 'artifacts/sharpness-labs'
OUT.mkdir(parents=True, exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=os.environ.get('AIWIKI_CHROMIUM_PATH') or None, args=['--no-sandbox'])
        count = 0
        for language in ('en','zh'):
            for width in (320,390,768,1024):
                for motion in ('reduce','no-preference'):
                    page = browser.new_page(viewport={'width':width,'height':920},reduced_motion=motion)
                    errors=[]
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.clock.install()
                    html=f'''<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><meta charset="utf-8"><style>{CSS}</style><style>body{{margin:0;padding:8px;font-family:Arial,sans-serif}}main{{max-width:1000px;margin:auto}}</style></head><body><main>
                    <div data-sharpness-lab="radius" data-lang="{language}"></div><div data-sharpness-lab="reparam" data-lang="{language}"></div>
                    </main><script>{JS}</script></body></html>'''
                    page.set_content(html)
                    assert page.locator('.sgl-panel').count()==2
                    assert page.locator('.sgl-scroll svg').count()==2
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width,language,'horizontal document overflow')
                    for kind in ('radius','reparam'):
                        lab=page.locator(f'[data-sharpness-lab="{kind}"]')
                        assert lab.locator('svg[role="img"][aria-label]').count()==1
                        slider=lab.locator('input[type="range"]')
                        if kind=='radius':
                            slider.fill('0.8')
                            d=lab.locator('.sgl-detail').inner_text()
                            assert 'ΔLflat=0.160' in d and 'ΔLsharp=0.640' in d,d
                        else:
                            slider.fill('1.5')
                            d=lab.locator('.sgl-detail').inner_text()
                            assert 'Hessian(u)=4.500' in d and 'physical Δw=0.900' in d and 'ΔL(u)=0.810' in d,d
                        step=lab.get_by_role('button',name='下一步' if language=='zh' else 'Next step')
                        step.focus();page.keyboard.press('Enter')
                        assert lab.locator('.sgl-detail').inner_text()!=d
                        if motion=='reduce':
                            assert lab.get_by_role('button',name='播放' if language=='zh' else 'Play').is_disabled()
                        else:
                            reset=lab.get_by_role('button',name='重設' if language=='zh' else 'Reset')
                            reset.click()
                            play=lab.get_by_role('button',name='播放' if language=='zh' else 'Play')
                            play.focus();page.keyboard.press('Space')
                            page.clock.run_for(1100)
                            pause=lab.get_by_role('button',name='暫停' if language=='zh' else 'Pause')
                            pause.click()
                            v=lab.locator('.sgl-detail').inner_text()
                            page.clock.run_for(500)
                            assert lab.locator('.sgl-detail').inner_text()==v
                        # Numeric graph labels must stay within the SVG viewBox.
                        rects=lab.locator('svg text').evaluate_all('els => els.map(e => {let r=e.getBBox(); return [r.x,r.y,r.x+r.width,r.y+r.height]})')
                        assert all(-1<=x0 and -1<=y0 and x1<=641 and y1<=301 for x0,y0,x1,y1 in rects),rects
                    assert not errors,errors
                    if width in (320,1024) and motion=='no-preference':
                        page.screenshot(path=str(OUT/f'{language}-{width}.png'),full_page=True)
                    # The keyboard-scrollable diagram must actually scroll on small screens.
                    if width==320:
                        scroll=page.locator('.sgl-scroll').first
                        scroll.focus();page.keyboard.press('ArrowRight');page.wait_for_timeout(300)
                        assert scroll.evaluate('(e)=>e.scrollLeft>0'),(language,width)
                    page.close();count+=1
        browser.close()
        print(f'Sharpness geometry labs: {count}/16 Chromium viewport/language/motion scenarios passed')


if __name__=='__main__':run()
