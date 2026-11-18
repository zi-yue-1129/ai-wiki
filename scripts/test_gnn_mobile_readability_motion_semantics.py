"""Prevent 640px GNN labels shrinking to unreadable text on mobile."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class Tags(HTMLParser):
    def __init__(self):super().__init__();self.tags=[]
    def handle_starttag(self,name,attrs):self.tags.append((name,dict(attrs)))

class GnnReadableFigures(unittest.TestCase):
    def test_bilingual_nested_focusable_natural_size_frames(self):
        for name in ['gin','graphsage']:
            for lang in ['', '.zh-TW']:
                path=ROOT/f'docs/theory/models/gnn/message-passing/{name}/index{lang}.md'
                parser=Tags();parser.feed(path.read_text())
                frames=[a for n,a in parser.tags if n=='div' and a.get('class')=='concept-motion-scroll']
                self.assertEqual(len(frames),1)
                self.assertEqual(frames[0]['tabindex'],'0');self.assertEqual(frames[0]['role'],'region')
                self.assertEqual(frames[0]['style'],'width:100%;overflow-x:auto')
                self.assertTrue(frames[0]['aria-label'])
                self.assertIn(('div',{'style':'width:640px'}),parser.tags)
                images=[a for n,a in parser.tags if n=='img' and 'data-motion-src' in a]
                self.assertEqual(len(images),1)
                image=images[0]
                self.assertIn('data-source-asset-urls',image)
                self.assertIn('min-width:640px;max-width:none',image['style'])
                self.assertEqual((image['width'],image['height']),('640','360'))
                for attr in ['src','data-still-src','data-motion-src']:
                    self.assertTrue((path.parent/image[attr]).resolve().is_file())

if __name__=='__main__':unittest.main()
