import copy
import unittest
from pathlib import Path
import knowledge as k


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.data = k.load()

    def test_catalog_valid(self):
        self.assertEqual(k.validate(self.data), [])

    def test_duplicate_id_rejected(self):
        self.data['claims'].append(copy.deepcopy(self.data['claims'][0]))
        self.assertTrue(k.validate(self.data))

    def test_unknown_source_rejected(self):
        self.data['claims'][0]['evidence'][0]['source'] = 'imaginary-paper'
        self.assertTrue(k.validate(self.data))

    def test_missing_section_rejected(self):
        self.data['claims'][0]['section'] = 'Missing section'
        self.assertTrue(k.validate(self.data))

    def test_path_escape_rejected(self):
        self.data['claims'][0]['page'] = '../README.md'
        self.assertTrue(k.validate(self.data))

    def test_invalid_page_path_rejected(self):
        for value in ('\0', [], '', None):
            self.data['claims'][0]['page'] = value
            self.assertTrue(k.validate(self.data))

    def test_missing_chinese_limitation_rejected(self):
        del self.data['claims'][0]['limits']['zh-TW']
        self.assertTrue(k.validate(self.data))

    def test_invalid_date_rejected(self):
        self.data['claims'][0]['review']['checked_on'] = 'not-a-date'
        self.assertTrue(k.validate(self.data))

    def test_reproduction_cannot_be_inferred(self):
        self.data['claims'][0]['review']['independently_reproduced'] = True
        self.assertTrue(k.validate(self.data))

    def test_insecure_source_rejected(self):
        self.data['sources']['lora-v2']['url'] = 'http://example.com'
        self.assertTrue(k.validate(self.data))

    def test_malformed_fields_rejected(self):
        for field, value in [('evidence', None), ('review', None), ('summary', 'text'), ('aliases', [3])]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data['claims'][0][field] = value
                self.assertTrue(k.validate(data))

    def test_malformed_root_rejected(self):
        for value in ([], None, 'catalog', 4):
            self.assertTrue(k.validate(value))

    def test_required_catalog_metadata(self):
        for field in ('scope', 'license'):
            for value in (None, [], '', 1):
                data = copy.deepcopy(self.data)
                data[field] = value
                self.assertTrue(k.validate(data))

    def test_unhashable_source_rejected(self):
        self.data['claims'][0]['evidence'][0]['source'] = []
        self.assertTrue(k.validate(self.data))

    def test_all_locales_must_be_strings(self):
        for field in ('summary', 'limits'):
            self.data['claims'][0][field]['fr'] = 2
            self.assertTrue(k.validate(self.data))

    def test_source_fields_require_strings(self):
        for field in ('url', 'title', 'version'):
            data = copy.deepcopy(self.data)
            data['sources']['lora-v2'][field] = ['value']
            self.assertTrue(k.validate(data))

    def test_noncanonical_and_future_dates_rejected(self):
        for value in ('20261116', '2026-W47-1', '2999-01-01'):
            self.data['claims'][0]['review']['checked_on'] = value
            self.assertTrue(k.validate(self.data))

    def test_returned_candidates_keep_limits_and_sources(self):
        result = k.search(self.data, 'NF4')[0]
        self.assertEqual(result['id'], 'qlora-nf4')
        self.assertIn('zh-TW', result['limits'])
        self.assertEqual(result['evidence'][0]['url'], 'https://arxiv.org/abs/2305.14314v1')
        self.assertFalse(result['review']['independently_reproduced'])

    def test_search_not_an_answer_generator(self):
        self.assertEqual(k.search(self.data, 'banana cake'), [])
        self.assertEqual(k.search(self.data, ''), [])
        self.assertEqual(k.search(self.data, 'the and or'), [])

    def test_fixture_retrieval_smoke(self):
        result = k.evaluate(self.data, k.load(k.CASES))
        self.assertEqual(result['passed'], result['total'], result)

    def test_get_record_does_not_mutate_source(self):
        before = copy.deepcopy(self.data)
        k.record(self.data, self.data['claims'][0])
        self.assertEqual(before, self.data)


if __name__ == '__main__':
    unittest.main()
