"""Literal source-to-production-render guards for eight pre-existing pages."""
import copy
import hashlib
import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml
from test_forward_math_markup import render, MathContainers, require_no_outside_tex
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'scripts/fixtures/existing-math-followup.json'
PAGES=('docs/society/interpretability/feature-attribution.md','docs/society/interpretability/feature-attribution.zh-TW.md','docs/theory/models/cnn/unet/3d-unet.md','docs/theory/models/cnn/unet/3d-unet.zh-TW.md','docs/theory/models/rnn/gated-cells/gru/index.md','docs/theory/models/rnn/gated-cells/gru/index.zh-TW.md','docs/theory/paradigms/probabilistic/mcmc/gibbs-sampling.md','docs/theory/paradigms/probabilistic/mcmc/gibbs-sampling.zh-TW.md')
COUNTS=(1,1,3,3,6,6,7,7)
REPAIRED=(1,1,2,2,2,2,4,4)
MUTATIONS=(1,1,2,2,1,1,4,4)

def verify(source,record):
    html=render(source);require_no_outside_tex(html)
    bodies=[''.join(x.split())[2:-2]for x in MathContainers(html).blocks]
    assert bodies==record['all_display_bodies']
    assert len(bodies)==record['display_count']
    for body in record['repaired_bodies']:assert bodies.count(''.join(body.split()))==1
    if 'list' in record:
        spec=record['list'];segment=re.search('<h2 id="'+spec['heading_id']+r'"[^>]*>.*?(?=<h2\b|\Z)',html,re.S);assert segment
        root=ET.fromstring('<root>'+segment[0].replace('&para;','¶')+'</root>');lists=root.findall('ul');assert len(lists)==1
        items=lists[0].findall('li');assert len(items)==4
        assert [''.join(x.find('.//strong').itertext())for x in items]==spec['titles']
        target=items[3];formulas=[x for x in target.iter('div')if 'arithmatex'in x.get('class','').split()];assert len(formulas)==1
        assert ''.join(''.join(formulas[0].itertext()).split())[2:-2]==bodies[0]
        assert len(target.findall('p'))==spec['item']['paragraphs']

def workflow_check(w):
    job=w['jobs']['build-docs'];assert 'if'not in job and (job.get('continue-on-error')is None or job.get('continue-on-error')is False)
    def locations(command):
        return [(i,j)for i,s in enumerate(job['steps'])if 'if'not in s and (s.get('continue-on-error')is None or s.get('continue-on-error')is False)for j,line in enumerate(s.get('run','').splitlines())if line.strip()==command]
    deps=locations('pip install -r requirements.txt');tests=locations('python scripts/test_existing_math_followup.py');assert len(tests)==1 and any(d<tests[0]for d in deps)
    paths=w.get('on',w.get(True))['pull_request']['paths']
    assert set(PAGES+('scripts/test_existing_math_followup.py','scripts/fixtures/existing-math-followup.json'))<=set(paths)

class ExistingMath(unittest.TestCase):
    def setUp(self):self.records=json.loads(FIXTURE.read_text())['pages']
    def test_independent_eight_page_scope_and_original_bytes(self):
        self.assertEqual(tuple(x['page']for x in self.records),PAGES)
        self.assertEqual(tuple(x['display_count']for x in self.records),COUNTS)
        self.assertEqual(tuple(len(x['repaired_bodies'])for x in self.records),REPAIRED)
        self.assertEqual(tuple(len(x['mutations'])for x in self.records),MUTATIONS)
        for record in self.records:
            source=(ROOT/record['page']).read_text();verify(source,record)
            for mutation in record['mutations']:
                self.assertEqual(source.count(mutation['new']),1);source=source.replace(mutation['new'],mutation['old'],1)
            self.assertEqual(hashlib.sha256(source.encode()).hexdigest(),record['original_source_sha256'])
    def test_each_original_markup_regression_missing_formula_and_raw_duplicate(self):
        for record in self.records:
            source=(ROOT/record['page']).read_text()
            bads=[source.replace(m['new'],m['old'],1)for m in record['mutations']]
            for body in record['repaired_bodies']:
                self.assertIn(body,source)
                bads += [source.replace(body,'',1),source+'\n\n<p>'+body+'</p>\n']
            for bad in bads:
                self.assertNotEqual(bad,source)
                with self.assertRaises(AssertionError):verify(bad,record)
    def test_future_each_document_fixture_and_test_route(self):
        w=yaml.safe_load((ROOT/'.github/workflows/concept-animation-validation.yml').read_text());workflow_check(w)
        for path in PAGES+('scripts/test_existing_math_followup.py','scripts/fixtures/existing-math-followup.json'):
            bad=copy.deepcopy(w);bad[True]['pull_request']['paths'].remove(path)
            with self.assertRaises(AssertionError):workflow_check(bad)
        for command in ['pip install -r requirements.txt','python scripts/test_existing_math_followup.py']:
            for key,value in [('if',False),('if',None),('continue-on-error',True),('continue-on-error',0),('run','# '+command),('run',command+' || true')]:
                bad=copy.deepcopy(w)
                for step in bad['jobs']['build-docs']['steps']:
                    if command in step.get('run','').splitlines():step[key]=value
                with self.assertRaises(AssertionError):workflow_check(bad)

if __name__=='__main__':unittest.main()
