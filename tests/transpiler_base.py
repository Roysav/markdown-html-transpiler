# tests/transpiler_base.py
import unittest
from md_html.transpiler_base import tokenizer


class TestIndividualRule(unittest.TestCase):
    """
    Testing for making individual token rules and tokenizing text correctly
    """
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

    def test_should_not_tokenized(self):
        cases = (
            ('Hello World', 1),
            (' 143', 0),
        )
        for text, start in cases:
            with self.subTest(text=text):
                self.assertFalse(self.INTEGER.tokenize(text, start))


if __name__ == '__main__':
    unittest.main()
