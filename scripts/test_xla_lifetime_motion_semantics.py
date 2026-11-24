from pathlib import Path
import xml.etree.ElementTree as ET
import unittest

ASSETS = Path(__file__).resolve().parents[1] / "docs/assets/concept-animations"
NS = '{http://www.w3.org/2000/svg}'


def columns(stem, kind):
    root = ET.parse(ASSETS / f'{stem}-{kind}.svg').getroot()
    assert root.tag == NS+'svg' and root.get('viewBox') == '0 0 640 360'
    assert root.find(NS+'title') is not None and root.find(NS+'desc') is not None
    for el in root.iter():
        assert el.tag.split('}')[-1] not in {'script','foreignObject','image','use'}
        assert all(not k.lower().startswith('on') and 'href' not in k.lower() for k in el.attrib)
    result=[]
    for g in root.findall(NS+'g'):
        rows=[]
        for yy in (166,244):
            rows.append([t.text for t in g.findall(NS+'text') if float(t.get('y')) == yy and t.text != '—'])
        result.append(rows)
    return result


def live(ops, external):
    last={}
    for i,(reads,write) in enumerate(ops):
        for v in reads: last[v]=i
        if write not in last: last[write]=i
    defined={}; rows=[]
    for i,(reads,write) in enumerate(ops):
        assert all(r in defined or r in external for r in reads)
        if write not in external: defined[write]=i
        rows.append({v for v in defined if last.get(v,-1)>=i})
    return rows


class XlaLifetime(unittest.TestCase):
    def test_buffer(self):
        ops=[(('x',),'a'),(('a',),'b'),(('b',),'c'),(('c',),'d')]
        expected=live(ops,{'x'})
        for kind in ('motion','still'):
            actual=columns('xla-buffer-lifetime-reuse',kind)
            self.assertEqual([set(a+b) for a,b in actual],expected)
            for col in actual: self.assertTrue(all(len(slot)<=1 for slot in col))
            self.assertEqual([col[0] for col in actual],[['a'],['a'],['c'],['c']])
            self.assertEqual([col[1] for col in actual],[[],['b'],['b'],['d']])

    def test_remat(self):
        keep=[(('x',),'a'),(('a',),'b'),(('b',),'c'),((), 'idle'),(('a','c'),'y')]
        remat=[(('x',),'a1'),(('a1',),'b'),(('b',),'c'),(('x',),'a2'),(('a2','c'),'y')]
        expected=[live(keep,{'x','y','idle'}),live(remat,{'x','y'})]
        self.assertEqual([max(map(len,r)) for r in expected],[3,2])
        for kind in ('motion','still'):
            actual=columns('xla-rematerialization-liveness',kind)
            self.assertEqual(len(actual), len(keep))
            for i,rows in enumerate(actual):
                for j,vals in enumerate(rows):
                    self.assertEqual(set(vals),{v.replace('a1','a').replace('a2','a') for v in expected[j][i]})
        f=lambda x:x+1;g=lambda a:2*a;h=lambda b:b-3;k=lambda a,c:a+c
        for x in range(-5,6):
            a=f(x);c=h(g(a));y=k(a,c);del a
            self.assertEqual(y,k(f(x),c))


    def test_weighted_peak_and_slot_capacity(self):
        from itertools import product

        for a, b, c, d in product((1, 4, 10), repeat=4):
            sizes = dict(a=a, b=b, c=c, d=d)
            for kind in ('motion', 'still'):
                slots = columns('xla-buffer-lifetime-reuse', kind)
                capacity = sum(max(sizes[v] for row in slots for v in row[j]) for j in (0, 1))
                self.assertEqual(capacity, max(a, c) + max(b, d))
                states = columns('xla-rematerialization-liveness', kind)
                peaks = [max(sum(sizes[v] for v in row[j]) for row in states) for j in (0, 1)]
                self.assertEqual(peaks, [a+b+c, max(a+b, b+c, a+c)])
                self.assertEqual(peaks[0]-peaks[1], min(a, b, c))


if __name__=='__main__':
    unittest.main()
