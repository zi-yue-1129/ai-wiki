#!/usr/bin/env python3
"""Exercise keyboard search on the built, Pagefind-indexed bilingual site."""
import argparse
from pathlib import Path
from urllib.parse import urljoin
from mkdocs.config import load_config
from playwright.sync_api import sync_playwright, expect
from test_built_motion_browser import serve_site

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--executable-path')
    args = parser.parse_args()
    config = load_config(str(ROOT / 'mkdocs.yml'))
    with serve_site(Path(config.site_dir), config.site_url) as base, sync_playwright() as pw:
        browser = pw.chromium.launch(**({'executable_path': args.executable_path} if args.executable_path else {}))
        for lang, path in [('en', ''), ('zh-TW', 'zh-TW/')]:
            page = browser.new_page()
            page.goto(urljoin(base, path), wait_until='domcontentloaded')
            query = page.locator('#wiki-search-query')
            clear = page.locator('.md-search__form button[type=reset]')
            results = page.locator('#wiki-search-list a')
            page.keyboard.press('/')
            expect(query).to_be_focused()
            query.fill('transformer')
            expect(results.first).to_be_visible(timeout=30000)
            page.keyboard.press('Tab')
            expect(clear).to_be_focused()
            assert clear.get_attribute('aria-label') == ('清除搜尋' if lang == 'zh-TW' else 'Clear search')
            page.keyboard.press('Tab')
            expect(page.locator('.md-search__scrollwrap')).to_be_focused()
            page.keyboard.press('Tab')
            expect(results.first).to_be_focused()
            page.keyboard.press('Shift+Tab')
            expect(page.locator('.md-search__scrollwrap')).to_be_focused()
            page.keyboard.press('Shift+Tab')
            expect(clear).to_be_focused()
            page.keyboard.press('Enter')
            expect(query).to_be_focused()
            expect(query).to_have_value('')
            expect(results).to_have_count(0)
            query.fill('attention')
            expect(results.first).to_be_visible(timeout=30000)
            query.fill('transformer')
            expect(results.first).to_be_visible(timeout=30000)
            page.keyboard.press('Tab'); page.keyboard.press('Tab'); page.keyboard.press('Tab')
            expect(results.first).to_be_focused()
            target = results.first.get_attribute('href')
            page.keyboard.press('Enter')
            page.wait_for_url(lambda url: url.path == target or url.path.rstrip('/') == target.rstrip('/'), timeout=30000)
            page.keyboard.press('/')
            query.fill('transformer')
            expect(results.first).to_be_visible(timeout=30000)
            page.keyboard.press('Tab'); page.keyboard.press('Tab'); page.keyboard.press('Tab')
            page.keyboard.press('Escape')
            assert not page.locator('#__search').is_checked()
            assert not page.locator('.md-search').evaluate('(el) => el.contains(document.activeElement)')
            page.close()
            # Delay an older request beyond a newer one and a reset using the actual built template.
            page = browser.new_page()
            page.route('**/pagefind/pagefind.js', lambda route: route.fulfill(content_type='text/javascript', body='''
export async function init() {}
export async function search(q) {
  await new Promise(r => setTimeout(r, q === 'old' ? 900 : 20));
  return {results:[{data:async()=>({url:'/ai-wiki/', meta:{title:q}, excerpt:q})}]};
}'''))
            page.goto(urljoin(base, path), wait_until='domcontentloaded')
            query = page.locator('#wiki-search-query'); results = page.locator('#wiki-search-list a')
            page.keyboard.press('/'); query.fill('old'); page.wait_for_timeout(100); query.fill('new')
            expect(results.first).to_contain_text('new')
            page.wait_for_timeout(1100)
            expect(results.first).to_contain_text('new')
            query.fill('old'); page.wait_for_timeout(100)
            page.keyboard.press('Tab'); page.keyboard.press('Enter')
            expect(query).to_be_focused(); page.wait_for_timeout(1100)
            expect(results).to_have_count(0)
            page.close()
            print(f'{lang}: keyboard, reset, stale responses, Escape and navigation passed')
        browser.close()

if __name__ == '__main__':
    main()
