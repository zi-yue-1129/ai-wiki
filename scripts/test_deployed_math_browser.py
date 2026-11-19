#!/usr/bin/env python3
"""Real built articles: six repaired bilingual pages, every display, three widths."""
import argparse
import json
import os
import hashlib
import math
from PIL import Image
import re
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from test_built_prose_browser import target
from test_built_motion_browser import serve_site, check_math_rendering, assert_document_fits
from test_forward_math_markup import (GUARDED_MATH_PAGES, MathContainers, render,
    require_no_outside_tex, MappoRecurrenceMarkupTests, RetainedDeployedMathTests, CqlObjectiveMarkupTests, DmlLimitationsMarkupTests)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/mappo/index.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.md', 'docs/theory/paradigms/reinforcement-learning/multi-agent-rl/maddpg/index.zh-TW.md', 'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde.md', 'docs/theory/paradigms/unsupervised/density-and-generative-models/diffusion/score-sde.zh-TW.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index.md', 'docs/theory/paradigms/reinforcement-learning/offline-rl/cql/index.zh-TW.md', 'docs/theory/causal-inference/double-machine-learning.md', 'docs/theory/causal-inference/double-machine-learning.zh-TW.md')
WIDTHS = (320, 390, 1280)
DISPLAY_COUNTS = dict(zip(SOURCES, (2,2,2,2,3,3,2,2,6,6)))

def compact(value):
    return re.sub(r'\s+', '', value)

def source_displays(source):
    blocks = MathContainers(render(source)).blocks
    return [compact(x)[2:-2] for x in blocks]

def required_bodies(source):
    if '/mappo/' in source: return MappoRecurrenceMarkupTests.BODIES
    if '/maddpg/' in source: return [RetainedDeployedMathTests.MADDPG]
    if '/cql/' in source: return [CqlObjectiveMarkupTests.BODY]
    if '/double-machine-learning' in source: return [DmlLimitationsMarkupTests.BODY]
    assert '/score-sde' in source
    return RetainedDeployedMathTests.SDE

# This runs in the actual loaded article after MathJax startup, not a synthetic SVG.
INSPECT = r'''() => {
 const article=document.querySelector('.md-content__inner');
 if(!article || !window.MathJax?.startup?.document?.math) throw Error('Missing article/MathJax');
 const items=Array.from(MathJax.startup.document.math);
 const wrappers=Array.from(article.querySelectorAll('div.arithmatex'));
 const displays=wrappers.map((w,index)=>{
   const matches=items.filter(m=>m.typesetRoot && w.contains(m.typesetRoot));
   if(matches.length!==1 || typeof matches[0].math!=='string') throw Error('Missing/ambiguous MathItem');
   const node=w.querySelector('mjx-container');
   if(!node || !node.getBoundingClientRect().height || node.querySelector('mjx-merror,[data-mjx-error]')) throw Error('Unrendered/error display');
   const li=w.closest('li');
   return {index,tex:matches[0].math,list_titles:li?Array.from(li.parentElement.children).map(x=>x.querySelector('strong')?.textContent):null,li:li?{
     title:li.querySelector('strong')?.textContent,
     count:li.parentElement.querySelectorAll(':scope > li').length,
     index:Array.from(li.parentElement.children).indexOf(li),
     displays:li.querySelectorAll('div.arithmatex').length,
     paragraphs:li.querySelectorAll(':scope > p').length}:null};
 });
 const clone=article.cloneNode(true);
 clone.querySelectorAll('.arithmatex,code,pre,script,style').forEach(x=>x.remove());
 return {displays,outside:clone.innerHTML};
}'''

GEOMETRY = r'''w => {
 const m=w.querySelector('mjx-container');
 const painted=m.querySelector('mjx-math')||m;const r=painted.getBoundingClientRect();
 const candidates=[];for(let e=m;e && e!==document.body;e=e.parentElement){
  const s=getComputedStyle(e);if(['auto','scroll'].includes(s.overflowX)&&e.scrollWidth>e.clientWidth+1)candidates.push(e);
 }
 const scroller=candidates[0];
 const rect=scroller?.getBoundingClientRect();
 return {left:r.left,right:r.right,width:r.width,height:r.height,
 viewport:innerWidth,scroll:scroller?{left:rect.left,right:rect.right,client:scroller.clientWidth,width:scroller.scrollWidth}:null};
}'''

