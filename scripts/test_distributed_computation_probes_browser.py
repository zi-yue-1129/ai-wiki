#!/usr/bin/env python3
"""Real Chromium coverage for FSDP/Megatron computation probes."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'screenshots';OUT.mkdir(exist_ok=True)
JS=(ROOT/'docs/javascripts/distributed-computation-probes.js').read_text()
CSS=(ROOT/'docs/stylesheets/distributed-computation-probes.css').read_text()
with sync_playwright() as pw:
    opts={'headless':True,'args':['--no-sandbox']}
    if os.getenv('CHROMIUM_EXECUTABLE'):opts['executable_path']=os.environ['CHROMIUM_EXECUTABLE']
    browser=pw.chromium.launch(**opts)
    for lab in ['fsdp','megatron']:
        for lang in ['en','zh']:
            for width in [360,900]:
                for reduce in [False,True]:
                    ctx=browser.new_context(viewport={'width':width,'height':800},reduced_motion='reduce' if reduce else 'no-preference')
                    page=ctx.new_page()
                    page.set_content(f'<html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:12px;font:14px system-ui"><p><img src="/assets/concept-animations/{lab}-still.svg" alt="Fallback"></p><div class="distributed-computation-probe" data-probe="{lab}" data-lang="{lang}"></div></body></html>')
                    assert page.get_by_alt_text('Fallback').is_visible()  # GitHub/no-script baseline
                    page.add_style_tag(content=CSS);page.add_script_tag(content=JS)
                    host=page.locator('.distributed-computation-probe')
                    assert host.get_attribute('data-ready')=='yes'
                    assert page.get_by_alt_text('Fallback').is_hidden()
                    play=host.get_by_role('button',name='播放' if lang=='zh' else 'Play')
                    assert play.is_disabled()==reduce
                    seek=host.get_by_role('slider',name='時間軸' if lang=='zh' else 'Timeline')
                    next_button=host.get_by_role('button',name='下一步' if lang=='zh' else 'Next step')
                    next_button.focus();page.keyboard.press('Space')
                    assert '2/' in host.locator('.dcp-status').inner_text()
                    seek.focus();page.keyboard.press('Home')
                    assert '1/' in host.locator('.dcp-status').inner_text()
                    if lab=='fsdp':
                        assert '64.0 MiB' in host.locator('.dcp-stats').inner_text()
                        seek.fill('3');assert '64.0 MiB' in host.locator('.dcp-stats').inner_text()
                        host.get_by_role('checkbox',name='前向後重新分片' if lang=='zh' else 'Reshard after forward').uncheck()
                        assert '256.0 MiB' in host.locator('.dcp-stats').inner_text()
                        seek.fill('4');assert 'All-gathers: 1' in host.locator('.dcp-stats').inner_text() if lang=='en' else 'All-gather 次數: 1' in host.locator('.dcp-stats').inner_text()
                        host.get_by_role('slider',name='裝置數' if lang=='zh' else 'Ranks').fill('8')
                        seek.fill('6');assert '32.0 MiB' in host.locator('.dcp-stats').inner_text()
                        # Reshard requires two gathers; retain requires one.
                        host.get_by_role('checkbox',name='前向後重新分片' if lang=='zh' else 'Reshard after forward').check()
                        assert '448.0 MiB' in host.locator('.dcp-stats').inner_text()
                        assert host.locator('.dcp-transfer-row').count()==2
                        assert '224.0 MiB' in host.locator('.dcp-transfer-row').nth(1).inner_text()
                        seek.fill('0');assert '0.0 MiB' in host.locator('.dcp-transfer-row').first.inner_text()
                    else:
                        assert '16/32' in host.locator('.dcp-stats').inner_text()
                        assert '32 B' in host.locator('.dcp-stats').inner_text()  # full tensor payload, before any transfer
                        seek.fill('1');assert host.locator('.dcp-col').count()==32
                        assert host.locator('.dcp-gelu').count()==0
                        seek.fill('2');assert host.locator('.dcp-gelu').count()==32
                        host.get_by_role('slider',name='裝置數' if lang=='zh' else 'Ranks').fill('3')
                        assert host.locator('.dcp-lane').count()==8
                        assert '4/32' in host.locator('.dcp-stats').inner_text()
                        host.get_by_role('slider',name='Token 數' if lang=='zh' else 'Tokens').fill('4')
                        assert '0.0 B' in host.locator('.dcp-stats').inner_text()  # no early collective
                        seek.fill('4');assert host.locator('.dcp-visible').count()==1
                        ring=host.get_by_role('slider',name='Ring 回合' if lang=='zh' else 'Ring round')
                        assert ring.count()==1
                        assert host.locator('.dcp-ring-cell.dcp-ring-complete').count()==0
                        ring.fill('7')
                        assert host.locator('.dcp-ring-cell.dcp-ring-complete').count()==8
                        assert '56.0 / 112.0 B' in host.locator('.dcp-ring-foot').inner_text()
                        ring=host.get_by_role('slider',name='Ring 回合' if lang=='zh' else 'Ring round')
                        ring.fill('14')
                        assert host.locator('.dcp-ring-cell.dcp-ring-complete').count()==64
                        assert '112.0 B' in host.locator('.dcp-stats').inner_text()
                        assert host.locator('.dcp-output').count()==0
                        seek.fill('5');assert host.locator('.dcp-output').count()==8
                        assert host.locator('.dcp-ring-cell.dcp-ring-complete').count()==64
                    if not reduce:
                        seek.fill('0');play.click()
                        assert host.get_by_role('button',name='暫停' if lang=='zh' else 'Pause').count()==1
                        page.wait_for_timeout(950)
                        assert '2/' in host.locator('.dcp-status').inner_text()
                        host.get_by_role('button',name='暫停' if lang=='zh' else 'Pause').click()
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(lab,lang,width,reduce)
                    page.screenshot(path=str(OUT/f'probe-{lab}-{lang}-{width}-reduce-{reduce}.png'),full_page=True)
                    ctx.close()
    browser.close()
print('PASS: 16 Chromium combinations, FSDP cumulative gather tradeoff, exact Megatron ring reduce-scatter/all-gather states, keyboard, reduced-motion and overflow')
