import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
if (ROOT/'docs/javascripts/policy-credit-labs.js').exists():
    js=(ROOT/'docs/javascripts/policy-credit-labs.js').read_text()
    css=(ROOT/'docs/stylesheets/policy-credit-labs.css').read_text()
    OUT=ROOT/'artifacts/policy-credit-labs'
else:
    js=(BASE/'policy-credit-labs.js').read_text()
    css=(BASE/'policy-credit-labs.css').read_text()
    OUT=BASE
OUT.mkdir(parents=True,exist_ok=True)

def html(locale):
    # Functional harness with all site asset paths represented by harmless local stub images.
    return '''<!doctype html><html lang="%s"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{margin:0;padding:14px;font:16px system-ui,sans-serif;background:#f8fafc;color:#17283a;max-width:900px;}main{width:100%%;max-width:900px;} h2{font-size:1.2rem} %s</style><main><h2>REINFORCE</h2><div data-policy-lab="reinforce" data-lang="%s"><p>Fallback</p></div><h2>GRPO</h2><div data-policy-lab="grpo" data-lang="%s"><p>Fallback</p></div></main><script>%s</script></html>''' % (locale,css,locale,locale,js)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True, **({'executable_path':'/usr/bin/chromium'} if Path('/usr/bin/chromium').exists() else {}), args=['--no-sandbox'])
    count=0
    for locale in ['en','zh']:
      for width in [320,360,720,1024]:
       for reduced in [False,True]:
        page=browser.new_page(viewport={'width':width,'height':900}, reduced_motion='reduce' if reduced else 'no-preference')
        errors=[]
        page.on('pageerror', lambda exc: errors.append(str(exc)))
        page.set_content(html(locale))
        hosts=page.locator('[data-policy-lab]')
        assert hosts.count()==2
        assert page.locator('.pcl-panel').count()==2
        assert page.locator('.pcl-scroll svg').count()==2
        assert page.locator('.pcl-scroll').first.evaluate('(e)=>e.scrollWidth>e.clientWidth')==(width<750)
        assert page.locator('body').evaluate('(e)=>e.scrollWidth<=document.documentElement.clientWidth+2')
        assert 'G=[2.560, 3.200, 4.000]' in page.locator('.pcl-read').first.inner_text()
        assert 'σ=1.581' in page.locator('.pcl-read').last.inner_text()
        page.locator('[data-policy-lab="reinforce"] .pcl-seek').evaluate("e=>{e.value='2';e.dispatchEvent(new Event('input',{bubbles:true}))}")
        assert page.locator('[data-policy-lab="reinforce"] .pcl-stage').inner_text().endswith('2/2')
        page.locator('[data-policy-lab="reinforce"] input[aria-label="'+('Baseline b' if locale=='en' else '基線 b')+'" ]').evaluate("e=>{e.value='4';e.dispatchEvent(new Event('input',{bubbles:true}))}")
        assert 'G−b=[-1.440, -0.800, 0.000]' in page.locator('.pcl-read').first.inner_text()
        page.locator('[data-policy-lab="reinforce"] .pcl-btn[aria-label="'+('Reset' if locale=='en' else '重設')+'" ]').click()
        assert 'G=[2.560, 3.200, 4.000]' in page.locator('.pcl-read').first.inner_text()
        assert page.locator('[data-policy-lab="reinforce"] .pcl-stage').inner_text().endswith('0/2'), 'Reset failed to restore step'
        assert page.locator('[data-policy-lab="reinforce"] input[type="range"]').nth(2).input_value()=='2', 'Reset failed to restore baseline'
        page.locator('.pcl-check input').check()
        assert 'σ=0.000' in page.locator('.pcl-read').last.inner_text()
        assert '[0.000, 0.000, 0.000, 0.000]' in page.locator('.pcl-read').last.inner_text()
        if reduced:
            assert page.locator('[data-policy-lab="reinforce"] .pcl-btn[aria-label="'+('Play' if locale=='en' else '播放')+'" ]').is_disabled()
        # Check SVG label positions remain inside the 700x328 viewbox.
        assert page.locator('svg').evaluate_all('xs => xs.every(x => !/[\u3400-\u9fff]/u.test(x.textContent))'), 'SVG must use English-only labels'
        boxes=page.locator('svg text').evaluate_all('els=>els.map(el=>{const b=el.getBBox();return [b.x,b.y,b.x+b.width,b.y+b.height]})')
        assert all(b[0]>=-0.5 and b[1]>=-0.5 and b[2]<=700.5 and b[3]<=328.5 for b in boxes),boxes
        if width in (320,1024) and not reduced:
            page.screenshot(path=str(OUT/f'qa-{locale}-{width}.png'),full_page=True)
        assert not errors, errors
        count+=1
        page.close()
    browser.close()
    print(f'PASS: {count} bilingual/responsive/reduced-motion cases; numerics, controls and bounding boxes')