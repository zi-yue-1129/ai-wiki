"""Deterministic Chromium regression for the committed bilingual VQ-VAE/3DGS labs."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / 'docs/javascripts/vq-splat-labs.js').read_text(encoding='utf-8')
CSS = (ROOT / 'docs/stylesheets/vq-splat-labs.css').read_text(encoding='utf-8')
PAGES = [
    ROOT/'docs/theory/paradigms/unsupervised/density-and-generative-models/vae/vq-vae.md',
    ROOT/'docs/theory/paradigms/unsupervised/density-and-generative-models/vae/vq-vae.zh-TW.md',
    ROOT/'docs/theory/models/computer-vision/3d-and-neural-rendering/gaussian-splatting.md',
    ROOT/'docs/theory/models/computer-vision/3d-and-neural-rendering/gaussian-splatting.zh-TW.md',
]
for p in PAGES:
    text = p.read_text(encoding='utf-8')
    assert 'data-vq-splat-lab=' in text and '-still.svg' in text, p

OUT = ROOT/'artifacts/vq-splat-labs'
OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    for lang in ('en', 'zh'):
        for width in (320, 360, 760, 1024):
            for reduced in (False, True):
                page = browser.new_page(viewport={'width':width,'height':850},reduced_motion='reduce' if reduced else 'no-preference')
                errors=[]
                page.on('pageerror', lambda e: errors.append(str(e)))
                body = f'''<!doctype html><html><meta charset="utf-8"><style>body {{font-family:Arial,sans-serif;margin:16px;max-width:1080px}} {CSS}</style><body>
                <section data-vq-splat-lab="vq" data-lang="{lang}"><p>Static fallback is in the Markdown page.</p></section>
                <section data-vq-splat-lab="splat" data-lang="{lang}"><p>Static fallback is in the Markdown page.</p></section><script>{JS}</script></body></html>'''
                page.set_content(body)
                assert not errors, errors
                assert page.locator('.vq-splat-lab svg').count() == 2
                assert page.evaluate('() => document.documentElement.scrollWidth <= innerWidth + 1')
                assert page.evaluate('''() => {let a=window.__vqSplatMath.composite([.5,.6,.8]); return a.weights.every((x,i)=>Math.abs(x-[.5,.3,.16][i])<1e-10) && Math.abs(a.t-.04)<1e-10 && window.__vqSplatMath.nearest(.74,.35).index===1}''')
                for lab in ('vq','splat'):
                    scope=page.locator(f'[data-vq-splat-lab="{lab}"]')
                    end='5' if lab=='vq' else '3'
                    scope.locator('[data-action=next]').click()
                    assert scope.locator('[data-action=seek]').input_value()=='1'
                    scope.locator('[data-action=seek]').evaluate("(el, value) => { el.value = value; el.dispatchEvent(new Event('input', {bubbles: true})); }", end)
                    assert scope.locator('[data-action=seek]').input_value()==end
                    assert scope.locator('[role=status]').inner_text()
                    if width==1024 and not reduced: page.screenshot(path=str(OUT/f'{lang}-{lab}-final.png'),full_page=True)
                    scope.locator('[data-action=reset]').click()
                    assert scope.locator('[data-action=seek]').input_value()=='0'
                    scope.locator('[data-param="0"]').evaluate("el=>{el.value='0.40';el.dispatchEvent(new Event('input',{bubbles:true}));}")
                    assert scope.locator('[data-value="0"]').inner_text()=='0.40'
                    scope.locator('[data-action=play]').click()
                    assert scope.locator('[data-action=play]').get_attribute('aria-pressed')=='true'
                    scope.locator('[data-action=play]').click()
                    assert scope.locator('[data-action=play]').get_attribute('aria-pressed')=='false'
                if width==320 and not reduced: page.screenshot(path=str(OUT/f'{lang}-mobile.png'),full_page=True)
                page.close()
                print('PASS',lang,width,'reduced' if reduced else 'normal')
    browser.close()