def validate_snapshot(source, expected, snapshot):
    actual=[compact(x['tex']) for x in snapshot['displays']]
    assert actual == expected, ('Source/display mismatch', source, expected, actual)
    require_no_outside_tex(snapshot['outside'])
    for body in required_bodies(source):
        assert actual.count(compact(body)) == 1, ('Missing/repeated repaired formula', body)
    if '/score-sde' in source:
        titles = (['前向 SDE。','逆時 SDE。','機率流 ODE。'] if '.zh-TW.' in source else
                  ['Forward SDE.','Reverse-time SDE.','Probability flow ODE.'])
        for i, (body,title) in enumerate(zip(required_bodies(source),titles)):
            row=snapshot['displays'][actual.index(compact(body))]
            assert row['li']=={'title':title,'count':3,'index':i,'displays':1,'paragraphs':2}, row
    if '/double-machine-learning' in source:
        record=DmlLimitationsMarkupTests.RECORDS[1 if '.zh-TW.' in source else 0]
        row=snapshot['displays'][actual.index(compact(DmlLimitationsMarkupTests.BODY))]
        assert row['li']==dict(title=record[3][1],count=5,index=1,displays=1,paragraphs=2),row
        assert row['list_titles']==record[3],row


def validate_geometry(g):
    assert all(isinstance(g[k],(float,int)) and not isinstance(g[k],bool) and __import__('math').isfinite(g[k]) for k in ('left','right','width','height','viewport'))
    assert g['width']>0 and g['height']>0
    if g['left'] >= -1 and g['right'] <= g['viewport']+1: return
    s=g['scroll'];assert s and s['client']>0 and s['width']>s['client'] and s['left']>=-1 and s['right']<=g['viewport']+1, g

def validate_report(report):
    assert report['status']=='passed'
    expected={(s,w) for s in SOURCES for w in WIDTHS}
    literal_sources={source:source_displays((ROOT/source).read_text())for source in SOURCES}
    cases=report['cases'];assert len(cases)==30 and {(x['source'],x['width']) for x in cases}==expected
    for case in cases:
        assert case['status']=='passed' and not case['errors']
        assert case['expected_displays']==DISPLAY_COUNTS[case['source']]
        assert len(case['displays'])==DISPLAY_COUNTS[case['source']]
        assert case['expected_tex']==literal_sources[case['source']], 'Self-declared formula inventory differs from source'
        validate_snapshot(case['source'],literal_sources[case['source']],case['snapshot'])
        assert len(case['expected_tex'])==DISPLAY_COUNTS[case['source']]
        for row in case['displays']:
            validate_geometry(row['geometry'])
            if row['geometry']['scroll']:
                assert row['right_image']==row['image'].replace('.png','-right.png')
                end=row['end'];assert all(type(end[k]) in (float,int) and math.isfinite(end[k]) for k in ('max','position','right','viewport_left','viewport_right'))
                assert abs(end['max']-(row['geometry']['scroll']['width']-row['geometry']['scroll']['client']))<=1
                assert end['viewport_left']>=-1 and end['viewport_right']<=row['geometry']['viewport']+1
                assert end['max']>0 and abs(end['position']-end['max'])<=1
                assert end['right']<=end['viewport_right']+1 and end['right']>=end['viewport_left'],end
        assert all(x['image']==f'display-{i:03d}.png' for i,x in enumerate(case['displays']))
        assert 'top.png' in case['screenshots']
        if '/score-sde' in case['source']:assert 'core-list.png' in case['screenshots']
        if '/double-machine-learning' in case['source']:assert 'limitations.png' in case['screenshots']

def image_receipt(path):
    data=path.read_bytes()
    with Image.open(path) as im:
        assert im.format=='PNG';im.verify()
    with Image.open(path) as im:
        im.load();size=list(im.size)
    return dict(sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),dimensions=size)

def capture(page,folder,name,case):
    page.screenshot(path=str(folder/name))
    case.setdefault('image_receipts',{})[name]=image_receipt(folder/name)

