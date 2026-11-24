from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
script=(root/'docs/javascripts/planning-labs.js').read_text()
css=(root/'docs/stylesheets/planning-labs.css').read_text()
shots=root/'artifacts/planning-labs'
shots.mkdir(parents=True, exist_ok=True)
forbidden=[]

with sync_playwright() as p:
    import shutil
    chrome=shutil.which('chromium') or shutil.which('google-chrome')
    browser=p.chromium.launch(headless=True, **({'executable_path':chrome} if chrome else {}), args=['--no-sandbox'])
    for lang in ('en','zh-TW'):
      for width in (320,360,720,1024):
       for reduced in (False,True):
        page=browser.new_page(viewport={'width':width,'height':850},reduced_motion='reduce' if reduced else 'no-preference')
        page.set_content('<!doctype html><html><head><meta charset="utf-8"><style>'+css+'</style></head><body style="margin:12px;max-width:950px;font-family:Arial,sans-serif"><h2>STRIPS &amp; Graphplan</h2><div class="planning-lab" data-planning-lab="strips" data-lang="'+lang+'"><p>Fallback</p></div><div class="planning-lab" data-planning-lab="graphplan" data-lang="'+lang+'"><p>Fallback</p></div><script>'+script+'</script></body></html>')
        a=page.locator('[data-planning-lab=strips]')
        b=page.locator('[data-planning-lab=graphplan]')
        assert a.locator('svg text').count()>4
        assert b.locator('svg text').count()>4
        assert ('可水平捲動' if lang=='zh-TW' else 'horizontal scroll') in b.locator('.planning-canvas').get_attribute('aria-label')
        assert a.locator('[role=status]').count()==1
        a.locator('[data-a=seek]').fill('4')
        assert 'At(B)' in a.locator('[role=status]').inner_text()
        a.locator('[data-p=atA]').uncheck()
        assert 'not applied' in a.locator('[data-a=seek]').evaluate('e=>e.closest("[data-planning-lab]").querySelector("svg").textContent')
        assert ('missing' if lang=='en' else '缺少') in a.locator('[role=status]').inner_text()
        a.locator('[data-a=reset]').click()
        assert a.locator('[data-a=seek]').input_value()=='0'
        b.locator('[data-a=seek]').fill('4')
        assert ('Move(A,B)' in b.locator('[role=status]').inner_text())
        b.locator('[data-p=goal]').select_option('AB')
        assert ('mutex' if lang=='en' else '互斥') in b.locator('[role=status]').inner_text()
        # Keyboard native controls and explicit motion reduction are preserved.
        a.locator('[data-a=next]').focus()
        page.keyboard.press('Enter')
        assert a.locator('[data-a=seek]').input_value()=='1'
        a.locator('[data-a=play]').click()
        assert a.locator('[data-a=play]').get_attribute('aria-pressed') == ('false' if reduced else 'true')
        if not reduced:
          a.locator('[data-a=play]').click()
          assert a.locator('[data-a=play]').get_attribute('aria-pressed')=='false'
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        assert a.locator('.planning-canvas').evaluate('e => e.scrollWidth >= e.clientWidth')
        if width in (320,1024) and not reduced:
          fn=shots/f'qa-{lang}-{width}.png'
          page.screenshot(path=str(fn),full_page=True)
        page.close()
    browser.close()
print('PASS: 16 bilingual responsive/reduced-motion scenarios, computed successors, mutex, reset and keyboard')
