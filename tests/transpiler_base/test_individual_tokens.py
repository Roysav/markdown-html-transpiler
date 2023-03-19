# tests/transpiler_base/test_individual_tokens.py
import unittest
from md_html.transpiler_base import tokenizer


"""
Testing for making individual token rules and tokenizing text correctly
"""


class TestIntegerRegexRule(unittest.TestCase):
    class INTEGER(tokenizer.RegexRule):
        match = r'[1-9]*[0-9]'

    def test_should_tokenized(self):
        cases = (
            ('1234', 0),
            (' 143', 1),
        )
        for text, start in cases:
            with self.subTest(text=text):
                self.assertTrue(self.INTEGER.tokenize(text, start))

if __name__ == '__main__':
    unittest.main()
