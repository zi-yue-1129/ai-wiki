#!/usr/bin/env python3
"""Test built bilingual Pagefind pagination and controlled asynchronous batches."""
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from mkdocs.config import load_config
from playwright.sync_api import sync_playwright, expect
from test_built_motion_browser import serve_site

ROOT = Path(__file__).resolve().parents[1]
MOCK = '''
export async function init() {}
window.calls = []; window.failOnce = true;
export async function search(q) {
  let count = q === 'empty' ? 0 : q === 'small' ? 3 : 23;
  return {results: Array.from({length:count}, (_, i) => ({data: async () => {
    window.calls.push(q + ':' + i);
    if (q === 'slow' || i >= 10) await new Promise(r => setTimeout(r, 500));
    if (q === 'failure' && i === 12 && window.failOnce) { window.failOnce = false; throw Error('failed'); }
    return {url:'/ai-wiki/?' + q + i, meta:{title:q + i}, excerpt:q};
  }}))};
}'''

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--executable-path'); args = parser.parse_args()
    config = load_config(str(ROOT / 'mkdocs.yml'))
    with serve_site(Path(config.site_dir), config.site_url) as base, sync_playwright() as pw:
        browser = pw.chromium.launch(**({'executable_path': args.executable_path} if args.executable_path else {}))
        for lang, path in [('en', ''), ('zh-TW', 'zh-TW/')]:
            page = browser.new_page(); page.goto(urljoin(base, path), wait_until='domcontentloaded')
            page.keyboard.press('/'); q = page.locator('#wiki-search-query'); links = page.locator('#wiki-search-list a'); more = page.locator('#wiki-search-more'); meta = page.locator('#wiki-search-meta')
            q.fill('transformer'); expect(links).to_have_count(10, timeout=30000); expect(more).to_be_visible()
            # Navigate from the last initial result to the button with the keyboard.
            links.nth(9).focus(); page.keyboard.press('Tab'); expect(more).to_be_focused(); page.keyboard.press('Enter')
            expect(links.nth(10)).to_be_focused(timeout=30000)
            total = int(meta.inner_text().split('/')[1].split()[0]) if lang == 'zh-TW' else int(meta.inner_text().split(' of ')[1].split()[0])
            while more.is_visible():
                more.focus(); page.keyboard.press('Enter'); page.wait_for_function("!document.querySelector('#wiki-search-more').hasAttribute('aria-disabled')", timeout=30000)
            expect(links).to_have_count(total); hrefs = links.evaluate_all('(els) => els.map(e => e.href)'); assert len(hrefs) == len(set(hrefs))
            target = links.nth(10).get_attribute('href'); links.nth(10).focus(); page.keyboard.press('Enter')
            page.wait_for_url(lambda url: urlsplit(url).path.rstrip('/') == urlsplit(target).path.rstrip('/'), timeout=30000)
            page.close()
            page = browser.new_page(); page.route('**/pagefind/pagefind.js', lambda r: r.fulfill(content_type='text/javascript', body=MOCK)); page.goto(urljoin(base, path), wait_until='domcontentloaded')
            page.keyboard.press('/'); q=page.locator('#wiki-search-query'); links=page.locator('#wiki-search-list a'); more=page.locator('#wiki-search-more'); meta=page.locator('#wiki-search-meta')
            q.fill('small'); expect(links).to_have_count(3); expect(more).to_be_hidden(); assert '3' in meta.inner_text()
            q.fill('empty'); expect(links).to_have_count(0); expect(more).to_be_hidden()
            q.fill('failure'); expect(links).to_have_count(10); assert len(page.evaluate('window.calls.filter(x => x.startsWith("failure:") )')) == 10
            more.focus(); page.keyboard.press('Enter'); page.keyboard.press('Enter'); expect(more).to_have_text('載入失敗，重試' if lang == 'zh-TW' else 'Loading failed, retry', timeout=5000)
            expect(links).to_have_count(10); assert len(page.evaluate('window.calls.filter(x => x.startsWith("failure:") )')) == 20
            page.keyboard.press('Enter'); expect(links).to_have_count(20, timeout=5000); expect(links.nth(10)).to_be_focused(); more.focus(); page.keyboard.press('Enter'); expect(links).to_have_count(23, timeout=5000); expect(more).to_be_hidden()
            assert links.locator('.md-search-result__title').all_text_contents() == [f'failure{i}' for i in range(23)]
            assert ('23 / 23' if lang == 'zh-TW' else '23 of 23') in meta.inner_text()
            q.fill('slow'); page.wait_for_timeout(100); q.fill('small'); expect(links).to_have_count(3); page.wait_for_timeout(700); expect(links).to_have_count(3)
            q.fill('failure'); expect(links).to_have_count(10); more.focus(); page.keyboard.press('Enter'); q.focus(); q.fill('small'); expect(links).to_have_count(3); page.wait_for_timeout(700); expect(links).to_have_count(3)
            q.fill('failure'); expect(links).to_have_count(10); more.focus(); page.keyboard.press('Enter'); page.locator('.md-search__form button[type=reset]').click(); expect(q).to_have_value(''); page.wait_for_timeout(700); expect(links).to_have_count(0); expect(more).to_be_hidden()
            page.close(); print(f'{lang}: real index and controlled batches passed')
        browser.close()

if __name__ == '__main__': main()
