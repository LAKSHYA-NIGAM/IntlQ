import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from nlp.technical_taxonomy_mapper import map_technical_taxonomy


class TestTaxonomyMapper(unittest.TestCase):
    def test_extracts_multi_category_skills(self):
        text = "I have 3 years of experience writing Python and TypeScript with FastAPI, PostgreSQL, and deploying via Docker."
        res = map_technical_taxonomy(text)

        self.assertIn('python', res['categories']['languages'])
        self.assertIn('typescript', res['categories']['languages'])
        self.assertIn('fastapi', res['categories']['frameworks'])
        self.assertIn('postgresql', res['categories']['databases'])
        self.assertIn('docker', res['categories']['devops'])
        self.assertEqual(res['total_unique_skills'], 5)

    def test_empty_text(self):
        res = map_technical_taxonomy("")
        self.assertEqual(res['total_unique_skills'], 0)


if __name__ == '__main__':
    unittest.main()
