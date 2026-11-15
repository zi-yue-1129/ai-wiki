"""Chromium visual/semantic regression for synthetic Kalman and particle labs.
Run: python scripts/test_bayesian_filter_labs_browser.py
"""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
OUT=Path('artifacts/bayesian-filter-labs')
OUT.mkdir(parents=True,exist_ok=True)
JS=(ROOT.parent/'docs/javascripts/bayesian-filter-labs.js').read_text(encoding='utf-8')
CSS=(ROOT.parent/'docs/stylesheets/bayesian-filter-labs.css').read_text(encoding='utf-8')
INSIGHT_JS=(ROOT.parent/'docs/javascripts/bayesian-filter-insights.js').read_text(encoding='utf-8')
INSIGHT_CSS=(ROOT.parent/'docs/stylesheets/bayesian-filter-insights.css').read_text(encoding='utf-8')
COMPARISON_JS=(ROOT.parent/'docs/javascripts/bayesian-filter-comparisons.js').read_text(encoding='utf-8')
INVARIANTS_JS=(ROOT.parent/'docs/javascripts/bayesian-filter-invariants.js').read_text(encoding='utf-8')

def fixture(lang='en'):
    fallback='Interactive numerical experiment requires JavaScript.' if lang=='en' else '互動數值實驗需要 JavaScript。'
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{max-width:960px;margin:0 auto;padding:12px;font-family:system-ui;background:#fff;color:#24394c}}*{{box-sizing:border-box}}{CSS}{INSIGHT_CSS}</style></head><body>
    <h1>{'Bayesian filter labs' if lang=='en' else '貝氏濾波互動實驗'}</h1>
    <h2>Kalman filter</h2><div class="bayesian-filter-lab" data-lab="kalman" data-lang="{lang}"><p class="bayesian-filter-fallback">{fallback}</p></div>
    <h2>Particle filter</h2><div class="bayesian-filter-lab" data-lab="particle" data-lang="{lang}"><p class="bayesian-filter-fallback">{fallback}</p></div>
    <script>{JS}</script><script>{INSIGHT_JS}</script><script>{COMPARISON_JS}</script><script>{INVARIANTS_JS}</script></body></html>'''

async def run():
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True,args=['--no-sandbox'])
        cases=0
        for lang in ('en','zh'):
            for width in (320,360,800,1024):
                page=await browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
                await page.set_content(fixture(lang),wait_until='load')
                labs=page.locator('.bf-panel');assert await labs.count()==2
                assert await page.locator('.bayesian-filter-fallback').count()==0
                assert await page.locator('.bf-graphic svg').count()==10
                assert await page.locator('svg[data-bf-invariant]').count()==2
                assert await page.locator('svg[data-bf-comparison]').count()==2
                assert await page.locator('svg[data-bf-diagnostic]').count()==2
                assert await page.locator('svg[data-bf-advanced]').count()==2
                init_k=await labs.nth(0).locator('.bf-advanced + .bf-insight-summary').inner_text()
                init_p=await labs.nth(1).locator('.bf-advanced + .bf-insight-summary').inner_text()
                assert ('Prediction only' in init_k if lang=='en' else '預測階段' in init_k)
                assert ('have not occurred' in init_p if lang=='en' else '尚未進行' in init_p)
                assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),f'{lang}/{width} page overflow'
                # Dynamic Kalman numeric result; y=7, prior=3, P=1.44, R=.64.
                ktext=await labs.nth(0).locator('.bf-output').inner_text()
                assert '3.000' in ktext and '1.440' in ktext,ktext
                # Move to final phase and assert posterior path appears.
                await labs.nth(0).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                await labs.nth(0).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                assert await labs.nth(0).locator('.bf-graphic').first.locator('svg path').count()==3
                assert '5.769' in await labs.nth(0).locator('.bf-output').inner_text()
                gain_svg=labs.nth(0).locator('svg[data-bf-diagnostic="kalman"]')
                assert abs(float(await gain_svg.get_attribute('data-gain'))-1.44/2.08)<1e-6
                assert abs(float(await gain_svg.get_attribute('data-shift'))-4*1.44/2.08)<1e-6
                compare_k=labs.nth(0).locator('svg[data-bf-comparison="kalman"]')
                assert abs(float(await compare_k.get_attribute('data-posterior-mean'))-5.769230769230769)<1e-6
                joseph=labs.nth(0).locator('svg[data-bf-invariant="kalman"]')
                j_prior=float(await joseph.get_attribute('data-prior-contribution'))
                j_noise=float(await joseph.get_attribute('data-noise-contribution'))
                assert abs(j_prior+j_noise-(1-1.44/2.08)*1.44)<1e-7
                assert abs(j_prior-((1-1.44/2.08)**2*1.44))<1e-7
                assert abs(j_noise-(1.44/2.08)**2*.64)<1e-7
                assert await joseph.get_attribute('data-stage')=='2'
                nis_svg=labs.nth(0).locator('svg[data-bf-advanced="kalman"]')
                assert abs(float(await nis_svg.get_attribute('data-nis'))-16/2.08)<1e-6
                live_k=await labs.nth(0).locator('.bf-advanced + .bf-insight-summary').inner_text()
                assert '7.692' in live_k
                assert abs(float(await gain_svg.get_attribute('data-posterior-variance'))-(1-1.44/2.08)*1.44)<1e-6
                # R slider changes gain, not merely the plot's display coordinates.
                await labs.nth(0).locator('.bf-ranges input').nth(1).fill('3')
                assert float(await gain_svg.get_attribute('data-gain'))<.35
                assert float(await compare_k.get_attribute('data-gain'))<.35
                await labs.nth(0).locator('.bf-ranges input').nth(1).fill('0.64')
                # Particle weights exactly normalised, systematic ancestor sequence.
                ptext=await labs.nth(1).locator('.bf-output').inner_text()
                assert 'N = 10' in ptext,ptext
                await labs.nth(1).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                assert 'Σw = 1.000' in await labs.nth(1).locator('.bf-output').inner_text()
                await labs.nth(1).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                await labs.nth(1).get_by_role('button',name='Next' if lang=='en' else '下一步').click()
                assert await labs.nth(1).locator('svg circle').count()>=4
                cdf_svg=labs.nth(1).locator('svg[data-bf-diagnostic="particle"]')
                assert await cdf_svg.get_attribute('data-ancestors')=='4,5,6,6,6,7,7,8,8,9'
                compare_p=labs.nth(1).locator('svg[data-bf-comparison="particle"]')
                assert abs(float(await compare_p.get_attribute('data-weighted-mean'))-6.369761008216016)<1e-6
                assert abs(float(await compare_p.get_attribute('data-resampled-mean'))-6.48)<1e-6
                discrepancy=labs.nth(1).locator('svg[data-bf-invariant="particle"]')
                gaps=[float(x) for x in (await discrepancy.get_attribute('data-deltas')).split(',')]
                assert len(gaps)==11 and abs(gaps[0])<1e-8 and abs(gaps[-1])<1e-8
                assert max(map(abs,gaps))<1
                assert await discrepancy.get_attribute('data-stage')=='3'
                assert await discrepancy.get_attribute('data-cumulative-last')=='10'
                if width in (320,1024):
                    await page.screenshot(path=str(OUT/f'{lang}-{width}-final-comparison.png'),full_page=True)
                    if width==320:
                        for region in await page.locator('.bf-comparison').all():
                            await region.evaluate('(e)=>e.scrollLeft=e.scrollWidth')
                        await page.screenshot(path=str(OUT/f'{lang}-{width}-comparison-right.png'),full_page=True)
                        for region in await page.locator('.bf-comparison').all():
                            await region.evaluate('(e)=>e.scrollLeft=0')
                offspring=labs.nth(1).locator('svg[data-bf-advanced="particle"]')
                assert await offspring.get_attribute('data-counts')=='0,0,0,0,1,1,3,2,2,1'
                assert await offspring.get_attribute('data-total')=='10'
                assert await offspring.get_attribute('data-unique')=='6'
                live_p=await labs.nth(1).locator('.bf-advanced + .bf-insight-summary').inner_text()
                assert ('Ten realised copies' in live_p if lang=='en' else '實際 10 個複本' in live_p)
                assert abs(float(await offspring.get_attribute('data-expected-total'))-10)<1e-6
                assert abs(float(await cdf_svg.get_attribute('data-weight-sum'))-1)<1e-6
                ess=float(await cdf_svg.get_attribute('data-ess'))
                # Changing only the systematic threshold offset cannot change weights/ESS.
                before_disc=float(await discrepancy.get_attribute('data-max-discrepancy'))
                await labs.nth(1).locator('.bf-ranges input').nth(2).fill('0.025')
                assert abs(float(await discrepancy.get_attribute('data-max-discrepancy'))-before_disc)>1e-3
                assert abs(float(await compare_p.get_attribute('data-resampled-mean'))-6.11)<1e-6
                assert abs(float(await cdf_svg.get_attribute('data-ess'))-ess)<1e-6
                await labs.nth(1).locator('.bf-ranges input').nth(2).fill('0.045')
                # All calculated SVG text remains inside its own viewBox.
                for i in range(2):
                    labels_outside=await page.locator('svg[data-bf-diagnostic]').nth(i).evaluate(
                        "(svg)=>[...svg.querySelectorAll('text')].filter(e=>{const b=e.getBBox();return b.x < -1 || b.y < -1 || b.x+b.width > 701 || b.y+b.height > 231}).map(e=>e.textContent)"
                    )
                    assert not labels_outside,(lang,width,i,labels_outside)
                for i in range(2):
                    bad=await page.locator('svg[data-bf-comparison]').nth(i).evaluate("(s)=>[...s.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x<-1||b.y<-1||b.x+b.width>701||b.y+b.height>225}).map(t=>t.textContent)")
                    assert not bad,(lang,width,i,bad)
                for i in range(2):
                    bad=await page.locator('svg[data-bf-invariant]').nth(i).evaluate("(s)=>[...s.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x<-1||b.y<-1||b.x+b.width>701||b.y+b.height>245}).map(t=>t.textContent)")
                    assert not bad,(lang,width,i,bad)
                for i in range(2):
                    bad=await page.locator('svg[data-bf-advanced]').nth(i).evaluate("(s)=>[...s.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x<-1||b.y<-1||b.x+b.width>701||b.y+b.height>231}).map(t=>t.textContent)")
                    assert not bad,(lang,width,i,bad)
                # Seek and reset works.
                await labs.nth(1).locator('.bf-step').fill('1')
                assert await compare_p.get_attribute('data-stage')=='1'
                assert await discrepancy.get_attribute('data-stage')=='1'
                assert await discrepancy.locator('path').count()==0
                assert ('Realised cumulative counts appear only' in await labs.nth(1).locator('.bf-invariant + .bf-insight-summary').inner_text() if lang=='en' else '才顯示實際累積' in await labs.nth(1).locator('.bf-invariant + .bf-insight-summary').inner_text())
                assert 'resampled mean' not in (await labs.nth(1).locator('.bf-comparison + .bf-insight-summary').inner_text()).lower()
                await labs.nth(1).get_by_role('button',name='Reset' if lang=='en' else '重設').click()
                assert (await labs.nth(1).locator('.bf-step').input_value())=='0'
                # Keyboard access + focus outlines.
                await labs.nth(0).locator('.bf-step').focus()
                await page.keyboard.press('End')
                assert (await labs.nth(0).locator('.bf-step').input_value())=='2'
                await page.screenshot(path=str(OUT/f'{lang}-{width}.png'),full_page=True)
                # Extreme observations can move the mean toward the right edge.
                # Verify no numerical label overlaps a drawn mean marker.
                for extreme_y in (1, 9):
                    await labs.nth(0).locator('.bf-ranges input').nth(2).fill(str(extreme_y))
                    await labs.nth(1).locator('.bf-ranges input').nth(0).fill(str(extreme_y))
                    await labs.nth(1).locator('.bf-ranges input').nth(1).fill('0.4')
                    await labs.nth(1).locator('.bf-step').fill('3')
                    for comparison in await page.locator('svg[data-bf-comparison]').all():
                        intersections=await comparison.evaluate("""s=>{
                            let hits=[];
                            for(const t of s.querySelectorAll('text')){
                                const b=t.getBBox();
                                for(const dot of s.querySelectorAll('circle')){
                                    const x=+dot.getAttribute('cx'), y=+dot.getAttribute('cy'), r=+dot.getAttribute('r');
                                    if(b.x<x+r && b.x+b.width>x-r && b.y<y+r && b.y+b.height>y-r)
                                        hits.push(t.textContent);
                                }
                            }
                            return hits;
                        }""")
                        assert not intersections,(lang,width,extreme_y,intersections)
                    # The observation label must not be drawn over a large
                    # descendant-count bubble (all ten may share one ancestor).
                    clash=await labs.nth(1).locator('.bf-graphic svg').first.evaluate("""s=>{
                        const t=[...s.querySelectorAll('text')].find(x=>x.textContent==='y');
                        if(!t)return ['missing y'];
                        const b=t.getBBox();
                        return [...s.querySelectorAll('circle[fill="#209e9a"]')].filter(dot=>{
                            const x=+dot.getAttribute('cx'),y=+dot.getAttribute('cy'),r=+dot.getAttribute('r');
                            return b.x<x+r && b.x+b.width>x-r && b.y<y+r && b.y+b.height>y-r;
                        }).map(dot=>dot.getAttribute('cx'));
                    }""")
                    assert not clash,(lang,width,extreme_y,clash)
                    if extreme_y==9 and width in (320,1024):
                        await page.screenshot(path=str(OUT/f'{lang}-{width}-extreme-comparison.png'),full_page=True)

                await page.close();cases+=1
        # Test reduced-motion without spontaneous autoplay, and no-script fallbacks.
        page=await browser.new_page(reduced_motion='reduce')
        await page.set_content(fixture('en'))
        assert (await page.locator('.bf-panel').nth(0).get_by_role('button',name='Play').count())==1
        await page.close();cases+=1
        page=await browser.new_page(java_script_enabled=False)
        await page.set_content(fixture('zh'))
        assert await page.locator('.bayesian-filter-fallback').count()==2
        await page.close();cases+=1
        await browser.close()
        print(json.dumps({'cases':cases,'result':'PASS','screenshots':len(list(OUT.glob('*.png')))}))

if __name__=='__main__':asyncio.run(run())