def validate_artifacts(report,output):
    validate_report(report)
    for case in report['cases']:
      folder=output/(case['source'].replace('/','__').removesuffix('.md')+f"-{case['width']}")
      names=case['screenshots']+[r['image'] for r in case['displays']]+[r['right_image'] for r in case['displays'] if 'right_image' in r]
      assert set(case['image_receipts'])==set(names)
      for name in names:
        actual=image_receipt(folder/name)
        assert actual==case['image_receipts'][name],('Changed image',name)
        assert actual['dimensions']==[case['width'],900],actual

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--site-dir',type=Path,default=ROOT/'site');parser.add_argument('--output',type=Path,default=ROOT/'artifacts/deployed-math');args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);report={'status':'running','cases':[]}
    try:
      with serve_site(args.site_dir.resolve(),'https://zi-yue-1129.github.io/ai-wiki/') as base,sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
        for source in SOURCES:
          expected=source_displays((ROOT/source).read_text())
          for width in WIDTHS:
            folder=args.output/(source.replace('/','__').removesuffix('.md')+f'-{width}');folder.mkdir(exist_ok=True)
            case={'source':source,'width':width,'status':'running','errors':[],'displays':[],'screenshots':[],'expected_displays':len(expected),'expected_tex':expected};report['cases'].append(case)
            page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');page.on('pageerror',lambda e,c=case:c['errors'].append(str(e)))
            try:
              lang,path=target(source);response=page.goto(urljoin(base,path),wait_until='load');assert response and response.ok
              assert page.locator('html').get_attribute('lang')==lang
              case['math']=check_math_rendering(page);page.evaluate('document.fonts.ready')
              case['layout']=assert_document_fits(page,{'width':width})
              snapshot=page.evaluate(INSPECT);validate_snapshot(source,expected,snapshot);case['snapshot']=snapshot
              capture(page,folder,'top.png',case);case['screenshots'].append('top.png')
              for i in range(len(expected)):
                w=page.locator('.md-content__inner div.arithmatex').nth(i);w.scroll_into_view_if_needed();assert w.is_visible()
                g=w.evaluate(GEOMETRY);validate_geometry(g)
                image=f'display-{i:03d}.png';capture(page,folder,image,case);row={'image':image,'geometry':g};case['displays'].append(row)
                if g['scroll']:
                  end=w.evaluate('''w=>{const m=w.querySelector('mjx-container');let e=m;while(e){if(['auto','scroll'].includes(getComputedStyle(e).overflowX)&&e.scrollWidth>e.clientWidth+1){e.scrollLeft=e.scrollWidth;const r=e.getBoundingClientRect(),p=(m.querySelector('mjx-math')||m).getBoundingClientRect();return {position:e.scrollLeft,max:e.scrollWidth-e.clientWidth,right:p.right,viewport_left:r.left,viewport_right:r.left+e.clientWidth}}e=e.parentElement}throw Error('Scroller missing')}''');row['end']=end
                  assert end['max']>0 and abs(end['position']-end['max'])<=1
                  assert end['right']<=end['viewport_right']+1 and end['right']>=end['viewport_left'],end
                  right=f'display-{i:03d}-right.png';capture(page,folder,right,case);row['right_image']=right
                  w.evaluate('''w=>{for(let e=w.querySelector('mjx-container');e;e=e.parentElement)e.scrollLeft=0}''')
              if '/score-sde' in source:
                heading=page.locator('#核心想法' if lang=='zh-TW' else '#core-idea');heading.scroll_into_view_if_needed();capture(page,folder,'core-list.png',case);case['screenshots'].append('core-list.png')
              if '/double-machine-learning' in source:
                page.locator('#限制' if lang=='zh-TW' else '#limitations').scroll_into_view_if_needed();capture(page,folder,'limitations.png',case);case['screenshots'].append('limitations.png')
              assert not case['errors'],case['errors'];case['status']='passed'
            except Exception as error:
              case['status']='failed';case['failure']=repr(error)
              page.screenshot(path=str(folder/'failed.png'));(folder/'failed.html').write_text(page.content())
              (folder/'failed.json').write_text(json.dumps(case,ensure_ascii=False,indent=2));raise
            finally:page.close()
        browser.close()
      report['status']='passed';validate_report(report)
      validate_artifacts(report,args.output)
    except Exception as error:report['status']='failed';report['failure']=repr(error);raise
    finally:(args.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
