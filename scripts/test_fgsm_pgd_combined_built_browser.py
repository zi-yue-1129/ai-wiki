#!/usr/bin/env python3
"""Actual built bilingual combined-trajectory page, math, native scroll and fallback QA."""
import argparse,json,os
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from test_built_motion_browser import serve_site,check_math_rendering,assert_document_fits
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--site-dir',type=Path,default=ROOT/'site');parser.add_argument('--output',type=Path,default=ROOT/'artifacts/fgsm-pgd-combined-built');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);report={'status':'running','cases':[]}
    try:
        with serve_site(args.site_dir,'https://zi-yue-1129.github.io/ai-wiki/') as base,sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
            try:
                for topic in ('fgsm','pgd-adversarial-training'):
                    for lang in ('en','zh-TW'):
                        for width in (390,1280):
                            for reduced in (False,True):
                                case={'topic':topic,'lang':lang,'width':width,'reduced':reduced,'status':'running','page_errors':[]};report['cases'].append(case)
                                page=browser.new_page(viewport={'width':width,'height':950},reduced_motion='reduce' if reduced else 'no-preference')
                                page.on('pageerror',lambda e,c=case:c['page_errors'].append(str(e)))
                                folder=args.output/f'{topic}-{lang}-{width}-{reduced}';folder.mkdir(exist_ok=True)
                                try:
                                    url=urljoin(base,('zh-TW/' if lang=='zh-TW' else '')+f'theory/machine-learning/adversarial-robustness/{topic}/')
                                    response=page.goto(url,wait_until='load');assert response and response.ok
                                    case['math']=check_math_rendering(page);page.evaluate('document.fonts.ready');case['layout']=assert_document_fits(page,{'width':width})
                                    image=page.locator('img[src$="fgsm-pgd-trajectory.svg"]');assert image.count()==1
                                    image.scroll_into_view_if_needed();image.evaluate('(e)=>e.decode()');assert image.evaluate('e=>e.complete && e.naturalWidth>0')
                                    assert abs(image.bounding_box()['width']-720)<1
                                    region=image.locator('xpath=../..');assert region.get_attribute('tabindex')=='0'
                                    region.evaluate('e=>e.scrollLeft=0');page.wait_for_timeout(300)
                                    assert region.evaluate('e=>e.scrollLeft')==0
                                    before=region.evaluate('e=>({client:e.clientWidth,scroll:e.scrollWidth,left:e.scrollLeft})')
                                    page.screenshot(path=str(folder/'initial.png'))
                                    if before['scroll']>before['client']+2:
                                        region.focus();page.keyboard.press('ArrowRight');page.wait_for_timeout(500);after=region.evaluate('e=>e.scrollLeft');assert after>0
                                        region.evaluate('e=>e.scrollLeft=e.scrollWidth');page.wait_for_timeout(300)
                                        case['scroll']={'before':before,'afterArrowRight':after,'rightEdge':region.evaluate('e=>e.scrollLeft')}
                                        assert case['scroll']['rightEdge']>=before['scroll']-before['client']-1
                                    page.screenshot(path=str(folder/'right-edge.png'));region.evaluate('e=>e.scrollLeft=0')
                                    assert not case['page_errors'];case['status']='passed'
                                finally:page.close()
                assert len(report['cases'])==16;report['status']='passed'
            finally:browser.close()
    finally:(args.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Combined FGSM/PGD: all 16 built bilingual viewport/motion cases passed')
if __name__=='__main__':main()
