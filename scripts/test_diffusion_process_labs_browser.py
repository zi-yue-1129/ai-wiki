"""Render and exercise toy video forward-noising and latent compression labs in Chromium."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
if (ROOT.parent / 'docs/javascripts/diffusion-process-labs.js').exists():
    JS=ROOT.parent/'docs/javascripts/diffusion-process-labs.js'
    CSS=ROOT.parent/'docs/stylesheets/diffusion-process-labs.css'
else:
    JS=ROOT/'diffusion-process-labs.js'
    CSS=ROOT/'diffusion-process-labs.css'
OUTPUT=Path(os.getenv('DIFFUSION_LAB_ARTIFACTS', ROOT/'qa'))
OUTPUT.mkdir(parents=True,exist_ok=True)
HTML='''<!DOCTYPE html><html lang="LANG"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;padding:16px;font:16px system-ui;color:#24364a}main{max-width:850px;margin:auto}h1{font-size:21px}h2{font-size:17px}</style></head><body><main><h1>Diffusion / 擴散</h1><h2>Video diffusion</h2><div data-diffusion-lab="video" data-lang="LANG"><p>Static preview stays visible without JavaScript.</p></div><h2>Latent diffusion</h2><div data-diffusion-lab="latent" data-lang="LANG"><p>Static preview stays visible without JavaScript.</p></div></main></body></html>'''


def exercise():
    n=0
    with sync_playwright() as playwright:
        executable=os.getenv('CHROMIUM_PATH') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None)
        browser=playwright.chromium.launch(executable_path=executable,headless=True,args=['--no-sandbox'])
        for lang in ('en','zh-TW'):
            for width in (320,360,760,1024):
                for reduced in (False,True):
                    context=browser.new_context(viewport={'width':width,'height':940},reduced_motion='reduce' if reduced else 'no-preference')
                    page=context.new_page();errors=[]
                    page.on('pageerror',lambda err: errors.append(str(err)))
                    page.set_content(HTML.replace('LANG',lang))
                    assert page.locator('text=Static preview stays visible without JavaScript.').count()==2
                    page.add_style_tag(content=CSS.read_text(encoding='utf-8'))
                    page.add_script_tag(content=JS.read_text(encoding='utf-8'))
                    video=page.locator('[data-diffusion-lab="video"]')
                    latent=page.locator('[data-diffusion-lab="latent"]')
                    assert video.locator('[data-role="svg"] rect').count()>700
                    assert latent.locator('[data-role="svg"] rect').count()>250
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),(lang,width)
                    assert not errors,errors
                    baseline=float(video.locator('[data-role="metrics"] strong').nth(1).inner_text())
                    assert baseline>0.25
                    video.locator('[data-role="alpha"]').fill('9')
                    assert '0.000' in video.locator('[data-role="metrics"]').inner_text()
                    video.locator('[data-action="previous"]').click()
                    assert float(video.locator('[data-role="metrics"] strong').nth(1).inner_text())>0
                    video.locator('[data-action="reset"]').click()
                    assert video.locator('[data-role="alpha-out"]').inner_text()=='0.05'
                    # Native range slider keyboard access: ArrowRight advances one discrete step.
                    alpha_slider=video.locator('[data-role="alpha"]')
                    alpha_slider.focus()
                    page.keyboard.press('ArrowRight')
                    assert video.locator('[data-role="alpha-out"]').inner_text()=='0.15'
                    video.locator('[data-action="reset"]').focus()
                    page.keyboard.press('Enter')
                    assert video.locator('[data-role="alpha-out"]').inner_text()=='0.05'
                    latent.locator('[data-role="seek"]').fill('8')
                    assert '16:1' in latent.locator('[data-role="metrics"]').inner_text()
                    assert '16' in latent.locator('[data-role="metrics"]').inner_text()
                    assert 'Pending' not in latent.locator('[data-role="svg"]').text_content()
                    latent.locator('[data-role="factor"]').select_option('8')
                    assert '64:1' in latent.locator('[data-role="metrics"]').inner_text()
                    assert '4' in latent.locator('[data-role="metrics"] strong').first.inner_text()
                    latent.locator('[data-role="factor"]').select_option('1')
                    assert '0.0000' in latent.locator('[data-role="metrics"]').inner_text()
                    latent.locator('[data-action="reset"]').click()
                    assert 'Pending' in latent.locator('[data-role="svg"]').text_content()
                    assert '—' in latent.locator('[data-role="metrics"]').inner_text()
                    latent.locator('[data-action="next"]').click()
                    assert latent.locator('[data-role="step-out"]').inner_text()=='1/8'
                    if reduced:
                        latent.locator('[data-action="toggle"]').click()
                        assert latent.locator('[data-action="toggle"]').inner_text() in ('Play','播放')
                    else:
                        latent.locator('[data-action="toggle"]').click()
                        assert latent.locator('[data-action="toggle"]').inner_text() in ('Pause','暫停')
                        latent.locator('[data-role="speed"]').select_option('2')
                        latent.locator('[data-action="toggle"]').click()
                    if width in (320,1024) and not reduced:
                        latent.locator('[data-role="seek"]').fill('8')
                        video.locator('[data-role="seek"]').fill('4')
                        page.screenshot(path=str(OUTPUT/f'{lang}-{width}.png'),full_page=True)
                        for widget in (video,latent):
                            svg=widget.locator('svg')
                            # Text bounds in SVG coordinates, including readable margins.
                            bounds=svg.evaluate('''svg=>[...svg.querySelectorAll('text')].map(t=>{let b=t.getBBox();return {x:b.x,y:b.y,r:b.x+b.width,b:b.y+b.height,label:t.textContent}})''')
                            assert all(-1<=b['x'] and b['r']<=761 and -1<=b['y'] and b['b']<=289 for b in bounds),bounds
                    n+=1
                    context.close()
        browser.close()
    print(f'PASS: {n} bilingual×viewport×reduced-motion Chromium scenarios; source math, controls, fallback and screenshots verified')

if __name__=='__main__':exercise()