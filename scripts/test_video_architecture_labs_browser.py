"""Local + CI Chromium integration of original ViViT / I3D numeric labs."""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if (ROOT / 'docs/javascripts/video-architecture-labs.js').exists():
    JS = ROOT / 'docs/javascripts/video-architecture-labs.js'
    CSS = ROOT / 'docs/stylesheets/video-architecture-labs.css'
    REPORT = ROOT / 'artifacts/video-architecture-labs'
else:
    JS = HERE / 'video-architecture-labs.js'
    CSS = HERE / 'video-architecture-labs.css'
    REPORT = HERE / 'qa'
REPORT.mkdir(parents=True, exist_ok=True)



def run():
    with sync_playwright() as p:
        kwargs = {'headless': True}
        if Path('/usr/bin/chromium').exists():
            kwargs['executable_path'] = '/usr/bin/chromium'
            kwargs['args'] = ['--no-sandbox']
        browser = p.chromium.launch(**kwargs)
        count = 0
        for lang in ('en', 'zh'):
            for width in (320, 360, 720, 1024):
                for reduced in (False, True):
                    page = browser.new_page(viewport={'width': width, 'height': 900}, reduced_motion='reduce' if reduced else 'no-preference')
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    html = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{font:16px system-ui;max-width:1020px;margin:0 auto;padding:12px}h2{font-size:22px}</style></head><body><h2>ViViT</h2><div class="video-arch-lab" data-lab="vivit" data-lang="en"></div><h2>I3D</h2><div class="video-arch-lab" data-lab="i3d" data-lang="en"></div></body></html>'
                    html = html.replace('data-lang="en"', f'data-lang="{lang}"')
                    html = html.replace('</head>', '<style>'+CSS.read_text()+'</style></head>').replace('</body>', '<script>'+JS.read_text()+'</script></body>')
                    page.set_content(html, wait_until='load')
                    assert not errors, errors
                    labs = page.locator('.video-arch-lab')
                    assert labs.count() == 2
                    assert page.locator('.val-scroll svg').count() == 2
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (lang, width, 'document overflow')
                    for lab in (labs.nth(0), labs.nth(1)):
                        box = lab.bounding_box()
                        assert box['x'] >= -1 and box['x']+box['width'] <= width+1
                        sc = lab.locator('.val-scroll')
                        assert sc.evaluate('(n)=>n.scrollWidth>=n.clientWidth')
                        if width < 720:
                            assert sc.evaluate('(n)=>n.scrollWidth>n.clientWidth')
                    v = labs.nth(0)
                    assert '48' in v.locator('.val-readout').inner_text()
                    v.locator('[data-op=next]').click()
                    assert '36' in v.locator('.val-readout').inner_text()
                    v.locator('[data-op=next]').click()
                    assert '84' in v.locator('.val-readout').inner_text()
                    v.locator('[data-op=frame]').fill('1')
                    v.locator('[data-op=patch]').fill('4')
                    assert '12/12' in v.locator('.val-readout').inner_text()
                    v.locator('[data-op=reset]').click()
                    assert '48' in v.locator('.val-readout').inner_text()
                    i = labs.nth(1)
                    assert '3.500' in i.locator('.val-readout').inner_text()
                    i.locator('[data-op=delta]').fill('2')
                    assert '4.167' in i.locator('.val-readout').inner_text()
                    i.locator('[data-op=next]').click()
                    assert '1.167' in i.locator('.val-readout').inner_text()
                    i.locator('[data-op=seek]').fill('3')
                    assert '4.167' in i.locator('.val-readout').inner_text()
                    i.locator('[data-op=reset]').click()
                    assert '3.500' in i.locator('.val-readout').inner_text()
                    # Focusable controls and native range keyboard behavior.
                    v.locator('[data-op=seek]').focus()
                    page.keyboard.press('ArrowRight')
                    assert '36' in v.locator('.val-readout').inner_text()
                    v.locator('[data-op=play]').click()
                    assert v.locator('[data-op=play]').inner_text() in ('Pause', '暫停')
                    v.locator('[data-op=play]').click()
                    assert v.locator('[data-op=play]').inner_text() in ('Play', '播放')
                    if width in (320, 1024) and not reduced:
                        v.locator('[data-op=seek]').fill('2')
                        i.locator('[data-op=seek]').fill('3')
                        page.screenshot(path=str(REPORT / f'{lang}-{width}.png'), full_page=True)
                    page.close()
                    count += 1
        browser.close()
        print(f'Chromium cases passed: {count}/16')

if __name__ == '__main__':
    run()