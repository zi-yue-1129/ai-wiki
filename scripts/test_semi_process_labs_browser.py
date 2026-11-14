#!/usr/bin/env python3
"""Chromium checks on actual semi-supervised process module: bilingual, mobile, controls, arithmetic."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
JS=(ROOT/'docs/javascripts/semi-supervised-process-labs.js').read_text(encoding='utf-8')
CSS=(ROOT/'docs/stylesheets/semi-supervised-process-labs.css').read_text(encoding='utf-8')
OUT=ROOT/'artifacts/semi-supervised-process-labs'
OUT.mkdir(parents=True,exist_ok=True)
def set_range(page,selector,value):
    page.locator(selector).evaluate("(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));}",str(value))
def main():
    count=0
    with sync_playwright() as p:
        kw={'executable_path':'/usr/bin/chromium','args':['--no-sandbox']} if Path('/usr/bin/chromium').exists() else {}
        browser=p.chromium.launch(headless=True,**kw)
        for kind in ('fixmatch','teacher'):
          for lang in ('en','zh'):
           for width in (320,360,720,1024):
            for reduce in (False,True):
              ctx=browser.new_context(viewport={'width':width,'height':780},reduced_motion='reduce' if reduce else 'no-preference')
              page=ctx.new_page();errors=[]
              page.on('pageerror',lambda e:errors.append(str(e)))
              page.set_content('<html><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><style>*,*:before,*:after{box-sizing:border-box}body{margin:0;padding:16px;font:16px system-ui}'+CSS+'</style><h2>Numerical demonstration</h2><div class="semi-process-lab" data-kind="'+kind+'" data-lang="'+lang+'">Static SVG is available above this lab.</div><script>'+JS+'</script></html>')
              assert page.locator('.semi-process-lab').get_attribute('data-ready')=='1'
              fig=page.locator('.semi-viewport svg')
              assert fig.evaluate('(e)=>e.namespaceURI')=='http://www.w3.org/2000/svg'
              assert fig.locator('rect').count()>0 and fig.locator('text').count()>0
              assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(kind,width,'overflow')
              if width<640:assert page.locator('.semi-viewport').evaluate('(e)=>e.scrollWidth>e.clientWidth')
              if kind=='fixmatch':
                set_range(page,'.semi-inputs label:nth-child(1) input','.90')
                set_range(page,'[data-act="seek"]','3')
                assert '0.000' in page.locator('.semi-read').inner_text()
                set_range(page,'.semi-inputs label:nth-child(2) input','.85')
                assert '0.478' in page.locator('.semi-read').inner_text()
                set_range(page,'.semi-inputs label:nth-child(3) input','.50')
                assert '0.693' in page.locator('.semi-read').inner_text()
              else:
                set_range(page,'[data-act="seek"]','1')
                assert '0.325' in page.locator('.semi-read').inner_text()
                set_range(page,'.semi-inputs input','.50')
                assert '0.500' in page.locator('.semi-read').inner_text()
              page.locator('[data-act="speed"]').select_option('2')
              page.locator('[data-act="reset"]').click()
              assert page.locator('[data-act="seek"]').input_value()=='0'
              page.locator('[data-act="next"]').focus()
              page.keyboard.press('Enter')
              assert page.locator('[data-act="seek"]').input_value()=='1'
              page.locator('[data-act="play"]').click()
              assert page.locator('[data-act="play"]').get_attribute('aria-pressed')=='true'
              page.locator('[data-act="play"]').click()
              assert page.locator('[data-act="play"]').get_attribute('aria-pressed')=='false'
              assert not errors,errors
              if width in (320,1024) and not reduce:page.screenshot(path=str(OUT/(kind+'-'+lang+'-'+str(width)+'.png')),full_page=True)
              count+=1;ctx.close()
        browser.close()
    print('PASS',count,'Chromium combinations')
if __name__=='__main__':main()
