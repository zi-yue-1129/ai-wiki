"""Check teaching HMM numbers against independent hidden-path enumeration."""
from itertools import product
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/concept-animations'
NS = '{http://www.w3.org/2000/svg}'
pi = (.6, .4)
A = ((.7, .3), (.4, .6))
B = ((.8, .3), (.2, .9), (.7, .4))

def paths(length):
    for z in product(range(2), repeat=length):
        p = pi[z[0]] * B[0][z[0]]
        for t in range(1, length):
            p *= A[z[t-1]][z[t]] * B[t][z[t]]
        yield z, p

alpha = [[sum(p for z, p in paths(t+1) if z[-1] == j) for j in range(2)] for t in range(3)]
likelihood = sum(alpha[-1])
assert abs(likelihood - .147936) < 1e-12
filtered = [a[0]/sum(a) for a in alpha]
gamma = [[sum(p for z, p in paths(3) if z[t] == j)/likelihood for j in range(2)] for t in range(3)]
xi = [[[sum(p for z, p in paths(3) if z[t] == i and z[t+1] == j)/likelihood for j in range(2)] for i in range(2)] for t in range(2)]
counts = [[sum(x[i][j] for x in xi) for j in range(2)] for i in range(2)]
updated = [[v/sum(row) for v in row] for row in counts]
for t in range(2):
    assert abs(sum(map(sum, xi[t])) - 1) < 1e-12
    for j in range(2):
        assert abs(sum(xi[t][j]) - gamma[t][j]) < 1e-12
        assert abs(sum(xi[t][i][j] for i in range(2)) - gamma[t+1][j]) < 1e-12
assert abs(sum(map(sum, counts)) - 2) < 1e-12

def svg(name, kind):
    return ET.parse(ASSETS / f'hmm-{name}-{kind}.svg').getroot()

def texts(r):
    return '|'.join(e.text or '' for e in r.iter(NS+'text'))

def bars(r):
    return [list(map(float, e.get('values').split(';'))) for e in r.iter(NS+'animate') if e.get('attributeName') == 'width']

def near(actual, expected):
    assert abs(actual - expected) <= .0011, (actual, expected)

for kind in ('motion', 'still'):
    s = texts(svg('forward-sum-product', kind))
    for row in alpha:
        for value in row:
            assert f'{value:.6f}' in s
    assert f'{likelihood:.6f}' in s
    s = texts(svg('filter-smooth', kind))
    for value in filtered + [g[0] for g in gamma]:
        assert f'{value*100:.1f}%' in s
    s = texts(svg('pairwise-posterior', kind))
    for table in (xi if kind == 'motion' else xi[-1:]):
        for row in table:
            for value in row:
                assert f'{value:.3f}' in s
    s = texts(svg('baum-welch-transition', kind))
    for row in counts + updated:
        for value in row:
            assert f'{value:.3f}' in s
for actual, first, last in zip(bars(svg('filter-smooth','motion')), filtered[:2], [g[0] for g in gamma[:2]]):
    near(actual[0], 184*first)
    near(actual[2], 184*last)
for k, actual in enumerate(bars(svg('pairwise-posterior','motion'))):
    i,j=divmod(k,2)
    near(actual[0],151*xi[0][i][j]); near(actual[2],151*xi[1][i][j])
for actual,value in zip(bars(svg('baum-welch-transition','motion')), sum(updated,[])):
    near(actual[2],290*value)
# Static geometry must show the same final values as the animated endpoint.
r = svg('filter-smooth', 'still')
actual = [e for e in r.iter(NS+'rect') if e.get('fill') == '#098d90' and e.get('height') == '24']
assert len(actual) == 6
for t in range(3):
    near(float(actual[2*t].get('width')), 184*filtered[t])
    near(float(actual[2*t+1].get('width')), 184*gamma[t][0])
r = svg('pairwise-posterior', 'still')
actual = [e for e in r.iter(NS+'rect') if e.get('height') == '16' and e.get('fill') != '#e8edf4']
assert len(actual) == 4
for e,value in zip(actual, sum(xi[-1], [])):
    near(float(e.get('width')),151*value)
r = svg('baum-welch-transition', 'still')
actual = [e for e in r.iter(NS+'rect') if e.get('height') == '30' and e.get('fill') != '#e8edf4']
assert len(actual) == 4
for e,value in zip(actual,sum(updated,[])):
    near(float(e.get('width')),290*value)
for p in (ROOT/'docs/theory/paradigms/probabilistic/graphical-models').glob('hidden-markov-models*.md'):
    s=p.read_text()
    assert '<div style="width:800px">' not in s
    assert s.count('width:640px;min-width:640px;max-width:none;height:auto') == 4
    for table in xi + [counts]:
        for row in table:
            for value in row:
                assert f'{value:.6f}' in s
    for row in updated:
        for value in row:
            assert f'{value:.4f}' in s
print('HMM: 8-path likelihood, filtering, smoothing, pairwise marginals, EM counts, SVG scales and bilingual figures passed')
