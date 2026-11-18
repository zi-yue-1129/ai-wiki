#!/usr/bin/env python3
"""Offline evidence-card search. Returns candidates, never generated answers.

python scripts/knowledge.py validate
python scripts/knowledge.py search 'QLoRA 運算精度'
python scripts/knowledge.py get qlora-comparison
python scripts/knowledge.py evaluate
"""
import argparse
import datetime as dt
import json
import math
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'docs/assets/knowledge/lora-qlora.json'
CASES = ROOT / 'scripts/fixtures/knowledge-queries.json'
STOP = set('a an the is are of to on in at for and or how what does do can why with it its only'.split())


def tokens(text):
    """English words and Chinese bigrams, without a model/API dependency."""
    out = set(re.findall(r'[a-z0-9]+', text.lower())) - STOP
    for run in re.findall(r'[\u3400-\u9fff]+', text):
        out.update(run[i:i+2] for i in range(len(run)-1))
        if len(run) == 1:
            out.add(run)
    return out


def load(path=CATALOG):
    return json.loads(path.read_text(encoding='utf-8'))


def validate(data, root=ROOT):
    """Structural validation only: cannot prove a source supports a claim."""
    errors = []
    if not isinstance(data, dict):
        return ['catalog must be an object']
    for field in ('scope', 'license'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f'{field} requires a nonempty string')
    if type(data.get('schema_version')) is not int or data.get('schema_version') != 1:
        errors.append('unsupported schema_version')
    sources = data.get('sources', {})
    if not isinstance(sources, dict) or not sources:
        return errors + ['sources must be a nonempty object']
    for key, source in sources.items():
        if not isinstance(source, dict):
            errors.append(f'{key}: source must be an object')
            continue
        if any(not isinstance(source.get(field), str) or not source[field].strip() for field in ('url', 'title', 'version')):
            errors.append(f'{key}: source fields must be nonempty strings')
            continue
        try:
            url = urlparse(source['url'])
        except ValueError:
            errors.append(f'{key}: invalid source URL')
            continue
        if url.scheme != 'https' or not url.netloc or not source.get('version') or not source.get('title'):
            errors.append(f'{key}: requires HTTPS URL, title and version')
    claims = data.get('claims', [])
    if not isinstance(claims, list) or not claims:
        return errors + ['claims must be a nonempty list']
    ids = set()
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append('claim must be an object')
            continue
        cid = claim.get('id', '')
        if not isinstance(cid, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', cid) or cid in ids:
            errors.append(f'{cid}: invalid or duplicate id')
        ids.add(str(cid))
        page = claim.get('page', '')
        try:
            if not isinstance(page, str) or not page.strip():
                raise ValueError('page requires a nonempty string')
            path = (root / 'docs' / page).resolve()
        except (ValueError, OSError):
            errors.append(f'{cid}: invalid page path')
            continue
        docs = (root / 'docs').resolve()
        if not path.is_relative_to(docs) or path.suffix != '.md' or not path.is_file():
            errors.append(f'{cid}: page must be an existing Markdown file under docs')
        else:
            headings = re.findall(r'^#{1,6}\s+(.+?)\s*$', path.read_text(encoding='utf-8'), re.M)
            if claim.get('section') not in headings:
                errors.append(f'{cid}: section missing from page')
        for field in ('summary', 'limits'):
            value = claim.get(field)
            if not isinstance(value, dict) or any(not isinstance(v, str) or not v.strip() for v in value.values()) or any(not isinstance(value.get(lang), str) or not value[lang].strip() for lang in ('en', 'zh-TW')):
                errors.append(f'{cid}: {field} requires nonempty en and zh-TW strings')
        aliases = claim.get('aliases')
        if not isinstance(aliases, list) or not aliases or any(not isinstance(a, str) or not a.strip() for a in aliases):
            errors.append(f'{cid}: aliases must be nonempty strings')
        evidence = claim.get('evidence')
        if not isinstance(evidence, list) or not evidence:
            errors.append(f'{cid}: evidence required')
        else:
            for ev in evidence:
                if not isinstance(ev, dict) or not isinstance(ev.get('source'), str) or ev['source'] not in sources or not isinstance(ev.get('locator'), str) or not ev['locator'].strip():
                    errors.append(f'{cid}: unresolved evidence or missing locator')
        review = claim.get('review', {})
        if not isinstance(review, dict):
            errors.append(f'{cid}: review must be an object')
            continue
        if review.get('method') != 'source-reading' or review.get('independently_reproduced') is not False or not isinstance(review.get('scope'), str) or not review['scope'].strip():
            errors.append(f'{cid}: pilot review must be scoped source-reading, not reproduction')
        try:
            value = review.get('checked_on', '')
            if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                raise ValueError('date must use YYYY-MM-DD')
            checked = dt.date.fromisoformat(value)
            if checked > dt.date.today():
                errors.append(f'{cid}: future review date')
        except (ValueError, TypeError):
            errors.append(f'{cid}: checked_on requires ISO date')
    return errors


def record(data, claim):
    result = dict(claim)
    result['evidence'] = [dict(ev, **data['sources'][ev['source']]) for ev in claim['evidence']]
    result['page_url'] = 'https://github.com/zi-yue-1129/ai-wiki/blob/main/docs/' + claim['page']
    return result


def search(data, query, limit=3):
    q = tokens(query)
    docs = [tokens(' '.join([c['id'], *c['aliases'], *c['summary'].values(), *c['limits'].values()])) for c in data['claims']]
    scored = []
    for c, terms in zip(data['claims'], docs):
        overlap = q & terms
        if not overlap:
            continue
        score = sum(math.log(1 + len(docs) / sum(t in d for d in docs)) for t in overlap)
        scored.append((score, c))
    scored.sort(key=lambda x: (-x[0], x[1]['id']))
    return [dict(record(data, c), lexical_score=round(score, 4)) for score, c in scored[:limit]]


def evaluate(data, cases):
    results = []
    for case in cases:
        ids = [r['id'] for r in search(data, case['query'])]
        expected = case['expected_ids']
        passed = bool(set(expected) & set(ids)) if expected else not ids
        results.append(dict(query=case['query'], expected_ids=expected, retrieved_ids=ids, passed=passed))
    return {'kind':'retrieval_smoke_test_not_answer_accuracy', 'passed':sum(r['passed'] for r in results), 'total':len(results), 'cases':results}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['validate', 'search', 'get', 'evaluate'])
    p.add_argument('query', nargs='?')
    p.add_argument('--limit', type=int, choices=range(1, 21), default=3)
    args = p.parse_args()
    data = load()
    errors = validate(data)
    if errors:
        print(json.dumps({'errors':errors}, ensure_ascii=False, indent=2))
        return 1
    if args.command == 'validate':
        out = {'valid':True, 'claims':len(data['claims']), 'note':'Structure only, not semantic verification'}
    elif args.command == 'evaluate':
        out = evaluate(data, load(CASES))
    else:
        if not args.query or not args.query.strip():
            p.error('a nonempty query or id is required')
        if args.command == 'get':
            results = [record(data, c) for c in data['claims'] if c['id'] == args.query]
        else:
            results = search(data, args.query, args.limit)
        out = {'status':'candidates_not_answers' if results else 'no_matching_evidence', 'scope':data['scope'], 'results':results}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return int(args.command == 'evaluate' and out['passed'] != out['total'])


if __name__ == '__main__':
    raise SystemExit(main())
