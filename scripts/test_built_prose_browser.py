#!/usr/bin/env python3
"""Check selected prose sources in the real built site: locale, math, layout and screenshots."""
from pathlib import Path
import json
import os
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from test_built_motion_browser import serve_site, assert_document_fits, check_math_rendering

ROOT = Path(__file__).resolve().parents[1]

def target(source):
    source = source.removeprefix('docs/')
    lang = 'zh-TW' if source.endswith('.zh-TW.md') else 'en'
    stem = source.removesuffix('.md').removesuffix('.zh-TW')
    path = stem.removesuffix('index') if stem.endswith('/index') else stem+'/'
    return lang, ('' if lang == 'en' else 'zh-TW/')+path

def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', nargs='+', help='Repository Markdown paths (including translated sources).')
    parser.add_argument('--manifest', type=Path, help='JSON list of source paths or objects with source and optional overview.')
    parser.add_argument('--site-dir', type=Path, default=ROOT/'site')
    parser.add_argument('--output', type=Path, default=ROOT/'artifacts'/'prose-pages')
    args = parser.parse_args()
    entries = json.loads(args.manifest.read_text()) if args.manifest else args.sources
    assert entries, 'Pass --sources or --manifest'
    entries = [{'source': x} if isinstance(x, str) else x for x in entries]
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'status': 'running', 'cases': []}
    try:
        with serve_site(args.site_dir.resolve(), 'https://zi-yue-1129.github.io/ai-wiki/') as base, sync_playwright() as p:
            browser = p.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM_EXECUTABLE') or None)
            for entry in entries:
                source = entry['source']
                lang, relative = target(source)
                for width in (390, 1280):
                    case = {'source': source, 'lang': lang, 'width': width, 'status': 'running', 'errors': []}
                    report['cases'].append(case)
                    page = browser.new_page(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
                    page.on('pageerror', lambda e, c=case: c['errors'].append(str(e)))
                    url = urljoin(base, relative)
                    if entry.get('overview'):
                        _, overview = target(entry['overview'])
                        response = page.goto(urljoin(base, overview), wait_until='load')
                        assert response and response.ok
                        from posixpath import relpath
                        href = relpath(relative, overview)+'/'
                        link = page.locator(f'.md-content__inner a[href="{href}"]').first
                        assert link.count() == 1, (source, 'missing overview link', href)
                        link.click()
                        page.wait_for_url(url)
                        page.wait_for_load_state('load')
                    else:
                        response = page.goto(url, wait_until='load')
                        assert response and response.ok
                    assert page.locator('html').get_attribute('lang') == lang
                    case['math'] = check_math_rendering(page)
                    page.evaluate('document.fonts.ready')
                    case['layout'] = assert_document_fits(page, {'width': width})
                    assert page.locator('.md-content__inner h1').count() == 1
                    folder = args.output/(source.replace('/', '__').removesuffix('.md')+f'-{width}')
                    folder.mkdir(exist_ok=True)
                    page.screenshot(path=str(folder/'top.png'))
                    for name, selector in [('math', '.md-content__inner mjx-container'), ('table', '.md-content__inner table')]:
                        element = page.locator(selector).first
                        if element.count():
                            element.scroll_into_view_if_needed()
                            page.screenshot(path=str(folder/f'{name}.png'))
                    assert not case['errors'], case
                    case['status'] = 'passed'
                    page.close()
            browser.close()
        report['status'] = 'passed'
    finally:
        (args.output/'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Prose pages: {len(report['cases'])} bilingual desktop/mobile cases passed")

if __name__ == '__main__':
    main()
