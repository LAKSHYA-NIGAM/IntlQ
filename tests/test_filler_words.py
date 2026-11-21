import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from nlp.filler_words_analyzer import analyze_speech_fluency


class TestFillerWordsAnalyzer(unittest.TestCase):
    def test_detects_fillers_accurately(self):
        text = "Um, so basically, I was working on the API and, you know, it was like really fast."
        res = analyze_speech_fluency(text)

        self.assertGreater(res['filler_count'], 0)
        self.assertIn('um', res['fillers_breakdown'])
        self.assertIn('basically', res['fillers_breakdown'])
        self.assertIn('you know', res['fillers_breakdown'])
        self.assertIn('like', res['fillers_breakdown'])

    def test_clean_speech_excellent_fluency(self):
        text = "I architected the database schema using PostgreSQL and indexed critical query paths."
        res = analyze_speech_fluency(text)
        self.assertEqual(res['filler_count'], 0)
        self.assertEqual(res['filler_density_pct'], 0.0)
        self.assertEqual(res['fluency_rating'], 'EXCELLENT')


if __name__ == '__main__':
    unittest.main()
